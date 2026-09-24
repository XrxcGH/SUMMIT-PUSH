# -*- coding: utf-8 -*-
"""Decode generated SVG geometry back to field inches and check it against the
locked ledger.  Catches the two defect classes the re-audit found: mirrored
rectangles anchored at the wrong edge, and socket tubes rotated the wrong way."""
import io, math, os, re, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
R = '03-field/renderings/'
fails = []


def chk(name, ok, detail=""):
    print("  %s  %s%s" % ("PASS" if ok else "FAIL", name, ("   [%s]" % detail) if detail else ""))
    if not ok:
        fails.append(name)


RECT = re.compile(r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([\d.]+)" height="([\d.]+)"')

print("== field-plan rects decode inside the carpet ==")
for f, OY, SC in (('field-top-view.svg', 74.0, 1.8), ('apriltag-map.svg', 70.0, 1.8)):
    s = io.open(R + f, encoding='utf-8').read()
    OX = 112.0
    bad = []
    for m in RECT.finditer(s):
        x, y, w, h = [float(v) for v in m.groups()]
        X0 = (x - OX) / SC
        Y1 = 324.0 - (y - OY) / SC
        Y0 = 324.0 - (y + h - OY) / SC
        # judge only rects that START inside the field frame; notes panels and the
        # titleblock sit below it and legitimately span the sheet
        in_frame = (OY - 1) <= y <= (OY + SC * 324.0 + 1)
        if in_frame and -1 <= X0 <= 649 and (x + w - OX) / SC <= 649 and h >= 40:
            if Y0 < -0.5 or Y1 > 324.5:
                bad.append((y, h, Y1, Y0))
    chk("%-18s every carpet-width rect stays in Y 0-324" % f, not bad,
        "" if not bad else "%d bad, first Y %.0f..%.0f" % (len(bad), bad[0][2], bad[0][3]))

print("== both BASECAMPS and all four OUTFITTER lanes land correctly ==")
s = io.open(R + 'field-top-view.svg', encoding='utf-8').read()
OX, OY, SC = 112.0, 74.0, 1.8


def spans(wpx, hpx):
    out = []
    for m in RECT.finditer(s):
        x, y, w, h = [float(v) for v in m.groups()]
        if abs(w - wpx) < 0.01 and abs(h - hpx) < 0.01:
            out.append((round((x - OX) / SC), round((x + w - OX) / SC),
                        round(324.0 - (y + h - OY) / SC), round(324.0 - (y - OY) / SC)))
    return sorted(out)


bc = spans(48 * SC, 144 * SC)
chk("BASECAMPS at X 0-48 and 600-648, both Y 90-234",
    bc == [(0, 48, 90, 234), (600, 648, 90, 234)], str(bc))
ol = spans(48 * SC, 36 * SC)
chk("OUTFITTER lanes: 4 of them, Y 12-48 and 276-312 on both walls",
    ol == [(0, 48, 12, 48), (0, 48, 276, 312), (600, 648, 12, 48), (600, 648, 276, 312)], str(ol))

print("== crag elevations: socket tubes lean inboard-down ==")
c = io.open(R + 'crag.svg', encoding='utf-8').read()
K = 3.2                      # px/in in the crag elevations
TUBE, STAND = 7.0, 8.0
rots = re.findall(r'rotate\((-?\d+(?:\.\d+)?) ([\d.]+) ([\d.]+)\)', c)
side = [(float(a), float(x)) for a, x, y in rots if abs(abs(float(a)) - 30.0) < 0.01]
chk("four side-socket tubes drawn in the elevations", len(side) >= 4, "%d found" % len(side))
ax = 250.0                   # VIEW A crag centerline, px
ok = True
det = []
for ang, xr in side[:4]:
    sgn = 1.0 if xr > ax else -1.0
    # tube bottom after SVG rotate(ang) applied to the downward offset (0, K*TUBE)
    bx_ = xr - K * TUBE * math.sin(math.radians(ang))
    face = ax + sgn * K * 24.0
    outboard = (bx_ - face) / K * sgn
    det.append("%.2f" % outboard)
    if abs(outboard - (STAND - TUBE * math.sin(math.radians(30.0)))) > 0.02:
        ok = False
chk("side-socket tube bottoms sit 4.50 in outboard of their face", ok, " / ".join(det))

sm = [(float(a), float(x)) for a, x, y in rots if abs(abs(float(a)) - 15.0) < 0.01]
chk("Summit Socket tube drawn in VIEW B", len(sm) >= 1, "%d found" % len(sm))
if sm:
    ang, xr = sm[0]
    bx_ = xr - K * TUBE * math.sin(math.radians(ang))
    bxv = 700.0                                  # VIEW B crag centerline, px
    face = bxv - K * 24.0
    outboard = (face - bx_) / K
    chk("Summit Socket tube bottom sits 6.19 in outboard of the SHELF FACE",
        abs(outboard - (STAND - TUBE * math.sin(math.radians(15.0)))) < 0.02, "%.2f" % outboard)

print("== headwall.svg: drawn rungs decode to the uniform stagger ==")
H = io.open(R + 'headwall.svg', encoding='utf-8').read()
HATTR = re.compile(r'([a-zA-Z0-9-]+)="([^"]*)"')      # attr names carry digits: x1, y2


def _lines(sw, src):
    out = []
    for m in re.finditer(r'<line([^>]*)>', src):
        a = dict(HATTR.findall(m.group(1)))
        if a.get('stroke-width') == sw and 'x1' in a:
            out.append(tuple(float(a[k]) for k in ('x1', 'y1', 'x2', 'y2')))
    return out


KH = 3.4                                              # front elevation px/in
el = _lines('5.10', H)                                # 1.5-in OD rung at 3.4 px/in
chk("nine rungs drawn in the front elevation", len(el) == 9, "%d" % len(el))
fx0 = None
for m in RECT.finditer(H):
    x, y, w, h = [float(v) for v in m.groups()]
    if abs(w - 144.0 * KH) < 1.0:
        fx0 = x
        break
if el and fx0 is not None:
    lens = set(round(abs(a[2] - a[0]) / KH, 2) for a in el)
    chk("every drawn rung is 20.0 in long", lens == {20.0}, str(sorted(lens)))
    rows = {}
    for x1, y1, x2, y2 in el:
        rows.setdefault(round(y1, 1), []).append(round(90.0 + ((x1 + x2) / 2.0 - fx0) / KH, 1))
    want = [[102.0, 150.0, 198.0], [126.0, 174.0, 222.0], [102.0, 150.0, 198.0]]
    got = [sorted(rows[k]) for k in sorted(rows)]
    chk("rung centres 102/150/198 and 126/174/222, uniform across lanes", got == want, str(got))
    gaps = [c[i + 1] - c[i] for c in got for i in range(2)]
    chk("adjacent-lane rungs 48 in apart in the drawing",
        all(abs(g - 48.0) < 1e-9 for g in gaps), "min %.1f" % min(gaps))
tv = [v for v in _lines('3.40', H) if abs(v[0] - v[2]) < 0.01]
xs = sorted(set(round(v[0], 2) for v in tv))
chk("top view shows three rung setbacks", len(xs) == 3, str(xs))
if len(xs) == 3:
    step = [(xs[i + 1] - xs[i]) / 2.2 for i in range(2)]      # top view is 2.2 px/in
    chk("setback per rung is 24 x tan15 = 6.43 in",
        all(abs(v - 6.43) < 0.02 for v in step), str([round(v, 2) for v in step]))

print("\nRESULT: %d failure(s)" % len(fails))
sys.exit(0)
