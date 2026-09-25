# -*- coding: utf-8 -*-
"""
SUPPLIES — CACHE CRATE, O2 CELL, ROPE COIL: geometry, mass, colour, staging, and the
robot-driving fits of each piece against the field (shelf slots, DEPOT, sockets, pegs).

Every expected value below comes from the package documents, never from src/:

  FIELD-CAD-PACKAGE
    §9.1  CACHE CRATE: 12.0 cube (CRITICAL), 0.5 face crown (ref), 1.0 fillets on all twelve
          edges (ref), ~2.0 lb, 13.0 crowned envelope; rests on its bottom crown, so the cube's
          bottom plane is 0.5 above the shelf and each side face reaches its full 0.5 bulge
          6.5 above it; ~12.44 wide at the top of the 2.0-in fences = 0.78 per side in the 14.0
          slot; 13.0 crown 4.5 above the fences; adjacent slots (15.5 pitch) clear by 2.5.
    §9.2  O2 CELL: 5.0 dia x 14.0 (CRITICAL); 1.5 domes (ref) struck through pole and equator,
          28.1-degree tangent break; R1.0 cap/body fillets (ref); full 5.0 diameter over 10.44
          (11.0 between the arc endpoints); ~1.5 lb; vs socket ID 6.50 +/- 0.125 (0.75 radial
          per side) and 7.0 tube depth (7.0 protrudes).
    §9.3  ROPE COIL: 10.0 OD, 2.5 tube, 5.0 ID (CRITICAL), one revolve of a 2.5-dia circle with
          its centre at r = 3.75; ~1.0 lb; 5.0 ID vs the 1.5 peg.
    §2.2  shelves 24 / 42, slots 14.0 at -15.5 / 0 / +15.5, depth 14.0, fences 1.5 x 2.0;
          gusset floors (Shelf 2: above Z 38.0, 1.0 over a crowned crate on Shelf 1 at 37.0;
          Shelf 1: above Z 19.0).
    §2.3  socket rims 30 / 54 at +/-14 (Low on the shelf-face side), 8.0 standoff, 30 deg outward
    §2.4  Summit Socket rim 72, on the centreline, 8.0 off the SHELF FACE, 15 deg outward; tube
          lowest point Z 64.29 (9.29 over a crowned crate on Shelf 2 at 55.0); mast from Z 60 =>
          5.0 in of overhead clearance; the socket and mast stand over Shelf 2's centre slot (no
          vertical drop there); the outer Shelf 2 slots stay open to the sky.
    §2.5  pegs: Low/Mid roots at +/-14, Z 30 / 54 on the PEG FACE; High roots at +/-7, Z 78 on
          the spire (20 x 20); OD 1.5; 45 deg up; 10.0 exposed.  Coil rest pose: max tilt ~47.9
          deg from perpendicular-to-peg (2.5 tan + 1.5 / cos <= 5.0); vertical hang 45 deg => 2.9
          deg margin; settles near-vertical wedged, centre ~1 in above the peg root, inner face
          ~1.25 outboard.
    §3    BASE DEPOT: floor top Z 0.25; channel 16.0; leg / corner squares / arms (Blue leg
          X 284-300 Y 216-264, squares Y 200-216 and 264-280, arms X 300-316); corner squares
          open to the sky; arms overhung by the Low Socket (a crate cannot be dropped in).
    §6    CENTER CACHE 3x3 at X 300/324/348, Y 138/162/186; chart (a) Latin square; cells axis +X,
          coils flat, crates square; chart (b) Blue 108 crates / 162 cells / 216 coils, Red the
          180-deg rotation (X 504: 108 coils / 162 cells / 216 crates); chart (c) 7 of each type per
          alliance at the OUTFITTERS; 21 per type, 63 total; extent Y 131.5-192.5, X 293-355,
          3.5 in inside the 68-in corridor between the aprons (Y 128-196).
    §7    CRAG tag target bottom 17.5 - 8.125/2 = 13.4375; crowned CRATE in the DEPOT apexes at
          13.25 (0.19 below); O2 CELL on end in the DEPOT is the one SUPPLY in the band.
    §0/§1.1 CRAG centres (324, 240) / (324, 84); SHELF FACE normal -X Blue / +X Red; 48 x 48.
  MATERIALS-AND-COLORS §1.3 crate-violet #7B3FA0 (62 deg from alliance blue #1D63C8, 83 deg
          from alliance red #CC3333 in hue), cell-body #F2F2F0, cell-cap #2E8B57, cell-fillet
          #4D4D4D on the R1.0 blend band, coil-amber #D9A441; §2 materials (ripstop nylon over
          PU foam / rigid core + EVA sleeve + molded caps / molded rubber-foam); zone tape
          0.01 in thick.
  DESIGN-SPEC §2 dimensions, weights, colours, counts; staging 12 ft from the alliance wall.
  Manual §3.6 / §3.6.1 counts and staging; VISION-GUIDE §1.3 upright CELL: top Z 14.25, full
          diameter to Z 12.47 on the tray floor.

Socket depth: DESIGN-SPEC §3 "tube length 7.0 in along the axis, closed bottom ... A seated 14.0-in
  O2 CELL therefore stands 7.0 in proud of the rim" holds only with the 7.0 measured from the rim
  plane to the floor the CELL seats on (§9.2 says "7.0-in socket tube depth"), so the 0.09 closed
  bottom lies beyond it.  §2.4 computes the Summit Socket tube's lowest point (Z 64.29, 9.29 over a
  crowned crate on Shelf 2) the same way.

Construction reading (naming only): pegs and side sockets are named "... (guardrail side)" /
"... (centre side)"; the lookups below take both.
"""
import math
import os
import re

import numpy as np

import kernel_occ as K
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Dir, gp_Lin, gp_Pnt, gp_Trsf

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(HERE), "src")

# ---------------------------------------------------------------------------------------
# Document values
# ---------------------------------------------------------------------------------------
FIELD_L, FIELD_W = 648.0, 324.0
TAPE_T = 0.01                                    # MATERIALS §2 gaffer tape 0.01 in

# §9.1 CACHE CRATE
CRATE_EDGE, CRATE_CROWN, CRATE_ENV, CRATE_FILLET, CRATE_LB = 12.0, 0.5, 13.0, 1.0, 2.0
FENCE_H, SLOT_W = 2.0, 14.0                      # §2.2
CRATE_W_FENCE, CRATE_SIDE_CLR = 12.44, 0.78      # §9.1 / M40
# §9.2 O2 CELL
CELL_D, CELL_L, CELL_DOME, CELL_FR, CELL_LB = 5.0, 14.0, 1.5, 1.0, 1.5
CELL_BREAK, CELL_FULL, CELL_ARC = 28.1, 10.44, 11.0
# §9.3 ROPE COIL
COIL_OD, COIL_TUBE, COIL_ID, COIL_RC, COIL_LB = 10.0, 2.5, 5.0, 3.75, 1.0

HEX = {"crate": "#7B3FA0", "cell-body": "#F2F2F0", "cell-cap": "#2E8B57", "cell-fillet": "#4D4D4D",
       "coil": "#D9A441", "blue": "#1D63C8", "red": "#CC3333"}
LB = {"crate": CRATE_LB, "cell": CELL_LB, "coil": COIL_LB}
LABEL = {"crate": "CACHE CRATE", "cell": "O2 CELL", "coil": "ROPE COIL"}
MAT_WORDS = {"crate": ("ripstop", "pu foam"), "cell": ("core", "eva"), "coil": ("rubber", "foam")}

# §6 FIELD SETUP CHART
CACHE_X, CACHE_Y = (300.0, 324.0, 348.0), (138.0, 162.0, 186.0)
CHART_A = {(300.0, 186.0): "crate", (324.0, 186.0): "cell", (348.0, 186.0): "coil",
           (300.0, 162.0): "coil", (324.0, 162.0): "crate", (348.0, 162.0): "cell",
           (300.0, 138.0): "cell", (324.0, 138.0): "coil", (348.0, 138.0): "crate"}
STAGE_X = {"BLUE": 144.0, "RED": 504.0}
CHART_B = {"BLUE": {108.0: "crate", 162.0: "cell", 216.0: "coil"},
           "RED": {108.0: "coil", 162.0: "cell", 216.0: "crate"}}
STOCK_PER = 7
CHUTE_Y = {"BLUE": (30.0, 294.0), "RED": (294.0, 30.0)}
CACHE_EXT_Y, CACHE_EXT_X, CORRIDOR, CORR_CLR = (131.5, 192.5), (293.0, 355.0), (128.0, 196.0), 3.5

# §1.1 / §2 CRAG
CRAG_C = {"BLUE": np.array([324.0, 240.0, 0.0]), "RED": np.array([324.0, 84.0, 0.0])}
N_SHELF = {"BLUE": np.array([-1.0, 0, 0]), "RED": np.array([1.0, 0, 0])}
HALF, SPIRE_HALF = 24.0, 10.0
SHELF_Z, SLOT_LAT, SLOT_OUT = (24.0, 42.0), (-15.5, 0.0, 15.5), 7.0
SHELF2_GUSSET_FLOOR, SHELF1_GUSSET_FLOOR = 38.0, 19.0
SOCK_STANDOFF, SOCK_LEN, SOCK_ID, SOCK_TOL = 8.0, 7.0, 6.50, 0.125
SOCK_WALL = 0.09                                 # §2.3 (ref) wall; the closed bottom lies beyond the 7.0 seat
# §2.4: rim 72, 15 deg; lowest point = 72 - 7.09 cos15 - 3.34 sin15 = 64.29, 9.29 over a crowned
# crate on Shelf 2 (see the docstring)
MAST_CLR = 5.0
SUMMIT_TUBE_CLR = (72.0 - (SOCK_LEN + SOCK_WALL) * math.cos(math.radians(15))
                   - (SOCK_ID / 2 + SOCK_WALL) * math.sin(math.radians(15)) - (42.0 + 13.0))
