# -*- coding: utf-8 -*-
"""
CRAG SOCKET FACES — the Low and Mid Sockets and their brackets, on both SOCKET FACES of
both CRAGS (8 tubes, 8 brackets).

Every expected value below is taken from the package documents, never from src/:

  FIELD-CAD-PACKAGE  §0   conventions: inches, NWU always-blue-origin, (ref) floats +/-0.25,
                          "every angle on the field is 15, 30 or 45 degrees"
                     §1.1 CRAG centres (324, 240) / (324, 84); SHELF FACE normal -X Blue / +X Red;
                          SOCKET FACES are the two +/-Y faces; 48 x 48 footprint
                     §2.3 every row (rims 30/54, lateral +/-14 with Low on the shelf-face side,
                          8.0 standoff normal to the face, 30 deg outward tilt, ID 6.50 +/- 0.125,
                          7.0 tube with closed bottom, wall 0.09) and both clearance paragraphs
                          (4.50 / 1.61 / Z 22.27 / 7.0 protrusion / 6.06 / 1.67 / 4.39; robot
                          standoff 16.75 / 19.75 / 11.75 / 5.0) and the attachment rule
                     §2.6/§8 tier rings 1.0 wide, centred on 30 and 54, band 77-78 for the 78 ring
                     §3   BASE DEPOT corner arm (16 x 16 along each SOCKET FACE), lip 0.75,
                          open-to-sky figures (X 306.7-313.3 x Y 265.6-274.9, clear columns
                          6.66 / 2.66 / 5.11 / 1.61), crowned CRATE in the tray to Z 13.25 (§7)
                     §7   tag table (8/9 +Y, 10/11 -Y Blue; Red = Blue + 13), panel 9.0, target
                          8.125, centre Z 17.5, occlusion budget
                     §9.2 O2 CELL 5.0 dia x 14.0, 1.5-in domes
  DESIGN-SPEC        §1.5 socket ID 6.50 +/- 0.125;  §3 SOCKET FACES
  MATERIALS-AND-COLORS §1.2 `socket` #9DB8D6, `crag-accent` #4A3B22; §2 socket tube = rolled
                          aluminium, 0.09 wall; socket bracket = aluminium plate 0.125 in
  VISION-GUIDE       §1.3 (tube 1.61-10.89 outboard, "clear at every outboard station"),
                     §5.2 camera bands (primary 10-20 in, optional second camera 24-36 in),
                     §6.6 (Low above tag 8/10/21/23, Mid above 9/11/22/24)
"""
import json
import math
import os

import numpy as np

import kernel_occ as K
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeSphere
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Line, GeomAbs_Plane
from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Ax1, gp_Ax2, gp_Dir, gp_Lin, gp_Pnt, gp_Trsf, gp_Vec

# ---------------------------------------------------------------------------------------
# Document values
# ---------------------------------------------------------------------------------------
CRAG_C = {"BLUE": (324.0, 240.0), "RED": (324.0, 84.0)}      # §1.1
HALF = 24.0                                                  # 48 x 48 footprint
SHELF_X = {"BLUE": -1.0, "RED": +1.0}                        # §1.1 SHELF FACE normal (world X sign)
RIM_Z = {"Low": 30.0, "Mid": 54.0}                           # §2.3
LAT = 14.0                                                   # §2.3
STANDOFF = 8.0                                               # §2.3
TILT = 30.0                                                  # §2.3
ID_NOM, ID_TOL = 6.50, 0.125                                 # §2.3, DESIGN-SPEC §1.5
LEN = 7.0                                                    # §2.3
WALL = 0.09                                                  # §2.3 (ref), MATERIALS §2
RO = ID_NOM / 2 + WALL                                       # 3.34 — the package's own "3.34"
RI = ID_NOM / 2
S30, C30 = math.sin(math.radians(TILT)), math.cos(math.radians(TILT))

# §2.3 clearance paragraph (and VISION-GUIDE §1.3), written as the package derives them
BOTTOM_OUT = STANDOFF - LEN * S30                            # 4.50
INBOARD_EDGE = BOTTOM_OUT - RO * C30                         # 1.61
OUTBOARD_EDGE = STANDOFF + RO * C30                          # 10.89 (VISION-GUIDE §1.3)
LOWEST_BELOW_RIM = LEN * C30 + RO * S30                      # 30 - 22.27
UPHILL_LIP = RO * S30                                        # 1.67
DOC_PROTRUSION = 7.0                                         # §2.3 / DESIGN-SPEC §3
DOC_APEX_ABOVE_RIM = 6.06                                    # §2.3 (7.0 cos 30)
DOC_MOUTH_CLEAR = 4.39                                       # §2.3

TAG_Z, PANEL, TARGET, BODY = 17.5, 9.0, 8.125, 6.5           # §7
RING_BANDS = [(29.5, 30.5), (53.5, 54.5), (77.0, 78.0)]      # §2.6 / §8
BRACKET_T = 0.125                                            # MATERIALS §2 (socket bracket)
RGB_SOCKET = (0x9D, 0xB8, 0xD6)                              # MATERIALS §1.2 `socket`
RGB_ACCENT = (0x4A, 0x3B, 0x22)                              # MATERIALS §1.2 `crag-accent`
AL_DENSITY = (2650.0, 2850.0)                                # aluminium, kg/m^3
CELL_D, CELL_L, CELL_DOME = 5.0, 14.0, 1.5                   # §9.2
ARM, LIP_T = 16.0, 0.75                                      # §3
FRAME_BEHIND_BUMPER, REACH_LIMIT = 3.0, 18.0                 # §2.3 robot standoff paragraph
LOW_REACH, MID_REACH = 11.75, 5.0                            # §2.3
CRATE_TOP_IN_TRAY = 13.25                                    # §7
ARM_CLEAR_COLUMNS = [1.61, 2.66, 5.11, 6.66]                 # §3 open-to-sky

