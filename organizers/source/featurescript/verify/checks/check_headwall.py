# -*- coding: utf-8 -*-
"""
Independent checks of the two HEADWALLS: truss (uprights, rails / rung carriers), the nine
rungs per alliance, the rung end brackets, the lower crossbeam, the three 15-degree tag wedges,
and the HEADWALL AprilTag panels they carry (IDs 3/4/5 Blue, 16/17/18 Red).

Expected values come from the package documents only — nothing is read from src/:
  * participants/03-field/FIELD-CAD-PACKAGE.md §0 (angle rule, CRITICAL / (ref) convention, heights to rung
    TOP), §1.1 (placement), §4.1 (plane P, width, lanes, rung table, derived rung positions,
    derived rung-end table, 4.0 clearance + bracket exception, truss top 84, 2x2 section, lower
    crossbeam row, wedge row, tag panel clearance 4.42, BASECAMP clear volume H(X), climb reach),
    §4.2 (bracket-only-in-outer-2.0, straight lane pattern, anchor forward of P prohibited),
    §7 (tags 3-5 / 16-18: X 39 / 609, Z 12, 9.0 panel, 8.125 target, plumb, facing),
    §10 rows 10, 11, 14.
  * organizers/design/DESIGN-SPEC.md §3 HEADWALL (same numbers; 16.0-in wrap band; 28.0 end to end).
  * organizers/source/manual/sections/02-arena.md §3.4 (lanes structurally independent; stagger table) and the
    BASECAMP commentary (H(X), 42 in up to X = 30.5).
  * REVISION-LOG M34 (crossbeam / wedge / panel must not share volume; beam notched or set back).
  * participants/03-field/MATERIALS-AND-COLORS.md §1.2, §2 (truss #8A6D3B, truss-dark #5C4823, rung #9AA0A6;
    steel square tube / steel round bar / steel plate 0.25 / aluminium wedge; tag neutral-white).
  * participants/04-vision/apriltag-field-layout.json (tag 3/4/5/16/17/18 poses).

Construction readings (the package leaves these free; the generator's documented design):
  * each lane's truss is ONE welded frame body "<A> HEADWALL lane n frame" (§4.2 "one lane frame",
    patterned x3): two 2 x 2 uprights running up plane P and 2 x 2 chords across the lane (a bottom
    rail, a carrier behind each rung, a top rail), all in one layer 4.0-6.0 in behind P.  Members
    are measured by sectioning the welded body: across the uprights at w stations clear of every
    chord, and across the chords at a lateral station clear of both uprights;
  * the lower crossbeam is welded to a 2 x 2 standoff at every upright ("<A> HEADWALL lower
    crossbeam"), so its own 2 x 2 section and centreline are measured at the lane centres;
  * 2 x 2 members are solid bars whose material is an effective density: their mass per inch must
    be that of a real 2 x 2 steel square tube (MATERIALS-AND-COLORS §2), wall 0.065-0.25 in.

Frames (built here from the document definition, not from the part code):
  A(side)  alliance frame: Blue = world; Red = world rotated 180 deg about (324, 162).  Local
           coordinates are "Blue-equivalent" (local X = distance from own alliance wall).
  P(side)  plane-P frame: origin on the carpet line of P, x = n = unit normal of P toward the
           field (the side robots climb), z = w = up the plane, y = lateral (Blue-equivalent Y).
           A point's n is its signed normal distance from P (negative = behind P, wall side).
"""
import json
import math
import os

import numpy as np

import kernel_occ as K
from OCP.BRep import BRep_Tool
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_Transform
from OCP.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.TopAbs import TopAbs_VERTEX
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
JSON_PATH = os.path.join(REPO, "participants", "04-vision", "apriltag-field-layout.json")

# ---- document values ------------------------------------------------------------------------
FIELD_L, FIELD_W = 648.0, 324.0                     # §0
P_X = {"BLUE": 48.0, "RED": 600.0}                  # §4.1 plane P carpet line
LEAN = 15.0                                         # §4.1 15 deg from vertical, top toward own wall
HW_Y0, HW_Y1 = 90.0, 234.0                          # §4.1 width 144 (Y 90-234)
LANE_W = 48.0
LANE_C = (114.0, 162.0, 210.0)                      # Blue lane centres (Red = rotation)
RUNGS = ("LEDGE", "CAMP", "SUMMIT")
RUNG_TOP = {"LEDGE": 30.0, "CAMP": 54.0, "SUMMIT": 78.0}      # vertical, carpet to rung TOP
RUNG_OD = 1.5
RUNG_L = 20.0
STAGGER = {"LEDGE": -12.0, "CAMP": 12.0, "SUMMIT": -12.0}    # identical in every lane
DERIVED_X = {"LEDGE": 40.16, "CAMP": 33.73, "SUMMIT": 27.30}  # §4.1 derived (Blue), 2 dp
RUNG_ENDS = {                                        # §4.1 derived rung-end table (Blue)
    "LEDGE": ((92, 112), (140, 160), (188, 208)),
    "CAMP": ((116, 136), (164, 184), (212, 232)),
    "SUMMIT": ((92, 112), (140, 160), (188, 208)),
}
SETBACK = 6.4                                        # "≈ 6.4 in (24 × tan 15°)"
END_TO_END = 28.0                                    # adjacent lanes, same height
MIN_INSIDE_LANE = 2.0
CLR = 4.0                                            # structure >= 4.0 behind P (normal)
BRACKET_ZONE = 2.0                                   # brackets only within 2.0 of each rung end
WRAP_LEN = 16.0                                      # middle 16.0 of every rung clear for wrap
TRUSS_TOP = 84.0                                     # (ref)
TUBE = 2.0                                           # 2-in square tube (ref)
REF_TOL = 0.25                                       # §0: (ref) may float ±0.25
BEAM_Z = 12.0                                        # lower crossbeam centreline (ref)
PANEL_BACK_X = 38.75                                 # panel back / wedge front ("at X = 38.75")
TAG_X = {"BLUE": 39.0, "RED": 609.0}                 # CRITICAL for vision
TAG_Z = 12.0
TAG_IDS = {"BLUE": (3, 4, 5), "RED": (16, 17, 18)}   # lane 1, 2, 3 (Red lane 1 at Y 210)
PANEL = 9.0
PANEL_T = 0.25                                       # (ref)
TARGET = 8.125
TAG_CLR = 4.4                                        # ">= 4.4 in behind plane P" (4.42 computed)
TAG_CLR_PUB = 4.42
H_K, H_X0 = 3.7321, 41.788                           # H(X) = 3.7321 (41.788 - X), under the frames' lower face
FRAME_D = 2.0                                        # (ref) front-layer member depth, 4.0-6.0 behind P
BEAM_SPAN, BEAM_CLEAR = (34.2, 38.6), 10.8           # the lower crossbeam limits H there (FCP §4.1)
H_TABLE = ((0, 156.0), (12, 111.2), (24, 66.4), (30.5, 42.1), (32.6, 34.3), (36, 10.8), (40, 6.7), (41.79, 0.0))
ROBOT_START_H = 42.0                                 # R104 42-in starting configuration
ROBOT_START_X = 30.5
REACH_TO_CL = {"LEDGE": 10.84, "CAMP": 17.27, "SUMMIT": 23.70}   # from FRAME PERIMETER X = 51
REACH_WRAP = {"LEDGE": 11.59, "CAMP": 18.02, "SUMMIT": 24.45}
FP_X = 51.0
DIRECT_INPLANE = 49.69                               # M25: LEDGE -> SUMMIT measured in plane P
DIRECT_BACK = 12.86
RGB = {"truss": (0x8A, 0x6D, 0x3B), "truss-dark": (0x5C, 0x48, 0x23), "rung": (0x9A, 0xA0, 0xA6),
       "neutral-white": (0xF5, 0xF5, 0xF5)}
