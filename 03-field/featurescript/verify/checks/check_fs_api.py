# -*- coding: utf-8 -*-
"""
FeatureScript API / language audit of the SUMMIT PUSH Feature Studio (SummitPushField.fs).

Onshape itself is unreachable, so this module is the compile check: it reads the Feature
Studio against the FeatureScript standard library (v2960) and encodes, as executable
assertions, what a reading of the std source establishes:

  A. build.py: dialect lint + api_check re-run in memory; assembled output == committed file;
     version header.
  B. every std name the Studio uses is exported through onshape/std/geometry.fs (the only
     import) - build.py's api_check only asks whether it exists in *some* std file.
  C. every definition-map field passed to a std operation/evaluator/constructor is one the std
     documents (or, for opRevolve, one the std revolve feature itself passes).
  D. specific API facts (units, opShell hollow, union survivor rule, status reporting ids,
     try silent/catch, bSplineSurface knots, qSketchRegion, evBox3d cSys ...).
  E. FeatureScript block scoping (the Python twin is function-scoped and cannot see it):
     unresolved names, nested redeclarations, assignments to const; and the Feature Studio
     editor's own warnings (verify/onshape_lint.py): unused declarations, locals set but not used.
  F. Id rules from std context.fs: characters, no duplicate operation ids, and "each Id
     (including parents) must refer to a contiguous region of operations" - checked on the
     real operation order by running the part code against a logging stub kernel.
  G. defineFeature: every UI parameter has a "Default" and a defaults-map entry that agree.
  H. selfCheck never asks evDistance for a point inside a solid (the one evDistance
     semantic the std does not document).

Only the std source is used as the reference; no numbers are taken from the part code.
"""
import glob
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VERIFY = os.path.dirname(HERE)
ROOT = os.path.dirname(VERIFY)                       # 03-field/featurescript
SRC = os.path.join(ROOT, "src")
STD_CANDIDATES = [
    os.environ.get("FS_STD", ""),
    os.path.join(ROOT, ".fs-std"),
]
FS_VERSION = "2960"

sys.path.insert(0, VERIFY)


# =====================================================================================
# helpers
# =====================================================================================
def _std_dir():
    for c in STD_CANDIDATES:
        if c and os.path.isfile(os.path.join(c, "geometry.fs")):
            return c
    return None


