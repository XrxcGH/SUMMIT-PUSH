# -*- coding: utf-8 -*-
"""
Independent check: BASE DEPOT tray (floor, lip, corner squares and arms, entry chamfer), both CRAGS.

Expected values come from the package documents only (never from src/20_ledger.fs or the part code):

  FIELD-CAD-PACKAGE §0    always-blue-origin NWU, inches; Red = Blue rotated 180 deg about (324, 162);
                          "(ref) may float +/-0.25 in"; "Every angle on the field is 15, 30 or 45 deg".
  FIELD-CAD-PACKAGE §1.1  BLUE CRAG (324, 240), RED CRAG (324, 84), 48 x 48 footprint; Blue SHELF FACE
                          normal -X (plane X = 300), SOCKET FACES Y = 216 / 264.
  FIELD-CAD-PACKAGE §1.2  CRAG APRON 36 from SHELF/PEG FACE, 20 from SOCKET FACES, R20 corners;
                          centreline X = 324, "the BASE DEPOT trays stop 8 in short of the line";
                          CENTER CACHE band "interrupted where the BASE DEPOT trays cross it".
  FIELD-CAD-PACKAGE §2.2  Shelf 1 top 24, thickness 0.75 (ref) -> underside 23.25; depth 14.0 (Blue X 286-300);
                          gusset floors: under Shelf 1 above Z 19.0, above Z 22.0 inside the tag prisms
                          (Blue Y 221.5-230.5 and 249.5-258.5); under Shelf 2 above Z 38.0.
  FIELD-CAD-PACKAGE §2.3  Low Socket over the arm; robot standoff at the arm: lip outer face 16.75,
                          FRAME PERIMETER 19.75, rim 8.0 outboard -> 11.75 of extension.
  FIELD-CAD-PACKAGE §3    U in plan: shelf-face leg 16 x 48 (Blue X 284-300, Y 216-264); corner squares
                          16 x 16 (X 284-300, Y 200-216 / 264-280); corner arms 16 x 16 (X 300-316, same
                          Y bands); lip top 4.0 above carpet = 3.75 above the floor (CRITICAL); lip top-edge
                          R0.25 (CRITICAL); channel 16.0 (CRITICAL); arms 16.0 from the SHELF FACE plane
                          (CRITICAL); lip 0.75 (ref); floor 0.25 thick, top at Z = 0.25 (CRITICAL); 45 deg
                          entry chamfer strip outside the lip, 1.0-in leg; tray area 1792 in^2; ~8 CRATES
                          one abreast, ~12 SUPPLIES mixed, single layer; 12 crates need 2028 in^2;
                          open-to-sky: outer 2.0 in of the leg, both corner squares fully, the arms except
                          under the Low Socket tube (X 306.7-313.3 x Y 265.6-274.9 from Z 22.19; clear
                          columns 6.66 / 2.66 / 5.11 / 1.56); only the corner squares take a dropped CRATE
                          or COIL; 23.25 to the Shelf 1 underside and >= 19.0 anywhere a gusset descends;
                          robot standoff: lip outer face 16.75, FRAME PERIMETER 19.75, shelf slot 7.0 ->
                          12.75, Summit rim 8.0 -> 11.75, all inside the 18-in limit.
  FIELD-CAD-PACKAGE §7    9.0 panel centred 17.5 -> target 13.4375-21.5625 (8.125 target); a CRATE standing
                          on the tray floor tops out at 13.25, 0.19 below the target.
  FIELD-CAD-PACKAGE §9    CRATE 12.0 cube + 0.5 crown -> 13.0 envelope, rests on its bottom crown;
                          CELL 5.0 x 14.0; COIL 10.0 OD, 2.5 tube.
  VISION-GUIDE §1.3       upright CELL in the DEPOT tops at 14.25; lying CELL 5.25; COIL on edge 10.25.
  MATERIALS-AND-COLORS    BASE DEPOT lip / floor / entry chamfer: painted plywood, `depot` #7F7F7F.
  Manual R403             BUMPER bottom edge between 1.25 and 2.5 in above the floor.

All expected coordinates below are written for the BLUE CRAG in world inches; the RED CRAG is checked
with every probe rotated 180 deg about (324, 162) and every measurement rotated back, so the same
numbers apply to both.

Low Socket overhang: DESIGN-SPEC §3 makes the 7.0 socket length the depth a CELL seats at ("a
seated 14.0-in O2 CELL therefore stands 7.0 in proud"), so the 0.09 closed bottom lies beyond it and
the tube is 7.09 overall.  The tube therefore starts 1.5625 off the SOCKET FACE (Y 265.56) at Z 22.19,
as the §3 overhang figures give (Y from 265.6, Z from 22.19, the 1.56 column).  They are derived
below from the §2.3 socket numbers (rim 30, 8.0 out, 30 deg, 3.34 outer radius).

Construction reading (naming only): the two Low Socket tubes of a CRAG are "<A> CRAG Low Socket
(guardrail side)" and "(center side)".
"""
import math

import kernel_occ as K

