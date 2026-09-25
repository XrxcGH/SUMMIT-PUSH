# -*- coding: utf-8 -*-
"""
Build the SUMMIT PUSH field off-line and verify it.

    python 03-field/featurescript/verify/run.py [--quick] [--only crags,tags,...] [--lit] [--stacked]

Transpiles the part code in src/2x-4x_*.fs to Python (fs2py), runs it against the
OpenCascade twin of the FeatureScript kernel (kernel_occ), then checks:

  * build      — every element builds with no kernel error; every body valid, named, styled
  * self-check — the same selfCheck() the Onshape feature runs (CRITICAL ledger dimensions)
  * grouping   — groupField() puts every element body in exactly one composite part
  * palette    — every palette value matches the hex in MATERIALS-AND-COLORS.md
  * tags       — all 26 panels match 04-vision/apriltag-field-layout.json exactly
  * supplies   — 63 pieces, 21 per type, each weighing its published weight
  * interference — no two bodies share volume (contact is fine; --quick skips it)

Writes verify/report.json and prints a summary.  Exit status non-zero on any failure.
Requires: pip install cadquery-ocp numpy
"""
import argparse
import glob
import json
import math
import os
import re
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PKG = os.path.dirname(os.path.dirname(ROOT))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

import fs2py  # noqa: E402
import kernel_occ as K  # noqa: E402

DEFAULT_OPTS = {"perimeter": True, "walls": True, "crags": True, "headwalls": True, "tape": True,
                "tags": True, "decals": True, "staged": True, "stock": True, "lit": False,
                "fieldLed": "DARK", "pairs": "SIDE", "cosmetics": True, "forecast": "WHITEOUT",
                "routeBlue": "LOW", "routeRed": "LOW"}


def load_part_code():
    ns = {}
    for name in dir(K):
        if not name.startswith("_"):
            ns[name] = getattr(K, name)
    exec(fs2py.PRELUDE, ns)
    src_files = sorted(f for f in glob.glob(os.path.join(ROOT, "src", "*.fs"))
                       if re.match(r"^[2-4]\d_", os.path.basename(f)))
    py = []
    for f in src_files:
        with open(f, encoding="utf-8") as fh:
            py.append(fs2py.transpile(fh.read(), os.path.relpath(f, ROOT)))
    code = "\n".join(py)
    exec(fs2py.compile_part(code, "<part-code>"), ns)
    return ns, code


def fs_line(code, exc):
    """Map a traceback in the transpiled part code back to src file:line."""
    tb = traceback.extract_tb(exc.__traceback__)
    lines = code.splitlines()
    out = []
    for fr in tb:
        if fr.filename == "<part-code>" and 0 < fr.lineno <= len(lines):
            m = re.search(r"# (src/\S+:\d+)$", lines[fr.lineno - 1])
            if m:
                out.append(m.group(1))
    return out


# ---------------------------------------------------------------------------------------
# checks that need Python (not expressible in the part code)
# ---------------------------------------------------------------------------------------
def body_list(ctx):
    out = []
    for key, rec in ctx.bodies.items():
        for i, s in enumerate(rec["solids"]):
            out.append((key, i, s, rec))
    return out


def bbox(shape):
    b = K.Bnd_Box()
    K.BRepBndLib.AddOptimal_s(shape, b, False, False)
    return K._box6(b)


def interference(ctx, tol_vol=1e-4):
    items = body_list(ctx)
    boxes = [bbox(s) for (_, _, s, _) in items]
    hits = []
    n = len(items)
    for i in range(n):
        a = boxes[i]
        for j in range(i + 1, n):
            b = boxes[j]
            if a[0] >= b[3] - 1e-6 or b[0] >= a[3] - 1e-6 or a[1] >= b[4] - 1e-6 or b[1] >= a[4] - 1e-6 \
                    or a[2] >= b[5] - 1e-6 or b[2] >= a[5] - 1e-6:
                continue
            com = K.BRepAlgoAPI_Common(items[i][2], items[j][2])
            if not com.IsDone():
                hits.append((items[i][3]["name"], items[j][3]["name"], float("nan")))
                continue
            v = K._volume(K._solids(com.Shape()))
            if v > tol_vol:
                hits.append((items[i][3]["name"] or str(items[i][0]), items[j][3]["name"] or str(items[j][0]), v))
    return hits