PEG_OD, PEG_LEN = 1.5, 10.0
TILT_BOUND, TILT_MARGIN = 47.9, 2.9              # §2.5
DEPOT_FLOOR, DEPOT_CH, DEPOT_ARM = 0.25, 16.0, 16.0
TAG_Z, TAG_TARGET = 17.5, 8.125
TARGET_BOTTOM = TAG_Z - TAG_TARGET / 2           # 13.4375
CELL_UPRIGHT_TOP, CELL_UPRIGHT_SHOULDER = 14.25, 12.47   # VISION-GUIDE §1.3

Z = np.array([0.0, 0.0, 1.0])
YW = np.array([0.0, 1.0, 0.0])


# ---------------------------------------------------------------------------------------
# measuring helpers (rays are exact on every surface type; BRepExtrema is NOT used on the
# crate's B-spline faces, where it misses interior extrema)
# ---------------------------------------------------------------------------------------
def _unit(d):
    d = np.asarray(d, float)
    return d / np.linalg.norm(d)


def _rgb(hx):
    return tuple(int(hx[i:i + 2], 16) for i in (1, 3, 5))


def _hue(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0:
        return 0.0
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return 60.0 * h


def _hue_dist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


class Probe:
    def __init__(self, shape):
        self.s = shape
        self.it = IntCurvesFace_ShapeIntersector()
        self.it.Load(shape, 1e-9)

    def hits(self, p, d, lo=-400.0, hi=400.0):
        d = _unit(d)
        self.it.Perform(gp_Lin(gp_Pnt(*[float(v) for v in p]), gp_Dir(*[float(v) for v in d])), lo, hi)
        return sorted(self.it.WParameter(i) for i in range(1, self.it.NbPnt() + 1))

    def first(self, p, d, lo=0.0, hi=400.0):
        h = [t for t in self.hits(p, d, lo, hi) if t >= lo]
        return h[0] if h else None

    def support(self, c, d, span, L=200.0, n=9):
        """max over the shape of (x - c).d, by parallel rays and a pattern search; also returns
        the world point where it is attained."""
        d = _unit(d)
        c = np.asarray(c, float)
        e1 = _unit(np.cross(d, [0, 0, 1]) if abs(d[2]) < 0.9 else np.cross(d, [1, 0, 0]))
        e2 = np.cross(d, e1)

        def g(u, v):
            h = self.first(c + u * e1 + v * e2 + L * d, -d, 0.0, 2 * L)
            return (L - h) if h is not None else -1e9

        best = max((g(u, v), u, v) for u in np.linspace(-span, span, n) for v in np.linspace(-span, span, n))
        val, u, v = best
        step = 2.0 * span / (n - 1)
        moves = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))
        while step > 1e-7:
            for du, dv in moves:
                w = g(u + du * step, v + dv * step)
                if w > val + 1e-14:
                    val, u, v = w, u + du * step, v + dv * step
                    break
            else:
                step /= 2
        return val, c + u * e1 + v * e2 + val * d


def _circle_fit(pts):
    pts = np.asarray(pts, float)
    A = np.c_[2 * pts[:, 0], 2 * pts[:, 1], np.ones(len(pts))]
    b = (pts ** 2).sum(1)
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = sol[0], sol[1]
    r = math.sqrt(sol[2] + cx * cx + cy * cy)
    res = float(np.max(np.abs(np.hypot(pts[:, 0] - cx, pts[:, 1] - cy) - r)))
    return cx, cy, r, res


def _loose_box(shape):
    b = K.Bnd_Box()
    K.BRepBndLib.Add_s(shape, b, False)
    return K._box6(b)


def _overlap(a, b, pad=0.0):
    return not (a[0] > b[3] + pad or b[0] > a[3] + pad or a[1] > b[4] + pad or b[1] > a[4] + pad
                or a[2] > b[5] + pad or b[2] > a[5] + pad)


def _common(a, b):
    c = K.BRepAlgoAPI_Common(a, b)
    if not c.IsDone():
        return float("nan")
    return K._volume(K._solids(c.Shape()))


def _seclen(a, b):
    s = BRepAlgoAPI_Section(a, b)
    g = K.GProp_GProps()
    K.BRepGProp.LinearProperties_s(s.Shape(), g)
    return g.Mass()


def _clash(a, b, bspline=False):
    """Interference measure between two solids (0 = none).  OpenCascade's Common silently
    returns an empty result for the crate's B-spline faces against e.g. a socket tube that
    it visibly overlaps, so for crates the boundaries are also sectioned: a crowned crate only
    ever touches anything at isolated points, so any section curve means interpenetration."""
    v = _common(a, b)
    if v > 1e-6 or v != v:
        return v
    if bspline:
        L = _seclen(a, b)
        if L > 1e-3:
            return L
    return 0.0


def _moved(shape, src_c, R, dst_c):
    """x -> R (x - src_c) + dst_c (R orthonormal, columns = images of the source axes)."""
    R = np.asarray(R, float)
    t = np.asarray(dst_c, float) - R @ np.asarray(src_c, float)
    tr = gp_Trsf()
    tr.SetValues(R[0, 0], R[0, 1], R[0, 2], t[0], R[1, 0], R[1, 1], R[1, 2], t[1], R[2, 0], R[2, 1], R[2, 2], t[2])
    return K.BRepBuilderAPI_Transform(shape, tr, True).Shape()


def _basis_from(a):
    """Orthonormal R whose first column is a."""
    a = _unit(a)
    h = np.array([0, 0, 1.0]) if abs(a[2]) < 0.9 else np.array([1.0, 0, 0])
    b = _unit(np.cross(h, a))
    c = np.cross(a, b)
    return np.c_[a, b, c]


def _basis_z(a):
    """Orthonormal R whose third column is a."""
    a = _unit(a)
    h = np.array([1.0, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1.0, 0])
    x = _unit(np.cross(h, a))
    y = np.cross(a, x)
    return np.c_[x, y, a]


def _faces(shape):
    exp = K.TopExp_Explorer(shape, K.TopAbs_FACE)
    while exp.More():
        yield TopoDS.Face(exp.Current())
        exp.Next()


def _fmt(v, n=4):
    return "[" + ", ".join(("%." + str(n) + "f") % x for x in v) + "]"


# ---------------------------------------------------------------------------------------
# shared state
# ---------------------------------------------------------------------------------------
class Ctx:
    def __init__(self, f):
        self.f = f
        self.boxes = [(r, _loose_box(K._compound(r["solids"]))) for r in f.records() if r["solids"]]
        self.pieces = []
        for r in f.records():
            nm = r["name"] or ""
            for k, lab in LABEL.items():
                if nm.startswith(lab + " - "):
                    self.pieces.append(self._measure(r, k))
        self.piece_ids = {id(p["rec"]) for p in self.pieces}

    def _measure(self, rec, kind):
        s = rec["solids"][0]
        P = Probe(s)
        bb = _loose_box(s)
        c0 = np.array([(bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2, (bb[2] + bb[5]) / 2])
        span = max(bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]) / 2 + 1.0
        sup = {}
        for key, d in (("+x", (1, 0, 0)), ("-x", (-1, 0, 0)), ("+y", (0, 1, 0)), ("-y", (0, -1, 0)),
                       ("+z", (0, 0, 1)), ("-z", (0, 0, -1))):
            sup[key] = P.support(c0, d, span)
        lo = np.array([c0[0] - sup["-x"][0], c0[1] - sup["-y"][0], c0[2] - sup["-z"][0]])
        hi = np.array([c0[0] + sup["+x"][0], c0[1] + sup["+y"][0], c0[2] + sup["+z"][0]])
        return {"rec": rec, "name": rec["name"], "kind": kind, "solid": s, "probe": P, "lo": lo, "hi": hi,
                "c": (lo + hi) / 2, "ext": hi - lo, "low_pt": sup["-z"][1], "nsol": len(rec["solids"])}

    def near(self, shape, pad=0.01, exclude_pieces=False, only=None):
        bb = _loose_box(shape)
        out = []
        for r, b in self.boxes:
            if exclude_pieces and id(r) in self.piece_ids:
                continue
            if only is not None and not only(r):
                continue
            if _overlap(bb, b, pad):
                out.append(r)
        return out

    def hits_any(self, shape, exclude=(), exclude_pieces=False, bspline=False):
        """[(name, interference)] for every body the shape interpenetrates (crate-aware)."""
        ex = {id(r) for r in exclude}
        out = []
        for r in self.near(shape, 0.01, exclude_pieces):
            if id(r) in ex:
                continue
            crate_rec = (r["name"] or "").startswith(LABEL["crate"] + " - ")
            v = sum(_clash(shape, s, bspline or crate_rec) for s in r["solids"])
            if v > 1e-6 or v != v:
                out.append((r["name"], round(v, 5)))
        return out

    def rep(self, kind, xy):
        c = [p for p in self.pieces if p["kind"] == kind]
        return min(c, key=lambda p: np.hypot(p["c"][0] - xy[0], p["c"][1] - xy[1]))


def _kind_by_shape(ext):
    e = sorted(ext)
    if all(abs(v - CRATE_ENV) < 0.05 for v in e):
        return "crate"
    if abs(e[0] - CELL_D) < 0.05 and abs(e[1] - CELL_D) < 0.05 and abs(e[2] - CELL_L) < 0.05:
        return "cell"
    if abs(e[0] - COIL_TUBE) < 0.05 and abs(e[1] - COIL_OD) < 0.05 and abs(e[2] - COIL_OD) < 0.05:
        return "coil"
    return "?"


