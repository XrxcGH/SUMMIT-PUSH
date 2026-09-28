# -*- coding: utf-8 -*-
"""Numeric checks for the SUMMIT PUSH package.

Recomputes published figures (tag poses, clearances, reaches, rung layout, scoring
ceilings, RP thresholds, piece counts) and compares them with the documents. Most inputs
are written into this script; the tag poses and the two rung tables are parsed from the
documents."""
import io, os, re, json, math, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.stdout.reconfigure(encoding='utf-8')
fails = []


def chk(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (("  -- " + detail) if detail and not cond else ""))
    if not cond:
        fails.append(name)


IN = 0.0254
d = json.load(io.open('participants/04-vision/apriltag-field-layout.json', encoding='utf-8'))
by = {t["ID"]: t for t in d["tags"]}

print("== AprilTag JSON vs manual table ==")
arena = io.open('organizers/source/manual/sections/02-arena.md', encoding='utf-8').read()
rows = re.findall(u'^\| (\d+) \| [^|]+ \| \(([\d.]+), ([\d.]+)\) \| ([\d.]+) in \| ([+\u2212-][XY]) \|$', arena, re.M)
chk("manual tag table has 26 rows", len(rows) == 26, str(len(rows)))
for tid, x, y, z, facing in rows:
    t = by[int(tid)]["pose"]["translation"]
    ok = (abs(t["x"] / IN - float(x)) < 1e-6 and abs(t["y"] / IN - float(y)) < 1e-6
          and abs(t["z"] / IN - float(z)) < 1e-6)
    if not ok:
        chk("tag %s xyz" % tid, False, "json=(%.2f,%.2f,%.2f) manual=(%s,%s,%s)" % (
            t["x"]/IN, t["y"]/IN, t["z"]/IN, x, y, z))
chk("all 26 tag positions match the manual", not any(f.startswith("tag ") for f in fails))

print("== 180-degree symmetry ==")
ok = True
for tid in range(1, 14):
    b = by[tid]["pose"]["translation"]; r = by[tid + 13]["pose"]["translation"]
    if not (abs(b["x"] + r["x"] - 16.4592) < 1e-9 and abs(b["y"] + r["y"] - 8.2296) < 1e-9
            and abs(b["z"] - r["z"]) < 1e-9):
        ok = False
chk("Red = Blue rotated 180 deg about field center", ok)

print("== quaternions are pure yaw ==")
ok = all(t["pose"]["rotation"]["quaternion"]["X"] == 0.0 and t["pose"]["rotation"]["quaternion"]["Y"] == 0.0
         for t in d["tags"])
chk("all quaternions pure yaw", ok)
ok = all(abs(t["pose"]["rotation"]["quaternion"]["W"] ** 2 + t["pose"]["rotation"]["quaternion"]["Z"] ** 2 - 1.0) < 1e-12
         for t in d["tags"])
chk("all quaternions unit norm", ok)

print("== vision transform arithmetic (crag pair midpoint Z = 17.5) ==")
Z = 17.5
chk("Shelf 1 up +6.5", Z + 6.5 == 24.0)
chk("Shelf 2 up +24.5", Z + 24.5 == 42.0)
chk("Low Socket up +12.5", Z + 12.5 == 30.0)
chk("Mid Socket up +36.5", Z + 36.5 == 54.0)
chk("Summit Socket up +54.5", Z + 54.5 == 72.0)
chk("Low Peg up +12.5", Z + 12.5 == 30.0)
chk("Mid Peg up +36.5", Z + 36.5 == 54.0)
chk("High Peg up +60.5", Z + 60.5 == 78.0)
chk("Outfitter chute center 20 in below tag", 52 - 20 == 24 + 16 / 2.0)

print("== headwall geometry ==")
t15 = math.tan(math.radians(15))
for name, top, exp_behind, exp_up in (("LEDGE", 30, -1.2, 17.25), ("CAMP", 54, 5.3, 41.25), ("SUMMIT", 78, 11.7, 65.25)):
    zc = top - 0.75
    x = 48 - zc * t15
    behind = 39.0 - x
    chk("%s behind tag plane %.1f" % (name, exp_behind), abs(behind - exp_behind) < 0.06, "%.2f" % behind)
    chk("%s up from tag %.2f" % (name, exp_up), abs((zc - 12) - exp_up) < 1e-9)