STEEL_RHO = (7750.0, 8050.0)                         # mild steel, kg/m^3 (plausible band)
TUBE_LB_PER_IN = (0.143, 0.496)                      # 2 x 2 steel square tube, wall 0.065-0.25 in
ALU_RHO = (2640.0, 2810.0)                           # aluminium alloys
M_PER_IN = 0.0254
CAM_Z = (10.0, 20.0)                                 # VISION-GUIDE §5: primary camera 10-20 in
SUPPLY_NAMES = ("CACHE CRATE", "O2 CELL", "ROPE COIL")

S15, C15, T15 = math.sin(math.radians(LEAN)), math.cos(math.radians(LEAN)), math.tan(math.radians(LEAN))

# FCP §4.1 publishes H(X) under the lane frames' lower (wall-side) face, 4.0 + FRAME_D behind P
H_FINDING = "FCP §4.1: H(X) = 3.7321 (41.788 - X), 10.8 under the lower crossbeam (X 34.2-38.6)"


# ---- helpers ------------------------------------------------------------------------------
def fmt(v, n=3):
    return ("%%.%df" % n) % v


def frame_A(f, side):
    if side == "BLUE":
        return f.frame((0, 0, 0), (1, 0, 0), (0, 0, 1))
    return f.frame((FIELD_L, FIELD_W, 0), (-1, 0, 0), (0, 0, 1))


def frame_P(f, side):
    if side == "BLUE":
        return f.frame((P_X["BLUE"], 0, 0), (C15, 0, S15), (-S15, 0, C15))
    return f.frame((P_X["RED"], FIELD_W, 0), (-C15, 0, S15), (S15, 0, C15))


def to_world(F, p):
    return tuple(float(v) for v in F.pt(p))


def shape_in(F, shape):
    return BRepBuilderAPI_Transform(shape, F.trsf(), True).Shape()


def box_in(F, lo, hi):
    b = BRepPrimAPI_MakeBox(gp_Pnt(*lo), gp_Pnt(*hi)).Shape()
    return shape_in(F, b)


def cyl_in(F, base, axis, r, h):
    c = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*base), gp_Dir(*axis)), r, h).Shape()
    return shape_in(F, c)


def loft(rect_a, rect_b):
    """Ruled solid between two 4-point polygons (world points) — their convex hull when the
    rectangles are parallel and corresponding corners are matched."""
    ws = []
    for rect in (rect_a, rect_b):
        mp = BRepBuilderAPI_MakePolygon()
        for p in rect:
            mp.Add(gp_Pnt(*p))
        mp.Close()
        ws.append(mp.Wire())
    ts = BRepOffsetAPI_ThruSections(True, True, 1e-6)
    for w in ws:
        ts.AddWire(w)
    ts.Build()
    return ts.Shape()


def common_shape(a, b):
    op = BRepAlgoAPI_Common(a, b)
    return op.Shape()


def vol(shape):
    return K._volume(K._solids(shape))


def bb_shape(shape):
    b = K.Bnd_Box()
    K.BRepBndLib.AddOptimal_s(shape, b, False, False)
    return K._box6(b)


def bb_overlap(a, b, pad=1e-6):
    return all(a[i] <= b[i + 3] + pad and b[i] <= a[i + 3] + pad for i in range(3))


def vertices(solids):
    out = []
    for s in solids:
        exp = TopExp_Explorer(s, TopAbs_VERTEX)
        while exp.More():
            p = BRep_Tool.Pnt_s(TopoDS.Vertex(exp.Current()))
            out.append((p.X(), p.Y(), p.Z()))
            exp.Next()
    return out


class World:
    """Cached world bboxes, for bbox-prefiltered common volumes against the whole field."""

    def __init__(self, f):
        self.f = f
        self.recs = f.records()
        self.bb = {r["id"]: f.bbox([r]) for r in self.recs}

    def is_floor(self, r):
        m = (r["mat"] or {}).get("name", "").lower()
        return "carpet" in m or "tape" in m

    def intruders(self, shape, exclude=(), skip_floor=True, tol=1e-6):
        sb = bb_shape(shape)
        hits = []
        for r in self.recs:
            if r["id"] in exclude or (skip_floor and self.is_floor(r)):
                continue
            if not bb_overlap(sb, self.bb[r["id"]]):
                continue
            v = 0.0
            for s in r["solids"]:
                v += vol(common_shape(shape, s))
            if v > tol:
                hits.append((r["name"], v, r["id"]))
        return hits


def hit_str(hits, n=6):
    if not hits:
        return "none"
    agg = {}
    for name, v, _ in hits:
        a = agg.setdefault(name, [0, 0.0])
        a[0] += 1
        a[1] += v
    items = sorted(agg.items(), key=lambda kv: -kv[1][1])
    return "; ".join("%s x%d (%.3f in^3)" % (k, c, v) for k, (c, v) in items[:n])


def lane_of(y_local):
    for i, yc in enumerate(LANE_C):
        if yc - LANE_W / 2 - 1e-6 <= y_local <= yc + LANE_W / 2 + 1e-6:
            return i + 1
    return None


def section(f, recs, F, lo, hi):
    """Solids of `recs` inside the box lo..hi of frame F, with their bboxes in F."""
    cut = box_in(F, lo, hi)
    out = []
    for r in recs:
        for sld in r["solids"]:
            for piece in K._solids(common_shape(sld, cut)):
                if vol(piece) > 1e-9:
                    out.append(bb_shape(BRepBuilderAPI_Transform(piece, F.trsf().Inverted(), True).Shape()))
    return out


def tube_mass_ok(f, rec):
    """A 2 x 2 steel member: either hollow steel, or a solid bar whose mass per inch of 2 x 2
    section is a real square tube's (the effective-density reading)."""
    lb_in = f.mass_lb([rec]) / (f.volume([rec]) / (TUBE * TUBE))
    return TUBE_LB_PER_IN[0] <= lb_in <= TUBE_LB_PER_IN[1], lb_in


def rgb_ok(rec, tok):
    return tuple(int(round(v)) for v in rec["rgb"]) == RGB[tok] and abs(rec["alpha"] - 1.0) < 1e-9