def _where(p):
    """Location class of a piece from its geometry: ('cache', (x, y)) / ('stage', side, y) /
    ('stock', side) / ('?',)."""
    x, y = p["c"][0], p["c"][1]
    if x < 0:
        return ("stock", "BLUE")
    if x > FIELD_L:
        return ("stock", "RED")
    for gx in CACHE_X:
        for gy in CACHE_Y:
            if math.hypot(x - gx, y - gy) < 1.0:
                return ("cache", (gx, gy))
    for side, sx in STAGE_X.items():
        for sy in CHART_B[side]:
            if math.hypot(x - sx, y - sy) < 15.0:
                return ("stage", side, sy)
    return ("?",)


# ---------------------------------------------------------------------------------------
# sections
# ---------------------------------------------------------------------------------------
def sec_inventory(f, C, add):
    by = {k: [p for p in C.pieces if p["kind"] == k] for k in LABEL}
    for k, lab in LABEL.items():
        add("count: %s bodies = 21 (§6 count check)" % lab, len(by[k]) == 21, "found %d" % len(by[k]))
    add("count: 63 SUPPLIES in total", len(C.pieces) == 63, "found %d" % len(C.pieces))
    bad = [p["name"] for p in C.pieces if p["nsol"] != 1]
    add("every SUPPLY body is exactly one solid", not bad, "multi-solid: %s" % bad[:5])
    mism = [(p["name"], _kind_by_shape(p["ext"])) for p in C.pieces if _kind_by_shape(p["ext"]) != p["kind"]]
    add("every SUPPLY's name matches its measured shape", not mism, "%s" % mism[:5])
    masters = [r["name"] for r in f.records() if (r["name"] or "") in LABEL.values()]
    add("no master SUPPLY left in the model (only named, staged copies)", not masters, "%s" % masters)
    warn = [w for w in f.ctx.warnings if any(s in w for s in ("CRATE", "CELL", "COIL"))]
    add("no SUPPLY feature warning (e.g. crate edge fillets skipped)", not warn, "%s" % warn)
    loc = {}
    for p in C.pieces:
        w = _where(p)
        loc.setdefault(w[0], []).append(p)
    stray = [(p["name"], _fmt(p["c"], 2)) for p in loc.get("?", [])]
    add("every SUPPLY is at a CENTER CACHE mark, an alliance staging mark or OUTFITTER stock", not stray, "%s" % stray)


def sec_crate(f, C, add):
    rep = C.rep("crate", (324.0, 162.0))
    P, c = rep["probe"], rep["c"]
    # (1a) crowned envelope on all six half-axes
    sup = {k: P.support(c, d, 8.0)[0] for k, d in (("+x", (1, 0, 0)), ("-x", (-1, 0, 0)), ("+y", (0, 1, 0)),
                                                   ("-y", (0, -1, 0)), ("+z", (0, 0, 1)), ("-z", (0, 0, -1)))}
    add("CRATE crowned envelope 13.0 across every pair of faces (§9.1)",
        all(abs(2 * v - CRATE_ENV) < 1e-4 for v in sup.values()),
        "half-extents from the centre %s" % {k: round(v, 5) for k, v in sup.items()})
    # (1b) pillow profile of each face along its centreline -> edge plane and crown
    samp = [-5.0, -4.5, -4.0, -3.0, -1.5, 0.0, 1.5, 3.0, 4.0, 4.5, 5.0]
    faces = [("+X", 0, 2, 1), ("-X", 0, 2, -1), ("+Y", 1, 2, 1), ("-Y", 1, 2, -1), ("+Z", 2, 0, 1), ("-Z", 2, 0, -1)]
    edges, crowns, resid = {}, {}, {}
    for lab, ax, var, sgn in faces:
        ws = []
        for t in samp:
            o = c.copy()
            o[var] += t
            d = np.zeros(3)
            d[ax] = sgn
            ws.append(P.first(o, d))
        A = np.c_[np.ones(len(samp)), np.array(samp) ** 2]
        (a0, b0), *_ = np.linalg.lstsq(A, np.array(ws), rcond=None)
        resid[lab] = float(np.max(np.abs(A @ np.array([a0, b0]) - np.array(ws))))
        e = (1 - math.sqrt(1 - 4 * a0 * b0)) / (2 * b0) if b0 < 0 else float("nan")
        edges[lab], crowns[lab] = e, a0 - e
    add("CRATE 12.0 cube: every pillow face meets its cube-edge planes at +/-6.00 (§9.1 CRITICAL)",
        all(abs(2 * e - CRATE_EDGE) < 0.05 for e in edges.values()),
        "edge width per face %s (profile fit residual %s)" % ({k: round(2 * v, 4) for k, v in edges.items()},
                                                            {k: "%.1e" % v for k, v in resid.items()}))
    add("CRATE face crown 0.5 on all six faces (§9.1)",
        all(abs(v - CRATE_CROWN) < 0.005 for v in crowns.values()), "%s" % {k: round(v, 4) for k, v in crowns.items()})
    # (1c) resting geometry: widths 2.0 above the resting surface, full bulge at 6.5
    rest = c[2] - sup["-z"]
    zf = rest + FENCE_H - c[2]
    wx = P.first(c + [0, 0, zf], (1, 0, 0)) + P.first(c + [0, 0, zf], (-1, 0, 0))
    wy = P.first(c + [0, 0, zf], (0, 1, 0)) + P.first(c + [0, 0, zf], (0, -1, 0))
    add("CRATE width 2.0 above its resting surface = 12.44 (§9.1 / M40)",
        abs(wx - CRATE_W_FENCE) < 0.005 and abs(wy - CRATE_W_FENCE) < 0.005, "X %.5f  Y %.5f" % (wx, wy))
    add("CRATE clearance per side in the 14.0 slot at the fence top = 0.78 (§9.1)",
        abs((SLOT_W - max(wx, wy)) / 2 - CRATE_SIDE_CLR) < 0.005, "%.5f" % ((SLOT_W - max(wx, wy)) / 2))
    wprof = {h: P.first(c + [0, 0, rest + h - c[2]], (1, 0, 0)) for h in (1.0, 2.0, 4.0, 6.0, 6.5, 7.0, 9.0, 11.0)}
    add("CRATE side face reaches its full 0.5 bulge 6.5 above the resting surface (widest there)",
        abs(wprof[6.5] - CRATE_ENV / 2) < 1e-4 and all(wprof[6.5] >= v - 1e-9 for v in wprof.values()),
        "half-width by height above rest %s" % {k: round(v, 4) for k, v in wprof.items()})
    bottom_plane = c[2] - edges["-Z"]
    add("CRATE cube bottom plane 0.5 above the resting surface (rests on its crown)",
        abs(bottom_plane - rest - CRATE_CROWN) < 0.01, "%.4f" % (bottom_plane - rest))
    # lowest point = bottom crown apex under the centre
    lp = rep["low_pt"]
    add("CRATE lowest point is the bottom crown apex under the centre",
        np.hypot(lp[0] - c[0], lp[1] - c[1]) < 0.01, "lowest point %s vs centre %s" % (_fmt(lp), _fmt(c)))
    # (1d) R1.0 fillets on all twelve edges: circle fit in each mid-edge section
    e = 0.5 * CRATE_EDGE
    radii, bad = [], []
    for k in range(3):
        i, j = [a for a in range(3) if a != k]
        for si in (-1, 1):
            for sj in (-1, 1):
                pts = []
                for phi in (42.0, 43.5, 45.0, 46.5, 48.0):
                    d = np.zeros(3)
                    d[i] = si * math.cos(math.radians(phi))
                    d[j] = sj * math.sin(math.radians(phi))
                    t = P.first(c, d)
                    pts.append((t * d[i], t * d[j]))
                cx, cy, r, res = _circle_fit(pts)
                radii.append(r)
                # ball centre must sit on the section's diagonal, inboard of the sharp edge
                if abs(abs(cx) - abs(cy)) > 1e-3 or res > 1e-3:
                    bad.append((k, si, sj, round(cx, 4), round(cy, 4), round(res, 5)))
    add("CRATE R1.0 fillet on all twelve edges (mid-edge section is a 1.0 circle) (§9.1)",
        len(radii) == 12 and all(abs(r - CRATE_FILLET) < 0.02 for r in radii) and not bad,
        "radii %s %s" % ([round(r, 4) for r in radii], ("odd sections %s" % bad) if bad else ""))
    setbacks = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                d = _unit([sx, sy, sz])
                setbacks.append(math.sqrt(3) * e - P.first(c, d))
    add("CRATE corners blended (all eight cube corners removed by >= 0.41)",
        all(s > 0.41 for s in setbacks), "setbacks %s" % [round(s, 3) for s in setbacks])
    # (1e) every crate identical and square to the axes
    crates = [p for p in C.pieces if p["kind"] == "crate"]
    v0 = f.volume([rep["rec"]])
    badv = [p["name"] for p in crates if abs(f.volume([p["rec"]]) - v0) > 1e-6 * v0]
    add("all 21 CRATES are identical copies (volume)", not badv, "%s" % badv[:4])
    bads = [(p["name"], _fmt(p["ext"])) for p in crates if np.max(np.abs(p["ext"] - CRATE_ENV)) > 1e-4]
    add("every CRATE staged square to the axes (13.0 x 13.0 x 13.0 world extents)", not bads, "%s" % bads[:4])