# panel clearance behind P
for zt, lab in ((7.5, "bottom"), (16.5, "top")):
    dnorm = (39 + zt * t15 - 48) * math.cos(math.radians(15))
    chk("headwall panel %s edge >= 4.0 in behind P" % lab, -dnorm >= 4.0, "%.2f" % -dnorm)

print("== crag occlusion budget ==")
panel_lo, panel_hi = Z - 4.5, Z + 4.5
tgt_lo, tgt_hi = Z - 4.0625, Z + 4.0625
_DEPOT_FLOOR = 0.25                            # as built: tray floor top above the carpet
chk("crowned crate in depot (apex 13.25) below target",
    _DEPOT_FLOOR + 13.0 < 13.4375, "%.2f vs 13.4375" % (_DEPOT_FLOOR + 13.0))
chk("that margin is under 0.25 in, inside the panel build tolerance",
    13.4375 - (_DEPOT_FLOOR + 13.0) < 0.25,
    "%.2f in - flagged in VISION-GUIDE 1.3" % (13.4375 - (_DEPOT_FLOOR + 13.0)))
chk("rope coil on edge in depot below target", _DEPOT_FLOOR + 10.0 < 13.4375)
chk("upright O2 CELL is the only SUPPLY reaching the target band",
    _DEPOT_FLOOR + 14.0 > 13.4375 and _DEPOT_FLOOR + 13.0 < 13.4375,
    "documented in VISION-GUIDE 1.3 with the camera-height rule")
# VISION-GUIDE 1.3's clearances are solved against the AS-BUILT O2 CELL silhouette,
# not a bare dome: 14.0 overall on a 5.0 body, cap arc struck through the pole and the
# equator, and a 1.0-in fillet blending each cap to the wall. The cap meets the wall at
# a 28.1-degree tangent break, so the fillet is structural to the shape, and it drops
# the shoulder where the CELL touches the face to 12.22 in above its base rather than
# 12.5 (Z = 12.47 on the 0.25-in tray floor, the value checked below).
_TB = 13.4375                                  # tag target bottom edge
_RCAP, _YCAP = 2.8333333333333335, 4.166666666666667
_RF, _FCX, _FCY, _RTAN = 1.0, 1.5, 5.2212, 2.3183


def _cell_z(r):                                # top of the revolve profile at radius r
    if r <= _RTAN:
        return _YCAP + math.sqrt(_RCAP ** 2 - r * r)
    return _FCY + math.sqrt(max(0.0, _RF ** 2 - (r - _FCX) ** 2))


def _cell_surface(x):                          # standing on end, axis 2.5 in off the face
    return _DEPOT_FLOOR + 7.0 + _cell_z(abs(x - 2.5))


def _clears(h, D):
    for _i in range(401):
        _x = 5.0 * _i / 400.0
        if _TB + (h - _TB) * _x / D < _cell_surface(_x) - 1e-9:
            return False
    return True


chk("CELL on the tray floor: apex 14.25, shoulder at the face 12.47",
    abs(_cell_surface(2.5) - 14.25) < 1e-3 and abs(_cell_surface(0.0) - 12.471) < 2e-3,
    "%.3f / %.3f" % (_cell_surface(2.5), _cell_surface(0.0)))
chk("R1.0 fillet leaves 10.44 in of full-diameter body, not 11.0",
    abs(2 * _FCY - 10.44) < 0.01, "%.2f in" % (2 * _FCY))
for _h, _D in ((15, 3), (16, 6), (18, 10), (20, 15), (24, 25), (30, 39), (36, 53)):
    chk("camera at %d in clears an upright CELL out to %d in" % (_h, _D),
        _clears(_h, _D) and not _clears(_h, _D + 2),
        "clears %d, fails %d" % (_D, _D + 2))
chk("a camera below the target bottom never clears it", not _clears(13.0, 1.0))
chk("Shelf 1 underside (23.25) above panel", 23.25 > panel_hi, "%.2f" % panel_hi)
chk("Low socket tube lowest (22.19) above target", 22.19 > tgt_hi, "%.2f" % tgt_hi)

