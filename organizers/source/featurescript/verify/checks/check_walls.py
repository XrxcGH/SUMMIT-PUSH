# -*- coding: utf-8 -*-
"""
Independent check: alliance walls, driver stations, E-STOP / A-STOP (both alliances).

Expected values come from the package documents only (never from src/20_ledger.fs):

  FIELD-CAD-PACKAGE §0   always-blue-origin NWU; Red = Blue rotated 180 deg about (324, 162);
                         field 648 x 324; (ref) may float +/-0.25 in.
  FIELD-CAD-PACKAGE §1.3 "Alliance walls: full width, 78 in tall and 2.0 in thick throughout (ref);
                         solid to Z = 39, glazed 39 -> 78.  Each wall has three driver stations, 96 in
                         wide on 108-in centers (Y = 54 / 162 / 270), each with a 0.75-in shelf topping
                         out at 36 in, a window in the glazed band, and an E-STOP and an A-STOP button
                         (ref).  The OUTFITTER chutes penetrate the wall at the coordinates above."
  FIELD-CAD-PACKAGE §1.1/§5  chutes Blue (0, 30), (0, 294); Red (648, 294), (648, 30); opening
                         30 W x 16 H, sill 24 (Z 24-40); "Alliance wall thickness at the chute 2.0 in
                         (ref)"; sill edge radius 0.5 (ref); ramp 30 deg (ref).
  FIELD-CAD-PACKAGE §9.1 CACHE CRATE 12.0 cube, 0.5 crown, 13.0 envelope, rests on its bottom crown.
  MATERIALS-AND-COLORS §1.2/§2
                         Alliance wall, lower  : painted plywood on steel frame, `wall` #9AA4B2, matte, 0.75
                         Alliance wall, glazing: polycarbonate, `glazing` #DCE8FA at 25 %, 0.25
                         Driver station shelf  : painted plywood, `wall`, 0.75
                         E-STOP / A-STOP       : molded plastic, red #CC2020 / blue #1D63C8, gloss,
                                                 dia 2 in mushroom head
                         `wall` also: "Alliance walls, guardrail frame"
  Manual §3.1            each driver station provides a shelf, a clear polycarbonate window, E-STOP and
                         A-STOP; R707 the OPERATOR CONSOLE "must fit within the driver-station shelf".

Construction readings (the generator's documented design; the package leaves them free):
  * the steel frame is ONE welded body "<A> alliance wall frame"; its lower members stay behind the
    0.75 lower panel (x -2..-0.75), its top rail and upper posts come forward to the glazing's back
    face (x = -0.25) so the 0.25 glazing is backed; nothing of it enters the panel / glazing layer;
  * at each chute a throat liner "<A> OUTFITTER n chute throat" fills the 2.0-in wall depth around
    the 30 x 16 opening, so the wall is 2.0 thick at the chute (§5) through the whole opening;
  * driver-station shelves run from the lower panel's back face (x = -0.75) 12 in back (ref: the
    package gives no shelf depth), at Z 35.25-36, and the corner stations' shelves are cut back
    at the OUTFITTER funnel, whose plan outline §5 fixes at c +/- (36/2 + 0.5 cheek plate).

Local alliance frame used throughout (built here from §0, not taken from the generator):
  Blue: origin (0, 0, 0),    x = +X (into the field), z = +Z
  Red : origin (648, 324, 0), x = -X,                  z = +Z      (the 180-deg rotation)
so in both frames the field face of the wall is the plane x = 0, the wall lies at x < 0, and the
driver stations / chutes are at local y = 54/162/270 and 30/294.
"""
import math

import numpy as np

import kernel_occ as K

# ---- document values -------------------------------------------------------------------
FIELD_L, FIELD_W = 648.0, 324.0
CX, CY = 324.0, 162.0
WALL_H = 78.0
WALL_T = 2.0            # (ref) 2.0 throughout, 2.0 at the chute
SOLID_TOP = 39.0
PANEL_T = 0.75          # MATERIALS §2 alliance wall, lower
GLAZE_T = 0.25          # MATERIALS §2 alliance wall, upper glazing
STATION_Y = (54.0, 162.0, 270.0)
STATION_PITCH = 108.0
STATION_W = 96.0
SHELF_TOP = 36.0
SHELF_T = 0.75
SHELF_D = 12.0          # (ref) the package gives no shelf depth; generator reading
BUTTON_D = 2.0
CHUTE_Y = (30.0, 294.0)
CHUTE_W = 30.0
CHUTE_SILL = 24.0
CHUTE_H = 16.0
SILL_R = 0.5            # (ref)
RAMP_ANG = 30.0         # (ref)
FLARE_W = 36.0          # §5 cheek funnels flare to 36 at the loading end (ref)
CHEEK_T = 0.5           # MATERIALS §2 OUTFITTER cheek funnel 0.5
CRATE = 12.0
CROWN = 0.5
REF = 0.25              # (ref) float

HEX = lambda h: (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))  # noqa: E731
RGB_WALL = HEX("#9AA4B2")
RGB_GLAZING = HEX("#DCE8FA")
ALPHA_GLAZING = 0.25
RGB_ESTOP = HEX("#CC2020")
RGB_ASTOP = HEX("#1D63C8")

EPS = 1e-3


