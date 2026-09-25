# -*- coding: utf-8 -*-
"""
CRAG SHELF FACE — Shelf 1 / Shelf 2, slot fences, shelf gussets, the Summit Socket and its
mast, on both CRAGS.

Every expected value below is taken from the package documents, never from src/:

  FIELD-CAD-PACKAGE  §0   inches, always-blue-origin NWU, (ref) floats +/-0.25, "every angle
                          on the field is 15, 30 or 45 degrees", heights to the interaction surface
                     §1.1 CRAG centres (324, 240) / (324, 84); SHELF FACE normal -X (Blue), +X (Red);
                          48 x 48 footprint, body to 60 (top plate), spire 20 x 20
                     §2.2 shelf tops 24 / 42; 3 slots x 14.0 at -15.5 / 0 / +15.5; fences 1.5 x 2.0
                          at 0 / 15.5 / 31 / 46.5 from the left face edge; depth 14.0; roundover 0.25;
                          thickness 0.75; gusset floors (Z 38.0 under Shelf 2, Z 19.0 under Shelf 1,
                          Z 22.0 in the tag prisms Y 221.5-230.5 / 249.5-258.5 Blue); gussets within
                          the shelf plan footprint; Shelf 1 plan inside the 16-in DEPOT channel
                     §2.4 Summit Socket: rim 72, on the crag centreline, 8.0 standoff, 15 deg outward,
                          ID 6.50 +/- 0.125, 7.0 tube, 0.09 wall, closed bottom; floor centre 6.19
                          outboard at Z 65.24; inboard edge 2.94 outboard; lowest point Z 64.29; mast
                          from the top plate within 4.0 of the shelf-face edge, leaning outward to the
                          tube bottom; above Z 62 nothing outside the plan silhouette + 2.0; socket +
                          mast over the Shelf 2 centre slot (X 286.8-299.0 x Y 234.7-245.3 Blue);
                          5.0 overhead clearance in that slot, outer Shelf 2 slots open to the sky;
                          9.29 tube clearance over a Shelf 2 crate; robot reach 11.75
                     §2.7 mirror symmetry about the crag's own X-Z plane; Red = Blue rotated 180 deg
                     §3   depot lip outer face 16.75 off the face -> FRAME PERIMETER 19.75; shelf slot
                          reach 12.75; outer 2.0-in strip of the shelf-face leg open to the sky;
                          23.25 to the Shelf 1 underside, >= 19.0 where a gusset descends
                     §7   CRAG tag panels 9.0 at Z 17.5 (top 22.0), Shelf 1 underside 1.25 above them;
                          shelf-face tags at +/-14 from the face centreline
                     §9.1 CRATE 12.0 cube, 0.5 crown, rests on its bottom crown; 12.44 wide at the
                          fence tops -> 0.78 per side; 13.0 envelope; adjacent crates clear 2.5
                     §9.2 O2 CELL 14.0 long
  DESIGN-SPEC        §3   shelf / Summit Socket rows; "A seated 14.0-in O2 CELL therefore stands
                          7.0 in proud of the rim along the tube axis"
  MATERIALS-AND-COLORS §1.2/§2  shelf slab painted plywood `shelf` #8A6D3B; slot fence painted
                          hardwood `shelf`; gusset aluminium plate `crag-accent` #4A3B22 0.125;
                          Summit Socket mast steel 2 x 2 square tube `crag-accent`; socket tube
                          rolled aluminium `socket` #9DB8D6, 0.09 wall, bore >= 6.375

Socket depth: DESIGN-SPEC §3 gives "tube length 7.0 in along the axis, closed bottom" and "a
  seated 14.0-in O2 CELL therefore stands 7.0 in proud of the rim"; both hold only if the 7.0 runs
  from the rim plane to the floor the CELL seats on (FCP §2.3: the length "sets the 7.0-in
  protrusion"; §9.2: "7.0-in socket tube depth").  The 0.09 closed bottom lies beyond it, 7.09
  overall, and the §2.4 clearance figures are computed that way: floor (seat) centre 6.19 outboard at
  Z 65.24, inboard edge 2.94, lowest point Z 64.29, 9.29 over a Shelf 2 CRATE.  The outer bottom face
  centre is 6.165 outboard at Z 65.15.

Mast reading (§2.4 Support, (ref)): the mast is "rising from the tower top plate within 4.0 in of
its shelf-face edge and leaning outward to the tube's closed bottom", with nothing outside the
socket's plan silhouette + 2.0 above Z 62.  A straight 2 x 2 member cannot both start on the plate
and be inside that envelope by Z 62, so the reading tested is an arm on the plate (Z 60-62) plus a
post that leans outward to the closed bottom.
"""
import math

import numpy as np

import kernel_occ as K
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pnt

# ---------------------------------------------------------------------------------------
# Document values
# ---------------------------------------------------------------------------------------
SIDES = ("BLUE", "RED")
CRAG_C = {"BLUE": (324.0, 240.0), "RED": (324.0, 84.0)}      # §1.1
SHELF_NX = {"BLUE": -1.0, "RED": +1.0}                       # §1.1 SHELF FACE normal (world X)
HALF = 24.0                                                  # §2.1 48 x 48 footprint
TOP_PLATE = 60.0                                             # §2.1 tower body to 60
SPIRE_HALF = 10.0                                            # §2.1 20 x 20 spire
SHELF_TOP = (24.0, 42.0)                                     # §2.2 CRITICAL
SHELF_DEPTH = 14.0                                           # §2.2 CRITICAL
SHELF_T = 0.75                                               # §2.2 (ref); §3/§7 underside 23.25
ROUNDOVER = 0.25                                             # §2.2 (ref)
SLOT_W = 14.0                                                # §2.2 CRITICAL
SLOT_C = (-15.5, 0.0, 15.5)                                  # §2.2 CRITICAL
FENCE_W, FENCE_H = 1.5, 2.0                                  # §2.2 (ref)
FENCE_FROM_LEFT = (0.0, 15.5, 31.0, 46.5)                    # §2.2 (ref)
GUSSET_FLOOR = {1: 19.0, 2: 38.0}                            # §2.2
GUSSET_TAG_FLOOR = 22.0                                      # §2.2 (inside the tag prisms)
TAG_LAT, TAG_HALF_W = 14.0, 4.5                              # §2.2 / §7 prisms +/-4.5 about +/-14
TAG_TOP = 17.5 + 4.5                                         # §7 panel top 22.0
GUSSET_T = 0.125                                             # MATERIALS §2
SUM_Z, SUM_STANDOFF, SUM_TILT = 72.0, 8.0, 15.0              # §2.4 CRITICAL
SOCK_ID, SOCK_ID_TOL = 6.50, 0.125                           # §2.4 CRITICAL
SOCK_LEN, SOCK_WALL = 7.0, 0.09                              # DESIGN-SPEC §3 rim to seat, CRITICAL / (ref)
SOCK_OVERALL = SOCK_LEN + SOCK_WALL                          # rim plane to the outer bottom face
RO = SOCK_ID / 2 + SOCK_WALL                                 # 3.34 — the package's own figure
MAST_BASE_BAND = 4.0                                         # §2.4
MAST_CAP_Z, MAST_SIL_MARGIN = 62.0, 2.0                      # §2.4
MAST_S = 2.0                                                 # MATERIALS §2: 2 x 2 in tube
CRATE_S, CRATE_CROWN = 12.0, 0.5                             # §9.1
CRATE_ENV = CRATE_S + 2 * CRATE_CROWN                        # 13.0
CRATE_W_FENCE_TOP = 12.44                                    # §9.1 "about 12.44 in"
CRATE_FENCE_CLR = 0.78                                       # §9.1 per side
CRATE_PAIR_CLR = 2.5                                         # §9.1
CELL_L = 14.0                                                # §9.2
CELL_PROTRUDE = 7.0                                          # DESIGN-SPEC §3 / FCP §2.3
DEPOT_LIP_OUT = 16.75                                        # §3 lip outer face off the crag face
BUMPER_TO_FP = 3.0                                           # §3 FRAME PERIMETER 3.0 behind bumpers
REACH_LIMIT = 18.0                                           # §3 / R105
SLOT_REACH, SUM_REACH = 12.75, 11.75                         # §3 / §2.4
DEPOT_CH = 16.0                                              # §3 channel depth
DEPOT_FLOOR_TOP = 0.25                                       # §3
# §2.4 "X 286.8-299.0 x Y 234.7-245.3 on the Blue CRAG" -> crag-local (x = 324 - X, y = 240 - Y)
DOC_SUM_RECT_LOCAL = (324.0 - 299.0, -5.3, 324.0 - 286.8, 5.3)

