# -*- coding: utf-8 -*-
"""
Independent check: BASE DEPOT ring tray (floor, lip, four legs and four corner squares, entry chamfer),
both CRAGS.

Expected values come from the package documents only (never from src/20_ledger.fs or the part code):

  FIELD-CAD-PACKAGE §0    always-blue-origin NWU, inches; Red = Blue rotated 180 deg about (324, 162);
                          "(ref) may float +/-0.25 in"; "Every angle on the field is 15, 30 or 45 deg".
  FIELD-CAD-PACKAGE §1.1  BLUE CRAG (324, 240), RED CRAG (324, 84), 48 x 48 footprint; Blue SHELF FACE
                          normal -X (plane X = 300), PEG FACE X = 348, SOCKET FACES Y = 216 / 264.
  FIELD-CAD-PACKAGE §1.2  CRAG APRON 36 from the SHELF / PEG FACES, 20 from the SOCKET FACES, R20 corners,
                          2-in tape laid inside the line; FIELD centerline X = 324, broken where each CRAG
                          and its tray cross it.
  FIELD-CAD-PACKAGE §2.2  Shelf 1 top 24, thickness 0.75 (ref) -> underside 23.25; depth 14.0 (Blue X 286-300);
                          gusset floors: under Shelf 1 above Z 19.0, above Z 22.0 inside the tag prisms
                          (Blue Y 221.5-230.5 and 249.5-258.5); under Shelf 2 above Z 38.0.
  FIELD-CAD-PACKAGE §2.3  Low Socket rim 30 at lateral +14 (shelf-face side, Blue X 310), Mid Socket rim 54
                          at -14 (Blue X 338); rims 8.0 out from the SOCKET FACE, 30 deg outward, outer
                          radius 3.34.
  FIELD-CAD-PACKAGE §2.5  Low / Mid Pegs on the PEG FACE at +/-14, Z 30 / 54; High Pegs on the spire face,
                          14.0 inboard of the PEG FACE, at +/-7, Z 78; 1.5 OD, 45 deg up, 10.0 exposed.
  DESIGN-SPEC §3 /        the ring: four legs 16 x 48 (SHELF FACE leg Blue X 284-300 x Y 216-264, SOCKET
  FIELD-CAD-PACKAGE §3    FACE legs X 300-348 x Y 200-216 / 264-280, PEG FACE leg X 348-364 x Y 216-264) and
                          four corner squares 16 x 16, no corner arms; channel 16.0 from each face to the
                          lip inner face (CRITICAL); lip top 4.0 above the carpet = 3.75 above the floor
                          (CRITICAL); lip 0.75 (ref) with an R0.25 top edge (CRITICAL); floor 0.25 thick,
                          top at Z = 0.25 (CRITICAL); 45 deg entry chamfer strip outside the lip, 1.0-in leg;
                          outer footprint 48 + 2 x 16.75 = 81.5 square (Blue X 283.25-364.75, Y 199.25-280.75),
                          83.5 over the chamfer (Blue X 282.25-365.75, Y 198.25-281.75); inside every CRAG
                          APRON, 0.25 in from the APRON tape (inner edge 18.0 off the face) along the SOCKET
                          FACES and 0.16 in at the corner arcs (chamfer corner 17.84 from the arc center,
                          against the tape's R18 inner arc); tray area 80^2 - 48^2 = 4096 in^2; about 18
                          CACHE CRATES one abreast or about 27 SUPPLIES mixed, single layer; open from above:
                          the outer 2 in of the SHELF FACE leg, all four corner squares, both SOCKET FACE legs
                          except where their socket tubes overhang them, and the PEG FACE leg, which only the
                          Low and Mid Pegs cross; no SUPPLY can be dropped in where a socket tube overhangs
                          the tray; the FIELD centerline is broken across the tray.  Robot reach from the
                          lip, FRAME PERIMETER 16.75 + 3.0 = 19.75 off every face: Shelf slot 12.75, Summit
                          rim 11.75, Low and Mid Socket rims 11.75, Low and Mid Peg tips 12.68 (roots 19.75),
                          High Peg tip 26.68 (root 33.75); the binding reach is the High Peg tip, 26.68 of
                          the 30 in allowed on the own CRAG APRON (G404), and the High Peg root is beyond it.
  FIELD-CAD-PACKAGE §7 /  9.0 panel centred 17.5 -> target 13.4375-21.5625 (8.125 target); the tray runs
  DESIGN-SPEC §6          beneath the tag panels on all four faces; a CRATE standing on the tray floor tops
                          out at 13.25, 0.19 below the target.
  FIELD-CAD-PACKAGE §9    CRATE 12.0 cube + 0.5 crown -> 13.0 envelope, rests on its bottom crown;
                          CELL 5.0 x 14.0; COIL 10.0 OD, 2.5 tube.
  VISION-GUIDE §1.3       upright CELL in the DEPOT tops at 14.25; lying CELL 5.25.
  MATERIALS-AND-COLORS    BASE DEPOT lip / floor / entry chamfer: painted plywood, `depot` #7F7F7F.
  Manual R403             BUMPER bottom edge between 1.25 and 2.5 in above the floor.

All expected coordinates below are written for the BLUE CRAG in world inches; the RED CRAG is checked
with every probe rotated 180 deg about (324, 162) and every measurement rotated back, so the same
numbers apply to both.

Socket overhang: DESIGN-SPEC §3 makes the 7.0 socket length the depth a CELL seats at ("a seated
14.0-in O2 CELL therefore stands 7.0 in proud"), so the 0.09 closed bottom lies beyond it and the tube
is 7.09 overall.  Each side-socket tube therefore covers 1.5625-10.8925 in off its SOCKET FACE in plan,
3.34 either side of its rim center, from Z 22.19 (Low) or Z 46.19 (Mid); the figures are derived below
from the §2.3 socket numbers.

Construction reading (naming only): the side-socket tubes of a CRAG are "<A> CRAG Low Socket
(guardrail side)" / "(center side)", and likewise the Mid Socket, the brackets and the pegs.
"""
import math