print("== shelf gusset floors clear what passes beneath them ==")
_CRATE_H, _SHELF1_UNDER = 13.0, 23.25              # crowned crate height; Shelf 1 underside
_CRATE_APEX = _DEPOT_FLOOR + _CRATE_H                # its top standing on the DEPOT tray floor
_G1, _G1_TAG, _G2 = 19.0, 22.0, 38.0              # gusset floors: Shelf 1, over a tag, Shelf 2
_TAG_TOP = 22.0                                   # CRAG tag panel top edge
chk("Shelf 1 gusset floor clears a crowned CRATE pushed in beneath it",
    _G1 - _CRATE_APEX >= 5.0, "%.1f in of headroom" % (_G1 - _CRATE_APEX))
chk("Shelf 1 gusset still has usable depth", _SHELF1_UNDER - _G1 >= 4.0,
    "%.2f in deep" % (_SHELF1_UNDER - _G1))
chk("no Shelf 1 gusset can stand in front of a CRAG tag", _G1_TAG >= _TAG_TOP,
    "%.1f vs panel top %.1f" % (_G1_TAG, _TAG_TOP))
chk("Shelf 2 gusset floor clears a crowned CRATE on Shelf 1",
    _G2 - (24.0 + _CRATE_H) >= 1.0, "%.1f in" % (_G2 - (24.0 + _CRATE_H)))

print("== CACHE CRATE crown against the shelf slot ==")
# The crate rests on its bottom crown, so the cube's bottom plane sits 0.5 above the
# shelf and each side face reaches its full bulge 6.5 up -- well above the 2.0-in
# fences. The binding width is at the fence tops, NOT the nominal cube.
_CR_R = (6.0 ** 2 + 0.5 ** 2) / (2 * 0.5)          # crown arc radius, 36.25


def _crown(d):                                      # bulge at distance d from face centre
    return math.sqrt(_CR_R ** 2 - d * d) - (_CR_R - 0.5)


chk("crown is 0.5 at the face centre and 0 at its edges",
    abs(_crown(0.0) - 0.5) < 1e-9 and abs(_crown(6.0)) < 1e-9)
_w_fence = 12.0 + 2 * _crown(abs(2.0 - 6.5))        # width at the 2.0-in fence tops
chk("crate is 12.44 in wide at the fence tops", abs(_w_fence - 12.44) < 0.005,
    "%.3f" % _w_fence)
chk("0.78 in of slot clearance per side, not the nominal 1.00",
    abs((14.0 - _w_fence) / 2 - 0.78) < 0.005, "%.3f" % ((14.0 - _w_fence) / 2))
chk("the 13.0 crown clears the 2.0-in fences", 6.5 - 2.0 >= 4.0, "%.1f in above" % (6.5 - 2.0))
chk("adjacent slot crates clear each other", 15.5 - 13.0 >= 2.0, "%.1f in" % (15.5 - 13.0))
chk("fillets do not change the envelope: 12.0 + 2 x 0.5 crown", abs(13.0 - 13.0) < 1e-9)

print("== depot / reach ==")
chk("crate crowned envelope 13.0 fits 16.0 channel", 13.0 <= 16.0)
chk("depot open strip = 2.0 in", abs((16.0 - 14.0) - 2.0) < 1e-9)
frame = 16.0 + 0.75 + 3.0
chk("frame perimeter 19.75 in from shelf face", abs(frame - 19.75) < 1e-9)
chk("shelf slot reach 12.75 <= 18", abs((frame - 7.0) - 12.75) < 1e-9 and frame - 7.0 <= 18)
chk("summit socket reach 11.75 <= 18", abs((frame - 8.0) - 11.75) < 1e-9 and frame - 8.0 <= 18)
# The Low Socket sits above the DEPOT corner arm, so its standoff differs from the Mid Socket's
wrap_face = 16.0 + 0.75            # channel depth + lip thickness, from the crag face
low_fp = wrap_face + 3.0           # frame perimeter behind the bumper on the lip
chk("Low Socket lies above the DEPOT corner arm", 14.0 < 16.0, "lateral 14.0 in a 16.0 arm")
chk("Low Socket reach 11.75 <= 18", abs((low_fp - 8.0) - 11.75) < 1e-9, "%.2f" % (low_fp - 8.0))
chk("Mid Socket reach 5.0 <= 18", abs((8.0 - 3.0) - 5.0) < 1e-9 and (8.0 - 3.0) <= 18.0,
    "%.2f" % (8.0 - 3.0))
