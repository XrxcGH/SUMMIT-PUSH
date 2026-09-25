# -*- coding: utf-8 -*-
"""
OUTFITTER chutes — independent checks of the four chute openings, ramps, cheek funnels, the
OUTFITTER AprilTag panels and the OUTFITTER LANE tape.

Every expected value below is taken from the package documents, never from src/:

  FIELD-CAD-PACKAGE.md  §0 (frame, angle rule, (ref) = +/-0.25), §1.1 (chute centres),
                        §1.2 (OUTFITTER LANE tape), §1.3 (alliance wall 78 x 2.0, solid to 39),
                        §5 (opening, sill, ramp, cheeks, tag, piece-pass), §7 (tags 1/2/14/15),
                        §9 (piece envelopes), §10 row 12-14
  02-manual 02-arena.md §3.2 (lane coordinates, tape is part of its zone), §3.5, §3.7
  MATERIALS-AND-COLORS  §1 palette, §2 (ramp UHMW-faced plywood 0.5, cheek painted plywood 0.5,
                        lower wall plywood 0.75, glazing 0.25 @ 25 %, tape 2 x 0.01, tag panel)
  participants/04-vision/apriltag-field-layout.json (tag poses)

Construction reading (the generator's documented design; §5 marks all behind-wall geometry (ref)):
  * a throat liner "<A> OUTFITTER n chute throat" (sill, two jambs, head; one body) lines the
    30 x 16 opening through the 2.0-in wall depth, so the wall is 2.0 thick at the chute;
  * the 30-deg ramp "<A> OUTFITTER n chute ramp" starts at the back of the throat (x = -2.0) and is
    40 in along the slope; plumb cheeks "... cheek 1/2" run on its side edges; 45-deg funnel wings
    "... funnel wing 1/2" open the funnel from the 30-in ramp to 36 in at the loading end; a leg
    "... ramp leg" carries the loading end;
  * each OUTFITTER LANE is one welded U-shaped tape body "<A> OUTFITTER LANE n tape".

The chute path is checked with a 2-D envelope sweep (all obstacles are taken as the worst case
over the piece's lateral extent, measured on the built model by ray casting) plus 3-D spot checks
of the worst poses with the real piece bodies.
"""
import json
import math
import os

import numpy as np

import kernel_occ as K
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus
from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector
from OCP.gp import gp_Ax2, gp_Dir, gp_Lin, gp_Pnt, gp_Trsf, gp_Vec
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

# ---------------------------------------------------------------------------------------
# Expected values (documents only)
# ---------------------------------------------------------------------------------------
FIELD_L, FIELD_W = 648.0, 324.0                       # §0
REF = 0.25                                            # §0: (ref) may float +/-0.25
OPEN_W, OPEN_H, SILL = 30.0, 16.0, 24.0               # §5 CRITICAL, manual §3.5
HEAD = SILL + OPEN_H                                  # 40  ("spans Z 24-40")
SILL_R = 0.5                                          # §5 (ref)
WALL_T, WALL_H, WALL_SOLID = 2.0, 78.0, 39.0          # §1.3 (ref) / §5 "wall thickness at the chute 2.0 (ref)"
PANEL_T, GLAZE_T = 0.75, 0.25                         # MATERIALS §2
RAMP_ANG, RAMP_W, RAMP_RUN, FLARE_W = 30.0, 30.0, 40.0, 36.0   # §5 (ref)
RAMP_T, CHEEK_T = 0.5, 0.5                            # MATERIALS §2
TAG_Z, TAG_PANEL, TAG_PANEL_T, TAG_TARGET = 52.0, 9.0, 0.25, 8.125  # §5, §7
LANE_W, LANE_D, TAPE_W, TAPE_T = 36.0, 48.0, 2.0, 0.01  # §1.2, manual §3.2, MATERIALS §2
CRATE_ENV, CRATE_CUBE, CRATE_CROWN, CRATE_FIL = 13.0, 12.0, 0.5, 1.0   # §9.1
CELL_D, CELL_L = 5.0, 14.0                            # §9.2
COIL_OD, COIL_TUBE = 10.0, 2.5                        # §9.3
STOCK_PER_TYPE = 7                                    # §6 (c), manual §3.6.1

# (alliance, world Y of the chute centre, tag ID)   — §1.1, §5, §7
CHUTES = [("BLUE", 30.0, 1), ("BLUE", 294.0, 2), ("RED", 294.0, 14), ("RED", 30.0, 15)]

HEX = {"wall": "#9AA4B2", "glazing": "#DCE8FA", "alliance-blue": "#1D63C8", "alliance-red": "#CC3333",
       "neutral-white": "#F5F5F5", "tag-black": "#111111"}


def rgb(tok):
    h = HEX[tok].lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PIECE_PREFIX = ("CACHE CRATE", "O2 CELL", "ROPE COIL")