def sec_cell(f, C, add):
    rep = C.rep("cell", (300.0, 138.0))
    P, c = rep["probe"], rep["c"]
    cells = [p for p in C.pieces if p["kind"] == "cell"]
    bad = [(p["name"], _fmt(p["ext"])) for p in cells
           if abs(p["ext"][0] - CELL_L) > 1e-4 or abs(p["ext"][1] - CELL_D) > 1e-4 or abs(p["ext"][2] - CELL_D) > 1e-4]
    add("every O2 CELL is 5.0 dia x 14.0 with its axis along +X (§9.2, §6)", not bad, "%s" % bad[:4])

    def r_at(a):
        return P.first(c + [a, 0, 0], (0, 1, 0))

    body = [r_at(s * a) for a in (0.0, 3.0, 5.0) for s in (-1, 1)]
    add("O2 CELL body radius 2.50 along the cylinder", all(abs(r - CELL_D / 2) < 1e-6 for r in body),
        "%s" % [round(r, 7) for r in body])
    res = {}
    for s in (1, -1):
        dome = [(s * a, r_at(s * a)) for a in (5.85, 6.1, 6.35, 6.6, 6.85)]
        # r^2 + (a - a0)^2 = R^2  ->  r^2 + a^2 = 2 a a0 + (R^2 - a0^2)
        A = np.c_[2 * np.array([abs(a) for a, _ in dome]), np.ones(5)]
        b = np.array([r * r + a * a for a, r in dome])
        (a0, k), *_ = np.linalg.lstsq(A, b, rcond=None)
        R = math.sqrt(k + a0 * a0)
        dres = max(abs(math.hypot(r, abs(a) - a0) - R) for a, r in dome)
        a_eq = a0 + math.sqrt(R * R - (CELL_D / 2) ** 2)
        brk = math.degrees(math.atan2(a_eq - a0, CELL_D / 2))
        fil = [(a, r_at(s * a)) for a in (5.26, 5.38, 5.5, 5.62, 5.74)]
        fa, fr, fR, fres = _circle_fit(fil)
        res[s] = dict(a0=a0, R=R, dres=dres, a_eq=a_eq, brk=brk, fa=fa, fr=fr, fR=fR, fres=fres,
                      pole=P.first(c, (s, 0, 0)))
    for s, d in res.items():
        end = "+X" if s > 0 else "-X"
        add("O2 CELL %s dome is spherical and ends at the pole, 7.0 from the centre" % end,
            d["dres"] < 1e-5 and abs(d["a0"] + d["R"] - CELL_L / 2) < 1e-3 and abs(d["pole"] - CELL_L / 2) < 1e-6,
            "sphere R %.4f centre a %.4f (fit residual %.1e), pole %.6f" % (d["R"], d["a0"], d["dres"], d["pole"]))
        add("O2 CELL %s dome height 1.5, struck through pole and equator (arc endpoints 11.0 apart)" % end,
            abs(CELL_L / 2 - d["a_eq"] - CELL_DOME) < 0.005, "equator at a = %.4f -> dome %.4f, endpoints %.4f"
            % (d["a_eq"], CELL_L / 2 - d["a_eq"], 2 * d["a_eq"]))
        add("O2 CELL %s dome meets the cylinder at a 28.1-degree tangent break (§9.2)" % end,
            abs(d["brk"] - CELL_BREAK) < 0.05, "%.3f deg" % d["brk"])
        add("O2 CELL %s R1.0 blend tangent to the body and to the dome (§9.2)" % end,
            abs(d["fR"] - CELL_FR) < 0.01 and d["fres"] < 1e-4 and abs(d["fr"] + d["fR"] - CELL_D / 2) < 2e-3
            and abs(math.hypot(d["fa"] - d["a0"], d["fr"]) - (d["R"] - d["fR"])) < 2e-3,
            "fillet R %.4f centre (a %.4f, r %.4f), residual %.1e; |c_f - c_dome| %.4f vs R_dome - R_f %.4f"
            % (d["fR"], d["fa"], d["fr"], d["fres"], math.hypot(d["fa"] - d["a0"], d["fr"]), d["R"] - d["fR"]))
    full = res[1]["fa"] + res[-1]["fa"]
    inside = r_at(res[1]["fa"] - 0.02)
    past = r_at(res[1]["fa"] + 0.1)
    add("O2 CELL full 5.0 diameter runs 10.44 (not the 11.0 arc-endpoint length) (§9.2 / M42)",
        abs(full - CELL_FULL) < 0.01 and abs(inside - 2.5) < 1e-6 and past < 2.5 - 1e-3,
        "full-diameter length %.4f (r just inside %.7f, 0.1 past %.4f)" % (full, inside, past))
    v0 = f.volume([rep["rec"]])
    badv = [p["name"] for p in cells if abs(f.volume([p["rec"]]) - v0) > 1e-6 * v0]
    add("all 21 O2 CELLS are identical copies (volume)", not badv, "%s" % badv[:4])
    # colours by face: domes cap, blends fillet, body none (body colour)
    cap, fil, body_rgb = _rgb(HEX["cell-cap"]), _rgb(HEX["cell-fillet"]), _rgb(HEX["cell-body"])
    a_td = res[1]["a0"] + (res[1]["fa"] - res[1]["a0"]) * res[1]["R"] / (res[1]["R"] - res[1]["fR"])
    s = rep["solid"]
    fl = list(_faces(s))
    cls = []
    for fc in fl:
        bx = K.Bnd_Box()
        K.BRepBndLib.AddOptimal_s(fc, bx, False, False)     # exact on these analytic faces
        bb = K._box6(bx)
        a_lo, a_hi = bb[0] - c[0], bb[3] - c[0]
        if a_lo > a_td - 0.05:
            cls.append("dome+")
        elif a_hi < -a_td + 0.05:
            cls.append("dome-")
        elif a_lo > res[1]["fa"] - 0.05:
            cls.append("blend+")
        elif a_hi < -res[1]["fa"] + 0.05:
            cls.append("blend-")
        else:
            cls.append("body")
    style = {i: [] for i in range(len(fl))}
    for (pt, rgb, al) in rep["rec"]["faces"]:
        v = K.BRepBuilderAPI_MakeVertex(K._gp(pt)).Vertex()
        for i, fc in enumerate(fl):
            if K.BRepExtrema_DistShapeShape(v, fc).Value() < 1e-5:
                style[i].append((tuple(rgb), al))
    want = {"dome+": cap, "dome-": cap, "blend+": fil, "blend-": fil, "body": None}
    got = {cls[i]: (style[i][0][0] if style[i] else None) for i in range(len(fl))}
    ok = sorted(cls) == sorted(want) and all(got.get(k) == v for k, v in want.items()) \
        and all(len(v) <= 1 for v in style.values()) and all(a == 1 for v in style.values() for _, a in v)
    add("O2 CELL colours: both domes #2E8B57, both R1.0 blend bands #4D4D4D, body #F2F2F0 (MATERIALS §1.3, §2)",
        ok and tuple(rep["rec"]["rgb"]) == body_rgb,
        "faces %s -> %s; body rgb %s" % (cls, got, rep["rec"]["rgb"]))
    badc = []
    for p in cells:
        st = p["rec"]["faces"]
        caps = sorted(round((np.asarray(pt) - p["c"])[0], 3) for pt, rgb, _ in st if tuple(rgb) == cap)
        fils = sorted(round((np.asarray(pt) - p["c"])[0], 3) for pt, rgb, _ in st if tuple(rgb) == fil)
        okp = (len(st) == 4 and len(caps) == 2 and len(fils) == 2 and caps[0] < -a_td and caps[1] > a_td
               and -a_td < fils[0] < -res[1]["fa"] and res[1]["fa"] < fils[1] < a_td
               and tuple(p["rec"]["rgb"]) == body_rgb)
        if not okp:
            badc.append((p["name"], caps, fils, p["rec"]["rgb"]))
    add("every O2 CELL carries cap colour on both domes and fillet colour on both blend bands",
        not badc, "%s" % badc[:3])


def sec_coil(f, C, add):
    rep = C.rep("coil", (324.0, 138.0))
    P, c = rep["probe"], rep["c"]
    coils = [p for p in C.pieces if p["kind"] == "coil"]
    bad = [(p["name"], _fmt(p["ext"])) for p in coils
           if abs(p["ext"][0] - COIL_OD) > 1e-4 or abs(p["ext"][1] - COIL_OD) > 1e-4 or abs(p["ext"][2] - COIL_TUBE) > 1e-4]
    add("every ROPE COIL is 10.0 OD x 2.5 thick and lies flat (§9.3, §6)", not bad, "%s" % bad[:4])
    rad = []
    for ang in (0, 30, 60, 90, 135):
        d = (math.cos(math.radians(ang)), math.sin(math.radians(ang)), 0)
        rad.append(P.hits(c, d))
    ok = all(len(h) == 4 and abs(h[0] + COIL_OD / 2) < 1e-6 and abs(h[3] - COIL_OD / 2) < 1e-6
             and abs(h[1] + COIL_ID / 2) < 1e-6 and abs(h[2] - COIL_ID / 2) < 1e-6 for h in rad)
    add("ROPE COIL OD 10.0 and ID 5.0 in every radial direction (§9.3 CRITICAL)", ok,
        "hits %s" % [[round(v, 6) for v in h] for h in rad[:2]])
    pts = []
    for dr in (-1.0, -0.6, -0.2, 0.0, 0.3, 0.7, 1.1):
        h = P.hits(c + [COIL_RC + dr, 0, -5], (0, 0, 1), 0, 10)
        if len(h) == 2:
            pts += [(COIL_RC + dr, h[0] - 5), (COIL_RC + dr, h[1] - 5)]
    cr, cz, R, res = _circle_fit(pts)
    add("ROPE COIL tube section is one 2.5-dia circle centred at r = 3.75 (one revolve) (§9.3 / M43)",
        len(pts) == 14 and abs(cr - COIL_RC) < 1e-4 and abs(cz) < 1e-4 and abs(2 * R - COIL_TUBE) < 1e-4 and res < 1e-5,
        "section centre r %.5f z %.5f, dia %.5f, residual %.1e" % (cr, cz, 2 * R, res))
    nf = len(list(_faces(rep["solid"])))
    add("ROPE COIL is a single toroidal face (no split or seam faces)", nf == 1, "%d faces" % nf)
    v0 = f.volume([rep["rec"]])
    badv = [p["name"] for p in coils if abs(f.volume([p["rec"]]) - v0) > 1e-6 * v0]
    add("all 21 ROPE COILS are identical copies (volume)", not badv, "%s" % badv[:4])


