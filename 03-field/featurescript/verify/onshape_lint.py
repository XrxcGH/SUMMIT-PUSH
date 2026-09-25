# -*- coding: utf-8 -*-
"""
The two warnings the Onshape Feature Studio editor reports for this code, reproduced off-line:

    Unused declaration: NAME          a top-level function, const or enum that is not exported
                                      and is referenced nowhere else in the Feature Studio
    Variable NAME set but not used    a local (var, const, for-loop or catch variable) that is
                                      assigned but never read

    python 03-field/featurescript/verify/onshape_lint.py [SummitPushField.fs]

build.py runs this on the assembled Feature Studio and fails on any warning, so the Studio
pastes into Onshape without warnings.  Scoping follows FeatureScript: blocks nest, a `for` or
`catch` header belongs to the block (or, for `for`, the single statement) that follows it, and `{`
after `=`, `(`, `,`, `:`, `[` or `return` opens a map literal, not a block.
"""
import os
import re
import sys

_TOK = re.compile(r"""
    (?P<ws>\s+)
  | (?P<lc>//[^\n]*)
  | (?P<bc>/\*.*?\*/)
  | (?P<str>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<num>\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)
  | (?P<id>[A-Za-z_]\w*)
  | (?P<op>\+=|-=|\*=|/=|==|!=|<=|>=|&&|\|\||->|[-+*/%^~<>=!?:;,.()\[\]{}@])
""", re.S | re.X)

DECL_KINDS = ("function", "const", "enum", "predicate", "type")
ASSIGN = ("=", "+=", "-=", "*=", "/=")
MAP_OPENERS = {"=", "(", ",", ":", "[", "return", "?", "||", "&&", "!", "+", "~"}


def tokenize(text):
    out, line, pos = [], 1, 0
    while pos < len(text):
        m = _TOK.match(text, pos)
        if not m:
            raise ValueError("cannot tokenize line %d: %r" % (line, text[pos:pos + 20]))
        kind = m.lastgroup
        val = m.group(kind)
        if kind not in ("ws", "lc", "bc"):
            out.append((kind, val, line))
        line += val.count("\n")
        pos = m.end()
    return out


def _close(toks, i, open_, close):
    d = 0
    for j in range(i, len(toks)):
        if toks[j][0] == "op" and toks[j][1] == open_:
            d += 1
        elif toks[j][0] == "op" and toks[j][1] == close:
            d -= 1
            if d == 0:
                return j
    raise ValueError("unbalanced %s at line %d" % (open_, toks[i][2]))


def _stmt_end(toks, j):
    """Index of the ';' (or the closing '}') that ends the statement starting at toks[j]."""
    d = 0
    for m in range(j, len(toks)):
        if toks[m][0] != "op":
            continue
        if toks[m][1] in "([{":
            d += 1
        elif toks[m][1] in ")]}":
            d -= 1
            if d == 0 and toks[m][1] == "}":
                return m
        elif toks[m][1] == ";" and d == 0:
            return m
    raise ValueError("unterminated statement at line %d" % toks[j][2])


def _top_level(toks):
    """[(name, line, exported, first token, last token)] for every top-level declaration."""
    out = []
    i, depth = 0, 0
    while i < len(toks):
        k, v, ln = toks[i]
        if k == "op" and v in "{([":
            depth += 1
        elif k == "op" and v in "})]":
            depth -= 1
        elif depth == 0 and k == "id" and v in DECL_KINDS and i + 1 < len(toks) and toks[i + 1][0] == "id":
            exported = i > 0 and toks[i - 1][1] == "export"
            j = i + 2
            if v in ("function", "predicate", "enum", "type"):
                while toks[j][1] != "{":
                    j += 1
                end = _close(toks, j, "{", "}")
            else:
                d = 0
                while not (toks[j][1] == ";" and d == 0):
                    if toks[j][1] in "([{":
                        d += 1
                    elif toks[j][1] in ")]}":
                        d -= 1
                    j += 1
                end = j
            out.append((toks[i + 1][1], ln, exported, i + 1, end))
        i += 1
    return out


def unused_declarations(toks):
    decls = _top_level(toks)
    refs = {}
    for i, (k, v, ln) in enumerate(toks):
        if k == "id" and not (i > 0 and toks[i - 1][1] == "."):
            refs.setdefault(v, []).append(i)
    out = []
    for name, ln, exported, at, end in decls:
        if exported:
            continue
        # references outside the declaration itself (recursion does not count as use)
        if not [i for i in refs.get(name, []) if not at <= i <= end]:
            out.append((ln, "Unused declaration: %s" % name))
    return out