def mat_ok(rec, kind):
    m = rec["mat"] or {}
    name = m.get("name", "").lower()
    rho = m.get("density", 0.0)
    if kind == "steel":
        return "steel" in name and STEEL_RHO[0] <= rho <= STEEL_RHO[1]
    return ("alumin" in name) and ALU_RHO[0] <= rho <= ALU_RHO[1]


# ---- the checks ---------------------------------------------------------------------------
def run(f):
    out = []

    def ck(label, ok, detail):
        out.append((label, bool(ok), detail))

    W = World(f)
    js = {t["ID"]: t for t in json.load(open(JSON_PATH))["tags"]}

    # document self-consistency of the derived numbers the checks lean on
    for r in RUNGS:
        zc = RUNG_TOP[r] - RUNG_OD / 2
        ck("doc: derived rung centre X for %s = 48 - Zc tan15 rounds to %.2f" % (r, DERIVED_X[r]),
           abs((48 - zc * T15) - DERIVED_X[r]) < 0.005, "48 - %.2f tan15 = %.4f" % (zc, 48 - zc * T15))
    ck("doc: H(X) constants: 41.788 = 48 - (4.0 + 2.0)/cos15 and 3.7321 = 1/tan15",
       abs((48 - (CLR + FRAME_D) / C15) - H_X0) < 5e-4 and abs(1 / T15 - H_K) < 5e-4,
       "48 - 6/cos15 = %.4f, 1/tan15 = %.5f" % (48 - (CLR + FRAME_D) / C15, 1 / T15))
    bad = [(x, h, H_K * (H_X0 - x)) for x, h in H_TABLE
           if not BEAM_SPAN[0] <= x <= BEAM_SPAN[1] and abs(H_K * (H_X0 - x) - h) > 0.051]
    bad += [(x, h, BEAM_CLEAR) for x, h in H_TABLE if BEAM_SPAN[0] <= x <= BEAM_SPAN[1] and abs(h - BEAM_CLEAR) > 0.051]
    ck("doc: H(X) table values follow the formula (and the crossbeam value under the crossbeam)", not bad,
       "mismatches: %s" % bad if bad else "all %d within 0.05" % len(H_TABLE))

    rot = K.Frame((FIELD_L, FIELD_W, 0), (-1, 0, 0), (0, 0, 1))   # 180 deg about (324, 162)
    all_hw_ids = {}

    for side in ("BLUE", "RED"):
        A = frame_A(f, side)
        PF = frame_P(f, side)
        pre = "%s HEADWALL" % side

        hw = f.find("re:^%s HEADWALL " % side)
        all_hw_ids[side] = hw
        rungs = {}
        for li in (1, 2, 3):
            for r in RUNGS:
                try:
                    rungs[(li, r)] = f.find("%s lane %d %s RUNG" % (pre, li, r))
                except KeyError:
                    rungs[(li, r)] = []
        brackets = f.find("%s rung end bracket" % pre)
        frames = {}
        for li in (1, 2, 3):
            try:
                frames[li] = f.find("%s lane %d frame" % (pre, li))
            except KeyError:
                frames[li] = []
        frame_recs = [x for v in frames.values() for x in v]
        beam = f.find("%s lower crossbeam" % pre)
        wedges = f.find("%s tag wedge bracket" % pre)
        tags = {}
        for li, tid in enumerate(TAG_IDS[side]):
            tags[li + 1] = f.find("re:^AprilTag %d - " % tid)
        rung_recs = [x for v in rungs.values() for x in v]
        rung_ids = {x["id"] for x in rung_recs}
        bracket_ids = {x["id"] for x in brackets}

        # ---------------- counts, names ----------------
        ck("%s: 9 rungs, one per lane per LEDGE/CAMP/SUMMIT, each one body" % pre,
           all(len(v) == 1 for v in rungs.values()) and len(rung_recs) == 9,
           "per-name counts %s" % sorted({k: len(v) for k, v in rungs.items()}.items()))
        ck("%s: 2 rung end brackets per rung (18)" % pre, len(brackets) == 18, "found %d" % len(brackets))
        ck("%s: one lower crossbeam, three tag wedge brackets, three lane tag panels" % pre,
           len(beam) == 1 and len(wedges) == 3 and all(len(v) == 1 for v in tags.values()),
           "crossbeam %d, wedges %d, tags %s" % (len(beam), len(wedges), [len(v) for v in tags.values()]))
        ck("%s: every lane has its own welded frame, one body and one solid, inside its lane" % pre,
           all(len(frames[li]) == 1 and len(frames[li][0]["solids"]) == 1 and
               lane_of(f.bbox(frames[li], A)[1] + 1e-3) == li and lane_of(f.bbox(frames[li], A)[4] - 1e-3) == li
               for li in (1, 2, 3)),
           "; ".join("lane %d: %d bodies, %s solids, local Y %s" % (
               li, len(frames[li]), [len(x["solids"]) for x in frames[li]],
               "-".join(fmt(v) for v in (f.bbox(frames[li], A)[1], f.bbox(frames[li], A)[4])) if frames[li] else "-")
               for li in (1, 2, 3)))
        ck("%s lower crossbeam: one welded body, one solid" % pre, len(beam) == 1 and len(beam[0]["solids"]) == 1,
           "%d bodies, solids %s" % (len(beam), [len(x["solids"]) for x in beam]))

        # ---------------- rungs ----------------
        xc_meas = {}
        for li in (1, 2, 3):
            yc = LANE_C[li - 1]
            for r in RUNGS:
                rs = rungs[(li, r)]
                if not rs:
                    continue
                tag = "%s lane %d %s RUNG" % (pre, li, r)
                b = f.bbox(rs, A)
                bp = f.bbox(rs, PF)
                top = RUNG_TOP[r]
                zc = top - RUNG_OD / 2
                xc = 48 - zc * T15
                y0, y1 = RUNG_ENDS[r][li - 1]
                ck(tag + ": top at %.0f (CRITICAL, vertical from carpet)" % top, abs(b[5] - top) < 1e-3,
                   "top Z %s" % fmt(b[5], 4))
                ck(tag + ": OD 1.5 (X and Z extent)", abs(b[3] - b[0] - RUNG_OD) < 1e-3 and abs(b[5] - b[2] - RUNG_OD) < 1e-3,
                   "X extent %s, Z extent %s" % (fmt(b[3] - b[0], 4), fmt(b[5] - b[2], 4)))
                ck(tag + ": ends at Y %d-%d (derived table; Red by rotation), length 20.0" % (y0, y1),
                   abs(b[1] - y0) < 1e-3 and abs(b[4] - y1) < 1e-3,
                   "local Y %s-%s (world Y %s-%s)" % (fmt(b[1]), fmt(b[4]),
                                                      fmt(min(to_world(A, (0, b[1], 0))[1], to_world(A, (0, b[4], 0))[1])),
                                                      fmt(max(to_world(A, (0, b[1], 0))[1], to_world(A, (0, b[4], 0))[1]))))
                ck(tag + ": stagger %+.1f from the lane centre" % STAGGER[r],
                   abs(0.5 * (b[1] + b[4]) - yc - STAGGER[r]) < 1e-3, "centre offset %s" % fmt(0.5 * (b[1] + b[4]) - yc))
                xm = 0.5 * (b[0] + b[3])
                xc_meas[(li, r)] = xm
                ck(tag + ": centre X = derived %.2f (world %s)" % (DERIVED_X[r], fmt(to_world(A, (DERIVED_X[r], 0, 0))[0], 2)),
                   abs(xm - xc) < 1e-3 and abs(xm - DERIVED_X[r]) < 0.005, "local X centre %s, exact %s" % (fmt(xm, 4), fmt(xc, 4)))
                ck(tag + ": centreline lies in plane P (n = 0 +/- 0.75)", abs(bp[0] + RUNG_OD / 2) < 1e-3 and abs(bp[3] - RUNG_OD / 2) < 1e-3,
                   "n %s .. %s" % (fmt(bp[0], 4), fmt(bp[3], 4)))
                v = f.volume(rs)
                vexp = math.pi * (RUNG_OD / 2) ** 2 * RUNG_L
                corner = (xm + 0.7, 0.5 * (b[1] + b[4]), zc + 0.7)
                ck(tag + ": solid round bar (volume pi r^2 L, square corner empty)",
                   abs(v - vexp) < 0.01 and not f.inside(rs, corner, A) and f.inside(rs, (xm, 0.5 * (b[1] + b[4]), zc), A),
                   "volume %s vs %s" % (fmt(v), fmt(vexp)))
                ck(tag + ": >= 2.0 inside its lane", b[1] - (yc - LANE_W / 2) >= MIN_INSIDE_LANE - 1e-6 and
                   (yc + LANE_W / 2) - b[4] >= MIN_INSIDE_LANE - 1e-6,
                   "margins %s / %s" % (fmt(b[1] - (yc - LANE_W / 2)), fmt((yc + LANE_W / 2) - b[4])))
                ck(tag + ": colour rung #9AA0A6, steel round bar", rgb_ok(rs[0], "rung") and mat_ok(rs[0], "steel"),
                   "rgb %s alpha %s mat %s" % (rs[0]["rgb"], rs[0]["alpha"], rs[0]["mat"]))
                # climb reach (G416 arithmetic): frame perimeter at X >= 51
                ck(tag + ": climb reach to centreline %.2f / to wrap %.2f" % (REACH_TO_CL[r], REACH_WRAP[r]),
                   abs((FP_X - xm) - REACH_TO_CL[r]) < 0.006 and abs((FP_X - xm + RUNG_OD / 2) - REACH_WRAP[r]) < 0.006,
                   "%s / %s" % (fmt(FP_X - xm), fmt(FP_X - xm + RUNG_OD / 2)))
        # rung relationships
        for li in (1, 2, 3):
            if all(rungs[(li, r)] for r in RUNGS):
                sb = [xc_meas[(li, "LEDGE")] - xc_meas[(li, "CAMP")], xc_meas[(li, "CAMP")] - xc_meas[(li, "SUMMIT")]]
                ck("%s lane %d: horizontal setback between successive rungs %.1f (24 tan15)" % (pre, li, SETBACK),
                   all(abs(x - 24 * T15) < 1e-3 and abs(x - SETBACK) < 0.05 for x in sb), "setbacks %s" % [fmt(x) for x in sb])
                bl = f.bbox(rungs[(li, "LEDGE")], A)
                bc = f.bbox(rungs[(li, "CAMP")], A)
                bs = f.bbox(rungs[(li, "SUMMIT")], A)
                gap = bc[1] - bl[4]
                ck("%s lane %d: no lateral position engages two successive rungs (LEDGE/CAMP, CAMP/SUMMIT Y spans disjoint)" % (pre, li),
                   gap > 0 and bc[1] - bs[4] > 0, "LEDGE ..%s, CAMP %s.., SUMMIT ..%s" % (fmt(bl[4]), fmt(bc[1]), fmt(bs[4])))
                d_in = math.hypot(48.0, xc_meas[(li, "LEDGE")] - xc_meas[(li, "SUMMIT")])
                ck("%s lane %d: direct LEDGE->SUMMIT is 48 up, %.2f back, %.2f in plane P (M25)" % (pre, li, DIRECT_BACK, DIRECT_INPLANE),
                   abs(xc_meas[(li, "LEDGE")] - xc_meas[(li, "SUMMIT")] - DIRECT_BACK) < 0.006 and abs(d_in - DIRECT_INPLANE) < 0.006,
                   "back %s, in-plane %s" % (fmt(xc_meas[(li, 'LEDGE')] - xc_meas[(li, 'SUMMIT')]), fmt(d_in)))
        for r in RUNGS:
            for li in (1, 2):
                a, b2 = rungs[(li, r)], rungs[(li + 1, r)]
                if a and b2:
                    ba, bb = f.bbox(a, A), f.bbox(b2, A)
                    cc = 0.5 * (bb[1] + bb[4]) - 0.5 * (ba[1] + ba[4])
                    d = f.dist(a, b2)
                    ck("%s %s RUNG lanes %d/%d: 48.0 centre to centre, 28.0 end to end" % (pre, r, li, li + 1),
                       abs(cc - LANE_W) < 1e-3 and abs(d - END_TO_END) < 1e-3, "c-c %s, gap %s" % (fmt(cc), fmt(d)))

        # ---------------- clearance behind plane P (CRITICAL) ----------------
        for grp, recs in (("lane frames (uprights, rails and rung carriers)", frame_recs), ("lower crossbeam", beam),
                          ("tag wedge brackets", wedges)):
            mx = max(f.bbox([x], PF)[3] for x in recs)
            ck("%s: %s >= 4.0 behind plane P (normal)" % (pre, grp), mx <= -CLR + 1e-6, "max n = %s (need <= -4.0)" % fmt(mx, 4))
        # the published field-side face X_t(Z) = 43.859 - 0.26795 Z is this model's face
        mx_truss = max(f.bbox([x], PF)[3] for x in frame_recs + beam)
        ck("%s: truss field-side face lies on the 4.0 surface (X_t(Z) = 43.859 - 0.26795 Z)" % pre,
           abs(mx_truss + CLR) < 1e-3, "front-most truss n = %s" % fmt(mx_truss, 4))

        # band 0 < depth < 4.0 behind P: only rungs and rung end brackets may be in it
        band = common_shape(box_in(PF, (-CLR + 1e-3, HW_Y0 - 2, -2), (0.0, HW_Y1 + 2, 100)),
                            box_in(A, (-5, -5, 0.02), (FIELD_L / 2, FIELD_W + 5, 110)))
        hits = W.intruders(band, exclude=rung_ids | bracket_ids)
        ck("%s: the 4.0-in band behind P holds nothing but rungs and rung end brackets" % pre, not hits,
           "intruders: %s" % hit_str(hits))
        # brackets: only within the outer 2.0 in of each rung end, inside the lane
        per_rung = {k: [] for k in rungs}
        stray = []
        for bk in brackets:
            bb = f.bbox([bk], A)
            bpb = f.bbox([bk], PF)
            owner = None
            for k, rs in rungs.items():
                if not rs:
                    continue
                rb = f.bbox(rs, A)
                if bb[1] >= rb[1] - 1e-6 and bb[4] <= rb[4] + 1e-6 and f.dist([bk], rs) < 1e-6:
                    owner = k
            if owner is None:
                stray.append((bk["id"], [fmt(x) for x in bb]))
                continue
            rb = f.bbox(rungs[owner], A)
            end_lo = bb[4] <= rb[1] + BRACKET_ZONE + 1e-6
            end_hi = bb[1] >= rb[4] - BRACKET_ZONE - 1e-6
            per_rung[owner].append((bk, end_lo, end_hi, bb, bpb))
        ck("%s: every rung end bracket sits on a rung (touches it, within its length)" % pre, not stray, "stray: %s" % stray[:4])
        ok_zone, ok_pair, det = True, True, []
        for k, lst in per_rung.items():
            lo = [x for x in lst if x[1]]
            hi = [x for x in lst if x[2]]
            if len(lst) != 2 or len(lo) != 1 or len(hi) != 1:
                ok_pair = False
                det.append("lane %d %s: %d brackets (%d low end, %d high end)" % (k[0], k[1], len(lst), len(lo), len(hi)))
            for bk, el, eh, bb, bpb in lst:
                if not (el or eh):
                    ok_zone = False
                    det.append("%s Y %s-%s outside both 2.0-in end zones" % (bk["id"][2:4], fmt(bb[1]), fmt(bb[4])))
        ck("%s: rung end brackets only within the outer 2.0 in of each rung end (middle 16.0 bracket-free)" % pre, ok_zone,
           "; ".join(det) if det else "all 18 inside an end zone")
        ck("%s: exactly one bracket at each end of every rung" % pre, ok_pair, "; ".join(det) if det else "9 x (1 + 1)")
        in_lane = True
        for bk in brackets:
            la, lb = lane_of(f.bbox([bk], A)[1]), lane_of(f.bbox([bk], A)[4])
            in_lane = in_lane and la is not None and la == lb
        ck("%s: rung end brackets stay inside their lane" % pre, in_lane, "")
        bt = sorted({round(f.bbox([bk], A)[4] - f.bbox([bk], A)[1], 4) for bk in brackets})
        ck("%s: rung end bracket = steel plate 0.25 thick, colour truss-dark" % pre,
           bt == [0.25] and all(rgb_ok(bk, "truss-dark") and mat_ok(bk, "steel") for bk in brackets),
           "thickness %s, rgb %s, mat %s" % (bt, brackets[0]["rgb"], brackets[0]["mat"]))
        sup = all(min(f.dist([bk], [t]) for t in frame_recs) < 1e-6 for bk in brackets)
        ck("%s: every rung end bracket is carried by its lane frame (contact)" % pre, sup, "")
        ov = sum(f.common_volume([bk], rungs[k]) for k, lst in per_rung.items() for bk, *_ in lst)
        ck("%s: rung passes through its brackets without shared volume" % pre, ov < 1e-6, "common volume %s" % fmt(ov, 6))
        # climbing volume: nothing but rungs (and bracket plates, reported below) forward of P
        fwd = common_shape(box_in(PF, (0.0, HW_Y0 - 2, -2), (30.0, HW_Y1 + 2, 100)),
                           box_in(A, (-5, -5, 0.02), (FIELD_L / 2, FIELD_W + 5, 110)))
        hits = W.intruders(fwd, exclude=rung_ids | bracket_ids)
        ck("%s: nothing but rungs / rung brackets forward of plane P (climbing volume; anchors forward of P prohibited)" % pre,
           not hits, "intruders: %s" % hit_str(hits))
        bmax = max(f.bbox([bk], PF)[3] for bk in brackets)
        ck("%s: rung end brackets do not stand proud of the rung's front surface into the climbing volume (n <= +0.75)" % pre,
           bmax <= RUNG_OD / 2 + 1e-6,
           "bracket front at n = %s (rung front 0.75): plates reach %s in forward of P, %s proud of the rung, "
           "%s in horizontally in front of the LEDGE rung face" % (fmt(bmax), fmt(bmax), fmt(bmax - RUNG_OD / 2),
                                                                    fmt((bmax - RUNG_OD / 2) / C15)))
        # hook wrap: a 4.0-in-radius cylinder about the middle 16.0 in of each rung is empty
        bad = []
        dmin = 1e9
        for k, rs in rungs.items():
            if not rs:
                continue
            rb = f.bbox(rs, A)
            xm = 0.5 * (rb[0] + rb[3])
            zc = 0.5 * (rb[2] + rb[5])
            cyl = cyl_in(A, (xm, rb[1] + BRACKET_ZONE, zc), (0, 1, 0), CLR - 1e-3, WRAP_LEN)
            h = W.intruders(cyl, exclude={x["id"] for x in rs})
            if h:
                bad.append("lane %d %s: %s" % (k[0], k[1], hit_str(h)))
            dmin = min(dmin, f.dist(rs, frame_recs + beam + wedges))
        ck("%s: hook-wrap envelope (R 4.0 about the axis, middle 16.0 in) of all 9 rungs is empty" % pre, not bad,
           "; ".join(bad) if bad else "empty")
        ck("%s: rung to nearest truss member >= 3.25 (4.0 - rung radius)" % pre, dmin >= CLR - RUNG_OD / 2 - 1e-6,
           "min distance %s" % fmt(dmin, 4))

        # ---------------- truss form (ref) ----------------
        zmax = max(W.bb[x["id"]][5] for x in hw)
        zmin = min(W.bb[x["id"]][2] for x in hw)
        ck("%s: structure top at 84 (ref, +/-0.25) and no rung above it" % pre,
           abs(zmax - TRUSS_TOP) <= REF_TOL and max(RUNG_TOP.values()) < zmax, "top Z %s" % fmt(zmax))
        ck("%s: stands on the carpet (lowest point Z 0)" % pre, abs(zmin) < 1e-6, "min Z %s" % fmt(zmin, 5))
        # uprights: sections across each lane frame at w stations clear of every chord
        w_st = (15.0, 42.0, 67.0)
        bad_up, n_up = [], []
        for li in (1, 2, 3):
            yl = LANE_C[li - 1]
            for w0 in w_st:
                secs = section(f, frames[li], PF, (-30.0, yl - LANE_W / 2, w0), (30.0, yl + LANE_W / 2, w0 + 0.5))
                n_up.append(len(secs))
                for b in secs:
                    if not (abs(b[3] - b[0] - TUBE) < 1e-3 and abs(b[4] - b[1] - TUBE) < 1e-3 and abs(b[5] - b[2] - 0.5) < 1e-3):
                        bad_up.append("lane %d w %g: n x y x w %s x %s x %s" % (li, w0, fmt(b[3] - b[0]), fmt(b[4] - b[1]), fmt(b[5] - b[2])))
        ck("%s: each lane frame has two uprights, 2 x 2 tube running up plane P (15 deg from vertical)" % pre,
           n_up == [2] * (3 * len(w_st)) and not bad_up,
           "sections per lane/station %s; off-size %s" % (n_up, bad_up[:4]))
        # chords: sections across each lane frame at a lateral station clear of both uprights
        bad_ch, n_ch = [], []
        for li in (1, 2, 3):
            yl = LANE_C[li - 1] + 5.0
            secs = section(f, frames[li], PF, (-30.0, yl, -10.0), (30.0, yl + 0.5, 120.0))
            n_ch.append(len(secs))
            for b in secs:
                if not (abs(b[3] - b[0] - TUBE) < 1e-3 and abs(b[5] - b[2] - TUBE) < 1e-3):
                    bad_ch.append("lane %d: n x w %s x %s" % (li, fmt(b[3] - b[0]), fmt(b[5] - b[2])))
        ck("%s: lane frame chords (bottom rail, a carrier behind each rung, top rail) are 2 x 2 tube in a P-parallel layer" % pre,
           all(n >= 2 for n in n_ch) and not bad_ch, "chords per lane %s; off-size %s" % (n_ch, bad_ch[:4]))
        # crossbeam: its own section at each lane centre, clear of the standoffs at the uprights
        bad_bm = []
        for yc in LANE_C:
            secs = section(f, beam, PF, (-30.0, yc, -10.0), (30.0, yc + 0.5, 120.0))
            if len(secs) != 1 or abs(secs[0][3] - secs[0][0] - TUBE) > 1e-3 or abs(secs[0][5] - secs[0][2] - TUBE) > 1e-3:
                bad_bm.append("Y %g: %s" % (yc, [(fmt(b[3] - b[0]), fmt(b[5] - b[2])) for b in secs]))
        ck("%s: lower crossbeam is 2 x 2 tube in a P-parallel layer (section at each lane centre)" % pre, not bad_bm,
           "; ".join(bad_bm) or "3 sections 2 x 2")
        mass = [(x["name"],) + tube_mass_ok(f, x) for x in frame_recs + beam]
        ck("%s: lane frames and crossbeam are 2 x 2 steel square tube (mass per inch of a real tube), colour truss" % pre,
           all(m[1] for m in mass) and all(rgb_ok(x, "truss") and "steel" in ((x["mat"] or {}).get("name", "").lower())
                                           for x in frame_recs + beam),
           "lb/in %s; rgb %s mat %s" % ([(m[0], fmt(m[2], 3)) for m in mass], frame_recs[0]["rgb"] if frame_recs else "-",
                                      frame_recs[0]["mat"] if frame_recs else "-"))
        loc = [f.bbox([x], A) for x in hw]
        ck("%s: width 144 — all structure within Y 90-234 and spanning it (Red by rotation)" % pre,
           min(b_[1] for b_ in loc) >= HW_Y0 - 1e-6 and max(b_[4] for b_ in loc) <= HW_Y1 + 1e-6 and
           min(b_[1] for b_ in loc) <= HW_Y0 + REF_TOL and max(b_[4] for b_ in loc) >= HW_Y1 - REF_TOL,
           "local Y %s-%s" % (fmt(min(b_[1] for b_ in loc)), fmt(max(b_[4] for b_ in loc))))
        # lanes structurally independent (manual §3.4) — lane frames do not touch each other
        lane_sets = {li: [] for li in (1, 2, 3)}
        for x in frame_recs + brackets + rung_recs:
            b_ = f.bbox([x], A)
            lane_sets[lane_of(0.5 * (b_[1] + b_[4]))].append(x)
        dl = [f.dist(lane_sets[1], lane_sets[2]), f.dist(lane_sets[2], lane_sets[3])]
        ck("%s: lane frames are separate (frames/rungs/brackets of adjacent lanes do not touch)" % pre,
           all(d > 1e-3 for d in dl), "gaps %s (the lower crossbeam alone spans all three lanes)" % [fmt(d) for d in dl])

        # ---------------- lower crossbeam, wedges, tag panels (M34) ----------------
        bb_beam = f.bbox(beam, A)
        zc_beam = []
        for yc in LANE_C:
            secs = section(f, beam, A, (-10.0, yc, -10.0), (100.0, yc + 0.5, 100.0))
            zc_beam += [0.5 * (b[2] + b[5]) for b in secs]
        ck("%s lower crossbeam: centreline Z 12.0 (ref, +/-0.25), measured at the lane centres" % pre,
           len(zc_beam) == 3 and all(abs(z - BEAM_Z) <= REF_TOL for z in zc_beam),
           "centre Z %s" % [fmt(z, 4) for z in zc_beam])
        for li in (1, 2, 3):
            yc = LANE_C[li - 1]
            tid = TAG_IDS[side][li - 1]
            pr = tags[li]
            tb = f.bbox(pr, A)
            tp = f.bbox(pr, PF)
            ttag = "%s lane %d tag %d" % (pre, li, tid)
            ck(ttag + ": panel face plane X = %.1f (local 39.0), back 38.75, plumb (CRITICAL)" % TAG_X[side],
               abs(tb[3] - 39.0) < 1e-3 and abs(tb[0] - (39.0 - PANEL_T)) < 1e-3,
               "local X %s-%s (world face X %s)" % (fmt(tb[0], 4), fmt(tb[3], 4), fmt(to_world(A, (tb[3], 0, 0))[0], 4)))
            ck(ttag + ": centred on the lane (Y %d local) at Z 12, 9.0 square" % yc,
               abs(0.5 * (tb[1] + tb[4]) - yc) < 1e-3 and abs(0.5 * (tb[2] + tb[5]) - TAG_Z) < 1e-3 and
               abs(tb[4] - tb[1] - PANEL) < 1e-3 and abs(tb[5] - tb[2] - PANEL) < 1e-3,
               "Y %s-%s Z %s-%s" % (fmt(tb[1]), fmt(tb[4]), fmt(tb[2]), fmt(tb[5])))
            ck(ttag + ": whole panel >= 4.4 behind P (published 4.42 at the top edge)",
               -tp[3] >= TAG_CLR and abs(-tp[3] - TAG_CLR_PUB) < 0.006, "min depth behind P %s" % fmt(-tp[3], 4))
            ck(ttag + ": panel below the LEDGE RUNG (Z-band clear of every rung)",
               tb[5] < min(f.bbox(rungs[(li, "LEDGE")], A)[2], 1e9) if rungs[(li, "LEDGE")] else False,
               "panel top %s vs LEDGE bottom %s" % (fmt(tb[5]), fmt(f.bbox(rungs[(li, 'LEDGE')], A)[2]) if rungs[(li, 'LEDGE')] else "-"))
            # JSON pose
            t = js[tid]["pose"]
            tr = t["translation"]
            q = t["rotation"]["quaternion"]
            yaw = math.degrees(2 * math.atan2(q["Z"], q["W"]))
            face_c = to_world(A, (39.0, yc, TAG_Z))
            jx, jy, jz = tr["x"] / M_PER_IN, tr["y"] / M_PER_IN, tr["z"] / M_PER_IN
            want_yaw = 0.0 if side == "BLUE" else 180.0
            dec = pr[0].get("decal") or {}
            nrm = dec.get("normal")
            ck(ttag + ": pose matches apriltag-field-layout.json and the decal faces the field",
               abs(jx - face_c[0]) < 0.01 and abs(jy - face_c[1]) < 0.01 and abs(jz - face_c[2]) < 0.01 and
               abs(((yaw - want_yaw + 180) % 360) - 180) < 1e-6 and nrm is not None and
               abs(nrm[0] - (1.0 if side == "BLUE" else -1.0)) < 1e-9 and
               np.linalg.norm(np.asarray(dec.get("origin")) - np.asarray(face_c)) < 1e-6,
               "JSON (%s, %s, %s) yaw %s; model face centre %s decal normal %s origin %s" % (
                   fmt(jx), fmt(jy), fmt(jz), fmt(yaw, 1), [fmt(v) for v in face_c], nrm, dec.get("origin")))
            ck(ttag + ": panel neutral-white", rgb_ok(pr[0], "neutral-white"), "rgb %s" % (pr[0]["rgb"],))
            # the tag's lane matches the rung lane naming (Red lane 1 is at world Y 210)
            wy = to_world(A, (0, yc, 0))[1]
            lane_rungs_y = [0.5 * (W.bb[x["id"]][1] + W.bb[x["id"]][4]) for r in RUNGS for x in rungs[(li, r)]]
            ck(ttag + ": tag and rungs named lane %d share the lane (world Y %.0f)" % (li, wy),
               all(abs(abs(y - wy) - 12.0) < 1e-3 for y in lane_rungs_y) and abs(W.bb[pr[0]["id"]][1] + 4.5 - wy) < 1e-3,
               "rung centres %s, tag Y %s" % ([fmt(y) for y in lane_rungs_y], fmt(W.bb[pr[0]["id"]][1] + 4.5)))
            # M34: crossbeam at the tag station at or behind X = 38.75, wedge between it and the panel
            station = common_shape(beam[0]["solids"][0], box_in(A, (-10, yc - PANEL / 2, -10), (100, yc + PANEL / 2, 100)))
            loc_station = BRepBuilderAPI_Transform(station, A.trsf().Inverted(), True).Shape()
            sbb = bb_shape(loc_station)
            ck(ttag + ": crossbeam field-side face at the tag station at or behind X = 38.75 (M34)", sbb[3] <= PANEL_BACK_X + 1e-6,
               "crossbeam max local X at the station %s" % fmt(sbb[3], 4))
            wd = [w for w in wedges if abs(0.5 * (f.bbox([w], A)[1] + f.bbox([w], A)[4]) - yc) < 1e-3]
            if len(wd) != 1:
                ck(ttag + ": one tag wedge on the lane centre", False, "found %d" % len(wd))
                continue
            wd = wd[0]
            wb = f.bbox([wd], A)
            cv = (f.common_volume([wd], beam), f.common_volume([wd], pr), f.common_volume(beam, pr))
            dd = (f.dist([wd], beam), f.dist([wd], pr))
            ck(ttag + ": crossbeam, wedge and panel share no volume (M34)", max(cv) < 1e-6,
               "wedge^beam %s, wedge^panel %s, beam^panel %s" % tuple(fmt(v, 6) for v in cv))
            ck(ttag + ": panel mounts on the crossbeam through the wedge (both contacts closed)", max(dd) < 1e-6,
               "gaps wedge-beam %s, wedge-panel %s" % tuple(fmt(v, 6) for v in dd))
            ck(ttag + ": wedge lies between the crossbeam face and the panel back, 9.0 wide on the lane centre",
               wb[3] <= PANEL_BACK_X + 1e-6 and wb[0] >= bb_beam[0] - 1e-6 and abs(wb[4] - wb[1] - PANEL) < 1e-3,
               "wedge local X %s-%s, Y width %s" % (fmt(wb[0]), fmt(wb[3]), fmt(wb[4] - wb[1])))
            ck(ttag + ": wedge hidden behind the panel (Y and Z inside the panel outline)",
               wb[1] >= tb[1] - 1e-6 and wb[4] <= tb[4] + 1e-6 and wb[2] >= tb[2] - 1e-6 and wb[5] <= tb[5] + 1e-6,
               "wedge Z %s-%s" % (fmt(wb[2]), fmt(wb[5])))
            # wedge angles: front plumb at 38.75, back face 15 deg from vertical, top toward the wall
            vs = [A.to_local(p) for p in vertices([s for s in wd["solids"]])]
            front = [v for v in vs if abs(v[0] - PANEL_BACK_X) < 1e-6]
            back = [v for v in vs if v[0] < PANEL_BACK_X - 1e-3]
            ang = None
            if back:
                lo = min(back, key=lambda v: v[2])
                hi = max(back, key=lambda v: v[2])
                if hi[2] - lo[2] > 1e-6:
                    ang = math.degrees(math.atan2(lo[0] - hi[0], hi[2] - lo[2]))
            ck(ttag + ": wedge is 15 deg (plumb front at X 38.75, back face 15 deg from vertical, leaning to the wall)",
               len(front) >= 4 and ang is not None and abs(ang - LEAN) < 1e-3,
               "front vertices %d, back-face angle %s deg" % (len(front), fmt(ang, 4) if ang is not None else "-"))
            ck(ttag + ": wedge aluminium, colour truss-dark", mat_ok(wd, "alu") and rgb_ok(wd, "truss-dark"),
               "rgb %s mat %s" % (wd["rgb"], wd["mat"]))
            # target border unobstructed from the field side: hull from the 8.125 target to a camera
            # window 10 ft out, 3 ft either side, at camera heights 10-20 in (VISION-GUIDE §5)
            h = TARGET / 2
            tgt = [(39.0 + 1e-3, yc - h, TAG_Z - h), (39.0 + 1e-3, yc + h, TAG_Z - h), (39.0 + 1e-3, yc + h, TAG_Z + h),
                   (39.0 + 1e-3, yc - h, TAG_Z + h)]
            win = [(159.0, yc - 36, CAM_Z[0]), (159.0, yc + 36, CAM_Z[0]), (159.0, yc + 36, CAM_Z[1]), (159.0, yc - 36, CAM_Z[1])]
            fr = loft([to_world(A, p) for p in tgt], [to_world(A, p) for p in win])
            # field structure only: SUPPLIES are loose pieces (the staged CRATES at X 144 are 8.5 ft out)
            hits = [h_ for h_ in W.intruders(fr, exclude={pr[0]["id"]}) if not h_[0].startswith(SUPPLY_NAMES)]
            ck(ttag + ": 8.125 target unobstructed by field structure (camera band 10-20 in, to 10 ft, +/-3 ft)", not hits and vol(fr) > 1000,
               "sight-hull %s in^3, intruders: %s" % (fmt(vol(fr), 0), hit_str(hits)))

        # ---------------- BASECAMP clear volume (published; governs starting configurations) ----------------
        hwall = hw + [x for v in tags.values() for x in v]
        hw_ids = {x["id"] for x in hwall}

        def hw_intr(shape):
            return [h_ for h_ in W.intruders(shape) if h_[2] in hw_ids]

        # a 42-in robot anywhere in Y 90-234 up to X = 30.5
        rb42 = box_in(A, (0.01, HW_Y0, 0.02), (ROBOT_START_X, HW_Y1, ROBOT_START_H))
        hits = hw_intr(rb42)
        # the X a 42-in robot can actually reach, and the clear height at the table stations
        reach = common_shape(box_in(A, (0.01, HW_Y0, 0.02), (60, HW_Y1, ROBOT_START_H)),
                             K._compound([s for x in hwall for s in x["solids"]]))
        rx = bb_shape(BRepBuilderAPI_Transform(reach, A.trsf().Inverted(), True).Shape())[0] if vol(reach) > 0 else float("nan")
        ck("%s: BASECAMP — a 42-in robot fits anywhere in Y 90-234 up to X = 30.5 (H(30.5) = 42.1)" % pre, not hits,
           "intruders: %s; a 42-in box across Y 90-234 reaches only X = %s. %s" % (hit_str(hits), fmt(rx), H_FINDING))
        stations = []
        okH = True
        for x, hpub in H_TABLE[1:-1]:
            col = common_shape(box_in(A, (0.01, HW_Y0, 0.02), (x, HW_Y1, 200)), K._compound([s for y in hwall for s in y["solids"]]))
            if vol(col) > 1e-6:
                zlow = bb_shape(BRepBuilderAPI_Transform(col, A.trsf().Inverted(), True).Shape())[2]
            else:
                zlow = float("inf")
            stations.append("X %s: published %s, clear %s" % (fmt(x, 1), fmt(hpub, 1), fmt(zlow, 1)))
            if zlow < hpub - 0.05:
                okH = False
        ck("%s: BASECAMP clear height under the truss >= published H(X) at X = 12/24/30.5/32.6/36/40" % pre, okH,
           "%s. %s" % ("; ".join(stations), H_FINDING))
        # between the uprights of each lane (lane centre +/- 15): the same 42-in robot
        mid_ok, mid_det = True, []
        for yc in LANE_C:
            h_ = hw_intr(box_in(A, (0.01, yc - 15, 0.02), (ROBOT_START_X, yc + 15, ROBOT_START_H)))
            if h_:
                mid_ok = False
                mid_det.append("lane Y %d: %s" % (yc, hit_str(h_)))
        ck("%s: BASECAMP — a 30-in-wide 42-in robot centred on a lane fits up to X = 30.5" % pre, mid_ok,
           "; ".join(mid_det) if mid_det else "clear in all three lanes")

    # ---------------- §4.2: the lane is linear-patterned x3 at 48 in, no mirroring ----------------
    from OCP.gp import gp_Trsf, gp_Vec
    for side, key in (("BLUE", "hwBlue"), ("RED", "hwRed")):
        A = frame_A(f, side)
        lanes = {li: {r["id"][3:]: r for r in f.records() if len(r["id"]) > 3 and r["id"][1] == key and r["id"][2] == "lane%d" % li}
                 for li in (1, 2, 3)}
        worst, miss = 0.0, []
        for li in (2, 3):
            d = A.dir((0, 1, 0)) * LANE_W * (li - 1)
            t = gp_Trsf()
            t.SetTranslation(gp_Vec(*d))
            miss += sorted(set(lanes[1]) ^ set(lanes[li]))
            for k in set(lanes[1]) & set(lanes[li]):
                a, b = lanes[1][k], lanes[li][k]
                cv = 0.0
                for sa in a["solids"]:
                    ta = BRepBuilderAPI_Transform(sa, t, True).Shape()
                    for sb in b["solids"]:
                        cv += vol(common_shape(ta, sb))
                worst = max(worst, abs(cv - f.volume([a])), abs(cv - f.volume([b])))
        ck("%s HEADWALL: lanes 2 and 3 are lane 1 translated 48 / 96 in (straight pattern, same stagger, no mirroring)" % side,
           not miss and worst < 1e-4 and len(lanes[1]) > 0,
           "%d bodies per lane; unmatched %s; worst volume mismatch %s" % (len(lanes[1]), miss[:4], fmt(worst, 6)))

    # ---------------- Red = Blue rotated 180 deg about (324, 162) ----------------
    blue = {r["id"][2:]: r for r in f.records() if len(r["id"]) > 1 and r["id"][1] == "hwBlue"}
    red = {r["id"][2:]: r for r in f.records() if len(r["id"]) > 1 and r["id"][1] == "hwRed"}
    miss = sorted(set(blue) ^ set(red))
    worst, bad_names = 0.0, []
    for k in sorted(set(blue) & set(red)):
        b, r = blue[k], red[k]
        if b["name"].replace("BLUE", "RED", 1) != r["name"] or b["rgb"] != r["rgb"] or b["mat"] != r["mat"]:
            bad_names.append(k)
        vb = f.volume([b])
        vr = f.volume([r])
        cv = 0.0
        for sb in b["solids"]:
            rs_ = BRepBuilderAPI_Transform(sb, rot.trsf(), True).Shape()
            for sr in r["solids"]:
                cv += vol(common_shape(rs_, sr))
        worst = max(worst, abs(vb - cv), abs(vr - cv))
    ck("RED HEADWALL = BLUE HEADWALL rotated 180 deg about (324, 162), body for body", not miss and worst < 1e-4,
       "%d bodies each side; unmatched %s; worst volume mismatch %s in^3" % (len(blue), miss[:4], fmt(worst, 6)))
    ck("RED HEADWALL bodies carry the Blue names (alliance swapped), colours and materials", not bad_names, "mismatched %s" % bad_names[:4])
    for tb_, tr_ in zip(TAG_IDS["BLUE"], TAG_IDS["RED"]):
        a = f.find("re:^AprilTag %d - " % tb_)
        b = f.find("re:^AprilTag %d - " % tr_)
        cv = sum(vol(common_shape(BRepBuilderAPI_Transform(s, rot.trsf(), True).Shape(), t)) for s in a[0]["solids"] for t in b[0]["solids"])
        ck("tag %d = tag %d rotated 180 deg about (324, 162)" % (tr_, tb_), abs(cv - f.volume(b)) < 1e-6 and abs(cv - f.volume(a)) < 1e-6,
           "common %s of %s" % (fmt(cv, 5), fmt(f.volume(b), 5)))

    # ---------------- interference: HEADWALL bodies + lane tags against everything ----------------
    pairs, seen = [], set()
    for side in ("BLUE", "RED"):
        for x in all_hw_ids[side] + [t for tid in TAG_IDS[side] for t in f.find("re:^AprilTag %d - " % tid)]:
            for s in x["solids"]:
                for h_ in W.intruders(s, exclude={x["id"]}, skip_floor=False):
                    key = tuple(sorted([str(x["id"]), str(h_[2])]))
                    if key not in seen:
                        seen.add(key)
                        pairs.append("%s ^ %s = %s" % (x["name"], h_[0], fmt(h_[1], 5)))
    ck("HEADWALLS: no body shares volume with any other body on the field", not pairs, "; ".join(pairs[:6]) if pairs else "none")
    return out