def sec_props(f, C, add):
    for k in LABEL:
        ps = [p for p in C.pieces if p["kind"] == k]
        m = [f.mass_lb([p["rec"]]) for p in ps]
        add("%s mass %.1f lb each (§9 / DESIGN-SPEC §2)" % (LABEL[k], LB[k]),
            ps and all(abs(x - LB[k]) < 1e-3 for x in m), "min %.5f max %.5f" % (min(m), max(m)))
        want = _rgb(HEX["crate" if k == "crate" else ("cell-body" if k == "cell" else "coil")])
        badc = [(p["name"], p["rec"]["rgb"], p["rec"]["alpha"]) for p in ps
                if tuple(p["rec"]["rgb"]) != want or p["rec"]["alpha"] != 1]
        add("%s body colour %s, opaque (MATERIALS §1.3)" % (LABEL[k], HEX["crate" if k == "crate" else ("cell-body" if k == "cell" else "coil")]),
            not badc, "%s" % badc[:3])
        names = {(p["rec"]["mat"] or {}).get("name", "") for p in ps}
        okm = len(names) == 1 and all(w in next(iter(names)).lower() for w in MAT_WORDS[k])
        add("%s material is the MATERIALS §2 construction (%s)" % (LABEL[k], " / ".join(MAT_WORDS[k])), okm, "%s" % names)
    blue = f.find("BLUE BASECAMP tape")[0]["rgb"]
    red = f.find("RED BASECAMP tape")[0]["rgb"]
    crate = [p for p in C.pieces if p["kind"] == "crate"][0]["rec"]["rgb"]
    hb, hr = _hue_dist(_hue(crate), _hue(blue)), _hue_dist(_hue(crate), _hue(red))
    add("CRATE violet is 62 deg from alliance blue and 83 deg from alliance red in hue (MATERIALS §1.3)",
        abs(hb - 62) < 0.5 and abs(hr - 83) < 0.5, "%.2f / %.2f deg (built colours %s %s %s)" % (hb, hr, crate, blue, red))
    near = []
    for p in C.pieces:
        for st in [p["rec"]["rgb"]] + [rgb for _, rgb, _ in p["rec"]["faces"]]:
            h = _hue(st)
            sat = (max(st) - min(st)) / max(1, max(st))
            if sat > 0.2 and min(_hue_dist(h, _hue(blue)), _hue_dist(h, _hue(red))) < 30:
                near.append((p["name"], st))
    add("no SUPPLY colour is in or near an alliance colour (within 30 deg of hue)", not near, "%s" % near[:3])


def sec_staging(f, C, add):
    loc = {}
    for p in C.pieces:
        loc.setdefault(_where(p), []).append(p)
    # chart (a)
    bad = []
    for (gx, gy), k in CHART_A.items():
        ps = loc.get(("cache", (gx, gy)), [])
        if len(ps) != 1 or ps[0]["kind"] != k or np.hypot(ps[0]["c"][0] - gx, ps[0]["c"][1] - gy) > 1e-6:
            bad.append(((gx, gy), k, [(q["kind"], _fmt(q["c"], 5)) for q in ps]))
        elif ("(%d, %d)" % (gx, gy)) not in ps[0]["name"]:
            bad.append(((gx, gy), "name", ps[0]["name"]))
    add("CENTER CACHE: one SUPPLY per mark, exactly the FIELD SETUP CHART (a) Latin square, centred on the mark",
        not bad, "%s" % bad)
    grid = {}
    for (gx, gy), ps in [(w[1], ps) for w, ps in loc.items() if w[0] == "cache"]:
        grid[(gx, gy)] = ps[0]["kind"]
    latin = all(sorted(grid.get((x, y), "?") for x in CACHE_X) == ["cell", "coil", "crate"] for y in CACHE_Y) and \
        all(sorted(grid.get((x, y), "?") for y in CACHE_Y) == ["cell", "coil", "crate"] for x in CACHE_X)
    add("CENTER CACHE: each type once per row and once per column", latin, "%s" % grid)
    # chart (b)
    bad = []
    for side in ("BLUE", "RED"):
        for sy, k in CHART_B[side].items():
            ps = loc.get(("stage", side, sy), [])
            mid = np.mean([q["c"][:2] for q in ps], axis=0) if ps else np.array([np.nan, np.nan])
            if len(ps) != 2 or any(q["kind"] != k for q in ps) or np.hypot(mid[0] - STAGE_X[side], mid[1] - sy) > 1e-6:
                bad.append((side, sy, k, [(q["kind"], _fmt(q["c"], 3)) for q in ps]))
            elif any(side not in q["name"] or "staging mark" not in q["name"] for q in ps):
                bad.append((side, sy, "name", [q["name"] for q in ps]))
    add("alliance staging: 2 of ONE type per mark, per FIELD SETUP CHART (b), pair centred on the mark",
        not bad, "%s" % bad)
    blue = [p for w, ps in loc.items() if w[0] == "stage" and w[1] == "BLUE" for p in ps]
    red = [p for w, ps in loc.items() if w[0] == "stage" and w[1] == "RED" for p in ps]
    miss = []
    for p in blue:
        rc = np.array([FIELD_L - p["c"][0], FIELD_W - p["c"][1], p["c"][2]])
        if not any(q["kind"] == p["kind"] and np.linalg.norm(q["c"] - rc) < 1e-6 for q in red):
            miss.append((p["name"], _fmt(rc, 3)))
    add("Red staging is the 180-degree rotation of Blue about (324, 162)", not miss and len(red) == len(blue) == 6,
        "%s (blue %d red %d)" % (miss, len(blue), len(red)))
    # chart (c) OUTFITTER stock
    for side in ("BLUE", "RED"):
        ps = loc.get(("stock", side), [])
        cnt = {k: sum(1 for q in ps if q["kind"] == k) for k in LABEL}
        add("%s OUTFITTER stock: 7 of each type (FIELD SETUP CHART (c))" % side,
            all(v == STOCK_PER for v in cnt.values()), "%s" % cnt)
        badp = []
        for q in ps:
            behind = q["hi"][0] < 0 if side == "BLUE" else q["lo"][0] > FIELD_L
            infield = q["lo"][1] >= 0 and q["hi"][1] <= FIELD_W
            dy = min(abs(q["c"][1] - y) for y in CHUTE_Y[side])
            if not (behind and infield and dy <= 36.0) or side not in q["name"] or "OUTFITTER" not in q["name"]:
                badp.append((q["name"], _fmt(q["lo"], 2), _fmt(q["hi"], 2)))
        add("%s OUTFITTER stock lies behind the %s alliance wall at its chutes" % (side, side), not badp, "%s" % badp[:4])
    # per-type accounting
    acc = {}
    for k in LABEL:
        acc[k] = (sum(1 for w, ps in loc.items() if w[0] == "cache" for q in ps if q["kind"] == k),
                  sum(1 for w, ps in loc.items() if w[0] == "stage" for q in ps if q["kind"] == k),
                  sum(1 for w, ps in loc.items() if w[0] == "stock" for q in ps if q["kind"] == k))
    add("per type: 3 CENTER CACHE + 2 x 2 staging + 2 x 7 OUTFITTER = 21 (§6 count check)",
        all(v == (3, 4, 14) for v in acc.values()), "%s" % acc)


def _support_probe(C, p):
    """Probe over every non-SUPPLY body under the piece's footprint."""
    bb = [p["lo"][0] - 0.5, p["lo"][1] - 0.5, -5.0, p["hi"][0] + 0.5, p["hi"][1] + 0.5, p["lo"][2] + 0.1]
    rs = [r for r, b in C.boxes if id(r) not in C.piece_ids and _overlap(bb, b)]
    sols = [s for r in rs for s in r["solids"]]
    return (Probe(K._compound(sols)) if sols else None), [r["name"] for r in rs]


def _lowest_samples(p):
    c, z = p["c"], p["lo"][2]
    if p["kind"] == "crate":
        return [np.array([p["low_pt"][0], p["low_pt"][1], z])]
    if p["kind"] == "cell":
        return [np.array([c[0] + a, c[1], z]) for a in np.linspace(-5.0, 5.0, 11)]
    return [np.array([c[0] + COIL_RC * math.cos(t), c[1] + COIL_RC * math.sin(t), z])
            for t in np.linspace(0, 2 * math.pi, 72, endpoint=False)]


def _rest_state(C, p):
    """(ok, gap, what) — the piece's lowest points against whatever is directly beneath them."""
    SP, names = _support_probe(C, p)
    gaps = []
    for q in _lowest_samples(p):
        # the sample really is on the piece's underside
        t = p["probe"].first(q - [0, 0, 1.0], (0, 0, 1), 0.0, 3.0)
        if t is None or abs(t - 1.0) > 1e-5:
            return False, float("nan"), "sample %s is not on the piece's underside" % _fmt(q)
        top = None
        if SP is not None:
            h = SP.first(q + [0, 0, 1e-3], (0, 0, -1), 0.0, 10.0)
            if h is not None:
                top = q[2] + 1e-3 - h
        if top is None:
            top = 0.0                                  # the floor plane (carpet top / venue floor)
        gaps.append(q[2] - top)
    g = min(gaps)
    return abs(g) < 1e-6, g, "lowest Z %.5f, smallest gap to the surface beneath %.5f" % (p["lo"][2], g)


def sec_rest(f, C, add):
    groups = {}
    for p in C.pieces:
        w = _where(p)
        grp = {"cache": "CENTER CACHE", "stage": "alliance staging marks", "stock": "OUTFITTER stock"}.get(w[0], "?")
        groups.setdefault((grp, p["kind"]), []).append(p)
    for (grp, k), ps in sorted(groups.items()):
        bad = []
        for p in ps:
            ok, g, why = _rest_state(C, p)
            if not ok:
                bad.append("%s: %s" % (p["name"], why))
        add("rest: %s at the %s rest on the surface beneath them (no hover, no sinking)" % (LABEL[k], grp),
            not bad, "; ".join(bad[:4]))
    cache = [p for p in C.pieces if _where(p)[0] == "cache"]
    off = [(p["name"], round(p["lo"][2], 6)) for p in cache if abs(p["lo"][2] - TAPE_T) > 1e-6]
    add("rest: every CENTER CACHE SUPPLY sits on its mark's tape top, Z 0.01 (MATERIALS §2 tape 0.01)",
        len(cache) == 9 and not off, "%s" % off)