# §7 / VISION-GUIDE §3: tag under each socket (Low above the alliance-wall-side tag)
TAGS = {("BLUE", +1): {"Low": 8, "Mid": 9}, ("BLUE", -1): {"Low": 10, "Mid": 11},
        ("RED", -1): {"Low": 21, "Mid": 22}, ("RED", +1): {"Low": 23, "Mid": 24}}

TOL = 0.005          # model fidelity for CRITICAL geometry (the CAD model is nominal)
EPS = 1e-6


# ---------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------
def _v(p):
    return np.array([p.X(), p.Y(), p.Z()], float)


def _faces(shape):
    exp = K.TopExp_Explorer(shape, K.TopAbs_FACE)
    while exp.More():
        yield TopoDS.Face(exp.Current())
        exp.Next()


def _edges(shape):
    exp = K.TopExp_Explorer(shape, K.TopAbs_EDGE)
    while exp.More():
        yield TopoDS.Edge(exp.Current())
        exp.Next()


def _common(a, b):
    c = K.BRepAlgoAPI_Common(a, b)
    if not c.IsDone():
        return float("nan")
    return K._volume(K._solids(c.Shape()))


def _loose_box(shape):
    b = K.Bnd_Box()
    K.BRepBndLib.Add_s(shape, b, False)
    return K._box6(b)


def _overlap(a, b, pad=0.0):
    return not (a[0] > b[3] + pad or b[0] > a[3] + pad or a[1] > b[4] + pad or b[1] > a[4] + pad
                or a[2] > b[5] + pad or b[2] > a[5] + pad)


def _xform(shape, trsf):
    return K.BRepBuilderAPI_Transform(shape, trsf, True).Shape()


def _translate(shape, d):
    t = gp_Trsf()
    t.SetTranslation(gp_Vec(float(d[0]), float(d[1]), float(d[2])))
    return _xform(shape, t)


def _fmt(v):
    return "[" + ", ".join("%.4f" % x for x in v) + "]"


_CACHE = {}


def _all_boxes(f):
    key = id(f)
    if key not in _CACHE:
        _CACHE[key] = [(r, _loose_box(K._compound(r["solids"]))) for r in f.records() if r["solids"]]
    return _CACHE[key]


def _bodies_near(f, shape, exclude=()):
    bb = _loose_box(shape)
    ex = {id(r) for r in exclude}
    return [r for r, b in _all_boxes(f) if id(r) not in ex and _overlap(bb, b, 0.01)]


def _hits_any(f, shape, exclude=()):
    """[(name, common volume)] of every body sharing volume with `shape`."""
    out = []
    for r in _bodies_near(f, shape, exclude):
        v = sum(_common(shape, s) for s in r["solids"])
        if v > 1e-6 or v != v:
            out.append((r["name"], v))
    return out


def virtual_cell():
    """O2 CELL per §9.2: 5.0 dia x 14.0, 1.5-in spherical domes struck through pole and
    equator (the R1.0 cap fillet is omitted, which only makes the envelope larger).
    Local frame: axis +z, lower pole at the origin."""
    r = CELL_D / 2
    rs = (r * r + CELL_DOME * CELL_DOME) / (2 * CELL_DOME)
    body = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, CELL_DOME), gp_Dir(0, 0, 1)), r, CELL_L - 2 * CELL_DOME).Shape()
    cap0 = K.BRepAlgoAPI_Common(BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, rs), rs).Shape(),
                                BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), r, CELL_DOME).Shape()).Shape()
    cap1 = K.BRepAlgoAPI_Common(BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, CELL_L - rs), rs).Shape(),
                                BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, CELL_L - CELL_DOME), gp_Dir(0, 0, 1)), r, CELL_DOME).Shape()).Shape()
    s = K.BRepAlgoAPI_Fuse(K.BRepAlgoAPI_Fuse(body, cap0).Shape(), cap1).Shape()
    return s


class Socket:
    """Expected geometry of one socket, straight from §1.1 / §2.3."""

    def __init__(self, side, ny, kind):
        self.side, self.ny, self.kind = side, ny, kind
        cx, cy = CRAG_C[side]
        self.face_y = cy + ny * HALF
        self.n = np.array([0.0, ny, 0.0])                        # face outward normal
        lat_sign = SHELF_X[side] if kind == "Low" else -SHELF_X[side]
        self.lat_x = cx + lat_sign * LAT
        self.zr = RIM_Z[kind]
        self.rim = np.array([self.lat_x, self.face_y + ny * STANDOFF, self.zr])
        self.a = np.array([0.0, ny * S30, C30])                  # axis toward the mouth
        self.e2 = np.array([0.0, ny * C30, -S30])                # outboard-down, perpendicular to a
        self.e1 = np.cross(self.e2, self.a)
        self.label = "%s %sY %s Socket" % (side, "+" if ny > 0 else "-", kind)
        self.tag = TAGS[(side, ny)][kind]


