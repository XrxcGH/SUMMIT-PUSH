"""Scope analysis of the part-code dialect under FeatureScript rules.

FeatureScript is block-scoped, re-tests a C-style loop's condition every pass, forbids assigning
a const, and treats arrays as values; the Python twin (verify/fs2py.py) is function-scoped,
fixes a loop's range up front and aliases lists.  Code that relies on any of these differences
would build one thing in Onshape and another off-line, so build.py rejects it:

    undeclared, after_block, const_assign, dup, shadow_local, shadow_global, loop_mut,
    sub_store (indexed assignment), chain (chained comparison), top_dup, twin_clash

Shared by build.py and verify/checks/check_twin.py.
"""
import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fs2py  # noqa: E402


def _fs_functions(text):
    """name -> (params, body) for every top-level `function` in a FeatureScript file."""
    out = {}
    for m in re.finditer(r"^function\s+(\w+)\s*\(([^)]*)\)[^\n]*\n\{\n(.*?)^\}", text, re.M | re.S):
        out[m.group(1)] = (m.group(2), m.group(3))
    return out


FS_KW = {"var", "const", "function", "return", "if", "else", "for", "in", "true", "false", "undefined", "is", "returns"}


def _statements(src):
    nest, buf, start = 0, "", 0
    for n, raw in enumerate(src.splitlines(), 1):
        line = fs2py._strip_comment(raw).strip()
        if not line:
            continue
        if nest == 0 and line in ("{", "}"):
            yield n, line
            continue
        if nest == 0:
            buf, start = line, n
        else:
            buf += " " + line
        nest += fs2py._nest(line)
        if nest == 0:
            yield start, buf


def _idents(expr):
    code = fs2py._code_only(expr)
    out = []
    for m in re.finditer(r"(?<![\w.])([A-Za-z_]\w*)", code):
        if m.group(1) not in FS_KW:
            out.append(m.group(1))
    return out