COLORS = {"shelf": (0x8A, 0x6D, 0x3B), "crag-accent": (0x4A, 0x3B, 0x22), "socket": (0x9D, 0xB8, 0xD6)}

S15, C15 = math.sin(math.radians(SUM_TILT)), math.cos(math.radians(SUM_TILT))

VTOL = 1e-4        # in^3 — "zero" common volume (touching bodies)
TOL = 1e-3


# ---------------------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------------------
def _frame(side):
    cx, cy = CRAG_C[side]
    return K.Frame((cx, cy, 0.0), (SHELF_NX[side], 0.0, 0.0), (0.0, 0.0, 1.0))


def _box_local(F, p0, p1):
    lo = [min(a, b) for a, b in zip(p0, p1)]
    hi = [max(a, b) for a, b in zip(p0, p1)]
    s = BRepPrimAPI_MakeBox(gp_Pnt(*lo), gp_Pnt(*hi)).Shape()
    return BRepBuilderAPI_Transform(s, F.trsf(), True).Shape()


def _inside(solids, p):
    for s in solids:
        st = K.BRepClass3d_SolidClassifier(s, K._gp(p), 1e-9).State()
        if st in (K.TopAbs_IN, K.TopAbs_ON):
            return True
    return False


def _reach(solids, F, p0, d, hi=20.0):
    """Largest t with crag-local p0 + t*d still inside `solids` (bisection; p0 must be inside).
    Used on the virtual CRATE, whose Bezier faces defeat OCC's optimal bounding box (~0.02 in)."""
    p0, d = np.asarray(p0, float), np.asarray(d, float)
    lo = 0.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if _inside(solids, F.pt(p0 + mid * d)):
            lo = mid
        else:
            hi = mid
    return lo


_VREG = K.Registry()
_VN = [0]


def _crate(F, c_local):
    """Doc CRATE (12.0 cube, 0.5 crown, no fillets — the conservative envelope), square to the
    crag axes, centred at crag-local point c_local."""
    _VN[0] += 1
    key = K.Id(("V", "crate%d" % _VN[0]))
    Fc = K.Frame(F.pt(c_local), F.x, F.z)
    K.mkPillowBox(_VREG, key, Fc, CRATE_S / 2, CRATE_CROWN)
    return {"solids": _VREG.solids_for([key]), "name": "virtual crate", "id": tuple(key)}


def _common(a_solids, b_solids):
    tot = 0.0
    for x in a_solids:
        for y in b_solids:
            c = BRepAlgoAPI_Common(x, y)
            tot += K._volume(K._solids(c.Shape()))
    return tot


def _overlap(b1, b2, pad=0.1):
    return not (b1[3] < b2[0] - pad or b2[3] < b1[0] - pad or b1[4] < b2[1] - pad or
                b2[4] < b1[1] - pad or b1[5] < b2[2] - pad or b2[5] < b1[2] - pad)


def _bb_world(solids):
    b = K.Bnd_Box()
    for s in solids:
        K.BRepBndLib.AddOptimal_s(s, b, False, False)
    return K._box6(b)


def _faces(shape):
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        yield TopoDS.Face(ex.Current())
        ex.Next()