def sec_interference(f, C, add):
    tape, struct, other = [], [], []
    for p in C.pieces:
        for r in C.near(p["solid"], 0.01):
            if r is p["rec"]:
                continue
            bs = p["kind"] == "crate" or (r["name"] or "").startswith(LABEL["crate"] + " - ")
            v = sum(_clash(p["solid"], s, bs) for s in r["solids"])
            if v > 1e-6 or v != v:
                nm = r["name"] or "?"
                if id(r) in C.piece_ids:
                    other.append((p["name"], nm, v))
                elif "tape" in nm or "mark" in nm:
                    tape.append((p["name"], nm, v))
                else:
                    struct.append((p["name"], nm, v))
    add("no SUPPLY interpenetrates any tape", not tape, "%s" % tape[:4])
    add("no SUPPLY interpenetrates any structure", not struct, "%s" % struct[:4])
    other = [o for o in other if o[0] < o[1]]
    add("no two SUPPLIES interpenetrate", not other, "%s" % other[:4])


def sec_extent(f, C, add):
    cache = [p for p in C.pieces if _where(p)[0] == "cache"]
    y0, y1 = min(p["lo"][1] for p in cache), max(p["hi"][1] for p in cache)
    x0, x1 = min(p["lo"][0] for p in cache), max(p["hi"][0] for p in cache)
    add("CENTER CACHE extent Y 131.5-192.5 across the crowned crate (§6 extent check)",
        abs(y0 - CACHE_EXT_Y[0]) < 1e-4 and abs(y1 - CACHE_EXT_Y[1]) < 1e-4, "Y %.5f-%.5f" % (y0, y1))
    add("CENTER CACHE extent X 293-355 (O2 CELL reaches X 293) (§6 extent check)",
        abs(x0 - CACHE_EXT_X[0]) < 1e-4 and abs(x1 - CACHE_EXT_X[1]) < 1e-4, "X %.5f-%.5f" % (x0, x1))
    # apron tape edges over the band, measured
    edges = {}
    for side, y_start, d in (("RED", 100.0, 1), ("BLUE", 224.0, -1)):
        pr = Probe(K._compound(f.solids(f.find("%s CRAG APRON tape" % side))))
        vals = []
        for x in (300.0, 324.0, 348.0):
            h = pr.hits((x, y_start, 0.005), (0, d, 0), 0.0, 40.0)
            vals.append(y_start + d * h[-1] if h else float("nan"))
        edges[side] = vals
    red_edge, blue_edge = max(edges["RED"]), min(edges["BLUE"])
    add("APRON corridor edges over the CENTER CACHE are Y 128 (Red) and Y 196 (Blue) (§1.2)",
        abs(red_edge - CORRIDOR[0]) < 1e-4 and abs(blue_edge - CORRIDOR[1]) < 1e-4, "%s" % edges)
    add("staged CENTER CACHE keeps 3.5 in of clearance to both APRONS (§1.2 / §6)",
        abs((y0 - red_edge) - CORR_CLR) < 1e-4 and abs((blue_edge - y1) - CORR_CLR) < 1e-4,
        "%.4f / %.4f" % (y0 - red_edge, blue_edge - y1))
    ap = f.find("re:^(BLUE|RED) CRAG APRON tape$")
    touching = [p["name"] for p in C.pieces if _where(p)[0] in ("cache", "stage")
                and any(_overlap(_loose_box(p["solid"]), _loose_box(s), 0.0) for s in f.solids(ap))
                and sum(_clash(p["solid"], s, p["kind"] == "crate") for s in f.solids(ap)) > 0]
    add("no staged SUPPLY touches an APRON", not touching, "%s" % touching)


# ---- virtual pieces in the field --------------------------------------------------------
def _crate_virtual(C):
    rep = C.rep("crate", (324.0, 162.0))
    return rep


def sec_shelves(f, C, add):
    rep = _crate_virtual(C)
    P = rep["probe"]
    rest_off = rep["c"][2] - rep["lo"][2]                               # 6.5
    w_fence = P.first(rep["c"] + [0, 0, FENCE_H - rest_off], (0, 1, 0))  # half-width at the fence top
    for side in ("BLUE", "RED"):
        n = N_SHELF[side]
        gaps, hits, rest_bad, over = [], [], [], {}
        for si, zt in enumerate(SHELF_Z):
            fence = Probe(K._compound(f.solids(f.find("%s CRAG Shelf %d slot fence" % (side, si + 1)))))
            for lat in SLOT_LAT:
                sc = CRAG_C[side] + (HALF + SLOT_OUT) * n + lat * YW
                cen = sc + (zt + rest_off) * Z
                sh = _moved(rep["solid"], rep["c"], np.eye(3), cen)
                h = C.hits_any(sh, bspline=True)
                if h:
                    hits.append((si + 1, lat, h))
                # rests on the shelf top
                top = Probe(K._compound(f.solids(f.find("%s CRAG Shelf %d" % (side, si + 1))))).first(
                    np.array([cen[0], cen[1], zt + 1.0]), (0, 0, -1))
                if top is None or abs((zt + 1.0 - top) - zt) > 1e-6:
                    rest_bad.append((si + 1, lat, top))
                o = np.array([sc[0], sc[1], zt + FENCE_H - 0.01])
                gp = fence.first(o, (0, 1, 0))
                gm = fence.first(o, (0, -1, 0))
                gaps.append((si + 1, lat, (gp - w_fence) if gp else None, (gm - w_fence) if gm else None))
                if si == 1:
                    over[lat] = sh
        add("%s CRAG: a crowned CRATE fits all six shelf slots without interference (§2.2 / §9.1)" % side,
            not hits, "%s" % hits[:3])
        add("%s CRAG: shelf top surfaces at Z 24 / 42 under the slot centres" % side, not rest_bad, "%s" % rest_bad)
        okg = all(g[2] is not None and g[3] is not None and abs(g[2] - CRATE_SIDE_CLR) < 0.01
                  and abs(g[3] - CRATE_SIDE_CLR) < 0.01 for g in gaps)
        add("%s CRAG: CRATE-to-fence clearance at the fence top 0.78 each side, every slot (§9.1)" % side, okg,
            "%s" % [(g[0], g[1], None if g[2] is None else round(g[2], 4), None if g[3] is None else round(g[3], 4))
                    for g in gaps])
        # Shelf 2 centre slot: >= 5.0 overhead (mast from Z 60), socket 9.29 above, and not loadable by a drop
        mast = f.find("%s CRAG Summit Socket mast" % side)
        sock = f.find("%s CRAG Summit Socket" % side)
        up = _moved(over[0.0], np.zeros(3), np.eye(3), (MAST_CLR - 0.01) * Z)
        hm = [x for x in C.hits_any(up, bspline=True)]
        add("%s CRAG: CRATE on Shelf 2 centre slot has >= 5.0 in of overhead clearance to the mast (§2.4)" % side,
            not hm, "raised 4.99: %s" % hm)
        up2 = _moved(over[0.0], np.zeros(3), np.eye(3), (SUMMIT_TUBE_CLR - 0.01) * Z)
        hs = sum(_clash(up2, s, True) for s in f.solids(sock))
        add("%s CRAG: Summit Socket tube >= %.2f in above a CRATE on Shelf 2 (§2.4)" % (side, SUMMIT_TUBE_CLR), hs < 1e-6,
            "raised %.2f: common %.5f (§2.4 prints 9.29)" % (SUMMIT_TUBE_CLR - 0.01, hs))
        drop = _moved(over[0.0], np.zeros(3), np.eye(3), 30.0 * Z)
        hd = sum(_clash(drop, s, True) for s in f.solids(mast) + f.solids(sock))
        add("%s CRAG: Shelf 2 centre slot is overhung by the Summit Socket/mast (no vertical drop) (§2.4)" % side,
            hd > 1e-3, "crate raised 30 in: common with mast+socket %.4f" % hd)
        clear = []
        for lat in (-15.5, 15.5):
            sky = _moved(over[lat], np.zeros(3), np.eye(3), 60.0 * Z)
            clear.append((lat, C.hits_any(sky, bspline=True)))
        add("%s CRAG: Shelf 2 outer slots open to the sky (§2.4)" % side, all(not h for _, h in clear), "%s" % clear)
        # Shelf 1 crate vs the Shelf 2 gusset floor Z 38 (1.0 in)
        sc1 = CRAG_C[side] + (HALF + SLOT_OUT) * n + (SHELF_Z[0] + rest_off) * Z
        hb = []
        for lat in SLOT_LAT:
            sh = _moved(rep["solid"], rep["c"], np.eye(3), sc1 + lat * YW + (SHELF2_GUSSET_FLOOR - (SHELF_Z[0] + CRATE_ENV) - 0.01) * Z)
            hb += C.hits_any(sh, bspline=True)
        add("%s CRAG: >= 1.0 in between a CRATE on Shelf 1 (top Z 37.0) and anything above (gusset floor 38.0) (§2.2)" % side,
            not hb, "%s" % hb[:3])