def _frames(f):
    return {"BLUE": f.frame((0, 0, 0), (1, 0, 0), (0, 0, 1)),
            "RED": f.frame((FIELD_L, FIELD_W, 0), (-1, 0, 0), (0, 0, 1))}


def _box_str(b):
    return "[" + ", ".join("%.3f" % v for v in b) + "]"


def _near(a, b, tol=EPS):
    return abs(a - b) <= tol


def _rec(solids):
    return [{"solids": list(solids)}]


def _trsf_from(M, t):
    tr = K.gp_Trsf()
    tr.SetValues(M[0][0], M[0][1], M[0][2], t[0],
                 M[1][0], M[1][1], M[1][2], t[1],
                 M[2][0], M[2][1], M[2][2], t[2])
    return tr


def _xform(solids, tr):
    out = []
    for s in solids:
        out += K._solids(K.BRepBuilderAPI_Transform(s, tr, True).Shape())
    return out


def _rot180():
    tr = K.gp_Trsf()
    tr.SetRotation(K.gp_Ax1(K.gp_Pnt(CX, CY, 0.0), K.gp_Dir(0.0, 0.0, 1.0)), math.pi)
    return tr


def _box_solid(F, p0, p1):
    """Axis-aligned box in local frame F between local corners p0, p1 (a virtual body)."""
    lo = [min(a, b) for a, b in zip(p0, p1)]
    hi = [max(a, b) for a, b in zip(p0, p1)]
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
    b = BRepPrimAPI_MakeBox(K.gp_Pnt(*lo), K.gp_Pnt(*hi)).Shape()
    return _xform(K._solids(b), F.trsf())


def _fast_box(r, pad=0.01):
    """Loose world bounding box of one record (prefilter only)."""
    b = K.Bnd_Box()
    for s in r["solids"]:
        K.BRepBndLib.Add_s(s, b, False)
    x = K._box6(b)
    return [x[0] - pad, x[1] - pad, x[2] - pad, x[3] + pad, x[4] + pad, x[5] + pad]


def _find(f, name):
    try:
        return f.find(name)
    except KeyError:
        return []