def _analyse_tube(solid):
    cyl, planes, other = [], [], []
    for fc in _faces(solid):
        ad = BRepAdaptor_Surface(fc)
        p = K.GProp_GProps()
        K.BRepGProp.SurfaceProperties_s(fc, p)
        area, c = p.Mass(), _v(p.CentreOfMass())
        t = ad.GetType()
        if t == GeomAbs_Cylinder:
            cy = ad.Cylinder()
            cyl.append((cy.Radius(), _v(cy.Location()), _v(cy.Axis().Direction()), area))
        elif t == GeomAbs_Plane:
            planes.append((_v(ad.Plane().Axis().Direction()), c, area))
        else:
            other.append(t)
    return cyl, planes, other


_JSON = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "..", "..", "..", "04-vision", "apriltag-field-layout.json"))


def _json_tag(tid):
    """(position in inches, unit facing normal) of a tag in the published layout JSON."""
    try:
        with open(_JSON) as fh:
            data = json.load(fh)
    except OSError:
        return None
    for t in data["tags"]:
        if t["ID"] == tid:
            tr = t["pose"]["translation"]
            q = t["pose"]["rotation"]["quaternion"]
            yaw = 2 * math.atan2(q["Z"], q["W"])
            pos = np.array([tr["x"], tr["y"], tr["z"]]) / 0.0254
            return pos, np.array([math.cos(yaw), math.sin(yaw), 0.0])
    return None


def _line_dist(p0, d0, p1, d1):
    """distance between two (parallel) lines"""
    w = p1 - p0
    return float(np.linalg.norm(w - (w @ d0) * d0))