def check_supplies(ctx):
    errs, info = [], {}
    want = {"CACHE CRATE": 2.0, "O2 CELL": 1.5, "ROPE COIL": 1.0}
    counts = {k: 0 for k in want}
    for key, rec in ctx.bodies.items():
        nm = rec["name"] or ""
        for k in want:
            if nm.startswith(k + " - "):
                counts[k] += len(rec["solids"])
                vol = K._volume(rec["solids"])
                mass = rec["mat"]["density"] * vol * K.IN3 / K.LB
                if abs(mass - want[k]) > 1e-6:
                    errs.append("%s weighs %.6f lb, expected %.1f" % (nm, mass, want[k]))
                info.setdefault(k, {"volume_in3": round(vol, 3), "density_kg_m3": round(rec["mat"]["density"], 3),
                                    "mass_lb": round(mass, 6)})
    for k, c in counts.items():
        if c != 21:
            errs.append("%s count %d, expected 21" % (k, c))
    return errs, info


def check_tags(ctx, ns):
    errs = []
    with open(os.path.join(PKG, "04-vision", "apriltag-field-layout.json")) as fh:
        js = json.load(fh)
    jt = {t["ID"]: t for t in js["tags"]}
    table = ns["tagTable"]()
    if sorted(t[0] for t in table) != list(range(1, 27)) or sorted(jt) != list(range(1, 27)):
        errs.append("tag IDs are not exactly 1..26")
    for t in table:
        tid, x, y, z, yaw = t[0], t[1], t[2], t[3], t[4]
        j = jt[tid]["pose"]
        tr = j["translation"]
        for got, want, ax in ((x * 0.0254, tr["x"], "x"), (y * 0.0254, tr["y"], "y"), (z * 0.0254, tr["z"], "z")):
            if abs(got - want) > 1e-4:
                errs.append("tag %d %s: model %.5f m vs JSON %.5f m" % (tid, ax, got, want))
        q = j["rotation"]["quaternion"]
        jyaw = math.degrees(2 * math.atan2(q["Z"], q["W"])) % 360
        if abs(((yaw - jyaw) + 180) % 360 - 180) > 1e-6:
            errs.append("tag %d yaw: model %.3f vs JSON %.3f" % (tid, yaw, jyaw))
        # the built panel: its front face centre is the tag pose, its normal the facing
        rec = ctx.bodies.get(K.Id(("F", "tags", "tag%d" % tid, "ex")))
        if rec is None:
            errs.append("tag %d panel not built" % tid)
            continue
        dec = rec.get("decal")
        if dec is None:
            errs.append("tag %d has no decal" % tid)
            continue
        o = np.array(dec["origin"])
        if np.linalg.norm(o - np.array([x, y, z])) > 1e-9:
            errs.append("tag %d decal origin %s" % (tid, o))
        n = np.array(dec["normal"])
        if np.linalg.norm(n - np.array([math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0])) > 1e-9:
            errs.append("tag %d decal normal %s" % (tid, n))
        black = set(dec["black"])
        ref = reference_black_cells(tid)
        if black != ref:
            errs.append("tag %d decal bit pattern differs from tag36h11" % tid)
    return errs


def reference_black_cells(tid):
    """Black cells straight from AprilRobotics tag36h11.c (independent of the part code)."""
    codes = [0xd7e00984b, 0xdda664ca7, 0xdc4a1c821, 0xe17b470e9, 0xef91d01b1, 0xf429cdd73, 0x5da29225,
             0x1106cba43, 0x223bed79d, 0x21f51213c, 0x33eb19ca6, 0x3f76eb0f8, 0x469a97414, 0x45dcfe0b0,
             0x4a6465f72, 0x51801db96, 0x5eb946b4e, 0x68a7cc2ec, 0x6f0ba2652, 0x78765559d, 0x87b83d129,
             0x86cc4a5c5, 0x8b64df90f, 0x9c577b611, 0xa3810f2f5, 0xaf4d75b83, 0xb59a03fef]
    bx = [1, 2, 3, 4, 5, 2, 3, 4, 3, 6, 6, 6, 6, 6, 5, 5, 5, 4, 6, 5, 4, 3, 2, 5, 4, 3, 4, 1, 1, 1, 1, 1, 2, 2, 2, 3]
    by = [1, 1, 1, 1, 1, 2, 2, 2, 3, 1, 2, 3, 4, 5, 2, 3, 4, 3, 6, 6, 6, 6, 6, 5, 5, 5, 4, 6, 5, 4, 3, 2, 5, 4, 3, 4]
    code = codes[tid]
    white = {(by[i] + 1, bx[i] + 1) for i in range(36) if (code >> (35 - i)) & 1}
    return {(r, c) for r in range(1, 9) for c in range(1, 9) if (r, c) not in white}