def unread_locals(toks):
    """Locals that are written but never read, with FeatureScript block scoping."""
    out = []
    frames = []      # {"kind": func|for|catch|block|map, "names": {name: [line, reads]}}

    def lookup(name):
        for fr in reversed(frames):
            if name in fr["names"]:
                return fr["names"][name]
        return None

    def close(fr):
        for name, (ln, reads) in fr["names"].items():
            if reads == 0 and name != "_":
                out.append((ln, "Variable %s set but not used" % name))

    def pop_headers(i):
        # a header whose body is a single statement (no braces) is closed at that statement's end
        while frames and frames[-1]["kind"] in ("for", "catch", "func") and "end" not in frames[-1]:
            if frames[-1]["kind"] == "func" and i + 1 < len(toks) and toks[i + 1][1] == "{":
                break
            fr = frames.pop()
            if fr["kind"] != "func":
                close(fr)

    i, n, prev = 0, len(toks), None
    while i < n:
        k, v, ln = toks[i]
        nxt = toks[i + 1][1] if i + 1 < n else ""
        if k == "id" and v in ("FeatureScript", "import") and not frames:
            while toks[i][1] != ";":
                i += 1
            prev, i = ("op", ";", ln), i + 1
            continue
        if k == "id" and v == "annotation" and nxt == "{":
            i = _close(toks, i + 1, "{", "}") + 1
            prev = ("op", "}", ln)
            continue
        if k == "id" and v == "enum" and not frames:
            j = i
            while toks[j][1] != "{":
                j += 1
            i = _close(toks, j, "{", "}") + 1
            prev = ("op", "}", ln)
            continue
        if k == "id" and v in ("function", "predicate") and (nxt == "(" or (toks[i + 1][0] == "id" and toks[i + 2][1] == "(")):
            j = i + 1 if nxt == "(" else i + 2
            e = _close(toks, j, "(", ")")
            # parameters are not reported; they are declared so their uses resolve
            fr = {"kind": "func", "names": {}}
            params = {}
            depth, expect = 0, True
            for t in toks[j + 1:e]:
                if t[1] in "([{":
                    depth += 1
                elif t[1] in ")]}":
                    depth -= 1
                elif t[1] == "," and depth == 0:
                    expect = True
                elif expect and t[0] == "id":
                    params[t[1]] = True
                    expect = False
            fr["params"] = params
            frames.append(fr)
            i = e + 1
            if i < n and toks[i][1] == "returns":
                i += 2
            prev = ("op", ")", ln)
            continue
        if k == "id" and v == "for" and nxt == "(":
            fr = {"kind": "for", "names": {}}
            e = _close(toks, i + 1, "(", ")")
            if e + 1 < n and toks[e + 1][1] != "{":
                fr["end"] = _stmt_end(toks, e + 1)
            frames.append(fr)
            if toks[i + 2][1] == "var":
                fr["names"][toks[i + 3][1]] = [toks[i + 3][2], 0]
                i += 4
            else:
                i += 2
            prev = ("op", "(", ln)
            continue
        if k == "id" and v == "catch":
            fr = {"kind": "catch", "names": {}}
            frames.append(fr)
            if nxt == "(":
                fr["names"][toks[i + 2][1]] = [toks[i + 2][2], 0]
                i += 4
            else:
                i += 1
            prev = ("op", ")", ln)
            continue
        if k == "id" and v in ("var", "const") and frames and toks[i + 1][0] == "id":
            target = next(fr for fr in reversed(frames) if fr["kind"] != "map")
            target["names"][toks[i + 1][1]] = [ln, 0]
            i += 2
            prev = ("id", "decl", ln)
            continue
        if k == "op" and v == "{":
            is_map = prev is not None and prev[1] in MAP_OPENERS
            frames.append({"kind": "map" if is_map else "block", "names": {}})
        elif k == "op" and v == "}":
            if frames:
                close(frames.pop())
            pop_headers(i)
        elif k == "id" and frames and not (prev is not None and prev[1] == "."):
            d = lookup(v)
            if d is not None and nxt not in ASSIGN:
                d[1] += 1
        while frames and frames[-1].get("end") == i:
            close(frames.pop())
        prev = (k, v, ln)
        i += 1
    return out


def warnings(text):
    toks = tokenize(text)
    return sorted(unused_declarations(toks) + unread_locals(toks))


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "SummitPushField.fs")
    with open(path, encoding="utf-8") as fh:
        found = warnings(fh.read())
    for ln, text in found:
        print("%s:%d: %s" % (os.path.basename(path), ln, text))
    print("%d warning(s)" % len(found))
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