# ---- document values -------------------------------------------------------------------
FL, FW = 648.0, 324.0
CX, CY = 324.0, 162.0
SHELF_X = 300.0                 # Blue SHELF FACE plane (CRAG centre 324 - 24)
SOCK_YN, SOCK_YP = 216.0, 264.0  # Blue SOCKET FACE planes
CH = 16.0                       # channel depth (CRITICAL)
ARM = 16.0                      # arm length from the SHELF FACE plane (CRITICAL)
LIP_Z = 4.0                     # lip top above carpet (CRITICAL)
FLOOR_T = 0.25                  # floor thickness, top at Z = 0.25 (CRITICAL)
LIP_T = 0.75                    # lip thickness (ref)
LIP_R = 0.25                    # lip top-edge radius (CRITICAL)
CHAMF = 1.0                     # entry chamfer leg, 45 deg
TRAY_AREA = 1792.0
LEG = (284.0, 216.0, 300.0, 264.0)            # X0, Y0, X1, Y1 (Blue)
SQ_N = (284.0, 200.0, 300.0, 216.0)
SQ_P = (284.0, 264.0, 300.0, 280.0)
ARM_N = (300.0, 200.0, 316.0, 216.0)
ARM_P = (300.0, 264.0, 316.0, 280.0)
U_PTS = [(284, 200), (316, 200), (316, 216), (300, 216), (300, 264), (316, 264), (316, 280), (284, 280)]
SHELF1_UNDER = 24.0 - 0.75      # 23.25
GUSSET_FLOOR1 = 19.0
GUSSET_FLOOR1_TAG = 22.0
GUSSET_FLOOR2 = 38.0
TAG_PRISMS_Y = ((221.5, 230.5), (249.5, 258.5))
SHELF_PLAN_X = (286.0, 300.0)   # Shelf 1 footprint (14.0 deep)
CRATE_S, CRATE_CROWN = 12.0, 0.5
CRATE_ENV = CRATE_S + 2 * CRATE_CROWN          # 13.0
CRATE_TOP_IN_TRAY = FLOOR_T + CRATE_ENV        # 13.25
CELL_D, CELL_L = 5.0, 14.0
COIL_OD, COIL_TUBE = 10.0, 2.5
TAG_Z, TAG_PANEL, TAG_TARGET = 17.5, 9.0, 8.125
TARGET_BOT = TAG_Z - TAG_TARGET / 2            # 13.4375
BUMPER = 3.0
REACH = 18.0
SLOT_X_OFF = 7.0
RIM_OFF = 8.0
BUMPER_BOTTOM_MIN = 1.25        # R403: 4.5 section, bottom edge 1.25 .. 2.5
# Low Socket tube over the +Y arm (Blue), from §2.3: rim (310, 272, 30), axis 30 deg outward, 3.34
# outer radius, 7.0 bore + 0.09 closed bottom (see the docstring).  §3 prints X 306.7-313.3 x
# Y 265.6-274.9 from Z 22.19 and columns 6.66 / 2.66 / 5.11 / 1.56.
_S30, _C30 = 0.5, math.sqrt(3) / 2
SOCK_RO, SOCK_OVERALL = 3.34, 7.0 + 0.09
SOCK_INBOARD = RIM_OFF - SOCK_OVERALL * _S30 - SOCK_RO * _C30       # 1.5625 (§3: 1.56)
LOW_SOCK_SIL = (310.0 - SOCK_RO, SOCK_YP + SOCK_INBOARD, 310.0 + SOCK_RO, SOCK_YP + RIM_OFF + SOCK_RO * _C30)
LOW_SOCK_ZMIN = 30.0 - SOCK_OVERALL * _C30 - SOCK_RO * _S30         # 22.19 (§3)
CENTRELINE_X = 324.0
STOP_SHORT = 8.0
APRON_SHELF, APRON_SOCK, APRON_R = 36.0, 20.0, 20.0
DEPOT_RGB = (0x7F, 0x7F, 0x7F)
SKY = 200.0

# CRAG tags whose faces the tray runs along (§7 table: 6/7 shelf face; 8/10 are the shelf-side tags on
# the +Y / -Y SOCKET FACES at X = 310; Red ID = Blue ID + 13)
ADJ_TAGS = {"BLUE": (6, 7, 8, 10), "RED": (19, 20, 21, 23)}

WF = K.Frame((0, 0, 0), (1, 0, 0), (0, 0, 1))
PL_XY = [[0, 0, 0], [0, 0, 1], [1, 0, 0]]


# ---- geometry helpers ------------------------------------------------------------------
def rp(side, p):
    """Blue world point -> the same point on `side` (Red = 180 deg about (324, 162))."""
    if side == "BLUE":
        return tuple(p)
    q = [FL - p[0], FW - p[1]]
    return tuple(q + list(p[2:]))


def rbox_back(side, b):
    """World bbox on `side` -> bbox in Blue-equivalent coordinates."""
    if b is None or side == "BLUE":
        return b
    return [FL - b[3], FW - b[4], b[2], FL - b[0], FW - b[1], b[5]]


def _solids_of(reg):
    out = []
    for r in reg.bodies.values():
        out += r["solids"]
    return out


def prism(side, pts, z0, z1):
    """Vertical prism over a Blue-world polygon, mapped to `side`."""
    reg = K.Registry()
    K.mkPrism(reg, K.Id(("probe",)), WF, PL_XY, [list(rp(side, p)) for p in pts], z0, z1)
    return _solids_of(reg)


def box(side, x0, y0, z0, x1, y1, z1):
    return prism(side, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], z0, z1)


def crate_at(side, x, y):
    """Crowned CACHE CRATE (12.0 cube, 0.5 crown, no edge fillets = its full envelope) resting on
    its bottom crown on the tray floor, centred on Blue point (x, y)."""
    c = rp(side, (x, y))
    reg = K.Registry()
    F = K.Frame((c[0], c[1], FLOOR_T + CRATE_S / 2 + CRATE_CROWN), (1, 0, 0), (0, 0, 1))
    K.mkPillowBox(reg, K.Id(("crate",)), F, CRATE_S / 2, CRATE_CROWN)
    return _solids_of(reg)


def cell_lying(side, x, y, axis):
    """O2 CELL envelope (5.0 dia x 14.0 cylinder) lying on the floor, axis 'x' or 'y'."""
    c = rp(side, (x, y))
    reg = K.Registry()
    zc = FLOOR_T + CELL_D / 2
    if axis == "x":
        pl = [[c[0] - CELL_L / 2, c[1], zc], [1, 0, 0], [0, 1, 0]]
    else:
        pl = [[c[0], c[1] - CELL_L / 2, zc], [0, 1, 0], [0, 0, 1]]
    K.mkCyl(reg, K.Id(("cell",)), WF, pl, [0, 0], CELL_D / 2, 0, CELL_L)
    return _solids_of(reg)


def cell_upright(side, x, y):
    c = rp(side, (x, y))
    reg = K.Registry()
    K.mkCyl(reg, K.Id(("cellU",)), WF, [[c[0], c[1], FLOOR_T], [0, 0, 1], [1, 0, 0]], [0, 0], CELL_D / 2, 0, CELL_L)
    return _solids_of(reg)


def coil_flat(side, x, y):
    c = rp(side, (x, y))
    reg = K.Registry()
    rt = COIL_TUBE / 2
    pl = [[c[0], c[1], FLOOR_T + rt], [0, -1, 0], [1, 0, 0]]   # plane containing the vertical axis
    K.mkRevolve(reg, K.Id(("coil",)), WF, pl, [["C", [COIL_OD / 2 - rt, 0], rt]])
    return _solids_of(reg)


def cyl_column(side, x, y, d, z0, z1):
    c = rp(side, (x, y))
    reg = K.Registry()
    K.mkCyl(reg, K.Id(("col",)), WF, [[c[0], c[1], z0], [0, 0, 1], [1, 0, 0]], [0, 0], d / 2, 0, z1 - z0)
    return _solids_of(reg)


def bb(solids):
    if not solids:
        return None
    b = K.Bnd_Box()
    K.BRepBndLib.AddOptimal_s(K._compound(solids), b, False, False)
    return K._box6(b)