def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def _load_build():
    spec = importlib.util.spec_from_file_location("fs_build", os.path.join(ROOT, "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _src_files():
    return sorted(glob.glob(os.path.join(SRC, "*.fs")))


# ---- tokenizer -----------------------------------------------------------------------
_TOK = re.compile(r"""
    (?P<ws>\s+)
  | (?P<lc>//[^\n]*)
  | (?P<bc>/\*.*?\*/)
  | (?P<str>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<num>\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)
  | (?P<id>[A-Za-z_]\w*)
  | (?P<op>\+=|-=|\*=|/=|==|!=|<=|>=|&&|\|\||->|[-+*/%^~<>=!?:;,.()\[\]{}@])
""", re.S | re.X)


def tokenize(text):
    out, line, pos = [], 1, 0
    while pos < len(text):
        m = _TOK.match(text, pos)
        if not m:
            raise ValueError("cannot tokenize at line %d: %r" % (line, text[pos:pos + 20]))
        kind = m.lastgroup
        val = m.group(kind)
        if kind not in ("ws", "lc", "bc"):
            out.append((kind, val, line))
        line += val.count("\n")
        pos = m.end()
    return out


def _match(tokens, i, open_, close):
    """Index of the token closing tokens[i] (which is `open_`)."""
    d = 0
    for j in range(i, len(tokens)):
        v = tokens[j][1]
        if tokens[j][0] == "op" and v == open_:
            d += 1
        elif tokens[j][0] == "op" and v == close:
            d -= 1
            if d == 0:
                return j
    raise ValueError("unbalanced %s at line %d" % (open_, tokens[i][2]))


# ---- std index ---------------------------------------------------------------------------
def std_reachable(std):
    """Names exported through onshape/std/geometry.fs (transitively via `export import`)."""
    names, seen, todo = {}, set(), ["geometry.fs"]
    while todo:
        f = todo.pop()
        if f in seen:
            continue
        seen.add(f)
        p = os.path.join(std, f)
        if not os.path.exists(p):
            continue
        t = _read(p)
        todo += re.findall(r'^export\s+import\s*\(\s*path\s*:\s*"onshape/std/([\w.]+)"', t, re.M)
        for n in re.findall(r"^export\s+(?:const|function|predicate|type|enum|operator)\s+(\w+)", t, re.M):
            names.setdefault(n, f)
    return names, seen


def std_doc_fields(std, fname, func):
    """@field names in the doc comment immediately preceding `func`'s definition."""
    t = _read(os.path.join(std, fname))
    m = re.search(r"/\*\*((?:(?!\*/).)*?)\*/\s*(?:/\*[^*]*\*/\s*)?export\s+(?:const|function)\s+%s\b" % re.escape(func), t, re.S)
    if not m:
        return None
    return set(re.findall(r"@field\s+(\w+)", m.group(1)))


def std_revolve_bound_fields(std):
    """Fields the std revolve feature writes into the map it hands to opRevolve."""
    t = _read(os.path.join(std, "revolve.fs"))
    return set(re.findall(r"definition\.(\w+)\s*=", t))


# =====================================================================================
# E. scope analysis (FeatureScript block scoping)
# =====================================================================================
FS_KEYWORDS = {"if", "else", "for", "while", "do", "return", "function", "var", "const", "in",
               "is", "new", "export", "import", "annotation", "precondition", "predicate",
               "type", "typecheck", "enum", "operator", "try", "catch", "throw", "silent",
               "switch", "returns", "as", "break", "continue", "true", "false", "undefined",
               "FeatureScript"}
MAP_OPENERS = {"=", "(", ",", ":", "[", "return", "?", "annotation", "||", "&&", "!", "+", "~"}


def top_level_names(files):
    names = {}
    for f in files:
        toks = tokenize(_read(f))
        depth = 0
        for i, (k, v, ln) in enumerate(toks):
            if k == "op" and v in "{([":
                depth += 1
            elif k == "op" and v in "})]":
                depth -= 1
            elif depth == 0 and k == "id" and v in ("function", "const", "enum") and i + 1 < len(toks) and toks[i + 1][0] == "id":
                names.setdefault(toks[i + 1][1], []).append("%s:%d" % (os.path.basename(f), ln))
    return names


def scope_analyse(path, known):
    """Return (unresolved, redeclared, const_assign) lists of strings for one file."""
    toks = tokenize(_read(path))
    fn = os.path.basename(path)
    unresolved, redecl, const_assign = [], [], []
    frames = []   # dicts: kind in {"func","for","catch","block","map"}, names {n: [kind, line, uses]}

    def lookup(name):
        for fr in reversed(frames):
            if name in fr["names"]:
                return fr["names"][name]
        return None

    def declare(name, kind, ln, target=None):
        fr = target
        if fr is None:
            for x in reversed(frames):
                if x["kind"] != "map":
                    fr = x
                    break
        if fr is None:
            return   # top level: pre-collected
        # enclosing local declaration of the same name (up to and including the function frame)
        for x in reversed(frames):
            if name in x["names"] and x is not fr:
                redecl.append("%s:%d '%s' redeclared (outer declaration at line %d)" % (fn, ln, name, x["names"][name][1]))
                break
            if x["kind"] == "func" and x is not fr:
                break
        if name in fr["names"]:
            redecl.append("%s:%d '%s' declared twice in one scope" % (fn, ln, name))
        fr["names"][name] = [kind, ln, 0]

    def pop_headers(i):
        # after a block closes: pop for/catch headers, and function headers unless another block follows
        while frames and frames[-1]["kind"] in ("for", "catch", "func"):
            nxt = toks[i + 1][1] if i + 1 < len(toks) else ""
            if frames[-1]["kind"] == "func" and nxt in ("{",):
                break
            frames.pop()

    i = 0
    n = len(toks)
    prev = None
    while i < n:
        k, v, ln = toks[i]
        if k == "id" and v == "FeatureScript":
            while toks[i][1] != ";":
                i += 1
            prev = None
            i += 1
            continue
        if k == "id" and v == "import" and not frames:
            while toks[i][1] != ";":
                i += 1
            i += 1
            continue
        if k == "id" and v == "annotation" and i + 1 < n and toks[i + 1][1] == "{":
            i = _match(toks, i + 1, "{", "}") + 1
            prev = ("op", "}", ln)
            continue
        if k == "id" and v == "enum":
            j = i
            while toks[j][1] != "{":
                j += 1
            i = _match(toks, j, "{", "}") + 1
            prev = ("op", "}", ln)
            continue
        if k == "id" and v == "function":
            j = i + 1
            if toks[j][0] == "id":
                j += 1
            if toks[j][1] != "(":
                raise ValueError("%s:%d function header" % (fn, ln))
            e = _match(toks, j, "(", ")")
            fr = {"kind": "func", "names": {}}
            # params: NAME [is TYPE] separated by commas at depth 0
            depth, expect = 0, True
            for t in toks[j + 1:e]:
                if t[1] in "([{":
                    depth += 1
                elif t[1] in ")]}":
                    depth -= 1
                elif t[1] == "," and depth == 0:
                    expect = True
                elif expect and t[0] == "id":
                    fr["names"][t[1]] = ["param", t[2], 0]
                    expect = False
            frames.append(fr)
            i = e + 1
            if i < n and toks[i][1] == "returns":
                i += 2
            prev = ("op", ")", ln)
            continue
        if k == "id" and v == "for" and toks[i + 1][1] == "(":
            fr = {"kind": "for", "names": {}}
            frames.append(fr)
            if toks[i + 2][1] == "var":
                declare(toks[i + 3][1], "loopvar", toks[i + 3][2], target=fr)
                i += 4
            else:
                i += 2
            prev = ("op", "(", ln)
            continue
        if k == "id" and v == "catch" and toks[i + 1][1] == "(":
            fr = {"kind": "catch", "names": {}}
            frames.append(fr)
            declare(toks[i + 2][1], "catchvar", toks[i + 2][2], target=fr)
            i += 4
            prev = ("op", ")", ln)
            continue
        if k == "id" and v in ("var", "const") and toks[i + 1][0] == "id":
            declare(toks[i + 1][1], v, ln)
            i += 2
            prev = ("id", "decl", ln)
            continue
        if k == "op" and v == "{":
            is_map = prev is not None and (prev[1] in MAP_OPENERS)
            frames.append({"kind": "map" if is_map else "block", "names": {}})
        elif k == "op" and v == "}":
            while frames and frames[-1]["kind"] in ("for", "catch", "func"):
                # a header frame whose block never opened (should not happen)
                frames.pop()
            if frames:
                frames.pop()
            pop_headers(i)
        elif k == "id" and v not in FS_KEYWORDS:
            after_dot = prev is not None and prev[1] == "."
            after_type = prev is not None and prev[1] in ("is", "returns", "as")
            is_key = (prev is not None and prev[1] in ("{", ",") and i + 1 < n and toks[i + 1][1] == ":"
                      and frames and frames[-1]["kind"] == "map")
            if not (after_dot or after_type or is_key):
                d = lookup(v)
                if d is not None:
                    d[2] += 1
                    nxt = toks[i + 1][1] if i + 1 < n else ""
                    if d[0] == "const" and nxt in ("=", "+=", "-=", "*=", "/=") :
                        const_assign.append("%s:%d assignment to const '%s'" % (fn, ln, v))
                    if d[0] == "const" and nxt == "[":
                        e = _match(toks, i + 1, "[", "]")
                        if e + 1 < n and toks[e + 1][1] in ("=", "+=", "-="):
                            const_assign.append("%s:%d element assignment to const '%s'" % (fn, ln, v))
                elif v not in known:
                    unresolved.append("%s:%d '%s'" % (fn, ln, v))
        prev = (k, v, ln)
        i += 1
    return unresolved, redecl, const_assign


# =====================================================================================
# F. Id rules: logging stub kernel
# =====================================================================================
ID_RE = re.compile(r"^\*?[a-zA-Z0-9_.+/\-]+$")    # std string.fs REGEX_ID_COMPONENT

# Operation ids each kernel helper issues, relative to the id it is given, as read from
# src/10_kernel.fs (verified against the source by kernel_op_suffixes()).
KOPS = {
    "mkPrismProfile": ["sk", "ex", "dl"],
    "mkRevolve": ["sk", "rv", "dl"],
    "mkPillowBox": ["face0n", "face0p", "face1n", "face1p", "face2n", "face2p", "ex", "dl"],
    "bSubtract": [None], "bUnion": [None], "bDelete": [None], "shellHollow": [None],
    "filletAt": [None], "copyBody": [None], "removeSlivers": [None], "groupParts": [None],
    "tagDecal": ["sk", "sp", "dl"],
}


def kernel_functions(text):
    """{name: body text} for top-level functions of a FeatureScript source."""
    out = {}
    for m in re.finditer(r"^function\s+(\w+)\s*\(", text, re.M):
        start = text.index("{", m.end())
        d = 0
        for j in range(start, len(text)):
            if text[j] == "{":
                d += 1
            elif text[j] == "}":
                d -= 1
                if d == 0:
                    out[m.group(1)] = text[start:j + 1]
                    break
    return out


def kernel_op_suffixes(ktext):
    """Static reading of 10_kernel.fs: the id suffixes each helper passes to std operations."""
    bodies = kernel_functions(ktext)
    got = {}
    for name, body in bodies.items():
        b = re.sub(r"//[^\n]*", "", body)
        ids = []
        # id + "x" passed as the operation id of an op*/newSketchOnPlane call, or via skId/sid
        for m in re.finditer(r"\b(op\w+|newSketchOnPlane)\s*\(\s*context\s*,\s*([^,]+),", b):
            ids.append(m.group(2).strip())
        for m in re.finditer(r"\b(filletAt|mkPrismProfile)\s*\(\s*context\s*,\s*([^,]+),", b):
            ids.append("->" + m.group(1) + ":" + m.group(2).strip())
        got[name] = ids
    return got, bodies


class StubCtx:
    def __init__(self):
        self.ops = []            # operation Ids in order (tuples)
        self.bodies = []         # [creator Id tuple, alive]
        self.errors = []
        self.queries = 0

    # ---- bodies: [creator Id, alive, body it was merged into (union) or None] -------------
    def create(self, oid):
        self.bodies.append([tuple(oid), True, None])

    def live(self, ids):
        out = []
        for i in ids:
            i = tuple(i)
            for b in self.bodies:
                if b[1] and b[0][:len(i)] == i and all(b is not x for x in out):
                    out.append(b)
        return out

    def need(self, what, ids):
        """kQ(ids) must be non-empty, and every id in it must still reach its geometry: either
        its own body, or (after a union) the surviving body, which the same query must match."""
        self.queries += 1
        whole = self.live(ids)
        if not whole:
            self.errors.append("%s: kQ(%s) is empty" % (what, ", ".join("/".join(i) for i in ids)))
            return
        for i in ids:
            i = tuple(i)
            if self.live([i]):
                continue
            merged = []
            for b in self.bodies:
                if b[0][:len(i)] == i and not b[1] and b[2] is not None:
                    s = b[2]
                    while s[2] is not None and not s[1]:
                        s = s[2]
                    merged.append(s)
            if merged and all(any(s is w for w in whole) for s in merged):
                continue
            self.errors.append("%s: qCreatedBy(%s) is empty and its geometry is not in the query" % (what, "/".join(i)))

    def op(self, base, suffixes):
        for s in suffixes:
            self.ops.append(tuple(base) if s is None else tuple(base) + (s,))


def make_stub_ns(K, R):
    ns, _ = R.load_part_code()
    Id = K.Id

    def mkPrismProfile(context, id, F, pl, loops, d0, d1):
        if not d1 > d0:
            context.errors.append("mkPrismProfile d1 <= d0 at %s" % (id,))
        context.op(id, KOPS["mkPrismProfile"])
        context.create(id + "ex")

    def mkPrism(context, id, F, pl, pts, d0, d1):
        mkPrismProfile(context, id, F, pl, [pts], d0, d1)

    def mkPrismHoles(context, id, F, pl, outer, holes, d0, d1):
        mkPrismProfile(context, id, F, pl, [outer] + list(holes), d0, d1)

    def mkCyl(context, id, F, pl, c, r, d0, d1):
        mkPrismProfile(context, id, F, pl, [], d0, d1)

    def mkRevolve(context, id, F, pl, loop):
        context.op(id, KOPS["mkRevolve"])
        context.create(id + "rv")

    def mkPillowBox(context, id, F, h, crown):
        context.op(id, KOPS["mkPillowBox"])
        context.create(id + "ex")

    def bSubtract(context, id, targets, tools, keepTools):
        context.need("bSubtract targets %s" % (id,), targets)
        context.need("bSubtract tools %s" % (id,), tools)
        context.op(id, KOPS["bSubtract"])
        if not keepTools:
            for b in context.live(tools):
                b[1] = False

    def bUnion(context, id, bodies):
        context.need("bUnion %s" % (id,), bodies)
        context.op(id, KOPS["bUnion"])
        # std opBoolean: "the identity of the tool that appears earliest in the query is preserved"
        lv = context.live(bodies)
        for b in lv[1:]:
            b[1] = False
            b[2] = lv[0]

    def bDelete(context, id, bodies):
        context.need("bDelete %s" % (id,), bodies)
        context.op(id, KOPS["bDelete"])
        for b in context.live(bodies):
            b[1] = False

    def shellHollow(context, id, bodies, t):
        context.need("shellHollow %s" % (id,), bodies)
        context.op(id, KOPS["shellHollow"])

    def filletAt(context, id, bodies, F, pts, r):
        context.need("filletAt %s" % (id,), bodies)
        context.op(id, KOPS["filletAt"])

    def softFilletAt(context, id, bodies, F, pts, r, label):
        filletAt(context, id, bodies, F, pts, r)

    def removeSlivers(context, id, bodies, minVolume):
        # the delete runs only when a sliver exists; record it so the Id order is checked either way
        context.need("removeSlivers %s" % (id,), bodies)
        context.op(id, KOPS["removeSlivers"])

    def groupParts(context, id, bodies, name):
        context.need("groupParts %r" % name, bodies)
        context.op(id, KOPS["groupParts"])

    def numberSharedNames(context, bodies):
        context.need("numberSharedNames", bodies)

    def kWarn(context, id, message):
        pass

    def copyBody(context, id, src, F):
        context.need("copyBody %s" % (id,), src)
        context.op(id, KOPS["copyBody"])
        context.create(id)

    def styleBody(context, bodies, name, rgb, alpha, mat):
        context.need("styleBody %r" % name, bodies)

    def nameBody(context, bodies, name):
        context.need("nameBody %r" % name, bodies)

    def styleFacesAt(context, bodies, F, pts, rgb, alpha):
        context.need("styleFacesAt", bodies)

    def massBody(context, bodies, matName, massLb):
        context.need("massBody %r" % matName, bodies)
        return 1.0

    def tagDecal(context, id, bodies, F, pl, black, cells, s, rgb):
        context.need("tagDecal %s" % (id,), bodies)
        context.op(id, KOPS["tagDecal"])

    def measureBox(context, bodies, F):
        context.need("measureBox", bodies)
        return [0.0] * 6

    def measureVolume(context, bodies):
        context.need("measureVolume", bodies)
        return 0.0

    def measureDistToPoint(context, bodies, F, p):
        context.need("measureDistToPoint", bodies)
        return 0.0

    def measureDist(context, a, b):
        context.need("measureDist", a)
        context.need("measureDist", b)
        return 0.0

    def countBodies(context, bodies):
        context.need("countBodies", bodies)
        return 0

    def decalApplied(context, bodies):
        context.need("decalApplied", bodies)
        return 1

    for f in (mkPrismProfile, mkPrism, mkPrismHoles, mkCyl, mkRevolve, mkPillowBox, bSubtract,
              bUnion, bDelete, removeSlivers, shellHollow, filletAt, softFilletAt, copyBody,
              styleBody, nameBody, numberSharedNames, styleFacesAt, massBody, tagDecal, kWarn, groupParts,
              decalApplied, measureBox, measureVolume, measureDistToPoint, measureDist, countBodies):
        ns[f.__name__] = f
    return ns, Id


def contiguity_errors(ops):
    first, last, count = {}, {}, {}
    for k, oid in enumerate(ops):
        for L in range(1, len(oid) + 1):
            p = oid[:L]
            if p not in first:
                first[p] = k
            last[p] = k
            count[p] = count.get(p, 0) + 1
    bad = []
    for p in first:
        if last[p] - first[p] + 1 != count[p]:
            # find the first foreign op inside the span
            for k in range(first[p], last[p] + 1):
                if ops[k][:len(p)] != p:
                    bad.append("%s interrupted by %s" % ("/".join(p), "/".join(ops[k])))
                    break
    return bad


def contains_point_audit(K):
    """Rebuild the field with filletAt / styleFacesAt wrapped, and measure how far each
    qContainsPoint probe point is from the nearest edge (fillets) or face (face styling), and how
    many entities lie within Onshape's TOLERANCE.zeroLength (1e-8 m) of it.  The twin itself
    accepts 1e-5 in (2.5e-7 m), 25x looser than Onshape."""
    from inspect_field import Field
    tol_in = 1e-8 / 0.0254
    rec = []
    of, osf = K.filletAt, K.styleFacesAt

    def near(shapes, wp, kind):
        v = K.BRepBuilderAPI_MakeVertex(K._gp(wp)).Vertex()
        best, n = float("inf"), 0
        for s in shapes:
            exp = K.TopExp_Explorer(s, kind)
            seen = []
            while exp.More():
                e = exp.Current()
                if not any(e.IsSame(x) for x in seen):
                    seen.append(e)
                    d = K.BRepExtrema_DistShapeShape(v, e).Value()
                    best = min(best, d)
                    if d < tol_in:
                        n += 1
                exp.Next()
        return best, n

    def filletAt(context, id, bodies, F, pts, r, **kw):
        for p in pts:
            d, n = near(context.solids_for(bodies), F.pt(p), K.TopAbs_EDGE)
            rec.append(("edge", "/".join(id), p, d, n))
        return of(context, id, bodies, F, pts, r, **kw)

    def styleFacesAt(context, bodies, F, pts, rgb, alpha):
        for p in pts:
            d, n = near(context.solids_for(bodies), F.pt(p), K.TopAbs_FACE)
            rec.append(("face", "/".join(bodies[0]), p, d, n))
        return osf(context, bodies, F, pts, rgb, alpha)

    K.filletAt, K.styleFacesAt = filletAt, styleFacesAt
    try:
        Field()
    finally:
        K.filletAt, K.styleFacesAt = of, osf
    return rec, tol_in


def id_rule_run(K, R, opts, game_piece=None):
    ns, Id = make_stub_ns(K, R)
    ctx = StubCtx()
    fid = Id(("FsumPushField1",))
    if game_piece is None:
        ns["buildField"](ctx, fid, opts)
        ns["selfCheck"](ctx, fid, opts)
    else:
        kind, rest = game_piece
        F = ns["restFrame"](kind, 0, 0, 0) if rest else ns["worldFrame"]()
        ns["buildPiece"](ctx, fid + "piece", kind, F)
    dup = sorted({"/".join(o) for o in ctx.ops if ctx.ops.count(o) > 1})
    badch = sorted({c for o in ctx.ops for c in o if not ID_RE.match(c) or c.startswith(".")})
    return ctx, dup, badch, contiguity_errors(ctx.ops)


# =====================================================================================
# the checks
# =====================================================================================
def run(f):
    out = []

    def ck(label, ok, detail=""):
        out.append((label, bool(ok), detail))

    std = _std_dir()
    ck("A0 FeatureScript std library v%s available" % FS_VERSION, std is not None, str(std))
    if std is None:
        return out
    vnum = _read(os.path.join(std, "featurescriptversionnumber.gen.fs"))
    ck("A0 std is at V%s (the version the Studio targets)" % FS_VERSION,
       re.search(r"FeatureScriptVersionNumberCurrent is FeatureScriptVersionNumber = FeatureScriptVersionNumber\.V%s_" % FS_VERSION, vnum) is not None,
       "current version enum in featurescriptversionnumber.gen.fs")

    # ---------------------------------------------------------------- A. build.py
    B = _load_build()
    files = _src_files()
    lint_errs = B.lint_parts(files)
    ck("A1 dialect lint (build.py lint_parts)", not lint_errs, "; ".join(lint_errs[:5]))
    code = B.assemble(files)
    api_errs = B.api_check(code, std)
    ck("A2 build.py api_check against std v%s" % FS_VERSION, not api_errs, "; ".join(api_errs[:8]) or "0 errors")
    regen = B.regen_check(code)
    ck("A2b no std call that fails while a feature regenerates (getProperty)", not regen, "; ".join(regen) or "none")
    committed = _read(os.path.join(ROOT, "SummitPushField.fs"))
    ck("A3 committed SummitPushField.fs == assembly of src/*.fs", committed == code,
       "differs" if committed != code else "identical (%d lines)" % code.count("\n"))
    lines = code.splitlines()
    ck("A4 first line is 'FeatureScript %s;'" % FS_VERSION, lines[0].strip() == "FeatureScript %s;" % FS_VERSION, lines[0])
    ck("A5 imports onshape/std/geometry.fs version \"%s.0\"" % FS_VERSION,
       re.search(r'^import\(path : "onshape/std/geometry\.fs", version : "%s\.0"\);' % FS_VERSION, code, re.M) is not None, lines[1])
    ck("A6 exactly one import", len(re.findall(r"^\s*(?:export\s+)?import\s*\(", code, re.M)) == 1, "")

    # ---------------------------------------------------------------- B. reachability
    reach, reach_files = std_reachable(std)
    stripped = B.strip_comments_and_strings(code)
    local = set(re.findall(r"^(?:export\s+)?(?:function|const|enum)\s+(\w+)", stripped, re.M))
    params = set()
    for m in re.finditer(r"function\s*\w*\s*\(([^)]*)\)", stripped):
        for p in m.group(1).split(","):
            p = p.strip()
            if p:
                params.add(p.split()[0])
    idents = set(re.findall(r"(?<![\.\w])([A-Za-z_]\w*)", stripped))
    all_std = set()
    for fp in glob.glob(os.path.join(std, "*.fs")):
        all_std |= set(re.findall(r"^export\s+(?:const|function|predicate|type|enum|operator)\s+(\w+)", _read(fp), re.M))
    used_std = sorted(n for n in idents if n in all_std and n not in local)
    unreach = [n for n in used_std if n not in reach]
    ck("B1 every std name used is exported through geometry.fs (%d names)" % len(used_std), not unreach,
       ", ".join(unreach) or "all reachable")
    coll = sorted(n for n in local if n in reach)
    ck("B2 no Feature Studio top-level name collides with a reachable std export", not coll, ", ".join(coll))
    tl = top_level_names(files)
    dups = {k: v for k, v in tl.items() if len(v) > 1}
    ck("B3 no duplicate top-level function/const/enum names across src/*.fs", not dups,
       "; ".join("%s at %s" % (k, ",".join(v)) for k, v in dups.items()))

    # ---------------------------------------------------------------- C. definition-map fields
    ktext = _read(os.path.join(SRC, "10_kernel.fs"))
    doc = {
        "opExtrude": ("geomOperations.fs", "opExtrude"), "opRevolve": ("geomOperations.fs", "opRevolve"),
        "opBoolean": ("geomOperations.fs", "opBoolean"), "opShell": ("geomOperations.fs", "opShell"),
        "opEnclose": ("geomOperations.fs", "opEnclose"), "opFillet": ("geomOperations.fs", "opFillet"),
        "opPattern": ("geomOperations.fs", "opPattern"), "opSplitFace": ("geomOperations.fs", "opSplitFace"),
        "opDeleteBodies": ("geomOperations.fs", "opDeleteBodies"),
        "opCreateBSplineSurface": ("geomOperations.fs", "opCreateBSplineSurface"),
        "evBox3d": ("evaluate.fs", "evBox3d"), "evDistance": ("evaluate.fs", "evDistance"),
        "evVolume": ("evaluate.fs", "evVolume"), "setProperty": ("properties.fs", "setProperty"),
        "newSketchOnPlane": ("sketch.fs", "newSketchOnPlane"), "skLineSegment": ("sketch.fs", "skLineSegment"),
        "skArc": ("sketch.fs", "skArc"), "skCircle": ("sketch.fs", "skCircle"),
        "bSplineSurface": ("surfaceGeometry.fs", "bSplineSurface"),
    }
    rev_extra = std_revolve_bound_fields(std)
    kt = tokenize(ktext)
    for fname, (sf, sfun) in doc.items():
        fields = std_doc_fields(std, sf, sfun)
        if fields is None:
            ck("C %s documented in std %s" % (fname, sf), False, "doc comment not found")
            continue
        used = set()
        ncalls = 0
        for i, t in enumerate(kt):
            if t[0] == "id" and t[1] == fname and i + 1 < len(kt) and kt[i + 1][1] == "(":
                ncalls += 1
                e = _match(kt, i + 1, "(", ")")
                # the definition map: first "{" argument at depth 1 of the call
                d = 0
                for j in range(i + 1, e):
                    if kt[j][1] in "([":
                        d += 1
                    elif kt[j][1] in ")]":
                        d -= 1
                    elif kt[j][1] == "{" and d == 1:
                        me = _match(kt, j, "{", "}")
                        dd = 0
                        for q in range(j + 1, me):
                            if kt[q][1] in "([{":
                                dd += 1
                            elif kt[q][1] in ")]}":
                                dd -= 1
                            elif dd == 0 and kt[q][0] == "str" and kt[q + 1][1] == ":":
                                used.add(kt[q][1][1:-1])
                        break
        if ncalls == 0:
            continue
        extra = used - fields
        if fname == "opRevolve":
            undocumented = sorted(extra)
            extra = extra - rev_extra
            ck("C opRevolve fields are ones std revolve.fs itself passes to opRevolve", not extra,
               "unknown: %s" % sorted(extra) if extra else "bounds form %s" % undocumented)
            # the opRevolve doc comment still lists the older angleForward/angleBack form; at this
            # version std revolve.fs passes the bounds form and treats angleBack as the pre-bounds marker
            out.append(("C (info) opRevolve uses the bounds form std revolve.fs passes, not the doc comment's %s"
                        % sorted(fields - {"entities", "axis"}), True, "kernel passes %s" % undocumented))
            continue
        ck("C %s: every definition field is documented (%d call(s))" % (fname, ncalls), not extra,
           ("undocumented: %s" % sorted(extra)) if extra else "fields %s" % sorted(used))

    # ---------------------------------------------------------------- D. specific API facts
    geo = _read(os.path.join(std, "geomOperations.fs"))
    ck("D1 opBoolean UNION keeps the identity of the earliest tool in the query (std doc)",
       "the identity of the tool that appears earliest in the query is preserved" in geo, "geomOperations.fs opBoolean doc")
    kick_union = re.search(r'bUnion\(context, id \+ "kickJoin", \[id \+ "kickV", id \+ "kickH"\]\)', _read(os.path.join(SRC, "41_crag.fs")))
    later_kickV = re.search(r'bSubtract\(context, id \+ "towerGroove".*id \+ "kickV"', _read(os.path.join(SRC, "41_crag.fs")))
    ck("D2 kick-guard: the body queried after the union (kickV) is the first tool, so it survives in Onshape",
       kick_union is not None and later_kickV is not None, "41_crag.fs kickJoin / towerGroove")
    shell_fs = _read(os.path.join(std, "shell.fs"))
    ck("D3 opShell on a body with negative thickness hollows inward, no faces removed (std shell.fs 'Hollow')",
       "definition.entities = qEntityFilter(definition.parts, EntityType.BODY)" in shell_fs
       and "definition.thickness = -definition.thickness" in shell_fs
       and re.search(r'opShell\(context, id, \{ "entities" : kQ\(bodies\), "thickness" : -t \* inch \}\)', ktext) is not None,
       "kernel shellHollow vs std shell.fs isHollow path")
    enc = _read(os.path.join(std, "enclose.fs"))
    ck("D4 opEnclose does not consume its input sheets (std enclose.fs deletes them itself), so the kernel's opDeleteBodies has work to do",
       "opDeleteBodies(context, id + \"delete\"" in enc and "keepTools" in enc, "enclose.fs")
    ck("D5 bSplineSurface: knots optional (padded, clamped) and control-point grid >= degree+1",
       "definition.uKnots is undefined || definition.uKnots is KnotArray" in _read(os.path.join(std, "surfaceGeometry.fs"))
       and '"uDegree" : 2' in ktext and "uKnots" not in ktext and re.search(r"for \(var i = 0; i < 3; i \+= 1\)", ktext) is not None,
       "3x3 net, degree 2, no knots -> Bezier patch")
    props = _read(os.path.join(std, "properties.fs"))
    ck("D6 setProperty APPEARANCE is allowed on faces", "Only\n * `APPEARANCE` and `NAME` properties are supported for faces" in props, "properties.fs")
    ck("D7 material() density must carry DENSITY_UNITS: kernel uses kg/m^3 and lb/volume",
       "precondition density.unit == DENSITY_UNITS" in props
       and 'mat["density"] * kilogram / meter ^ 3' in ktext and "massLb * pound / vol" in ktext
       and re.search(r'^export const DENSITY_UNITS = \{ "kilogram" : 1, "meter" : -3 \}', _read(os.path.join(std, "units.fs")), re.M) is not None,
       "evVolume returns meter^3; pound is a MASS_UNITS value")
    ev = _read(os.path.join(std, "evaluate.fs"))
    ck("D8 evBox3d takes cSys and tight; evVolume returns ValueWithUnits",
       "arg.cSys == undefined || arg.cSys is CoordSystem" in ev and "export function evVolume(context is Context, arg is map) returns ValueWithUnits" in ev,
       "evaluate.fs")
    ck("D9 evDistance accepts a 3D length point as a side",
       "A query, or a point (3D Length Vector)" in ev and '"side1" : kPt(F, p)' in ktext, "evaluate.fs evDistance doc")
    q = _read(os.path.join(std, "query.fs"))
    ck("D10 qSketchRegion(featureId, filterInnerLoops) exists and excludes contained regions (holes)",
       "export function qSketchRegion(featureId is Id, filterInnerLoops is boolean)" in q and "qSketchRegion(skId, true)" in ktext, "query.fs")
    ck("D11 qOwnedByBody(body, EntityType) and qContainsPoint(query, 3D length point) signatures",
       "export function qOwnedByBody(body is Query, entityType is EntityType)" in q
       and "export function qContainsPoint(queryToFilter is Query, point is Vector)" in q, "query.fs")
    ctxfs = _read(os.path.join(std, "context.fs"))
    ck("D12 Ids are hierarchical: qCreatedBy(id + \"x\") covers the sub-operations id + \"x\" + ... (std context.fs)",
       "Ids are hierarchical" in ctxfs and "represents an id named `\"bar\"` whose parent" in ctxfs, "")
    cs = _read(os.path.join(std, "coordSystem.fs"))
    ck("D13 toWorld(CoordSystem) returns a Transform for opPattern",
       "export function toWorld(cSys is CoordSystem) returns Transform" in cs, "coordSystem.fs")
    ck("D14 opPattern copies properties by default (copyPropertiesAndAttributes)",
       "If true (default), copies properties and attributes to patterned entities" in geo, "")
    std_trycatch = sum(1 for fp in glob.glob(os.path.join(std, "*.fs"))
                       if re.search(r"try(?: silent)?\s*\{[^{}]*(\{[^{}]*\}[^{}]*)*\}\s*catch\s*\{", _read(fp)))
    ck("D15 'try silent { } catch { }' (no catch variable) is std syntax", std_trycatch > 0, "%d std files use it" % std_trycatch)
    ck("D16 color(r, g, b, alpha) 4-argument overload exists",
       "export function color(red is number, green is number, blue is number, alpha is number) returns Color" in props, "")
    un = _read(os.path.join(std, "units.fs"))
    ck("D17 atan2(ValueWithUnits, ValueWithUnits) and sin(angle) -> number exist",
       "export function atan2(y is ValueWithUnits, x is ValueWithUnits) returns ValueWithUnits" in un
       and "export function sin(value is ValueWithUnits) returns number" in un, "")
    ck("D18 string ~ number concatenation is std practice (context.fs: \"\" ~ addend)", '"" ~ addend' in ctxfs, "")

    # status reporting: std stores feature status per id and only propagates sub-ids via
    # processSubfeatureStatus, so warnings must go on the feature's own id.
    err = _read(os.path.join(std, "error.fs"))
    ck("D19 std status is per-id; sub-id status needs processSubfeatureStatus to reach the feature",
       "export function processSubfeatureStatus" in err and "Attaches a warning-level status to the given feature id" in err, "error.fs")
    kb = kernel_functions(ktext)
    sub_reports = []
    for name, body in kb.items():
        for m in re.finditer(r"reportFeature(Warning|Info|Error)\(context, (\w+)", body):
            # kWarn rebuilds the feature's own id from its first component
            if m.group(2) != "id" and re.search(r"const %s = newId\(\) \+ id\[0\];" % m.group(2), body):
                continue
            sub_reports.append("10_kernel.fs %s -> reportFeature%s(context, %s, ...) where %s is an operation sub-id" % (name, m.group(1), m.group(2), m.group(2)))
    ck("D20 kernel warnings are reported on the feature id (visible), not on an operation sub-id",
       not sub_reports, "; ".join(sub_reports))

    # kernel op-id suffixes as read from the source agree with the stub table
    ops_read, _ = kernel_op_suffixes(ktext)
    mism = []
    for name, want in (("mkPrismProfile", ['id + "ex"', 'id + "dl"', "skId"]), ("mkRevolve", ['id + "rv"', 'id + "dl"', "skId"]),
                       ("mkPillowBox", ["sid", 'id + "ex"', 'id + "dl"']), ("tagDecal", ["skId", 'id + "sp"', 'id + "dl"', 'id + "dl2"']),
                       ("bSubtract", ["id"]), ("bUnion", ["id"]), ("bDelete", ["id"]), ("shellHollow", ["id"]),
                       ("filletAt", ["id"]), ("copyBody", ["id"]), ("removeSlivers", ["id"]),
                       ("groupParts", ["id"])):
        got = [x for x in ops_read.get(name, []) if not x.startswith("->")]
        if sorted(set(got)) != sorted(set(want)):
            mism.append("%s: %s" % (name, got))
    ck("D21 kernel operation ids match the table the Id-rule stub uses", not mism, "; ".join(mism))
    ck("D22 skId is id + \"sk\" in every kernel helper that sketches",
       len(re.findall(r'const skId = id \+ "sk";', ktext)) == 3, "")

    # ---------------------------------------------------------------- E. block scoping
    std_all_names = set(all_std) | set(reach)
    known = set(tl) | std_all_names | {"true", "false", "undefined"}
    tot_unres, tot_redecl, tot_const = [], [], []
    for fp in files:
        u, r, c = scope_analyse(fp, known)
        tot_unres += u
        tot_redecl += r
        tot_const += c
    ck("E1 every identifier resolves in FeatureScript's block scope (no use outside its block)", not tot_unres,
       "; ".join(tot_unres[:10]) or "all resolve")
    ck("E2 no local redeclared in an enclosing scope", not tot_redecl, "; ".join(tot_redecl[:10]))
    ck("E3 no assignment to a const", not tot_const, "; ".join(tot_const[:10]))
    import onshape_lint
    ow = onshape_lint.warnings(code)
    unused_decl = ["line %d %s" % w for w in ow if w[1].startswith("Unused declaration")]
    unread = ["line %d %s" % w for w in ow if not w[1].startswith("Unused declaration")]
    ck("E4 no local is set but not used (the Feature Studio editor's 'Variable X set but not used')", not unread,
       "; ".join(unread[:10]) or "none")
    ck("E7 every top-level declaration is used (the Feature Studio editor's 'Unused declaration')", not unused_decl,
       "; ".join(unused_decl[:20]) or "none")
    shadow, tl_refs = [], []
    for fp in files:
        toks = tokenize(_read(fp))
        depth = 0
        for i, (k, v, ln) in enumerate(toks):
            if k == "op" and v in "{([":
                depth += 1
            elif k == "op" and v in "})]":
                depth -= 1
            elif k == "id" and v in ("var", "const") and toks[i + 1][0] == "id":
                nme = toks[i + 1][1]
                if depth > 0 and nme in reach:
                    shadow.append("%s:%d %s (std %s)" % (os.path.basename(fp), ln, nme, reach[nme]))
                if depth == 0 and v == "const" and toks[i + 3][1] != "defineFeature":
                    j, d = i + 3, 0
                    while not (toks[j][1] == ";" and d == 0):
                        if toks[j][1] in "([{":
                            d += 1
                        elif toks[j][1] in ")]}":
                            d -= 1
                        elif toks[j][0] == "id" and toks[j][1] not in ("true", "false", "undefined") and toks[j - 1][1] != ".":
                            tl_refs.append("%s:%d %s -> %s" % (os.path.basename(fp), ln, nme, toks[j][1]))
                        j += 1
    out.append(("E5 (info) locals that shadow a std export (legal: std itself writes `const line = line(...)`): %d" % len(shadow),
                True, "; ".join(shadow)))
    ck("E6 top-level consts are literal (no load-order dependence between module constants)", not tl_refs, "; ".join(tl_refs[:10]))

    # ---------------------------------------------------------------- F. Id rules (stub run)
    import kernel_occ as K
    import run as R
    base = dict(R.DEFAULT_OPTS)
    variants = [("default", {}), ("no decals", {"decals": False}), ("no tags", {"tags": False}),
                ("stock only", {"staged": False}), ("staged only", {"stock": False}),
                ("stacked/lit/route", {"pairs": "STACKED", "lit": True, "fieldLed": "ROUTE"}),
                ("crags only", {"perimeter": False, "walls": False, "headwalls": False, "tape": False, "tags": False,
                                "staged": False, "stock": False})]
    for label, o in variants:
        opts = dict(base)
        opts.update(o)
        ctx, dup, badch, cont = id_rule_run(K, R, opts)
        ck("F %s: Id components use only [A-Za-z0-9_.+/-] (%d ops)" % (label, len(ctx.ops)), not badch, ", ".join(badch[:10]))
        ck("F %s: no operation id used twice" % label, not dup, ", ".join(dup[:10]))
        ck("F %s: every Id prefix is one contiguous run of operations (std context.fs rule)" % label, not cont, "; ".join(cont[:10]))
        ck("F %s: every body query (build, style, selfCheck) resolves to a live body" % label, not ctx.errors,
           "; ".join(ctx.errors[:10]) or "%d queries" % ctx.queries)
    for kind in ("crate", "cell", "coil"):
        for rest in (True, False):
            ctx, dup, badch, cont = id_rule_run(K, R, base, (kind, rest))
            ck("F game piece %s rest=%s: Id rules hold" % (kind, rest), not (dup or badch or cont or ctx.errors),
               "; ".join(dup + badch + cont + ctx.errors)[:300])

    # qContainsPoint probe points vs Onshape's zeroLength
    rec, tol_in = contains_point_audit(K)
    far = [r for r in rec if r[3] > tol_in / 100]
    multi = [r for r in rec if r[4] != 1]
    worst = max(r[3] for r in rec) if rec else 0.0
    ck("D23 every qContainsPoint probe (%d fillet/face points) lies on its entity to <1%% of TOLERANCE.zeroLength" % len(rec),
       not far, "worst %.2e in; %s" % (worst, "; ".join("%s %s %s d=%.2e" % (r[0], r[1], r[2], r[3]) for r in far[:5])))
    ck("D24 every qContainsPoint probe hits exactly one edge/face (no vertex or shared-edge hits)", not multi,
       "; ".join("%s %s %s hits %d" % (r[0], r[1], [round(x, 3) for x in r[2]], r[4]) for r in multi[:8]))

    # op / evaluation volume (information for regeneration time in Onshape)
    ctx0, _, _, _ = id_rule_run(K, R, dict(R.DEFAULT_OPTS))
    ndec = sum(1 for o in ctx0.ops if len(o) >= 3 and o[-1] == "sp")
    out.append(("I (info) default build: %d std operations (+%d sketches solved), %d decal face splits; %d body queries incl. selfCheck"
                % (len(ctx0.ops), sum(1 for o in ctx0.ops if o[-1] == "sk"), ndec, ctx0.queries), True, ""))

    # ---------------------------------------------------------------- G. feature UI
    ftext = _read(os.path.join(SRC, "90_features.fs"))
    enums = {}
    for m in re.finditer(r"export enum (\w+)\s*\{(.*?)\n\}", ftext, re.S):
        body = re.sub(r"annotation\s*\{[^}]*\}", "", m.group(2))
        enums[m.group(1)] = [x.strip() for x in body.split(",") if x.strip()]
    for fm in re.finditer(r"export const (\w+) = defineFeature\(function\(context is Context, id is Id, definition is map\)\s*precondition\s*\{", ftext):
        start = fm.end() - 1
        d = 0
        for j in range(start, len(ftext)):
            if ftext[j] == "{":
                d += 1
            elif ftext[j] == "}":
                d -= 1
                if d == 0:
                    pre_end = j
                    break
        pre = ftext[start:pre_end + 1]
        # defaults map: the last {...} before the closing ");" of defineFeature
        rest = ftext[pre_end:]
        close = rest.index("});")
        dmap_start = rest.rindex("{", 0, close)
        dmap = dict(re.findall(r'"(\w+)"\s*:\s*([\w.]+)', rest[dmap_start:close + 1]))
        params = re.findall(r'annotation\s*\{([^}]*)\}\s*definition\.(\w+) is (\w+);', pre)
        problems = []
        for ann, pname, ptype in params:
            dm = re.search(r'"Default"\s*:\s*([\w.]+)', ann)
            if dm is None:
                problems.append("%s has no UI Default" % pname)
                continue
            dv = dm.group(1)
            if pname not in dmap:
                problems.append("%s missing from defaults map" % pname)
            elif dmap[pname] != dv:
                problems.append("%s: UI default %s vs defaults map %s" % (pname, dv, dmap[pname]))
            if ptype in enums:
                if not dv.startswith(ptype + ".") or dv.split(".", 1)[1] not in enums[ptype]:
                    problems.append("%s: default %s not a member of %s" % (pname, dv, ptype))
            elif ptype == "boolean" and dv not in ("true", "false"):
                problems.append("%s: boolean default %s" % (pname, dv))
        extra = set(dmap) - {p for _, p, _ in params}
        if extra:
            problems.append("defaults for unknown parameters %s" % sorted(extra))
        ck("G %s: every parameter has a UI Default matching the defaults map (%d params)" % (fm.group(1), len(params)),
           not problems, "; ".join(problems))
    ann = re.findall(r'annotation \{ "Feature Type Name" : "([^"]+)"', ftext)
    ck("G feature type names are distinct", len(ann) == len(set(ann)), ", ".join(ann))
    # reportFeature* in the features use the feature's own id
    ck("G self-check status is reported on the feature id",
       re.search(r"reportFeatureInfo\(context, id, ", ftext) is not None and re.search(r"reportFeatureWarning\(context, id, ", ftext) is not None, "")

    # ---------------------------------------------------------------- H. evDistance inside-point semantics
    inside_hits = []
    orig = f.ns["measureDistToPoint"]

    def probe(context, bodies, F, p):
        wp = F.pt(p)
        for s in context.solids_for(bodies):
            cl = K.BRepClass3d_SolidClassifier(s, K._gp(wp), 1e-7)
            if cl.State() == K.TopAbs_IN:
                inside_hits.append("%s at %s" % ([str(b) for b in bodies], [round(x, 3) for x in p]))
        return orig(context, bodies, F, p)

    f.ns["measureDistToPoint"] = probe
    try:
        checks = f.ns["selfCheck"](f.ctx, f.id, f.opts)
    finally:
        f.ns["measureDistToPoint"] = orig
    nprobe = sum(1 for c in checks if "bore radius" in c[0] or "half height" in c[0] or "jamb" in c[0] or "BASE DEPOT c" in c[0])
    ck("H selfCheck never measures evDistance from a point inside a solid (%d point probes)" % nprobe,
       not inside_hits, "; ".join(inside_hits[:5]))
    fails = f.ns["failures"](checks)
    ck("H selfCheck (%d checks) passes on the twin" % len(checks), not fails, "; ".join(fails[:5]))
    return out
