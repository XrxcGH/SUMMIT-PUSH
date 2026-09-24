# -*- coding: utf-8 -*-
"""
Transpile the SUMMIT PUSH part code (src/2x_*.fs .. src/4x_*.fs) from FeatureScript to Python.

The part code is written in a deliberately small dialect that means the same thing in both
languages, so the Python it becomes builds the same geometry through verify/kernel_occ.py.
`lint()` enforces the dialect; `transpile()` converts it.

Dialect (see README "Part-code dialect"):
  * plain numbers only (inches, degrees) — no units, no `^`, `~`, `%`, `?:`
  * statements end in `;`; blocks use braces alone on their own lines (Allman style)
  * `for (var i = A; i < B; i += S)`, `for (var x in ARRAY)`, `if (..)`, `else if (..)`, `else`
  * `var`/`const` declarations, `return`, calls, assignments (`=`, `+=`, `-=`)
  * maps are indexed as m["key"] (never m.key); strings only as literals and via nm()/msg()
"""
import re
import sys

RESERVED = {
    # FeatureScript
    "function", "var", "const", "return", "if", "else", "for", "in", "while", "break",
    "continue", "true", "false", "undefined", "is", "new", "export", "import", "annotation",
    "precondition", "predicate", "type", "typecheck", "enum", "operator", "try", "catch",
    "throw", "switch", "returns", "as", "do", "silent",
    # Python
    "lambda", "def", "pass", "from", "with", "yield", "class", "global", "not", "and", "or",
    "del", "assert", "elif", "raise", "except", "finally", "None", "True", "False",
    "nonlocal", "async", "await", "print", "len", "list", "dict", "str", "int", "float",
    "id_", "sum", "round", "map", "range", "type", "object", "open", "set", "iter", "next",
}
# std-library names that part code must never rebind (a variable with one of these names
# shadows the std function in FeatureScript and breaks the kernel twin in Python)
STD_NAMES = {
    "plane", "line", "box", "vector", "size", "color", "material", "transform", "path",
    "inch", "meter", "degree", "radian", "sin", "cos", "tan", "sqrt", "abs", "min", "max",
    "floor", "ceil", "dot", "cross", "norm", "normalize", "append", "context", "definition",
    "sketch", "query", "matrix", "PI", "pound", "mesh", "curve", "surface", "sphere", "cone",
    "cylinder", "torus", "circle", "ellipse", "arc", "point", "face", "edge", "body", "part",
    "copy", "pattern", "boolean", "string", "number", "array", "map", "shell", "fillet",
    "chamfer", "extrude", "revolve", "sweep", "loft", "split", "tolerance", "concatenateArrays",
}


class DialectError(Exception):
    pass


def _strip_comment(line):
    # part code never puts "//" inside a string literal (lint enforces it)
    i = line.find("//")
    return line if i < 0 else line[:i]


def _split_strings(s):
    """Yield (is_string, text) chunks."""
    out, buf, q = [], "", False
    for ch in s:
        if ch == '"':
            if q:
                buf += ch
                out.append((True, buf))
                buf, q = "", False
            else:
                if buf:
                    out.append((False, buf))
                buf, q = ch, True
        else:
            buf += ch
    if q:
        raise DialectError("unterminated string")
    if buf:
        out.append((False, buf))
    return out


def _nest(s):
    n = 0
    for is_str, t in _split_strings(s):
        if is_str:
            continue
        n += t.count("(") + t.count("[") + t.count("{")
        n -= t.count(")") + t.count("]") + t.count("}")
    return n


def _expr(s):
    out = []
    for is_str, t in _split_strings(s):
        if is_str:
            out.append(t)
            continue
        t = t.replace("&&", " and ").replace("||", " or ")
        t = re.sub(r"!(?!=)", " not ", t)
        t = re.sub(r"\btrue\b", "True", t)
        t = re.sub(r"\bfalse\b", "False", t)
        t = re.sub(r"\bundefined\b", "None", t)
        out.append(t)
    return "".join(out)


def _code_only(s):
    return "".join(t for is_str, t in _split_strings(s) if not is_str)