def check_palette(ns):
    errs = []
    with open(os.path.join(PKG, "03-field", "MATERIALS-AND-COLORS.md"), encoding="utf-8") as fh:
        md = fh.read()
    spec = {}
    for m in re.finditer(r"`([a-z0-9-]+)`\s*\|\s*`(#[0-9A-Fa-f]{6})`", md):
        spec[m.group(1)] = m.group(2)
    for m in re.finditer(r"\|\s*[A-Z0-9 ]+\|\s*`([a-z0-9-]+)`\s*\|\s*`(#[0-9A-Fa-f]{6})`", md):
        spec[m.group(1)] = m.group(2)
    pal = ns["PAL"]
    for tok, hx in spec.items():
        if tok not in pal:
            errs.append("palette token %s (%s) missing from PAL" % (tok, hx))
            continue
        rgb = tuple(int(hx[i:i + 2], 16) for i in (1, 3, 5))
        if tuple(pal[tok]) != rgb:
            errs.append("palette %s: PAL %s vs spec %s %s" % (tok, pal[tok], hx, rgb))
    for tok, hx in (("estop-red", "#CC2020"), ("tag-black", "#111111")):
        rgb = tuple(int(hx[i:i + 2], 16) for i in (1, 3, 5))
        if tuple(pal[tok]) != rgb:
            errs.append("palette %s: PAL %s vs spec %s" % (tok, pal[tok], hx))
    return errs, len(spec)