def bb_exact(solids):
    """Exact extents of a virtual SUPPLY (OCC's optimal box is loose on the CRATE's Bezier faces):
    distance from a far point on each axis through the piece's centre.  Exact for these pieces, which
    are symmetric about their centre lines (crate apex / cylinder generatrix / torus equator)."""
    b0 = bb(solids)
    if b0 is None:
        return None
    c = [(b0[0] + b0[3]) / 2, (b0[1] + b0[4]) / 2, (b0[2] + b0[5]) / 2]
    M = 1.0e4
    comp = K._compound(solids)
    out = [0.0] * 6
    for ax in range(3):
        for sg in (-1, 1):
            p = list(c)
            p[ax] += sg * M
            v = K.BRepBuilderAPI_MakeVertex(K._gp(p)).Vertex()
            d = K.BRepExtrema_DistShapeShape(v, comp).Value()
            out[ax + (3 if sg > 0 else 0)] = p[ax] - sg * d
    return out


def common(a, b):
    out = []
    for x in a:
        for y in b:
            op = K.BRepAlgoAPI_Common(x, y)
            out += K._solids(op.Shape())
    return [s for s in out if K._volume([s]) > 1e-12]


def cvol(a, b):
    return K._volume(common(a, b))


def vol(s):
    return K._volume(s)


def ext(side, rs_solids, x0, y0, z0, x1, y1, z1):
    """Blue-equivalent bbox of (bodies ∩ probe box given in Blue coordinates)."""
    return rbox_back(side, bb(common(rs_solids, box(side, x0, y0, z0, x1, y1, z1))))


def rot180(solids):
    t = K.gp_Trsf()
    t.SetRotation(K.gp_Ax1(K.gp_Pnt(CX, CY, 0), K.gp_Dir(0, 0, 1)), math.pi)
    return [K.BRepBuilderAPI_Transform(s, t, True).Shape() for s in solids]


def overlaps(b1, b2, pad=0.0):
    return (b1[0] < b2[3] + pad and b2[0] < b1[3] + pad and b1[1] < b2[4] + pad and b2[1] < b1[4] + pad
            and b1[2] < b2[5] + pad and b2[2] < b1[5] + pad)


