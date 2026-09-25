# -*- coding: utf-8 -*-
"""
Run the independent element checks in verify/checks/check_*.py against one off-line build.

    python 03-field/featurescript/verify/run_checks.py [name ...]

Each check module defines `run(f)` taking an inspect_field.Field and returning a list of
(label, ok, detail) tuples.  The expected values in those modules are derived from the
package documents (FIELD-CAD-PACKAGE.md, MATERIALS-AND-COLORS.md, the Game Manual), not from
the part code, so they check the generator rather than restate it.
"""
import glob
import importlib.util
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from inspect_field import Field  # noqa: E402


def main():
    want = set(sys.argv[1:])
    files = sorted(glob.glob(os.path.join(HERE, "checks", "check_*.py")))
    if want:
        files = [f for f in files if os.path.basename(f)[6:-3] in want]
    t0 = time.time()
    f = Field()
    print("built field in %.1f s" % (time.time() - t0))
    total = bad = 0
    for path in files:
        name = os.path.basename(path)[6:-3]
        spec = importlib.util.spec_from_file_location("check_" + name, path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            res = mod.run(f)
        except Exception as e:  # noqa: BLE001
            print("[%s] ERROR %s: %s" % (name, type(e).__name__, e))
            bad += 1
            total += 1
            continue
        nb = sum(1 for r in res if not r[1])
        total += len(res)
        bad += nb
        print("[%s] %d/%d pass" % (name, len(res) - nb, len(res)))
        for label, ok, detail in res:
            if not ok:
                print("    FAIL %s — %s" % (label, detail))
    print("RESULT: %d of %d checks pass" % (total - bad, total))
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