def run(f):
    out = []

    def chk(label, ok, detail):
        out.append((label, bool(ok), detail))

    FR = _frames(f)
    rec = {}
    for A in ("BLUE", "RED"):
        r = {"panel": _find(f, A + " alliance wall lower panel"),
             "glaze": _find(f, A + " alliance wall glazing"),
             "frame": _find(f, A + " alliance wall frame")}
        for i in (1, 2, 3):
            r["shelf%d" % i] = _find(f, "%s driver station %d shelf" % (A, i))
            r["estop%d" % i] = _find(f, "%s driver station %d E-STOP" % (A, i))
            r["astop%d" % i] = _find(f, "%s driver station %d A-STOP" % (A, i))
            r["estopb%d" % i] = _find(f, "%s driver station %d E-STOP base" % (A, i))
            r["astopb%d" % i] = _find(f, "%s driver station %d A-STOP base" % (A, i))
        rec[A] = r
    # OUTFITTER chute bodies behind each wall (throat liner, ramp, cheeks, funnel wings, leg);
    # kept apart from rec so the interference sweep below still tests the wall against them
    chute = {}
    for A in ("BLUE", "RED"):
        for o in (1, 2):
            chute[(A, o)] = {k: _find(f, "%s OUTFITTER %d %s" % (A, o, k))
                             for k in ("chute throat", "chute ramp", "cheek", "funnel wing", "ramp leg")}

    # ---- 0. presence and counts ---------------------------------------------------------
    for A in ("BLUE", "RED"):
        r = rec[A]
        chk("%s wall: one lower panel, one glazing body, one welded frame body" % A,
            len(r["panel"]) == 1 and len(r["glaze"]) == 1 and len(r["frame"]) == 1,
            "panel %d, glazing %d, frame %d bodies" % (len(r["panel"]), len(r["glaze"]), len(r["frame"])))
        try:
            shelves = f.find(r"re:^%s driver station \d+ shelf$" % A)
        except KeyError:
            shelves = []
        chk("%s wall: exactly 3 driver-station shelves (§1.3)" % A, len(shelves) == 3, "found %d" % len(shelves))
        try:
            es = f.find(r"re:^%s driver station \d+ E-STOP$" % A)
        except KeyError:
            es = []
        try:
            as_ = f.find(r"re:^%s driver station \d+ A-STOP$" % A)
        except KeyError:
            as_ = []
        chk("%s wall: one E-STOP and one A-STOP per station (3 + 3)" % A,
            len(es) == 3 and len(as_) == 3 and all(len(r["estop%d" % i]) == 1 and len(r["astop%d" % i]) == 1 for i in (1, 2, 3)),
            "E-STOP heads %d, A-STOP heads %d" % (len(es), len(as_)))
    if not all(rec[A]["panel"] and rec[A]["glaze"] and rec[A]["frame"] for A in rec):
        return out
    for A in ("BLUE", "RED"):
        np_, ng_ = len(f.solids(rec[A]["panel"])), len(f.solids(rec[A]["glaze"]))
        chk("%s lower panel and glazing each stay one connected solid after the chute/tag cuts" % A,
            np_ == 1 and ng_ == 1, "panel %d solid(s), glazing %d solid(s)" % (np_, ng_))
        nf_ = len(f.solids(rec[A]["frame"]))
        chk("%s steel wall frame is welded into one connected solid" % A, nf_ == 1, "frame %d solid(s)" % nf_)

    # ---- 1. wall envelope, both alliances --------------------------------------------------
    for A in ("BLUE", "RED"):
        F = FR[A]
        r = rec[A]
        wall = r["panel"] + r["glaze"] + r["frame"]
        b = f.bbox(wall, F)
        want = [-WALL_T, 0.0, 0.0, 0.0, FIELD_W, WALL_H]
        chk("%s wall envelope x -2..0 (2.0 thick), y 0..324 (full width), z 0..78" % A,
            all(_near(g, w) for g, w in zip(b, want)), "local bbox %s want %s" % (_box_str(b), _box_str(want)))
        bw = f.bbox(wall)
        if A == "BLUE":
            ok = _near(bw[3], 0.0) and _near(bw[0], -WALL_T)
            want_s = "field face X = 0, back X = -2"
        else:
            ok = _near(bw[0], FIELD_L) and _near(bw[3], FIELD_L + WALL_T)
            want_s = "field face X = 648, back X = 650"
        chk("%s wall world position (%s)" % (A, want_s), ok and _near(bw[1], 0) and _near(bw[4], FIELD_W),
            "world bbox %s" % _box_str(bw))

        bp = f.bbox(r["panel"], F)
        chk("%s lower panel: solid Z 0..39, full width, 0.75 thick on the field face" % A,
            _near(bp[0], -PANEL_T) and _near(bp[3], 0) and _near(bp[1], 0) and _near(bp[4], FIELD_W)
            and _near(bp[2], 0) and _near(bp[5], SOLID_TOP),
            "local bbox %s want [-0.75, 0, 0, 0, 324, 39]" % _box_str(bp))
        bg = f.bbox(r["glaze"], F)
        chk("%s glazing: Z 39..78, full width, 0.25 thick on the field face" % A,
            _near(bg[0], -GLAZE_T) and _near(bg[3], 0) and _near(bg[1], 0) and _near(bg[4], FIELD_W)
            and _near(bg[2], SOLID_TOP) and _near(bg[5], WALL_H),
            "local bbox %s want [-0.25, 0, 39, 0, 324, 78]" % _box_str(bg))
        bf = f.bbox(r["frame"], F)
        chk("%s wall frame stays inside the 2.0-in envelope behind the panel/glazing (x -2..-0.25)" % A,
            bf[0] >= -WALL_T - EPS and bf[3] <= -GLAZE_T + EPS and bf[2] >= -EPS and bf[5] <= WALL_H + EPS
            and bf[1] >= -EPS and bf[4] <= FIELD_W + EPS,
            "local bbox %s" % _box_str(bf))
        # the lower members stay behind the 0.75 lower panel: no frame steel in front of the
        # panel's back plane (x > -0.75) anywhere in the solid band Z 0..39 (chute openings included)
        lo_band = _rec(_box_solid(F, (-PANEL_T, -1.0, -1.0), (1.0, FIELD_W + 1.0, SOLID_TOP)))
        cvl = f.common_volume(r["frame"], lo_band)
        cvpg = f.common_volume(r["frame"], r["panel"] + r["glaze"])
        chk("%s wall frame: lower members behind the 0.75 panel (x <= -0.75 below Z 39), no overlap with panel/glazing" % A,
            cvl < 1e-4 and cvpg < 1e-4,
            "frame steel in front of the panel back plane below Z 39: %.5f in^3; frame x panel/glazing %.5f in^3" % (cvl, cvpg))

        # nothing of the wall or the driver stations reaches into the field (x > 0)
        allw = list(wall)
        for i in (1, 2, 3):
            for k in ("shelf", "estop", "astop", "estopb", "astopb"):
                allw += r["%s%d" % (k, i)]
        ball = f.bbox(allw, F)
        chk("%s wall + driver stations: nothing crosses the field-side plane" % A, ball[3] <= EPS,
            "max local x %.4f (field face at 0)" % ball[3])

        # field face: sample the wall plane.  Just outside (x = +0.01) must be free; just
        # inside (x = -0.01) must be wall (panel / glazing / flush OUTFITTER tag panel)
        # except inside the two chute openings.
        try:
            tags = f.find("re:^AprilTag \\d+ - %s OUTFITTER chute$" % A)
        except KeyError:
            tags = []
        in_open = lambda y, z: any(abs(y - c) < CHUTE_W / 2 and CHUTE_SILL < z < CHUTE_SILL + CHUTE_H for c in CHUTE_Y)  # noqa: E731
        miss_in, hit_out, n = [], [], 0
        for y in np.arange(0.5, FIELD_W, 4.0):
            for z in np.arange(0.5, WALL_H, 3.0):
                n += 1
                if f.inside(allw, (0.01, y, z), F):
                    hit_out.append((y, z))
                if not in_open(y, z) and not f.inside(r["panel"] + r["glaze"] + tags, (-0.01, y, z), F):
                    miss_in.append((round(y, 1), round(z, 1)))
        chk("%s field face is one flush plane at x = 0 (%d samples, closed outside the chutes)" % (A, n),
            not hit_out and not miss_in,
            "points past the face %s; holes in the face %s" % (hit_out[:4], miss_in[:6]))

        # solid to Z 39: the lower band is the opaque panel, the upper band is glazing
        bad = []
        for y in np.arange(1.0, FIELD_W, 6.0):
            for z in np.arange(0.5, SOLID_TOP, 2.5):
                if not in_open(y, z) and not f.inside(r["panel"], (-PANEL_T / 2, y, z), F):
                    bad.append((round(y, 1), round(z, 1)))
        chk("%s wall solid (lower panel) everywhere from Z 0 to 39 outside the chute openings" % A,
            not bad, "gaps at %s" % bad[:6])
        bad = []
        for y in np.arange(1.0, FIELD_W, 6.0):
            for z in np.arange(40.5, WALL_H, 2.5):
                on_tag = bool(tags) and f.inside(tags, (-GLAZE_T / 2, y, z), F)
                if not on_tag and not f.inside(r["glaze"], (-GLAZE_T / 2, y, z), F):
                    bad.append((round(y, 1), round(z, 1)))
                if f.inside(r["panel"], (-0.1, y, z), F):
                    bad.append(("panel above 39", round(y, 1), round(z, 1)))
        chk("%s wall glazed from Z 39 to 78 across the full width (tag panels excepted)" % A,
            not bad, "non-glazed points %s" % bad[:6])

        # the OUTFITTER chutes penetrate the whole wall (panel, glazing, frame and throat liner)
        throats = chute[(A, 1)]["chute throat"] + chute[(A, 2)]["chute throat"]
        blocked = []
        for c in CHUTE_Y:
            for x in (-0.05, -0.4, -1.0, -1.6, -1.95):
                for y in (c - CHUTE_W / 2 + 0.05, c, c + CHUTE_W / 2 - 0.05):
                    for z in (CHUTE_SILL + 0.05, CHUTE_SILL + CHUTE_H / 2, CHUTE_SILL + CHUTE_H - 0.05):
                        if f.inside(wall + throats, (x, y, z), F):
                            blocked.append((x, y, z))
        chk("%s chute openings Y c+/-15, Z 24..40 pierce the full 2.0-in wall (throat liners included)" % A, not blocked,
            "wall material inside the openings at %s" % blocked[:4])
        edges = []
        for c in CHUTE_Y:
            for (p, what) in (((-0.3, c, CHUTE_SILL - 0.05), "sill"), ((-0.1, c, CHUTE_SILL + CHUTE_H + 0.05), "head"),
                              ((-0.3, c - CHUTE_W / 2 - 0.05, 30.0), "jamb -"), ((-0.3, c + CHUTE_W / 2 + 0.05, 30.0), "jamb +")):
                if not f.inside(r["panel"] + r["glaze"], p, F):
                    edges.append((c, what))
        chk("%s chute openings are bounded by wall at sill 24, head 40 and jambs c+/-15" % A, not edges,
            "missing wall at %s" % edges)

        # sill edge radius 0.5 (ref) on the field-side sill edge
        ds = [f.dist_point(r["panel"], (0.0, c, CHUTE_SILL), F) for c in CHUTE_Y]
        want = SILL_R * (math.sqrt(2) - 1)
        chk("%s OUTFITTER sill edge rounded R0.5 (ref) on the wall panel" % A,
            all(abs(d - want) < 0.02 for d in ds),
            "sharp-corner-to-panel distance %s, want %.4f (R0.5 round)" % (["%.4f" % d for d in ds], want))

        # §5: "Alliance wall thickness at the chute 2.0 in (ref)": wall material (panel / glazing /
        # frame / throat liner) must bound the opening through the full 2.0 depth.  Probes 0.1 in
        # outside each edge of the 30 x 16 opening, at depths x = -0.1 .. -1.9 behind the field face
        # (1.75 = 2.0 - (ref) 0.25 is the least acceptable depth), along the sill and head at three
        # stations and along both jambs at Z 25 / 32 / 38.5 (the solid band).
        wt = wall + throats
        depths = (-0.1, -0.5, -0.9, -1.3, -1.7, -1.9)
        missing = []
        for c in CHUTE_Y:
            pts = []
            for yy in (c - 12.0, c, c + 12.0):
                pts.append(((yy, CHUTE_SILL - 0.1), "sill"))
                pts.append(((yy, CHUTE_SILL + CHUTE_H + 0.1), "head"))
            for zz in (25.0, 32.0, 38.5):
                pts.append(((c - CHUTE_W / 2 - 0.1, zz), "jamb -"))
                pts.append(((c + CHUTE_W / 2 + 0.1, zz), "jamb +"))
            for (yz, what) in pts:
                for x in depths:
                    zp = yz[1]
                    if what == "sill" and x > -SILL_R:
                        zp = CHUTE_SILL - SILL_R - 0.1      # below the R0.5 field-side sill roundover
                    if not f.inside(wt, (x, yz[0], zp), F):
                        missing.append("%s@Y%g z%.1f x%.1f" % (what, c, yz[1], x))
        chk("%s wall is 2.0 in thick at the chute: sill, head and jambs bounded to x = -1.9 (§5, ref +/-0.25)" % A,
            not missing, "no wall/throat material 0.1 in outside the opening at %s" % missing[:6])
        # the same through the 1-in strip of the jambs that lies in the glazed band (Z 39..40): the
        # 0.25 glazing is the only field-side layer there, so the throat liner must reach it
        missing = []
        for c in CHUTE_Y:
            for yy in (c - CHUTE_W / 2 - 0.1, c + CHUTE_W / 2 + 0.1):
                for zz in (39.25, 39.75):
                    for x in depths:
                        if not f.inside(wt, (x, yy, zz), F):
                            missing.append("Y%g z%.2f x%.1f" % (yy, zz, x))
        chk("%s chute jambs lined through the full 2.0 depth where they pass the glazed band (Z 39..40, §5)" % A,
            not missing, "open (no wall/glazing/throat material) 0.1 in outside the jamb at %s — the jamb liner stops at "
            "the panel's back plane x = -0.75 while the glazing above Z 39 is only 0.25 deep" % missing[:6])

        # throat liner: one body per chute, flush with the opening, joined to the panel and glazing
        for o, c in enumerate(CHUTE_Y, start=1):
            th = chute[(A, o)]["chute throat"]
            if not th:
                chk("%s OUTFITTER %d chute throat liner present" % (A, o), False, "no body '%s OUTFITTER %d chute throat'" % (A, o))
                continue
            tb = f.bbox(th, F)
            ns = len(f.solids(th))
            cvw = f.common_volume(th, wall)
            dw = f.dist(th, r["panel"])
            chk("%s OUTFITTER %d chute throat: one solid in the 2.0-in wall depth (x -2..0), around Y c+/-15 Z 24..40, "
                "touching the panel, no overlap with panel/glazing/frame" % (A, o),
                len(th) == 1 and ns == 1 and tb[0] >= -WALL_T - EPS and tb[3] <= EPS
                and tb[1] < c - CHUTE_W / 2 and tb[4] > c + CHUTE_W / 2 and tb[2] < CHUTE_SILL and tb[5] > CHUTE_SILL + CHUTE_H
                and cvw < 1e-4 and dw < EPS,
                "bodies %d solids %d local bbox %s; common with wall %.5f; gap to panel %.4f" % (len(th), ns, _box_str(tb), cvw, dw))

        # appearance / material
        rgb, al = f.color(r["panel"])
        mat = f.material(r["panel"])
        chk("%s lower panel appearance `wall` #9AA4B2 opaque, painted plywood" % A,
            tuple(rgb) == RGB_WALL and al == 1 and "plywood" in mat["name"].lower() and 350 <= mat["density"] <= 800,
            "rgb %s alpha %s material %s" % (rgb, al, mat))
        rgb, al = f.color(r["glaze"])
        mat = f.material(r["glaze"])
        chk("%s glazing appearance `glazing` #DCE8FA at 25 %%, polycarbonate" % A,
            tuple(rgb) == RGB_GLAZING and _near(al, ALPHA_GLAZING, 1e-9) and "polycarbonate" in mat["name"].lower()
            and 1180 <= mat["density"] <= 1230,
            "rgb %s alpha %s material %s" % (rgb, al, mat))
        bad = [x for x in r["frame"] if tuple(x["rgb"]) != RGB_WALL or x["alpha"] != 1 or "steel" not in x["mat"]["name"].lower()]
        chk("%s wall frame appearance `wall`, steel (lower panel is 'plywood on steel frame')" % A, not bad,
            "%d frame bodies off-spec, e.g. %s" % (len(bad), (bad[0]["rgb"], bad[0]["mat"]) if bad else ""))

        # support: the glazing sheet must be held by the wall structure, not float
        dgf = f.dist(r["glaze"], r["frame"])
        chk("%s glazing is backed by the wall frame (no air gap)" % A, dgf < EPS,
            "glazing back face x = -0.25 vs frame front face: gap %.3f in; the 39-in sheet touches only the "
            "panel's top edge" % dgf)

    # ---- 2. driver stations --------------------------------------------------------------
    for A in ("BLUE", "RED"):
        F = FR[A]
        r = rec[A]
        wall = r["panel"] + r["glaze"] + r["frame"]
        chute_bodies = []
        for o in (1, 2):
            for v in chute[(A, o)].values():
                chute_bodies += v
        chk("%s OUTFITTER chute bodies found behind the wall (throat, ramp, 2 cheeks, 2 funnel wings, leg per chute)" % A,
            all(len(chute[(A, o)]["chute throat"]) == 1 and len(chute[(A, o)]["chute ramp"]) == 1
                and len(chute[(A, o)]["cheek"]) == 2 and len(chute[(A, o)]["funnel wing"]) == 2
                and len(chute[(A, o)]["ramp leg"]) == 1 for o in (1, 2)),
            "; ".join("chute %d: %s" % (o, {k: len(v) for k, v in chute[(A, o)].items()}) for o in (1, 2)))
        prev_hi = None
        for i, s in enumerate(STATION_Y, start=1):
            sh = r["shelf%d" % i]
            if not sh:
                continue
            b = f.bbox(sh, F)
            lo, hi = s - STATION_W / 2, s + STATION_W / 2
            chk("%s station %d shelf top at Z 36, 0.75 thick" % (A, i),
                _near(b[5], SHELF_TOP) and _near(b[5] - b[2], SHELF_T), "z %.3f..%.3f" % (b[2], b[5]))
            chk("%s station %d shelf on the driver side: from the lower panel's back face x = -0.75 back 12 in (ref)" % (A, i),
                _near(b[3], -PANEL_T) and _near(b[0], -PANEL_T - SHELF_D), "shelf local x %.3f..%.3f want -12.750..-0.750" % (b[0], b[3]))
            cvs = f.common_volume(sh, wall)
            chk("%s station %d shelf shares no volume with the wall panel, glazing or frame" % (A, i), cvs < 1e-4,
                "common %.5f in^3" % cvs)
            chk("%s station %d shelf lies inside its 96-in station band (Y %g..%g)" % (A, i, lo, hi),
                b[1] >= lo - EPS and b[4] <= hi + EPS, "shelf y %.3f..%.3f" % (b[1], b[4]))
            # world position: Blue at Y = s, Red at the rotation Y = 324 - s
            bw = f.bbox(sh)
            wy = s if A == "BLUE" else FIELD_W - s
            wlo, whi = wy - STATION_W / 2, wy + STATION_W / 2
            chk("%s station %d world band Y %g..%g (centre %g)" % (A, i, wlo, whi, wy),
                bw[1] >= wlo - EPS and bw[4] <= whi + EPS and ((A == "BLUE" and bw[3] <= EPS) or (A == "RED" and bw[0] >= FIELD_L - EPS)),
                "world bbox %s" % _box_str(bw))
            # coverage: the whole 96-in band except the OUTFITTER funnel (plus <= 3 in margin);
            # stubs narrower than 12 in beside the chute are not counted
            chute_here = [c for c in CHUTE_Y if lo < c < hi]
            if not chute_here:
                chk("%s station %d shelf spans the full 96-in station width" % (A, i),
                    _near(b[1], lo) and _near(b[4], hi), "shelf y %.3f..%.3f want %g..%g" % (b[1], b[4], lo, hi))
            else:
                c = chute_here[0]
                fb = f.bbox([x for x in chute_bodies if abs(0.5 * (f.bbox([x], F)[1] + f.bbox([x], F)[4]) - c) < 30], F)
                # funnel plan outline: the measured chute bodies, but never wider than §5 allows
                # (36-in flare at the loading end + the 0.5 cheek plate each side)
                half = FLARE_W / 2 + CHEEK_T
                if c < s:
                    need = (max(lo, min(fb[4], c + half) + 3.0), hi)
                else:
                    need = (lo, min(hi, max(fb[1], c - half) - 3.0))
                chk("%s station %d shelf covers its band except the OUTFITTER funnel (Y %.1f..%.1f needed)" % (A, i, need[0], need[1]),
                    b[1] <= need[0] + EPS and b[4] >= need[1] - EPS,
                    "shelf y %.3f..%.3f (%.1f in wide of the 96-in station; funnel occupies y %.2f..%.2f)"
                    % (b[1], b[4], b[4] - b[1], fb[1], fb[4]))
                d = f.dist(sh, chute_bodies)
                chk("%s station %d shelf clear of the OUTFITTER throat/ramp/cheeks/funnel wings, not over-cut (0 < gap <= 3)" % (A, i),
                    0.0 < d <= 3.0, "gap %.3f in" % d)
                # necessity: a full 96-in shelf at the same depth and height would hit the chute
                virt = _box_solid(F, (b[0], lo, b[2]), (b[3], hi, b[5]))
                cv = f.common_volume(_rec(virt), chute_bodies)
                chk("%s station %d: a full 96-in shelf at the modelled depth/height would collide with the "
                    "OUTFITTER chute (cut-back required)" % (A, i), cv > 1.0,
                    "virtual full shelf overlaps ramp/cheeks by %.2f in^3" % cv)
            if prev_hi is not None:
                chk("%s stations %d/%d: 108-in pitch leaves a 12-in gap between shelves" % (A, i - 1, i),
                    b[1] >= prev_hi - EPS, "shelf %d ends %.3f, shelf %d starts %.3f" % (i - 1, prev_hi, i, b[1]))
            prev_hi = b[4]
            # appearance
            rgb, al = f.color(sh)
            mat = f.material(sh)
            chk("%s station %d shelf appearance `wall`, painted plywood" % (A, i),
                tuple(rgb) == RGB_WALL and al == 1 and "plywood" in mat["name"].lower(),
                "rgb %s alpha %s material %s" % (rgb, al, mat["name"]))
            # attachment: the shelf must be carried by the wall, not float behind it
            d = f.dist(sh, wall)
            chk("%s station %d shelf is attached to the wall (touches wall structure)" % (A, i), d < EPS,
                "gap to panel/frame %.3f in: no bracket or frame member at Z 35.25-36 in the station span" % d)
            # window in the glazed band: glazing at the station centre, no frame post in front
            bad = [z for z in np.arange(39.5, WALL_H, 2.0) if not f.inside(r["glaze"], (-GLAZE_T / 2, s, z), F)]
            # the welded frame is one body: look for frame steel in the station's window
            # (Y lo..hi, Z 40..75, the whole wall depth) instead of per-member bounding boxes
            win = _rec(_box_solid(F, (-WALL_T - 1.0, lo + EPS, SOLID_TOP + 1), (0.0, hi - EPS, WALL_H - 3)))
            cvp = f.common_volume(r["frame"], win)
            chk("%s station %d window: glazed band 39-78 at the station, no frame post inside the station band" % (A, i),
                not bad and cvp < 1e-4, "unglazed z %s; frame steel in the window %.4f in^3" % (bad[:3], cvp))

            # buttons
            for key, rgb_w, label in (("estop", RGB_ESTOP, "E-STOP"), ("astop", RGB_ASTOP, "A-STOP")):
                hd = r["%s%d" % (key, i)]
                bs = r["%sb%d" % (key, i)]
                if not hd:
                    continue
                hb = f.bbox(hd, F)
                dx, dy = hb[3] - hb[0], hb[4] - hb[1]
                chk("%s station %d %s head dia 2.0" % (A, i, label), _near(dx, BUTTON_D, 0.005) and _near(dy, BUTTON_D, 0.005),
                    "head %.4f x %.4f" % (dx, dy))
                rgb, al = f.color(hd)
                mat = f.material(hd)
                chk("%s station %d %s colour %s, opaque, molded plastic" % (A, i, label, "#CC2020" if key == "estop" else "#1D63C8"),
                    tuple(rgb) == rgb_w and al == 1 and ("abs" in mat["name"].lower() or "plastic" in mat["name"].lower())
                    and 900 <= mat["density"] <= 1300,
                    "rgb %s alpha %s material %s" % (rgb, al, mat))
                # mushroom: head wider than its stem, sitting on top of it, domed crown
                cxy = (0.5 * (hb[0] + hb[3]), 0.5 * (hb[1] + hb[4]))
                stem_ok, detail = True, "no stem body"
                support = hd
                if bs:
                    sb = f.bbox(bs, F)
                    stem_ok = (sb[3] - sb[0]) < BUTTON_D - 0.2 and sb[5] <= hb[2] + EPS
                    detail = "stem %.3f wide z %.3f..%.3f; head z %.3f..%.3f" % (sb[3] - sb[0], sb[2], sb[5], hb[2], hb[5])
                    support = bs + hd
                dome = (f.inside(hd, (cxy[0], cxy[1], hb[5] - 0.02), F)
                        and not f.inside(hd, (cxy[0] + 0.9 * BUTTON_D / 2, cxy[1], hb[5] - 0.02), F))
                chk("%s station %d %s is a mushroom head (overhangs a narrower stem, domed crown)" % (A, i, label),
                    stem_ok and dome, detail + ("; domed" if dome else "; crown not domed"))
                sp = f.bbox(support, F)
                on_shelf = (_near(sp[2], SHELF_TOP) and sp[0] >= b[0] - EPS and sp[3] <= b[3] + EPS
                            and sp[1] >= b[1] - EPS and sp[4] <= b[4] + EPS and f.dist(support, sh) < EPS)
                chk("%s station %d %s sits on its own station's shelf" % (A, i, label), on_shelf,
                    "button bbox %s, shelf bbox %s" % (_box_str(sp), _box_str(b)))
                cv = f.common_volume(support, sh + wall)
                chk("%s station %d %s does not intersect shelf or wall" % (A, i, label), cv < 1e-4, "common %.5f in^3" % cv)
            if r["estop%d" % i] and r["astop%d" % i]:
                d = f.dist(r["estop%d" % i], r["astop%d" % i])
                chk("%s station %d E-STOP and A-STOP are separate buttons (clear of each other)" % (A, i), d > 0.25,
                    "head-to-head gap %.3f in" % d)
            # a DRIVE TEAM member must be able to press them: nothing in a 4-in square x 18-in
            # tall column above either head
            for key, label in (("estop", "E-STOP"), ("astop", "A-STOP")):
                hd = r["%s%d" % (key, i)]
                if not hd:
                    continue
                hb = f.bbox(hd, F)
                cxy = (0.5 * (hb[0] + hb[3]), 0.5 * (hb[1] + hb[4]))
                col = _rec(_box_solid(F, (cxy[0] - 2, cxy[1] - 2, hb[5] + 0.01), (cxy[0] + 2, cxy[1] + 2, hb[5] + 18)))
                cb = _fast_box(col[0])
                blk = []
                for y in f.records():
                    yb = _fast_box(y)
                    if any(cb[j] > yb[j + 3] or yb[j] > cb[j + 3] for j in range(3)):
                        continue
                    if f.common_volume(col, [y]) > 1e-4:
                        blk.append(y["name"])
                chk("%s station %d %s is unobstructed from above (reachable)" % (A, i, label), not blk,
                    "bodies over the button: %s" % blk[:3])

    # ---- 3. CACHE CRATE slides down each chute ramp past the driver-station shelves ------------
    # Two virtual crates ride the ramp (FIELD-CAD-PACKAGE §9.1: it rests on its bottom crown):
    #   * ENV  - the 13.0-in maximum envelope as a cube whose bottom face lies on the ramp
    #            (conservative: bigger than the real crate everywhere) -> clearance check;
    #   * REAL - the modelled CACHE CRATE body -> "would an uncut 96-in shelf block it?".
    th = math.radians(RAMP_ANG)
    Ry = np.array([[math.cos(th), 0, math.sin(th)], [0, 1, 0], [-math.sin(th), 0, math.cos(th)]])
    n_up = np.array([math.sin(th), 0, math.cos(th)])       # ramp up-normal (local)
    up = np.array([-math.cos(th), 0, math.sin(th)])        # up-slope direction (local)
    E = CRATE + 2 * CROWN
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
    env_src = K._solids(BRepPrimAPI_MakeBox(K.gp_Pnt(-E / 2, -E / 2, -E / 2), K.gp_Pnt(E / 2, E / 2, E / 2)).Shape())
    real_src, real_c = None, None
    try:
        cr0 = f.find("re:^CACHE CRATE - ")[0]
        real_src = cr0["solids"]
        cb = f.bbox([cr0])
        real_c = np.array([(cb[0] + cb[3]) / 2, (cb[1] + cb[4]) / 2, (cb[2] + cb[5]) / 2])
    except KeyError:
        pass

    def place(src, ctr, F, p_local):
        Fm = np.array([F.x, F.y, F.z]).T
        M = Fm @ Ry
        return _xform(src, _trsf_from(M, F.pt(p_local) - M @ ctr))

    for A in ("BLUE", "RED"):
        F = FR[A]
        r = rec[A]
        stations = []
        for i in (1, 2, 3):
            for k in ("shelf", "estop", "astop", "estopb", "astopb"):
                stations += r["%s%d" % (k, i)]
        for o, c in enumerate(CHUTE_Y, start=1):
            ramp = _find(f, "%s OUTFITTER %d chute ramp" % (A, o))
            if not ramp:
                continue
            rb = f.bbox(ramp, F)
            x_sill = rb[3]                                  # ramp top meets the sill line here
            near = [x for x in stations if abs(0.5 * (f.bbox([x], F)[1] + f.bbox([x], F)[4]) - c) < 90]
            full = []
            for i, s in enumerate(STATION_Y, start=1):
                if s - STATION_W / 2 < c < s + STATION_W / 2 and r["shelf%d" % i]:
                    sb = f.bbox(r["shelf%d" % i], F)
                    full = _box_solid(F, (sb[0], s - STATION_W / 2, sb[2]), (sb[3], s + STATION_W / 2, sb[5]))
            worst, hits, ramp_bad, virt_hit = 1e9, [], [], 0.0
            for sd in np.arange(8.0, 34.0, 2.0):
                base = np.array([x_sill, c, CHUTE_SILL]) + up * sd
                for dy in (-8.0, 0.0, 8.0):
                    lat = np.array([0, dy, 0])
                    env = _rec(place(env_src, np.zeros(3), F, base + n_up * (E / 2) + lat))
                    d = f.dist(env, near) if near else 1e9
                    worst = min(worst, d)
                    if d < 1e-6 and f.common_volume(env, near) > 1e-4:
                        hits.append((float(sd), dy))
                    if dy == 0.0 and real_src is not None:
                        real = _rec(place(real_src, real_c, F, base + n_up * (CRATE / 2 + CROWN)))
                        if f.common_volume(real, ramp) > 1e-3 or f.dist(real, ramp) > 0.05:
                            ramp_bad.append(float(sd))
                        if full:
                            virt_hit = max(virt_hit, f.common_volume(real, _rec(full)))
            chk("%s OUTFITTER %d: virtual CACHE CRATE rests on the 30-deg ramp surface (sweep is valid)" % (A, o),
                not ramp_bad, "crate not seated on the ramp at slope stations %s" % ramp_bad[:4])
            chk("%s OUTFITTER %d: 13.0-in crate envelope slides the whole ramp (+/-8 in lateral) clear of every "
                "driver-station shelf and button" % (A, o),
                not hits and worst > 0, "min clearance %.3f in; collisions at %s" % (worst, hits[:4]))
            if full:
                chk("%s OUTFITTER %d: an uncut 96-in shelf would block the sliding crate (cut-back is necessary)" % (A, o),
                    virt_hit > 1.0, "max overlap of the real crate with a virtual full shelf %.2f in^3" % virt_hit)

    # ---- 4. Red is the 180-degree rotation of Blue ----------------------------------------
    tr = _rot180()
    keys = ["panel", "glaze", "frame"] + ["%s%d" % (k, i) for i in (1, 2, 3) for k in ("shelf", "estop", "astop", "estopb", "astopb")]
    bad = []
    for k in keys:
        b_ = rec["BLUE"][k]
        r_ = rec["RED"][k]
        if not b_ or not r_:
            bad.append((k, "missing"))
            continue
        rb = _xform(f.solids(b_), tr)
        vb = K._volume(rb)
        vr = f.volume(r_)
        cv = f.common_volume(_rec(rb), r_)
        if abs(vb - vr) > 1e-3 * max(1.0, vr) or cv < vr - 1e-3 * max(1.0, vr):
            bad.append((k, "Vblue %.3f Vred %.3f common %.3f" % (vb, vr, cv)))
    chk("RED wall, stations and buttons are the BLUE ones rotated 180 deg about (324, 162)", not bad,
        "mismatch %s" % bad[:4])

    # ---- 5. no interference with anything else on the field --------------------------------
    mine = set()
    for A in rec:
        for k, v in rec[A].items():
            for x in v:
                mine.add(id(x))
    others = [x for x in f.records() if id(x) not in mine]
    obox = [(y, _fast_box(y)) for y in others]
    hits = []
    for A in rec:
        for k, v in rec[A].items():
            for x in v:
                bx = _fast_box(x)
                for y, by in obox:
                    if any(bx[j] > by[j + 3] or by[j] > bx[j + 3] for j in range(3)):
                        continue
                    cv = f.common_volume([x], [y])
                    if cv > 1e-4:
                        hits.append("%s x %s: %.4f in^3" % (x["name"], y["name"], cv))
    chk("walls, shelves and buttons share no volume with any other body", not hits, "; ".join(hits[:5]))
    return out