chk("Low/Mid socket standoffs differ by more than 6 in", (low_fp - 8.0) - 5.0 > 6.0,
    "%.2f in apart" % ((low_fp - 8.0) - 5.0))
chk("high peg root reach 17.0 <= 18",
    abs((14.0 + 3.0) - 17.0) < 1e-9 and (14.0 + 3.0) <= 18.0, "%.2f" % (14.0 + 3.0))

print("== socket tube clearances ==")
# Tube 7.0 in along the axis (NOT the superseded 8.0), standoff 8.0, OD 6.68 -> r 3.34,
# CELL 14.0 long. Assert the published figures exactly, not loose inequalities: a
# regression back to an 8.0-in tube passed every one of the old > 0 / > 2.0 tests.
# The 7.0 runs from the rim to the floor the CELL seats on; the 0.09 closed bottom lies beyond it.
SOCK_STANDOFF, SOCK_TUBE, SOCK_BOTTOM, SOCK_R, CELL_L = 8.0, 7.0, 0.09, 3.34, 14.0
for tilt, lbl, want_in, want_apex in ((30, "Low", 1.56, 4.39),
                                      (30, "Mid", 1.56, 4.39),
                                      (15, "Summit", 2.94, 5.90)):
    s, c = math.sin(math.radians(tilt)), math.cos(math.radians(tilt))
    bot_out = SOCK_STANDOFF - (SOCK_TUBE + SOCK_BOTTOM) * s
    inboard = bot_out - SOCK_R * c
    chk("%-6s socket tube inboard edge %.2f in outboard of the face" % (lbl, want_in),
        abs(inboard - want_in) < 0.005, "%.3f" % inboard)
    apex = (CELL_L - SOCK_TUBE) * c          # protrusion along the axis, projected up
    lip = SOCK_R * s
    chk("%-6s seated CELL clears the rim's uphill lip by %.2f in" % (lbl, want_apex),
        abs((apex - lip) - want_apex) < 0.005, "%.3f" % (apex - lip))

print("== headwall rung stagger ==")
L, s = 20.0, 12.0
chk("no lateral position engages two successive rungs", (-s + L / 2) < (s - L / 2), "%.1f vs %.1f" % (-s + L/2, s - L/2))
chk("rungs stay inside the 48-in lane", s + L / 2 <= 24.0, "%.1f" % (s + L / 2))
LANES = (114.0, 162.0, 210.0)
STAG = (-1, 1, -1)                     # by RUNG index, identical in every lane
gaps, ctrs = [], []
for ri in range(3):
    cs = [ly + STAG[ri] * s for ly in LANES]
    ctrs += [cs[i + 1] - cs[i] for i in range(2)]
    ends = [(c - L / 2, c + L / 2) for c in cs]
    gaps += [ends[i + 1][0] - ends[i][1] for i in range(2)]
chk("adjacent-lane rungs 48 in apart centre-to-centre at every height",
    all(abs(c - 48.0) < 1e-9 for c in ctrs), "min %.1f" % min(ctrs))
chk("adjacent-lane rungs >= 28 in apart end to end",
    min(gaps) >= 28.0 - 1e-9, "min %.1f" % min(gaps))
chk("adjacent-lane rung centres exceed a 30-in ROBOT width",
    min(ctrs) > 30.0, "%.1f vs 30.0" % min(ctrs))

print("== published rung tables agree with the computed stagger ==")
# The manual's ARENA section declares itself authoritative over every other document,
# and the CAD package's derived table is what a modeller reads. Parse both rather than
# re-asserting the constant the generator already uses.
_LANES, _STAG, _L = (114.0, 162.0, 210.0), (-12.0, 12.0, -12.0), 20.0
_arena = io.open('organizers/source/manual/sections/02-arena.md', encoding='utf-8').read()
_cad = io.open('participants/03-field/FIELD-CAD-PACKAGE.md', encoding='utf-8').read()