def _edge_points(shape, n=48):
    pts = []
    ex = TopExp_Explorer(shape, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge(ex.Current())
        try:
            c = BRepAdaptor_Curve(e)
            t0, t1 = c.FirstParameter(), c.LastParameter()
            for k in range(n + 1):
                p = c.Value(t0 + (t1 - t0) * k / n)
                pts.append((p.X(), p.Y(), p.Z()))
        except Exception:  # noqa: BLE001 — degenerate edge
            pass
        ex.Next()
    return pts


def _hull2d(pts):
    pts = sorted(set((round(p[0], 9), round(p[1], 9)) for p in pts))
    if len(pts) < 3:
        return pts

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def _dist_to_hull(p, hull):
    """2-D distance from p to a CCW convex polygon (0 inside)."""
    inside = True
    best = float("inf")
    n = len(hull)
    for i in range(n):
        a, b = np.array(hull[i]), np.array(hull[(i + 1) % n])
        q = np.array(p)
        ab = b - a
        if ab[0] * (q[1] - a[1]) - ab[1] * (q[0] - a[0]) < -1e-12:
            inside = False
        t = max(0.0, min(1.0, float(np.dot(q - a, ab) / max(np.dot(ab, ab), 1e-30))))
        best = min(best, float(np.linalg.norm(q - (a + t * ab))))
    return 0.0 if inside else best


def _loc_dir(F, d):
    d = np.asarray(d, float)
    return np.array([d @ F.x, d @ F.y, d @ F.z])


def _is_mult15(a, tol=0.02):
    r = a % 15.0
    return min(r, 15.0 - r) <= tol


def _plane_angles(F, solids):
    """(tilt from vertical, azimuth) in degrees of every planar face normal, crag-local."""
    out = []
    for s in solids:
        for fc in _faces(s):
            ad = BRepAdaptor_Surface(fc)
            if ad.GetType() != GeomAbs_Plane:
                continue
            d = ad.Plane().Axis().Direction()
            n = _loc_dir(F, (d.X(), d.Y(), d.Z()))
            tilt = math.degrees(math.acos(min(1.0, abs(n[2]))))
            az = math.degrees(math.atan2(n[1], n[0])) % 180.0 if math.hypot(n[0], n[1]) > 1e-9 else 0.0
            out.append((tilt, az, n))
    return out


# ---------------------------------------------------------------------------------------
def run(f):
    out = []

    def ck(label, ok, detail):
        out.append((label, bool(ok), detail))

    def near(label, got, want, tol, extra=""):
        ck(label, abs(got - want) <= tol, "got %.4f want %.4f +/- %g%s" % (got, want, tol, extra))

    # ---- field index for interference / clear-volume tests ---------------------------------
    allrecs = f.records()
    bbs = [(r, _bb_world(r["solids"])) for r in allrecs]

    def offenders(solids, exclude_ids=(), tol=VTOL):
        wb = _bb_world(solids)
        bad = []
        for r, b in bbs:
            if r["id"] in exclude_ids or not _overlap(wb, b):
                continue
            v = _common(solids, r["solids"])
            if v > tol:
                bad.append("%s (%.4f in^3)" % (r["name"], v))
        return bad

    def clear_region(label, F, p0, p1, exclude_ids=()):
        reg = K._solids(_box_local(F, p0, p1))
        bad = offenders(reg, exclude_ids)
        ck(label, not bad, "region local x %.3f..%.3f y %.3f..%.3f z %.3f..%.3f; intruders: %s"
           % (p0[0], p1[0], p0[1], p1[1], p0[2], p1[2], ", ".join(bad[:6]) or "none"))
        return bad

    blue_local = {}

    for A in SIDES:
        F = _frame(A)
        cn = A + " CRAG"

        def get(name, cn=cn):
            try:
                return f.find(cn + " " + name)
            except KeyError:
                return []

        tower = get("tower")
        slabs = {i: get("Shelf %d" % i) for i in (1, 2)}
        fences = {i: get("Shelf %d slot fence" % i) for i in (1, 2)}
        gussets = {i: get("Shelf %d gusset" % i) for i in (1, 2)}
        tube = get("Summit Socket")
        mast = get("Summit Socket mast")
        lip = get("BASE DEPOT lip")

        # ---- presence / counts / naming ----------------------------------------------------
        for i in (1, 2):
            ck("%s Shelf %d: one slab body named '%s Shelf %d'" % (A, i, cn, i), len(slabs[i]) == 1,
               "found %d" % len(slabs[i]))
            ck("%s Shelf %d: 4 slot fences" % (A, i), len(f.solids(fences[i])) == 4,
               "found %d solids" % len(f.solids(fences[i])))
            ck("%s Shelf %d: gussets present" % (A, i), len(gussets[i]) >= 1, "found %d" % len(gussets[i]))
        ck("%s Summit Socket: exactly one tube" % A, len(f.solids(tube)) == 1, "found %d" % len(f.solids(tube)))
        ck("%s Summit Socket mast present" % A, len(mast) >= 1, "found %d" % len(mast))
        if not (all(slabs[i] and len(f.solids(fences[i])) == 4 for i in (1, 2)) and tube and mast):
            continue

        # ---- appearance / material -----------------------------------------------------------
        def ck_look(label, rs, tok, mat_kw, dens):
            for r in rs:
                ok_c = tuple(int(round(c)) for c in r["rgb"]) == COLORS[tok] and abs(r["alpha"] - 1) < 1e-9
                ck("%s colour %s" % (label, tok), ok_c, "%s rgb %s alpha %s" % (r["name"], r["rgb"], r["alpha"]))
                m = r["mat"] or {}
                nm = (m.get("name") or "").lower()
                ok_m = all(k in nm for k in mat_kw) and dens[0] <= m.get("density", -1) <= dens[1]
                ck("%s material %s" % (label, "/".join(mat_kw)), ok_m,
                   "%s: %r density %s (want %s in %s)" % (r["name"], m.get("name"), m.get("density"), mat_kw, dens))
                break   # every body of a group is styled together; one record is representative
        for i in (1, 2):
            ck_look("%s Shelf %d slab" % (A, i), slabs[i], "shelf", ("plywood",), (400, 800))
            ck_look("%s Shelf %d slot fence" % (A, i), fences[i], "shelf", ("hardwood",), (550, 950))
            ck_look("%s Shelf %d gusset" % (A, i), gussets[i], "crag-accent", ("alumin",), (2600, 2850))
            for grp, nmg in ((fences[i], "fences"), (gussets[i], "gussets")):
                looks = {(tuple(r["rgb"]), r["alpha"], (r["mat"] or {}).get("name")) for r in grp}
                ck("%s Shelf %d all %s share one appearance/material" % (A, i, nmg), len(looks) == 1, "%s" % looks)
        ck_look("%s Summit Socket tube" % A, tube, "socket", ("alumin",), (2600, 2850))
        ck_look("%s Summit Socket mast" % A, mast, "crag-accent", ("steel",), (1, 8100))
        # mast is a 2 x 2 steel tube: mass per inch must match a real 2 x 2 steel tube, wall
        # 0.065-0.25 in (0.143-0.496 lb/in) whether it is modelled hollow or as an effective solid
        mb = f.bbox(mast, F)
        m_lb = f.mass_lb(mast)
        vol = f.volume(mast)
        lb_per_in = m_lb / (vol / (MAST_S * MAST_S))
        ck("%s Summit Socket mast mass per inch is a 2 x 2 steel tube's" % A, 0.143 <= lb_per_in <= 0.496,
           "%.4f lb/in (mass %.2f lb over %.2f in of 2 x 2 section)" % (lb_per_in, m_lb, vol / 4.0))

        # ---- shelf slabs ----------------------------------------------------------------------
        for i in (1, 2):
            zt = SHELF_TOP[i - 1]
            sb = f.bbox(slabs[i], F)
            near("%s Shelf %d top surface Z (CRITICAL)" % (A, i), sb[5], zt, TOL)
            near("%s Shelf %d underside Z (0.75 thick)" % (A, i), sb[2], zt - SHELF_T, 0.01)
            near("%s Shelf %d back edge on the SHELF FACE plane" % (A, i), sb[0], HALF, TOL)
            near("%s Shelf %d depth face-to-front-edge (CRITICAL 14.0)" % (A, i), sb[3] - HALF, SHELF_DEPTH, TOL)
            wb_ = f.bbox(slabs[i])
            fx = wb_[0] if SHELF_NX[A] < 0 else wb_[3]
            near("%s Shelf %d front edge at world X %g" % (A, i, CRAG_C[A][0] + SHELF_NX[A] * (HALF + SHELF_DEPTH)), fx,
                 CRAG_C[A][0] + SHELF_NX[A] * (HALF + SHELF_DEPTH), TOL)
            near("%s Shelf %d spans the face width, left end" % (A, i), sb[1], -HALF, TOL)
            near("%s Shelf %d spans the face width, right end" % (A, i), sb[4], HALF, TOL)
            # level, flat top over every slot at mid-depth and at the ends of the 12-in crate footprint
            flat = True
            det = []
            for c in SLOT_C:
                for xo in (0.5, 7.0, 12.5):
                    pin = (HALF + xo, c, zt - 0.005)
                    pout = (HALF + xo, c, zt + 0.005)
                    a, b = f.inside(slabs[i], pin, F), f.inside(slabs[i], pout, F)
                    if not a or b:
                        flat = False
                        det.append("(%g,%g)" % (xo, c))
            ck("%s Shelf %d top is a flat supporting surface under all 3 slots (12-in CRATE fully supported)" % (A, i),
               flat, "bad probes: %s" % (det or "none"))
            # front-edge roundover 0.25: sharp corner lies r(sqrt2-1) outside the rounded edge
            want = ROUNDOVER * (math.sqrt(2) - 1)
            for zc, nmz in ((zt, "top"), (zt - SHELF_T, "bottom")):
                d = f.dist_point(slabs[i], (HALF + SHELF_DEPTH, 0.0, zc), F)
                near("%s Shelf %d front %s edge roundover R0.25 (ref)" % (A, i, nmz), d, want, 0.01)
            # attached to the tower
            dt = f.dist(slabs[i], tower)
            ck("%s Shelf %d bears on the tower face" % (A, i), dt < TOL, "gap %.5f" % dt)
            # angle rule
            bad = [a for a in _plane_angles(F, f.solids(slabs[i])) if not (_is_mult15(a[0]) and _is_mult15(a[1]))]
            ck("%s Shelf %d every face at a multiple of 15 deg" % (A, i), not bad, "%d off-angle faces" % len(bad))

        # ---- slot fences and slots ----------------------------------------------------------------
        for i in (1, 2):
            zt = SHELF_TOP[i - 1]
            fb = sorted([f.bbox([{"solids": [s]}], F) for s in f.solids(fences[i])], key=lambda b: b[1])
            for j, b in enumerate(fb):
                lab = "%s Shelf %d fence %d" % (A, i, j + 1)
                near(lab + " left edge from the left face edge (ref)", b[1] - (-HALF), FENCE_FROM_LEFT[j], TOL)
                near(lab + " width 1.5 (ref)", b[4] - b[1], FENCE_W, TOL)
                near(lab + " sits on the shelf top", b[2], zt, TOL)
                near(lab + " height 2.0 above the shelf (ref)", b[5] - zt, FENCE_H, TOL)
                ck(lab + " within the shelf plan footprint", b[0] >= HALF - TOL and b[3] <= HALF + SHELF_DEPTH + TOL,
                   "x %.4f..%.4f (shelf %.1f..%.1f)" % (b[0], b[3], HALF, HALF + SHELF_DEPTH))
                # a fence must separate adjacent crates over the whole 12-in crate footprint at mid-depth
                ck(lab + " runs the crate footprint (0.5..12.5 outboard)", b[0] <= HALF + 0.5 + TOL and b[3] >= HALF + 12.5 - TOL,
                   "fence x %.4f..%.4f outboard" % (b[0] - HALF, b[3] - HALF))
            ws = []
            for j in range(3):
                lo, hi = fb[j][4], fb[j + 1][1]
                ws.append(hi - lo)
                near("%s Shelf %d slot %d width (CRITICAL 14.0)" % (A, i, j + 1), hi - lo, SLOT_W, TOL)
                near("%s Shelf %d slot %d centre from the face centreline (CRITICAL)" % (A, i, j + 1), (hi + lo) / 2, SLOT_C[j], TOL)
            near("%s Shelf %d 4 x 1.5 + 3 x 14.0 tiles the 48.0 face" % (A, i), fb[-1][4] - fb[0][1], 2 * HALF, TOL)
            for s in f.solids(fences[i]):
                d = f.dist([{"solids": [s]}], slabs[i])
                if d > TOL:
                    ck("%s Shelf %d fence bears on the slab" % (A, i), False, "gap %.4f" % d)
                    break
            else:
                ck("%s Shelf %d every fence bears on the slab" % (A, i), True, "all touching")

        # ---- gussets -------------------------------------------------------------------------------
        for i in (1, 2):
            zt = SHELF_TOP[i - 1]
            ys = []
            for k, s in enumerate(f.solids(gussets[i])):
                b = f.bbox([{"solids": [s]}], F)
                ys.append((b[1] + b[4]) / 2)
                lab = "%s Shelf %d gusset %d" % (A, i, k)
                ck(lab + " within the shelf plan footprint (§2.2)",
                   b[0] >= HALF - TOL and b[3] <= HALF + SHELF_DEPTH + TOL and b[1] >= -HALF - TOL and b[4] <= HALF + TOL,
                   "x %.3f..%.3f y %.3f..%.3f" % (b[0], b[3], b[1], b[4]))
                ck(lab + " entirely above its floor Z %.1f" % GUSSET_FLOOR[i], b[2] >= GUSSET_FLOOR[i] - 1e-6,
                   "lowest Z %.4f (margin %.4f)" % (b[2], b[2] - GUSSET_FLOOR[i]))
                ck(lab + " under its shelf (top <= shelf underside)", b[5] <= zt - SHELF_T + TOL, "top Z %.4f" % b[5])
                near(lab + " plate thickness 0.125", b[4] - b[1], GUSSET_T, TOL)
                dx, dz = b[3] - b[0], b[5] - b[2]
                v = K._volume([s])
                tri = abs(v - 0.5 * dx * dz * GUSSET_T) <= 0.01 * v
                rect = abs(v - dx * dz * GUSSET_T) <= 0.01 * v
                ang = math.degrees(math.atan2(dz, dx))
                ck(lab + " brace angle is 15/30/45 (angle rule)", rect or (tri and _is_mult15(ang, 0.05) and 0 < ang < 90),
                   "legs %.3f x %.3f -> %.2f deg, %s" % (dx, dz, ang, "triangle" if tri else ("rect" if rect else "other")))
                touch = f.dist([{"solids": [s]}], slabs[i]) < TOL and f.dist([{"solids": [s]}], tower) < TOL
                ck(lab + " ties the slab to the tower face", touch, "slab/tower contact %s" % touch)
                bad = [a for a in _plane_angles(F, [s]) if not (_is_mult15(a[0]) and _is_mult15(a[1]))]
                ck(lab + " every face at a multiple of 15 deg", not bad, "%d off-angle faces" % len(bad))
            ys.sort()
            sym = all(abs(a + b) < TOL for a, b in zip(ys, reversed(ys)))
            ck("%s Shelf %d gussets mirror-symmetric about the crag X-Z plane (§2.7)" % (A, i), sym, "y stations %s" % [round(y, 3) for y in ys])
            # nothing of either shelf's gussets in front of a tag below Z 22.0
            for sg in (-1, 1):
                prism = K._solids(_box_local(F, (HALF - 0.001, sg * TAG_LAT - TAG_HALF_W, -1.0),
                                             (HALF + SHELF_DEPTH + 0.001, sg * TAG_LAT + TAG_HALF_W, GUSSET_TAG_FLOOR)))
                v = _common(f.solids(gussets[i]), prism)
                ck("%s Shelf %d gussets clear of the tag prism y %+g below Z 22.0" % (A, i, sg * TAG_LAT), v <= VTOL,
                   "common volume %.5f in^3" % v)

        # tag prisms and the Shelf 1 underside against the actual tag panels
        tags = f.find(r"re:^AprilTag \d+ - %s CRAG SHELF FACE$" % A)
        tb = f.bbox(tags, F)
        near("%s shelf-face tag panels top at Z 22.0 (§7)" % A, tb[5], TAG_TOP, 0.01)
        near("%s Shelf 1 underside 1.25 above the tag panels (§7)" % A, f.bbox(slabs[1], F)[2] - tb[5], 1.25, 0.01)
        for t in tags:
            c = f.bbox([t], F)
            yc = (c[1] + c[4]) / 2
            ck("%s tag %s centre inside a gusset tag prism (+/-14 +/- 4.5)" % (A, t["name"].split(" - ")[0]),
               any(abs(yc - s * TAG_LAT) <= 1e-3 for s in (-1, 1)), "tag centre y %.3f" % yc)

        # ---- Summit Socket --------------------------------------------------------------------------
        ts = f.solids(tube)[0]
        st = []
        cyl = []
        planes = []
        for fc in _faces(ts):
            ad = BRepAdaptor_Surface(fc)
            if ad.GetType() == GeomAbs_Cylinder:
                c = ad.Cylinder()
                d, l = c.Axis().Direction(), c.Axis().Location()
                cyl.append((c.Radius(), np.array([d.X(), d.Y(), d.Z()]), np.array([l.X(), l.Y(), l.Z()])))
            elif ad.GetType() == GeomAbs_Plane:
                p = ad.Plane()
                d, l = p.Axis().Direction(), p.Location()
                planes.append((np.array([d.X(), d.Y(), d.Z()]), np.array([l.X(), l.Y(), l.Z()])))
        radii = sorted({round(c[0], 6) for c in cyl})
        ck("%s Summit Socket is an analytic tube: inner + outer cylinder" % A, len(radii) == 2, "radii %s" % radii)
        if len(radii) == 2:
            ri, ro = radii
            axis_w = cyl[0][1] / np.linalg.norm(cyl[0][1])
            a_loc = _loc_dir(F, axis_w)
            if a_loc[2] < 0:
                a_loc = -a_loc
                axis_w = -axis_w
            p_axis_w = cyl[0][2]
            coax = all(np.linalg.norm(np.cross(c[1] / np.linalg.norm(c[1]), axis_w)) < 1e-6 and
                       np.linalg.norm(np.cross(c[2] - p_axis_w, axis_w)) < 1e-6 for c in cyl)
            ck("%s Summit Socket bore and outside coaxial" % A, coax, "cylinders %d" % len(cyl))
            tilt = math.degrees(math.acos(min(1.0, a_loc[2])))
            near("%s Summit Socket axis tilt from vertical (CRITICAL 15)" % A, tilt, SUM_TILT, 0.01)
            ck("%s Summit Socket tilts outward toward the owning alliance (mouth leans +x local)" % A,
               a_loc[0] > 0 and abs(a_loc[1]) < 1e-6, "axis local %s" % np.round(a_loc, 5))
            # axial stations of the planes perpendicular to the axis
            st = sorted(float((pl[1] - p_axis_w) @ axis_w) for pl in planes
                        if np.linalg.norm(np.cross(pl[0], axis_w)) < 1e-6)
            ck("%s Summit Socket has rim, inner floor and outer bottom planes" % A, len(st) == 3, "stations %s" % np.round(st, 4))
            if len(st) == 3:
                s_bot, s_floor, s_rim = st
                rim_w = p_axis_w + axis_w * s_rim
                rim_l = F.to_local(rim_w)
                near("%s Summit Socket rim centre height (CRITICAL 72)" % A, rim_l[2], SUM_Z, TOL)
                near("%s Summit Socket rim centre lateral on the crag centreline (CRITICAL 0)" % A, rim_l[1], 0.0, TOL)
                near("%s Summit Socket rim standoff from the SHELF FACE (CRITICAL 8.0)" % A, rim_l[0] - HALF, SUM_STANDOFF, TOL)
                want_w = np.array([CRAG_C[A][0] + SHELF_NX[A] * (HALF + SUM_STANDOFF), CRAG_C[A][1], SUM_Z])
                ck("%s Summit Socket rim centre at world %s" % (A, tuple(float(v) for v in want_w)),
                   np.linalg.norm(rim_w - want_w) <= TOL, "got %s" % np.round(rim_w, 4))
                near("%s Summit Socket bore ID (CRITICAL 6.50 +/- 0.125)" % A, 2 * ri, SOCK_ID, SOCK_ID_TOL)
                near("%s Summit Socket bore ID nominal" % A, 2 * ri, SOCK_ID, 0.005)
                near("%s Summit Socket wall 0.09 (ref)" % A, ro - ri, SOCK_WALL, 0.005)
                near("%s Summit Socket bore depth along the axis, rim to the floor a CELL seats on (CRITICAL 7.0)" % A,
                     s_rim - s_floor, SOCK_LEN, TOL, " — DESIGN-SPEC §3's 7.0 length and 7.0 protrusion both hold only with "
                     "the 7.0 measured to the seat")
                near("%s Summit Socket overall length rim to outer bottom = 7.0 + 0.09 closed bottom" % A, s_rim - s_bot,
                     SOCK_OVERALL, TOL)
                ck("%s Summit Socket closed bottom" % A,
                   s_floor - s_bot > 0.01 and f.inside(tube, rim_w - axis_w * ((s_rim - s_bot) - 0.5 * (s_floor - s_bot))),
                   "bottom plate %.4f thick" % (s_floor - s_bot))
                bore = s_rim - s_floor
                prot = CELL_L - bore
                near("%s seated 14.0 O2 CELL protrudes 7.0 proud of the rim (DESIGN-SPEC §3)" % A, prot, CELL_PROTRUDE, TOL,
                     " — bore depth rim->floor %.4f (a 7.0 taken to the outer bottom would leave the CELL 7.09 proud)"
                     % bore)
                bot_l = F.to_local(p_axis_w + axis_w * s_bot)
                flo_l = F.to_local(p_axis_w + axis_w * s_floor)
                near("%s Summit Socket floor (seat) centre outboard of the face (6.19)" % A, flo_l[0] - HALF,
                     SUM_STANDOFF - SOCK_LEN * S15, 0.01)
                near("%s Summit Socket floor (seat) centre Z (65.24)" % A, flo_l[2], SUM_Z - SOCK_LEN * C15, 0.01)
                near("%s Summit Socket outer bottom centre outboard of the face (8.0 - 7.09 sin15)" % A, bot_l[0] - HALF,
                     SUM_STANDOFF - SOCK_OVERALL * S15, TOL)
                near("%s Summit Socket outer bottom centre Z (72 - 7.09 cos15)" % A, bot_l[2], SUM_Z - SOCK_OVERALL * C15, TOL)
                # ID is the same the whole bore depth (bore reached at three depths)
                for dd in (0.5, 2.0, 3.5):
                    d = f.dist_point(tube, rim_w - axis_w * dd)
                    near("%s Summit Socket bore radius %.1f below the rim" % (A, dd), d, SOCK_ID / 2, 0.0625)
        tb_l = f.bbox(tube, F)
        near("%s Summit Socket inboard edge outboard of the face (free air)" % A, tb_l[0] - HALF,
             SUM_STANDOFF - SOCK_OVERALL * S15 - RO * C15, TOL, " (§2.4: 2.94)")
        near("%s Summit Socket lowest point Z" % A, tb_l[2], SUM_Z - SOCK_OVERALL * C15 - RO * S15, TOL,
             " (§2.4: Z 64.29)")
        bad = offenders(f.solids(tube), exclude_ids={r["id"] for r in tube + mast})
        ck("%s Summit Socket interferes with nothing" % A, not bad, ", ".join(bad) or "none")

        # ---- mast ----------------------------------------------------------------------------------
        near("%s mast base on the tower top plate (Z 60)" % A, mb[2], TOP_PLATE, TOL)
        ck("%s mast footprint on the top plate within 4.0 of the shelf-face edge" % A,
           HALF - MAST_BASE_BAND - TOL <= mb[0] < HALF,
           "mast inboard end at x %.4f (edge %.1f, band to %.1f)" % (mb[0], HALF, HALF - MAST_BASE_BAND))
        dmt = f.dist(mast, tower)
        ck("%s mast bears on the tower" % A, dmt < TOL, "gap %.5f" % dmt)
        ck("%s mast does not hang off the SHELF FACE below the top plate" % A, mb[2] >= TOP_PLATE - TOL, "mast zmin %.4f" % mb[2])
        near("%s mast lateral section 2.0 on the centreline (2 x 2 tube)" % A, mb[4] - mb[1], MAST_S, 0.01)
        near("%s mast mirror-symmetric about the crag X-Z plane" % A, mb[1] + mb[4], 0.0, TOL)
        if len(radii) == 2 and len(st) == 3:
            dmb = f.dist_point(mast, p_axis_w + axis_w * s_bot)
            ck("%s mast reaches the tube's closed bottom (bottom-face centre)" % A, dmb < 0.01, "distance %.4f" % dmb)
        if len(radii) == 2 and len(st) == 3:
            hmax = max(float((np.asarray(p) - (p_axis_w + axis_w * s_bot)) @ axis_w)
                       for r in mast for sld in r["solids"] for p in _edge_points(sld, 24))
            ck("%s mast stays below the tube's closed bottom (never climbs the tube or breaks the rim plane)" % A,
               hmax <= TOL, "highest mast point %.4f along the axis above the bottom plane" % hmax)
        dmtube = f.dist(mast, tube)
        vmt = f.common_volume(mast, tube)
        ck("%s mast meets the tube without entering it" % A, dmtube < TOL and vmt <= VTOL, "gap %.5f, common %.5f in^3" % (dmtube, vmt))
        bad = offenders(f.solids(mast), exclude_ids={r["id"] for r in tube + mast + tower})
        vtow = f.common_volume(mast, tower)
        ck("%s mast interferes with nothing" % A, not bad and vtow <= VTOL, (", ".join(bad) or "none") + "; tower common %.5f" % vtow)
        # "leaning outward": at least one mast member inclined outward (a face whose normal is
        # tilted from both vertical and horizontal, other than the 15-deg tube-seat face)
        angs = _plane_angles(F, f.solids(mast))
        seat_tilt = SUM_TILT
        inclined = [a for a in angs if 0.5 < a[0] < 89.5 and abs(a[0] - seat_tilt) > 0.5]
        seat = [a for a in angs if abs(a[0] - seat_tilt) <= 0.5]
        ck("%s mast leans outward from the top plate to the tube bottom (§2.4 Support, (ref))" % A, bool(inclined),
           "planar-face tilts from vertical: %s; %d tube-seat face(s); inclined member faces %d "
           "(arm on the plate x %.2f..%.2f, Z %.1f-%.1f)"
           % (sorted({round(a[0], 2) for a in angs}), len(seat), len(inclined), mb[0], mb[3], mb[2], mb[2] + MAST_S))
        # the leaning member tilts OUTWARD: its inclined faces' normals point down-outboard or up-inboard
        lean_out = all(a[2][0] * a[2][2] < 0 for a in inclined)
        ck("%s mast leans outward (toward the owning alliance), never back over the tower" % A, bool(inclined) and lean_out,
           "inclined face normals (local) %s" % [np.round(a[2], 3).tolist() for a in inclined])
        bad = [a for a in angs if not (_is_mult15(a[0]) and _is_mult15(a[1]))]
        ck("%s mast every face at a multiple of 15 deg" % A, not bad, "%d off-angle faces" % len(bad))
        # above Z 62: nothing outside the socket's plan silhouette + 2.0
        hull = _hull2d([F.to_local(p)[:2] for p in _edge_points(ts, 96)])
        worst = 0.0
        worst_p = None
        for r in mast + tube:
            for s in r["solids"]:
                cut = BRepAlgoAPI_Common(s, _box_local(F, (-60, -60, MAST_CAP_Z), (60, 60, 200))).Shape()
                for p in _edge_points(cut, 24):
                    q = F.to_local(p)
                    d = _dist_to_hull(q[:2], hull)
                    if d > worst:
                        worst, worst_p = d, q
        ck("%s above Z 62 nothing lies outside the socket plan silhouette + 2.0" % A, worst <= MAST_SIL_MARGIN + TOL,
           "worst %.4f in outside the silhouette at local %s" % (worst, None if worst_p is None else np.round(worst_p, 3)))
        # the doc's published plan envelope X 286.8-299.0 x Y 234.7-245.3 (Blue) above Z 62
        up = []
        for r in mast + tube:
            for s in r["solids"]:
                cut = K._solids(BRepAlgoAPI_Common(s, _box_local(F, (-60, -60, MAST_CAP_Z + 1e-4), (60, 60, 200))).Shape())
                up += cut
        ub = f.bbox([{"solids": up}], F)
        rx0, ry0, rx1, ry1 = DOC_SUM_RECT_LOCAL
        ck("%s socket + mast above Z 62 inside the published plan envelope (Blue X 286.8-299.0 x Y 234.7-245.3)" % A,
           ub[0] >= rx0 - 0.05 and ub[3] <= rx1 + 0.05 and ub[1] >= ry0 - 0.05 and ub[4] <= ry1 + 0.05,
           "local x %.3f..%.3f y %.3f..%.3f vs x %.2f..%.2f y %.2f..%.2f" % (ub[0], ub[3], ub[1], ub[4], rx0, rx1, ry0, ry1))
        # everything of socket + mast outboard of the face stands over the Shelf 2 centre slot
        ob = []
        for r in mast + tube:
            for s in r["solids"]:
                ob += K._solids(BRepAlgoAPI_Common(s, _box_local(F, (HALF + 1e-4, -60, 0), (200, 60, 200))).Shape())
        obb = f.bbox([{"solids": ob}], F)
        ck("%s socket + mast outboard of the face lie over the Shelf 2 centre slot only" % A,
           obb[1] >= SLOT_C[1] - SLOT_W / 2 - TOL and obb[4] <= SLOT_C[1] + SLOT_W / 2 + TOL and obb[3] <= HALF + SHELF_DEPTH + TOL,
           "outboard part x %.3f..%.3f y %.3f..%.3f (centre slot y +/-7, depth to %.1f)" % (obb[0], obb[3], obb[1], obb[4], HALF + SHELF_DEPTH))

        # ---- virtual CRATES in every slot (§9.1) ---------------------------------------------------
        c_off = CRATE_S / 2 + CRATE_CROWN      # cube centre above the shelf when resting on its crown
        crates = {}
        for i in (1, 2):
            zt = SHELF_TOP[i - 1]
            for j, c in enumerate(SLOT_C):
                crates[(i, j)] = _crate(F, (HALF + SHELF_DEPTH / 2, c, zt + c_off))
        # the virtual crate itself reproduces the doc's profile (sanity of the probe, once)
        cx0 = HALF + SHELF_DEPTH / 2
        if A == "BLUE":
            cr = crates[(1, 1)]["solids"]
            zt = SHELF_TOP[0]
            c0 = (cx0, SLOT_C[1], zt + c_off)
            h_up = _reach(cr, F, c0, (0, 0, 1))
            h_dn = _reach(cr, F, c0, (0, 0, -1))
            near("virtual CRATE crowned height (doc 13.0)", h_up + h_dn, CRATE_ENV, 1e-4)
            near("virtual CRATE rests on its bottom crown on the shelf (cube bottom 0.5 up)", c0[2] - h_dn, zt, 1e-4)
            w = _reach(cr, F, c0, (0, 1, 0)) + _reach(cr, F, c0, (0, -1, 0))
            near("virtual CRATE crowned width (doc 13.0)", w, CRATE_ENV, 1e-4)
            pf = (cx0, SLOT_C[1], zt + FENCE_H)
            wf = _reach(cr, F, pf, (0, 1, 0)) + _reach(cr, F, pf, (0, -1, 0))
            near("virtual CRATE width at the fence tops (doc 12.44)", wf, CRATE_W_FENCE_TOP, 0.005)
        for i in (1, 2):
            zt = SHELF_TOP[i - 1]
            fb = sorted([f.bbox([{"solids": [s]}], F) for s in f.solids(fences[i])], key=lambda b: b[1])
            for j, c in enumerate(SLOT_C):
                cr = crates[(i, j)]
                lab = "%s Shelf %d slot %d CRATE" % (A, i, j + 1)
                pf = (cx0, c, zt + FENCE_H)
                gl = (c - _reach(cr["solids"], F, pf, (0, -1, 0))) - fb[j][4]
                gr = fb[j + 1][1] - (c + _reach(cr["solids"], F, pf, (0, 1, 0)))
                near(lab + " lateral clearance to the left fence at its top (0.78)", gl, CRATE_FENCE_CLR, 0.01)
                near(lab + " lateral clearance to the right fence at its top (0.78)", gr, CRATE_FENCE_CLR, 0.01)
                dfen = f.dist([cr], fences[i])
                ck(lab + " clears the fences in 3-D", dfen >= 0.75, "min distance %.4f" % dfen)
                ds = f.dist([cr], slabs[i])
                ck(lab + " rests on the shelf top", ds < TOL, "gap %.5f" % ds)
                bad = offenders(cr["solids"], exclude_ids=set())
                ck(lab + " interferes with nothing on the field", not bad, ", ".join(bad) or "none")
            for j in range(2):
                d = f.dist([crates[(i, j)]], [crates[(i, j + 1)]])
                near("%s Shelf %d CRATES in slots %d/%d clear each other (2.5)" % (A, i, j + 1, j + 2), d, CRATE_PAIR_CLR, 0.01)
        # Shelf 1 crates under the Shelf 2 gussets: >= 1.0 (crown top 37.0 vs floor 38.0)
        top1 = max(SHELF_TOP[0] + c_off + _reach(crates[(1, j)]["solids"], F, (cx0, SLOT_C[j], SHELF_TOP[0] + c_off), (0, 0, 1))
                   for j in range(3))
        near("%s CRATE on Shelf 1 tops out at Z 37.0" % A, top1, SHELF_TOP[0] + CRATE_ENV, 0.005)
        d = min(f.dist([crates[(1, j)]], gussets[2]) for j in range(3))
        ck("%s Shelf 1 CRATES clear the Shelf 2 gussets by >= 1.0" % A, d >= 1.0 - TOL, "min distance %.4f" % d)
        d1 = min(f.dist([crates[(1, j)]], slabs[2]) for j in range(3))
        near("%s Shelf 1 CRATE overhead clearance to the Shelf 2 underside (41.25 - 37.0)" % A, d1, SHELF_TOP[1] - SHELF_T - (SHELF_TOP[0] + CRATE_ENV), 0.01)
        b1 = offenders(K._solids(_box_local(F, (HALF + 0.001, SLOT_C[0] - 6.999, SHELF_TOP[0] + 0.001), (HALF + SHELF_DEPTH - 0.001, SLOT_C[0] + 6.999, 400.0))))
        ck("%s Shelf 1 slots are overhung by Shelf 2 (front-load only too; contradicts FCP §2.4 'only slot on the CRAG')" % A,
           bool(b1), "overhead: %s" % (", ".join(sorted({x.split(" (")[0] for x in b1})) or "nothing"))
        # worst-case placement inside the slot (+/-0.75 lateral, face-to-front fore/aft)
        worst_g, worst_m, worst_t = 1e9, 1e9, 1e9
        hits = []
        for xo in (CRATE_S / 2 + CRATE_CROWN, SHELF_DEPTH - CRATE_S / 2):
            for dy in (-0.75, 0.0, 0.75):
                for j, c in enumerate(SLOT_C):
                    c1 = _crate(F, (HALF + xo, c + dy, SHELF_TOP[0] + c_off))
                    worst_g = min(worst_g, f.dist([c1], gussets[2]))
                    c2 = _crate(F, (HALF + xo, c + dy, SHELF_TOP[1] + c_off))
                    worst_t = min(worst_t, f.dist([c2], tube))
                    if j == 1:
                        worst_m = min(worst_m, f.dist([c2], mast))
                    for cc in (c1, c2):
                        b = offenders(cc["solids"])
                        if b:
                            hits.append("x%+.2f dy%+.2f slot%d: %s" % (xo, dy, j + 1, b[0]))
        ck("%s CRATES anywhere in a slot (+/-0.75, face to front) interfere with nothing" % A, not hits, "; ".join(hits[:4]) or "none")
        ck("%s Shelf 1 CRATE anywhere in its slot clears the Shelf 2 gussets by >= 1.0" % A, worst_g >= 1.0 - TOL, "min %.4f" % worst_g)
        ck("%s Shelf 2 centre-slot CRATE has >= 5.0 overhead clearance to the mast" % A, worst_m >= 5.0 - TOL, "min %.4f" % worst_m)
        near("%s Shelf 2 centre-slot overhead clearance is the published 5.0" % A, worst_m, 5.0, 0.02)
        near("%s Shelf 2 CRATE clearance under the Summit Socket tube" % A, tb_l[2] - (SHELF_TOP[1] + CRATE_ENV),
             SUM_Z - SOCK_OVERALL * C15 - RO * S15 - (SHELF_TOP[1] + CRATE_ENV), TOL,
             " (§2.4: 9.29)")
        ck("%s Shelf 2 CRATE anywhere in a slot clears the tube by >= 9.3" % A, worst_t >= 9.3, "min %.4f" % worst_t)

        # ---- clear volumes ---------------------------------------------------------------------------
        e = 0.001
        for j, c in enumerate(SLOT_C):
            clear_region("%s Shelf 1 slot %d clear from the shelf to Z 38.0" % (A, j + 1), F,
                         (HALF + e, c - SLOT_W / 2 + e, SHELF_TOP[0] + e), (HALF + SHELF_DEPTH - e, c + SLOT_W / 2 - e, 38.0 - e))
        clear_region("%s under Shelf 2, full width, fence tops to Z 38.0 clear" % A, F,
                     (HALF + e, -HALF + e, SHELF_TOP[0] + FENCE_H + e), (HALF + SHELF_DEPTH - e, HALF - e, 38.0 - e))
        for j in (0, 2):
            c = SLOT_C[j]
            clear_region("%s Shelf 2 outer slot %d open to the sky" % (A, j + 1), F,
                         (HALF + e, c - SLOT_W / 2 + e, SHELF_TOP[1] + e), (HALF + SHELF_DEPTH - e, c + SLOT_W / 2 - e, 400.0))
        c = SLOT_C[1]
        clear_region("%s Shelf 2 centre slot clear to Z 60 (5.0 over a 55.0 CRATE)" % A, F,
                     (HALF + e, c - SLOT_W / 2 + e, SHELF_TOP[1] + e), (HALF + SHELF_DEPTH - e, c + SLOT_W / 2 - e, TOP_PLATE - e))
        b = offenders(K._solids(_box_local(F, (HALF + e, c - SLOT_W / 2 + e, SHELF_TOP[1] + e),
                                           (HALF + SHELF_DEPTH - e, c + SLOT_W / 2 - e, 400.0))))
        ck("%s Shelf 2 centre slot is overhung (front-load only, as published)" % A, bool(b), "overhead: %s" % (", ".join(b) or "nothing"))
        clear_region("%s under Shelf 1 (DEPOT leg) clear from the tray floor to Z 19.0" % A, F,
                     (HALF + e, -HALF + e, DEPOT_FLOOR_TOP + e), (HALF + SHELF_DEPTH - e, HALF - e, 19.0 - e))
        for sg in (-1, 1):
            clear_region("%s tag prism y %+g clear from the tray floor to Z 22.0" % (A, sg * TAG_LAT), F,
                         (HALF + e, sg * TAG_LAT - TAG_HALF_W, DEPOT_FLOOR_TOP + e), (HALF + SHELF_DEPTH - e, sg * TAG_LAT + TAG_HALF_W, GUSSET_TAG_FLOOR - e))
        clear_region("%s outer 2.0-in strip of the DEPOT leg open to the sky (§3)" % A, F,
                     (HALF + SHELF_DEPTH + e, -HALF + e, DEPOT_FLOOR_TOP + e), (HALF + DEPOT_CH - e, HALF - e, 400.0))

        # ---- DEPOT relation and robot reach ------------------------------------------------------------
        if lip:
            # the shelf-face leg of the lip: its inner wall is the channel edge, outer face the bumper stop
            lb_leg = f.bbox([{"solids": K._solids(BRepAlgoAPI_Common(s, _box_local(F, (HALF + 1, -HALF, -1), (HALF + 30, HALF, 10))).Shape())}
                             for r in lip for s in r["solids"]], F)
            near("%s Shelf 1 plan footprint inside the DEPOT channel (2.0 to the lip)" % A, lb_leg[0] - (HALF + SHELF_DEPTH), DEPOT_CH - SHELF_DEPTH, 0.01)
            fp = lb_leg[3] - HALF + BUMPER_TO_FP
            near("%s FRAME PERIMETER at the DEPOT lip (19.75)" % A, fp, DEPOT_LIP_OUT + BUMPER_TO_FP, 0.01)
            near("%s shelf-slot reach from the lip (12.75, <= 18)" % A, fp - (f.bbox(slabs[1], F)[3] + f.bbox(slabs[1], F)[0]) / 2 + HALF, SLOT_REACH, 0.01)
            if len(radii) == 2 and len(st) == 3:
                near("%s Summit rim reach from the lip (11.75, <= 18)" % A, fp - (rim_l[0] - HALF), SUM_REACH, 0.01)

        # ---- whole-element interference with the rest of the field ---------------------------------------
        allowed_touch = {r["id"] for r in tower}
        hits = []
        for r in [x for i in (1, 2) for x in slabs[i] + fences[i] + gussets[i]]:
            b = offenders(r["solids"], exclude_ids={r["id"]} | allowed_touch)
            v = f.common_volume([r], tower)
            if b or v > VTOL:
                hits.append("%s: %s%s" % (r["name"], ", ".join(b), " tower %.4f" % v if v > VTOL else ""))
        ck("%s shelves, fences and gussets interfere with nothing (touching only)" % A, not hits, "; ".join(hits[:4]) or "none")

        # ---- symmetry / Red = Blue rotated ---------------------------------------------------------------
        groups = {"slab1": slabs[1], "slab2": slabs[2], "fence1": fences[1], "fence2": fences[2],
                  "gusset1": gussets[1], "gusset2": gussets[2], "tube": tube, "mast": mast}
        loc = {k: f.bbox(v, F) for k, v in groups.items()}
        for k in ("slab1", "slab2", "fence1", "fence2", "gusset1", "gusset2", "tube", "mast"):
            near("%s %s mirror-symmetric about the crag X-Z plane (§2.7)" % (A, k), loc[k][1] + loc[k][4], 0.0, TOL)
        if A == "BLUE":
            blue_local = loc
        else:
            worst = max(abs(a - b) for k in loc for a, b in zip(loc[k], blue_local.get(k, loc[k])))
            ck("RED shelf face = BLUE rotated 180 deg about (324, 162) (local boxes match)", bool(blue_local) and worst < 1e-6,
               "max local-box difference %.2e" % worst)
            vb = sum(f.volume(f.find("BLUE CRAG " + n)) for n in ("Shelf 1", "Shelf 2", "Shelf 1 slot fence", "Shelf 2 slot fence",
                                                                 "Shelf 1 gusset", "Shelf 2 gusset", "Summit Socket", "Summit Socket mast"))
            vr = sum(f.volume(f.find("RED CRAG " + n)) for n in ("Shelf 1", "Shelf 2", "Shelf 1 slot fence", "Shelf 2 slot fence",
                                                                "Shelf 1 gusset", "Shelf 2 gusset", "Summit Socket", "Summit Socket mast"))
            near("RED shelf-face volume = BLUE", vr, vb, 1e-4)

    return out