# ---------------------------------------------------------------------------------------
def run(f):
    out = []

    def add(label, ok, detail):
        out.append((label, bool(ok), detail))

    def near(label, got, want, tol, extra=""):
        add(label, abs(got - want) <= tol, "measured %.4f, expected %.4f +/- %g%s" % (got, want, tol, extra))

    sockets = [Socket(side, ny, kind) for side in ("BLUE", "RED") for ny in (+1, -1) for kind in ("Low", "Mid")]

    # ---- counts and naming ---------------------------------------------------------------
    recs = {}
    for side in ("BLUE", "RED"):
        for kind in ("Low", "Mid"):
            tubes = f.find("%s CRAG %s Socket" % (side, kind))
            brks = f.find("%s CRAG %s Socket bracket" % (side, kind))
            add("%s CRAG: 2 %s Socket tubes (one per SOCKET FACE), one solid each" % (side, kind),
                len(tubes) == 2 and all(len(r["solids"]) == 1 for r in tubes),
                "%d bodies, solids %s" % (len(tubes), [len(r["solids"]) for r in tubes]))
            add("%s CRAG: 2 %s Socket brackets, one solid each" % (side, kind),
                len(brks) == 2 and all(len(r["solids"]) == 1 for r in brks),
                "%d bodies, solids %s" % (len(brks), [len(r["solids"]) for r in brks]))
            recs[(side, kind, "tube")] = tubes
            recs[(side, kind, "brk")] = brks
    allsock = f.find(r"re:^(BLUE|RED) CRAG (Low|Mid) Socket$")
    add("8 side-face socket tubes on the FIELD (4 per CRAG)", len(allsock) == 8, "%d" % len(allsock))

    towers = {s: f.find("%s CRAG tower" % s) for s in ("BLUE", "RED")}
    rings = {s: f.find(r"re:^%s CRAG tier ring" % s) for s in ("BLUE", "RED")}
    depot_lip = {s: f.find("%s CRAG BASE DEPOT lip" % s) for s in ("BLUE", "RED")}
    cell_ref = virtual_cell()
    bbc = _loose_box(cell_ref)
    add("virtual O2 CELL (built from §9.2) is 5.0 x 14.0",
        abs(bbc[5] - bbc[2] - CELL_L) < 1e-3 and abs(bbc[3] - bbc[0] - CELL_D) < 0.02, _fmt(bbc))

    gen_cell = None
    try:
        gen_cell = f.find("O2 CELL - CENTER CACHE (300, 138)")
    except KeyError:
        pass

    tube_vol_doc = math.pi * (RO * RO * LEN - RI * RI * (LEN - WALL))
    per_socket = {}

    for S in sockets:
        L = S.label
        # pick the body whose bbox centre is nearest the expected tube centre
        want_c = S.rim - S.a * (LEN / 2)
        tubes = recs[(S.side, S.kind, "tube")]
        tube = min(tubes, key=lambda r: np.linalg.norm(np.array(f.bbox([r])).reshape(2, 3).mean(0) - want_c))
        solid = tube["solids"][0]
        F = f.frame(S.rim, S.e1, S.a)          # rim frame: z = axis, y = outboard-down, x lateral

        # ---- appearance / material -------------------------------------------------------
        rgb, alpha = f.color([tube])
        add(L + ": colour `socket` #9DB8D6, opaque", tuple(rgb) == RGB_SOCKET and alpha == 1, "rgb %s alpha %s" % (rgb, alpha))
        m = f.material([tube])
        add(L + ": material aluminium (MATERIALS §2 rolled aluminium tube)",
            "alum" in m["name"].lower() and AL_DENSITY[0] <= m["density"] <= AL_DENSITY[1], str(m))

        # ---- direct measurement of the revolved tube ------------------------------------
        cyl, planes, other = _analyse_tube(solid)
        add(L + ": tube surfaces are 2 cylinders + 3 planes (bore, outside, rim, floor, bottom)",
            len(cyl) == 2 and len(planes) == 3 and not other,
            "%d cylinders, %d planes, other %s" % (len(cyl), len(planes), other))
        if len(cyl) < 2 or len(planes) < 3:
            continue
        cyl.sort(key=lambda c: c[0])
        ri, ro = cyl[0][0], cyl[-1][0]
        ax = cyl[-1][2] / np.linalg.norm(cyl[-1][2])
        if ax[2] < 0:
            ax = -ax
        add(L + ": bore and outside coaxial", _line_dist(cyl[0][1], ax, cyl[-1][1], ax) < 1e-6
            and abs(abs(cyl[0][2] @ ax) - 1) < 1e-9, "axis offset %.2e" % _line_dist(cyl[0][1], ax, cyl[-1][1], ax))
        # planar faces ordered along the axis: bottom (outer), floor (inner), rim annulus
        planes.sort(key=lambda p: p[1] @ ax)
        bottom, floor_, rimf = planes
        rim_c, bot_c, flo_c = rimf[1], bottom[1], floor_[1]
        near(L + ": bore ID within 6.50 +/- 0.125 (DESIGN-SPEC §1.5)", 2 * ri, ID_NOM, ID_TOL)
        near(L + ": bore ID modelled at nominal 6.50", 2 * ri, ID_NOM, 1e-4)
        near(L + ": wall 0.09 (ref; MATERIALS §2)", ro - ri, WALL, 1e-3)
        near(L + ": rim annulus area = pi(3.34^2 - 3.25^2)", rimf[2], math.pi * (RO ** 2 - RI ** 2), 1e-3)
        add(L + ": rim plane is normal to the tube axis", abs(abs(rimf[0] @ ax) - 1) < 1e-9,
            "|n.a| = %.12f" % abs(rimf[0] @ ax))
        near(L + ": rim centre X (lateral station)", rim_c[0], S.rim[0], TOL)
        near(L + ": rim centre Y (8.0 standoff)", rim_c[1], S.rim[1], TOL)
        near(L + ": rim centre height Z", rim_c[2], S.zr, TOL)
        tilt = math.degrees(math.acos(min(1.0, ax[2])))
        near(L + ": axis tilt from vertical (deg)", tilt, TILT, 0.01)
        add(L + ": tilts OUTWARD, in the vertical plane containing the face normal",
            ax @ S.n > 0.49 and abs(ax[0]) < 1e-9, "axis %s, face normal %s" % (_fmt(ax), _fmt(S.n)))
        near(L + ": tube length along axis (rim plane to closed bottom)", (rim_c - bot_c) @ ax, LEN, TOL)
        floor_depth = (rim_c - flo_c) @ ax
        add(L + ": closed bottom (floor face present, floor thickness > 0)",
            abs(floor_[2] - math.pi * ri * ri) < 1e-3 and LEN - floor_depth > 0.05,
            "floor at %.4f below the rim, bottom plate %.4f thick" % (floor_depth, LEN - floor_depth))
        add(L + ": closed bottom — point on the axis inside the bottom plate is solid",
            f.inside([tube], (0, 0, -(LEN - WALL / 2)), F), "rim-frame point (0, 0, %.3f)" % (-(LEN - WALL / 2)))

        # ---- tight box in the expected rim frame (position + orientation in one test) -----
        bb = f.bbox([tube], F)
        want = [-RO, -RO, -LEN, RO, RO, 0.0]
        add(L + ": tight box in the document rim frame = [-3.34, -3.34, -7.0, 3.34, 3.34, 0]",
            max(abs(a - b) for a, b in zip(bb, want)) <= TOL, "got %s" % _fmt(bb))

        # ---- bore clear over its full depth ----------------------------------------------
        dmin = min(f.dist_point([tube], (0, 0, -t), F) for t in (0.25, 1.0, 2.0, 3.0, 3.5))
        near(L + ": clear bore radius on the axis, rim to 3.5 in deep", dmin, RI, 1e-3)
        lo_cyl = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, -floor_depth + 0.01), gp_Dir(0, 0, 1)),
                                          (ID_NOM - ID_TOL) / 2, floor_depth + 1.0).Shape()
        lo_cyl = _xform(lo_cyl, F.trsf())
        hits = _hits_any(f, lo_cyl)
        add(L + ": a 6.375-dia plug (bore lower limit) floor-to-rim+1 touches no body", not hits, str(hits))

        # ---- derived clearances (§2.3 clearance check, VISION-GUIDE §1.3) -----------------
        face_meas = (max if S.ny > 0 else min)(f.bbox(towers[S.side])[1], f.bbox(towers[S.side])[4])
        near(L + ": face plane (tower box) at doc Y", face_meas, S.face_y, 1e-3)
        near(L + ": rim-centre standoff normal to the face = 8.0", (rim_c[1] - face_meas) * S.ny, STANDOFF, TOL)
        near(L + ": closed-bottom centre outboard of the face = 4.50", (bot_c[1] - face_meas) * S.ny, BOTTOM_OUT, TOL)
        wb = f.bbox([tube])
        inb = (wb[1] - face_meas) if S.ny > 0 else (face_meas - wb[4])
        outb = (wb[4] - face_meas) if S.ny > 0 else (face_meas - wb[1])
        near(L + ": inboard edge outboard of the face = 1.61", inb, INBOARD_EDGE, TOL)
        near(L + ": outboard extent = 10.89 (VISION-GUIDE §1.3)", outb, OUTBOARD_EDGE, TOL)
        near(L + ": lowest point Z (%s)" % ("22.27 per §2.3/§7" if S.kind == "Low" else "rim - 7.73"),
             wb[2], S.zr - LOWEST_BELOW_RIM, TOL)
        near(L + ": uphill lip = rim + 1.67", wb[5], S.zr + UPHILL_LIP, TOL)
        near(L + ": lateral silhouette +/-3.34 about the station", (wb[0] + wb[3]) / 2, S.lat_x, TOL,
             ", width %.4f" % (wb[3] - wb[0]))
        tv = sum(_common(solid, s) for s in towers[S.side][0]["solids"])
        dt = f.dist([tube], towers[S.side])
        add(L + ": nothing penetrates the tower shell (no common volume, gap = 1.61)",
            tv < 1e-9 and abs(dt - INBOARD_EDGE) < TOL, "common %.2e in^3, gap %.4f" % (tv, dt))
        near(L + ": tube volume = pi(3.34^2*7.0 - 3.25^2*6.91)", f.volume([tube]), tube_vol_doc, 1e-3)

        # ---- the tag under the socket ------------------------------------------------------
        tag = f.find(r"re:^AprilTag %d - " % S.tag)
        tb = f.bbox(tag)
        near(L + ": sits directly above tag %d (rim lateral = tag centre)" % S.tag, rim_c[0], (tb[0] + tb[3]) / 2, TOL)
        near(L + ": tag %d centre Z" % S.tag, (tb[2] + tb[5]) / 2, TAG_Z, 1e-3)
        jt = _json_tag(S.tag)
        if jt is None:
            add(L + ": tag %d present in apriltag-field-layout.json" % S.tag, False, "missing")
        else:
            pos, nrm = jt
            pred = pos + STANDOFF * nrm + np.array([0, 0, S.zr - TAG_Z])
            add(L + ": rim = JSON tag %d pose + 8.0 out + %.1f up (VISION-GUIDE §6.6 tagToTarget)"
                % (S.tag, S.zr - TAG_Z), float(np.linalg.norm(pred - rim_c)) <= TOL and nrm @ S.n > 0.999,
                "predicted %s, measured %s, tag normal %s" % (_fmt(pred), _fmt(rim_c), _fmt(nrm)))
        add(L + ": tube clear of tag %d panel (lowest point above panel top 22.0 and target top 21.56)" % S.tag,
            wb[2] > tb[5] and f.dist([tube], tag) > 0.2,
            "tube low %.4f, panel top %.4f, target top %.4f, gap %.4f" % (wb[2], tb[5], TAG_Z + TARGET / 2, f.dist([tube], tag)))

        # ---- O2 CELL seated (virtual, from §9.2) --------------------------------------------
        fd =f.dist_point([tube], (0, 0, -5.0), F) + 5.0
        near(L + ": floor depth by point probe agrees with face analysis", fd, floor_depth, 1e-4)
        cell_c = _xform(_translate(cell_ref, (0, 0, -fd)), F.trsf())
        cv = _common(cell_c, solid)
        add(L + ": seated CELL (coaxial) fits the bore", cv < 1e-6, "common volume %.2e in^3" % cv)
        protr = CELL_L - fd
        near(L + ": seated CELL protrudes 7.0 along the axis (§2.3; +0.1 allows the modelled floor)",
             protr, DOC_PROTRUSION, 0.1, " — floor %.3f below the rim" % fd)
        near(L + ": seated CELL pole above the rim centre = 6.06", protr * C30, DOC_APEX_ABOVE_RIM, 0.1)
        near(L + ": seated CELL clears the uphill lip by 4.39", S.zr + protr * C30 - wb[5], DOC_MOUTH_CLEAR, 0.1)
        hits = _hits_any(f, cell_c, exclude=[tube])
        add(L + ": seated CELL (coaxial) meets no other field body", not hits, str(hits))
        # physical rest: gravity presses the CELL onto the downhill (outboard) side of the bore
        off = RI - CELL_D / 2 - 0.001
        cell_r = _xform(_translate(cell_ref, (0, off, -fd)), F.trsf())
        cvr = _common(cell_r, solid)
        pole_r = S.zr + protr * C30 - off * S30
        add(L + ": CELL resting on the downhill wall fits and its pole stays above the uphill lip",
            cvr < 1e-6 and pole_r > wb[5],
            "common %.2e in^3; pole Z %.3f vs uphill lip %.3f -> %.3f clear (doc 4.39 assumes a centred CELL)"
            % (cvr, pole_r, wb[5], pole_r - wb[5]))
        hits = _hits_any(f, cell_r, exclude=[tube])
        add(L + ": resting CELL meets no other field body", not hits, str(hits))
        if gen_cell is not None:
            gs = K._compound(f.solids(gen_cell))
            gb = f.bbox(gen_cell)
            c = np.array(gb).reshape(2, 3).mean(0)
            ext = np.array(gb[3:]) - np.array(gb[:3])
            if ext[0] > ext[1] and ext[0] > ext[2]:
                t1 = gp_Trsf()
                t1.SetTranslation(gp_Vec(-c[0], -c[1], -c[2]))
                t2 = gp_Trsf()
                t2.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), -math.pi / 2)   # +X -> +Z
                t3 = gp_Trsf()
                t3.SetTranslation(gp_Vec(0, 0, -fd + ext[0] / 2))
                g = _xform(_xform(_xform(_xform(gs, t1), t2), t3), F.trsf())
                gv = _common(g, solid)
                add(L + ": the model's own O2 CELL SUPPLY seats in the bore without interference",
                    gv < 1e-6, "common %.2e in^3 (cell length %.3f)" % (gv, ext[0]))

        # ---- the depot corner arm below (§2.3 robot standoff, §3 open-to-sky) --------------
        cx = CRAG_C[S.side][0]
        shelf_plane = cx + SHELF_X[S.side] * HALF
        arm_x = sorted([shelf_plane, shelf_plane - SHELF_X[S.side] * ARM])
        arm_y = sorted([S.face_y, S.face_y + S.ny * ARM])
        in_arm = arm_x[0] <= wb[0] and wb[3] <= arm_x[1] and arm_y[0] <= wb[1] and wb[4] <= arm_y[1]
        if S.kind == "Low":
            add(L + ": plan silhouette lies over the DEPOT corner arm (§2.3 'directly above it')", in_arm,
                "tube X %.3f-%.3f Y %.3f-%.3f, arm X %s Y %s" % (wb[0], wb[3], wb[1], wb[4], arm_x, arm_y))
            cols = sorted([wb[0] - arm_x[0], arm_x[1] - wb[3], wb[1] - arm_y[0], arm_y[1] - wb[4]])
            add(L + ": clear sky columns in the arm = 1.61 / 2.66 / 5.11 / 6.66 (§3)",
                max(abs(a - b) for a, b in zip(cols, ARM_CLEAR_COLUMNS)) < 0.01, "measured %s" % _fmt(cols))
            lb = f.bbox(depot_lip[S.side])
            lip_out = (lb[4] - S.face_y) if S.ny > 0 else (S.face_y - lb[1])
            near(L + ": DEPOT lip outer face along the SOCKET FACE = 16.75", lip_out, ARM + LIP_T, 1e-3)
            reach = lip_out + FRAME_BEHIND_BUMPER - (rim_c[1] - face_meas) * S.ny
            add(L + ": reach from the FRAME PERIMETER at the lip = 11.75, inside 18",
                abs(reach - LOW_REACH) < 0.01 and reach <= REACH_LIMIT, "%.4f" % reach)
            add(L + ": lowest point clears a crowned CRATE in the arm (Z 13.25)", wb[2] > CRATE_TOP_IN_TRAY,
                "%.3f above" % (wb[2] - CRATE_TOP_IN_TRAY))
        else:
            lb = f.bbox(depot_lip[S.side])
            add(L + ": clear of the DEPOT arm in plan (§2.3 'clear of the arm')",
                wb[0] > lb[3] or wb[3] < lb[0], "tube X %.3f-%.3f, depot lip X %.3f-%.3f" % (wb[0], wb[3], lb[0], lb[3]))
            # bumpers can come to the face at the Mid station: nothing within 3.0 in of the face below Z 12
            y0, y1 = sorted([S.face_y + S.ny * 0.01, S.face_y + S.ny * FRAME_BEHIND_BUMPER])
            box = BRepPrimAPI_MakeBox(gp_Pnt(S.lat_x - 6, y0, 0.01), gp_Pnt(S.lat_x + 6, y1, 12.0)).Shape()
            hits = _hits_any(f, box)
            add(L + ": BUMPER zone at the face in front of the Mid station is clear (reach 5.0 in)",
                not hits and abs((STANDOFF - FRAME_BEHIND_BUMPER) - MID_REACH) < 1e-9, str(hits))

        per_socket[L] = dict(S=S, tube=tube, F=F, wb=wb, rim=rim_c, fd=fd, tag=tag, tb=tb)

    # ---- brackets --------------------------------------------------------------------------
    for L, d in per_socket.items():
        S, tube, F, wb = d["S"], d["tube"], d["F"], d["wb"]
        brks = recs[(S.side, S.kind, "brk")]
        brk = min(brks, key=lambda r: np.linalg.norm(np.array(f.bbox([r])).reshape(2, 3).mean(0) - (S.rim - S.a * LEN)))
        bl = L + " bracket"
        bw = f.bbox([brk])
        add(bl + ": one bracket at this socket's lateral station",
            sum(1 for r in brks if abs(np.mean([f.bbox([r])[0], f.bbox([r])[3]]) - S.lat_x) < RO
                and abs(np.mean([f.bbox([r])[1], f.bbox([r])[4]]) - S.face_y) < 8) == 1,
            "bbox %s" % _fmt(bw))
        rgb, alpha = f.color([brk])
        add(bl + ": colour `crag-accent` #4A3B22 (MATERIALS §2 socket bracket)",
            tuple(rgb) == RGB_ACCENT and alpha == 1, "rgb %s alpha %s" % (rgb, alpha))
        m = f.material([brk])
        add(bl + ": material aluminium plate", "alum" in m["name"].lower()
            and AL_DENSITY[0] <= m["density"] <= AL_DENSITY[1], str(m))
        near(bl + ": plate thickness 0.125 (MATERIALS §2)", bw[3] - bw[0], BRACKET_T, 1e-3)
        add(bl + ": plate within the tube's lateral silhouette",
            bw[0] >= wb[0] - EPS and bw[3] <= wb[3] + EPS, "plate X %.4f-%.4f, tube X %.4f-%.4f" % (bw[0], bw[3], wb[0], wb[3]))
        # the plate lies in the vertical plane containing the face normal
        big = max(_analyse_tube(brk["solids"][0])[1], key=lambda p: p[2])
        add(bl + ": plate plane is vertical and contains the face normal", abs(abs(big[0][0]) - 1) < 1e-9,
            "largest face normal %s (area %.3f)" % (_fmt(big[0]), big[2]))
        # attaches: touches both the tube and the face
        dtube, dface = f.dist([brk], [tube]), f.dist([brk], towers[S.side])
        add(bl + ": actually joins tube to face (touches both)", dtube < 1e-6 and dface < 1e-6,
            "gap to tube %.2e, to tower %.2e" % (dtube, dface))
        cvt = sum(_common(brk["solids"][0], s) for s in towers[S.side][0]["solids"])
        cvb = _common(brk["solids"][0], tube["solids"][0])
        add(bl + ": no interference with the tower; tube overlap within contact tolerance (1e-4 in^3)",
            cvt < 1e-9 and cvb <= 1e-4, "tower %.2e in^3, tube %.2e in^3" % (cvt, cvb))
        others = _hits_any(f, brk["solids"][0], exclude=[brk, tube])
        add(bl + ": meets no other field body", not others, str(others))
        # attachment rule (§2.3): never breaks the rim plane, never outboard of the tube silhouette
        bf = f.bbox([brk], F)
        add(bl + ": does not break the rim plane (all points below it along the axis)", bf[5] <= EPS,
            "max axial %.4f (rim plane at 0)" % bf[5])
        add(bl + ": does not project outboard of the tube silhouette (rim frame, outboard <= +3.34)",
            bf[4] <= RO + EPS and abs(bf[0]) <= RO + EPS and abs(bf[3]) <= RO + EPS, "rim-frame box %s" % _fmt(bf))
        bout = (bw[4] - S.face_y) if S.ny > 0 else (S.face_y - bw[1])
        tout = (wb[4] - S.face_y) if S.ny > 0 else (S.face_y - wb[1])
        add(bl + ": horizontal reach off the face within the tube's", bout <= tout + EPS,
            "bracket %.4f, tube %.4f outboard" % (bout, tout))
        add(bl + ": lives in the wedge under the tube (inboard of the tube wall, above its bottom plane)",
            bf[4] <= -RO + 1e-3 and bf[2] >= -LEN - 1e-3, "rim-frame box %s" % _fmt(bf))
        add(bl + ": attaches below the rim", bw[5] < S.zr, "top Z %.4f vs rim %.1f" % (bw[5], S.zr))
        # tag below
        tb = d["tb"]
        add(bl + ": clear of the tag panel band (lowest point above panel top Z %.2f)" % tb[5],
            bw[2] > tb[5] and f.dist([brk], d["tag"]) > 1.0, "bracket low Z %.4f, gap to panel %.4f" % (bw[2], f.dist([brk], d["tag"])))
        # tier rings: no overlap with any band on the face, no contact with the ring bodies
        overl = [b for b in RING_BANDS if not (bw[5] < b[0] or bw[2] > b[1])]
        dr = f.dist([brk], rings[S.side])
        add(bl + ": does not cross a tier ring (Z %.2f-%.2f vs bands %s)" % (bw[2], bw[5], RING_BANDS[:2]),
            not overl and dr > 0.1, "overlapping bands %s, gap to ring bodies %.4f" % (overl, dr))
        # angle rule on every straight edge
        bad = []
        for e in _edges(brk["solids"][0]):
            c = BRepAdaptor_Curve(e)
            if c.GetType() == GeomAbs_Line:
                dv = _v(c.Line().Direction())
                ang = math.degrees(math.acos(min(1.0, abs(dv[2]))))
                if abs(ang / 15.0 - round(ang / 15.0)) > 1e-6:
                    bad.append(round(ang, 4))
        add(bl + ": every edge at a multiple of 15 deg from vertical (§0 angle rule)", not bad, "off-grid %s" % bad)

    # ---- tag occlusion by tubes / brackets (§7 occlusion budget) -------------------------
    out += _occlusion(f, per_socket, recs)

    # ---- Red = Blue rotated 180 deg about (324, 162) ---------------------------------------
    for L, d in per_socket.items():
        S = d["S"]
        if S.side != "BLUE":
            continue
        rl = "RED %sY %s Socket" % ("+" if -S.ny > 0 else "-", S.kind)
        if rl not in per_socket:
            continue
        b, r = d["wb"], per_socket[rl]["wb"]
        rot = [648 - b[3], 324 - b[4], b[2], 648 - b[0], 324 - b[1], b[5]]
        add("%s maps to %s under the 180-deg rotation about (324, 162)" % (L, rl),
            max(abs(x - y) for x, y in zip(rot, r)) < 1e-6, "rotated %s vs %s" % (_fmt(rot), _fmt(r)))
    bvols = [f.volume([r]) for s in ("BLUE", "RED") for k in ("Low", "Mid") for r in recs[(s, k, "brk")]]
    add("all 8 brackets identical in volume", len(bvols) == 8 and max(bvols) - min(bvols) < 1e-6, _fmt(bvols))
    tvols = [f.volume([r]) for r in allsock]
    add("all 8 side-face tubes identical in volume", len(tvols) == 8 and max(tvols) - min(tvols) < 1e-6, _fmt(tvols))
    return out


