# -*- coding: utf-8 -*-
"""
Independent checks of the field TAPE (src/43_tape.fs) against the package documents.

Expected values come only from the documents:
  FIELD-CAD-PACKAGE.md  §0 (frame, 180-degree symmetry, angle rule), §1.1 (placements),
                        §1.2 (taping plan table + apron corridor check), §3 (DEPOT extents),
                        §6 (CENTER CACHE grid, staging marks, extent check), §10 row 13 / 16
  02-manual 02-arena.md §3.2 (zones and markings table; "a zone extends to the outer edge of
                        its tape"), §3.1.1 (Red = Blue rotated 180 deg about (324, 162))
  DESIGN-SPEC.md        §1.1 (APRON 36 / 20 / R20, corridor Y 128-196), §3 (placements)
  MATERIALS-AND-COLORS  §1.1 (alliance-blue #1D63C8, alliance-red #CC3333, neutral-white
                        #F5F5F5), §2 ("Zone tape | Gaffer tape | alliance color | 2 in wide,
                        0.01 in"; "Neutral marks | Gaffer tape | neutral-white | 2 in wide")
Nothing is imported from src/ and no number is taken from src/20_ledger.fs.

Frames are built here from the documents: the Blue CRAG frame has its origin at (324, 240)
and +x along the Blue SHELF FACE normal (-X world); Red at (324, 84), +x = +X world.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import kernel_occ as K  # noqa: E402  (OpenCascade helpers only — not part code)

# ------------------------------------------------------------------------------------------
# Document values
# ------------------------------------------------------------------------------------------
FIELD_L, FIELD_W = 648.0, 324.0            # §0 carpet 648 x 324
CX, CY = 324.0, 162.0                       # §0 field centre / centerline X = 324
TW = 2.0                                    # §1.2 "All lines are 2-in tape geometry"
TT = 0.01                                   # MATERIALS §2 zone tape "2 in wide, 0.01 in"
TAPE_MAT = "Gaffer tape"                    # MATERIALS §2 zone tape and neutral marks
RGB = {"BLUE": (0x1D, 0x63, 0xC8),          # MATERIALS §1.1 alliance-blue #1D63C8
       "RED": (0xCC, 0x33, 0x33),           # alliance-red #CC3333
       "WHITE": (0xF5, 0xF5, 0xF5)}         # neutral-white #F5F5F5
SIDES = ("BLUE", "RED")

BASECAMP_B = (0.0, 90.0, 48.0, 234.0)       # §1.1 / §1.2 / manual §3.2: Blue X 0-48, Y 90-234
CLIMB_X_B = 48.0                            # §1.2 CLIMB LINE: X = 48 (Blue), Y 0-324
CHUTE_Y_B = (30.0, 294.0)                   # §1.1 chutes centred (0, 30) and (0, 294)
LANE_W, LANE_D = 36.0, 48.0                 # §1.2 / §5 OUTFITTER LANE 36 wide x 48 deep

CRAG_C = {"BLUE": (324.0, 240.0), "RED": (324.0, 84.0)}   # §1.1
CRAG_S = 48.0                               # §1.1 48 x 48 footprint
AP_SHELF = AP_PEG = 36.0                    # §1.2 / DESIGN-SPEC §1.1 / §10 row 13
AP_SOCK = 20.0
AP_R = 20.0                                 # R20 corner arcs, tangent to both offset lines
CORRIDOR = (128.0, 196.0)                   # §1.2 apron corridor check: open corridor Y 128-196
CACHE_CLEAR = 3.5                           # §1.2 / §6: 3.5 in clearance at each end

BAND = (300.0, 108.0, 348.0, 216.0)         # §1.2 CENTER CACHE band X 300-348, Y 108-216
CACHE_X = (300.0, 324.0, 348.0)             # §6 grid X = 300/324/348
CACHE_Y = (138.0, 162.0, 186.0)             # §6 grid Y = 138/162/186
MARK = 12.0                                 # §1.2 12-in "X" marks
STAGE_X = {"BLUE": 144.0, "RED": 504.0}     # §1.1 / §1.2 / §6
STAGE_Y = (108.0, 162.0, 216.0)
DEPOT_STOP = 8.0                            # §1.2 "the BASE DEPOT trays stop 8 in short of the line"

ZMID = TT / 2.0
EPS = 0.05                                  # probe offset from a stated edge (in)
VOL_TOL = 1e-7                              # in^3 — 1e-5 in^2 of overlapping tape area


# ------------------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------------------
def rot(p):
    """Blue -> Red: 180 degrees about (324, 162)."""
    return (2 * CX - p[0], 2 * CY - p[1])


def side_pt(side, x, y):
    return (x, y) if side == "BLUE" else rot((x, y))


def box6(shape):
    b = K.Bnd_Box()
    K.BRepBndLib.AddOptimal_s(shape, b, False, False)
    return K._box6(b)


class Plan:
    """Fast point membership against a set of records (bbox prefilter + solid classifier)."""

    def __init__(self, recs):
        self.items = []
        for r in recs:
            for s in r["solids"]:
                self.items.append((box6(s), s, r))

    def hit(self, x, y, z=ZMID):
        for b, s, r in self.items:
            if b[0] - 1e-7 <= x <= b[3] + 1e-7 and b[1] - 1e-7 <= y <= b[4] + 1e-7 and b[2] - 1e-7 <= z <= b[5] + 1e-7:
                cl = K.BRepClass3d_SolidClassifier(s, K._gp((x, y, z)), 1e-7)
                if cl.State() in (K.TopAbs_IN, K.TopAbs_ON):
                    return r
        return None

    def has(self, x, y, z=ZMID):
        return self.hit(x, y, z) is not None


def frange(a, b, step):
    n = max(1, int(round((b - a) / step)))
    return [a + (b - a) * i / n for i in range(n + 1)]


def approx(a, b, tol):
    return abs(a - b) <= tol


def fmt_box(b):
    return "[" + ", ".join("%.3f" % v for v in b) + "]"


def crag_frame(f, side):
    cx, cy = CRAG_C[side]
    xd = (-1.0, 0.0, 0.0) if side == "BLUE" else (1.0, 0.0, 0.0)   # SHELF FACE normal
    return f.frame((cx, cy, 0.0), xd, (0.0, 0.0, 1.0))


def rot_solids(solids):
    t = K.gp_Trsf()
    t.SetRotation(K.gp_Ax1(K.gp_Pnt(CX, CY, 0.0), K.gp_Dir(0.0, 0.0, 1.0)), math.pi)
    return [K.TopoDS.Solid(K.BRepBuilderAPI_Transform(s, t, True).Shape()) for s in solids]


def common_solids(a, b):
    tot = 0.0
    for x in a:
        bx = box6(x)
        for y in b:
            by = box6(y)
            if all(bx[i] <= by[i + 3] + 1e-6 and by[i] <= bx[i + 3] + 1e-6 for i in range(3)):
                tot += K._volume(K._solids(K.BRepAlgoAPI_Common(x, y).Shape()))
    return tot


def safe_find(f, name):
    try:
        return f.find(name)
    except KeyError:
        return []


# ------------------------------------------------------------------------------------------
def run(f):
    out = []

    def add(label, ok, detail):
        out.append((label, bool(ok), detail))

    # ---------------- inventory ---------------------------------------------------------
    groups = {}
    for s in SIDES:
        groups[s + " BASECAMP"] = safe_find(f, s + " BASECAMP tape")
        groups[s + " CLIMB"] = safe_find(f, "re:^%s CLIMB LINE" % s)
        groups[s + " LANE"] = safe_find(f, "re:^%s OUTFITTER LANE tape" % s)
        groups[s + " APRON"] = safe_find(f, s + " CRAG APRON tape")
        groups[s + " STAGE"] = safe_find(f, s + " staging mark")
        groups[s + " STAGE BORDER"] = safe_find(f, s + " staging mark border")
    groups["CENTERLINE"] = safe_find(f, "FIELD centerline tape")
    groups["BAND"] = safe_find(f, "CENTER CACHE band tape")
    groups["CACHE MARK"] = safe_find(f, "CENTER CACHE mark")
    for g, rs in groups.items():
        add("inventory: %s tape present" % g, len(rs) > 0, "%d bodies" % len(rs))

    all_tape = [r for r in f.records() if r["mat"] and r["mat"].get("name") == TAPE_MAT]
    grouped_ids = {id(r) for rs in groups.values() for r in rs}
    stray = [r["name"] for r in all_tape if id(r) not in grouped_ids]
    add("inventory: every Gaffer-tape body belongs to a named §1.2 marking", not stray,
        "unaccounted tape bodies: %s" % sorted(set(stray)) if stray else "%d tape bodies, all accounted for" % len(all_tape))
    named_tape = [r for rs in groups.values() for r in rs]
    not_tape = [r["name"] for r in named_tape if not (r["mat"] and r["mat"].get("name") == TAPE_MAT)]
    add("material: every marking is Gaffer tape (MATERIALS §2)", not not_tape,
        "wrong material on %s" % sorted(set(not_tape)) if not_tape else "all %d marking bodies 'Gaffer tape'" % len(named_tape))
    dens = sorted({r["mat"]["density"] for r in named_tape if r["mat"]})
    add("material: tape density is a positive physical value (no document value; info)",
        all(d > 0 for d in dens), "densities in use: %s kg/m^3" % dens)

    # ---------------- colour ------------------------------------------------------------
    for s in SIDES:
        for g in ("BASECAMP", "CLIMB", "LANE", "APRON", "STAGE BORDER"):
            rs = groups[s + " " + g]
            bad = [r["name"] for r in rs if tuple(r["rgb"]) != RGB[s] or r["alpha"] != 1]
            add("colour: %s %s is alliance colour %s, opaque" % (s, g, RGB[s]), rs and not bad,
                "wrong: %s" % bad if bad else "ok (%d bodies)" % len(rs))
        rs = groups[s + " STAGE"]
        bad = [r["name"] for r in rs if tuple(r["rgb"]) != RGB["WHITE"] or r["alpha"] != 1]
        add("colour: %s staging mark body is neutral-white" % s, rs and not bad, "wrong: %s" % bad if bad else "ok")
    for g in ("CENTERLINE", "BAND", "CACHE MARK"):
        rs = groups[g]
        bad = [(r["name"], r["rgb"]) for r in rs if tuple(r["rgb"]) != RGB["WHITE"] or r["alpha"] != 1]
        add("colour: %s is neutral-white #F5F5F5" % g, rs and not bad, "wrong: %s" % bad if bad else "ok")

    # ---------------- thickness / on the carpet -----------------------------------------
    bad_t, bad_xy = [], []
    for r in named_tape:
        b = f.bbox([r])
        if not (approx(b[2], 0.0, 1e-6) and approx(b[5], TT, 1e-6)):
            bad_t.append((r["name"], round(b[2], 4), round(b[5], 4)))
        if b[0] < -1e-6 or b[1] < -1e-6 or b[3] > FIELD_L + 1e-6 or b[4] > FIELD_W + 1e-6:
            bad_xy.append((r["name"], fmt_box(b)))
    add("thickness: every tape body spans Z 0 .. 0.01 on the carpet (MATERIALS §2)", not bad_t,
        "bad: %s" % bad_t[:6] if bad_t else "all %d bodies Z 0-0.01" % len(named_tape))
    add("extent: every tape body lies on the 648 x 324 carpet", not bad_xy, "outside: %s" % bad_xy[:6] if bad_xy else "ok")

    all_plan = Plan(named_tape)

    # ---------------- BASECAMP / HEADWALL ZONE ------------------------------------------
    for s in SIDES:
        rs = groups[s + " BASECAMP"]
        if not rs:
            continue
        P = Plan(rs)
        x0, y0, x1, y1 = BASECAMP_B
        c0, c1 = side_pt(s, x0, y0), side_pt(s, x1, y1)
        want = [min(c0[0], c1[0]), min(c0[1], c1[1]), 0.0, max(c0[0], c1[0]), max(c0[1], c1[1]), TT]
        got = f.bbox(rs)
        add("%s BASECAMP: tape bbox = zone X %g-%g, Y %g-%g (outer tape edges on the zone boundary)" % (s, want[0], want[3], want[1], want[4]),
            all(approx(a, b, 1e-6) for a, b in zip(got, want)), "got %s want %s" % (fmt_box(got), fmt_box(want)))
        # X = 48 line: 2 in wide, inside the zone (X 46-48), edge on X = 48
        miss_in, hit_out, hit_in2 = [], [], []
        for y in frange(y0 + 0.1, y1 - 0.1, 0.5):
            for d in (EPS, TW / 2, TW - EPS):
                p = side_pt(s, x1 - d, y)
                if not P.has(*p):
                    miss_in.append((round(x1 - d, 2), round(y, 2)))
            p = side_pt(s, x1 + EPS, y)
            if all_plan.has(*p):
                hit_out.append(round(y, 2))
            if y0 + TW + EPS < y < y1 - TW - EPS:
                p = side_pt(s, x1 - TW - EPS, y)
                if all_plan.has(*p):
                    hit_in2.append(round(y, 2))
        add("%s BASECAMP: X = 48 line present over Y 90-234, 2 in wide inside the zone" % s, not miss_in,
            "missing at (Blue coords) %s" % miss_in[:5] if miss_in else "X 46-48 covered at every probe")
        add("%s BASECAMP: nothing taped just field-side of X = 48 over Y 90-234 (CLIMB LINE needs no second line)" % s,
            not hit_out, "tape at Y %s" % hit_out[:5] if hit_out else "clear")
        add("%s BASECAMP: X = 48 line is exactly 2 in wide (nothing at X 45.95 inside the zone)" % s,
            not hit_in2, "tape at Y %s" % hit_in2[:5] if hit_in2 else "clear")
        # Y = 90 and Y = 234 lines, X 0-48, inside the zone
        for yl, sgn in ((y0, +1), (y1, -1)):
            miss_in, hit_out, hit_in2 = [], [], []
            for x in frange(x0 + 0.1, x1 - 0.1, 0.5):
                for d in (EPS, TW / 2, TW - EPS):
                    if not P.has(*side_pt(s, x, yl + sgn * d)):
                        miss_in.append((round(x, 2), round(yl + sgn * d, 2)))
                if all_plan.has(*side_pt(s, x, yl - sgn * EPS)):
                    hit_out.append(round(x, 2))
                if x < x1 - TW - EPS and all_plan.has(*side_pt(s, x, yl + sgn * (TW + EPS))):
                    hit_in2.append(round(x, 2))
            add("%s BASECAMP: Y = %g line present over X 0-48, 2 in wide inside the zone" % (s, yl), not miss_in,
                "missing at %s" % miss_in[:5] if miss_in else "ok")
            add("%s BASECAMP: Y = %g line edge on the stated coordinate (clear outside)" % (s, yl), not hit_out,
                "tape outside at X %s" % hit_out[:5] if hit_out else "ok")
            add("%s BASECAMP: Y = %g line exactly 2 in wide" % (s, yl), not hit_in2,
                "tape at X %s" % hit_in2[:5] if hit_in2 else "ok")
        # the wall closes the fourth side: no tape along the wall
        wall_hits = [round(y, 1) for y in frange(y0 + TW + EPS, y1 - TW - EPS, 1.0) if all_plan.has(*side_pt(s, 0.5, y))]
        add("%s BASECAMP: open on the wall side (the wall closes the fourth side)" % s, not wall_hits,
            "tape at X 0.5, Y %s" % wall_hits[:5] if wall_hits else "ok")

    # ---------------- CLIMB LINE ----------------------------------------------------------
    for s in SIDES:
        rs = groups[s + " CLIMB"]
        if not rs:
            continue
        Pc, Pb, Pl = Plan(rs), Plan(groups[s + " BASECAMP"]), Plan(groups[s + " LANE"])
        got = f.bbox(rs)
        xa, xb = sorted([side_pt(s, CLIMB_X_B - TW, 0)[0], side_pt(s, CLIMB_X_B, 0)[0]])
        add("%s CLIMB LINE: dashes are 2-in tape inside BASECAMP side of X = %g (X %g-%g)" % (s, side_pt(s, CLIMB_X_B, 0)[0], xa, xb),
            approx(got[0], xa, 1e-6) and approx(got[3], xb, 1e-6), "got X %.3f-%.3f" % (got[0], got[3]))
        cats = []
        for y in frange(0.05, FIELD_W - 0.05, 0.25):
            p = side_pt(s, CLIMB_X_B - TW / 2, y)
            c = "climb" if Pc.has(*p) else "basecamp" if Pb.has(*p) else "lane" if Pl.has(*p) else None
            cats.append((y, c))
        in_bc = [(y, c) for y, c in cats if BASECAMP_B[1] < y < BASECAMP_B[3]]
        out_bc = [(y, c) for y, c in cats if not (BASECAMP_B[1] < y < BASECAMP_B[3])]
        add("%s CLIMB LINE: over Y 90-234 it is the BASECAMP line (no second line)" % s,
            all(c == "basecamp" for _, c in in_bc), "categories there: %s" % sorted({str(c) for _, c in in_bc}))
        n_cl = sum(1 for _, c in out_bc if c == "climb")
        n_gap = sum(1 for _, c in out_bc if c is None)
        add("%s CLIMB LINE: dashed outside BASECAMP (both tape and gaps present in Y 0-90 and 234-324)" % s,
            n_cl > 0 and n_gap > 0 and any(c == "climb" for y, c in out_bc if y < 90) and any(c == "climb" for y, c in out_bc if y > 234),
            "%d dash probes, %d gap probes" % (n_cl, n_gap))
        add("%s CLIMB LINE: carried to the full field width (tape at Y = 0 and Y = 324)" % s,
            cats[0][1] is not None and cats[-1][1] is not None, "Y 0.05: %s, Y 323.95: %s" % (cats[0][1], cats[-1][1]))
        gaps, run0 = [], None
        for y, c in cats:
            if c is None and run0 is None:
                run0 = y
            elif c is not None and run0 is not None:
                gaps.append(y - run0)
                run0 = None
        mg = max(gaps) if gaps else 0.0
        add("%s CLIMB LINE: the dashed line reads as one line (longest gap <= 12 in; ref)" % s, mg <= 12.0 + 0.3,
            "longest untaped run along the line %.2f in; %d gaps" % (mg, len(gaps)))
        # the dashes: edge on X = 48 (field-side edge), nothing field-side of it
        bad = []
        for y, c in cats:
            if c == "climb":
                if all_plan.has(*side_pt(s, CLIMB_X_B + EPS, y)) or not Pc.has(*side_pt(s, CLIMB_X_B - EPS, y)) \
                        or not Pc.has(*side_pt(s, CLIMB_X_B - TW + EPS, y)) or Pc.has(*side_pt(s, CLIMB_X_B - TW - EPS, y)):
                    bad.append(round(y, 2))
        add("%s CLIMB LINE: every dash is 2 in wide with its field-side edge on the G416 plane" % s, not bad,
            "bad at Y %s" % bad[:5] if bad else "ok")

    # ---------------- OUTFITTER LANES ---------------------------------------------------
    for s in SIDES:
        rs = groups[s + " LANE"]
        add("%s OUTFITTER LANE: 2 lanes" % s, len({r["name"] for r in rs}) == 2, "names %s" % sorted({r["name"] for r in rs}))
        tags = safe_find(f, "re:^AprilTag \\d+ - %s OUTFITTER chute" % s)
        ramps = safe_find(f, "re:^%s OUTFITTER \\d chute ramp" % s)
        for cyb in CHUTE_Y_B:
            cy = side_pt(s, 0, cyb)[1]
            lane = [r for r in rs if f.bbox([r])[1] - 1 <= cy <= f.bbox([r])[4] + 1]
            lane_names = sorted({r["name"] for r in lane})
            lane = [r for r in rs if r["name"] in lane_names]
            if not lane:
                add("%s OUTFITTER LANE at chute Y %g present" % (s, cy), False, "no lane tape there")
                continue
            P = Plan(lane)
            got = f.bbox(lane)
            a, b = side_pt(s, 0, cyb - LANE_W / 2), side_pt(s, LANE_D, cyb + LANE_W / 2)
            want = [min(a[0], b[0]), min(a[1], b[1]), 0, max(a[0], b[0]), max(a[1], b[1]), TT]
            add("%s OUTFITTER LANE at chute Y %g: 36 wide x 48 deep, centred on the chute (bbox)" % (s, cy),
                all(approx(u, v, 1e-6) for u, v in zip(got, want)), "got %s want %s" % (fmt_box(got), fmt_box(want)))
            # centred on the as-built chute: tag panel centred above the chute, and the ramp
            refs = []
            for grp in (tags, ramps):
                for r in grp:
                    bb = f.bbox([r])
                    if abs((bb[1] + bb[4]) / 2 - cy) < 10:
                        refs.append((r["name"], (bb[1] + bb[4]) / 2))
            lc = (got[1] + got[4]) / 2
            add("%s OUTFITTER LANE at chute Y %g: centred on the as-built chute (tag panel / ramp)" % (s, cy),
                refs and all(approx(lc, v, 0.01) for _, v in refs), "lane centre %.3f; refs %s" % (lc, [(n, round(v, 3)) for n, v in refs]))
            miss, outside, inner = [], [], []
            yl, yh = cyb - LANE_W / 2, cyb + LANE_W / 2
            for y in frange(yl + 0.1, yh - 0.1, 0.5):          # end line X 46-48
                for d in (EPS, TW - EPS):
                    if not P.has(*side_pt(s, LANE_D - d, y)):
                        miss.append(("end", round(y, 1)))
                if all_plan.has(*side_pt(s, LANE_D + EPS, y)):
                    outside.append(("end", round(y, 1)))
                if yl + TW + EPS < y < yh - TW - EPS and all_plan.has(*side_pt(s, LANE_D - TW - EPS, y)):
                    inner.append(("end", round(y, 1)))
            for x in frange(0.1, LANE_D - 0.1, 0.5):            # side lines
                for yy, sg in ((yl, 1), (yh, -1)):
                    for d in (EPS, TW - EPS):
                        if not P.has(*side_pt(s, x, yy + sg * d)):
                            miss.append(("side", round(x, 1)))
                    if all_plan.has(*side_pt(s, x, yy - sg * EPS)):
                        outside.append(("side", round(x, 1)))
                    if x < LANE_D - TW - EPS and all_plan.has(*side_pt(s, x, yy + sg * (TW + EPS))):
                        inner.append(("side", round(x, 1)))
            add("%s OUTFITTER LANE at chute Y %g: 3 lines, 2 in wide, inside the lane" % (s, cy), not miss,
                "missing %s" % miss[:5] if miss else "ok")
            add("%s OUTFITTER LANE at chute Y %g: line edges on the stated boundary (clear outside)" % (s, cy), not outside,
                "tape outside %s" % outside[:5] if outside else "ok")
            add("%s OUTFITTER LANE at chute Y %g: lines exactly 2 in (lane interior clear)" % (s, cy), not inner,
                "tape inside %s" % inner[:5] if inner else "ok")
            wall = [round(y, 1) for y in frange(yl + TW + EPS, yh - TW - EPS, 1.0) if all_plan.has(*side_pt(s, 0.5, y))]
            add("%s OUTFITTER LANE at chute Y %g: open at the wall" % (s, cy), not wall, "tape at wall %s" % wall[:5] if wall else "ok")

    # ---------------- CRAG APRON --------------------------------------------------------
    hx = CRAG_S / 2 + AP_SHELF      # 60 (SHELF / PEG faces are symmetric about the crag)
    hy = CRAG_S / 2 + AP_SOCK       # 44
    ring_area = (4 * hx * hy - (4 - math.pi) * AP_R ** 2) - (4 * (hx - TW) * (hy - TW) - (4 - math.pi) * (AP_R - TW) ** 2)
    staged = safe_find(f, "re:- CENTER CACHE \\(")
    for s in SIDES:
        rs = groups[s + " APRON"]
        if not rs:
            continue
        F = crag_frame(f, s)
        P = Plan(rs)
        got = f.bbox(rs, F)
        want = [-hx, -hy, 0, hx, hy, TT]
        add("%s CRAG APRON: local bbox = +/-(24+36) along the face normal, +/-(24+20) along the SOCKET FACES" % s,
            all(approx(a, b, 1e-4) for a, b in zip(got, want)), "got %s want %s" % (fmt_box(got), fmt_box(want)))
        # offsets measured against the as-built tower faces
        tower = safe_find(f, s + " CRAG tower")
        if tower:
            tb, ab = f.bbox(tower), f.bbox(rs)
            if s == "BLUE":
                shelf, peg = tb[0] - ab[0], ab[3] - tb[3]
            else:
                shelf, peg = ab[3] - tb[3], tb[0] - ab[0]
            sockA, sockB = tb[1] - ab[1], ab[4] - tb[4]
            add("%s CRAG APRON: offset from the built SHELF FACE = 36 (CRITICAL)" % s, approx(shelf, AP_SHELF, 1e-4), "%.4f" % shelf)
            add("%s CRAG APRON: offset from the built PEG FACE = 36 (CRITICAL)" % s, approx(peg, AP_PEG, 1e-4), "%.4f" % peg)
            add("%s CRAG APRON: offsets from both built SOCKET FACES = 20 (CRITICAL)" % s,
                approx(sockA, AP_SOCK, 1e-4) and approx(sockB, AP_SOCK, 1e-4), "-Y %.4f, +Y %.4f" % (sockA, sockB))
        n_sol = len(f.solids(rs))
        vol = f.volume(rs)
        add("%s CRAG APRON: one closed, untrimmed 2-in ring (1 solid, area = rounded-rect annulus)" % s,
            n_sol == 1 and approx(vol, ring_area * TT, ring_area * TT * 1e-3),
            "%d solid(s); area %.3f in^2, expected %.3f" % (n_sol, vol / TT, ring_area))
        # profile sampling: outer edge on the offset line, inner edge 2 in inside, R20 tangent arcs
        samples = []
        for t in frange(-(hy - AP_R), hy - AP_R, 1.0):                   # x = +/-60 straights
            samples += [((hx, t), (1, 0)), ((-hx, t), (-1, 0))]
        for t in frange(-(hx - AP_R), hx - AP_R, 1.0):                   # y = +/-44 straights
            samples += [((t, hy), (0, 1)), ((t, -hy), (0, -1))]
        for sx in (1, -1):
            for sy in (1, -1):
                ccx, ccy = sx * (hx - AP_R), sy * (hy - AP_R)
                for a in frange(0, 90, 5):
                    n = (sx * math.cos(math.radians(a)), sy * math.sin(math.radians(a)))
                    samples.append(((ccx + AP_R * n[0], ccy + AP_R * n[1]), n))
        bad = []
        for (px, py), (nx, ny) in samples:
            def w(d):
                return tuple(F.pt((px - nx * d, py - ny * d, ZMID))[:2])
            exp = {-EPS: False, EPS: True, TW - EPS: True, TW + EPS: False}
            for d, e in exp.items():
                if P.has(*w(d)) != e:
                    bad.append(((round(px, 2), round(py, 2)), d))
        add("%s CRAG APRON: outer edge on the 36/20 offset line, 2 in inside, R20 tangent corners (%d profile probes)" % (s, 4 * len(samples)),
            not bad, "mismatch at local %s" % bad[:6] if bad else "all probes match")
        # corridor
        wb = f.bbox(rs)
        if s == "BLUE":
            add("BLUE CRAG APRON: -Y socket-face apron starts at Y 196 (corridor upper bound)", approx(wb[1], CORRIDOR[1], 1e-4), "Y min %.4f" % wb[1])
        else:
            add("RED CRAG APRON: +Y socket-face apron ends at Y 128 (corridor lower bound)", approx(wb[4], CORRIDOR[0], 1e-4), "Y max %.4f" % wb[4])
        if staged:
            dmin = min(f.dist(rs, [r]) for r in staged)
            add("%s CRAG APRON: no staged CENTER CACHE SUPPLY touches it" % s, dmin > 0.0, "closest staged SUPPLY %.3f in (3D)" % dmin)
            sb = f.bbox(staged)
            clear = wb[1] - sb[4] if s == "BLUE" else sb[1] - wb[4]
            add("%s CRAG APRON: staged CENTER CACHE plan extent (Y %.2f-%.2f) clears it by >= 3.5 in (§1.2 corridor check)" % (s, sb[1], sb[4]),
                clear >= CACHE_CLEAR - 0.01, "plan clearance %.3f in (document: 3.5)" % clear)
    # corridor open and continuous: no tape of either apron anywhere in Y 128-196
    aps = groups["BLUE APRON"] + groups["RED APRON"]
    if aps:
        Pa = Plan(aps)
        hits = [(x, y) for x in frange(0.5, FIELD_L - 0.5, 4.0) for y in frange(CORRIDOR[0] + EPS, CORRIDOR[1] - EPS, 4.0) if Pa.has(x, y)]
        add("APRON corridor: Y 128-196 (68 in) free of APRON tape along the whole field", not hits,
            "apron tape at %s" % hits[:5] if hits else "open, width %.1f" % (CORRIDOR[1] - CORRIDOR[0]))

    # band end regions lie inside the aprons (enclosure by the built ring, cast 4 rays)
    def enclosed(Pring, x, y):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if not any(Pring.has(x + dx * d, y + dy * d) for d in frange(0.0, 130.0, 0.25)):
                return False
        return True
    if groups["BLUE APRON"] and groups["RED APRON"]:
        PB, PR = Plan(groups["BLUE APRON"]), Plan(groups["RED APRON"])
        bx0, by0, bx1, by1 = BAND
        pts_b = [(x, y) for x in (bx0 + 0.1, (bx0 + bx1) / 2, bx1 - 0.1) for y in (by1 - 20 + 0.1, by1 - 0.1)]
        pts_r = [(x, y) for x in (bx0 + 0.1, (bx0 + bx1) / 2, bx1 - 0.1) for y in (by0 + 0.1, by0 + 20 - 0.1)]
        nb = [p for p in pts_b if not enclosed(PB, *p)]
        nr = [p for p in pts_r if not enclosed(PR, *p)]
        add("APRON: the outer 20 in at each end of the CENTER CACHE band lies inside a CRAG APRON (DESIGN-SPEC §1.1)",
            not nb and not nr, "not enclosed: Blue %s Red %s" % (nb, nr) if (nb or nr) else "ok")

    # ---------------- FIELD centerline --------------------------------------------------
    cl = groups["CENTERLINE"]
    if cl:
        Pcl = Plan(cl)
        cross = Plan(aps + groups["CACHE MARK"])
        got = f.bbox(cl)
        add("centerline: 2-in line centred on X = 324 (X 323-325), running Y 0-324",
            approx(got[0], CX - TW / 2, 1e-6) and approx(got[3], CX + TW / 2, 1e-6) and approx(got[1], 0, 1e-6) and approx(got[4], FIELD_W, 1e-6),
            "bbox %s" % fmt_box(got))
        foot = [(CRAG_C[s][1] - CRAG_S / 2, CRAG_C[s][1] + CRAG_S / 2) for s in SIDES]
        in_foot = [round(y, 2) for (a, b) in foot for y in frange(a + EPS, b - EPS, 0.5) if all_plan.has(CX, y)]
        add("centerline: broken where the two CRAG footprints cross it (Y 60-108, 216-264 untaped)", not in_foot,
            "tape at Y %s" % in_foot[:5] if in_foot else "ok")
        bare, own, tot = [], 0, 0
        for y in frange(0.05, FIELD_W - 0.05, 0.25):
            if any(a - 1e-9 <= y <= b + 1e-9 for a, b in foot):
                continue
            for x in (CX - TW / 2 + EPS, CX, CX + TW / 2 - EPS):
                tot += 1
                if Pcl.has(x, y):
                    own += 1
                elif not cross.has(x, y):
                    bare.append((round(x, 2), round(y, 2)))
        add("centerline: continuous from Y 0 to 324 outside the footprints (only APRON / cache marks cross it)", not bare,
            "untaped at %s" % bare[:6] if bare else "%.1f%% own tape, rest APRON/mark crossings" % (100.0 * own / max(tot, 1)))
        add("centerline: the white line itself carries >= 85% of its length (crossings are short)", own >= 0.85 * tot,
            "%.1f%%" % (100.0 * own / max(tot, 1)))
        ends = [(y, Pcl.has(CX, y)) for y in (foot[1][0] - EPS, foot[1][1] + EPS, foot[0][0] - EPS, foot[0][1] + EPS, 0.05, FIELD_W - 0.05)]
        add("centerline: segments run right up to both CRAG footprints and both guardrails", all(v for _, v in ends),
            "%s" % [(round(y, 2), v) for y, v in ends])
        for s in SIDES:
            fl = safe_find(f, s + " CRAG BASE DEPOT floor")
            dep = safe_find(f, "re:^%s CRAG BASE DEPOT" % s)
            if fl:
                b = f.bbox(fl)
                gap = CX - b[3] if s == "BLUE" else b[0] - CX
                add("centerline: %s BASE DEPOT tray stops 8 in short of X = 324" % s, approx(gap, DEPOT_STOP, 1e-4), "%.4f in" % gap)
            if dep:
                d = f.dist(dep, cl)
                add("centerline: %s BASE DEPOT (lip, chamfer) does not reach the centerline tape" % s, d > 1e-6, "gap %.3f in" % d)

    # ---------------- CENTER CACHE band -------------------------------------------------
    band = groups["BAND"]
    if band:
        Pband = Plan(band)
        depots = safe_find(f, "re:CRAG BASE DEPOT")
        Pdep = Plan(depots)
        crossers = Plan(groups["CENTERLINE"] + groups["CACHE MARK"] + aps)
        got = f.bbox(band)
        bx0, by0, bx1, by1 = BAND
        add("band: outline bbox X 300-348, Y 108-216 (48 x 108)",
            all(approx(a, b, 1e-6) for a, b in zip(got, [bx0, by0, 0, bx1, by1, TT])), "bbox %s" % fmt_box(got))
        tb = safe_find(f, "BLUE CRAG tower")
        tr = safe_find(f, "RED CRAG tower")
        if tb and tr:
            add("band: end edges coincide with the two built CRAG SOCKET FACE planes",
                approx(got[4], f.bbox(tb)[1], 1e-6) and approx(got[1], f.bbox(tr)[4], 1e-6),
                "band Y %.3f-%.3f; Blue -Y face %.3f, Red +Y face %.3f" % (got[1], got[4], f.bbox(tb)[1], f.bbox(tr)[4]))
        edges = [("X=300", lambda t, d: (bx0 + d, t), (by0, by1)), ("X=348", lambda t, d: (bx1 - d, t), (by0, by1)),
                 ("Y=108", lambda t, d: (t, by0 + d), (bx0, bx1)), ("Y=216", lambda t, d: (t, by1 - d), (bx0, bx1))]
        bare, outside, inner, under = [], [], [], []
        for nm_, fn, (a, b) in edges:
            for t in frange(a + 0.1, b - 0.1, 0.25):
                for d in (EPS, TW / 2, TW - EPS):
                    x, y = fn(t, d)
                    if Pband.has(x, y) or crossers.has(x, y):
                        continue
                    if Pdep.has(x, y, 0.1):
                        under.append((nm_, round(t, 2)))
                        continue
                    q = K.BRepBuilderAPI_MakeVertex(K._gp((x, y, ZMID))).Vertex()
                    dd = min(K.BRepExtrema_DistShapeShape(q, s).Value() for _, s, _ in Pdep.items) if Pdep.items else 1e9
                    if dd <= 0.3:
                        under.append((nm_, round(t, 2)))
                    else:
                        bare.append((nm_, round(x, 2), round(y, 2)))
                x, y = fn(t, -EPS)
                if Pband.has(x, y):
                    outside.append((nm_, round(t, 2)))
                x, y = fn(t, TW + EPS)
                if a + TW + EPS < t < b - TW - EPS and Pband.has(x, y):
                    inner.append((nm_, round(t, 2)))
        add("band: 2-in outline present everywhere except under crossing tape and the BASE DEPOT trays", not bare,
            "untaped outline at %s" % bare[:6] if bare else "ok (%d probes interrupted at the trays)" % len(under))
        add("band: interrupted where the BASE DEPOT trays cross it", len(under) > 0 and f.common_volume(band, depots) <= VOL_TOL,
            "%d outline probes at the trays; band/tray overlap %.2e in^3" % (len(under), f.common_volume(band, depots)))
        if depots:
            dd = f.dist(band, depots)
            add("band: stops right at the trays (touches the tray footprint)", dd <= 0.01, "gap %.4f in" % dd)
        add("band: tape edges on the stated coordinates (nothing outside the band)", not outside, "%s" % outside[:5] if outside else "ok")
        add("band: lines exactly 2 in wide (an outline, not a filled area)", not inner and not Pband.has(312, 150) and not Pband.has(336, 174),
            "%s" % inner[:5] if inner else "ok")

    # ---------------- X marks -----------------------------------------------------------
    def arm_len(P, cx, cy, ux, uy):
        """Centre-to-tip length of the arm along (ux, uy), by bisection on the axis."""
        if not P.has(cx, cy):
            return 0.0
        lo, hi = 0.0, 20.0
        for d in frange(0.0, 20.0, 0.25):
            if not P.has(cx + ux * d, cy + uy * d):
                lo, hi = d - 0.25, d
                break
        for _ in range(30):
            m = (lo + hi) / 2
            if P.has(cx + ux * m, cy + uy * m):
                lo = m
            else:
                hi = m
        return lo

    def xmark_probe(P, cx, cy):
        """(ok, detail) for a 12-in X of 2-in bars along the 45-degree diagonals.

        §1.2 says only '12-in "X"'.  Both readings are accepted: 12-in strokes (arm 6.0 from
        the centre) or a 12-in overall span (arm 6*sqrt(2) = 8.49); the measured arm is reported."""
        errs = []
        c = math.sqrt(0.5)
        axes = [(c, c), (-c, c), (-c, -c), (c, -c)]
        arms = [arm_len(P, cx, cy, ux, uy) for ux, uy in axes]
        half = arms[0]
        if not (approx(half, MARK / 2, 0.02) or approx(half, MARK / 2 * math.sqrt(2), 0.02)):
            errs.append("arm %.3f is neither 6.0 (12-in strokes) nor 8.49 (12-in span)" % half)
        if max(arms) - min(arms) > 0.01:
            errs.append("unequal arms %s" % [round(a, 3) for a in arms])
        for ux, uy in axes:
            vx, vy = -uy, ux
            for dist in (2.5, 4.0, half - 0.5):
                if not P.has(cx + ux * dist + vx * (TW / 2 - EPS), cy + uy * dist + vy * (TW / 2 - EPS)):
                    errs.append("arm narrower than 2 in")
                if P.has(cx + ux * dist + vx * (TW / 2 + EPS), cy + uy * dist + vy * (TW / 2 + EPS)):
                    errs.append("arm wider than 2 in")
        for ax_, ay_ in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if P.has(cx + ax_ * 3.0, cy + ay_ * 3.0):
                errs.append("tape on the field axes at 3 in (a '+', not an 'X')")
        return not errs, errs, half

    cm = groups["CACHE MARK"]
    if cm:
        centres = []
        for r in cm:
            for sld in r["solids"]:
                b = box6(sld)
                centres.append(((b[0] + b[3]) / 2, (b[1] + b[4]) / 2))
        grid = [(x, y) for x in CACHE_X for y in CACHE_Y]
        matched = {g: [c for c in centres if abs(c[0] - g[0]) < 0.01 and abs(c[1] - g[1]) < 0.01] for g in grid}
        add("CENTER CACHE marks: exactly 9, one on each 3x3 grid point (X 300/324/348 x Y 138/162/186)",
            len(centres) == 9 and all(len(v) == 1 for v in matched.values()),
            "%d mark solids; unmatched grid points %s" % (len(centres), [g for g, v in matched.items() if len(v) != 1]))
        pitch_ok = all(approx(CACHE_X[i + 1] - CACHE_X[i], 24, 1e-9) and approx(CACHE_Y[i + 1] - CACHE_Y[i], 24, 1e-9) for i in range(2))
        add("CENTER CACHE marks: 24-in pitch centred on (324, 162)", pitch_ok and approx(sum(CACHE_X) / 3, CX, 1e-9) and approx(sum(CACHE_Y) / 3, CY, 1e-9),
            "grid from §6")
        Pm = Plan(cm)
        errs, halves = [], []
        for g in grid:
            ok, e, h = xmark_probe(Pm, *g)
            halves.append(h)
            if not ok:
                errs.append((g, sorted(set(e))))
        add("CENTER CACHE marks: each a 12-in X of 2-in bars on the 45-degree diagonals (angle rule)", not errs,
            "%s" % errs[:3] if errs else "all 9 marks; arm (centre to tip) %.3f in -> strokes %.2f in tip-to-tip, overall span %.2f in"
            % (halves[0], 2 * halves[0], 2 * (halves[0] * math.sqrt(0.5) + TW / 2 * math.sqrt(0.5))))
        # staged SUPPLIES placed exactly on the mark centres (§6 CAD notes)
        if staged:
            off = []
            for r in staged:
                b = f.bbox([r])
                c = ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2)
                gd = min(math.hypot(c[0] - g[0], c[1] - g[1]) for g in grid)
                off.append((r["name"], round(gd, 3)))
            add("CENTER CACHE marks: one staged SUPPLY centred on each mark (§6 'exactly on mark centers')",
                len(staged) == 9 and all(d <= 0.02 for _, d in off), "%s" % [o for o in off if o[1] > 0.02] or "9 on centre")

    for s in SIDES:
        white, border = groups[s + " STAGE"], groups[s + " STAGE BORDER"]
        if not white:
            continue
        cents = []
        for r in white:
            for sld in r["solids"]:
                b = box6(sld)
                cents.append(((b[0] + b[3]) / 2, (b[1] + b[4]) / 2))
        want = [(STAGE_X[s], y) for y in STAGE_Y]
        add("%s staging marks: 3 marks at X = %g, Y = 108/162/216" % (s, STAGE_X[s]),
            len(cents) == 3 and all(any(abs(c[0] - w[0]) < 0.01 and abs(c[1] - w[1]) < 0.01 for c in cents) for w in want),
            "centres %s" % [(round(a, 3), round(b, 3)) for a, b in cents])
        Pw = Plan(white)
        probes = {w: xmark_probe(Pw, *w) for w in want}
        errs = [(w, sorted(set(v[1]))) for w, v in probes.items() if not v[0]]
        whalf = probes[want[0]][2]
        add("%s staging marks: white 12-in X of 2-in bars on the diagonals" % s, not errs,
            "%s" % errs[:3] if errs else "ok; white arm %.3f in" % whalf)
        if border:
            Pb = Plan(border)
            ov = f.common_volume(white, border)
            c = math.sqrt(0.5)
            miss = []
            for w in want:
                for ux, uy in ((c, c), (-c, c), (-c, -c), (c, -c)):
                    vx, vy = -uy, ux
                    for dist in (2.5, 4.5):
                        for sg in (1, -1):
                            p = (w[0] + ux * dist + sg * vx * (TW / 2 + EPS), w[1] + uy * dist + sg * vy * (TW / 2 + EPS))
                            if not Pb.has(*p):
                                miss.append((w, round(dist, 1)))
                    p = (w[0] + ux * (whalf + EPS), w[1] + uy * (whalf + EPS))
                    if not Pb.has(*p):
                        miss.append((w, "tip"))
            bw = arm_len(Plan(white + border), STAGE_X[s], STAGE_Y[0], c, c) if s == "BLUE" else \
                arm_len(Plan(white + border), *rot((STAGE_X["BLUE"], STAGE_Y[0])), -c, -c)
            add("%s staging marks: alliance-colour border surrounds the white X without overlapping it" % s,
                ov <= VOL_TOL and not miss,
                "overlap %.2e; border missing at %s; border beyond the white tip %.3f in" % (ov, miss[:4], bw - whalf))
            nb = sum(len(r["solids"]) for r in border)
            add("%s staging marks: one border per mark" % s, nb == 3, "%d border solids" % nb)
        # §6 FIELD SETUP CHART (b): 2 pieces of ONE type per mark, staged on the mark
        chart = {"BLUE": {108.0: "CACHE CRATE", 162.0: "O2 CELL", 216.0: "ROPE COIL"},
                 "RED": {108.0: "ROPE COIL", 162.0: "O2 CELL", 216.0: "CACHE CRATE"}}[s]
        pcs = safe_find(f, "re:- %s staging mark #" % s)
        if pcs:
            bad = []
            for w in want:
                near = [r for r in pcs if math.hypot((f.bbox([r])[0] + f.bbox([r])[3]) / 2 - w[0],
                                                     (f.bbox([r])[1] + f.bbox([r])[4]) / 2 - w[1]) < 20]
                types = sorted({r["name"].split(" - ")[0] for r in near})
                if len(near) != 2 or types != [chart[w[1]]]:
                    bad.append((w, len(near), types))
                    continue
                b = f.bbox(near)
                if math.hypot((b[0] + b[3]) / 2 - w[0], (b[1] + b[4]) / 2 - w[1]) > 0.05:
                    bad.append((w, "pair centred at (%.3f, %.3f)" % ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2)))
            add("%s staging marks: 2 SUPPLIES of the charted type on each mark, pair centred on the mark (§6 chart b)" % s,
                not bad, "%s" % bad if bad else "ok")

    # ---------------- no two tapes overlap; no tape inside other bodies ---------------------
    items = [(r, s, box6(s)) for r in named_tape for s in r["solids"]]
    worst = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][2], items[j][2]
            if all(a[k] <= b[k + 3] - 1e-6 and b[k] <= a[k + 3] - 1e-6 for k in range(3)):
                v = K._volume(K._solids(K.BRepAlgoAPI_Common(items[i][1], items[j][1]).Shape()))
                if v > VOL_TOL:
                    worst.append((items[i][0]["name"], items[j][0]["name"], round(v / TT, 5)))
    add("overlap: no two tape bodies share area (tolerance 1e-5 in^2)", not worst,
        "overlapping pairs (name, name, in^2): %s" % worst[:6] if worst else "%d tape solids, none overlap" % len(items))
    others = [r for r in f.records() if id(r) not in {id(x) for x in named_tape}]
    hits = []
    for r in others:
        for s2 in r["solids"]:
            ob = box6(s2)
            if ob[2] > TT:
                continue
            for tr, ts, tbx in items:
                if all(tbx[k] <= ob[k + 3] - 1e-6 and ob[k] <= tbx[k + 3] - 1e-6 for k in range(3)):
                    v = K._volume(K._solids(K.BRepAlgoAPI_Common(ts, s2).Shape()))
                    if v > VOL_TOL:
                        hits.append((tr["name"], r["name"], round(v, 7)))
    add("interference: no tape shares volume with any other field body (walls, HEADWALL, CRAG, DEPOT, SUPPLIES)",
        not hits, "%s" % hits[:6] if hits else "clear")

    # ---------------- Red = Blue rotated 180 degrees about (324, 162) ------------------------
    pairs = [("BLUE " + g, "RED " + g) for g in ("BASECAMP", "CLIMB", "LANE", "APRON", "STAGE", "STAGE BORDER")]
    pairs += [(g, g) for g in ("CENTERLINE", "BAND", "CACHE MARK")]
    for a, b in pairs:
        A, B = f.solids(groups[a]), f.solids(groups[b])
        if not A or not B:
            continue
        va, vb = K._volume(A), K._volume(B)
        cv = common_solids(rot_solids(A), B)
        sd = va + vb - 2 * cv
        add("symmetry: %s is %s rotated 180 deg about (324, 162)" % (b, a) if a != b else "symmetry: %s is invariant under the 180-deg rotation" % a,
            sd <= 1e-6 * max(va, 1e-9) + 1e-9, "symmetric difference %.3e in^3 (vol %.5f / %.5f)" % (sd, va, vb))
    # Red colours are Red, Blue are Blue, per name pair (a swapped palette would pass the geometry test)
    for g in ("LANE", "APRON"):
        nb = sorted({r["name"] for r in groups["BLUE " + g]})
        nr = sorted({r["name"] for r in groups["RED " + g]})
        add("naming: %s groups exist for both alliances with matching names" % g,
            [n.replace("BLUE", "") for n in nb] == [n.replace("RED", "") for n in nr], "%s / %s" % (nb, nr))

    # ---------------- informational: fragmentation of the cut tapes ---------------------------
    frag = []
    for g in ("CENTERLINE", "BAND"):
        for r in groups[g]:
            for sld in r["solids"]:
                a = K._volume([sld]) / TT
                if a < 1.0:
                    b = box6(sld)
                    frag.append((g, round(a, 3), (round((b[0] + b[3]) / 2, 2), round((b[1] + b[4]) / 2, 2))))
    add("info: sliver tape bodies (< 1 in^2) left by the overlap booleans (reported, not failed)", True,
        "%d slivers: %s" % (len(frag), frag) if frag else "none")
    return out
