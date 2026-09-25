# -*- coding: utf-8 -*-
"""
Assemble SummitPushField.fs (one Feature Studio, ready to paste into Onshape) from src/*.fs,
and check it.

    python 03-field/featurescript/build.py [--std PATH]

Checks, in order:
  1. every part-code file (src/2x-4x) passes the dialect lint (verify/fs2py.py) and the
     FeatureScript scope rules (verify/scope_lint.py)
  2. the assembled Feature Studio raises none of the Onshape editor's warnings
     (verify/onshape_lint.py: unused declarations, variables set but not used)
  3. with --std PATH, or $FS_STD, or a checkout at .fs-std/ (the FeatureScript standard
     library, e.g. https://github.com/javawizard/onshape-std-library-mirror), every function
     the Feature Studio calls is either defined in it or exported by the standard library, and
     every Enum.MEMBER it names exists
Exit status is non-zero if any check fails.
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "verify"))
import fs2py  # noqa: E402
import onshape_lint  # noqa: E402
import scope_lint  # noqa: E402

OUT = os.path.join(HERE, "SummitPushField.fs")
PART_RE = re.compile(r"^[2-4]\d_.*\.fs$")

FS_KEYWORDS = {"if", "for", "while", "return", "function", "precondition", "annotation", "catch",
               "try", "silent", "switch", "defineFeature", "import", "throw", "typecheck", "predicate",
               "else", "is", "in", "var", "const", "export", "new"}


def sources():
    files = sorted(glob.glob(os.path.join(HERE, "src", "*.fs")))
    if not files:
        raise SystemExit("no sources in src/")
    return files


def assemble(files):
    parts = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            txt = fh.read().rstrip() + "\n"
        name = os.path.basename(f)
        if name.startswith("00_"):
            parts.append(txt)
        else:
            parts.append("\n// ---------------------------------------------------------------- src/%s\n\n%s" % (name, txt))
    return "".join(parts)


def lint_parts(files, std=None):
    errs = []
    parts = []
    kernel = ""
    for f in files:
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        if PART_RE.match(os.path.basename(f)):
            errs += fs2py.lint(text, os.path.relpath(f, HERE))
            parts.append((os.path.relpath(f, HERE), text))
        elif os.path.basename(f) == "10_kernel.fs":
            kernel = text
    # block scope, const, loop and value semantics that FeatureScript and the twin must share
    std_names = None
    if std:
        names, enums = std_index(std)
        std_names = set(names) | set(enums)
    issues = scope_lint.analyze(parts, kernel, std_names)[0]
    for kind, found in sorted(issues.items()):
        for where in found:
            errs.append("scope (%s): %s" % (kind, where))
    return errs


def strip_comments_and_strings(code):
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    code = re.sub(r"//[^\n]*", "", code)
    code = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
    return code


def std_index(std):
    names, enums = set(), {}
    for f in glob.glob(os.path.join(std, "*.fs")):
        with open(f, encoding="utf-8") as fh:
            t = fh.read()
        for m in re.finditer(r"^export\s+(?:const|function|predicate|type|operator)\s+(\w+)", t, re.M):
            names.add(m.group(1))
        for m in re.finditer(r"^export\s+enum\s+(\w+)\s*\{(.*?)\n\}", t, re.M | re.S):
            body = re.sub(r"annotation\s*\{[^}]*\}", "", m.group(2))
            body = strip_comments_and_strings(body)
            enums[m.group(1)] = {x.strip() for x in body.split(",") if x.strip()}
    return names, enums


def api_check(code, std):
    names, enums = std_index(std)
    src = strip_comments_and_strings(code)
    local = set(re.findall(r"^(?:export\s+)?(?:function|const)\s+(\w+)", src, re.M))
    local_enums = {}
    for m in re.finditer(r"^export\s+enum\s+(\w+)\s*\{(.*?)\n\}", code, re.M | re.S):
        body = re.sub(r"annotation\s*\{[^}]*\}", "", m.group(2))
        local_enums[m.group(1)] = {x.strip() for x in body.split(",") if x.strip()}
    params = set()
    for m in re.finditer(r"function\s*\w*\s*\(([^)]*)\)", src):
        for p in m.group(1).split(","):
            p = p.strip()
            if p:
                params.add(p.split()[0])
    errs = []
    for nme in sorted(local):
        if nme in names:
            errs.append("name collides with a standard-library export: %s" % nme)
    for nme in sorted(local_enums):
        if nme in names or nme in enums:
            errs.append("enum name collides with a standard-library export: %s" % nme)
    called = set(re.findall(r"(?<![\.\w])([A-Za-z_]\w*)\s*\(", src))
    for c in sorted(called):
        if c in FS_KEYWORDS or c in local or c in names or c in params:
            continue
        errs.append("unknown function: %s" % c)
    for e, mem in set(re.findall(r"\b([A-Z]\w+)\.([A-Z][A-Z0-9_]*)\b", src)):
        pool = enums.get(e) or local_enums.get(e)
        if pool is None:
            if e not in names:
                errs.append("unknown enum: %s" % e)
            continue
        if mem not in pool:
            errs.append("unknown enum member: %s.%s" % (e, mem))
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--std", help="path to a FeatureScript standard-library checkout")
    a = ap.parse_args()
    if not a.std:
        for cand in (os.environ.get("FS_STD"), os.path.join(HERE, ".fs-std")):
            if cand and os.path.isfile(os.path.join(cand, "geometry.fs")):
                a.std = cand
                break
    files = sources()
    errs = lint_parts(files, a.std)
    code = assemble(files)
    for ln, text in onshape_lint.warnings(code):
        errs.append("SummitPushField.fs:%d: %s (Onshape editor warning)" % (ln, text))
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(code)
    print("wrote %s (%d lines)" % (os.path.relpath(OUT, os.getcwd()), code.count("\n")))
    if a.std:
        errs += api_check(code, a.std)
        print("standard-library API check against %s" % a.std)
    for e in errs:
        print("ERROR", e)
    if errs:
        sys.exit(1)
    print("OK: dialect lint, Onshape warning check%s passed" % (" and API check" if a.std else ""))


if __name__ == "__main__":
    main()