# ---------------------------------------------------------------------------------------
# sight lines from camera stations to the socket-face tag targets
# ---------------------------------------------------------------------------------------
def _occlusion(f, per_socket, recs):
    out = []
    # occluders per face: both tubes and both brackets of that face
    faces = {}
    for L, d in per_socket.items():
        S = d["S"]
        key = (S.side, S.ny)
        faces.setdefault(key, {"tube": [], "brk": [], "tags": []})
        faces[key]["tube"].append((S.kind, d["tube"]["solids"][0]))
        brks = recs[(S.side, S.kind, "brk")]
        brk = min(brks, key=lambda r: abs(np.mean([f.bbox([r])[1], f.bbox([r])[4]]) - S.face_y)
                  + abs(np.mean([f.bbox([r])[0], f.bbox([r])[3]]) - S.lat_x))
        faces[key]["brk"].append((S.kind, brk["solids"][0]))
        faces[key]["tags"].append((S, d["tb"]))

    def loader(s):
        it = IntCurvesFace_ShapeIntersector()
        it.Load(s, 1e-7)
        return it

    zs = [TAG_Z + v for v in (-TARGET / 2, -BODY / 2, -2.0, 0.0, 2.0, BODY / 2, TARGET / 2)]
    us = [-TARGET / 2, -BODY / 2, 0.0, BODY / 2, TARGET / 2]
    lats = [-36.0, -12.0, 0.0, 12.0, 36.0]
    primary = [10.0, 12.0, 14.0, 16.0, 18.0, 20.0]         # VISION-GUIDE §5.2 primary camera band
    second = [24.0, 27.0, 30.0, 33.0, 36.0]                # VISION-GUIDE §5.2 optional second camera

    DS = [3.0, 6.0, 12.0, 17.0, 24.0, 36.0, 48.0, 72.0, 96.0]
    res = {"prim_tube": [], "prim_brk": [], "sec_tube": [], "any_brk": []}
    worst = {}
    n_cam = {}
    for key, fd in faces.items():
        tubes = [(k, loader(s)) for k, s in fd["tube"]]
        brks = [(k, loader(s)) for k, s in fd["brk"]]
        shelf_plane = CRAG_C[key[0]][0] + SHELF_X[key[0]] * HALF
        for S, tb in fd["tags"]:
            # the tag panel's field-side face
            yface = tb[4] if S.ny > 0 else tb[1]
            xc = (tb[0] + tb[3]) / 2
            for hc in primary + second:
                for D in DS:
                    for lo in lats:
                        # robot keep-out (§2.3 robot standoff): where the DEPOT corner arm or corner
                        # square lies in front of the face, BUMPERS stop at the lip (16.75 in);
                        # elsewhere the FRAME PERIMETER is >= 3.0 in off the face
                        inside = (xc + lo - shelf_plane) * (-SHELF_X[key[0]])
                        if -(ARM + LIP_T) <= inside <= ARM + LIP_T and D < ARM + LIP_T:
                            continue
                        n_cam[(S.tag, hc)] = n_cam.get((S.tag, hc), 0) + 1
                        cam = np.array([xc + lo, S.face_y + S.ny * D, hc])
                        for u in us:
                            for z in zs:
                                p = np.array([xc + u, yface + S.ny * 0.002, z])
                                dv = cam - p
                                ln = float(np.linalg.norm(dv))
                                lin = gp_Lin(gp_Pnt(*p), gp_Dir(*(dv / ln)))
                                for k, it in tubes:
                                    it.Perform(lin, 0.0, ln)
                                    if it.NbPnt() > 0:
                                        rec = (S.tag, k, hc, D, lo, u, z)
                                        (res["prim_tube"] if hc in primary else res["sec_tube"]).append(rec)
                                        if hc in second and lo == 0.0:
                                            w = worst.setdefault((S.tag, hc, D), [99.0, 0])
                                            w[0] = min(w[0], z)
                                            w[1] += 1
                                for k, it in brks:
                                    it.Perform(lin, 0.0, ln)
                                    if it.NbPnt() > 0:
                                        res["any_brk"].append((S.tag, k, hc, D, lo, u, z))
    npts = len(us) * len(zs)
    n_prim = sum(v for (t, h), v in n_cam.items() if h in primary) * npts
    n_sec = sum(v for (t, h), v in n_cam.items() if h in second) * npts
    out.append(("§7: primary camera band 10-20 in (VISION-GUIDE §5.2) — no socket tube or bracket blocks any "
                "sight line to tags 8-11 / 21-24", not res["prim_tube"] and not res["prim_brk"],
                "%d of %d sight lines blocked, e.g. %s" % (len(res["prim_tube"]), n_prim, res["prim_tube"][:3])))
    out.append(("§2.3/§7: brackets block no sight line to any socket-face tag, cameras 10-36 in",
                not res["any_brk"], "%d of %d blocked, e.g. %s" % (len(res["any_brk"]), n_prim + n_sec, res["any_brk"][:3])))
    ex = sorted(worst.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2]))
    summ = "; ".join("tag %d, camera %.0f in high %.0f in off the face, square-on: %d/%d target points hidden, "
                     "down to Z %.2f" % (k[0], k[1], k[2], v[1], npts, v[0])
                     for k, v in ex if k[0] in (8, 21) and k[1] in (24.0, 30.0, 36.0) and k[2] in (17.0, 24.0, 48.0))
    tags_hit = sorted({r[0] for r in res["sec_tube"]})
    kinds_hit = sorted({r[1] for r in res["sec_tube"]})
    out.append(("§7 claim 'no field structure ... can occlude a CRAG tag' / VISION-GUIDE §1.3 'clear at every "
                "outboard station' — for the VISION-GUIDE §5.2 second camera (24-36 in) the Low Socket tube "
                "blocks no sight line to the tag below it",
                not res["sec_tube"],
                "%d of %d sight lines blocked (tags %s, by %s tube). %s"
                % (len(res["sec_tube"]), n_sec, tags_hit, kinds_hit, summ)))
    return out