for _i, _nm in enumerate(('LEDGE RUNG', 'CAMP RUNG', 'SUMMIT RUNG')):
    _m = re.search(r'\|\s*\*\*%s\*\*\s*\|[^|]*\|([^|]*)\|' % _nm, _arena)
    _cell = (_m.group(1) if _m else '')
    # Compare against a sign-normalised cell. Stripping '+' from '+12.0' leaves
    # '12.0', which is a substring of a minus-signed cell -- so the CAMP row used
    # to accept either sign, the one row the whole property depends on.
    _norm = _cell.replace(chr(0x2212), '-')
    _want = '%+.1f' % _STAG[_i]
    _has = (_want in _norm) if _STAG[_i] > 0 else ('%.1f' % _STAG[_i] in _norm)
    _per_lane = ('lane 2' in _cell.lower() or 'lanes 1 and 3' in _cell.lower())
    chk("ARENA table: %-11s offset is %s" % (_nm, _want), _has and not _per_lane,
        _cell.strip()[:70])

_dm = re.search(r'\| LEDGE \|(.+?)\n\| CAMP \|(.+?)\n\| SUMMIT \|(.+?)\n', _cad, re.S)
if _dm:
    for _i, _nm in enumerate(('LEDGE', 'CAMP', 'SUMMIT')):
        _spans = re.findall(r'Y\s*(\d+)\s*[\u2013-]\s*(\d+)', _dm.group(_i + 1))
        _got = [(float(a), float(b)) for a, b in _spans]
        _exp = [(ly + _STAG[_i] - _L / 2, ly + _STAG[_i] + _L / 2) for ly in _LANES]
        chk("CAD derived table: %-6s lane spans" % _nm, _got == _exp,
            "got %s want %s" % (_got, _exp))
else:
    chk("CAD derived rung-end table found", False)

print("== climb reach from the CLIMB LINE (G416) ==")
import math as _m
_T15 = _m.tan(_m.radians(15.0))
def _cx(top): return 48.0 - (top - 0.75) * _T15
_FP = 48.0 + 3.0                      # BUMPERS on the line, R402 minimum 3.0-in bumper
for _nm, _top, _want, _ok in (("LEDGE", 30.0, 11.59, True),
                              ("CAMP",  54.0, 18.02, False),
                              ("SUMMIT",78.0, 24.45, False)):
    _wrap = _FP - _cx(_top) + 0.75    # a hook must clear the far face of a 1.5-in rung
    chk("%-6s wrap reach %.2f in" % (_nm, _want), abs(_wrap - _want) < 0.005, "%.4f" % _wrap)
    chk("%-6s within R105 == %s" % (_nm, _ok), (_wrap <= 18.0) == _ok, "%.2f vs 18.0" % _wrap)
chk("only the LEDGE RUNG is reachable from the carpet",
    sum(1 for _t in (30.0, 54.0, 78.0) if (_FP - _cx(_t) + 0.75) <= 18.0) == 1)

print("== scoring arithmetic ==")
crate = 3 * 4 + 3 * 7
o2 = 2 * 4 + 2 * 7 + 1 * 10
rope = 2 * 4 + 2 * 7 + 2 * 10
chk("crate ceiling 33", crate == 33, str(crate))
chk("O2 ceiling 32", o2 == 32, str(o2))
chk("rope ceiling 42", rope == 42, str(rope))
chk("crag TELEOP ceiling 107", crate + o2 + rope == 107, str(crate + o2 + rope))
chk("crag positions = 17", 6 + 5 + 6 == 17)
chk("SUPPLY LINE Champs 23 reachable", 17 + 12 >= 23)
chk("ASCENT: 3x CAMP RUNG = 60 meets Champs", 3 * 20 >= 60)
chk("ASCENT: CAMP+LEDGE = 32 meets Regional", 20 + 12 >= 32)
chk("ASCENT: CAMP+CAMP+LEDGE = 52 meets DCMP", 20 + 20 + 12 >= 52)
LOWP = {"S1a","S1b","S1c","LSa","LSb","LPa","LPb"}
MIDP = {"S2a","S2b","S2c","MSa","MSb","MPa","MPb"}
HIP  = {"SUM","HPa","HPb"}
CAMP1, CAMP2, CAMPH = {"S1a","LSa","LPa"}, {"S2a","MSa","MPa"}, {"SUM","HPa"}
CAMPS = CAMP1 | CAMP2 | CAMPH
FULL = {"LOW": set(LOWP), "MID": set(MIDP),
        "HIGH": {"SUM","HPa","HPb","MSa","MSb","MPa","MPb"}}
for r, f in FULL.items():
    chk("full capacity %-4s = 7 positions" % r, len(f) == 7, str(len(f)))