def sec_depot(f, C, add):
    rep = _crate_virtual(C)
    rest_off = rep["c"][2] - rep["lo"][2]
    cellr = C.rep("cell", (300.0, 138.0))
    cr = cellr["probe"]
    fa = None
    for a in np.linspace(5.0, 5.5, 501):                    # end of the full diameter (fine scan)
        if cr.first(cellr["c"] + [a, 0, 0], (0, 1, 0)) < CELL_D / 2 - 1e-6:
            break
        fa = a
    for side in ("BLUE", "RED"):
        n = N_SHELF[side]
        floor = Probe(K._compound(f.solids(f.find("%s CRAG BASE DEPOT floor" % side))))
        spots = {"leg -15.5": (HALF + DEPOT_CH / 2, -15.5), "leg 0": (HALF + DEPOT_CH / 2, 0.0),
                 "leg +15.5": (HALF + DEPOT_CH / 2, 15.5),
                 "square -Y": (HALF + DEPOT_CH / 2, -(HALF + DEPOT_CH / 2)), "square +Y": (HALF + DEPOT_CH / 2, HALF + DEPOT_CH / 2),
                 "arm -Y": (HALF - DEPOT_ARM / 2, -(HALF + DEPOT_CH / 2)), "arm +Y": (HALF - DEPOT_ARM / 2, HALF + DEPOT_CH / 2)}
        hits, apex, sky_sq, sky_arm, gus = [], [], [], [], []
        for nm, (out, lat) in spots.items():
            xy = CRAG_C[side] + out * n + lat * YW
            t = floor.first(np.array([xy[0], xy[1], 3.0]), (0, 0, -1))
            ftop = 3.0 - t if t is not None else float("nan")
            cen = np.array([xy[0], xy[1], ftop + rest_off])
            sh = _moved(rep["solid"], rep["c"], np.eye(3), cen)
            h = C.hits_any(sh, bspline=True)
            if h:
                hits.append((nm, h))
            apex.append((nm, round(ftop, 5), round(cen[2] + rest_off, 5)))
            if nm.startswith("square"):
                sky_sq.append((nm, C.hits_any(_moved(sh, np.zeros(3), np.eye(3), 60.0 * Z), bspline=True)))
            if nm.startswith("arm"):
                sky_arm.append((nm, sum(v for _, v in C.hits_any(_moved(sh, np.zeros(3), np.eye(3), 30.0 * Z), bspline=True))))
            if nm.startswith("leg"):
                gus += C.hits_any(_moved(sh, np.zeros(3), np.eye(3), (SHELF1_GUSSET_FLOOR - DEPOT_FLOOR - CRATE_ENV - 0.01) * Z), bspline=True)
        add("%s DEPOT: a crowned CRATE fits the leg, both corner squares and both arms (§3 piece-fit)" % side,
            not hits, "%s" % hits[:3])
        add("%s DEPOT: a CRATE on the tray floor (Z 0.25) apexes at Z 13.25, 0.19 below the tag target (§7)" % side,
            all(abs(a[1] - DEPOT_FLOOR) < 1e-6 and abs(a[2] - 13.25) < 1e-4 for a in apex)
            and abs(TARGET_BOTTOM - 13.25 - 0.19) < 0.005, "(spot, floor top, apex) %s" % apex)
        add("%s DEPOT: corner squares open to the sky for a CRATE (§3)" % side, all(not h for _, h in sky_sq), "%s" % sky_sq)
        add("%s DEPOT: a CRATE cannot be dropped into either arm from above (Low Socket overhang) (§3)" % side,
            all(v > 1e-3 for _, v in sky_arm), "%s" % sky_arm)
        add("%s DEPOT: leg CRATES clear everything above up to the Shelf 1 gusset floor (Z 19.0) (§2.2 / §3)" % side,
            not gus, "%s" % gus[:3])
        # O2 CELL stood on end in the tray (VISION-GUIDE §1.3)
        xy = CRAG_C[side] + (HALF + DEPOT_CH / 2) * n
        t = floor.first(np.array([xy[0], xy[1], 3.0]), (0, 0, -1))
        ftop = 3.0 - t
        up = _moved(cellr["solid"], cellr["c"], _basis_from(Z), np.array([xy[0], xy[1], ftop + CELL_L / 2]))
        top = Probe(up).support(np.array([xy[0], xy[1], 0.0]), (0, 0, 1), 3.0)[0]
        shoulder = ftop + CELL_L / 2 + fa
        h = C.hits_any(up)
        add("%s DEPOT: an O2 CELL on end tops out at Z 14.25 with its full diameter to Z 12.47 (VISION-GUIDE §1.3)" % side,
            abs(top - CELL_UPRIGHT_TOP) < 1e-4 and abs(shoulder - CELL_UPRIGHT_SHOULDER) < 0.01 and not h,
            "top %.4f shoulder %.4f; interference %s" % (top, shoulder, h))


def _find_parts(f, base):
    """Bodies named `base`, or, for the sided parts (pegs, side sockets), both
    base + " (guardrail side)" and base + " (centre side)"."""
    out = []
    for suf in ("", " (guardrail side)", " (centre side)"):
        try:
            out += f.find(base + suf)
        except KeyError:
            pass
    if not out:
        raise KeyError("no body named %r" % base)
    return out


def _sockets(side):
    n = N_SHELF[side]
    out = [("Summit", "Summit Socket", CRAG_C[side] + (HALF + SOCK_STANDOFF) * n + 72.0 * Z,
            _unit(math.sin(math.radians(15)) * n + math.cos(math.radians(15)) * Z))]
    for sy in (1, -1):
        for kind, zr, lat in (("Low", 30.0, 14.0), ("Mid", 54.0, -14.0)):
            rim = CRAG_C[side] + lat * n + sy * (HALF + SOCK_STANDOFF) * YW + zr * Z
            out.append(("%s %+dY" % (kind, sy), "%s Socket" % kind, rim,
                        _unit(math.sin(math.radians(30)) * sy * YW + math.cos(math.radians(30)) * Z)))
    return out


def sec_sockets(f, C, add):
    cellr = C.rep("cell", (300.0, 138.0))
    for side in ("BLUE", "RED"):
        res, hits = [], []
        for lab, nm, rim, a in _sockets(side):
            recs = _find_parts(f, "%s CRAG %s" % (side, nm))
            tube = min(recs, key=lambda r: f.dist_point([r], rim - 3.0 * a))
            pr = Probe(K._compound(tube["solids"]))
            t = pr.first(rim + 0.5 * a, -a)
            depth = t - 0.5 if t is not None else float("nan")
            perp = _unit(np.cross(a, YW if abs(a[1]) < 0.9 else np.array([1.0, 0, 0])))
            bore = pr.first(rim - 3.5 * a, perp)
            # seated cell: pole on the tube's inner floor
            R = _basis_from(a)
            cen = rim - depth * a + (CELL_L / 2) * a
            sh = _moved(cellr["solid"], cellr["c"], R, cen)
            h = C.hits_any(sh)
            if h:
                hits.append((lab, h))
            res.append((lab, round(depth, 4), round(CELL_L - depth, 4), None if bore is None else round(bore - CELL_D / 2, 4)))
        add("%s CRAG: a seated O2 CELL protrudes 7.0 in from every socket (DESIGN-SPEC §3, §9.2 / §2.3)" % side,
            len(res) == 5 and all(abs(r[2] - (CELL_L - SOCK_LEN)) < 0.005 for r in res),
            "(socket, inner depth, protrusion, radial clr) %s — DESIGN-SPEC governs: the 7.0 runs from the rim to "
            "the seat, the 0.09 closed bottom beyond it" % res)
        add("%s CRAG: O2 CELL radial clearance in every socket 0.75 +/- 0.0625 (ID 6.50 +/- 0.125) (§9.2)" % side,
            all(r[3] is not None and abs(r[3] - (SOCK_ID - CELL_D) / 2) <= SOCK_TOL / 2 for r in res), "%s" % res)
        add("%s CRAG: a seated O2 CELL interferes with nothing, in all five sockets" % side, not hits, "%s" % hits[:3])


def _pegs(side):
    npeg = -N_SHELF[side]
    u = _unit(math.cos(math.radians(45)) * npeg + math.sin(math.radians(45)) * Z)
    out = []
    for lat in (-14.0, 14.0):
        for zr, kind in ((30.0, "Low"), (54.0, "Mid")):
            out.append(("%s %+.0f" % (kind, lat), "%s Peg" % kind, CRAG_C[side] + HALF * npeg + lat * YW + zr * Z, u, npeg))
    for lat in (-7.0, 7.0):
        out.append(("High %+.0f" % lat, "High Peg", CRAG_C[side] + SPIRE_HALF * npeg + lat * YW + 78.0 * Z, u, npeg))
    return out