import kernel_occ as K

# ---- document values -------------------------------------------------------------------
FL, FW = 648.0, 324.0
CX, CY = 324.0, 162.0
SHELF_X, PEG_X = 300.0, 348.0    # Blue SHELF FACE / PEG FACE planes (CRAG centre 324 -/+ 24)
SOCK_YN, SOCK_YP = 216.0, 264.0  # Blue SOCKET FACE planes
CH = 16.0                       # channel depth, every face (CRITICAL)
LIP_Z = 4.0                     # lip top above carpet (CRITICAL)
FLOOR_T = 0.25                  # floor thickness, top at Z = 0.25 (CRITICAL)
LIP_T = 0.75                    # lip thickness (ref)
LIP_R = 0.25                    # lip top-edge radius (CRITICAL)
CHAMF = 1.0                     # entry chamfer leg, 45 deg
TRAY_AREA = 80.0 ** 2 - 48.0 ** 2               # 4096
CHAN = (284.0, 200.0, 364.0, 280.0)             # channel outer edge (lip inner faces)
FOOT = (300.0, 216.0, 348.0, 264.0)             # CRAG footprint
LIP_OUT = (283.25, 199.25, 364.75, 280.75)      # 81.5 square
CHAMF_OUT = (282.25, 198.25, 365.75, 281.75)    # 83.5 square
LEGS = [("SHELF FACE leg 16 x 48 (Blue X 284-300, Y 216-264)", (284.0, 216.0, 300.0, 264.0)),
        ("PEG FACE leg 16 x 48 (Blue X 348-364, Y 216-264)", (348.0, 216.0, 364.0, 264.0)),
        ("-Y SOCKET FACE leg 48 x 16 (Blue X 300-348, Y 200-216)", (300.0, 200.0, 348.0, 216.0)),
        ("+Y SOCKET FACE leg 48 x 16 (Blue X 300-348, Y 264-280)", (300.0, 264.0, 348.0, 280.0))]
SQUARES = [("SHELF FACE / -Y corner square (Blue X 284-300, Y 200-216)", (284.0, 200.0, 300.0, 216.0)),
           ("SHELF FACE / +Y corner square (Blue X 284-300, Y 264-280)", (284.0, 264.0, 300.0, 280.0)),
           ("PEG FACE / -Y corner square (Blue X 348-364, Y 200-216)", (348.0, 200.0, 364.0, 216.0)),
           ("PEG FACE / +Y corner square (Blue X 348-364, Y 264-280)", (348.0, 264.0, 364.0, 280.0))]
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
REACH_APRON = 30.0              # G404: own CRAG APRON limit
SLOT_X_OFF = 7.0
RIM_OFF = 8.0
PEG_EXP, PEG_OD = 10.0, 1.5
HPEG_INBOARD = 14.0
PEG_ROOTS = {"Low": (30.0, 14.0), "Mid": (54.0, 14.0)}   # Z, lateral (+/-) on the PEG FACE
HPEG = (78.0, 7.0)
REACH_DOC = {"shelf": 12.75, "summit": 11.75, "sock": 11.75, "peg_tip": 12.68, "peg_root": 19.75,
             "hpeg_tip": 26.68, "hpeg_root": 33.75}
BUMPER_BOTTOM_MIN = 1.25        # R403: 4.5 section, bottom edge 1.25 .. 2.5
APRON_SHELF, APRON_SOCK, APRON_R, APRON_TAPE = 36.0, 20.0, 20.0, 2.0
TOE = CH + LIP_T + CHAMF        # chamfer toe off each face, 17.75
TAPE_GAP_SOCK = APRON_SOCK - APRON_TAPE - TOE   # 0.25: the tape's inner edge is 18.0 off the SOCKET FACES
# corner arcs: the chamfer corner against the tape's R18 inner arc (arc centre 16 / 0 in off the faces)
TAPE_GAP_ARC = (APRON_R - APRON_TAPE) - math.hypot(TOE - (APRON_SHELF - APRON_R), TOE - (APRON_SOCK - APRON_R))   # 0.164
# side-socket tubes, from §2.3: rim 8.0 out, axis 30 deg outward, 3.34 outer radius, 7.0 bore +
# 0.09 closed bottom (see the docstring)
_S30, _C30 = 0.5, math.sqrt(3) / 2
SOCK_RO, SOCK_OVERALL = 3.34, 7.0 + 0.09
SOCK_IN = RIM_OFF - SOCK_OVERALL * _S30 - SOCK_RO * _C30        # 1.5625 off the face
SOCK_OUT = RIM_OFF + SOCK_RO * _C30                              # 10.8925 off the face
SOCKS = [("Low", 310.0, 30.0 - SOCK_OVERALL * _C30 - SOCK_RO * _S30),    # (kind, Blue X, lowest Z 22.19)
         ("Mid", 338.0, 54.0 - SOCK_OVERALL * _C30 - SOCK_RO * _S30)]    # 46.19
CENTRELINE_X = 324.0
DEPOT_RGB = (0x7F, 0x7F, 0x7F)
SKY = 200.0

# CRAG tags: all eight faces' tags stand over the ring (VISION-GUIDE §3: Red ID = Blue ID + 13)
CRAG_TAGS = {"BLUE": tuple(range(6, 14)), "RED": tuple(range(19, 27))}

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


def rect(r):
    return [(r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3])]


def ring_prism(side, outer, inner, z0, z1):
    """Vertical prism over the Blue-world square ring outer - inner, mapped to `side`."""
    reg = K.Registry()
    K.mkPrismHoles(reg, K.Id(("ring",)), WF, PL_XY, [list(rp(side, p)) for p in rect(outer)],
                   [[list(rp(side, p)) for p in rect(inner)]], z0, z1)
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
    """O2 CELL envelope (5.0 dia x 14.0 cylinder) lying on the floor, axis 'x' or 'y' (Blue)."""
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