def near(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol


def fmt(v):
    return "None" if v is None else ("%.4f" % v)


# ---- the check ---------------------------------------------------------------------------
class Ctx:
    def __init__(self, f):
        self.f = f
        self.recs = f.records()
        self.bbs = {r["id"]: f.bbox([r]) for r in self.recs}

    def hits(self, solids, exclude=lambda r: False, tol=1e-6):
        """Field bodies sharing volume with `solids`: list of (name, volume)."""
        b = bb(solids)
        out = []
        for r in self.recs:
            if exclude(r) or not overlaps(self.bbs[r["id"]], b):
                continue
            v = cvol(r["solids"], solids)
            if v > tol:
                out.append((r["name"], v))
        return out


def is_tray(r):
    return "BASE DEPOT" in (r["name"] or "")


def run(f):
    out = []
    C = Ctx(f)

    def add(label, ok, detail):
        out.append((label, bool(ok), detail))

    for side in ("BLUE", "RED"):
        S = side + " DEPOT: "
        pre = side + " CRAG BASE DEPOT "
        try:
            floor = f.find(pre + "floor")
            lip = f.find(pre + "lip")
            chamf = f.find(pre + "entry chamfer")
        except KeyError as e:
            add(S + "tray bodies present", False, str(e))
            continue
        tower = f.find(side + " CRAG tower")
        base = tower + f.find(side + " CRAG kick-guard")   # the kick-guard is let in flush at the base
        fs, ls, cs = f.solids(floor), f.solids(lip), f.solids(chamf)
        tray_s = fs + ls + cs

        # ---------- A. identity, appearance -------------------------------------------------
        for nm_, rs in (("floor", floor), ("lip", lip), ("entry chamfer", chamf)):
            add(S + nm_ + " is one body / one solid (continuous U, one weldment)",
                len(rs) == 1 and len(f.solids(rs)) == 1, "%d bodies, %d solids" % (len(rs), len(f.solids(rs))))
            rgb, a = f.color(rs)
            add(S + nm_ + " colour `depot` #7F7F7F, opaque", tuple(rgb) == DEPOT_RGB and a == 1,
                "got rgb %s alpha %s" % (rgb, a))
            m = f.material(rs)
            add(S + nm_ + " material painted plywood (MATERIALS §2)",
                "plywood" in m["name"].lower() and "paint" in m["name"].lower() and 350 <= m["density"] <= 800,
                "got %r at %s kg/m^3" % (m["name"], m["density"]))

        # ---------- as-built CRAG faces (the channel is measured from these) ------------------
        tw = f.solids(tower)
        fx = ext(side, tw, 290, 239.99, 7.99, 310, 240.01, 8.01)
        fyn = ext(side, tw, 307.99, 206, 7.99, 308.01, 226, 8.01)
        fyp = ext(side, tw, 307.99, 254, 7.99, 308.01, 274, 8.01)
        face_x = fx[0] if fx else None
        face_yn = fyn[1] if fyn else None    # outer surface of the -Y panel
        face_yp = fyp[4] if fyp else None    # outer surface of the +Y panel
        add(S + "as-built SHELF FACE / SOCKET FACE planes (Blue X 300, Y 216 / 264)",
            near(face_x, SHELF_X, 1e-4) and near(face_yn, SOCK_YN, 1e-4) and near(face_yp, SOCK_YP, 1e-4),
            "shelf face %s, -Y face %s, +Y face %s (Blue-equivalent)" % (fmt(face_x), fmt(face_yn), fmt(face_yp)))
        face_x = face_x if face_x is not None else SHELF_X
        face_yn = face_yn if face_yn is not None else SOCK_YN
        face_yp = face_yp if face_yp is not None else SOCK_YP

        # ---------- B. floor ------------------------------------------------------------------
        fb = rbox_back(side, f.bbox(floor))
        add(S + "floor laid on the carpet (bottom Z = 0) with its top at Z = 0.25",
            near(fb[2], 0.0, 1e-6) and near(fb[5], FLOOR_T, 1e-6), "floor Z %.4f .. %.4f" % (fb[2], fb[5]))
        u_all = prism(side, U_PTS, 0, FLOOR_T)
        v_f, v_u = vol(fs), vol(u_all)
        v_c = cvol(fs, u_all)
        symdiff = v_f + v_u - 2 * v_c
        add(S + "floor plan is exactly the five-rectangle U (leg + 2 corner squares + 2 arms)",
            abs(symdiff) < 1e-4, "symmetric-difference volume %.6f in^3 (floor %.4f, expected %.4f)" % (symdiff, v_f, v_u))
        add(S + "tray area 1792 in^2", near(v_f / FLOOR_T, TRAY_AREA, 1e-3), "floor area %.4f in^2" % (v_f / FLOOR_T))
        for pname, r in (("shelf-face leg 16 x 48 (Blue X 284-300, Y 216-264)", LEG),
                         ("corner square -Y 16 x 16 (Blue X 284-300, Y 200-216)", SQ_N),
                         ("corner square +Y 16 x 16 (Blue X 284-300, Y 264-280)", SQ_P),
                         ("corner arm -Y 16 x 16 (Blue X 300-316, Y 200-216)", ARM_N),
                         ("corner arm +Y 16 x 16 (Blue X 300-316, Y 264-280)", ARM_P)):
            want = (r[2] - r[0]) * (r[3] - r[1]) * FLOOR_T
            got = cvol(fs, box(side, r[0], r[1], 0, r[2], r[3], FLOOR_T))
            add(S + "floor covers the " + pname, near(got, want, 1e-4), "covered %.4f of %.4f in^3" % (got, want))
        foot = box(side, 300, 216, -1, 348, 264, 100)
        add(S + "no tray part enters the CRAG footprint", cvol(tray_s, foot) < 1e-6,
            "overlap %.6f in^3" % cvol(tray_s, foot))
        d_ft = f.dist(floor, base)
        add(S + "floor meets the CRAG faces / flush kick-guard (no gap a piece could drop into)", d_ft < 1e-6,
            "floor-to-CRAG gap %.6f" % d_ft)

        # ---------- C. lip ---------------------------------------------------------------------
        lb = rbox_back(side, f.bbox(lip))
        add(S + "lip top 4.0 above the carpet (CRITICAL)", near(lb[5], LIP_Z, 1e-6) and near(lb[2], 0, 1e-6),
            "lip Z %.4f .. %.4f" % (lb[2], lb[5]))
        add(S + "lip top 3.75 above the tray floor", near(lb[5] - fb[5], LIP_Z - FLOOR_T, 1e-6),
            "lip top - floor top = %.4f" % (lb[5] - fb[5]))
        o = LIP_T
        ring_outer = [(284 - o, 200 - o), (316 + o, 200 - o), (316 + o, 216), (300, 216), (300, 264),
                      (316 + o, 264), (316 + o, 280 + o), (284 - o, 280 + o)]
        ring_o = prism(side, ring_outer, 0, LIP_Z)
        ring_i = prism(side, U_PTS, 0, LIP_Z)
        area_ring = (vol(ring_o) - vol(ring_i)) / LIP_Z
        inside_ring = cvol(ls, ring_o) - cvol(ls, ring_i)
        add(S + "lip lies entirely in the 0.75-in band outside the channel (no lip inside the channel)",
            cvol(ls, ring_i) < 1e-6 and near(inside_ring, vol(ls), 1e-4),
            "lip vol %.4f, in band %.4f, in channel %.6f" % (vol(ls), inside_ring, cvol(ls, ring_i)))
        mid_o = prism(side, ring_outer, 1.0, 3.0)
        mid_i = prism(side, U_PTS, 1.0, 3.0)
        got_mid = cvol(ls, mid_o) - cvol(ls, mid_i)
        add(S + "lip fills the whole band all round (leg, squares, arms, both arm ends) at mid-height",
            near(got_mid, area_ring * 2.0, 1e-3), "band area %.4f in^2, lip section Z1-3 %.4f in^3 (want %.4f)"
            % (area_ring, got_mid, area_ring * 2.0))

        # stations: (label, probe box in Blue coords, axis, crag face position, sign of 'outward')
        stations = [
            ("shelf-face leg @Y205", (270, 204.99, 1.99, 300, 205.01, 2.01), 0, face_x, -1),
            ("shelf-face leg @Y240", (270, 239.99, 1.99, 300, 240.01, 2.01), 0, face_x, -1),
            ("shelf-face leg @Y275", (270, 274.99, 1.99, 300, 275.01, 2.01), 0, face_x, -1),
            ("-Y run @X290", (289.99, 190, 1.99, 290.01, 216, 2.01), 1, face_yn, -1),
            ("-Y arm @X308", (307.99, 190, 1.99, 308.01, 216, 2.01), 1, face_yn, -1),
            ("+Y run @X290", (289.99, 264, 1.99, 290.01, 290, 2.01), 1, face_yp, +1),
            ("+Y arm @X308", (307.99, 264, 1.99, 308.01, 290, 2.01), 1, face_yp, +1),
        ]
        for lab, pb, ax, face, sg in stations:
            e = ext(side, ls, *pb)
            if e is None:
                add(S + "lip section " + lab, False, "no lip found")
                continue
            lo, hi = e[ax], e[ax + 3]
            inner = hi if sg < 0 else lo
            outer = lo if sg < 0 else hi
            add(S + "channel depth 16.0 face-to-lip (CRITICAL) " + lab, near(abs(inner - face), CH, 1e-4),
                "lip inner face %.4f, crag face %.4f -> %.4f" % (inner, face, abs(inner - face)))
            add(S + "lip 0.75 thick, outer face 16.75 off the crag face " + lab,
                near(hi - lo, LIP_T, 1e-4) and near(abs(outer - face), CH + LIP_T, 1e-4),
                "thickness %.4f, outer face %.4f off the face" % (hi - lo, abs(outer - face)))
        for lab, y in (("-Y arm end", 208.0), ("+Y arm end", 272.0)):
            e = ext(side, ls, 300, y - 0.01, 1.99, 330, y + 0.01, 2.01)
            if e is None:
                add(S + "arm-end lip " + lab, False, "no lip found")
                continue
            add(S + "arm runs 16.0 along the SOCKET FACE from the SHELF FACE plane (CRITICAL) " + lab,
                near(e[0] - face_x, ARM, 1e-4), "arm-end lip inner face X %.4f -> %.4f from X %.4f" % (e[0], e[0] - face_x, face_x))
            add(S + "arm-end lip 0.75 thick " + lab, near(e[3] - e[0], LIP_T, 1e-4), "thickness %.4f" % (e[3] - e[0]))
            add(S + "channel stops 8.0 short of the centreline " + lab, near(CENTRELINE_X - e[0], STOP_SHORT, 1e-4),
                "channel end X %.4f -> %.4f short of X 324 (lip to %.4f, i.e. %.4f short)"
                % (e[0], CENTRELINE_X - e[0], e[3], CENTRELINE_X - e[3]))
        # lip walls plumb (inner face the same at Z 0.5 and 3.5)
        e1 = ext(side, ls, 270, 239.99, 0.49, 300, 240.01, 0.51)
        e2 = ext(side, ls, 270, 239.99, 3.49, 300, 240.01, 3.51)
        add(S + "lip walls plumb (inner/outer faces identical at Z 0.5 and 3.5)",
            e1 and e2 and near(e1[0], e2[0], 1e-5) and near(e1[3], e2[3], 1e-5),
            "Z0.5 %s / Z3.5 %s" % (e1 and [round(v, 4) for v in (e1[0], e1[3])], e2 and [round(v, 4) for v in (e2[0], e2[3])]))

        # lip top-edge radius R0.25 on every top edge (outer and inner) of every run
        k = math.sqrt(2) - 1
        edges = [  # (label, sharp-corner point, direction into the lip along the top, horizontal axis)
            ("outer leg", (284 - o, 240), (+1, 0)), ("inner leg", (284, 240), (-1, 0)),
            ("outer -Y run", (292, 200 - o), (0, +1)), ("inner -Y run", (292, 200), (0, -1)),
            ("outer +Y run", (292, 280 + o), (0, -1)), ("inner +Y run", (292, 280), (0, +1)),
            ("outer -Y arm end", (316 + o, 208), (-1, 0)), ("inner -Y arm end", (316, 208), (+1, 0)),
            ("outer +Y arm end", (316 + o, 272), (-1, 0)), ("inner +Y arm end", (316, 272), (+1, 0)),
        ]
        for lab, p, dvec in edges:
            wp = rp(side, (p[0], p[1], LIP_Z))
            d = f.dist_point(lip, wp)
            r_est = d / k
            # height 0.10 in from the face along the top: 4 - r + sqrt(r^2 - (r - u)^2)
            u = 0.10
            q = (p[0] + dvec[0] * u, p[1] + dvec[1] * u)
            e = ext(side, ls, q[0] - 0.002, q[1] - 0.002, 3.0, q[0] + 0.002, q[1] + 0.002, 5.0)
            hz = e[5] if e else None
            want_h = LIP_Z - LIP_R + math.sqrt(LIP_R ** 2 - (LIP_R - u) ** 2)
            add(S + "lip top edge R0.25 (CRITICAL) " + lab,
                near(r_est, LIP_R, 0.004) and hz is not None and abs(hz - want_h) < 0.004,
                "corner-to-surface %.5f -> R %.4f; height 0.10 in from the face %s (R0.25 gives %.4f)"
                % (d, r_est, fmt(hz), want_h))
        # flat top between the two roundovers (0.75 - 2 x 0.25 = 0.25 wide) is at exactly 4.0
        e = ext(side, ls, 283.61, 239.99, 3.0, 283.64, 240.01, 5.0)
        add(S + "lip flat top at mid-thickness is at Z 4.0", e is not None and near(e[5], LIP_Z, 1e-5),
            "top at mid-thickness %s" % (fmt(e[5]) if e else None))

        # ---------- D. entry chamfer ------------------------------------------------------------
        cb = rbox_back(side, f.bbox(chamf))
        want_cb = [284 - o - CHAMF, 200 - o - CHAMF, 0, 316 + o + CHAMF, 280 + o + CHAMF, CHAMF]
        add(S + "entry chamfer strip: 1.0 tall, 1.0 beyond the lip outer face all round",
            all(abs(a - b) < 1e-4 for a, b in zip(cb, want_cb)),
            "bbox %s want %s" % ([round(v, 4) for v in cb], want_cb))
        csta = [  # (label, lip outer face point, outward unit vector)
            ("outer leg", (284 - o, 240), (-1, 0)), ("-Y run", (292, 200 - o), (0, -1)),
            ("+Y run", (292, 280 + o), (0, +1)), ("-Y arm end", (316 + o, 208), (+1, 0)),
            ("+Y arm end", (316 + o, 272), (+1, 0)), ("-Y arm", (308, 200 - o), (0, -1)),
            ("+Y arm", (308, 280 + o), (0, +1)),
        ]
        for lab, p, dv in csta:
            hs = []
            for dd in (0.25, 0.5, 0.75):
                q = (p[0] + dv[0] * dd, p[1] + dv[1] * dd)
                e = ext(side, cs, q[0] - 0.002, q[1] - 0.002, -0.5, q[0] + 0.002, q[1] + 0.002, 2.0)
                hs.append(e[5] if e else None)
            ok = all(h is not None for h in hs)
            ang = math.degrees(math.atan2(hs[0] - hs[2], 0.5)) if ok else None
            ok = ok and all(abs(h - (CHAMF - dd)) < 0.003 for h, dd in zip(hs, (0.25, 0.5, 0.75)))
            add(S + "entry chamfer 45 deg, 1.0-in leg, " + lab, ok and abs(ang - 45.0) < 0.2,
                "heights at 0.25/0.5/0.75 out: %s -> slope %s deg" % ([fmt(h) for h in hs], fmt(ang)))
        # chamfer volume: triangular section 0.5 in^2 swept along the lip outer runs, hip-mitred at the
        # four convex corners, cut square at the two crag faces
        runs = 2 * (ARM + LIP_T) + 2 * (CH + ARM + 2 * LIP_T) + (80 + 2 * LIP_T)
        want_cv = 0.5 * CHAMF * CHAMF * (runs + 4 * 2 * CHAMF / 3.0)
        add(S + "entry chamfer continuous round the whole outer lip (volume check)", near(vol(cs), want_cv, 1e-3),
            "volume %.4f, 45-deg 1.0 strip along %.2f in of lip gives %.4f" % (vol(cs), runs, want_cv))
        add(S + "entry chamfer abuts the lip (touching, no overlap) and runs to the CRAG at both arm ends",
            f.dist(chamf, lip) < 1e-6 and f.common_volume(chamf, lip) < 1e-6 and f.dist(chamf, base) < 1e-6
            and f.dist(lip, base) < 1e-6,
            "chamfer-lip gap %.6f, overlap %.6f, chamfer-CRAG gap %.6f, lip-CRAG gap %.6f"
            % (f.dist(chamf, lip), f.common_volume(chamf, lip), f.dist(chamf, base), f.dist(lip, base)))
        add(S + "chamfer high edge (1.0) below the lowest legal BUMPER bottom (R403 1.25): bumpers reach the lip face",
            cb[5] < BUMPER_BOTTOM_MIN, "chamfer top %.4f vs bumper bottom >= %.2f" % (cb[5], BUMPER_BOTTOM_MIN))

        # ---------- E. rotational symmetry ----------------------------------------------------------
        if side == "RED":
            for nm_ in ("floor", "lip", "entry chamfer"):
                b_s = f.solids(f.find("BLUE CRAG BASE DEPOT " + nm_))
                r_s = f.solids(f.find("RED CRAG BASE DEPOT " + nm_))
                rb_ = rot180(b_s)
                vb, vr, vc = vol(b_s), vol(r_s), cvol(rb_, r_s)
                add("RED DEPOT: " + nm_ + " is the Blue one rotated 180 deg about (324, 162)",
                    near(vb, vr, 1e-4) and near(vc, vr, 1e-4), "Blue %.4f, Red %.4f, common after rotation %.4f" % (vb, vr, vc))

        # ---------- F. interference, contact, tape --------------------------------------------------
        for nm_, rs in (("floor", floor), ("lip", lip), ("entry chamfer", chamf)):
            hit = C.hits(f.solids(rs), exclude=lambda r: is_tray(r))
            add(S + nm_ + " shares no volume with any other field body", not hit,
                "; ".join("%s %.5f" % h for h in hit) or "clear")
        tape_rs = [r for r in C.recs if "tape" in (r["name"] or "").lower() or "mark" in (r["name"] or "").lower()]
        tb = bb(tray_s)
        dmin, dname = 1e9, None
        tape_hit = []
        for r in tape_rs:
            if not overlaps(C.bbs[r["id"]], tb, pad=3.0):
                continue
            dd = f.dist([r], floor + lip + chamf)
            if dd < dmin:
                dmin, dname = dd, r["name"]
            v = cvol(r["solids"], tray_s)
            if v > 1e-7:
                tape_hit.append((r["name"], v))
        add(S + "no tape runs under or through the tray (CENTER CACHE band interrupted, APRON clear)",
            not tape_hit, ("; ".join("%s %.6f" % h for h in tape_hit) or "clear")
            + "; nearest tape %s at %.4f in" % (dname, dmin))
        # tray entirely inside the CRAG APRON region (36 / 20 offsets, R20 corners)
        cpts = [(284 - o - CHAMF, 200 - o - CHAMF), (284 - o - CHAMF, 280 + o + CHAMF)]
        ac = [(SHELF_X - APRON_SHELF + APRON_R, SOCK_YN - APRON_SOCK + APRON_R),
              (SHELF_X - APRON_SHELF + APRON_R, SOCK_YP + APRON_SOCK - APRON_R)]
        rr = [math.hypot(p[0] - c[0], p[1] - c[1]) for p, c in zip(cpts, ac)]
        add(S + "tray (to the chamfer toe) lies inside its CRAG APRON line incl. the R20 corners",
            all(x < APRON_R for x in rr) and cb[0] > SHELF_X - APRON_SHELF and cb[1] > SOCK_YN - APRON_SOCK
            and cb[4] < SOCK_YP + APRON_SOCK,
            "chamfer outer corners at R %.3f / %.3f from the apron arc centres (arc R20)" % tuple(rr))

        # ---------- G. overhead clearances, open-to-sky -------------------------------------------
        chan_low = prism(side, U_PTS, FLOOR_T + 1e-3, GUSSET_FLOOR1)
        hit = C.hits(chan_low, exclude=is_tray)
        add(S + "channel empty from the floor to Z 19.0 everywhere (any SUPPLY can be pushed round the whole U)",
            not hit, "; ".join("%s %.5f" % h for h in hit) or "clear")
        s1 = f.find(side + " CRAG Shelf 1")
        s1b = rbox_back(side, f.bbox(s1))
        add(S + "Shelf 1 underside 23.25 above the carpet (CRITICAL clearance for pushed SUPPLIES)",
            near(s1b[2], SHELF1_UNDER, 1e-4), "Shelf 1 slab Z min %.4f" % s1b[2])
        add(S + "Shelf 1 plan footprint (Blue X 286-300) lies inside the 16-in channel (X 284-300)",
            s1b[0] >= 284 - 1e-6 and near(s1b[0], SHELF_PLAN_X[0], 1e-4) and near(s1b[3], SHELF_PLAN_X[1], 1e-4)
            and s1b[1] >= 216 - 1e-6 and s1b[4] <= 264 + 1e-6,
            "Shelf 1 X %.4f..%.4f Y %.4f..%.4f" % (s1b[0], s1b[3], s1b[1], s1b[4]))
        g1 = f.find(side + " CRAG Shelf 1 gusset")
        g2 = f.find(side + " CRAG Shelf 2 gusset")
        g1b = rbox_back(side, f.bbox(g1))
        g2b = rbox_back(side, f.bbox(g2))
        add(S + "Shelf 1 gussets entirely above Z 19.0 (§2.2 floor)", g1b[2] >= GUSSET_FLOOR1 - 1e-6,
            "lowest gusset point Z %.4f" % g1b[2])
        add(S + "Shelf 2 gussets entirely above Z 38.0 (§2.2 floor)", g2b[2] >= GUSSET_FLOOR2 - 1e-6,
            "lowest gusset point Z %.4f" % g2b[2])
        gtag = 0.0
        for y0, y1 in TAG_PRISMS_Y:
            gtag += cvol(f.solids(g1), box(side, 280, y0, 0, 300, y1, GUSSET_FLOOR1_TAG))
        add(S + "no Shelf 1 gusset below Z 22.0 in front of a SHELF FACE tag (prisms Y 221.5-230.5, 249.5-258.5)",
            gtag < 1e-7, "gusset volume in the tag prisms below Z 22: %.6f" % gtag)
        leg_col = box(side, 284 + 1e-3, 216 + 1e-3, FLOOR_T + 1e-3, 300 - 1e-3, 264 - 1e-3, SHELF1_UNDER)
        hit = C.hits(leg_col, exclude=lambda r: is_tray(r) or "gusset" in (r["name"] or ""))
        add(S + "over the shelf-face leg nothing but gussets comes below the Shelf 1 underside (23.25)",
            not hit, "; ".join("%s %.5f" % h for h in hit) or "clear")
        # minimum overhead clearance over the leg, all bodies (gussets included) -> >= 19.0
        lo = 1e9
        legbox = box(side, 284, 216, FLOOR_T + 1e-3, 300, 264, 30)
        legbb = bb(legbox)
        for r in C.recs:
            if is_tray(r) or not overlaps(C.bbs[r["id"]], legbb):
                continue
            e = rbox_back(side, bb(common(r["solids"], legbox)))
            if e is not None:
                lo = min(lo, e[2])
        add(S + "lowest structure over the shelf-face leg is >= 19.0 (clearance >= 18.75 over the floor)",
            lo >= GUSSET_FLOOR1 - 1e-6, "lowest overhead point Z %.4f (%.4f above the tray floor)" % (lo, lo - FLOOR_T))

        eps = 0.01
        sky = [
            ("outer 2.0-in strip of the shelf-face leg (48 x 2)", (284 + eps, 216, 286 - eps, 264)),
            ("-Y corner square (16 x 16), fully clear", (284 + eps, 200 + eps, 300 - eps, 216)),
            ("+Y corner square (16 x 16), fully clear", (284 + eps, 264, 300 - eps, 280 - eps)),
            ("-Y arm 6.66-in column at the SHELF FACE side", (300, 200 + eps, 306.66 - eps, 216 - eps)),
            ("+Y arm 6.66-in column at the SHELF FACE side", (300, 264 + eps, 306.66 - eps, 280 - eps)),
            ("-Y arm 2.66-in column at the arm end", (313.34 + eps, 200 + eps, 316 - eps, 216 - eps)),
            ("+Y arm 2.66-in column at the arm end", (313.34 + eps, 264 + eps, 316 - eps, 280 - eps)),
            ("-Y arm 5.11-in column along the lip", (300 + eps, 200 + eps, 316 - eps, 205.11 - eps)),
            ("+Y arm 5.11-in column along the lip", (300 + eps, 274.89 + eps, 316 - eps, 280 - eps)),
        ]
        for lab, (x0, y0, x1, y1) in sky:
            hit = C.hits(box(side, x0, y0, FLOOR_T + 1e-3, x1, y1, SKY), exclude=is_tray)
            add(S + "open to the sky: " + lab, not hit, "; ".join("%s %.5f" % h for h in hit) or "clear")
        for lab, (x0, y0, x1, y1) in (("-Y arm %.2f-in column at the SOCKET FACE" % SOCK_INBOARD,
                                       (300 + eps, SOCK_YN - SOCK_INBOARD + eps, 316 - eps, 216)),
                                      ("+Y arm %.2f-in column at the SOCKET FACE" % SOCK_INBOARD,
                                       (300 + eps, 264, 316 - eps, SOCK_YP + SOCK_INBOARD - eps))):
            hit = C.hits(box(side, x0, y0, FLOOR_T + 1e-3, x1, y1, SKY), exclude=is_tray)
            others = [h for h in hit if "Low Socket bracket" not in h[0]]
            add(S + lab + " clear except the Low Socket attachment (§2.3 wedge under the tube)", not others,
                "; ".join("%s %.5f" % h for h in hit) or "clear")
        # the Low Socket tube overhang over each arm, as published
        for lab, (ax0, ay0, ax1, ay1), sil in (
                ("+Y arm", ARM_P, LOW_SOCK_SIL),
                ("-Y arm", ARM_N, (LOW_SOCK_SIL[0], 480 - LOW_SOCK_SIL[3], LOW_SOCK_SIL[2], 480 - LOW_SOCK_SIL[1]))):
            tube = f.find(side + " CRAG Low Socket (guardrail side)") + f.find(side + " CRAG Low Socket (center side)")
            e = ext(side, f.solids(tube), ax0, ay0, 0, ax1, ay1, SKY)
            ok = e is not None and all(abs(a - b) < 0.02 for a, b in zip((e[0], e[1], e[3], e[4]), sil)) \
                and abs(e[2] - LOW_SOCK_ZMIN) < 0.01
            add(S + "Low Socket tube overhangs the " + lab + " at X %.2f-%.2f x Y %.2f-%.2f from Z %.2f" % (
                sil[0], sil[2], sil[1], sil[3], LOW_SOCK_ZMIN),
                ok, "tube over the arm: %s (§3 prints X 306.7-313.3 x Y 265.6-274.9 from Z 22.19)"
                % ([round(v, 3) for v in e] if e else None))
        # drop tests
        for lab, (x0, y0, x1, y1) in (("-Y corner square", SQ_N), ("+Y corner square", SQ_P)):
            cx_, cy_ = (x0 + x1) / 2, (y0 + y1) / 2
            col = box(side, cx_ - CRATE_ENV / 2, cy_ - CRATE_ENV / 2, FLOOR_T + 1e-3, cx_ + CRATE_ENV / 2, cy_ + CRATE_ENV / 2, SKY)
            hit = C.hits(col, exclude=is_tray)
            add(S + "a crowned CRATE can be dropped straight into the " + lab, not hit,
                "; ".join("%s %.5f" % h for h in hit) or "13.0 x 13.0 column clear to the sky")
        for lab, (x0, y0, x1, y1) in (("-Y arm", ARM_N), ("+Y arm", ARM_P)):
            crate_clear, coil_clear = [], []
            n = 7
            for i in range(n):
                for j in range(n):
                    a = x0 + (x1 - x0 - CRATE_ENV) * i / (n - 1)
                    b = y0 + (y1 - y0 - CRATE_ENV) * j / (n - 1)
                    col = box(side, a, b, FLOOR_T + 1e-3, a + CRATE_ENV, b + CRATE_ENV, SKY)
                    if not C.hits(col, exclude=is_tray):
                        crate_clear.append((a, b))
                    ca = x0 + COIL_OD / 2 + (x1 - x0 - COIL_OD) * i / (n - 1)
                    cb_ = y0 + COIL_OD / 2 + (y1 - y0 - COIL_OD) * j / (n - 1)
                    col = cyl_column(side, ca, cb_, COIL_OD, FLOOR_T + 1e-3, SKY)
                    if not C.hits(col, exclude=is_tray):
                        coil_clear.append((ca, cb_))
            add(S + "no CRATE or COIL can be dropped straight into the " + lab + " (overhung by the Low Socket)",
                not crate_clear and not coil_clear,
                "clear crate columns %s; clear coil columns %s (of %d positions each)" % (crate_clear[:4], coil_clear[:4], n * n))

        # ---------- H. virtual SUPPLIES ------------------------------------------------------------
        tag_bot = {}
        for tid in ADJ_TAGS[side]:
            try:
                pr = f.find(r"re:^AprilTag %d - " % tid)
                tag_bot[tid] = f.bbox(pr)[2] + (TAG_PANEL - TAG_TARGET) / 2
            except KeyError:
                tag_bot[tid] = None
        placements = [
            ("-Y corner square", (292, 208)), ("+Y corner square", (292, 272)),
            ("leg in front of the shelf-face tags (Y 226)", (292, 226)), ("leg centre (Y 240)", (292, 240)),
            ("leg in front of the shelf-face tags (Y 254)", (292, 254)),
            ("-Y arm under the Low Socket", (308, 208)), ("+Y arm under the Low Socket", (308, 272)),
        ]
        chan_col = prism(side, U_PTS, 0, 40)
        for lab, (x, y) in placements:
            cr = crate_at(side, x, y)
            b = rbox_back(side, bb_exact(cr))
            hit = C.hits(cr)
            inproj = cvol(cr, chan_col)
            add(S + "crowned CRATE stands in the " + lab + ": fits, inside the channel projection, top 13.25",
                not hit and near(inproj, vol(cr), 1e-3) and near(b[2], FLOOR_T, 1e-4) and near(b[5], CRATE_TOP_IN_TRAY, 1e-4),
                "hits %s; %.1f%% inside the channel projection; Z %.4f..%.4f; side clearance %.3f / %.3f"
                % ([h[0] for h in hit] or "none", 100 * inproj / vol(cr), b[2], b[5],
                   min(b[0] - 284, 300 - b[3]) if x < 300 else min(b[0] - 300, 316 - b[3]),
                   min(b[1] - 200, 216 - b[4]) if y < 216 else (min(b[1] - 264, 280 - b[4]) if y > 264 else 0.0)))
        cr = crate_at(side, 292, 240)
        top = bb_exact(cr)[5]
        for tid, tb_ in tag_bot.items():
            add(S + "CRATE in the tray (top %.2f) stays below tag %d's target bottom (13.44), margin 0.19" % (CRATE_TOP_IN_TRAY, tid),
                tb_ is not None and near(tb_, TARGET_BOT, 1e-3) and top < tb_ and near(tb_ - top, TARGET_BOT - CRATE_TOP_IN_TRAY, 1e-3),
                "crate top %.4f, as-built target bottom %s, margin %s" % (top, fmt(tb_), fmt(tb_ - top if tb_ else None)))
        lipb = rbox_back(side, f.bbox(lip))
        add(S + "no part of the tray can occlude a CRAG tag (tray top below every adjacent panel)",
            all(tb_ is not None and lipb[5] < tb_ - (TAG_PANEL - TAG_TARGET) / 2 for tb_ in tag_bot.values()),
            "tray top %.3f vs panel bottoms %s" % (lipb[5], [fmt(v - (TAG_PANEL - TAG_TARGET) / 2) if v else None for v in tag_bot.values()]))

        # eight crates one abreast (6 along the 80-in outer run, 1 in each arm)
        gap = (80.0 - 6 * CRATE_ENV) / 7
        pos = [(292, 200 + gap + CRATE_ENV / 2 + i * (CRATE_ENV + gap)) for i in range(6)] + [(308, 208), (308, 272)]
        crates = [crate_at(side, x, y) for x, y in pos]
        bad = []
        for i, cr in enumerate(crates):
            h = C.hits(cr)
            if h or not near(cvol(cr, chan_col), vol(cr), 1e-3):
                bad.append((pos[i], [x[0] for x in h]))
        pair = max((cvol(crates[i], crates[j]) for i in range(8) for j in range(i + 1, 8)), default=0.0)
        add(S + "about 8 CACHE CRATES fit one abreast in a single layer (6 along the outer run + 1 per arm)",
            not bad and pair < 1e-6, "problems %s; max crate-crate overlap %.6f; spacing gap %.3f" % (bad or "none", pair, gap))
        add(S + "twelve crowned crates (2028 in^2) cannot fit the measured tray area",
            12 * CRATE_ENV ** 2 > v_f / FLOOR_T and near(12 * CRATE_ENV ** 2, 2028.0, 1e-9),
            "12 x 13.0^2 = %.1f vs tray %.1f in^2" % (12 * CRATE_ENV ** 2, v_f / FLOOR_T))
        # a mixed load of 12 SUPPLIES in a single layer
        mix = [("crate", (292, 206.7)), ("crate", (292, 219.9)), ("cellx", (292, 229.1)), ("cellx", (292, 234.3)),
               ("coil", (292, 242.0)), ("coil", (292, 252.2)), ("cellx", (292, 259.9)), ("crate", (292, 269.1)),
               ("coil", (305.2, 208.0)), ("celly", (313.1, 208.0)), ("coil", (305.2, 272.0)), ("celly", (313.1, 272.0))]
        pieces = []
        for kind, (x, y) in mix:
            if kind == "crate":
                pieces.append(crate_at(side, x, y))
            elif kind == "coil":
                pieces.append(coil_flat(side, x, y))
            elif kind == "cellx":
                pieces.append(cell_lying(side, x, y, "x"))
            else:
                pieces.append(cell_lying(side, x, y, "y"))
        bad = []
        for (kind, p), pc in zip(mix, pieces):
            h = C.hits(pc)
            b = rbox_back(side, bb_exact(pc))
            if h or not near(cvol(pc, chan_col), vol(pc), 1e-3) or not near(b[2], FLOOR_T, 1e-3):
                bad.append((kind, p, [x[0] for x in h]))
        pair = max((cvol(pieces[i], pieces[j]) for i in range(12) for j in range(i + 1, 12)), default=0.0)
        add(S + "about 12 SUPPLIES fit as a mixed single layer (3 crates, 5 cells, 4 coils, all on the floor)",
            not bad and pair < 1e-6, "problems %s; max piece-piece overlap %.6f" % (bad or "none", pair))
        # other standing heights from VISION-GUIDE §1.3
        cu = cell_upright(side, 292, 240)
        bcu = bb(cu)
        hit = C.hits(cu)
        add(S + "O2 CELL stood on end in the DEPOT tops out at 14.25 (VISION-GUIDE §1.3) and fits under Shelf 1",
            near(bcu[5], FLOOR_T + CELL_L, 1e-4) and not hit,
            "top %.4f (%.4f into the 13.44 target band); hits %s" % (bcu[5], bcu[5] - TARGET_BOT, [h[0] for h in hit] or "none"))
        cl = cell_lying(side, 292, 240, "x")
        add(S + "O2 CELL lying in the DEPOT tops out at 5.25 (VISION-GUIDE §1.3)", near(bb(cl)[5], 5.25, 1e-4),
            "top %.4f" % bb(cl)[5])

        # ---------- I. robot standoff and reach -----------------------------------------------------
        lo_x = lb[0]
        frame = SHELF_X - lo_x + BUMPER
        add(S + "robot standoff: lip outer face 16.75 off the SHELF FACE -> FRAME PERIMETER 19.75",
            near(SHELF_X - lo_x, CH + LIP_T, 1e-4) and near(frame, 19.75, 1e-4), "outer face %.4f -> frame %.4f" % (SHELF_X - lo_x, frame))
        add(S + "shelf-slot reach 12.75 and Summit/Low Socket rim reach 11.75, inside the 18-in limit",
            near(frame - SLOT_X_OFF, 12.75, 1e-4) and near(frame - RIM_OFF, 11.75, 1e-4) and frame - SLOT_X_OFF <= REACH,
            "slot %.4f, rim %.4f" % (frame - SLOT_X_OFF, frame - RIM_OFF))
        add(S + "robot standoff at each arm: lip outer face 16.75 off the SOCKET FACE",
            near(SOCK_YN - lb[1], CH + LIP_T, 1e-4) and near(lb[4] - SOCK_YP, CH + LIP_T, 1e-4),
            "-Y %.4f, +Y %.4f" % (SOCK_YN - lb[1], lb[4] - SOCK_YP))
    return out