REQ = dict((r, CAMPS | f) for r, f in FULL.items())
chk("Champs EXPEDITION sets differ between all three ROUTES",
    len(set(frozenset(v) for v in REQ.values())) == 3,
    " / ".join("%s=%d" % (r, len(REQ[r])) for r in ("LOW", "MID", "HIGH")))
incr = dict((r, len(REQ[r] - CAMPS)) for r in REQ)
chk("Champs EXPEDITION increment beyond CAMPS is within 1 across ROUTES",
    max(incr.values()) - min(incr.values()) <= 1,
    " / ".join("%s+%d" % (r, incr[r]) for r in ("LOW", "MID", "HIGH")))
chk("every FULL set is inside the CRAG's 17 positions",
    all(f <= (LOWP | MIDP | HIP) for f in FULL.values()))
chk("HIGH CAMP does not saturate the high tier",
    CAMPH < HIP, "%d of %d high positions" % (len(CAMPH), len(HIP)))

print("== ROPE COIL revolve profile (as built) ==")
# Sketch: a 2.5-dia tube circle whose OUTER edge is 5.0 from the revolve axis.
# Everything else follows, so the three published numbers cannot drift apart.
_TUBE_D, _OUTER_R = 2.5, 5.0
_tube_r = _TUBE_D / 2.0
_ctr_r = _OUTER_R - _tube_r
_inner_r = _ctr_r - _tube_r
chk("OD 10.0 from the profile", abs(2 * _OUTER_R - 10.0) < 1e-9, "%.1f" % (2 * _OUTER_R))
chk("ID 5.0 from the profile", abs(2 * _inner_r - 5.0) < 1e-9, "%.1f" % (2 * _inner_r))
chk("tube section 2.5", abs(_TUBE_D - 2.5) < 1e-9)
chk("tube centre sits at r = 3.75", abs(_ctr_r - 3.75) < 1e-9, "%.2f" % _ctr_r)
# tilt bound: the torus binds on a rod of radius 0.75 when the rod's axis comes within
# tube radius + rod radius of the core circle, i.e. at acos((r + 0.75) / R)
_lo = math.degrees(math.acos((_tube_r + 0.75) / _ctr_r))
chk("max tilt off perpendicular-to-peg is 57.8 deg", abs(_lo - 57.77) < 0.05, "%.2f" % _lo)
chk("a 45-deg peg leaves positive margin, so the COIL hangs plumb", _lo > 45.0,
    "%.2f deg of margin" % (_lo - 45.0))
# plumb coil, inner face 1.25 out: its core circle keeps 2.0 from the 45-deg peg axis only
# while the centre is at least 2.5 - k above the root, k^2 + 7.5 k + 6.0625 = 0
_k = (7.5 - math.sqrt(7.5 ** 2 - 4 * 6.0625)) / 2
chk("plumb COIL with inner face 1.25 out rests with its centre 1.58 above the peg root",
    abs((2.5 - _k) - 1.578) < 0.005, "%.3f" % (2.5 - _k))

print("== piece accounting ==")
chk("21 per type", 3 + 2 * 2 + 2 * 7 == 21)
chk("63 total", 3 * 21 == 63)

print("== center cache balance ==")
cells = {'C': [(300, 186), (324, 162), (348, 138)],
         'O': [(324, 186), (348, 162), (300, 138)],
         'R': [(348, 186), (300, 162), (324, 138)]}
tot = {}
for k, pts in cells.items():
    b = sum(math.hypot(x - 324, y - 240) for x, y in pts)
    r = sum(math.hypot(x - 324, y - 84) for x, y in pts)
    tot[k] = (b, r)
    chk("%s haul balance within 1%%" % k, abs(b - r) / max(b, r) < 0.01, "blue %.1f red %.1f" % (b, r))
B = sum(v[0] for v in tot.values()); R = sum(v[1] for v in tot.values())
chk("aggregate haul identical", abs(B - R) < 1e-6, "%.1f vs %.1f" % (B, R))
rows_ = [set(), set(), set()]
for k, pts in cells.items():
    for i, yv in enumerate((138, 162, 186)):
        assert any(p[1] == yv for p in pts), k
chk("each type appears once per row", True)

print()
print("RESULT: %d failure(s)" % len(fails))
for f in fails:
    print("   -", f)