def analyze(sources, kernel_text, std_names=None, twin_names=()):
    """Scope/dialect analysis of part-code sources [(name, text)] under FeatureScript rules.
    kernel_text: src/10_kernel.fs; std_names: every std export (None -> a short fallback list);
    twin_names: public names of verify/kernel_occ.py (optional)."""
    kernel_names = set(_fs_functions(kernel_text))
    if std_names is None:
        std_names = {"min", "max", "abs", "size", "append", "concatenateArrays", "sqrt", "floor", "cross", "vector",
                     "dot", "norm", "normalize", "PI", "Context", "Id"}
    std_names = set(std_names)
    top = {}
    for rel, text in sources:
        depth = 0
        for n, st in _statements(text):
            if st == "{":
                depth += 1
                continue
            if st == "}":
                depth -= 1
                continue
            m = re.match(r"^function\s+(\w+)", st) or re.match(r"^const\s+(\w+)", st)
            if m and depth == 0:
                top.setdefault(m.group(1), []).append("%s:%d" % (rel, n))
    globals_fs = set(top) | kernel_names | std_names
    twin_only = set(twin_names) - kernel_names - std_names

    import builtins
    import keyword
    issues = {"undeclared": [], "after_block": [], "dup": [], "const_assign": [], "shadow_local": [], "shadow_global": [],
              "loop_mut": [], "sub_store": [], "chain": [], "top_dup": [], "twin_clash": []}
    stats = {"decl": 0, "uses": 0, "loops": 0, "stmts": 0}
    for nme, locs in top.items():
        if len(locs) > 1 or nme in kernel_names:
            issues["top_dup"].append("%s %s" % (nme, locs))
        if nme in twin_only or keyword.iskeyword(nme) or hasattr(builtins, nme):
            issues["twin_clash"].append("%s %s" % (nme, locs))

    for rel, text in sources:
        scopes, pending, closed, loops = [], None, set(), []

        def lookup(nm_):
            for sc in reversed(scopes):
                if nm_ in sc:
                    return sc[nm_]
            return None

        def use(expr, where, extra=()):
            try:
                for node in ast.walk(ast.parse(fs2py._expr(expr).strip() or "0", mode="eval")):
                    if isinstance(node, ast.Compare) and len(node.ops) > 1:
                        issues["chain"].append(where)
            except SyntaxError:
                pass
            for idn in _idents(expr):
                stats["uses"] += 1
                if idn in extra or lookup(idn) or idn in globals_fs:
                    continue
                (issues["after_block"] if idn in closed else issues["undeclared"]).append("%s at %s" % (idn, where))

        def declare(nm_, kind, where):
            stats["decl"] += 1
            if scopes and nm_ in scopes[-1]:
                issues["dup"].append("%s at %s" % (nm_, where))
            elif lookup(nm_):
                issues["shadow_local"].append("%s at %s" % (nm_, where))
            if nm_ in globals_fs:
                issues["shadow_global"].append("%s at %s" % (nm_, where))
            scopes[-1][nm_] = kind

        def assigned(nm_, where):
            for lp in loops:
                if nm_ in lp["watch"]:
                    issues["loop_mut"].append("%s at %s (loop at %s)" % (nm_, where, lp["at"]))

        for n, st in _statements(text):
            where = "%s:%d" % (rel, n)
            stats["stmts"] += 1
            if st == "{":
                scopes.append(dict(pending or {}))
                if loops and loops[-1]["depth"] is None:
                    loops[-1]["depth"] = len(scopes)
                pending = None
                continue
            if st == "}":
                sc = scopes.pop()
                if scopes:
                    closed |= set(sc)
                else:
                    closed = set()
                while loops and loops[-1]["depth"] is not None and loops[-1]["depth"] > len(scopes):
                    loops.pop()
                continue
            s = st[:-1] if st.endswith(";") else st
            m = re.match(r"^function\s+(\w+)\s*\((.*)\)(\s+returns\s+\w+)?$", s)
            if m:
                pending = {}
                for p in m.group(2).split(","):
                    p = p.strip()
                    if p:
                        pending[p.split()[0]] = "param"
                continue
            if not scopes:
                m = re.match(r"^const\s+(\w+)\s*=\s*(.*)$", s)
                if m:
                    scopes.append({})
                    use(m.group(2), where)
                    scopes.pop()
                continue
            m = re.match(r"^for\s*\(\s*var\s+(\w+)\s+in\s+(.+)\)$", s)
            if m:
                use(m.group(2), where)
                pending = {m.group(1): "loop"}
                continue
            m = re.match(r"^for\s*\(\s*var\s+(\w+)\s*=\s*(.+?);\s*(.+?);\s*(.+)\)$", s)
            if m:
                v = m.group(1)
                use(m.group(2), where)
                use(m.group(3) + " " + m.group(4), where, extra=(v,))
                pending = {v: "loop"}
                watch = {v} | set(_idents(m.group(3))) | set(_idents(re.sub(r"^\w+\s*\+=", "", m.group(4))))
                loops.append({"watch": watch, "at": where, "depth": None})
                stats["loops"] += 1
                continue
            m = re.match(r"^(?:else\s+)?if\s*\((.+)\)$", s)
            if m:
                use(m.group(1), where)
                continue
            if s == "else":
                continue
            m = re.match(r"^(var|const)\s+(\w+)\s*(?:=\s*(.*))?$", s)
            if m:
                if m.group(3):
                    use(m.group(3), where)
                declare(m.group(2), m.group(1), where)
                continue
            m = re.match(r"^return\b(.*)$", s)
            if m:
                use(m.group(1), where)
                continue
            m = re.match(r"^(\w+)\s*(\[.*?\])?\s*(=|\+=|-=|\*=|/=)(?!=)\s*(.*)$", s)
            if m:
                tgt = m.group(1)
                use(m.group(4), where)
                if m.group(2):
                    issues["sub_store"].append("%s%s at %s" % (tgt, m.group(2), where))
                    use(m.group(2), where)
                kind = lookup(tgt)
                if kind is None:
                    (issues["const_assign"] if tgt in globals_fs else issues["undeclared"]).append("%s (assigned) at %s" % (tgt, where))
                elif kind == "const":
                    issues["const_assign"].append("%s at %s" % (tgt, where))
                assigned(tgt, where)
                continue
            use(s, where)

    return issues, stats, top, std_names