def check_bodies(ctx):
    errs = []
    for key, rec in ctx.bodies.items():
        if not rec["name"]:
            errs.append("unnamed body %s" % (key,))
        if rec["rgb"] is None:
            errs.append("no appearance on %s" % (rec["name"] or key,))
        if not rec["mat"] or not rec["mat"].get("density"):
            errs.append("no material on %s" % (rec["name"] or key,))
        for s in rec["solids"]:
            if not K.BRepCheck_Analyzer(s).IsValid():
                errs.append("invalid solid in %s" % (rec["name"] or key,))
    count = {}
    for n in K.part_names(ctx):
        count[n] = count.get(n, 0) + 1
    for n, c in sorted(count.items()):
        if c > 1:
            errs.append("%d parts share the name %r" % (c, n))
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma list of options to enable (others off)")
    ap.add_argument("--quick", action="store_true", help="skip the all-pairs interference check")
    ap.add_argument("--lit", action="store_true")
    ap.add_argument("--stacked", action="store_true")
    ap.add_argument("--json", default=os.path.join(HERE, "report.json"))
    a = ap.parse_args()
    opts = dict(DEFAULT_OPTS)
    if a.only:
        on = set(a.only.split(","))
        for k in ("perimeter", "walls", "crags", "headwalls", "tape", "tags", "staged", "stock"):
            opts[k] = k in on
        opts["decals"] = opts["tags"]
    opts["lit"] = a.lit
    if a.stacked:
        opts["pairs"] = "STACKED"
    report = {"options": opts, "sections": {}}
    fails = 0
    t0 = time.time()
    ns, code = load_part_code()
    ctx = K.Registry()
    fid = K.Id(("F",))
    try:
        ns["buildField"](ctx, fid, opts)
    except Exception as e:  # noqa: BLE001
        print("BUILD FAILED:", type(e).__name__, e)
        print("  at", " <- ".join(reversed(fs_line(code, e))))
        report["sections"]["build"] = {"ok": False, "error": str(e), "where": fs_line(code, e)}
        with open(a.json, "w") as fh:
            json.dump(report, fh, indent=1)
        sys.exit(2)
    nsol = sum(len(r["solids"]) for r in ctx.bodies.values())
    print("build: %d bodies (%d solids) in %.1f s; %d warning(s)" % (len(ctx.bodies), nsol, time.time() - t0, len(ctx.warnings)))
    for w in ctx.warnings:
        print("  WARNING", w)
    report["sections"]["build"] = {"ok": True, "bodies": len(ctx.bodies), "solids": nsol, "warnings": ctx.warnings}

    errs = check_bodies(ctx)
    print("bodies: %s" % ("OK — every body valid, uniquely named, coloured and given a material" if not errs else "%d problem(s)" % len(errs)))
    for e in errs[:40]:
        print("  FAIL", e)
    fails += len(errs)
    report["sections"]["bodies"] = errs

    checks = ns["selfCheck"](ctx, fid, opts)
    bad = ns["failures"](checks)
    print("self-check: %d of %d dimension checks pass" % (len(checks) - len(bad), len(checks)))
    for b in bad:
        print("  FAIL", b)
    fails += len(bad)
    report["sections"]["selfcheck"] = {"total": len(checks), "failures": bad,
                                       "checks": [[c[0], c[1], c[2], c[3]] for c in checks]}

    # composite grouping, as the feature does last: every element body in exactly one group
    ns["groupField"](ctx, fid, opts)
    comps = getattr(ctx, "composites", {})
    member = {}
    for c in comps.values():
        for k in c["members"]:
            member.setdefault(k, []).append(c["name"])
    gerr = []
    for k, rec in ctx.bodies.items():
        solo = k[:2] in (("F", "carpet"), ("F", "supplies"))
        if not solo and len(member.get(k, [])) != 1:
            gerr.append("%s is in %d composite parts" % (rec["name"], len(member.get(k, []))))
    print("grouping: %d composite parts%s" % (len(comps), "; every element body in exactly one" if not gerr else "; %d problem(s)" % len(gerr)))
    for e in gerr[:20]:
        print("  FAIL", e)
    fails += len(gerr)
    report["sections"]["grouping"] = {"composites": sorted(c["name"] for c in comps.values()), "errors": gerr}

    perr, ntok = check_palette(ns)
    print("palette: %d spec tokens, %s" % (ntok, "all match" if not perr else "%d mismatch(es)" % len(perr)))
    for e in perr:
        print("  FAIL", e)
    fails += len(perr)
    report["sections"]["palette"] = perr

    if opts["tags"]:
        terr = check_tags(ctx, ns)
        print("tags: %s" % ("26 panels match apriltag-field-layout.json and tag36h11" if not terr else "%d problem(s)" % len(terr)))
        for e in terr:
            print("  FAIL", e)
        fails += len(terr)
        report["sections"]["tags"] = terr

    if opts["staged"] and opts["stock"]:
        serr, sinfo = check_supplies(ctx)
        print("supplies: %s" % ("63 pieces, 21 per type, each at its published weight" if not serr else "%d problem(s)" % len(serr)))
        for k, v in sinfo.items():
            print("  %-12s volume %9.3f in^3  density %8.3f kg/m^3  mass %.4f lb" % (k, v["volume_in3"], v["density_kg_m3"], v["mass_lb"]))
        for e in serr:
            print("  FAIL", e)
        fails += len(serr)
        report["sections"]["supplies"] = {"errors": serr, "info": sinfo}

    if not a.quick:
        t1 = time.time()
        hits = interference(ctx)
        print("interference: %s (%.0f s)" % ("none — no two bodies share volume" if not hits else "%d pair(s)" % len(hits), time.time() - t1))
        for h in hits[:60]:
            print("  FAIL %s  x  %s  : %.5f in^3" % h)
        fails += len(hits)
        report["sections"]["interference"] = [list(h) for h in hits]

    mass = {}
    for rec in ctx.bodies.values():
        v = K._volume(rec["solids"])
        m = rec["mat"]["density"] * v * K.IN3 / K.LB if rec["mat"] else 0
        grp = re.sub(r" \d+$", "", (rec["name"] or "?").split(" - ")[0])
        mass[grp] = mass.get(grp, 0) + m
    report["sections"]["mass_lb_by_name"] = {k: round(v, 3) for k, v in sorted(mass.items())}
    report["failures"] = fails
    with open(a.json, "w") as fh:
        json.dump(report, fh, indent=1)
    print("RESULT: %s" % ("PASS" if fails == 0 else "%d failure(s)" % fails))
    sys.exit(0 if fails == 0 else 1)


if __name__ == "__main__":
    main()