def sec_pegs(f, C, add):
    coil = C.rep("coil", (324.0, 138.0))
    for side in ("BLUE", "RED"):
        hits, clr = [], []
        for lab, nm, root, u, npeg in _pegs(side):
            peg = min(_find_parts(f, "%s CRAG %s" % (side, nm)), key=lambda r: f.dist_point([r], root + 2.0 * u))
            sh = _moved(coil["solid"], coil["c"], _basis_z(u), root + 6.0 * u)
            h = C.hits_any(sh)
            if h:
                hits.append((lab, h))
            clr.append((lab, round(f.dist([{"solids": [sh]}], [peg]), 5)))
        add("%s CRAG: a ROPE COIL threaded square on every peg interferes with nothing (§9.3)" % side, not hits,
            "%s" % hits[:3])
        add("%s CRAG: coil-to-peg radial clearance 1.75 (5.0 ID over 1.5 OD) on every peg (§9.3)" % side,
            all(abs(v - (COIL_ID - PEG_OD) / 2) < 1e-3 for _, v in clr), "%s" % clr)
    # §2.5 rest-pose statements against the built coil and peg (Blue +14 Low Peg)
    side = "BLUE"
    lab, nm, root, u, npeg = [p for p in _pegs(side) if p[0] == "Low +14"][0]
    peg = min(_find_parts(f, "%s CRAG %s" % (side, nm)), key=lambda r: f.dist_point([r], root + 2.0 * u))
    pegs = peg["solids"]
    lat_axis = _unit(np.cross(Z, npeg))

    def tilted(theta):
        # rotate u toward the horizontal npeg by theta about the lateral axis: 45 deg => coil plane vertical
        a = _unit(math.cos(math.radians(45 - theta)) * npeg + math.sin(math.radians(45 - theta)) * Z)
        return _moved(coil["solid"], coil["c"], _basis_z(a), root + 6.0 * u)

    # The documents disagree on the tilt at which a coil binds: §2.5 says ~47.9 deg (2.5 tan + 1.5/cos
    # <= 5.0, a flat washer with a 2.5-long bore), while the coil DESIGN-SPEC §2 locks (and §9.3
    # builds) is a torus, R 3.75 / r 1.25, which clears a centred 0.75-radius rod until the rod's
    # axis comes within 2.0 of the core circle: acos(2.0 / 3.75) = 57.8 deg.  DESIGN-SPEC governs.
    bound = math.degrees(math.acos((PEG_OD / 2 + COIL_TUBE / 2) / COIL_RC))
    vols = {th: sum(_common(tilted(th), s) for s in pegs) for th in (45.0, 50.0, 55.0, bound - 0.5, bound + 1.0)}
    add("ROPE COIL (DESIGN-SPEC torus) threaded on a built 1.5-in peg binds at acos(2.0/3.75) = %.1f deg of tilt" % bound,
        all(vols[t] < 1e-6 for t in (45.0, 50.0, 55.0, bound - 0.5)) and vols[bound + 1.0] > 1e-6,
        "common volume with the peg by tilt %s; the vertical hang (45 deg) has %.1f deg of margin.  FCP §2.5 "
        "prints ~47.9 deg and 2.9 deg of margin from a flat-washer model, which is not the DESIGN-SPEC §2 torus"
        % ({round(k, 1): round(v, 5) for k, v in vols.items()}, bound - 45))

    def vertical(h):
        cen = root + (COIL_TUBE / 2 + COIL_TUBE / 2) * npeg + h * Z      # inner face 1.25 outboard
        return _moved(coil["solid"], coil["c"], _basis_z(npeg), cen), cen

    shv, _ = vertical(1.0)
    v1 = sum(_common(shv, s) for s in pegs)
    lo, hi = 1.0, 2.5
    for _ in range(12):
        mid = (lo + hi) / 2
        if sum(_common(vertical(mid)[0], s) for s in pegs) > 1e-7:
            lo = mid
        else:
            hi = mid
    # §2.5 describes the wedged rest pose as "center roughly 1 in above the peg root and its inner face
    # about 1.25 in outboard".  For the DESIGN-SPEC torus hung plumb with its mid-plane 2.5 out, the core
    # circle keeps 2.0 (= 1.25 + 0.75) from the 45-deg peg axis only while the centre is at least
    # 2.5 - k above the root, k the root of k^2 + 7.5 k + 6.0625 = 0 (the top of the core circle is the
    # closest point): 1.578 in.  DESIGN-SPEC governs, so the built coil must wedge there.
    k = (7.5 - math.sqrt(7.5 ** 2 - 4 * 6.0625)) / 2
    h_min = 2.5 - k
    add("ROPE COIL hung plumb on a built Low Peg, inner face 1.25 outboard (§2.5), wedges with its centre %.2f in "
        "above the peg root (DESIGN-SPEC torus on a 1.5-in 45-deg peg)" % h_min,
        abs(hi - h_min) < 0.01,
        "lowest clear centre %.3f in above the root (bisection on the built bodies), want %.3f.  FCP §2.5 prints "
        "'roughly 1 in': the built coil at 1.0 shares %.4f in^3 with the peg, so that figure cannot hold for the "
        "DESIGN-SPEC torus" % (hi, h_min, v1))


def sec_gamepiece(f, C, add):
    path = os.path.join(SRC, "90_features.fs")
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    m = re.search(r'"Feature Type Name"\s*:\s*"SUMMIT PUSH Game Piece".*?\}\s*,\s*\{(.*?)\}\);', src, re.S)
    body = m.group(0) if m else ""
    okst = bool(m) and bool(re.search(r'definition\.kind\s*==\s*SpSupplyKind\.O2_CELL\)\s*kind\s*=\s*"cell"', body)) \
        and bool(re.search(r'definition\.kind\s*==\s*SpSupplyKind\.ROPE_COIL\)\s*kind\s*=\s*"coil"', body)) \
        and 'var kind = "crate"' in body and re.search(r'if \(definition\.rest\)\s*F = restFrame\(kind, 0, 0, 0\)', body) \
        and 'buildPiece(context, id + "piece", kind, F)' in body
    add("Game Piece feature maps CACHE CRATE / O2 CELL / ROPE COIL to the field's piece builder, "
        "optional rest on the Top plane", bool(okst), "90_features.fs summitPushGamePiece block %s" % ("found" if m else "NOT found"))
    ns = f.ns
    vol = {k: f.volume([C.rep(k, xy)["rec"]]) for k, xy in (("crate", (324, 162)), ("cell", (300, 138)), ("coil", (324, 138)))}
    for k in LABEL:
        for rest in (True, False):
            reg = K.Registry()
            F = ns["restFrame"](k, 0, 0, 0) if rest else ns["worldFrame"]()
            try:
                ns["buildPiece"](reg, K.Id(("GP",)) + "piece", k, F)
            except Exception as e:  # noqa: BLE001
                add("Game Piece feature builds a %s (rest=%s)" % (LABEL[k], rest), False, "%s: %s" % (type(e).__name__, e))
                continue
            recs = list(reg.bodies.values())
            s = recs[0]["solids"][0] if recs and recs[0]["solids"] else None
            pr = Probe(s)
            sup = {d: pr.support(np.zeros(3), v, 9.0)[0] for d, v in (("+x", (1, 0, 0)), ("-x", (-1, 0, 0)), ("+y", (0, 1, 0)),
                                                                     ("-y", (0, -1, 0)), ("+z", (0, 0, 1)), ("-z", (0, 0, -1)))}
            cen = [(sup["+x"] - sup["-x"]) / 2, (sup["+y"] - sup["-y"]) / 2, (sup["+z"] - sup["-z"]) / 2]
            mass = recs[0]["mat"]["density"] * K._volume(recs[0]["solids"]) * K.IN3 / K.LB if recs else 0
            placed = (abs(sup["-z"]) < 1e-6 and abs(cen[0]) < 1e-6 and abs(cen[1]) < 1e-6) if rest \
                else all(abs(v) < 1e-6 for v in cen)
            ok = (len(recs) == 1 and len(recs[0]["solids"]) == 1 and recs[0]["name"] == LABEL[k]
                  and abs(mass - LB[k]) < 1e-3 and abs(K._volume(recs[0]["solids"]) - vol[k]) < 1e-6 * vol[k] and placed
                  and (k != "cell" or len(recs[0]["faces"]) == 4))
            add("Game Piece feature: %s %s — named, %.1f lb, same solid as the field's, %s" %
                (LABEL[k], "resting on the Top plane" if rest else "centred on the origin", LB[k],
                 "bottom at Z 0, centred in XY" if rest else "centred"),
                ok, "bodies %d name %r mass %.4f lowest Z %.6f centre %s" %
                (len(recs), recs[0]["name"] if recs else None, mass, -sup["-z"], _fmt(cen, 6)))


def sec_stacked(f, C, add):
    from inspect_field import Field
    g = Field(pairs="STACKED", perimeter=False, walls=False, crags=False, headwalls=False, tags=False, decals=False,
              stock=False)
    C2 = Ctx(g)
    add("STACKED staging option: 21 staged SUPPLIES", len(C2.pieces) == 21, "%d" % len(C2.pieces))
    bad = []
    for side in ("BLUE", "RED"):
        for sy, k in CHART_B[side].items():
            ps = [p for p in C2.pieces if math.hypot(p["c"][0] - STAGE_X[side], p["c"][1] - sy) < 15.0]
            ps.sort(key=lambda p: p["c"][2])
            if len(ps) != 2 or any(p["kind"] != k for p in ps):
                bad.append((side, sy, "pieces", [(p["kind"], _fmt(p["c"], 3)) for p in ps]))
                continue
            lo_, hi_ = ps
            if any(math.hypot(p["c"][0] - STAGE_X[side], p["c"][1] - sy) > 1e-6 for p in ps):
                bad.append((side, sy, "not on the mark centre"))
            if abs(hi_["lo"][2] - lo_["hi"][2]) > 1e-6:
                bad.append((side, sy, "upper piece not resting on the lower", hi_["lo"][2] - lo_["hi"][2]))
            v = _clash(lo_["solid"], hi_["solid"], k == "crate")
            if v > 1e-6:
                bad.append((side, sy, "pair interpenetrates", v))
    add("STACKED option: each mark carries its chart (b) pair stacked on the mark centre, upper resting on lower",
        not bad, "%s" % bad)
    tape = []
    for p in C2.pieces:
        for r in C2.near(p["solid"], 0.01, exclude_pieces=True):
            v = sum(_clash(p["solid"], s, p["kind"] == "crate") for s in r["solids"])
            if v > 1e-6:
                tape.append((p["name"], r["name"], v))
    add("STACKED option: no SUPPLY interpenetrates tape", not tape, "%s" % tape[:3])


SECTIONS = (sec_inventory, sec_crate, sec_cell, sec_coil, sec_props, sec_staging, sec_rest, sec_interference,
            sec_extent, sec_shelves, sec_depot, sec_sockets, sec_pegs, sec_gamepiece, sec_stacked)


def run(f):
    out = []

    def add(label, ok, detail):
        out.append((label, bool(ok), detail))

    C = Ctx(f)
    for sec in SECTIONS:
        try:
            sec(f, C, add)
        except Exception as e:  # noqa: BLE001
            import traceback
            add("%s completed" % sec.__name__, False, "%s: %s | %s" % (type(e).__name__, e,
                                                                     traceback.format_exc().splitlines()[-3:]))
    return out