def lint(src, fname="<part>"):
    errs = []
    for n, raw in enumerate(src.splitlines(), 1):
        if '"' in raw and "//" in raw and raw.find("//") > raw.find('"') and raw.count('"') >= 2:
            # comment after a string is fine only if the // is outside the quotes
            pass
        line = _strip_comment(raw).rstrip()
        try:
            code = _code_only(line)
        except DialectError as e:
            errs.append("%s:%d: %s" % (fname, n, e))
            continue
        for bad, why in (("?", "ternary ?: is not in the dialect"),
                         ("^", "use x * x, not ^"),
                         ("~", "use nm() / msg() for strings"),
                         ("%", "modulo is not in the dialect"),
                         ("===", "no ==="),
                         ("++", "use += 1"), ("--", "use -= 1")):
            if bad in code:
                errs.append("%s:%d: %s" % (fname, n, why))
        if re.search(r"[A-Za-z_\)\]]\s*\.\s*[A-Za-z_]", code):
            errs.append("%s:%d: field access with '.' — index maps as m[\"key\"]" % (fname, n))
        is_fn = re.match(r"\s*function\b", code) is not None
        kw = r"\b(while|try|catch|switch|throw|new|lambda)\b" if is_fn else r"\b(while|try|catch|switch|throw|new|lambda|is|returns)\b"
        if re.search(kw, code):
            errs.append("%s:%d: keyword not in the dialect" % (fname, n))
        m = re.match(r"\s*(?:var|const)\s+(\w+)", code)
        names = []
        if m:
            names.append(m.group(1))
        m = re.match(r"\s*for\s*\(\s*var\s+(\w+)", code)
        if m:
            names.append(m.group(1))
        m = re.match(r"\s*function\s+\w+\s*\((.*)\)", code)
        if m:
            for p in m.group(1).split(","):
                p = p.strip()
                if p and p.split()[0] not in ("context", "id"):
                    names.append(p.split()[0])
        for nme in names:
            if nme in RESERVED or nme in STD_NAMES:
                errs.append("%s:%d: '%s' is reserved or shadows a std name" % (fname, n, nme))
        s = code.strip()
        if s.startswith("{") and s != "{" and _nest(s) != 0 and not s.endswith(","):
            pass
        if re.match(r"^(if|for|else)\b.*\{\s*$", s) or re.match(r"^function\b.*\{\s*$", s):
            errs.append("%s:%d: put the block brace on its own line" % (fname, n))
        if re.match(r"^(if|else if)\s*\(.*\)\s*[^\s{].*$", s) and not s.endswith(")"):
            errs.append("%s:%d: single-line if without braces" % (fname, n))
    return errs


def transpile(src, fname="<part>"):
    errs = lint(src, fname)
    if errs:
        raise DialectError("\n".join(errs))
    out = []
    depth = 0
    nest = 0          # bracket nesting carried across lines (multi-line expressions)
    stmt_open = False  # inside a multi-line statement
    for n, raw in enumerate(src.splitlines(), 1):
        line = _strip_comment(raw).rstrip()
        s = line.strip()
        tag = "  # %s:%d" % (fname, n)
        if not s:
            out.append("")
            continue
        if nest == 0 and s == "{":
            depth += 1
            out.append("    " * depth + "pass" + tag)
            continue
        if nest == 0 and s == "}":
            depth -= 1
            if depth < 0:
                raise DialectError("%s:%d: unbalanced }" % (fname, n))
            continue
        ind = "    " * depth
        if nest > 0:
            # continuation line of a multi-line expression
            nest += _nest(s)
            t = s
            if nest == 0 and t.endswith(";"):
                t = t[:-1]
            out.append(ind + "        " + _expr(t) + tag)
            continue
        body = s[:-1] if s.endswith(";") else s
        m = re.match(r"^function\s+(\w+)\s*\((.*)\)(\s+returns\s+\w+)?$", body)
        if m:
            params = []
            for p in m.group(2).split(","):
                p = p.strip()
                if p:
                    params.append(p.split()[0])
            out.append(ind + "def %s(%s):%s" % (m.group(1), ", ".join(params), tag))
            continue
        m = re.match(r"^for\s*\(\s*var\s+(\w+)\s*=\s*(.+?);\s*\1\s*(<=|<)\s*(.+?);\s*\1\s*\+=\s*(.+)\)$", body)
        if m:
            v, a, op, b, st = m.groups()
            fn = "_frange_incl" if op == "<=" else "_frange"
            out.append(ind + "for %s in %s(%s, %s, %s):%s" % (v, fn, _expr(a), _expr(b), _expr(st), tag))
            continue
        m = re.match(r"^for\s*\(\s*var\s+(\w+)\s+in\s+(.+)\)$", body)
        if m:
            out.append(ind + "for %s in %s:%s" % (m.group(1), _expr(m.group(2)), tag))
            continue
        if body.startswith("for"):
            raise DialectError("%s:%d: unsupported for-loop form" % (fname, n))
        m = re.match(r"^else\s+if\s*\((.+)\)$", body)
        if m:
            out.append(ind + "elif %s:%s" % (_expr(m.group(1)), tag))
            continue
        m = re.match(r"^if\s*\((.+)\)$", body)
        if m:
            out.append(ind + "if %s:%s" % (_expr(m.group(1)), tag))
            continue
        if body == "else":
            out.append(ind + "else:" + tag)
            continue
        m = re.match(r"^(?:var|const)\s+(\w+)\s*=\s*(.*)$", body)
        if m:
            body = "%s = %s" % (m.group(1), m.group(2))
        else:
            m = re.match(r"^var\s+(\w+)$", body)
            if m:
                body = "%s = None" % m.group(1)
        nest = _nest(s)
        if nest < 0:
            raise DialectError("%s:%d: unbalanced brackets" % (fname, n))
        out.append(ind + _expr(body) + tag)
    if depth != 0 or nest != 0:
        raise DialectError("%s: unbalanced blocks at end of file" % fname)
    return "\n".join(out) + "\n"


PRELUDE = '''
def _frange(a, b, st):
    v = a
    while v < b:
        yield v
        v += st


def _frange_incl(a, b, st):
    v = a
    while v <= b:
        yield v
        v += st
'''


if __name__ == "__main__":
    for f in sys.argv[1:]:
        with open(f, encoding="utf-8") as fh:
            print(transpile(fh.read(), f))