# ---------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------
def local_frame(f, side):
    """Alliance-local frame built from §0/§1.1: x into the field from that alliance's wall,
    z up; Red is Blue rotated 180 deg about (324, 162)."""
    if side == "BLUE":
        return f.frame((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
    return f.frame((FIELD_L, FIELD_W, 0.0), (-1.0, 0.0, 0.0), (0.0, 0.0, 1.0))


def local_c(side, Y):
    return Y if side == "BLUE" else FIELD_W - Y


class Rays:
    def __init__(self, solids):
        self.it = IntCurvesFace_ShapeIntersector()
        self.it.Load(K._compound(solids), 1e-7)

    def first(self, p, d, tmax=500.0):
        self.it.Perform(gp_Lin(gp_Pnt(*map(float, p)), gp_Dir(*map(float, d))), 0.0, tmax)
        if not self.it.IsDone() or self.it.NbPnt() == 0:
            return None
        return min(self.it.WParameter(i) for i in range(1, self.it.NbPnt() + 1))


def fast_bbox(solids):
    b = K.Bnd_Box()
    for s in solids:
        K.BRepBndLib.Add_s(s, b, False)
    return K._box6(b)


def shape_dist(shape, solids):
    if not solids:
        return float("inf")
    return BRepExtrema_DistShapeShape(shape, K._compound(solids)).Value()


def rec(shape):
    return {"solids": K._solids(shape) or [shape]}


def bb_overlap(a, b, pad=0.0):
    return all(a[i] - pad <= b[i + 3] and b[i] - pad <= a[i + 3] for i in range(3))


def angle_ok(a, tol=0.05):
    """§0: every angle on the field is 15, 30 or 45 deg (0/90 and their complements included)."""
    a = abs(a) % 90.0
    return min(abs(a - k) for k in (0, 15, 30, 45, 60, 75, 90)) <= tol


def mesh_pts(shape, defl=0.01):
    BRepMesh_IncrementalMesh(shape, defl, False, 0.1, True)
    pts = []
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        fc = TopoDS.Face(exp.Current())
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(fc, loc)
        if tri is not None:
            tr = loc.Transformation()
            for i in range(1, tri.NbNodes() + 1):
                p = tri.Node(i).Transformed(tr)
                pts.append((p.X(), p.Y(), p.Z()))
        exp.Next()
    return np.array(pts)


def densify(loop, step=0.02):
    out = []
    n = len(loop)
    for i in range(n):
        a = np.asarray(loop[i], float)
        b = np.asarray(loop[(i + 1) % n], float)
        k = max(1, int(math.ceil(np.linalg.norm(b - a) / step)))
        for t in np.arange(k) / k:
            out.append(a + (b - a) * t)
    return np.array(out)


def hull2d(P):
    P = sorted(set(map(tuple, np.round(np.asarray(P, float), 6))))

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def clip_halfplane(poly, n, d):
    """Keep the part of convex polygon `poly` with n.p <= d."""
    out = []
    m = len(poly)
    for i in range(m):
        a, b = np.asarray(poly[i]), np.asarray(poly[(i + 1) % m])
        fa, fb = n @ a - d, n @ b - d
        if fa <= 0:
            out.append(a)
        if fa * fb < 0:
            out.append(a + (b - a) * (fa / (fa - fb)))
    return out


def crate_section_doc():
    """Mid-plane (maximum) section of the CACHE CRATE from §9.1: 12.0 cube, 0.5 face crown that
    is parabolic across the face (it gives the 12.44 width at 1.5 in from the edge the section
    quotes), 1.0 edge fillets.  Convex, so the fillets are an erosion/dilation by R = 1.0."""
    h, cr_, R = CRATE_CUBE / 2, CRATE_CROWN, CRATE_FIL
    a = np.linspace(-h, h, 121)
    bulge = h + cr_ * (1 - (a / h) ** 2)
    pts = np.concatenate([np.c_[bulge, a], np.c_[-bulge, a], np.c_[a, bulge], np.c_[a, -bulge]])
    poly = [np.array(p) for p in hull2d(pts)]
    er = poly
    m = len(poly)
    for i in range(m):
        p0, p1 = poly[i], poly[(i + 1) % m]
        t = p1 - p0
        if np.linalg.norm(t) < 1e-12:
            continue
        n = np.array([t[1], -t[0]]) / np.linalg.norm(t)      # outward for a CCW hull
        er = clip_halfplane(er, n, n @ p0 - R)
    th = np.linspace(0, 2 * math.pi, 181)[:-1]
    dil = [p + R * np.array([math.cos(t), math.sin(t)]) for p in er for t in th]
    return densify(hull2d(dil))


def stadium(half_len, r):
    th = np.linspace(-math.pi / 2, math.pi / 2, 61)
    right = [(half_len - r + r * math.cos(t), r * math.sin(t)) for t in th]
    left = [(-(half_len - r) - r * math.cos(t), -r * math.sin(t)) for t in th]
    return densify(right + left)


def disk(r):
    th = np.linspace(0, 2 * math.pi, 721)[:-1]
    return np.c_[r * np.cos(th), r * np.sin(th)]


def rect(w, h):
    return densify([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)])


# doc-derived 2-D projections (x along the chute travel, z along the piece's own "up")
PIECES_2D = {
    "CACHE CRATE (12 cube, 0.5 crown, R1 fillets)": (crate_section_doc, 6.5),
    "O2 CELL end-on (axis along the travel, 14 x 5 envelope)": (lambda: rect(CELL_L, CELL_D), 2.5),
    "O2 CELL lengthwise (axis across the chute, rolling)": (lambda: disk(CELL_D / 2), 7.0),
    "ROPE COIL flat": (lambda: stadium(COIL_OD / 2, COIL_TUBE / 2), 5.0),
    "ROPE COIL on edge (rolling)": (lambda: disk(COIL_OD / 2), 1.25),
}


_HULLS = {}


def rot2(v, deg):
    """Nose-down rotation (toward +x) in the (x, z) plane."""
    s, c = math.sin(math.radians(deg)), math.cos(math.radians(deg))
    return np.array([v[0] * c + v[1] * s, -v[0] * s + v[1] * c])


# ---------------------------------------------------------------------------------------
# the checks
# ---------------------------------------------------------------------------------------
def run(f):
    out = []

    def chk(label, ok, detail):
        out.append((label, bool(ok), detail))

    def near(label, got, want, tol, extra=""):
        ok = got is not None and abs(got - want) <= tol
        chk(label, ok, "got %s want %.4f +/- %g%s" % ("None" if got is None else "%.4f" % got, want, tol, extra))

    recs = f.records()
    nonpiece = [r for r in recs if not (r["name"] or "").startswith(PIECE_PREFIX)]
    wbox = {id(r): fast_bbox(r["solids"]) for r in recs}      # loose boxes, for candidate filtering only

    def fx(rx):
        try:
            return f.find("re:" + rx)
        except KeyError:
            return []

    # chute part names (§5 construction reading above)
    RX = {"ramp": r"^%s OUTFITTER \d+ chute ramp$", "throat": r"^%s OUTFITTER \d+ chute throat$",
          "cheek": r"^%s OUTFITTER \d+ cheek \d+$", "wing": r"^%s OUTFITTER \d+ funnel wing \d+$",
          "leg": r"^%s OUTFITTER \d+ ramp leg$", "lane": r"^%s OUTFITTER LANE \d+ tape$"}

    def near_y(rs, Y, tol):
        return [r for r in rs if abs((wbox[id(r)][1] + wbox[id(r)][4]) / 2 - Y) < tol]

    # ---- counts ---------------------------------------------------------------------------
    for side in ("BLUE", "RED"):
        got = {k: fx(v % side) for k, v in RX.items()}
        n = {k: len(v) for k, v in got.items()}
        ns = {k: sum(len(r["solids"]) for r in v) for k, v in got.items()}
        chk("%s: 2 chute throats, 2 ramps, 4 cheek plates, 4 funnel wings, 2 legs, 2 OUTFITTER LANES (§5 x4 stations), "
            "one solid each" % side,
            n == {"ramp": 2, "throat": 2, "cheek": 4, "wing": 4, "leg": 2, "lane": 2} and ns == n,
            "bodies %s, solids %s" % (n, ns))

    ceil_rows = []
    wall_depths = []
    flare_rows = []
    run_rows = []
    sweep_rows = {}
    level_rows = []
    worst3d = {}
    envelope_tip = []

    crate_real = f.find(r"re:^CACHE CRATE - CENTER CACHE")[0]["solids"][0]
    M = mesh_pts(crate_real)
    crate_ctr = (M.max(0) + M.min(0)) / 2

    for side, Y, tid in CHUTES:
        F = local_frame(f, side)
        c = local_c(side, Y)
        P = lambda x, y, z: F.pt((x, y, z))         # noqa: E731
        D = lambda x, y, z: F.dir((x, y, z))        # noqa: E731
        tag = "%s chute (%g, %g)" % (side, 0.0 if side == "BLUE" else FIELD_L, Y)

        panel = f.find("%s alliance wall lower panel" % side)
        glaze = f.find("%s alliance wall glazing" % side)
        frame = f.find("%s alliance wall frame" % side)
        wall = panel + glaze
        rw = Rays(f.solids(wall))
        throat = near_y(fx(RX["throat"] % side), Y, 5)
        rwt = Rays(f.solids(wall + throat))

        # ---- A. opening (CRITICAL) ----------------------------------------------------------
        for dy in (0.0, -14.0, 14.0):
            h = rw.first(P(-0.6, c + dy, 35.0), D(0, 0, -1))
            near("%s: sill Z at y%+g (flat part behind the R%.1f roundover)" % (tag, dy, SILL_R),
                 None if h is None else 35.0 - h, SILL, 0.001)
            h = rw.first(P(-0.1, c + dy, 30.0), D(0, 0, 1))
            near("%s: opening head Z at y%+g" % (tag, dy), None if h is None else 30.0 + h, HEAD, 0.001)
        jl = rw.first(P(-0.1, c, 32.0), D(0, -1, 0))
        jh = rw.first(P(-0.1, c, 32.0), D(0, 1, 0))
        jl2 = rw.first(P(-0.1, c, 39.5), D(0, -1, 0))
        jh2 = rw.first(P(-0.1, c, 39.5), D(0, 1, 0))
        near("%s: opening width in the solid panel (Z 32)" % tag, (jl or 0) + (jh or 0), OPEN_W, 0.001)
        near("%s: opening width in the glazed band (Z 39.5)" % tag, (jl2 or 0) + (jh2 or 0), OPEN_W, 0.001)
        yc_loc = c + ((jh or 0) - (jl or 0)) / 2
        # field-side wall plane: ray from the field toward the wall below the sill
        hx = rw.first(P(5.0, c, 20.0), D(-1, 0, 0))
        xplane = 5.0 - hx if hx is not None else None
        ctr_w = F.pt((xplane or 0.0, yc_loc, (SILL + HEAD) / 2))
        want_x = 0.0 if side == "BLUE" else FIELD_L
        chk("%s: opening centre (world) = (%g, %g), Z 24-40, in the field-side wall plane" % (tag, want_x, Y),
            xplane is not None and abs(ctr_w[0] - want_x) < 1e-3 and abs(ctr_w[1] - Y) < 1e-3 and abs(xplane) < 1e-3,
            "measured centre (%.4f, %.4f, %.2f)" % tuple(ctr_w))
        # bounded exactly: material just outside every edge, none just inside
        probes_in = [(-0.6, c, SILL - 0.05), (-0.1, c, HEAD + 0.05), (-0.1, c - 15.05, 32.0), (-0.1, c + 15.05, 32.0),
                     (-0.1, c - 15.05, 39.5), (-0.1, c + 15.05, 39.5)]
        probes_out = [(-0.6, c, SILL + 0.05), (-0.1, c, HEAD - 0.05), (-0.1, c - 14.95, 32.0), (-0.1, c + 14.95, 32.0),
                      (-0.6, c - 14.95, SILL + 0.05), (-0.1, c + 14.95, HEAD - 0.05)]
        bad = [p for p in probes_in if not f.inside(wall, P(*p))] + [p for p in probes_out if f.inside(wall, P(*p))]
        chk("%s: opening is exactly 30 x 16 (wall present 0.05 outside each edge, absent 0.05 inside)" % tag,
            not bad, "bad probes %s" % bad)
        # ... and stays exactly 30 x 16 through the 2.0-in wall depth: behind the panel the
        # throat liner bounds it (probes at x = -1.0 / -1.4 / -1.9)
        bad = []
        for xd in (-1.0, -1.4, -1.9):
            pin = [(xd, c, SILL - 0.05), (xd, c, HEAD + 0.05), (xd, c - 15.05, 32.0), (xd, c + 15.05, 32.0),
                   (xd, c - 15.05, 39.5), (xd, c + 15.05, 39.5)]
            pout = [(xd, c, SILL + 0.05), (xd, c, HEAD - 0.05), (xd, c - 14.95, 32.0), (xd, c + 14.95, 32.0),
                    (xd, c - 14.95, SILL + 0.05), (xd, c + 14.95, HEAD - 0.05)]
            bad += [p for p in pin if not f.inside(wall + throat, P(*p))] + [p for p in pout if f.inside(wall + throat, P(*p))]
        chk("%s: opening is exactly 30 x 16 through the 2.0-in wall depth (throat liner flush with the opening)" % tag,
            len(throat) == 1 and not bad, "throat bodies %d; bad probes %s" % (len(throat), bad[:6]))
        for xd in (-1.0, -1.9):
            h = rwt.first(P(xd, c, 35.0), D(0, 0, -1))
            near("%s: sill Z at x %g (throat sill, flush with the panel sill)" % (tag, xd), None if h is None else 35.0 - h, SILL, 0.001)
            h = rwt.first(P(xd, c, 30.0), D(0, 0, 1))
            near("%s: opening head Z at x %g (throat head)" % (tag, xd), None if h is None else 30.0 + h, HEAD, 0.001)
            a_ = rwt.first(P(xd, c, 32.0), D(0, -1, 0))
            b_ = rwt.first(P(xd, c, 32.0), D(0, 1, 0))
            near("%s: opening width at x %g (throat jambs)" % (tag, xd), None if a_ is None or b_ is None else a_ + b_, OPEN_W, 0.001)
        # the window through the full 2.0-in wall depth is clear of every body
        wf = K.Frame(P(-WALL_T, c - OPEN_W / 2 + 0.01, SILL + 0.01), D(1, 0, 0), D(0, 0, 1))
        box = BRepPrimAPI_MakeBox(WALL_T, OPEN_W - 0.02, OPEN_H - 0.02).Shape()
        win = K.BRepBuilderAPI_Transform(box, wf.trsf(), True).Shape()
        wbb = f.bbox([rec(win)])
        cands = [r for r in recs if bb_overlap(wbox[id(r)], wbb)]
        cv = f.common_volume([rec(win)], cands) if cands else 0.0
        chk("%s: 30 x 16 window through the full 2.0-in wall depth is empty" % tag, cv < 1e-6,
            "common volume %.6f in^3 with %s" % (cv, sorted({r["name"] for r in cands})))
        # throat liner: one aluminium-lined body inside the wall depth, joined to panel and glazing
        if throat:
            tbb = f.bbox(throat, F)
            cvt = f.common_volume(throat, wall + frame)
            dtp, dtg = f.dist(throat, panel), f.dist(throat, glaze)
            chk("%s: chute throat liner within the 2.0-in wall (x -2.0..-0.25, behind the 0.25 glazing), touches panel "
                "and glazing, no overlap with panel/glazing/frame" % tag,
                abs(tbb[0] + WALL_T) < 1e-3 and abs(tbb[3] + GLAZE_T) < 1e-3 and cvt < 1e-6 and dtp < 1e-6 and dtg < 1e-6,
                "local x %.4f..%.4f; common %.6f; gap to panel %.4f, glazing %.4f" % (tbb[0], tbb[3], cvt, dtp, dtg))
            chk("%s: chute throat liner styled as wall structure (`wall`, opaque)" % tag,
                throat[0]["rgb"] == rgb("wall") and throat[0]["alpha"] == 1,
                "rgb %s alpha %s mat %s" % (throat[0]["rgb"], throat[0]["alpha"], throat[0]["mat"]["name"]))
        # sill roundover radius (ref 0.5): fit z(x) of the field-side edge
        xs_f = np.linspace(-0.45, -0.02, 12)
        zs_f = []
        for x in xs_f:
            h = rw.first(P(x, c, 35.0), D(0, 0, -1))
            zs_f.append(35.0 - h)
        zs_f = np.array(zs_f)
        best = None
        for R in np.arange(0.05, 1.5, 0.0005):
            zz = (SILL - R) + np.sqrt(np.clip(R * R - (xs_f + R) ** 2, 0, None))
            m = (xs_f > -R)
            err = np.max(np.abs(np.where(m, zz, SILL) - zs_f))
            if best is None or err < best[1]:
                best = (R, err)
        near("%s: sill field-side edge radius (ref)" % tag, best[0], SILL_R, REF, " (fit residual %.4f)" % best[1])
        # wall depth at the chute: the material bounding the opening 0.1 in outside the sill,
        # the head and both jambs (Z 32), walked from the field face through every solid layer
        # contiguous with it (panel / glazing / frame / throat liner).  Measured from the
        # field-side plane x = 0; the sill entry lies on the R0.5 roundover, which is allowed.
        hs = []
        wtf = wall + frame + throat
        rwf = Rays(f.solids(wtf))
        for (yy, z) in ((c, SILL - 0.1), (c, HEAD + 0.1), (c - OPEN_W / 2 - 0.1, 32.0), (c + OPEN_W / 2 + 0.1, 32.0)):
            e = rwf.first(P(0.5, yy, z), D(-1, 0, 0))
            if e is None or 0.5 - e < -SILL_R - 1e-3:
                hs.append(float("nan"))
                continue
            x_in = 0.5 - e
            # walk through every solid layer that is contiguous with the field face
            x = x_in
            while True:
                ex = rwf.first(P(x - 1e-4, yy, z), D(-1, 0, 0))
                if ex is None:
                    break
                x = x - 1e-4 - ex
                if not f.inside(wtf, P(x - 1e-3, yy, z)):
                    break
            hs.append(0.0 - x)
        wall_depths.append((tag, hs))
        env = f.bbox(wall + frame, F)
        near("%s: alliance wall envelope depth (ref 2.0) and height 78" % tag, env[3] - env[0], WALL_T, REF,
             ", height %.3f" % (env[5] - env[2]))

        # ---- B. OUTFITTER tag ------------------------------------------------------------------
        trs = f.find(r"re:^AprilTag %d - " % tid)
        tb = f.bbox(trs, F)
        near("%s: tag %d centre Z" % (tag, tid), (tb[2] + tb[5]) / 2, TAG_Z, 0.001)
        near("%s: tag %d centred above the measured opening centre (local y)" % (tag, tid), (tb[1] + tb[4]) / 2, yc_loc, 0.001)
        near("%s: tag %d field face in the field-side wall plane" % (tag, tid), tb[3], 0.0, 0.001)
        chk("%s: tag %d panel 9.0 sq x 0.25, plumb and square to the wall (extent is exact)" % (tag, tid),
            abs(tb[4] - tb[1] - TAG_PANEL) < 1e-3 and abs(tb[5] - tb[2] - TAG_PANEL) < 1e-3 and abs(tb[3] - tb[0] - TAG_PANEL_T) < 1e-3,
            "extent x %.4f y %.4f z %.4f" % (tb[3] - tb[0], tb[4] - tb[1], tb[5] - tb[2]))
        near("%s: tag %d bottom clears the opening head (doc 7.50)" % (tag, tid), tb[2] - HEAD, 7.5, 0.001)
        dec = trs[0].get("decal")
        nrm = np.array(dec["normal"]) if dec else None
        facing = F.dir((1, 0, 0))
        right = np.cross(-facing, np.array([0.0, 0.0, 1.0]))
        chk("%s: tag %d decal on the field face, normal %s, not mirrored, 10 x 0.8125 = 8.125 target" % (tag, tid, "+X" if side == "BLUE" else "-X"),
            dec is not None and np.allclose(nrm, facing, atol=1e-9) and np.allclose(dec["x"], right, atol=1e-9)
            and abs(F.to_local(dec["origin"])[0]) < 1e-6 and abs(dec["cells"] * dec["s"] - TAG_TARGET) < 1e-9,
            "decal %s" % ({k: v for k, v in dec.items() if k != "black"} if dec else None))
        chk("%s: tag %d colour neutral-white #F5F5F5, opaque" % (tag, tid), trs[0]["rgb"] == rgb("neutral-white") and trs[0]["alpha"] == 1,
            "rgb %s alpha %s" % (trs[0]["rgb"], trs[0]["alpha"]))
        cvg = f.common_volume(trs, glaze)
        chk("%s: tag %d sits in a glazing pocket (no overlap with the glazing)" % (tag, tid), cvg < 1e-6, "common %.6f" % cvg)
        # unobstructed from the field: nothing in front of the 8.125 target out to 120 in
        pf = K.Frame(P(0.001, c - TAG_TARGET / 2, TAG_Z - TAG_TARGET / 2), D(1, 0, 0), D(0, 0, 1))
        pb = K.BRepBuilderAPI_Transform(BRepPrimAPI_MakeBox(120.0, TAG_TARGET, TAG_TARGET).Shape(), pf.trsf(), True).Shape()
        pbb = f.bbox([rec(pb)])
        cands = [r for r in recs if bb_overlap(wbox[id(r)], pbb)]
        cvp = f.common_volume([rec(pb)], cands) if cands else 0.0
        chk("%s: tag %d target unobstructed from the field (120-in sight box)" % (tag, tid), cvp < 1e-6,
            "common %.6f with %s" % (cvp, sorted({r["name"] for r in cands})))
        # JSON layout
        lay = json.load(open(os.path.join(REPO, "participants", "04-vision", "apriltag-field-layout.json")))
        jt = [t for t in lay["tags"] if t["ID"] == tid][0]
        tr = jt["pose"]["translation"]
        q = jt["pose"]["rotation"]["quaternion"]
        yaw = math.degrees(2 * math.atan2(q["Z"], q["W"])) % 360
        fc = F.pt(((tb[0] + tb[3]) / 2 + TAG_PANEL_T / 2, (tb[1] + tb[4]) / 2, (tb[2] + tb[5]) / 2))
        jv = np.array([tr["x"], tr["y"], tr["z"]]) / 0.0254
        want_yaw = 0.0 if side == "BLUE" else 180.0
        chk("%s: tag %d face centre and yaw match apriltag-field-layout.json" % (tag, tid),
            np.allclose(fc, jv, atol=1e-3) and abs(yaw - want_yaw) < 1e-6 and np.allclose(facing, [math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0], atol=1e-9),
            "model %s json %s yaw %.3f" % (np.round(fc, 4), np.round(jv, 4), yaw))

        # ---- C. ramp ------------------------------------------------------------------------
        ramp = near_y(fx(RX["ramp"] % side), Y, 5)
        cheeks = near_y(fx(RX["cheek"] % side), Y, 25)
        wings = near_y(fx(RX["wing"] % side), Y, 25)
        legs = near_y(fx(RX["leg"] % side), Y, 25)
        chk("%s: one ramp, two cheek plates, two funnel wings, one leg, one throat found" % tag,
            len(ramp) == 1 and sum(len(r["solids"]) for r in cheeks) == 2 and sum(len(r["solids"]) for r in wings) == 2
            and len(legs) == 1 and len(throat) == 1,
            "ramp %d cheeks %d wings %d legs %d throat %d" % (len(ramp), sum(len(r["solids"]) for r in cheeks),
                                                              sum(len(r["solids"]) for r in wings), len(legs), len(throat)))
        rr = Rays(f.solids(ramp))
        rb = f.bbox(ramp, F)
        sb_all = f.bbox(ramp + cheeks + wings + legs + throat, F)
        chk("%s: throat, ramp, cheeks, funnel wings and leg are entirely behind the field-side wall plane" % tag, sb_all[3] <= 1e-6,
            "local x max %.4f" % sb_all[3])
        pts = []
        for x in np.linspace(rb[0] + 1.0, rb[3] - 0.05, 9):
            for dy in (-10.0, 0.0, 10.0):
                h = rr.first(P(x, c + dy, 90.0), D(0, 0, -1))
                if h is not None:
                    pts.append((x, dy, 90.0 - h))
        pts = np.array(pts)
        A = np.c_[pts[:, 0], pts[:, 1], np.ones(len(pts))]
        coef, *_ = np.linalg.lstsq(A, pts[:, 2], rcond=None)
        resid = np.max(np.abs(A @ coef - pts[:, 2]))
        slope = math.degrees(math.atan(-coef[0]))
        near("%s: ramp top slope from horizontal (ref 30, angle rule)" % tag, slope, RAMP_ANG, 0.05,
             ", cross-slope %.5f, planarity %.5f" % (coef[1], resid))
        chk("%s: ramp top is one plane, level across the chute (smooth, no cross-slope)" % tag,
            resid < 1e-4 and abs(coef[1]) < 1e-6, "residual %.6f, dz/dy %.2e" % (resid, coef[1]))
        # lower end meets the sill without a step
        x_lo = rb[3]
        z_lo = coef[0] * x_lo + coef[2]
        near("%s: ramp top meets the sill at Z 24 (no step)" % tag, z_lo, SILL, 0.01, " at local x %.4f" % x_lo)
        # the sill runs level through the wall: panel sill, then the throat's sill plate (both
        # top at Z 24, checked above), then the ramp from the back of the 2.0-in wall
        hb = rwt.first(P(-5.0, c, SILL - 0.1), D(1, 0, 0))
        x_back = None if hb is None else -5.0 + hb
        chk("%s: ramp lower edge abuts the back of the sill through the wall (throat sill back face, no gap)" % tag,
            x_back is not None and abs(x_lo - x_back) < 0.01,
            "ramp lower edge at local x %.4f, back of the sill at %s" % (x_lo, "None" if x_back is None else "%.4f" % x_back))
        near("%s: sill depth through the wall = wall thickness at the chute (2.0, ref)" % tag,
             None if x_back is None else -x_back, WALL_T, REF)
        dts = f.dist(ramp, throat) if throat else float("inf")
        chk("%s: ramp touches the throat sill (gap <= 0.01)" % tag, dts <= 0.01, "ramp-throat distance %.4f" % dts)
        if x_back is None:
            x_back = x_lo
        # extents: width at the sill end, run, rise, thickness
        def ramp_width(x):
            zt = coef[0] * x + coef[2]
            a = rr.first(P(x, c - 40, zt - 0.05), D(0, 1, 0))
            b = rr.first(P(x, c + 40, zt - 0.05), D(0, -1, 0))
            return None if a is None or b is None else ((c + 40 - b) - (c - 40 + a), (c - 40 + a + c + 40 - b) / 2)
        w0 = ramp_width(x_lo - 0.1)
        near("%s: ramp width at the sill end (30, ref)" % tag, w0[0] if w0 else None, RAMP_W, REF)
        near("%s: ramp centred on the chute" % tag, w0[1] if w0 else None, c, 0.001)
        # top-surface extent along x (loading end = last x with a hit at the top-surface height)
        xt = x_lo
        for x in np.arange(x_lo, -80, -0.01):
            h = rr.first(P(x, c, coef[0] * x + coef[2] + 0.02), D(0, 0, -1), 0.04)
            if h is None:
                break
            xt = x
        run_h = x_lo - xt
        rise = (coef[0] * xt + coef[2]) - z_lo
        slope_len = math.hypot(run_h, rise)
        run_rows.append((tag, run_h, slope_len, rise, coef[0] * xt + coef[2]))
        chk("%s: ramp run 40 (ref; horizontal run or length along the slope)" % tag,
            abs(run_h - RAMP_RUN) <= REF or abs(slope_len - RAMP_RUN) <= REF,
            "horizontal run %.3f, along-slope %.3f, rise %.3f, loading end at Z %.3f" % (run_h, slope_len, rise, coef[0] * xt + coef[2]))
        # thickness normal to the slope
        n_up = np.array([math.sin(math.radians(slope)), 0.0, math.cos(math.radians(slope))])
        x_m = (x_lo + xt) / 2
        p_top = np.array([x_m, c, coef[0] * x_m + coef[2]]) + n_up * 0.01
        h1 = rr.first(P(*p_top), D(*(-n_up)))
        tpts = p_top - n_up * (h1 + 0.001)
        h2 = rr.first(P(*tpts), D(*(-n_up)))
        tk = None if h2 is None else h2 + 0.001
        near("%s: ramp thickness normal to the slope (MATERIALS 0.5)" % tag, tk, RAMP_T, 0.002)
        chk("%s: ramp appearance wall #9AA4B2, UHMW-faced plywood" % tag,
            ramp[0]["rgb"] == rgb("wall") and ramp[0]["alpha"] == 1 and "UHMW" in ramp[0]["mat"]["name"],
            "rgb %s alpha %s mat %s" % (ramp[0]["rgb"], ramp[0]["alpha"], ramp[0]["mat"]["name"]))

        # ---- D. cheeks and funnel wings ------------------------------------------------------
        # §5 "side cheek funnels flaring to 36 in at the loading end" (ref): plumb cheek plates on
        # the ramp's side edges (30 inner, the ramp width) and two 45-deg funnel wings behind the
        # ramp's loading end that open the funnel to 36 at its mouth.
        fun = cheeks + wings
        rc = Rays(f.solids(fun))
        cb = f.bbox(cheeks, F)

        def zr(x, zoff):
            """zoff above the ramp top (held at the loading-end height beyond the ramp)."""
            return coef[0] * max(x, xt) + coef[2] + zoff

        def inner(x, zoff=3.0):
            zt = zr(x, zoff)
            a = rc.first(P(x, c, zt), D(0, -1, 0))
            b = rc.first(P(x, c, zt), D(0, 1, 0))
            return None if a is None or b is None else (c - a, c + b)

        def ythick(x, y_in, sgn, zoff=3.0):
            """y-thickness of the plate whose inner face is at y_in (sgn = side)."""
            zt = zr(x, zoff)
            h = rc.first(P(x, y_in + sgn * 1e-4, zt), D(0, sgn, 0))
            return None if h is None else h + 1e-4

        # cheeks: plumb, parallel, 30 inner along the ramp run, from the throat to the loading end
        x_beg = cb[3] - 0.5
        x_end = xt + 0.02
        ib, ie = inner(x_beg), inner(x_end)
        near("%s: cheek inner width at the sill end (= 30 opening and ramp width, ref)" % tag,
             None if ib is None else ib[1] - ib[0], RAMP_W, REF)
        near("%s: cheek inner width at the ramp's loading end (cheeks run on the ramp edges, ref 30)" % tag,
             None if ie is None else ie[1] - ie[0], RAMP_W, REF)
        chk("%s: cheeks symmetric about the chute centre" % tag,
            ib is not None and ie is not None and abs((ib[0] + ib[1]) / 2 - c) < 1e-3 and abs((ie[0] + ie[1]) / 2 - c) < 1e-3,
            "mid %s / %s vs %.4f" % (None if ib is None else round((ib[0] + ib[1]) / 2, 4),
                                     None if ie is None else round((ie[0] + ie[1]) / 2, 4), c))
        im_lo, im_hi = inner(x_m, 3.0), inner(x_m, 7.0)
        chk("%s: cheek plates plumb (same inner width 3 in and 7 in above the ramp)" % tag,
            im_lo is not None and im_hi is not None and abs((im_lo[1] - im_lo[0]) - (im_hi[1] - im_hi[0])) < 1e-3,
            "%s vs %s" % (im_lo, im_hi))
        cheek_deg = None
        if ib and ie:
            cheek_deg = math.degrees(math.atan2(abs(ib[1] - ie[1]), abs(x_beg - x_end)))
        tk_c = None if im_lo is None else ythick(x_m, im_lo[1], 1)
        near("%s: cheek plate thickness (MATERIALS 0.5)" % tag,
             None if tk_c is None or cheek_deg is None else tk_c * math.cos(math.radians(cheek_deg)), CHEEK_T, 0.005)
        # funnel wings: scan back from the ramp's loading end along the chute axis
        scan = []
        for x in np.arange(xt - 0.01, xt - 20.0, -0.01):
            iw = inner(x)
            if iw is None:
                break
            scan.append((x, iw[0], iw[1], ythick(x, iw[0], -1), ythick(x, iw[1], 1)))
        mouth = None
        tip_w = None
        if scan:
            tip_w = scan[-1][2] - scan[-1][1]
            full = [max(s[3], s[4]) for s in scan if s[3] and s[4]]
            tfull = max(full) if full else None
            ok_rows = [s for s in scan if tfull and s[3] and s[4] and s[3] >= tfull - 2e-3 and s[4] >= tfull - 2e-3]
            if ok_rows:
                mouth = ok_rows[-1]          # rearmost section where both wing plates are full thickness
        near("%s: funnel inner width at the loading end (mouth of the funnel wings, 36 ref)" % tag,
             None if mouth is None else mouth[2] - mouth[1], FLARE_W, REF,
             "" if mouth is None else " at local x %.2f (%.2f behind the ramp's loading end); the square-cut wing tips reach "
             "%.2f" % (mouth[0], xt - mouth[0], tip_w))
        chk("%s: funnel wings symmetric about the chute centre" % tag,
            mouth is not None and abs((mouth[1] + mouth[2]) / 2 - c) < 1e-3,
            "mouth mid %s vs %.4f" % (None if mouth is None else round((mouth[1] + mouth[2]) / 2, 4), c))
        wing_deg, tk_w, wedge = None, None, None
        if mouth is not None and len(scan) > 60:
            s1 = scan[20]
            wing_deg = math.degrees(math.atan2(abs(mouth[2] - s1[2]), abs(mouth[0] - s1[0])))
            sm = scan[len([s for s in scan if s[0] >= (s1[0] + mouth[0]) / 2]) - 1]
            tk_w = sm[4] * math.cos(math.radians(wing_deg))
            im7 = inner(sm[0], 7.0)
            chk("%s: funnel wings plumb (same inner width 3 in and 7 in above the loading-end ramp top)" % tag,
                im7 is not None and abs((im7[1] - im7[0]) - (sm[2] - sm[1])) < 1e-3, "%s vs %s" % ((sm[1], sm[2]), im7))
        near("%s: funnel wing plate thickness normal to the plate (MATERIALS cheek funnel 0.5)" % tag, tk_w, CHEEK_T, 0.005)
        # top-edge slopes in each plate's own plane (by-products, within the manual's +/-1 deg)
        tops_c = []
        for x in (x_beg - 1.0, x_end + 1.0):
            iy = inner(x)
            h = None if iy is None else rc.first(P(x, iy[1] + 0.25, 90.0), D(0, 0, -1))
            tops_c.append(None if h is None else (x, iy[1], 90.0 - h))
        edge_c = None
        if all(tops_c):
            run_e = math.hypot(tops_c[0][0] - tops_c[1][0], tops_c[0][1] - tops_c[1][1])
            edge_c = math.degrees(math.atan2(abs(tops_c[1][2] - tops_c[0][2]), run_e))
        edge_w = None
        if mouth is not None and len(scan) > 60:
            pts_w = []
            for s in (scan[20], [s for s in scan if s[0] >= mouth[0] + 0.3][-1]):
                h = rc.first(P(s[0], s[2] + 0.25, 90.0), D(0, 0, -1))
                pts_w.append(None if h is None else (s[0], s[2], 90.0 - h))
            if all(pts_w):
                run_w = math.hypot(pts_w[0][0] - pts_w[1][0], pts_w[0][1] - pts_w[1][1])
                edge_w = math.degrees(math.atan2(abs(pts_w[1][2] - pts_w[0][2]), run_w))
        flare_rows.append((tag, wing_deg, edge_w))
        chk("%s: cheek and funnel-wing plan angles and top edges obey the 15/30/45 rule (§0)" % tag,
            None not in (cheek_deg, wing_deg, edge_c, edge_w) and angle_ok(cheek_deg) and angle_ok(wing_deg)
            and angle_ok(edge_c, 1.0) and angle_ok(edge_w, 1.0),
            "cheek plan %s deg, wing plan %s deg, cheek top edge %s deg, wing top edge %s deg" %
            tuple("None" if v is None else "%.3f" % v for v in (cheek_deg, wing_deg, edge_c, edge_w)))
        # the funnel is closed: cheeks on the ramp edges, wings on the cheek ends, cheeks from the
        # back of the throat to the loading end
        dcr = f.dist(ramp, cheeks)
        chk("%s: cheeks close on the ramp side edges (gap <= 0.01)" % tag, dcr <= 0.01, "ramp-cheek distance %.4f" % dcr)
        dwc = f.dist(wings, cheeks) if wings else float("inf")
        chk("%s: funnel wings close on the cheek ends (gap <= 0.01)" % tag, dwc <= 0.01, "wing-cheek distance %.4f" % dwc)
        chk("%s: cheeks run from the back of the throat (within 0.5 of x %.2f) to the loading end" % (tag, x_back),
            cb[3] >= x_back - 0.5 and cb[0] <= xt + 0.5, "cheek local x %.3f..%.3f, ramp top %.3f..%.3f" % (cb[0], cb[3], xt, x_lo))
        mins = [(ch["rgb"], ch["alpha"], ch["mat"]["name"]) for ch in fun]
        chk("%s: cheek and funnel-wing appearance wall #9AA4B2, painted plywood" % tag,
            len(mins) == 4 and all(m[0] == rgb("wall") and m[1] == 1 and "lywood" in m[2] for m in mins), "%s" % mins)
        chk("%s: ramp leg (not in MATERIALS table) styled as wall structure" % tag,
            legs and legs[0]["rgb"] == rgb("wall"), "%s" % ([(l["rgb"], l["mat"]["name"]) for l in legs]))

        # ---- E. interference of the chute bodies with anything else --------------------------
        mine = throat + ramp + cheeks + wings + legs + trs
        hits = []
        for k, r in enumerate(mine):
            for o in recs:
                # every other body, the chute's own parts included (each pair tested once)
                if o is r or (any(o is m for m in mine[:k])) or not bb_overlap(wbox[id(r)], wbox[id(o)], 1e-3):
                    continue
                v = f.common_volume([r], [o])
                if v > 1e-6:
                    hits.append("%s x %s: %.4f" % (r["name"], o["name"], v))
        chk("%s: throat, ramp, cheeks, funnel wings, leg and tag panel interfere with nothing (each other included)" % tag,
            not hits, "; ".join(hits) or "none")
        # driver-station shelf / anything above the ramp corridor
        shelves = [r for r in f.find(r"re:^%s driver station \d shelf$" % side)]
        over = []
        for s in shelves:
            sb = f.bbox([s], F)
            if sb[1] < c + FLARE_W / 2 + CHEEK_T and sb[4] > c - FLARE_W / 2 - CHEEK_T:
                over.append("%s local y %.2f..%.2f" % (s["name"], sb[1], sb[4]))
        chk("%s: no driver-station shelf overhangs the ramp/cheek corridor" % tag, not over, "; ".join(over) or "clear")

        # ---- F. OUTFITTER LANE tape -----------------------------------------------------------
        lanes = near_y(fx(RX["lane"] % side), Y, 25)
        chk("%s: OUTFITTER LANE tape is one welded body, one connected solid" % tag,
            len(lanes) == 1 and sum(len(l["solids"]) for l in lanes) == 1,
            "%d bodies, %d solids" % (len(lanes), sum(len(l["solids"]) for l in lanes)))
        lb = f.bbox(lanes, F)
        chk("%s: lane tape outer edges X 0-48 from the wall, Y c +/- 18 (36 x 48), Z 0-0.01" % tag,
            np.allclose(lb, [0, c - LANE_W / 2, 0, LANE_D, c + LANE_W / 2, TAPE_T], atol=1e-4),
            "local bbox %s" % np.round(lb, 4))
        lin = [(1.0, c - 17.0), (24.0, c - 17.0), (47.0, c - 17.0), (47.0, c), (47.0, c + 17.0), (24.0, c + 17.0), (1.0, c + 17.0),
               (24.0, c - 17.99), (24.0, c - 16.01), (47.99, c), (46.01, c)]
        lout = [(24.0, c), (10.0, c - 10.0), (24.0, c - 15.99), (24.0, c + 15.99), (45.99, c), (48.01, c), (24.0, c - 18.01),
                (24.0, c + 18.01), (-0.01, c - 17.0)]
        badl = [p for p in lin if not f.inside(lanes, P(p[0], p[1], TAPE_T / 2))] + \
               [p for p in lout if f.inside(lanes, P(p[0], p[1], TAPE_T / 2))]
        chk("%s: lane tape is three 2-in strips (wall closes the 4th side), tape inside the zone" % tag, not badl,
            "bad probes %s" % badl)
        near("%s: lane centred on the measured chute centre" % tag, (lb[1] + lb[4]) / 2, yc_loc, 1e-3)
        # the protected loading corridor above the lane is free of field structure
        cf = K.Frame(P(0.001, c - LANE_W / 2, TAPE_T + 0.001), D(1, 0, 0), D(0, 0, 1))
        cbox = K.BRepBuilderAPI_Transform(BRepPrimAPI_MakeBox(LANE_D - 0.002, LANE_W, 60.0).Shape(), cf.trsf(), True).Shape()
        cbb = f.bbox([rec(cbox)])
        cands = [r for r in nonpiece if bb_overlap(wbox[id(r)], cbb) and "tape" not in (r["name"] or "").lower()]
        cvc = f.common_volume([rec(cbox)], cands) if cands else 0.0
        chk("%s: OUTFITTER LANE corridor (36 x 48, up to 60 in) free of field structure" % tag, cvc < 1e-6,
            "common %.6f with %s" % (cvc, sorted({r["name"] for r in cands})))
        want_rgb = rgb("alliance-blue" if side == "BLUE" else "alliance-red")
        chk("%s: lane tape colour %s, gaffer tape" % (tag, HEX["alliance-blue" if side == "BLUE" else "alliance-red"]),
            all(l["rgb"] == want_rgb and l["alpha"] == 1 and "affer" in l["mat"]["name"] for l in lanes),
            "%s" % sorted({(l["rgb"], l["mat"]["name"]) for l in lanes}))
        lbw = f.bbox(lanes)
        other_tape = [r for r in recs if "tape" in (r["name"] or "").lower() and id(r) not in {id(l) for l in lanes}
                      and bb_overlap(wbox[id(r)], lbw, 1e-3)]
        cvt = f.common_volume(lanes, other_tape) if other_tape else 0.0
        chk("%s: lane tape does not overlap other tape" % tag, cvt < 1e-6,
            "common %.6f with %s" % (cvt, sorted({r["name"] for r in other_tape})))

        # ---- G. piece-pass at the opening (doc §5), doc-derived solids ----------------------
        aperture = panel + glaze + frame + throat + trs
        # the part of the throat liner at and above the head line Z 40 (its head plate): the head
        # of the opening is the glazing edge plus this plate; the sill plate is not "overhead"
        cut = BRepPrimAPI_MakeBox(gp_Pnt(-1e4, -1e4, HEAD), gp_Pnt(1e4, 1e4, 1e3)).Shape()
        thead = [{"solids": K._solids(K.BRepAlgoAPI_Common(s_, cut).Shape())} for s_ in f.solids(throat)]
        head = glaze + thead
        jamb_lo, jamb_hi = c - (jl or 0), c + (jh or 0)
        for label, shape, height, width in (
                ("CACHE CRATE 13.0 envelope", BRepPrimAPI_MakeBox(gp_Pnt(-6.5, -6.5, 0), CRATE_ENV, CRATE_ENV, CRATE_ENV).Shape(), 13.0, 13.0),
                ("O2 CELL end-on 5 x 5", BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(-7, 0, 2.5), gp_Dir(1, 0, 0)), 2.5, 14.0).Shape(), 5.0, 5.0),
                ("O2 CELL lengthwise 14 x 5", BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, -7, 2.5), gp_Dir(0, 1, 0)), 2.5, 14.0).Shape(), 5.0, 14.0),
                ("ROPE COIL flat 10 x 2.5", BRepPrimAPI_MakeTorus(gp_Ax2(gp_Pnt(0, 0, 1.25), gp_Dir(0, 0, 1)), 3.75, 1.25).Shape(), 2.5, 10.0),
                ("ROPE COIL on edge 10 tall", BRepPrimAPI_MakeTorus(gp_Ax2(gp_Pnt(0, 0, 5.0), gp_Dir(0, 1, 0)), 3.75, 1.25).Shape(), 10.0, 2.5)):
            pfr = K.Frame(P(-0.125, c, SILL + 0.005), D(1, 0, 0), D(0, 0, 1))
            sh = K.BRepBuilderAPI_Transform(shape, pfr.trsf(), True).Shape()
            cvx = f.common_volume([rec(sh)], aperture)
            dhead = f.dist([rec(sh)], head)
            djamb = f.dist([rec(sh)], panel + throat)
            pbl = f.bbox([rec(sh)], F)
            lat = min(pbl[1] - jamb_lo, jamb_hi - pbl[4])
            ok = cvx < 1e-6 and abs(dhead - (OPEN_H - height - 0.005)) < 0.01 and djamb > 1e-4 and abs(lat - (OPEN_W - width) / 2) < 0.01
            level_rows.append((tag, label, dhead))
            chk("%s: piece-pass %s through the opening on the sill (head clearance %.2f)" % (tag, label, OPEN_H - height),
                ok, "overlap %.6f, head clearance %.4f, lateral clearance to the measured jambs %.4f (doc %.2f), nearest panel %.4f" %
                (cvx, dhead, lat, (OPEN_W - width) / 2, djamb))
        # the real CACHE CRATE of the package, level on the sill, crown apex under the head
        T0 = gp_Trsf()
        T0.SetTranslation(gp_Vec(*map(float, -crate_ctr)))
        pfr = K.Frame(P(-0.125, c, SILL + 6.5 + 0.005), D(1, 0, 0), D(0, 0, 1))
        sh = K.BRepBuilderAPI_Transform(crate_real, pfr.trsf().Multiplied(T0), True).Shape()
        dh = f.dist([rec(sh)], head)
        cvx = f.common_volume([rec(sh)], aperture)
        chk("%s: modelled CACHE CRATE level on the sill clears the head by 3.0 (doc)" % tag,
            cvx < 1e-6 and abs(dh - (OPEN_H - CRATE_ENV - 0.005)) < 0.02, "overlap %.6f head clearance %.4f" % (cvx, dh))

        # ---- H. path sweep: ramp -> sill -> field ---------------------------------------------
        corners = np.array([F.pt((x, y, z)) for x in (-45.0, 30.0) for y in (c - 25.0, c + 25.0) for z in (-1.0, 90.0)])
        region = list(corners.min(0)) + list(corners.max(0))
        near_bodies = [r for r in nonpiece if bb_overlap(wbox[id(r)], region)]
        rays = Rays(f.solids(near_bodies))
        dx = 0.02
        xs = np.arange(-38.0, 14.0, dx) + 0.005
        sup = np.full(len(xs), -1e9)
        cei = np.full(len(xs), 1e9)
        ys = np.linspace(-7.5, 7.5, 7)
        blocked = []
        for i, x in enumerate(xs):
            # probe seed 1 in above the measured chute floor (ramp plane, sill, carpet)
            if x > 0:
                z0 = 1.0
            elif x > x_lo:
                z0 = SILL + 1.0
            else:
                z0 = coef[0] * max(x, xt) + coef[2] + 1.0
            for yo in ys:
                p = P(x, c + yo, z0)
                if i % 50 == 0 and yo == 0 and f.inside(near_bodies, p):
                    blocked.append(round(float(x), 2))
                h = rays.first(p, D(0, 0, -1), 200.0)
                if h is not None:
                    sup[i] = max(sup[i], z0 - h)
                h = rays.first(p, D(0, 0, 1), 200.0)
                if h is not None:
                    cei[i] = min(cei[i], z0 + h)
        supw = np.maximum(np.maximum(sup, np.roll(sup, 1)), np.roll(sup, -1))
        ceiw = np.minimum(np.minimum(cei, np.roll(cei, 1)), np.roll(cei, -1))

        def S(X):
            return supw[np.clip(np.round((X - xs[0]) / dx).astype(int), 0, len(xs) - 1)]

        def C(X):
            return ceiw[np.clip(np.round((X - xs[0]) / dx).astype(int), 0, len(xs) - 1)]
        x_load = xt
        # overhead obstruction directly above the ramp run (anything lower than 20 in over the ramp)
        m = (xs > x_load + 0.1) & (xs < x_lo - 0.1)       # over the ramp (it starts at the back of the throat)
        head_room = np.min(cei[m] - sup[m])
        ceil_rows.append((tag, head_room))
        chk("%s: nothing overhead along the ramp run (free height above the ramp >= 20 in)" % tag,
            head_room >= 20.0 and not blocked, "min free height above the ramp %.2f in%s" % (head_room, ", blocked at %s" % blocked if blocked else ""))
        fil_c = np.array([-best[0], SILL - best[0]])      # measured sill roundover centre (local x, z)
        for pname, (mk, halfy) in PIECES_2D.items():
            H = _HULLS[pname] if pname in _HULLS else _HULLS.setdefault(pname, mk())

            def pose(xc, phi, H=H):
                s, co = math.sin(math.radians(phi)), math.cos(math.radians(phi))
                return xc + H[:, 0] * co + H[:, 1] * s, -H[:, 0] * s + H[:, 1] * co
            # phase A: sliding flat on the ramp at the measured ramp angle
            xmin_h = np.min(pose(0.0, slope)[0])
            xa0 = x_load - xmin_h + 0.3
            worstA = (1e9, None)
            restA = {}
            for xc in np.arange(xa0, 0.0001, 0.1):
                X, Zr = pose(xc, slope)
                zc = np.max(S(X) - Zr) + 0.005
                cl = np.min(C(X) - (zc + Zr))
                restA[round(xc, 1)] = zc
                if cl < worstA[0]:
                    worstA = (cl, xc, zc)
            # phase B: tipping over the sill roundover without slip, CoM starting over the
            # roundover centre, at its top, or at the wall plane
            worstB = (1e9, None, None)
            for xs0 in (fil_c[0], fil_c[0] / 2, 0.0):
                X, Zr = pose(xs0, slope)
                zc = np.max(S(X) - Zr) + 0.005
                cen = np.array([xs0, zc])
                for dl in np.arange(0.0, 60.01, 0.25):
                    c2 = fil_c + rot2(cen - fil_c, dl)
                    X, Zr = pose(c2[0], slope + dl)
                    Z = c2[1] + Zr
                    cl = np.min(C(X) - Z)
                    if cl < worstB[0]:
                        worstB = (cl, xs0, dl)
                    if np.min(X) > 0.01:
                        break
            sweep_rows.setdefault(pname, []).append((tag, worstA, worstB))
            chk("%s: %s slides down the ramp and through the opening with head clearance" % (tag, pname),
                worstA[0] > 0.0, "min overhead clearance %.3f in at CoM x %.2f (ramp angle %.2f)" % (worstA[0], worstA[1], slope))
            chk("%s: %s tips off the sill edge without striking the head" % (tag, pname),
                worstB[0] > 0.0, "min overhead clearance %.3f in (tip start CoM x %.2f, after %.2f deg)" % worstB)
            if pname.startswith("CACHE CRATE"):
                worst3d[tag] = (worstA, worstB, S, C, pose, slope, fil_c, restA)
        # the same tip-off with the sharp-cornered 13.0 envelope (info: shows the R1.0 crate
        # fillets, not the 3.0 envelope margin, are what clear the head during tip-off)
        Hb = rect(CRATE_ENV, CRATE_ENV)
        wBb = 1e9
        for xs0 in (fil_c[0], fil_c[0] / 2, 0.0):
            X = xs0 + Hb[:, 0] * math.cos(math.radians(slope)) + Hb[:, 1] * math.sin(math.radians(slope))
            Zr = -Hb[:, 0] * math.sin(math.radians(slope)) + Hb[:, 1] * math.cos(math.radians(slope))
            cen = np.array([xs0, np.max(S(X) - Zr) + 0.005])
            for dl in np.arange(0.0, 60.01, 0.25):
                c2 = fil_c + rot2(cen - fil_c, dl)
                ph = math.radians(slope + dl)
                X = c2[0] + Hb[:, 0] * math.cos(ph) + Hb[:, 1] * math.sin(ph)
                Z = c2[1] - Hb[:, 0] * math.sin(ph) + Hb[:, 1] * math.cos(ph)
                wBb = min(wBb, np.min(C(X) - Z))
                if np.min(X) > 0.01:
                    break
        envelope_tip.append((tag, wBb))
        # 3-D spot checks with the modelled CACHE CRATE at the worst sweep poses — one chute per
        # alliance (Blue local y 30, Red local y 294), the other two are covered by the identical
        # 2-D sweeps above and the rotation check below (each 3-D distance costs ~1 s)
        if (side, Y) not in (("BLUE", 30.0), ("RED", 30.0)):
            continue
        wA, wB = worst3d[tag][0], worst3d[tag][1]

        def placed(xc, zc, phi):
            s, co = math.sin(math.radians(phi)), math.cos(math.radians(phi))
            fr = K.Frame(P(xc, c, zc), D(co, 0, -s), D(s, 0, co))
            return K.BRepBuilderAPI_Transform(crate_real, fr.trsf().Multiplied(T0), True).Shape()
        overhead = glaze + trs + frame + throat
        spots = [("slide worst", wA[1], wA[2] + 0.02, slope)]
        X, Zr = worst3d[tag][4](wB[1], slope)
        zc0 = np.max(S(X) - Zr) + 0.005
        c2 = fil_c + rot2(np.array([wB[1], zc0]) - fil_c, wB[2])
        spots.append(("tip worst", c2[0], c2[1] + 0.02, slope + wB[2]))
        spots.append(("loading end", xt + 7.0, None, slope))
        for lab, xc, zc, phi in spots:
            if zc is None:
                X, Zr = worst3d[tag][4](xc, phi)
                zc = np.max(S(X) - Zr) + 0.025
            sh = placed(xc, zc, phi)
            sbb = fast_bbox([sh])
            loc = [r for r in near_bodies if bb_overlap(wbox[id(r)], sbb, 1.0)]
            d_all = shape_dist(sh, f.solids(loc))
            d_over = shape_dist(sh, f.solids(overhead))
            d_side = shape_dist(sh, f.solids(cheeks + wings + panel + throat)) if lab != "tip worst" else float("nan")
            chk("%s: 3-D modelled CACHE CRATE at the %s pose touches nothing" % (tag, lab), d_all > 1e-4,
                "min distance %.4f to any body; overhead (glazing/tag/frame) %.3f; cheeks/jambs %.3f" % (d_all, d_over, d_side))

    # ---- aggregated (ref) findings across the four chutes ----------------------------------
    chk("all chutes: alliance wall thickness at the chute 2.0 (ref +/-0.25) — solid depth bounding the sill, the head "
        "and both jambs",
        all(abs(d - WALL_T) <= REF for _, hs in wall_depths for d in hs),
        "; ".join("%s sill %.2f head %.2f jambs %.2f / %.2f" % ((t,) + tuple(hs)) for t, hs in wall_depths))

    # ---- OUTFITTER stock (§6 c) ----------------------------------------------------------------
    for side in ("BLUE", "RED"):
        F = local_frame(f, side)
        stock = f.find(r"re:^(CACHE CRATE|O2 CELL|ROPE COIL) - %s OUTFITTER" % side)
        cnt = {k: sum(1 for r in stock if r["name"].startswith(k)) for k in PIECE_PREFIX}
        chk("%s: OUTFITTER stock is 7 of each type (§6 c)" % side, all(v == STOCK_PER_TYPE for v in cnt.values()), "%s" % cnt)
        sb = f.bbox(stock, F)
        chk("%s: OUTFITTER stock behind the wall, on the floor" % side, sb[3] <= -WALL_T + 1e-6 and abs(sb[2]) < 0.02,
            "stock local bbox %s" % np.round(sb, 3))
        struct = fx(r"^%s OUTFITTER \d+ (chute ramp|chute throat|cheek \d+|funnel wing \d+|ramp leg)$" % side)
        d = f.dist(stock, struct)
        chk("%s: OUTFITTER stock clear of the throats, ramps, cheeks, funnel wings and legs" % side, d > 0.0, "min distance %.3f" % d)

    # ---- Red = Blue rotated 180 deg about (324, 162) ------------------------------------------
    def rot_bb(b):
        return [FIELD_L - b[3], FIELD_W - b[4], b[2], FIELD_L - b[0], FIELD_W - b[1], b[5]]
    pairs = []
    for kind in ("throat", "ramp", "cheek", "wing", "leg", "lane"):
        for Yb, Yr in ((30.0, 294.0), (294.0, 30.0)):
            bl = near_y(fx(RX[kind] % "BLUE"), Yb, 25)
            rd = near_y(fx(RX[kind] % "RED"), Yr, 25)
            pairs.append(("%s Y%g" % (kind, Yb), bl, rd))
    pairs.append(("tag 1 -> 14", f.find(r"re:^AprilTag 1 - "), f.find(r"re:^AprilTag 14 - ")))
    pairs.append(("tag 2 -> 15", f.find(r"re:^AprilTag 2 - "), f.find(r"re:^AprilTag 15 - ")))
    badr = []
    for lab, bl, rd in pairs:
        if not bl or not rd or len(bl) != len(rd):
            badr.append("%s: %d blue / %d red bodies" % (lab, len(bl), len(rd)))
            continue
        if not np.allclose(rot_bb(f.bbox(bl)), f.bbox(rd), atol=1e-4) or abs(f.volume(bl) - f.volume(rd)) > 1e-4:
            badr.append("%s: blue->%s red %s" % (lab, np.round(rot_bb(f.bbox(bl)), 3), np.round(f.bbox(rd), 3)))
    chk("Red OUTFITTER throats, ramps, cheeks, funnel wings, legs, lanes and tags are the Blue ones rotated 180 deg "
        "about (324, 162)", not badr,
        "; ".join(badr) or "%d pairs match" % len(pairs))

    # ---- informational summaries (always pass) ------------------------------------------------
    chk("info: ramp run as built (doc 'ramp run 40' is ambiguous)", True,
        "; ".join("%s horiz %.2f slope-len %.2f rise %.2f top Z %.2f" % r for r in run_rows[:1]))
    crow = sweep_rows["CACHE CRATE (12 cube, 0.5 crown, R1 fillets)"]
    chk("info: CACHE CRATE real passage clearance vs the documented 3.0 (level) figure", True,
        "slide %.3f in, tip-off %.3f in (doc-derived crowned section); level-on-sill %.3f" %
        (min(r[1][0] for r in crow), min(r[2][0] for r in crow), min(r[2] for r in level_rows if r[1].startswith("CACHE"))))
    chk("info: sharp-cornered 13.0 envelope tipping off the sill (no R1.0 edge fillets)", True,
        "min head clearance %.3f in (negative = the envelope corner would strike the 0.25-in glazing head)" % min(v for _, v in envelope_tip))
    return out