def sdist(a, b):
    return K.BRepExtrema_DistShapeShape(K._compound(a), K._compound(b)).Value()


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


def crag_frame(f, side):
    """CRAG-local frame from §1.1: +x along the SHELF FACE normal (Blue -X world), z up."""
    if side == "BLUE":
        return f.frame((324.0, 240.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
    return f.frame((324.0, 84.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))


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

    def hitstr(hit):
        return "; ".join("%s %.5f" % h for h in hit) or "clear"

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
            add(S + nm_ + " is one body / one solid (a continuous ring round all four faces)",
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
        fpx = ext(side, tw, 338, 239.99, 7.99, 358, 240.01, 8.01)
        fyn = ext(side, tw, 323.99, 206, 7.99, 324.01, 226, 8.01)
        fyp = ext(side, tw, 323.99, 254, 7.99, 324.01, 274, 8.01)
        face_x = fx[0] if fx else None
        face_p = fpx[3] if fpx else None
        face_yn = fyn[1] if fyn else None    # outer surface of the -Y panel
        face_yp = fyp[4] if fyp else None    # outer surface of the +Y panel
        add(S + "as-built CRAG faces: SHELF FACE X 300, PEG FACE X 348, SOCKET FACES Y 216 / 264 (Blue)",
            near(face_x, SHELF_X, 1e-4) and near(face_p, PEG_X, 1e-4) and near(face_yn, SOCK_YN, 1e-4) and near(face_yp, SOCK_YP, 1e-4),
            "SHELF %s, PEG %s, -Y %s, +Y %s (Blue-equivalent)" % (fmt(face_x), fmt(face_p), fmt(face_yn), fmt(face_yp)))
        face_x = face_x if face_x is not None else SHELF_X
        face_p = face_p if face_p is not None else PEG_X
        face_yn = face_yn if face_yn is not None else SOCK_YN
        face_yp = face_yp if face_yp is not None else SOCK_YP

        # ---------- B. floor ------------------------------------------------------------------
        fb = rbox_back(side, f.bbox(floor))
        add(S + "floor laid on the carpet (bottom Z = 0) with its top at Z = 0.25",
            near(fb[2], 0.0, 1e-6) and near(fb[5], FLOOR_T, 1e-6), "floor Z %.4f .. %.4f" % (fb[2], fb[5]))
        ring_all = ring_prism(side, CHAN, FOOT, 0, FLOOR_T)
        v_f, v_r = vol(fs), vol(ring_all)
        v_c = cvol(fs, ring_all)
        symdiff = v_f + v_r - 2 * v_c
        add(S + "floor plan is exactly the ring: four legs and four corner squares (80 x 80 less the 48 x 48 CRAG footprint)",
            abs(symdiff) < 1e-4, "symmetric-difference volume %.6f in^3 (floor %.4f, expected %.4f)" % (symdiff, v_f, v_r))
        add(S + "tray area 80^2 - 48^2 = 4096 in^2", near(v_f / FLOOR_T, TRAY_AREA, 1e-3), "floor area %.4f in^2" % (v_f / FLOOR_T))
        for pname, r in LEGS + SQUARES:
            want = (r[2] - r[0]) * (r[3] - r[1]) * FLOOR_T
            got = cvol(fs, box(side, r[0], r[1], 0, r[2], r[3], FLOOR_T))
            add(S + "floor covers the " + pname, near(got, want, 1e-4), "covered %.4f of %.4f in^3" % (got, want))
        foot = box(side, FOOT[0], FOOT[1], -1, FOOT[2], FOOT[3], 100)
        add(S + "no tray part enters the CRAG footprint", cvol(tray_s, foot) < 1e-6,
            "overlap %.6f in^3" % cvol(tray_s, foot))
        edges = [("SHELF FACE", ext(side, fs, 295, 239.99, 0.1, 305, 240.01, 0.15), 3, face_x),
                 ("PEG FACE", ext(side, fs, 343, 239.99, 0.1, 353, 240.01, 0.15), 0, face_p),
                 ("-Y SOCKET FACE", ext(side, fs, 323.99, 211, 0.1, 324.01, 221, 0.15), 4, face_yn),
                 ("+Y SOCKET FACE", ext(side, fs, 323.99, 259, 0.1, 324.01, 269, 0.15), 1, face_yp)]
        bad = [(n, fmt(e[k] if e else None), fmt(w)) for n, e, k, w in edges if not (e and near(e[k], w, 1e-4))]
        d_ft = f.dist(floor, base)
        add(S + "floor meets all four CRAG faces / the flush kick-guard (no gap a piece could drop into)",
            not bad and d_ft < 1e-6, "floor-to-CRAG gap %.6f; edges off their face %s" % (d_ft, bad or "none"))

        # ---------- C. lip ---------------------------------------------------------------------
        lb = rbox_back(side, f.bbox(lip))
        add(S + "lip top 4.0 above the carpet (CRITICAL)", near(lb[5], LIP_Z, 1e-6) and near(lb[2], 0, 1e-6),
            "lip Z %.4f .. %.4f" % (lb[2], lb[5]))
        add(S + "lip top 3.75 above the tray floor", near(lb[5] - fb[5], LIP_Z - FLOOR_T, 1e-6),
            "lip top - floor top = %.4f" % (lb[5] - fb[5]))
        add(S + "outer footprint over the lip 81.5 in square, centred on the CRAG (Blue X 283.25-364.75, Y 199.25-280.75)",
            all(near(a, b, 1e-4) for a, b in zip((lb[0], lb[1], lb[3], lb[4]), LIP_OUT)),
            "lip plan X %.4f-%.4f Y %.4f-%.4f" % (lb[0], lb[3], lb[1], lb[4]))
        ring_o = prism(side, rect(LIP_OUT), 0, LIP_Z)
        ring_i = prism(side, rect(CHAN), 0, LIP_Z)
        area_band = (vol(ring_o) - vol(ring_i)) / LIP_Z
        inside_band = cvol(ls, ring_o) - cvol(ls, ring_i)
        add(S + "lip lies entirely in the 0.75-in band outside the channel (no lip inside the channel)",
            cvol(ls, ring_i) < 1e-6 and near(inside_band, vol(ls), 1e-4),
            "lip vol %.4f, in band %.4f, in channel %.6f" % (vol(ls), inside_band, cvol(ls, ring_i)))
        mid_o = prism(side, rect(LIP_OUT), 1.0, 3.0)
        mid_i = prism(side, rect(CHAN), 1.0, 3.0)
        got_mid = cvol(ls, mid_o) - cvol(ls, mid_i)
        add(S + "lip fills the whole band all round (four legs, four corner squares) at mid-height",
            near(got_mid, area_band * 2.0, 1e-3), "band area %.4f in^2, lip section Z1-3 %.4f in^3 (want %.4f)"
            % (area_band, got_mid, area_band * 2.0))

        # stations: (label, probe box in Blue coords, axis, crag face position, sign of 'outward')
        stations = []
        for y in (226.0, 240.0, 254.0):
            stations.append(("SHELF FACE leg @Y%g" % y, (270, y - 0.01, 1.99, 300, y + 0.01, 2.01), 0, face_x, -1))
            stations.append(("PEG FACE leg @Y%g" % y, (348, y - 0.01, 1.99, 380, y + 0.01, 2.01), 0, face_p, +1))
        for x in (310.0, 324.0, 338.0):
            stations.append(("-Y SOCKET FACE leg @X%g" % x, (x - 0.01, 190, 1.99, x + 0.01, 216, 2.01), 1, face_yn, -1))
            stations.append(("+Y SOCKET FACE leg @X%g" % x, (x - 0.01, 264, 1.99, x + 0.01, 290, 2.01), 1, face_yp, +1))
        for x, fxv, sx in ((292.0, face_x, -1), (356.0, face_p, +1)):
            lo_x, hi_x = (270, 300) if sx < 0 else (348, 380)
            for y, fyv, sy in ((208.0, face_yn, -1), (272.0, face_yp, +1)):
                lo_y, hi_y = (190, 216) if sy < 0 else (264, 290)
                q = "%s / %s corner square" % ("SHELF FACE" if sx < 0 else "PEG FACE", "-Y" if sy < 0 else "+Y")
                stations.append((q + " across Y @X%g" % x, (x - 0.01, lo_y, 1.99, x + 0.01, hi_y, 2.01), 1, fyv, sy))
                stations.append((q + " across X @Y%g" % y, (lo_x, y - 0.01, 1.99, hi_x, y + 0.01, 2.01), 0, fxv, sx))
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
        # lip walls plumb (inner face the same at Z 0.5 and 3.5), on the SHELF and PEG sides
        for lab, (x0, x1) in (("SHELF side", (270, 300)), ("PEG side", (348, 380))):
            e1 = ext(side, ls, x0, 239.99, 0.49, x1, 240.01, 0.51)
            e2 = ext(side, ls, x0, 239.99, 3.49, x1, 240.01, 3.51)
            add(S + "lip walls plumb (inner/outer faces identical at Z 0.5 and 3.5), " + lab,
                e1 and e2 and near(e1[0], e2[0], 1e-5) and near(e1[3], e2[3], 1e-5),
                "Z0.5 %s / Z3.5 %s" % (e1 and [round(v, 4) for v in (e1[0], e1[3])], e2 and [round(v, 4) for v in (e2[0], e2[3])]))

        # lip top-edge radius R0.25 on every top edge (outer and inner) of every side
        k = math.sqrt(2) - 1
        o = LIP_T
        edges = [  # (label, sharp-corner point, direction into the lip along the top)
            ("outer SHELF side", (284 - o, 240), (+1, 0)), ("inner SHELF side", (284, 240), (-1, 0)),
            ("outer PEG side", (364 + o, 240), (-1, 0)), ("inner PEG side", (364, 240), (+1, 0)),
            ("outer -Y side", (324, 200 - o), (0, +1)), ("inner -Y side", (324, 200), (0, -1)),
            ("outer +Y side", (324, 280 + o), (0, -1)), ("inner +Y side", (324, 280), (0, +1)),
            ("outer -Y side at the SHELF FACE / -Y corner square", (292, 200 - o), (0, +1)),
            ("inner PEG side at the PEG FACE / +Y corner square", (364, 272), (+1, 0)),
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
        want_cb = [CHAMF_OUT[0], CHAMF_OUT[1], 0, CHAMF_OUT[2], CHAMF_OUT[3], CHAMF]
        add(S + "entry chamfer strip: 1.0 tall, 1.0 beyond the lip outer face all round (83.5 square plan envelope)",
            all(abs(a - b) < 1e-4 for a, b in zip(cb, want_cb)),
            "bbox %s want %s" % ([round(v, 4) for v in cb], want_cb))
        csta = [  # (label, lip outer face point, outward unit vector)
            ("SHELF side", (284 - o, 240), (-1, 0)), ("PEG side", (364 + o, 240), (+1, 0)),
            ("-Y side", (324, 200 - o), (0, -1)), ("+Y side", (324, 280 + o), (0, +1)),
            ("-Y side at the SHELF FACE / -Y corner square", (292, 200 - o), (0, -1)),
            ("PEG side at the PEG FACE / +Y corner square", (364 + o, 272), (+1, 0)),
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
        # chamfer volume: triangular section 0.5 in^2 along the four 81.5-in lip sides, hip-mitred at the
        # four convex corners (each corner block c^3 / 3)
        bh = (LIP_OUT[2] - LIP_OUT[0]) / 2
        want_cv = 4 * bh * CHAMF * CHAMF + 4 * CHAMF ** 3 / 3.0
        add(S + "entry chamfer continuous round the whole lip, hip-mitred at the four corners (volume check)",
            near(vol(cs), want_cv, 1e-3), "volume %.4f, 45-deg 1.0 strip round the 81.5 square gives %.4f" % (vol(cs), want_cv))
        add(S + "entry chamfer abuts the lip (touching, no overlap) and leaves the lip's plan untouched",
            f.dist(chamf, lip) < 1e-6 and f.common_volume(chamf, lip) < 1e-6 and cvol(cs, ring_o) < 1e-6,
            "chamfer-lip gap %.6f, overlap %.6f, chamfer inside the lip outline %.6f"
            % (f.dist(chamf, lip), f.common_volume(chamf, lip), cvol(cs, ring_o)))
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

        # ---------- F. interference, contact, tape, APRON -------------------------------------------
        for nm_, rs in (("floor", floor), ("lip", lip), ("entry chamfer", chamf)):
            hit = C.hits(f.solids(rs), exclude=lambda r: is_tray(r))
            add(S + nm_ + " shares no volume with any other field body", not hit, hitstr(hit))
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
        add(S + "no tape runs under or through the tray (centerline and CENTER CACHE band broken, APRON clear)",
            not tape_hit, ("; ".join("%s %.6f" % h for h in tape_hit) or "clear")
            + "; nearest tape %s at %.4f in" % (dname, dmin))
        add(S + "the tray crosses the FIELD centerline X = 324 (both SOCKET FACE legs span it)",
            cb[0] < CENTRELINE_X < cb[3] and fb[0] < CENTRELINE_X < fb[3], "tray X %.4f-%.4f" % (cb[0], cb[3]))
        try:
            cl = f.find("FIELD centerline tape")
            env = box(side, CHAMF_OUT[0], CHAMF_OUT[1], -1, CHAMF_OUT[2], CHAMF_OUT[3], 1)
            vcl = cvol(f.solids(cl), env)
            dcl = f.dist(cl, chamf + lip + floor)
            add(S + "no FIELD centerline tape inside the tray's 83.5-in plan envelope (the line is broken across it)",
                vcl < 1e-9 and dcl > 1e-6, "centerline in the envelope %.2e in^3; nearest centerline tape %.4f in from the tray" % (vcl, dcl))
        except KeyError as e:
            add(S + "FIELD centerline tape present", False, str(e))
        # tray entirely inside the CRAG APRON line (36 / 20 offsets, R20 corners)
        cpts = [(CHAMF_OUT[0], CHAMF_OUT[1]), (CHAMF_OUT[0], CHAMF_OUT[3]), (CHAMF_OUT[2], CHAMF_OUT[1]), (CHAMF_OUT[2], CHAMF_OUT[3])]
        ac = [(SHELF_X - APRON_SHELF + APRON_R, SOCK_YN - APRON_SOCK + APRON_R), (SHELF_X - APRON_SHELF + APRON_R, SOCK_YP + APRON_SOCK - APRON_R),
              (PEG_X + APRON_SHELF - APRON_R, SOCK_YN - APRON_SOCK + APRON_R), (PEG_X + APRON_SHELF - APRON_R, SOCK_YP + APRON_SOCK - APRON_R)]
        rr = [math.hypot(p[0] - c[0], p[1] - c[1]) for p, c in zip(cpts, ac)]
        add(S + "tray (to the chamfer toe) lies inside its CRAG APRON line incl. the R20 corners",
            all(x < APRON_R for x in rr) and cb[0] > SHELF_X - APRON_SHELF and cb[3] < PEG_X + APRON_SHELF
            and cb[1] > SOCK_YN - APRON_SOCK and cb[4] < SOCK_YP + APRON_SOCK,
            "chamfer outer corners at R %s from the apron arc centres (arc R20)" % ", ".join("%.3f" % x for x in rr))
        try:
            apron = f.solids(f.find(side + " CRAG APRON tape"))
            d_all = sdist(cs, apron)
            runs = common(apron, box(side, SHELF_X, 150, -1, PEG_X, 330, 1))
            d_run = sdist(cs, runs) if runs else None
            add(S + "clear of the APRON tape by 0.25 in along the SOCKET FACES and 0.16 in at the corner arcs (chamfer toe 17.75, tape inner edge 18.0 / R18)",
                near(d_run, TAPE_GAP_SOCK, 1e-4) and near(d_all, TAPE_GAP_ARC, 1e-3) and d_all > 0,
                "along the SOCKET FACE runs %s; nearest (corner arcs) %.4f (want %.4f)" % (fmt(d_run), d_all, TAPE_GAP_ARC))
        except KeyError as e:
            add(S + "CRAG APRON tape present", False, str(e))

        # ---------- G. overhead clearances, open-to-sky -------------------------------------------
        chan_low = ring_prism(side, CHAN, FOOT, FLOOR_T + 1e-3, GUSSET_FLOOR1)
        hit = C.hits(chan_low, exclude=is_tray)
        add(S + "channel empty from the floor to Z 19.0 everywhere (any SUPPLY can be pushed round the whole ring)",
            not hit, hitstr(hit))
        s1 = f.find(side + " CRAG Shelf 1")
        s1b = rbox_back(side, f.bbox(s1))
        add(S + "Shelf 1 underside 23.25 above the carpet (CRITICAL clearance for pushed SUPPLIES)",
            near(s1b[2], SHELF1_UNDER, 1e-4), "Shelf 1 slab Z min %.4f" % s1b[2])
        add(S + "Shelf 1 plan footprint (Blue X 286-300) lies inside the SHELF FACE leg (X 284-300)",
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
        add(S + "over the SHELF FACE leg nothing but gussets comes below the Shelf 1 underside (23.25)",
            not hit, hitstr(hit))
        lo = 1e9
        legbox = box(side, 284, 216, FLOOR_T + 1e-3, 300, 264, 30)
        legbb = bb(legbox)
        for r in C.recs:
            if is_tray(r) or not overlaps(C.bbs[r["id"]], legbb):
                continue
            e = rbox_back(side, bb(common(r["solids"], legbox)))
            if e is not None:
                lo = min(lo, e[2])
        add(S + "lowest structure over the SHELF FACE leg is >= 19.0 (clearance >= 18.75 over the floor)",
            lo >= GUSSET_FLOOR1 - 1e-6, "lowest overhead point Z %.4f (%.4f above the tray floor)" % (lo, lo - FLOOR_T))

        eps = 0.01
        yn_in, yn_out = SOCK_YN - SOCK_IN, SOCK_YN - SOCK_OUT      # -Y tube plan band (Blue)
        yp_in, yp_out = SOCK_YP + SOCK_IN, SOCK_YP + SOCK_OUT
        low_x1, mid_x0 = SOCKS[0][1] + SOCK_RO, SOCKS[1][1] - SOCK_RO
        peg_reach = PEG_EXP * math.cos(math.radians(45)) + PEG_OD / 2      # bound on a peg's plan reach
        sky = [("outer 2.0-in strip of the SHELF FACE leg (48 x 2)", (284 + eps, 216, 286 - eps, 264))]
        sky += [(nm_ + ", fully clear", (r[0] + eps, r[1] + eps, r[2] - eps, r[3] - eps)) for nm_, r in SQUARES]
        sky += [("-Y SOCKET FACE leg between the Low and Mid Socket tubes (X %.2f-%.2f)" % (low_x1, mid_x0), (low_x1 + eps, 200 + eps, mid_x0 - eps, 216)),
                ("+Y SOCKET FACE leg between the Low and Mid Socket tubes (X %.2f-%.2f)" % (low_x1, mid_x0), (low_x1 + eps, 264, mid_x0 - eps, 280 - eps)),
                ("-Y SOCKET FACE leg: the %.2f-in strip along the lip, outboard of both tubes" % (yn_out - 200), (300, 200 + eps, 348, yn_out - eps)),
                ("+Y SOCKET FACE leg: the %.2f-in strip along the lip, outboard of both tubes" % (280 - yp_out), (300, yp_out + eps, 348, 280 - eps)),
                ("PEG FACE leg outboard of the peg tips (X %.2f-364)" % (PEG_X + peg_reach), (PEG_X + peg_reach + eps, 216, 364 - eps, 264))]
        for lab, (x0, y0, x1, y1) in sky:
            hit = C.hits(box(side, x0, y0, FLOOR_T + 1e-3, x1, y1, SKY), exclude=is_tray)
            add(S + "open to the sky: " + lab, not hit, hitstr(hit))
        for lab, r, allow in (("-Y SOCKET FACE leg", LEGS[2][1], ("Socket",)), ("+Y SOCKET FACE leg", LEGS[3][1], ("Socket",)),
                              ("PEG FACE leg", LEGS[1][1], ("Low Peg", "Mid Peg"))):
            hit = C.hits(box(side, r[0] + eps, r[1] + eps, FLOOR_T + 1e-3, r[2] - eps, r[3] - eps, SKY), exclude=is_tray)
            others = [h for h in hit if not any(a in h[0] for a in allow)]
            over = sorted({h[0] for h in hit})
            add(S + "over the %s only %s come overhead" % (lab, "the side-socket tubes and their brackets" if allow[0] == "Socket"
                                                          else "the Low and Mid Pegs"),
                not others and len(over) >= 2, "overhead: %s" % (over or "nothing"))
        hp = f.find(side + " CRAG High Peg (guardrail side)") + f.find(side + " CRAG High Peg (center side)")
        hpb = rbox_back(side, f.bbox(hp))
        add(S + "the High Pegs (spire face 14.0 inboard of the PEG FACE) do not reach over the tray",
            hpb[3] < PEG_X, "High Peg plan X to %.4f (PEG FACE X %.1f)" % (hpb[3], PEG_X))
        # the side-socket tube overhang, as published
        for kind, xc, zmin in SOCKS:
            tubes = f.find(side + " CRAG %s Socket (guardrail side)" % kind) + f.find(side + " CRAG %s Socket (center side)" % kind)
            for lab, r, sil in (("+Y", LEGS[3][1], (xc - SOCK_RO, yp_in, xc + SOCK_RO, yp_out)),
                                ("-Y", LEGS[2][1], (xc - SOCK_RO, yn_out, xc + SOCK_RO, yn_in))):
                e = ext(side, f.solids(tubes), r[0], r[1], 0, r[2], r[3], SKY)
                ok = e is not None and all(abs(a - b) < 0.02 for a, b in zip((e[0], e[1], e[3], e[4]), sil)) and abs(e[2] - zmin) < 0.01
                add(S + "%s Socket tube overhangs the %s SOCKET FACE leg at X %.2f-%.2f x Y %.2f-%.2f from Z %.2f"
                    % (kind, lab, sil[0], sil[2], sil[1], sil[3], zmin),
                    ok, "tube over the leg: %s" % ([round(v, 3) for v in e] if e else None))
        # drop tests
        drops = [(nm_, ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)) for nm_, r in SQUARES]
        drops += [("PEG FACE leg between the pegs", (356.0, 240.0)),
                  ("-Y SOCKET FACE leg between the socket tubes", (324.0, 208.0)),
                  ("+Y SOCKET FACE leg between the socket tubes", (324.0, 272.0))]
        for lab, (cx_, cy_) in drops:
            col = box(side, cx_ - CRATE_ENV / 2, cy_ - CRATE_ENV / 2, FLOOR_T + 1e-3, cx_ + CRATE_ENV / 2, cy_ + CRATE_ENV / 2, SKY)
            hit = C.hits(col, exclude=is_tray)
            add(S + "a crowned CRATE can be dropped straight into the " + lab, not hit,
                hitstr(hit) if hit else "13.0 x 13.0 column clear to the sky")
        blocked = []
        for kind, xc, _ in SOCKS:
            for yc in ((yn_in + yn_out) / 2, (yp_in + yp_out) / 2):
                col = box(side, xc - CRATE_ENV / 2, yc - CRATE_ENV / 2, FLOOR_T + 1e-3, xc + CRATE_ENV / 2, yc + CRATE_ENV / 2, SKY)
                ccol = cyl_column(side, xc, yc, COIL_OD, FLOOR_T + 1e-3, SKY)
                hc = [h[0] for h in C.hits(col, exclude=is_tray) if "%s Socket" % kind in h[0]]
                ho = [h[0] for h in C.hits(ccol, exclude=is_tray) if "%s Socket" % kind in h[0]]
                blocked.append((kind, round(yc, 2), bool(hc), bool(ho)))
        add(S + "no CRATE or COIL can be dropped straight in under any of the four side-socket tubes",
            all(b[2] and b[3] for b in blocked), "(socket, Y, crate column blocked, coil column blocked) %s" % blocked)

        # ---------- H. virtual SUPPLIES ------------------------------------------------------------
        tag_bot = {}
        for tid in CRAG_TAGS[side]:
            try:
                pr = f.find(r"re:^AprilTag %d - " % tid)
                tag_bot[tid] = f.bbox(pr)[2] + (TAG_PANEL - TAG_TARGET) / 2
            except KeyError:
                tag_bot[tid] = None
        placements = [(nm_, ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)) for nm_, r in SQUARES]
        placements += [("SHELF FACE leg @Y%g" % y, (292.0, y)) for y in (226.0, 240.0, 254.0)]
        placements += [("PEG FACE leg @Y%g" % y, (356.0, y)) for y in (226.0, 240.0, 254.0)]
        placements += [("%s SOCKET FACE leg @X%g%s" % (s_, x, {310.0: " under the Low Socket", 338.0: " under the Mid Socket"}.get(x, "")), (x, y))
                       for s_, y in (("-Y", 208.0), ("+Y", 272.0)) for x in (310.0, 324.0, 338.0)]
        chan_col = ring_prism(side, CHAN, FOOT, 0, 40)
        bad = []
        for lab, (x, y) in placements:
            cr = crate_at(side, x, y)
            b = rbox_back(side, bb_exact(cr))
            hit = C.hits(cr)
            inproj = cvol(cr, chan_col)
            if hit or not near(inproj, vol(cr), 1e-3) or not near(b[2], FLOOR_T, 1e-4) or not near(b[5], CRATE_TOP_IN_TRAY, 1e-4):
                bad.append((lab, [h[0] for h in hit], round(100 * inproj / vol(cr), 2), round(b[2], 4), round(b[5], 4)))
        add(S + "a crowned CRATE stands anywhere round the ring (4 corner squares, 3 stations on each leg): fits, inside the channel projection, top 13.25",
            not bad, "problems %s" % bad if bad else "%d placements clear" % len(placements))
        cr = crate_at(side, 292, 240)
        top = bb_exact(cr)[5]
        for tid, tb_ in tag_bot.items():
            add(S + "CRATE in the tray (top %.2f) stays below tag %d's target bottom (13.44), margin 0.19" % (CRATE_TOP_IN_TRAY, tid),
                tb_ is not None and near(tb_, TARGET_BOT, 1e-3) and top < tb_ and near(tb_ - top, TARGET_BOT - CRATE_TOP_IN_TRAY, 1e-3),
                "crate top %.4f, as-built target bottom %s, margin %s" % (top, fmt(tb_), fmt(tb_ - top if tb_ else None)))
        lipb = rbox_back(side, f.bbox(lip))
        add(S + "no part of the tray can occlude a CRAG tag (tray top below every panel on all four faces)",
            all(tb_ is not None and lipb[5] < tb_ - (TAG_PANEL - TAG_TARGET) / 2 for tb_ in tag_bot.values()),
            "tray top %.3f vs panel bottoms %s" % (lipb[5], [fmt(v - (TAG_PANEL - TAG_TARGET) / 2) if v else None for v in tag_bot.values()]))

        # eighteen crates one abreast: 6 along each 80-in run (SHELF and PEG FACE legs with their corner
        # squares), 3 along each 48-in SOCKET FACE leg
        g80 = (80.0 - 6 * CRATE_ENV) / 7
        g48 = (48.0 - 3 * CRATE_ENV) / 4
        pos = [(x, 200 + g80 + CRATE_ENV / 2 + i * (CRATE_ENV + g80)) for x in (292.0, 356.0) for i in range(6)]
        pos += [(300 + g48 + CRATE_ENV / 2 + i * (CRATE_ENV + g48), y) for y in (208.0, 272.0) for i in range(3)]
        crates = [crate_at(side, x, y) for x, y in pos]
        bad = []
        for i, cr in enumerate(crates):
            h = C.hits(cr)
            if h or not near(cvol(cr, chan_col), vol(cr), 1e-3):
                bad.append((pos[i], [x[0] for x in h]))
        pair = 0.0
        cbb = [bb(c) for c in crates]
        for i in range(len(crates)):
            for j in range(i + 1, len(crates)):
                if overlaps(cbb[i], cbb[j]):
                    pair = max(pair, cvol(crates[i], crates[j]))
        add(S + "about 18 CACHE CRATES fit one abreast in a single layer (6 + 6 along the two 80-in runs, 3 + 3 along the SOCKET FACE legs)",
            not bad and pair < 1e-6 and len(crates) == 18 and 18 * CRATE_ENV ** 2 <= v_f / FLOOR_T,
            "problems %s; max crate-crate overlap %.6f; gaps %.3f / %.3f; %d x 13.0^2 = %.0f of %.0f in^2"
            % (bad or "none", pair, g80, g48, len(crates), len(crates) * CRATE_ENV ** 2, v_f / FLOOR_T))
        # a mixed load of 27 SUPPLIES in a single layer: 8 along each 80-in run, 6 and 5 along the legs
        run80 = [("crate", 206.7), ("crate", 219.9), ("cellx", 229.1), ("cellx", 234.3), ("coil", 242.0), ("coil", 252.2),
                 ("cellx", 259.9), ("crate", 269.1)]
        mix = [(k_, (x, y)) for x in (292.0, 356.0) for k_, y in run80]
        mix += [(k_, (x, 208.0)) for k_, x in (("coil", 305.5), ("celly", 313.5), ("coil", 321.5), ("celly", 329.5),
                                                ("coil", 337.5), ("celly", 345.5))]
        mix += [(k_, (x, 272.0)) for k_, x in (("crate", 307.0), ("coil", 319.0), ("celly", 327.0), ("coil", 335.0),
                                                ("celly", 343.0))]
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
        pbb = [bb(p) for p in pieces]
        pair = 0.0
        for i in range(len(pieces)):
            for j in range(i + 1, len(pieces)):
                if overlaps(pbb[i], pbb[j]):
                    pair = max(pair, cvol(pieces[i], pieces[j]))
        counts = {k_: sum(1 for m in mix if m[0].startswith(k_)) for k_ in ("crate", "cell", "coil")}
        add(S + "about 27 SUPPLIES fit as a mixed single layer (%d crates, %d cells, %d coils, all on the floor)"
            % (counts["crate"], counts["cell"], counts["coil"]),
            not bad and pair < 1e-6 and len(mix) == 27, "problems %s; max piece-piece overlap %.6f" % (bad or "none", pair))
        # other standing heights from VISION-GUIDE §1.3
        cu = cell_upright(side, 292, 240)
        bcu = bb(cu)
        hit = C.hits(cu)
        add(S + "O2 CELL stood on end in the DEPOT tops out at 14.25 (VISION-GUIDE §1.3) and fits under Shelf 1",
            near(bcu[5], FLOOR_T + CELL_L, 1e-4) and not hit,
            "top %.4f (%.4f into the 13.44 target band); hits %s" % (bcu[5], bcu[5] - TARGET_BOT, [h[0] for h in hit] or "none"))
        cl_ = cell_lying(side, 292, 240, "x")
        add(S + "O2 CELL lying in the DEPOT tops out at 5.25 (VISION-GUIDE §1.3)", near(bb(cl_)[5], 5.25, 1e-4),
            "top %.4f" % bb(cl_)[5])

        # ---------- I. robot standoff and reach -----------------------------------------------------
        offs = {"SHELF FACE": SHELF_X - lb[0], "PEG FACE": lb[3] - PEG_X, "-Y SOCKET FACE": SOCK_YN - lb[1], "+Y SOCKET FACE": lb[4] - SOCK_YP}
        add(S + "robot standoff on every face: lip outer face 16.75 off the face -> FRAME PERIMETER 19.75",
            all(near(v, CH + LIP_T, 1e-4) for v in offs.values()),
            "; ".join("%s %.4f -> %.4f" % (k_, v, v + BUMPER) for k_, v in offs.items()))
        frame = CH + LIP_T + BUMPER
        # peg tips measured along each peg's own axis from its documented root
        CF = crag_frame(f, side)
        u_loc = (-math.cos(math.radians(45)), 0.0, math.sin(math.radians(45)))
        tipx = {}
        for kind, roots in (("Low", [(-24.0, s_ * PEG_ROOTS["Low"][1], PEG_ROOTS["Low"][0]) for s_ in (-1, 1)]),
                            ("Mid", [(-24.0, s_ * PEG_ROOTS["Mid"][1], PEG_ROOTS["Mid"][0]) for s_ in (-1, 1)]),
                            ("High", [(-10.0, s_ * HPEG[1], HPEG[0]) for s_ in (-1, 1)])):
            recs = f.find(side + " CRAG %s Peg (guardrail side)" % kind) + f.find(side + " CRAG %s Peg (center side)" % kind)
            outs = []
            for root in roots:
                wroot = CF.pt(root)
                wmid = CF.pt([root[i] + 5.0 * u_loc[i] for i in range(3)])
                rec = min(recs, key=lambda r: sum((a - b) ** 2 for a, b in zip(
                    [(C.bbs[r["id"]][i] + C.bbs[r["id"]][i + 3]) / 2 for i in range(3)], wmid)))
                P = f.frame(tuple(wroot), tuple(CF.dir((0.0, 1.0, 0.0))), tuple(CF.dir(u_loc)))
                zmax = f.bbox([rec], P)[5]
                outs.append(zmax * math.cos(math.radians(45)) - (root[0] + 24.0))   # tip beyond the PEG FACE plane
            tipx[kind] = max(outs)
        reach = {"shelf": frame - SLOT_X_OFF, "summit": frame - RIM_OFF, "sock": frame - RIM_OFF,
                 "peg_tip": frame - max(tipx["Low"], tipx["Mid"]), "peg_root": frame,
                 "hpeg_tip": frame - tipx["High"], "hpeg_root": frame + HPEG_INBOARD}
        add(S + "reach from the lip: Shelf slot 12.75, Summit rim 11.75, Low and Mid Socket rims 11.75",
            all(near(reach[k_], REACH_DOC[k_], 1e-4) for k_ in ("shelf", "summit", "sock")),
            "slot %.4f, Summit rim %.4f, side rims %.4f" % (reach["shelf"], reach["summit"], reach["sock"]))
        add(S + "reach from the lip: Low and Mid Peg tips 12.68 (roots 19.75), High Peg tip 26.68 (root 33.75), measured along each peg",
            all(near(reach[k_], REACH_DOC[k_], 0.006) for k_ in ("peg_tip", "peg_root", "hpeg_tip", "hpeg_root")),
            "peg tip %.4f, root %.4f; High Peg tip %.4f, root %.4f" % (reach["peg_tip"], reach["peg_root"], reach["hpeg_tip"], reach["hpeg_root"]))
        tips = [reach[k_] for k_ in ("shelf", "summit", "sock", "peg_tip", "hpeg_tip")]
        add(S + "binding reach is the High Peg tip, 26.68 of the 30 in allowed on the own CRAG APRON (G404); the High Peg root is beyond it",
            max(tips) == reach["hpeg_tip"] and reach["hpeg_tip"] <= REACH_APRON and reach["hpeg_root"] > REACH_APRON,
            "largest reach %.4f (High Peg tip); High Peg root %.4f vs %.1f" % (max(tips), reach["hpeg_root"], REACH_APRON))
    return out
