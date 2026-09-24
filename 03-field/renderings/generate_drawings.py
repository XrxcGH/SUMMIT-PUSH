# -*- coding: utf-8 -*-
"""
Generates the six SUMMIT PUSH field drawing sheets from the locked
dimension ledger. Run from anywhere:

    python 03-field/renderings/generate_drawings.py

Every dimension below comes from 03-field/FIELD-CAD-PACKAGE.md 10
(the master dimension ledger). Change a number here only if the ledger
changed first.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _drawlib import *  # noqa: F401,F403
from _drawlib import Sheet

# =====================================================================
# LOCKED DIMENSIONS (master ledger)
# =====================================================================
FL, FW = 648.0, 324.0                 # field carpet
CRAG_B = (324.0, 240.0)               # blue crag center
CRAG_R = (324.0, 84.0)
CRAG_S = 48.0                         # footprint
BODY_H = 60.0                         # tower top plate
SPIRE_S = 20.0
SPIRE_TOP = 90.0
LANTERN_LO = 78.0                     # translucent beacon section 78 -> 90
BEACON_Z = 84.0
SHELF1, SHELF2 = 24.0, 42.0
SHELF_DEPTH = 14.0
SLOT_W = 14.0
SLOT_CTRS = (-15.5, 0.0, 15.5)
FENCE_W, FENCE_H = 1.5, 2.0
SOCK_STANDOFF = 8.0
SOCK_TUBE = 7.0
SOCK_ID = 6.50
SOCK_WALL = 0.09
SOCK_OD = SOCK_ID + 2 * SOCK_WALL
LOW_SOCK_Z, MID_SOCK_Z = 30.0, 54.0
SUM_SOCK_Z = 72.0
SOCK_LAT = 14.0
SOCK_TILT = 30.0
SUM_TILT = 15.0
PEG_OD = 1.5
PEG_EXP = 10.0
PEG_ANG = 45.0
LOW_PEG_Z, MID_PEG_Z, HIGH_PEG_Z = 30.0, 54.0, 78.0
PEG_LAT, HPEG_LAT = 14.0, 7.0
DEPOT_LIP = 4.0
DEPOT_CH = 16.0
DEPOT_WRAP = 16.0
LIP_THK = 0.75
TIER_Z = (30.0, 54.0, 78.0)
HW_X = 48.0                            # plane P carpet line (Blue)
HW_LEAN = 15.0
HW_W = 144.0
LANE_W = 48.0
LANE_Y = (114.0, 162.0, 210.0)
RUNG_TOP = (30.0, 54.0, 78.0)
RUNG_OD = 1.5
RUNG_L = 20.0
RUNG_STAG = 12.0
TRUSS_TOP = 84.0
TRUSS_CLR = 4.0
CHUTE_W, CHUTE_H, CHUTE_SILL = 30.0, 16.0, 24.0
CHUTE_Y = (30.0, 294.0)
LANE_TAPE = (36.0, 48.0)
APRON_XF, APRON_YF, APRON_R = 36.0, 20.0, 20.0
BASECAMP = (0.0, 48.0, 90.0, 234.0)
CACHE_X = (300.0, 324.0, 348.0)
CACHE_Y = (138.0, 162.0, 186.0)
STAGE_X_B, STAGE_X_R = 144.0, 504.0
STAGE_Y = (108.0, 162.0, 216.0)
TAG_BODY, TAG_TGT, TAG_PANEL = 6.5, 8.125, 9.0
TAG_Z_CRAG, TAG_Z_HW, TAG_Z_OUT = 17.5, 12.0, 52.0
TAG_HW_X = 39.0
CRATE_S, CRATE_CROWN = 12.0, 0.5
CELL_D, CELL_L, CELL_DOME = 5.0, 14.0, 1.5
COIL_OD, COIL_TUBE, COIL_ID = 10.0, 2.5, 5.0

T15 = math.tan(math.radians(15.0))
NOTES = [
    "All dimensions in INCHES. Heights are to the robot-interaction surface (shelf top, socket rim center, peg root, rung top, tag center).",
    "Boxed values are CRITICAL - hold exactly. Values suffixed (ref) may float +/-0.25 in. Every angle on the field is 15, 30 or 45 degrees.",
    "Coordinate frame: always-blue-origin NWU. Origin at the right corner of the Blue alliance wall; +X toward Red, +Y left, +Z up. Blue half shown; Red = 180 deg rotation about (324, 162).",
]


def rung_center_x(top):
    """Blue rung centerline X for a given rung-top height."""
    return HW_X - (top - RUNG_OD / 2.0) * T15


def truss_face_x(z):
    """Field-side face of the truss structure at height z (Blue)."""
    return HW_X - TRUSS_CLR / math.cos(math.radians(15.0)) - z * T15


def _crag_plan(s, fx, fy, SC, cx, cy, d, col, cold, name):
    """Draw one CRAG in plan. d = +1 if its SHELF FACE is the +X face."""
    half = CRAG_S / 2.0
    shelf_plane = cx + d * half
    peg_plane = cx - d * half

    def R(x0, x1, y0, y1, **kw):
        s.rect(min(fx(x0), fx(x1)), min(fy(y0), fy(y1)),
               abs(fx(x1) - fx(x0)), abs(fy(y1) - fy(y0)), **kw)

    # BASE DEPOT: outer leg + two corner squares closing it + two corner arms
    R(shelf_plane, shelf_plane + d * DEPOT_CH,
      cy - half - DEPOT_WRAP, cy + half + DEPOT_WRAP,
      fill=DEPOT, stroke=CRAG_EDGE, sw=1.1, op=0.95)
    for sg in (-1, 1):
        R(shelf_plane, shelf_plane - d * DEPOT_WRAP, cy + sg * half,
          cy + sg * (half + DEPOT_WRAP), fill=DEPOT, stroke=CRAG_EDGE, sw=1.1, op=0.95)
    # CRAG body and spire
    R(cx - half, cx + half, cy - half, cy + half, fill=col, stroke=cold, sw=2.2, op=0.70)
    R(cx - SPIRE_S / 2, cx + SPIRE_S / 2, cy - SPIRE_S / 2, cy + SPIRE_S / 2,
      fill="#FFFFFF", stroke=cold, sw=1.2, op=0.9)
    s.text(fx(cx), fy(cy) + 3, "SPIRE", size=7.5, fill=cold, weight="bold", anchor="middle")
    # sockets
    for lat, nm in ((d * SOCK_LAT, "LOW"), (-d * SOCK_LAT, "MID")):
        for sg in (-1, 1):
            s.circle(fx(cx + lat), fy(cy + sg * (half + SOCK_STANDOFF)),
                     SC * SOCK_OD / 2, fill=SOCKET_L, stroke=BLUE_D, sw=1.1)
    # summit socket
    s.circle(fx(shelf_plane + d * SOCK_STANDOFF), fy(cy), SC * SOCK_OD / 2,
             fill=SOCKET_L, stroke=BLUE_D, sw=1.4)
    # pegs
    for sg in (-1, 1):
        s.line(fx(peg_plane), fy(cy + sg * PEG_LAT),
               fx(peg_plane - d * PEG_EXP * 0.7071), fy(cy + sg * PEG_LAT),
               stroke="#555555", sw=3.0, cap="round")
        s.line(fx(cx - d * SPIRE_S / 2), fy(cy + sg * HPEG_LAT),
               fx(cx - d * (SPIRE_S / 2 + PEG_EXP * 0.7071)), fy(cy + sg * HPEG_LAT),
               stroke="#555555", sw=3.0, cap="round", dash="3 2")
    # APRON
    ax0, ax1 = cx - half - APRON_XF, cx + half + APRON_XF
    ay0, ay1 = cy - half - APRON_YF, cy + half + APRON_YF
    s.rect(fx(ax0), fy(ay1), SC * (ax1 - ax0), SC * (ay1 - ay0), fill="none",
           stroke=cold, sw=1.8, dash="8 5", rx=SC * APRON_R)
    s.text(fx(cx), fy(ay1) - 7, name, size=9.5, fill=cold, weight="bold", anchor="middle")


def sheet_field():
    s = Sheet(1460, 940, "DRAWING 1 OF 6 - FIELD TOP VIEW (PLAN)", 1, 6,
              "Field 648 x 324 in (54 ft x 27 ft) - scale 1.8 px/in - Blue alliance at left")
    SC = 1.8
    OX, OY = 112, 74

    def fx(X):
        return OX + SC * X

    def fy(Y):
        return OY + SC * (FW - Y)

    s.rect(fx(0), fy(FW), SC * FL, SC * FW, fill=CARPET, stroke=INK, sw=2.4)
    for yy in (FW, 0):
        s.rect(fx(0), fy(yy) - (5 if yy == FW else 0), SC * FL, 5, fill=WALL,
               stroke=WALL_D, sw=0.8)
    s.rect(fx(0) - 9, fy(FW), 9, SC * FW, fill=BLUE, stroke=BLUE_D, sw=1.2, op=0.30)
    s.rect(fx(FL), fy(FW), 9, SC * FW, fill=RED, stroke=RED_D, sw=1.2, op=0.30)
    s.text(fx(0) - 18, fy(FW / 2), "BLUE ALLIANCE WALL", size=10, fill=BLUE_D,
           weight="bold", anchor="middle", rot=-90)
    s.text(fx(FL) + 22, fy(FW / 2), "RED ALLIANCE WALL", size=10, fill=RED_D,
           weight="bold", anchor="middle", rot=90)
    # FIELD centerline: 2-in white TAPE, broken where the two CRAG footprints cross
    # it (the DEPOT trays stop 8 in short). G402 and G502 are line calls against it.
    for _y0, _y1 in ((324.0, 264.0), (216.0, 108.0), (60.0, 0.0)):
        s.line(fx(FL / 2), fy(_y0), fx(FL / 2), fy(_y1), stroke="#FFFFFF", sw=3.0)
        s.line(fx(FL / 2), fy(_y0), fx(FL / 2), fy(_y1), stroke=MUTED, sw=0.7, dash="10 6")
    s.text(fx(FL / 2) + 6, fy(FW) + 16, "FIELD CENTERLINE X = 324 (2-in white tape)",
           size=8.5, fill=MUTED)

    for mir in (False, True):
        def X(v):
            return FL - v if mir else v

        def Y(v):
            return FW - v if mir else v
        col, cold = (RED, RED_D) if mir else (BLUE, BLUE_D)
        nm = "RED" if mir else "BLUE"

        x0, x1, y0, y1 = BASECAMP
        s.rect(min(fx(X(x0)), fx(X(x1))), min(fy(Y(y0)), fy(Y(y1))), SC * 48, SC * 144,
               fill=col, stroke=cold, sw=1.4, dash="6 4", op=0.10)
        # CLIMB LINE: the G416 plane, carried to the full field width. Over
        # Y 90-234 the BASECAMP boundary above already marks it.
        for _y0, _y1 in ((0.0, 90.0), (234.0, 324.0)):
            s.line(fx(X(48.0)), fy(Y(_y0)), fx(X(48.0)), fy(Y(_y1)),
                   stroke=cold, sw=1.4, dash="5 5")
        s.text(fx(X(24)), fy(Y(162)), "BASECAMP = HEADWALL ZONE", size=8,
               fill=cold, weight="bold", anchor="middle", rot=-90 if not mir else 90)

        htop = HW_X - TRUSS_TOP * T15
        s.rect(min(fx(X(htop)), fx(X(HW_X))), min(fy(Y(90.0)), fy(Y(234.0))),
               abs(fx(X(HW_X)) - fx(X(htop))), SC * HW_W,
               fill=TRUSS, stroke=TRUSS_D, sw=1.6, op=0.85)
        for yb in (138.0, 186.0):
            s.line(fx(X(htop)), fy(Y(yb)), fx(X(HW_X)), fy(Y(yb)), stroke=TRUSS_D, sw=1.2)
        s.text(fx(X(36)), fy(Y(240)), "%s HEADWALL" % nm, size=9, fill=TRUSS_D,
               weight="bold", anchor="middle")
        for i, ly in enumerate(LANE_Y):
            s.text(fx(X(36)), fy(Y(ly)) + 3, "L%d" % (i + 1), size=8, fill="#FFFFFF",
                   weight="bold", anchor="middle")

        for cy_ in CHUTE_Y:
            s.rect(min(fx(X(0)), fx(X(48))),
                   min(fy(Y(cy_ - 18)), fy(Y(cy_ + 18))), SC * 48, SC * 36,
                   fill="#E8A33D", stroke="#B57718", sw=1.5, dash="6 4", op=0.28)
            s.rect(fx(X(0)) - (6 if mir else 0),
                   min(fy(Y(cy_ - 15)), fy(Y(cy_ + 15))), 6, SC * 30,
                   fill="#E8A33D", stroke="#B57718", sw=1.3)
            s.text(fx(X(24)), fy(Y(cy_)) + 3, "OUTFITTER LANE 36 x 48", size=7.5,
                   fill="#7A4E0C", anchor="middle")
            s.text(fx(X(24)), fy(Y(cy_)) + 13, "chute (%d, %d)" % (X(0), Y(cy_)),
                   size=7, fill="#7A4E0C", anchor="middle")

        sx_ = STAGE_X_R if mir else STAGE_X_B
        for ty_, t in zip(STAGE_Y, ("2 CRATES", "2 O2 CELLS", "2 ROPE COILS")):
            s.line(fx(sx_) - 9, fy(Y(ty_)) - 9, fx(sx_) + 9, fy(Y(ty_)) + 9, stroke=cold, sw=1.6)
            s.line(fx(sx_) - 9, fy(Y(ty_)) + 9, fx(sx_) + 9, fy(Y(ty_)) - 9, stroke=cold, sw=1.6)
            s.text(fx(sx_), fy(Y(ty_)) - 14, t, size=7.5, fill=cold, anchor="middle")
        s.text(fx(sx_), fy(Y(258)), "%s STAGING MARKS  X = %d" % (nm, sx_), size=8.5,
               fill=cold, weight="bold", anchor="middle")

        ccx, ccy = (CRAG_R if mir else CRAG_B)
        _crag_plan(s, fx, fy, SC, ccx, ccy, 1 if mir else -1, col, cold,
                   "%s CRAG (%d, %d)" % (nm, ccx, ccy))

    s.rect(fx(300), fy(216), SC * 48, SC * 108, fill="#FFFFFF", stroke=MUTED,
           sw=1.3, dash="7 4", op=0.5)
    LATIN = {(300, 186): ("CRATE", CRATE), (324, 186): ("O2", CELL_CAP), (348, 186): ("COIL", COIL),
             (300, 162): ("COIL", COIL), (324, 162): ("CRATE", CRATE), (348, 162): ("O2", CELL_CAP),
             (300, 138): ("O2", CELL_CAP), (324, 138): ("COIL", COIL), (348, 138): ("CRATE", CRATE)}
    for (mx, my), (lbl, c) in LATIN.items():
        s.line(fx(mx) - 7, fy(my) - 7, fx(mx) + 7, fy(my) + 7, stroke=MUTED, sw=1.4)
        s.line(fx(mx) - 7, fy(my) + 7, fx(mx) + 7, fy(my) - 7, stroke=MUTED, sw=1.4)
        s.circle(fx(mx), fy(my), 7.0, fill=c, stroke="#333333", sw=0.9)
    s.leader(fx(324), fy(162), fx(324) - 190, fy(162) - 4,
             "CENTER CACHE  X 300-348, Y 108-216", anchor="end")

    # dimensions
    s.dim_h(fx(0), fx(FL), fy(0) + 52, "648.0", ext_from=fy(0) + 8, critical=True)
    s.dim_v(fy(FW), fy(0), fx(0) - 54, "324.0", ext_from=fx(0) - 12, critical=True)
    s.dim_h(fx(0), fx(48), fy(234) - 30, "48.0", ext_from=fy(234) - 6, critical=True, size=9)
    s.dim_v(fy(234), fy(90), fx(66), "144.0", ext_from=fx(58), critical=True, size=9, side="right")
    s.dim_h(fx(264), fx(384), fy(304), "120.0 apron span (36 + 48 + 36)",
            ext_from=fy(300) - 4, size=9)
    s.dim_v(fy(264), fy(216), fx(410), "48.0", ext_from=fx(388), size=9, side="right", critical=True)
    s.dim_v(fy(216), fy(196), fx(438), "20.0", ext_from=fx(388), size=9, side="right", critical=True)
    s.dim_v(fy(128), fy(108), fx(438), "20.0", ext_from=fx(388), size=9, side="right", critical=True)
    s.dim_v(fy(196), fy(128), fx(466), "68.0 open corridor", ext_from=fx(442), size=9, side="right")

    # origin + axes
    s.circle(fx(0), fy(0), 5, fill="none", stroke=INK, sw=1.6)
    s.circle(fx(0), fy(0), 1.6, fill=INK, stroke=INK, sw=0.6)
    s.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6" marker-end="url(#arr)"/>'
          % (fx(0), fy(0), fx(0) + 56, fy(0), INK))
    s.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6" marker-end="url(#arr)"/>'
          % (fx(0), fy(0), fx(0), fy(0) - 56, INK))
    s.text(fx(0) + 60, fy(0) + 4, "+X", size=10, fill=INK, weight="bold")
    s.text(fx(0) - 4, fy(0) - 60, "+Y", size=10, fill=INK, weight="bold", anchor="end")
    s.text(fx(0) + 10, fy(0) + 18, "ORIGIN (0, 0), +Z up", size=8.5, fill=MUTED)
    s.scalebar(fx(FL) - 210, fy(0) + 62, SC, 48)
    s.text(fx(FL) - 210, fy(0) + 94, "Scale 1.8 px/in", size=8.5, fill=MUTED)

    # ---- notes panels ----
    lx, ly = 112, 762
    s.rect(lx, ly - 16, 470, 138, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(lx + 8, ly, "TAPE KEY", size=9.5, fill=ACCENT, weight="bold")
    items = [("BASECAMP / HEADWALL ZONE  X 0-48, Y 90-234", BLUE, "6 4"),
             ("CLIMB LINE  X = 48 / 600, full width - G416 line call", BLUE, "5 5"),
             ("CRAG APRON  36 shelf & peg faces / 20 socket faces / R20", BLUE, "8 5"),
             ("OUTFITTER LANE  36 x 48, centered on the chute", "#B57718", "6 4"),
             ("FIELD CENTERLINE  2-in white at X = 324 - G402 / G502 line call", MUTED, "10 6"),
             ("CENTER CACHE band + nine white marks", MUTED, "7 4")]
    for i, (t, c, dsh) in enumerate(items):
        yy = ly + 17 + i * 15
        s.line(lx + 10, yy - 3, lx + 40, yy - 3, stroke=c, sw=1.8, dash=dsh)
        s.text(lx + 46, yy, t, size=8.5, fill=INK)

    mx0 = 560
    s.rect(mx0, ly - 16, 420, 108, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(mx0 + 8, ly, "CENTER CACHE - LATIN SQUARE STAGING", size=9.5, fill=ACCENT, weight="bold")
    hdr = ("", "X = 300", "X = 324", "X = 348")
    colx = [mx0 + 8, mx0 + 96, mx0 + 202, mx0 + 308]
    for cxx, cell in zip(colx, hdr):
        s.text(cxx, ly + 18, cell, size=8.5, fill=ACCENT, weight="bold")
    for i, yv in enumerate((186, 162, 138)):
        row = ["Y = %d" % yv] + [LATIN[(xv, yv)][0] for xv in (300, 324, 348)]
        for cxx, cell in zip(colx, row):
            s.text(cxx, ly + 34 + i * 14, cell, size=8.5, fill=INK)
    s.text(mx0 + 8, ly + 80, "Each type appears once per row and once per column.", size=8, fill=MUTED)
    s.text(mx0 + 8, ly + 92, "Aggregate haul distance is identical for both alliances (725.0 in each).", size=8, fill=MUTED)

    nx0 = 996
    s.rect(nx0, ly - 16, 404, 108, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(nx0 + 8, ly, "PLAN NOTES", size=9.5, fill=ACCENT, weight="bold")
    for i, t in enumerate([
            "All tape 2.0 in wide; the line edge sits on the stated coordinate.",
            "Alliance-colored tape for alliance zones; white for neutral marks.",
            "CRAG plan tint is a drafting convention; the CRAG itself is tan",
            "(see 03-field/MATERIALS-AND-COLORS.md).",
            "Model the Blue half once, then rotate-pattern 180 deg about (324, 162)."]):
        s.text(nx0 + 8, ly + 17 + i * 13, t, size=8, fill=INK if i < 2 else MUTED)

    s.titleblock(NOTES)
    return s


# =====================================================================
# SHEET 6 - APRILTAG MAP
# =====================================================================
TAGS = [
    (1, 0, 30, TAG_Z_OUT, 0, "OUTFITTER"), (2, 0, 294, TAG_Z_OUT, 0, "OUTFITTER"),
    (3, TAG_HW_X, 114, TAG_Z_HW, 0, "HEADWALL"), (4, TAG_HW_X, 162, TAG_Z_HW, 0, "HEADWALL"),
    (5, TAG_HW_X, 210, TAG_Z_HW, 0, "HEADWALL"),
    (6, 300, 226, TAG_Z_CRAG, 180, "CRAG shelf"), (7, 300, 254, TAG_Z_CRAG, 180, "CRAG shelf"),
    (8, 310, 264, TAG_Z_CRAG, 90, "CRAG +Y socket"), (9, 338, 264, TAG_Z_CRAG, 90, "CRAG +Y socket"),
    (10, 310, 216, TAG_Z_CRAG, 270, "CRAG -Y socket"), (11, 338, 216, TAG_Z_CRAG, 270, "CRAG -Y socket"),
    (12, 348, 226, TAG_Z_CRAG, 0, "CRAG peg"), (13, 348, 254, TAG_Z_CRAG, 0, "CRAG peg"),
]
TAGS += [(i + 13, FL - x, FW - y, z, (yaw + 180) % 360, lab.replace("+Y", "@Y").replace("-Y", "+Y").replace("@Y", "-Y"))
         for (i, x, y, z, yaw, lab) in TAGS]


def sheet_tags():
    s = Sheet(1420, 900, "DRAWING 6 OF 6 - APRILTAG MAP", 6, 6,
              "26 tags, family 36h11 - body 6.5 in on an 8.125 in target on a 9.0 in panel - scale 1.8 px/in")
    SC = 1.8
    OX, OY = 96, 70

    def fx(X):
        return OX + SC * X

    def fy(Y):
        return OY + SC * (FW - Y)

    s.rect(fx(0), fy(FW), SC * FL, SC * FW, fill=CARPET, stroke=INK, sw=2.4)
    s.line(fx(FL / 2), fy(FW), fx(FL / 2), fy(0), stroke=MUTED, sw=1.2, dash="12 4 3 4")
    for cc, col in ((CRAG_B, BLUE), (CRAG_R, RED)):
        s.rect(fx(cc[0] - CRAG_S / 2), fy(cc[1] + CRAG_S / 2), SC * CRAG_S, SC * CRAG_S,
               fill=col, stroke=col, sw=1.2, op=0.16)
    for mir in (False, True):
        def X(v):
            return FL - v if mir else v

        def Y(v):
            return FW - v if mir else v
        htop = HW_X - TRUSS_TOP * T15
        s.rect(min(fx(X(htop)), fx(X(HW_X))), min(fy(Y(90.0)), fy(Y(234.0))),
               abs(fx(X(HW_X)) - fx(X(htop))), SC * HW_W,
               fill=TRUSS, stroke=TRUSS_D, sw=1.0, op=0.30)

    for (tid, x, y, z, yaw, lab) in TAGS:
        px, py = fx(x), fy(y)
        s.rect(px - 6, py - 6, 12, 12, fill="#F5F5F5", stroke="#666666", sw=0.9)
        s.rect(px - 3.6, py - 3.6, 7.2, 7.2, fill="#111111", stroke="none", sw=0)
        a = math.radians(yaw)
        nx, ny = math.cos(a), -math.sin(a)
        s.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.3" marker-end="url(#arr)"/>'
              % (px + nx * 7, py + ny * 7, px + nx * 24, py + ny * 24, DIM))
        off = 15
        s.text(px + nx * (off + 14), py + ny * (off + 14) + 3.5, str(tid),
               size=10, fill=INK, weight="bold", anchor="middle")

    s.text(fx(324), fy(FW) - 10,
           "Arrows show the tag FACE NORMAL (the direction a camera must look FROM to see it head-on is the opposite)",
           size=9, fill=MUTED, anchor="middle")

    # table of heights
    tx, ty = 96, 690
    s.rect(tx, ty - 14, 700, 118, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(tx + 8, ty, "TAG HEIGHTS AND PLANES", size=9.5, fill=ACCENT, weight="bold")
    rows = [("IDs", "Structure", "Z center", "Panel plane", "Facing"),
            ("1, 2 / 14, 15", "OUTFITTER (above chute)", "52.0", "X = 0 / 648 (wall)", "+X / -X"),
            ("3-5 / 16-18", "HEADWALL lane center", "12.0", "X = 39.0 / 609.0 (plumb)", "+X / -X"),
            ("6-13 / 19-26", "CRAG face pairs, +/-14.0 from the face centerline", "17.5",
             "the face plane", "outward")]
    colx = [tx + 8, tx + 112, tx + 384, tx + 452, tx + 620]
    for i, r in enumerate(rows):
        yy = ty + 18 + i * 15
        for cxx, cell in zip(colx, r):
            s.text(cxx, yy, cell, size=8.5, fill=INK if i else ACCENT,
                   weight="bold" if i == 0 else None)
        if i == 0:
                    s.line(tx + 6, yy + 4, tx + 694, yy + 4, stroke=RULE, sw=0.8)
    s.text(tx + 8, ty + 88,
           "CRAG tags sit at 17.5 in so a crowned CACHE CRATE standing in the BASE DEPOT (apex Z = 13.0) cannot occlude the 8.125-in target (Z 13.44-21.56), by 0.44 in.",
           size=8.5, fill=MUTED)
    s.text(tx + 8, ty + 100,
           "HEADWALL panels are plumb at X = 39.0 - at least 4.42 in behind plane P over the whole panel, so nothing enters the climbing volume.",
           size=8.5, fill=MUTED)

    # panel detail
    dx, dy, k = 850, 690, 9.0
    s.text(dx + 90, dy - 22, "PANEL DETAIL - 9.0 px/in", size=11, fill=ACCENT,
           weight="bold", anchor="middle")
    s.rect(dx, dy, k * TAG_PANEL, k * TAG_PANEL, fill="#F5F5F5", stroke="#666666", sw=1.2)
    o1 = (TAG_PANEL - TAG_TGT) / 2.0 * k
    s.rect(dx + o1, dy + o1, k * TAG_TGT, k * TAG_TGT, fill="#FFFFFF", stroke="#999999", sw=1.0)
    o2 = (TAG_PANEL - TAG_BODY) / 2.0 * k
    s.rect(dx + o2, dy + o2, k * TAG_BODY, k * TAG_BODY, fill="#111111", stroke="none", sw=0)
    s.dim_h(dx, dx + k * TAG_PANEL, dy + k * TAG_PANEL + 22, "9.00 panel",
            ext_from=dy + k * TAG_PANEL + 2, size=9)
    s.dim_h(dx + o1, dx + o1 + k * TAG_TGT, dy + k * TAG_PANEL + 48, "8.125 target",
            ext_from=dy + k * TAG_PANEL + 28, size=9, critical=True)
    s.dim_v(dy + o2, dy + o2 + k * TAG_BODY, dx - 20, "6.50 body", ext_from=dx - 2,
            size=9, critical=True)
    s.text(dx + 130, dy + 16, "Vision software wants the BODY size:", size=8.5, fill=INK)
    s.text(dx + 130, dy + 28, "6.5 in = 0.1651 m. Never enter 8.125 or 9.0.", size=8.5, fill=INK)
    s.text(dx + 130, dy + 44, "Panels plumb +/-1 deg, square to facing +/-1 deg.", size=8.5, fill=MUTED)
    s.text(dx + 130, dy + 56, "Field build tolerance +/-0.25 in on tag centers;", size=8.5, fill=MUTED)
    s.text(dx + 130, dy + 68, "the CAD model must match the JSON exactly.", size=8.5, fill=MUTED)
    s.text(dx + 130, dy + 84, "Matte, non-glare finish. Keep the white border clear.", size=8.5, fill=MUTED)

    s.titleblock(["Poses must match 04-vision/apriltag-field-layout.json exactly; the JSON is generated from this table and drives every simulation.",
                  NOTES[1], NOTES[2]])
    return s


# =====================================================================
# SHEET 2 - CRAG
# =====================================================================
def _notes(s, x, y, lines, w=420, title=None, size=8.5):
    yy = y
    if title:
        s.text(x, yy, title, size=9, fill=ACCENT, weight="bold")
        yy += 14
    for t in lines:
        s.text(x, yy, t, size=size, fill=INK if not t.startswith("(") else MUTED)
        yy += 12
    return yy


def sheet_crag():
    s = Sheet(1960, 1300, "DRAWING 2 OF 6 - CRAG (x2 PER FIELD)", 2, 6,
              "Blue CRAG shown - Red is the 180 deg rotation about field center - main views 3.2 px/in, details as noted")
    K = 3.2
    GY = 470.0
    hw = K * CRAG_S / 2
    sw_ = K * SPIRE_S / 2

    def z(v):
        return GY - K * v

    s.line(40, GY, 1560, GY, stroke=INK, sw=2.0)
    s.text(42, GY + 13, "carpet Z = 0", size=9, fill=MUTED)

    # ================= VIEW A - SHELF FACE =================
    ax = 250.0
    s.view_label(ax, 84, "VIEW A - SHELF FACE", "3.2 px/in", "faces the owning alliance wall")
    s.rect(ax - hw, z(BODY_H), 2 * hw, K * BODY_H, fill=CRAG_BODY, stroke=CRAG_EDGE, sw=2.0)
    s.rect(ax - sw_, z(SPIRE_TOP), 2 * sw_, K * (SPIRE_TOP - BODY_H), fill=CRAG_SPIRE,
           stroke=CRAG_EDGE, sw=2.0)
    s.rect(ax - sw_, z(SPIRE_TOP), 2 * sw_, K * (SPIRE_TOP - LANTERN_LO), fill=BEACON,
           stroke=CRAG_EDGE, sw=1.6)
    for sz in (SHELF1, SHELF2):
        s.rect(ax - hw, z(sz), 2 * hw, K * 0.75, fill=SHELF, stroke=CRAG_EDGE, sw=1.0)
        for f in (0, 15.5, 31.0, 46.5):
            s.rect(ax - hw + K * f, z(sz + FENCE_H), K * FENCE_W, K * FENCE_H,
                   fill=SHELF, stroke=CRAG_EDGE, sw=0.8)
    s.ellipse(ax, z(SUM_SOCK_Z), K * SOCK_OD / 2, K * SOCK_OD / 6, fill=SOCKET_L,
              stroke=BLUE_D, sw=1.8)
    for zz in (LOW_SOCK_Z, MID_SOCK_Z):
        for sgn in (-1, 1):
            cxp = ax + sgn * K * (CRAG_S / 2 + SOCK_STANDOFF)
            s.add('<g transform="rotate(%g %.2f %.2f)">' % (sgn * SOCK_TILT, cxp, z(zz)))
            s.rect(cxp - K * SOCK_OD / 2, z(zz), K * SOCK_OD, K * SOCK_TUBE,
                   fill=SOCKET, stroke=BLUE_D, sw=1.2)
            s.add('</g>')
            s.ellipse(cxp, z(zz), K * SOCK_OD / 2, K * SOCK_OD / 5, fill=SOCKET_L,
                      stroke=BLUE_D, sw=1.4, rot=sgn * SOCK_TILT)
    for tz in TIER_Z:
        w = sw_ + 5 if tz >= LANTERN_LO else hw + 5
        s.line(ax - w, z(tz), ax + w, z(tz), stroke="#E8443A", sw=1.6, dash="4 3")
    s.rect(ax - hw - K * DEPOT_WRAP, z(DEPOT_LIP), 2 * (hw + K * DEPOT_WRAP), K * DEPOT_LIP,
           fill=DEPOT, stroke=CRAG_EDGE, sw=1.2)
    for c in (-SOCK_LAT, SOCK_LAT):
        s.rect(ax + K * c - K * TAG_PANEL / 2, z(TAG_Z_CRAG + TAG_PANEL / 2),
               K * TAG_PANEL, K * TAG_PANEL, fill="#F5F5F5", stroke="#666666", sw=0.9)
        s.rect(ax + K * c - K * TAG_BODY / 2, z(TAG_Z_CRAG + TAG_BODY / 2),
               K * TAG_BODY, K * TAG_BODY, fill="#111111", stroke="none", sw=0)
    s.dim_h(ax - hw, ax + hw, GY + 52, "48.0", ext_from=GY + 4, critical=True)
    s.dim_h(ax, ax + K * SLOT_CTRS[2], z(SHELF2) - 30, "15.5", ext_from=z(SHELF2) - 8,
            size=9, critical=True)
    s.dim_h(ax - sw_, ax + sw_, z(SPIRE_TOP) - 18, "20.0", ext_from=z(SPIRE_TOP) - 2,
            size=9, critical=True)
    s.leader(ax, z(SUM_SOCK_Z), ax + hw + 26, z(SUM_SOCK_Z) - 22, "Summit Socket (D2)")
    s.leader(ax + sw_ * 0.4, z(BEACON_Z), ax + hw + 26, z(BEACON_Z) + 4, "SUMMIT BEACON lantern")
    s.leader(ax - hw - K * SOCK_STANDOFF, z(LOW_SOCK_Z), ax - hw - 40, z(LOW_SOCK_Z) - 26,
             "side-face sockets (D1)", anchor="end")
    _notes(s, 60, GY + 78, [
        "Shelf 1 top 24.0, Shelf 2 top 42.0; 3 slots of 14.0 with four 1.5 x 2.0 fences.",
        "Slot centers -15.5 / 0 / +15.5 from the face centerline.",
        "Summit Socket rim Z = 72.0, on the crag centerline, 8.0 out from THIS face.",
        "Tags 6 / 7 (Blue): ctr Z = 17.5, +/-14.0 from the face centerline.",
        "BASE DEPOT lip 4.0 runs this face and wraps 16.0 onto both socket faces.",
    ], title="VIEW A NOTES")

    # ================= VIEW B - SOCKET FACE =================
    bx = 700.0
    s.view_label(bx, 84, "VIEW B - SOCKET FACE", "3.2 px/in",
                 "-Y face shown; +Y is its mirror - shelf side LEFT, peg side RIGHT")
    s.rect(bx - hw, z(BODY_H), 2 * hw, K * BODY_H, fill=CRAG_BODY, stroke=CRAG_EDGE, sw=2.0)
    s.rect(bx - sw_, z(SPIRE_TOP), 2 * sw_, K * (SPIRE_TOP - BODY_H), fill=CRAG_SPIRE,
           stroke=CRAG_EDGE, sw=2.0)
    s.rect(bx - sw_, z(SPIRE_TOP), 2 * sw_, K * (SPIRE_TOP - LANTERN_LO), fill=BEACON,
           stroke=CRAG_EDGE, sw=1.6)
    for lat, zz in ((-SOCK_LAT, LOW_SOCK_Z), (SOCK_LAT, MID_SOCK_Z)):
        cxp = bx + K * lat
        s.rect(cxp - K * SOCK_OD / 2, z(zz), K * SOCK_OD, K * SOCK_TUBE * 0.87,
               fill=SOCKET, stroke=BLUE_D, sw=1.2)
        s.ellipse(cxp, z(zz), K * SOCK_OD / 2, K * SOCK_OD / 4, fill=SOCKET_L,
                  stroke=BLUE_D, sw=1.8)
    s.text(bx + K * (-SOCK_LAT), z(LOW_SOCK_Z) - 14, "Low Socket 30.0", size=8.5,
           fill=INK, anchor="middle")
    s.text(bx + K * SOCK_LAT, z(MID_SOCK_Z) - 14, "Mid Socket 54.0", size=8.5,
           fill=INK, anchor="middle")
    s.add('<g transform="rotate(-15 %.2f %.2f)">' % (bx - K * (CRAG_S / 2 + SOCK_STANDOFF), z(SUM_SOCK_Z)))
    s.rect(bx - K * (CRAG_S / 2 + SOCK_STANDOFF) - K * SOCK_OD / 2, z(SUM_SOCK_Z),
           K * SOCK_OD, K * SOCK_TUBE, fill=SOCKET, stroke=BLUE_D, sw=1.2)
    s.add('</g>')
    s.ellipse(bx - K * (CRAG_S / 2 + SOCK_STANDOFF), z(SUM_SOCK_Z), K * SOCK_OD / 2,
              K * SOCK_OD / 5, fill=SOCKET_L, stroke=BLUE_D, sw=1.6, rot=-15)
    for zz, lat in ((LOW_PEG_Z, CRAG_S / 2), (MID_PEG_Z, CRAG_S / 2), (HIGH_PEG_Z, SPIRE_S / 2)):
        x0 = bx + K * lat
        s.line(x0, z(zz), x0 + K * PEG_EXP * 0.7071, z(zz + PEG_EXP * 0.7071),
               stroke=RUNG, sw=K * PEG_OD, cap="round")
    lx = bx + 186
    ladder = ((SHELF1, "24.0  Shelf 1"), (LOW_SOCK_Z, "30.0  Low Socket / Low Peg"),
              (SHELF2, "42.0  Shelf 2"), (MID_SOCK_Z, "54.0  Mid Socket / Mid Peg"),
              (BODY_H, "60.0  tower top plate"), (SUM_SOCK_Z, "72.0  Summit Socket rim"),
              (HIGH_PEG_Z, "78.0  High Pegs / lantern base"),
              (BEACON_Z, "84.0  beacon luminous ctr"), (SPIRE_TOP, "90.0  spire top"))
    for v, lbl in ladder:
        s.line(bx + K * 26, z(v), lx - 6, z(v), stroke=DIM, sw=0.7)
        s.text(lx + 6, z(v) + 3.2, lbl, size=8.5, fill=DIM)
    s.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.1" marker-start="url(#arr)" marker-end="url(#arr)"/>'
          % (lx - 2, GY, lx - 2, z(SPIRE_TOP), DIM))
    s.dim_h(bx + K * (-SOCK_LAT), bx, GY + 34, "14.0", ext_from=GY + 4, size=9, critical=True)
    s.dim_h(bx, bx + K * SOCK_LAT, GY + 34, "14.0", ext_from=GY + 4, size=9, critical=True)
    _notes(s, 560, GY + 78, [
        "Socket rim centers sit +/-14.0 from the face centerline and 8.0 OUT",
        "from the face plane, measured normal to it (Detail D1).",
        "LOW is on the shelf-face side; MID is on the peg-face side, so each",
        "socket sits directly above one tag of the face pair.",
        "The Summit Socket, shown edge-on at the left, is on the SHELF FACE.",
    ], title="VIEW B NOTES")

    # ================= VIEW C - PEG FACE =================
    cx = 1150.0
    s.view_label(cx, 84, "VIEW C - PEG FACE", "3.2 px/in", "pegs project toward the viewer at 45 deg (D3)")
    s.rect(cx - hw, z(BODY_H), 2 * hw, K * BODY_H, fill=CRAG_BODY, stroke=CRAG_EDGE, sw=2.0)
    s.rect(cx - sw_, z(SPIRE_TOP), 2 * sw_, K * (SPIRE_TOP - BODY_H), fill=CRAG_SPIRE,
           stroke=CRAG_EDGE, sw=2.0)
    s.rect(cx - sw_, z(SPIRE_TOP), 2 * sw_, K * (SPIRE_TOP - LANTERN_LO), fill=BEACON,
           stroke=CRAG_EDGE, sw=1.6)
    s.line(cx, z(SPIRE_TOP), cx, GY, stroke=MUTED, sw=0.9, dash="12 4 3 4")
    for zz, lat in ((LOW_PEG_Z, PEG_LAT), (MID_PEG_Z, PEG_LAT), (HIGH_PEG_Z, HPEG_LAT)):
        for sgn in (-1, 1):
            s.circle(cx + sgn * K * lat, z(zz), K * PEG_OD / 2 + 1.4, fill="#777777",
                     stroke="#333333", sw=1.2)
    for tz in TIER_Z:
        w = sw_ + 5 if tz >= LANTERN_LO else hw + 5
        s.line(cx - w, z(tz), cx + w, z(tz), stroke="#E8443A", sw=1.6, dash="4 3")
        s.text(cx + w + 8, z(tz) + 3.2, "LED tier ring %g" % tz, size=8.5, fill=INK)
    for c in (-SOCK_LAT, SOCK_LAT):
        s.rect(cx + K * c - K * TAG_PANEL / 2, z(TAG_Z_CRAG + TAG_PANEL / 2),
               K * TAG_PANEL, K * TAG_PANEL, fill="#F5F5F5", stroke="#666666", sw=0.9)
        s.rect(cx + K * c - K * TAG_BODY / 2, z(TAG_Z_CRAG + TAG_BODY / 2),
               K * TAG_BODY, K * TAG_BODY, fill="#111111", stroke="none", sw=0)
    s.dim_h(cx, cx + K * PEG_LAT, z(LOW_PEG_Z) - 24, "14.0", ext_from=z(LOW_PEG_Z) - 6,
            size=9, critical=True)
    s.dim_h(cx, cx + K * HPEG_LAT, z(HIGH_PEG_Z) - 24, "7.0", ext_from=z(HIGH_PEG_Z) - 6,
            size=9, critical=True)
    s.dim_h(cx - hw, cx + hw, GY + 52, "48.0", ext_from=GY + 4, critical=True)
    _notes(s, 1010, GY + 78, [
        "Low and Mid Peg roots +/-14.0 from the face centerline, Z 30.0 and 54.0.",
        "High Peg roots +/-7.0 from the spire centerline (14.0 apart), Z 78.0.",
        "All pegs OD 1.5, 45 deg up from the face, 10.0 exposed, tip R0.75.",
        "Tags 12 / 13 (Blue): ctr Z = 17.5, +/-14.0.",
        "Tier rings latch on CAMP establishment; the lantern is the SUMMIT BEACON.",
    ], title="VIEW C NOTES")

    # ================= VIEW D - TOP (plan) =================
    dx, dy = 1660.0, 250.0
    s.view_label(dx, 84, "VIEW D - TOP (PLAN)", "3.2 px/in",
                 "shelf face LEFT, peg face RIGHT")
    h = K * CRAG_S / 2
    s.rect(dx - h - K * DEPOT_CH, dy - h - K * DEPOT_WRAP, K * DEPOT_CH,
           K * (CRAG_S + 2 * DEPOT_WRAP), fill=DEPOT, stroke=CRAG_EDGE, sw=1.3)
    for sgn in (-1, 1):
        s.rect(dx - h, dy + (sgn * h if sgn > 0 else -h - K * DEPOT_WRAP),
               K * DEPOT_WRAP, K * DEPOT_WRAP, fill=DEPOT, stroke=CRAG_EDGE, sw=1.3)
    s.rect(dx - h - K * SHELF_DEPTH, dy - h, K * SHELF_DEPTH, K * CRAG_S,
           fill="none", stroke=SHELF, sw=1.3, dash="6 3")
    s.rect(dx - h, dy - h, 2 * h, 2 * h, fill=CRAG_BODY, stroke=CRAG_EDGE, sw=2.0)
    s.rect(dx - K * SPIRE_S / 2, dy - K * SPIRE_S / 2, K * SPIRE_S, K * SPIRE_S,
           fill=CRAG_SPIRE, stroke=CRAG_EDGE, sw=1.6)
    for sgn in (-1, 1):
        for lat, nm in ((-SOCK_LAT, "LOW"), (SOCK_LAT, "MID")):
            pxx = dx + K * lat
            pyy = dy + sgn * (h + K * SOCK_STANDOFF)
            s.circle(pxx, pyy, K * SOCK_OD / 2, fill=SOCKET_L, stroke=BLUE_D, sw=1.5)
            s.text(pxx, pyy + (15 if sgn > 0 else -9), nm, size=8, fill=INK, anchor="middle")
    s.circle(dx - h - K * SOCK_STANDOFF, dy, K * SOCK_OD / 2, fill=SOCKET_L, stroke=BLUE_D, sw=1.8)
    s.text(dx - h - K * SOCK_STANDOFF, dy - 14, "SUMMIT", size=8, fill=INK, anchor="middle")
    for sgn in (-1, 1):
        s.line(dx + h, dy + sgn * K * PEG_LAT, dx + h + K * PEG_EXP * 0.7071,
               dy + sgn * K * PEG_LAT, stroke="#666666", sw=4, cap="round")
        s.line(dx + K * SPIRE_S / 2, dy + sgn * K * HPEG_LAT,
               dx + K * SPIRE_S / 2 + K * PEG_EXP * 0.7071, dy + sgn * K * HPEG_LAT,
               stroke="#666666", sw=4, cap="round", dash="4 3")
    s.dim_h(dx - h, dx + h, dy + h + 76, "48.0", ext_from=dy + h + 6, critical=True)
    s.dim_h(dx - h - K * DEPOT_CH, dx - h, dy + h + 46, "16.0", ext_from=dy + h + 6,
            size=9, critical=True)
    s.dim_v(dy - h - K * SOCK_STANDOFF, dy - h, dx + K * SOCK_LAT + 40, "8.0",
            ext_from=dx + K * SOCK_LAT + 8, size=9, critical=True, side="right")
    s.dim_v(dy - h, dy + h, dx + h + 116, "48.0", ext_from=dx + h + 60, critical=True, side="right")
    _notes(s, 1500, GY + 78, [
        "BASE DEPOT: channel 16.0 from the shelf face, wrapping 16.0 onto",
        "each socket face. Lip 4.0 tall, top edge R0.25 (Detail D4).",
        "Shelves overhang 14.0 and span only the 48-in face, so the outer 2.0 of",
        "the shelf-face leg and both 16 x 16 corner SQUARES are open from above.",
        "The two corner ARMS are overhung by their Low Socket tubes: push, do not drop.",
        "Dashed rectangle = shelves above.",
    ], title="VIEW D NOTES")

    # ===================== ROW 2 DETAILS =====================
    s.line(40, 620, 1920, 620, stroke=RULE, sw=1.0)
    E = 9.0

    # ---- D1 socket section ----
    d1x, d1y = 250.0, 806.0
    s.view_label(d1x, 664, "D1 - SOCKET SECTION", "9.0 px/in", "typical of all four side sockets")
    s.line(d1x - 120, d1y - 90, d1x - 120, d1y + 190, stroke=CRAG_EDGE, sw=3)
    s.text(d1x - 128, d1y + 60, "CRAG face plane", size=9, fill=INK, anchor="middle", rot=-90)
    rimx, rimy = d1x - 120 + E * SOCK_STANDOFF, d1y
    s.add('<g transform="rotate(%g %.2f %.2f)">' % (SOCK_TILT, rimx, rimy))
    s.rect(rimx - E * SOCK_OD / 2, rimy, E * SOCK_OD, E * SOCK_TUBE, fill="none",
           stroke=BLUE_D, sw=2.2)
    s.line(rimx - E * SOCK_OD / 2, rimy + E * SOCK_TUBE, rimx + E * SOCK_OD / 2,
           rimy + E * SOCK_TUBE, stroke=BLUE_D, sw=4)
    s.rect(rimx - E * CELL_D / 2, rimy + E * SOCK_TUBE - E * CELL_L, E * CELL_D, E * CELL_L,
           fill="none", stroke=GHOST, sw=2.0, rx=E * 1.5, dash="5 3")
    s.add('</g>')
    s.ellipse(rimx, rimy, E * SOCK_OD / 2, E * SOCK_OD / 6, fill="none", stroke=BLUE_D,
              sw=2.2, rot=SOCK_TILT)
    s.line(rimx, rimy - 70, rimx, rimy + 30, stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.angle(rimx, rimy, 44, -90, -60, "30 deg", lx=rimx + 62, ly=rimy - 50)
    s.dim_h(d1x - 120, rimx, rimy - 88, "8.0", ext_from=rimy - 70, size=9.5, critical=True)
    s.ellipse(rimx, rimy, E * SOCK_ID / 2, E * SOCK_ID / 6, fill="none", stroke=BLUE_D,
              sw=1.2, rot=SOCK_TILT)
    s.dim_a((rimx - E * SOCK_ID / 2 * math.cos(math.radians(SOCK_TILT)),
             rimy + E * SOCK_ID / 2 * math.sin(math.radians(SOCK_TILT))),
            (rimx + E * SOCK_ID / 2 * math.cos(math.radians(SOCK_TILT)),
             rimy - E * SOCK_ID / 2 * math.sin(math.radians(SOCK_TILT))),
            "ID 6.50 +/- 0.125", off=-30, critical=True, size=10)
    _notes(s, 60, 1024, [
        "Rim ctr Z = 30.0 (Low) / 54.0 (Mid). Standoff 8.0 normal to the face.",
        "Tube 7.0 along the axis, closed bottom, wall 0.09 (ref).",
        "Tilt 30 deg from vertical, tilting OUTWARD, open end up.",
        "Bottom center lands 4.50 out from the face; inboard edge 1.61 out,",
        "so nothing enters the tower and no relief pocket is needed.",
        "A seated 14.0 O2 CELL protrudes 7.0 along the axis and stands",
        "4.39 above the rim's uphill lip - the SCORED call is a glance.",
        "The attachment lives in the wedge under the tube and may not break",
        "the rim plane (geometry otherwise free, ref).",
    ], title="D1 NOTES", w=400)

    # ---- D2 summit socket ----
    d2x, d2y = 700.0, 806.0
    s.view_label(d2x, 664, "D2 - SUMMIT SOCKET", "9.0 px/in", "on the SHELF FACE, on the crag centerline")
    s.line(d2x + 90, d2y - 90, d2x + 90, d2y + 190, stroke=CRAG_EDGE, sw=3)
    s.text(d2x + 100, d2y + 170, "SHELF FACE plane", size=9, fill=INK)
    rx2, ry2 = d2x + 90 - E * SOCK_STANDOFF, d2y
    s.add('<g transform="rotate(%g %.2f %.2f)">' % (-SUM_TILT, rx2, ry2))
    s.rect(rx2 - E * SOCK_OD / 2, ry2, E * SOCK_OD, E * SOCK_TUBE, fill=SOCKET,
           stroke=BLUE_D, sw=2.0)
    s.rect(rx2 - E * CELL_D / 2, ry2 + E * SOCK_TUBE - E * CELL_L, E * CELL_D, E * CELL_L,
           fill="none", stroke=GHOST, sw=2.0, rx=E * 1.5, dash="5 3")
    s.add('</g>')
    s.ellipse(rx2, ry2, E * SOCK_OD / 2, E * SOCK_OD / 6, fill=SOCKET_L, stroke=BLUE_D,
              sw=2.0, rot=-SUM_TILT)
    s.line(rx2, ry2 - 70, ry2 * 0 + rx2, ry2 + 30, stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.angle(rx2, ry2, 44, -105, -90, "15 deg", lx=rx2 - 56, ly=ry2 - 52)
    s.dim_h(rx2, d2x + 90, ry2 - 88, "8.0", ext_from=ry2 - 70, size=9.5, critical=True)
    s.rect(d2x + 90, d2y + 150, 130, 24, fill=CRAG_BODY, stroke=CRAG_EDGE, sw=1.6)
    s.text(d2x + 226, d2y + 166, "tower top plate Z = 60.0", size=8.5, fill=INK)
    _notes(s, 520, 1024, [
        "Rim ctr Z = 72.0, on the crag centerline, 8.0 OUT from the SHELF FACE.",
        "Tube 7.0 along the axis at 15 deg from vertical, tilting outward.",
        "Bottom center 6.19 out from the face at Z = 65.24; inboard edge 2.96",
        "out - free air outboard of the tower, no pocket required.",
        "A crowned CRATE on Shelf 2 tops out at Z = 55.0; the tube bottom is Z = 64.4 - 9.4 clear.",
        "The MAST stands over Shelf 2's CENTRE slot from Z = 60: only 5.0 overhead, so that",
        "slot is loaded from the front. The two outer slots stay open to the sky.",
        "A seated CELL's apex reaches Z = 78.76, leaning toward the owning",
        "alliance's driver stations.",
        "THERE IS NO SPIRE RECESS - the spire is a clean 20 x 20 prism.",
        "Reach: a ROBOT at the DEPOT lip has its FRAME PERIMETER 19.75 from",
        "the face, so the rim is 11.75 of extension - inside the 18 in limit.",
    ], title="D2 NOTES", w=400)

    # ---- D3 peg + coil ----
    d3x, d3y = 1150.0, 830.0
    F = 10.0
    s.view_label(d3x, 664, "D3 - PEG AND COIL REST POSE", "10.0 px/in",
                 "the geometry every hook and spear is designed against")
    s.line(d3x - 130, d3y - 120, d3x - 130, d3y + 110, stroke=CRAG_EDGE, sw=3)
    s.text(d3x - 138, d3y + 100, "face", size=9, fill=INK, anchor="end")
    root = (d3x - 130, d3y + 20)
    tip = (root[0] + F * PEG_EXP * 0.7071, root[1] - F * PEG_EXP * 0.7071)
    s.add('<g transform="rotate(-45 %.2f %.2f)">' % root)
    s.rect(root[0], root[1] - F * PEG_OD / 2, F * PEG_EXP, F * PEG_OD, fill="#999999",
           stroke="#333333", sw=1.6, rx=F * PEG_OD / 2)
    s.add('</g>')
    s.line(root[0], root[1], root[0] + 96, root[1], stroke=MUTED, sw=0.9, dash="6 3")
    s.angle(root[0], root[1], 58, 0, -45, "45 deg", lx=root[0] + 80, ly=root[1] - 26)
    s.dim_a(root, tip, "10.0 exposed", off=-24, critical=True, size=9.5)
    s.circle(root[0] + 12, root[1] - 10, F * COIL_OD / 2, fill="none", stroke=GHOST, sw=2.2)
    s.circle(root[0] + 12, root[1] - 10, F * COIL_ID / 2, fill="none", stroke=GHOST, sw=1.4)
    s.text(root[0] + 12, root[1] - 10 - F * COIL_OD / 2 - 8, "REST POSE A", size=8.5,
           fill=GHOST, anchor="middle")
    s.add('<g transform="rotate(-45 %.2f %.2f)">' % (root[0] + 74, root[1] - 74))
    s.ellipse(root[0] + 74, root[1] - 74, F * COIL_TUBE / 2, F * COIL_OD / 2, fill="none",
              stroke=MUTED, sw=1.4)
    s.add('</g>')
    s.text(root[0] + 108, root[1] - 96, "REST POSE B", size=8.5, fill=MUTED)
    _notes(s, 1010, 1024, [
        "Peg OD 1.5 (CRITICAL), 45 deg up from the face, 10.0 exposed, tip R0.75.",
        "Root heights Z = 30 / 54 / 78; roots +/-14.0 (low, mid) and +/-7.0 (high).",
        "POSE A (settled): the COIL hangs near-vertical in a plane parallel to",
        "the face and wedges on the peg. A 5.0 hole over a 1.5 peg permits at",
        "most about 48 deg (47.9) of tilt (2.5 tan t + 1.5 / cos t <= 5.0); a vertical",
        "hang needs 45 deg, so a SCORED COIL is captured, not balanced.",
        "The coil center rests about 1 in above the peg root, its inner face",
        "about 1.25 in outboard of the crag face.",
        "POSE B (as dropped, dashed): perpendicular to the peg; it settles to A.",
    ], title="D3 NOTES", w=400)

    # ---- D4 shelf + depot ----
    d4x, d4y = 1700.0, 730.0
    G = 6.2
    s.view_label(d4x - 120, 664, "D4 - SHELF AND DEPOT SECTION", "6.2 px/in",
                 "section normal to the SHELF FACE")
    base = d4y + 300

    def zz4(v):
        return base - G * v
    s.line(d4x - 250, base, d4x + 40, base, stroke=INK, sw=2.0)
    s.line(d4x, zz4(0), d4x, zz4(50), stroke=CRAG_EDGE, sw=3)
    s.text(d4x + 6, zz4(48), "SHELF FACE", size=8.5, fill=INK)
    s.text(d4x - G * SHELF_DEPTH - 6, zz4(SHELF1) + 3, "Shelf 1", size=8.5, fill=INK, anchor="end")
    s.text(d4x - G * SHELF_DEPTH - 6, zz4(SHELF2) + 3, "Shelf 2", size=8.5, fill=INK, anchor="end")
    s.text(d4x - G * 7, zz4(SHELF1 + CRATE_S) - 6, "CRATE on Shelf 1", size=8, fill=GHOST, anchor="middle")
    s.text(d4x - G * 7, zz4(CRATE_S) - 6, "CRATE in the DEPOT", size=8, fill=CRATE_D, anchor="middle")
    for szv in (SHELF1, SHELF2):
        s.rect(d4x - G * SHELF_DEPTH, zz4(szv), G * SHELF_DEPTH, G * 0.75,
               fill=SHELF, stroke=CRAG_EDGE, sw=1.4)
        s.rect(d4x - G * SHELF_DEPTH, zz4(szv + FENCE_H), G * FENCE_W, G * FENCE_H,
               fill=SHELF, stroke=CRAG_EDGE, sw=1.0)
        s.path("M %.2f %.2f L %.2f %.2f L %.2f %.2f Z" %
               (d4x, zz4(szv), d4x - G * 6, zz4(szv), d4x, zz4(szv - 6)),
               fill="#D9CDB2", stroke=CRAG_EDGE, sw=0.9)
    s.rect(d4x - G * (SHELF_DEPTH - 1), zz4(SHELF1 + CRATE_S), G * CRATE_S, G * CRATE_S,
           fill="none", stroke=GHOST, sw=1.8, rx=G * 0.8, dash="5 3")
    s.rect(d4x - G * (DEPOT_CH + LIP_THK), zz4(DEPOT_LIP), G * LIP_THK, G * DEPOT_LIP,
           fill=DEPOT, stroke=CRAG_EDGE, sw=1.3)
    s.rect(d4x - G * DEPOT_CH, zz4(0.25), G * DEPOT_CH, G * 0.25, fill=DEPOT,
           stroke=CRAG_EDGE, sw=1.0)
    s.rect(d4x - G * (DEPOT_CH - 1), zz4(0.25 + 13.0), G * CRATE_S, G * 13.0,
           fill=CRATE, stroke=CRATE_D, sw=1.4, rx=G * 0.8, op=0.55)
    s.dim_v(zz4(0.25 + 13.0), zz4(0.25), d4x - G * (DEPOT_CH - 1) - 22, "13.0 crowned",
            ext_from=d4x - G * (DEPOT_CH - 1) - 4, size=8.5)
    s.dim_h(d4x - G * SHELF_DEPTH, d4x, zz4(SHELF2) - 24, "14.0", ext_from=zz4(SHELF2) - 6,
            size=9, critical=True)
    s.dim_h(d4x - G * DEPOT_CH, d4x, base + 40, "16.0", ext_from=base + 4, size=9.5, critical=True)
    s.dim_v(zz4(DEPOT_LIP), base, d4x - G * (DEPOT_CH + LIP_THK) - 24, "4.0",
            ext_from=d4x - G * (DEPOT_CH + LIP_THK) - 4, size=9, critical=True)
    s.dim_v(zz4(SHELF1), base, d4x + 40, "24.0", ext_from=d4x + 4, size=9, critical=True, side="right")
    s.dim_v(zz4(SHELF2), base, d4x + 78, "42.0", ext_from=d4x + 4, size=9, critical=True, side="right")
    _notes(s, 1500, 1090, [
        "Lip 4.0 tall, top edge R0.25; lip thickness 0.75 (ref);",
        "tray floor 0.25 with a 45 deg entry chamfer (ref).",
        "The floor top is at Z = 0.25, so a crowned CRATE apexes at 13.25 -",
        "only 0.19 below the CRAG tag target at 13.44. See VISION-GUIDE 1.3.",
        "A CRATE stands proud of the lip and is SCORED so long as the tray",
        "floor alone supports it.",
        "Robot standoff: bumper face 16.75 from the crag face,",
        "FRAME PERIMETER 19.75; a shelf slot center is 12.75 of extension.",
    ], title="D4 NOTES", w=400)

    s.titleblock(NOTES)
    return s


# =====================================================================
# SHEET 3 - HEADWALL
# =====================================================================
def sheet_headwall():
    s = Sheet(1720, 1060, "DRAWING 3 OF 6 - HEADWALL (x2 PER FIELD)", 3, 6,
              "Blue HEADWALL shown - plane P crosses the carpet at X = 48 (Red mirrors at X = 600) - rung heights are VERTICAL, carpet to rung TOP")
    K = 3.4
    GY = 600.0

    def z(v):
        return GY - K * v

    def stag(lane_i, rung_i):
        # Stagger alternates by RUNG, never by lane: alternating the sign per
        # lane put adjacent lanes' rungs 24 in apart centre-to-centre, closer
        # than two hanging ROBOTS are wide.
        return (-1, 1, -1)[rung_i] * RUNG_STAG

    # ---------- FRONT ELEVATION ----------
    fx0 = 90.0

    def fy_(Y):
        return fx0 + K * (Y - 90.0)

    s.view_label(fx0 + K * HW_W / 2, 92, "FRONT ELEVATION", "3.4 px/in",
                 "viewed from the FIELD, projected onto the vertical plane")
    s.line(50, GY, fx0 + K * HW_W + 60, GY, stroke=INK, sw=2.0)
    s.text(52, GY + 14, "carpet Z = 0", size=9, fill=MUTED)
    s.rect(fx0, z(TRUSS_TOP), K * HW_W, K * TRUSS_TOP, fill="#EFE7D8", stroke=TRUSS_D, sw=2.4)
    for yb in (138.0, 186.0):
        s.line(fy_(yb), z(TRUSS_TOP), fy_(yb), GY, stroke=TRUSS_D, sw=1.6, dash="8 5")
    for i, ly in enumerate(LANE_Y):
        s.text(fy_(ly), z(TRUSS_TOP) - 10, "LANE %d (Y %d-%d)" % (i + 1, ly - 24, ly + 24),
               size=9, fill=INK, anchor="middle")
        s.line(fy_(ly), z(TRUSS_TOP), fy_(ly), z(4), stroke=MUTED, sw=0.9, dash="12 4 3 4")
        s.rect(fy_(ly) - K * TAG_PANEL / 2, z(TAG_Z_HW + TAG_PANEL / 2), K * TAG_PANEL,
               K * TAG_PANEL, fill="#F5F5F5", stroke="#666666", sw=1.0)
        s.rect(fy_(ly) - K * TAG_BODY / 2, z(TAG_Z_HW + TAG_BODY / 2), K * TAG_BODY,
               K * TAG_BODY, fill="#111111", stroke="none", sw=0)
    for li, ly in enumerate(LANE_Y):
        for ri, top in enumerate(RUNG_TOP):
            c = ly + stag(li, ri)
            s.line(fy_(c - RUNG_L / 2), z(top - RUNG_OD / 2), fy_(c + RUNG_L / 2),
                   z(top - RUNG_OD / 2), stroke="#444444", sw=K * RUNG_OD, cap="round")
    for lbl, top in (("LEDGE RUNG - top 30.0", 30.0), ("CAMP RUNG - top 54.0", 54.0),
                     ("SUMMIT RUNG - top 78.0", 78.0)):
        s.text(fx0 + K * HW_W + 12, z(top) + 4, lbl, size=9.5, fill=INK)
    l2 = LANE_Y[1]
    s.dim_h(fy_(l2), fy_(l2 + stag(1, 0)), z(30) + 34, "12.0", ext_from=z(30) + 6,
            size=9, critical=True)
    s.dim_h(fy_(l2 + stag(1, 1)), fy_(l2), z(54) + 34, "12.0", ext_from=z(54) + 6,
            size=9, critical=True)
    s.dim_h(fy_(LANE_Y[0] + stag(0, 0) - RUNG_L / 2), fy_(LANE_Y[0] + stag(0, 0) + RUNG_L / 2),
            z(78) + 32, "20.0 rung length", ext_from=z(78) + 8, size=9, critical=True)
    s.dim_h(fx0, fx0 + K * HW_W, GY + 46, "144.0 (three 48.0-in lanes)", ext_from=GY + 4,
            critical=True)
    s.dim_h(fx0, fy_(138.0), GY + 76, "48.0", ext_from=GY + 4, size=9, critical=True)
    lx = 66
    for v, lbl in ((30.0, "30.0"), (54.0, "54.0"), (78.0, "78.0")):
        s.line(fx0 - 6, z(v), lx + 6, z(v), stroke=DIM, sw=0.7)
        s.text(lx - 2, z(v) + 3.5, lbl, size=9, fill=DIM, anchor="end")
    s.line(fx0 - 6, z(84.0), lx + 6, z(84.0), stroke=DIM, sw=0.7)
    s.text(fx0 + K * HW_W + 12, z(84.0) + 4, "84.0 truss top (ref)", size=9, fill=DIM)
    s.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.1" marker-start="url(#arr)" marker-end="url(#arr)"/>'
          % (lx + 10, GY, lx + 10, z(TRUSS_TOP), DIM))
    s.text(fx0 + K * HW_W / 2, GY + 104,
           "Stagger is the same in every lane: LEDGE -12.0, CAMP +12.0, SUMMIT -12.0 from the lane centerline,",
           size=9, fill=INK, anchor="middle")
    s.text(fx0 + K * HW_W / 2, GY + 118,
           "in every lane - the sign alternates by rung, never by lane. Red = 180 deg rotation about (324, 162).",
           size=9, fill=INK, anchor="middle")
    s.text(fx0 + K * HW_W / 2, GY + 134,
           "A 20.0-in rung at +/-12.0 leaves NO lateral position that engages two successive rungs: LEDGE spans -22 to -2, CAMP spans +2 to +22.",
           size=9, fill=DIM, anchor="middle")

    # ---------- SIDE PROFILE ----------
    px0 = 660.0

    def sx(X):
        return px0 + K * (100.0 - X)

    s.view_label(sx(50), 92, "SIDE PROFILE - PLANE P", "3.4 px/in",
                 "field LEFT, alliance wall RIGHT")
    s.line(sx(110), GY, sx(-4), GY, stroke=INK, sw=2.0)
    s.rect(sx(0), z(78.0), 10, K * 78.0, fill=WALL, stroke=WALL_D, sw=1.6)
    s.text(sx(0) + 22, z(40), "ALLIANCE WALL (78 ref)", size=9, fill=WALL_D, rot=-90)
    s.line(sx(HW_X), GY, sx(HW_X - TRUSS_TOP * T15), z(TRUSS_TOP), stroke=BLUE_D, sw=2.4)
    s.text(sx(44), z(50), "PLANE P", size=10, fill=BLUE_D, rot=-72)
    s.line(sx(HW_X), GY, sx(HW_X), z(TRUSS_TOP + 4), stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.angle(sx(HW_X), GY, 74, -90, -68, "15 deg from vertical", lx=sx(HW_X) - 110, ly=z(14))
    s.line(sx(HW_X) - 68, z(14) - 4, sx(HW_X) + 10, z(21), stroke=DIM, sw=0.7)
    s.line(sx(truss_face_x(0)), GY, sx(truss_face_x(TRUSS_TOP)), z(TRUSS_TOP),
           stroke=TRUSS, sw=5, cap="round")
    s.text(sx(truss_face_x(62)) + 10, z(64), "truss structure, all >= 4.0 behind P", size=8.5, fill=TRUSS_D)
    for lbl, top in (("LEDGE", 30.0), ("CAMP", 54.0), ("SUMMIT", 78.0)):
        cxx = rung_center_x(top)
        s.circle(sx(cxx), z(top - RUNG_OD / 2), 5.5, fill="#444444", stroke="#222222", sw=1.0)
        s.text(sx(cxx) - 12, z(top - RUNG_OD / 2) + 4, lbl, size=9, fill=INK, anchor="end")
    s.rect(sx(TAG_HW_X) - 3, z(TAG_Z_HW + TAG_PANEL / 2), 6, K * TAG_PANEL,
           fill="#111111", stroke="#666666", sw=0.8)
    s.leader(sx(TAG_HW_X), z(TAG_Z_HW), sx(TAG_HW_X) - 150, z(TAG_Z_HW) - 44,
             "tag panel PLUMB, face plane X = 39.0, ctr Z = 12.0", anchor="start")
    s.text(sx(TAG_HW_X) - 146, z(TAG_Z_HW) - 30, "4.42 in behind P at the panel top edge",
           size=8.5, fill=INK)
    s.rect(sx(HW_X), GY - 7, K * HW_X, 7, fill=BLUE, stroke=BLUE_D, sw=0.8, op=0.55)
    s.text(sx(24), GY - 12, "BASECAMP / HEADWALL ZONE (X 0-48)", size=8.5, fill=BLUE_D, anchor="middle")
    s.dim_h(sx(HW_X), sx(0), GY + 46, "48.0", ext_from=GY + 4, critical=True)
    s.line(sx(0), z(42), sx(32.6), z(42), stroke=GHOST, sw=1.6, dash="6 4")
    s.text(sx(32.6) - 8, z(42) - 7, "42-in STARTING CONFIGURATION fits up to X = 32.6",
           size=8.5, fill=GHOST, anchor="end")

    # ---------- TOP VIEW ----------
    tx0, ty0 = 1130.0, 150.0
    T = 2.2
    s.view_label(tx0 + 66, 92, "TOP VIEW (PLAN)", "2.2 px/in", "field LEFT, wall RIGHT")

    def tx(X):
        return tx0 + T * (60.0 - X)

    def ty(Y):
        return ty0 + T * (Y - 90.0)

    s.rect(tx(0) - 6, ty(90), 6, T * HW_W, fill=WALL, stroke=WALL_D, sw=1.2)
    s.line(tx(HW_X), ty(90), tx(HW_X), ty(234), stroke=BLUE_D, sw=2.0)
    s.text(tx(HW_X) - 4, ty(90) - 6, "P carpet line X = 48", size=8.5, fill=BLUE_D, anchor="end")
    for yb in (90.0, 138.0, 186.0, 234.0):
        s.line(tx(60), ty(yb), tx(0), ty(yb), stroke=TRUSS_D, sw=1.2,
               dash=None if yb in (90.0, 234.0) else "6 4")
    for li, ly in enumerate(LANE_Y):
        for ri, top in enumerate(RUNG_TOP):
            c = ly + stag(li, ri)
            cxx = rung_center_x(top)
            s.line(tx(cxx), ty(c - RUNG_L / 2), tx(cxx), ty(c + RUNG_L / 2),
                   stroke="#444444", sw=3.4, cap="round", op=0.9)
    for ri, (lbl, top) in enumerate((("LEDGE", 30.0), ("CAMP", 54.0), ("SUMMIT", 78.0))):
        lyy = ty(234) + 16 + ri * 11
        s.line(tx(rung_center_x(top)), ty(234) + 4, tx(rung_center_x(top)), lyy - 7,
               stroke=MUTED, sw=0.6)
        s.text(tx(rung_center_x(top)), lyy, lbl, size=8, fill=INK, anchor="middle")
    s.dim_v(ty(90), ty(234), tx(0) - 30, "144.0", ext_from=tx(0) - 8, side="right", size=9)
    s.text(tx0 + 66, ty(234) + 62, "rungs step toward the wall", size=8.5, fill=MUTED, anchor="middle")
    s.text(tx0 + 66, ty(234) + 74, "with height (15 deg lean)", size=8.5, fill=MUTED, anchor="middle")

    # ---------- RUNG DETAIL ----------
    rx0, ry0 = 1400.0, 190.0
    R = 9.0
    s.view_label(rx0 + 100, 96, "RUNG DETAIL", "9.0 px/in", "section normal to plane P")
    s.line(rx0 + 60, ry0, rx0 + 60, ry0 + 190, stroke=BLUE_D, sw=2.0, dash="10 4")
    s.text(rx0 + 50, ry0 + 95, "plane P", size=9, fill=BLUE_D, anchor="middle", rot=-90)
    s.circle(rx0 + 60, ry0 + 90, R * RUNG_OD / 2, fill="#444444", stroke="#222222", sw=1.2)
    s.dim_h(rx0 + 60 - R * RUNG_OD / 2, rx0 + 60 + R * RUNG_OD / 2, ry0 + 58,
            "OD 1.5", ext_from=ry0 + 80, size=9, critical=True)
    s.rect(rx0 + 60 + R * TRUSS_CLR, ry0, R * 2.0, 190, fill="#EFE7D8", stroke=TRUSS_D, sw=1.6)
    s.text(rx0 + 60 + R * TRUSS_CLR + 8, ry0 - 6, "truss chord 2 x 2 (ref)", size=8.5, fill=INK)
    s.dim_h(rx0 + 60, rx0 + 60 + R * TRUSS_CLR, ry0 + 152, "4.0", ext_from=ry0 + 132,
            size=9, critical=True)
    s.path("M %.1f %.1f q 34 -2 34 28 q 0 24 -24 24" % (rx0 + 34, ry0 + 60),
           stroke=GHOST, sw=2.0, dash="5 3")
    s.text(rx0 + 30, ry0 + 52, "climber hook wrap", size=8.5, fill=GHOST, anchor="end")
    s.text(rx0 + 100, ry0 + 188, "structure >= 4.0 behind P except the end brackets - clear wrap over the middle 16.0 of 20.0",
           size=8.5, fill=INK, anchor="middle")

    # ---------- TABLES ----------
    bx, by = 90, 762
    s.rect(bx, by - 16, 760, 196, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(bx + 8, by, "DERIVED (do NOT drive these - dimension plane P and the vertical heights; let CAD compute)",
           size=9.5, fill=ACCENT, weight="bold")
    hdr = ("Rung", "Top Z", "Ctr Z", "Ctr X", "Lane-1 Y span", "Lane-2 Y span", "Lane-3 Y span")
    colx = [bx + 8, bx + 84, bx + 140, bx + 196, bx + 268, bx + 400, bx + 532]
    for cxx, cell in zip(colx, hdr):
        s.text(cxx, by + 20, cell, size=8.5, fill=ACCENT, weight="bold")
    s.line(bx + 6, by + 25, bx + 752, by + 25, stroke=RULE, sw=0.8)
    for ri, (nm, top) in enumerate((("LEDGE", 30.0), ("CAMP", 54.0), ("SUMMIT", 78.0))):
        zc = top - RUNG_OD / 2
        row = [nm, "%.1f" % top, "%.2f" % zc, "%.2f" % rung_center_x(top)]
        for li, ly in enumerate(LANE_Y):
            c = ly + stag(li, ri)
            row.append("%.0f - %.0f" % (c - RUNG_L / 2, c + RUNG_L / 2))
        for cxx, cell in zip(colx, row):
            s.text(cxx, by + 42 + ri * 15, cell, size=8.5, fill=INK)
    s.text(bx + 8, by + 104, "Rung ctr Z = top - 0.75. Blue rung ctr X = 48 - Z x tan 15. Setback between successive rungs = 24 x tan 15 = 6.43 in.",
           size=8.5, fill=MUTED)
    s.text(bx + 8, by + 117, "Every rung sits at least 2.0 in inside its lane boundary; adjacent lanes are 48.0 apart centre-to-centre, 28.0 end to end.",
           size=8.5, fill=MUTED)
    s.text(bx + 8, by + 136, "BASECAMP CLEAR VOLUME:   H(X) = 3.7321 x (43.859 - X) inches",
           size=9, fill=ACCENT, weight="bold")
    cells = [(0, 163.7), (12, 118.9), (24, 74.1), (32.6, 42.0), (36, 29.3), (40, 14.4), (43.86, 0.0)]
    s.text(bx + 8, by + 152, "X (in)", size=8.5, fill=ACCENT, weight="bold")
    s.text(bx + 8, by + 165, "H (in)", size=8.5, fill=ACCENT, weight="bold")
    for i, (xv, hv) in enumerate(cells):
        s.text(bx + 78 + i * 74, by + 152, "%g" % xv, size=8.5, fill=INK)
        s.text(bx + 78 + i * 74, by + 165, "%.1f" % hv, size=8.5, fill=INK,
               weight="bold" if abs(hv - 42.0) < 0.01 else None)
    s.text(bx + 8, by + 181, "A 42-in STARTING CONFIGURATION fits anywhere up to X = 32.6, which is why G302 stages ROBOTS against the alliance wall.",
           size=8.5, fill=MUTED)

    cx2, cy2 = 890, 762
    s.rect(cx2, cy2 - 16, 760, 196, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(cx2 + 8, cy2, "CLIMB REACH (the arithmetic behind G416)", size=9.5, fill=ACCENT, weight="bold")
    s.text(cx2 + 8, cy2 + 19,
           "G416: no rung contact while any BUMPER is on the wall side of the CLIMB LINE (X = 48 Blue / 600 Red),",
           size=8.5, fill=INK)
    s.text(cx2 + 8, cy2 + 32,
           "unless the ROBOT is then supported solely by rungs. The nearest bumper face is X = 48, so the FRAME",
           size=8.5, fill=INK)
    s.text(cx2 + 8, cy2 + 45, "PERIMETER is at X = 51 (R402: 0.75 backing + 2.25 foam) and an 18-in reach (R105) ends at X = 33.0.",
           size=8.5, fill=INK)
    hdr2 = ("Rung", "Rung ctr X", "To centerline", "To wrap the rung", "Within R105 (18 in)?")
    colx2 = [cx2 + 8, cx2 + 90, cx2 + 190, cx2 + 300, cx2 + 430]
    for cxx, cell in zip(colx2, hdr2):
        s.text(cxx, cy2 + 70, cell, size=8.5, fill=ACCENT, weight="bold")
    s.line(cx2 + 6, cy2 + 75, cx2 + 752, cy2 + 75, stroke=RULE, sw=0.8)
    for i, (nm, top) in enumerate((("LEDGE", 30.0), ("CAMP", 54.0), ("SUMMIT", 78.0))):
        cxx_ = rung_center_x(top)
        ext = 51.0 - cxx_
        wrap = ext + RUNG_OD / 2.0          # a hook must clear the far face of the rung
        ok = "yes" if wrap <= 18.0 else "NO - from a hang only"
        for cX, cell in zip(colx2, (nm, "%.2f" % cxx_, "%.2f in" % ext,
                                    "%.2f in" % wrap, ok)):
            s.text(cX, cy2 + 92 + i * 15, cell, size=8.5,
                   fill=DIM if ext > 18 else INK, weight="bold" if ext > 18 else None)
    s.text(cx2 + 8, cy2 + 152,
           "From a hang on the LEDGE RUNG the CAMP RUNG is 6.43 in back, 24 in up, 24 in across (24.9 in plane P);",
           size=8.5, fill=MUTED)
    s.text(cx2 + 8, cy2 + 164,
           "the same step again reaches SUMMIT. LEDGE and SUMMIT share -12.0, so a direct LEDGE-SUMMIT",
           size=8.5, fill=MUTED)
    s.text(cx2 + 8, cy2 + 176,
           "reach (48 up, 12.86 back, 49.7 in plane P) is legal too - twice the reach, no traverse. Both count.",
           size=8.5, fill=MUTED)
    s.text(cx2 + 8, cy2 + 193,
           "PARK 3 / LEDGE RUNG 12 / CAMP RUNG 20 / SUMMIT RUNG 30. Protection runs from the start of ENDGAME through climb assessment.",
           size=8.5, fill=INK)

    s.titleblock(NOTES)
    return s


# =====================================================================
# SHEET 4 - OUTFITTER
# =====================================================================
def sheet_outfitter():
    s = Sheet(1500, 900, "DRAWING 4 OF 6 - OUTFITTER STATION (x4 PER FIELD)", 4, 6,
              "Chute centers: Blue (0, 30) and (0, 294) - Red (648, 294) and (648, 30) - model one, mirror/rotate three")
    K = 4.0
    GY = 560.0

    def z(v):
        return GY - K * v

    ex = 300.0
    s.view_label(ex, 96, "FIELD-SIDE ELEVATION", "4.0 px/in", "60-in wall segment shown; wall continues both ways")
    s.line(60, GY, 540, GY, stroke=INK, sw=2.0)
    s.text(62, GY + 14, "carpet Z = 0", size=9, fill=MUTED)
    s.rect(ex - K * 30, z(78), K * 60, K * 78, fill="#DFE3E8", stroke=WALL_D, sw=2.4)
    s.rect(ex - K * CHUTE_W / 2, z(CHUTE_SILL + CHUTE_H), K * CHUTE_W, K * CHUTE_H,
           fill="#8D97A3", stroke=INK, sw=2.0)
    s.text(ex, z(CHUTE_SILL + CHUTE_H / 2) + 4, "OPENING", size=10, fill="#ffffff", anchor="middle")
    s.rect(ex - K * TAG_PANEL / 2, z(TAG_Z_OUT + TAG_PANEL / 2), K * TAG_PANEL, K * TAG_PANEL,
           fill="#F5F5F5", stroke="#666666", sw=1.2)
    s.rect(ex - K * TAG_BODY / 2, z(TAG_Z_OUT + TAG_BODY / 2), K * TAG_BODY, K * TAG_BODY,
           fill="#111111", stroke="none", sw=0)
    s.text(ex - K * TAG_PANEL / 2 - 10, z(TAG_Z_OUT) - 4, "tag panel 9.0 sq", size=8.5,
           fill=INK, anchor="end")
    s.text(ex - K * TAG_PANEL / 2 - 10, z(TAG_Z_OUT) + 9, "tag ctr Z = 52.0", size=8.5, fill=INK, anchor="end")
    s.text(ex - K * TAG_PANEL / 2 - 10, z(TAG_Z_OUT) + 22, "IDs 1/2 (Blue), 14/15 (Red)", size=8.5, fill=INK, anchor="end")
    s.dim_h(ex - K * CHUTE_W / 2, ex + K * CHUTE_W / 2, z(CHUTE_SILL + CHUTE_H) - 16,
            "30.0", ext_from=z(CHUTE_SILL + CHUTE_H) - 2, critical=True)
    s.dim_v(z(CHUTE_SILL + CHUTE_H), z(CHUTE_SILL), ex + K * CHUTE_W / 2 + 34, "16.0",
            ext_from=ex + K * CHUTE_W / 2 + 6, critical=True, side="right")
    s.dim_v(z(CHUTE_SILL), GY, ex - K * CHUTE_W / 2 - 36, "24.0 sill",
            ext_from=ex - K * CHUTE_W / 2 - 6, critical=True)
    s.dim_v(z(TAG_Z_OUT), GY, ex - K * 30 - 34, "52.0 tag ctr", ext_from=ex - K * 30 - 6, size=9)
    s.text(ex, GY + 46, "opening 30.0 x 16.0 and sill 24.0 are CRITICAL - they set intake-from-chute geometry",
           size=9, fill=INK, anchor="middle")
    s.text(ex, GY + 60, "sill edge R0.5 (ref) - the opening spans Z 24.0 to 40.0", size=8.5,
           fill=MUTED, anchor="middle")

    sx0 = 780.0
    s.view_label(sx0 + 60, 96, "SECTION A-A (through the chute centerline)", "4.0 px/in",
                 "field LEFT, human player RIGHT")
    s.line(sx0 - 150, GY, sx0 + 300, GY, stroke=INK, sw=2.0)
    s.rect(sx0, z(78), K * 2.0, K * 78, fill=WALL, stroke=WALL_D, sw=1.6)
    s.rect(sx0, z(CHUTE_SILL + CHUTE_H), K * 2.0, K * CHUTE_H, fill="#FFFFFF",
           stroke=WALL_D, sw=1.0)
    rx1 = sx0 + K * 2.0
    ry1 = z(CHUTE_SILL)
    rx2 = rx1 + K * 40.0 * math.cos(math.radians(30))
    ry2 = ry1 - K * 40.0 * math.sin(math.radians(30))
    s.line(rx1, ry1, rx2, ry2, stroke=TRUSS_D, sw=5, cap="round")
    s.line(rx2, ry2, rx2, GY, stroke=TRUSS, sw=3)
    s.line(rx1, ry1, rx1 + 90, ry1, stroke=MUTED, sw=0.9, dash="6 3")
    s.angle(rx1, ry1, 62, 0, -30, "30 deg (ref)", lx=rx1 + 96, ly=ry1 - 24)
    s.rect(sx0 - 8, z(TAG_Z_OUT + TAG_PANEL / 2), 8, K * TAG_PANEL, fill="#111111",
           stroke="#666666", sw=0.8)
    s.text(sx0 - 16, z(TAG_Z_OUT) + 4, "tag panel (field side)", size=8.5, fill=INK, anchor="end")
    s.dim_v(z(CHUTE_SILL), GY, sx0 - 44, "24.0", ext_from=sx0 - 8, size=9, critical=True)
    s.dim_v(z(CHUTE_SILL + CHUTE_H), z(CHUTE_SILL), sx0 + K * 2 + 26, "16.0",
            ext_from=sx0 + K * 2 + 6, size=9, critical=True, side="right")
    s.text(sx0 + 40, GY + 46, "Wall thickness 2.0 (ref). Ramp run 40 in at 30 deg (ref), width 30,", size=8.5, fill=MUTED)
    s.text(sx0 + 40, GY + 58, "side cheek funnels flaring to 36 in at the loading end (ref).", size=8.5, fill=MUTED)
    s.text(sx0 + 40, GY + 70, "Behind-wall geometry is non-interactive; delivery is by gravity onto the sill.", size=8.5, fill=MUTED)

    cx0, cy0 = 1180.0, 190.0
    C = 6.0
    s.view_label(cx0 + 90, 96, "CLEARANCE - CRATE THROUGH CHUTE", "6.0 px/in")
    s.rect(cx0, cy0, C * CHUTE_W, C * CHUTE_H, fill="#EDEFF2", stroke=INK, sw=2.0)
    env = CRATE_S + 2 * CRATE_CROWN
    s.rect(cx0 + (C * CHUTE_W - C * env) / 2, cy0 + (C * CHUTE_H - C * env) / 2,
           C * env, C * env, fill=CRATE, stroke=CRATE_D, sw=2.0, rx=C * 1.0, op=0.85)
    s.dim_h(cx0, cx0 + C * CHUTE_W, cy0 - 20, "30.0 opening", ext_from=cy0 - 4, size=9,
            critical=True)
    s.dim_v(cy0, cy0 + C * CHUTE_H, cx0 + C * CHUTE_W + 34, "16.0 opening",
            ext_from=cx0 + C * CHUTE_W + 6, size=9, critical=True, side="right")
    s.dim_v(cy0 + (C * CHUTE_H - C * env) / 2, cy0 + (C * CHUTE_H + C * env) / 2, cx0 - 30,
            "13.0 crowned envelope", ext_from=cx0 - 6, size=9)
    s.text(cx0 - 40, cy0 + C * CHUTE_H + 34, "Clearance 3.0 in on the crate's crowned envelope.", size=9, fill=INK)
    s.text(cx0 - 40, cy0 + C * CHUTE_H + 48, "A cube's minimum width in any orientation is its edge,", size=8.5, fill=MUTED)
    s.text(cx0 - 40, cy0 + C * CHUTE_H + 60, "so tilting does not help - the opening must exceed 13.0 in.", size=8.5, fill=MUTED)
    s.text(cx0 - 40, cy0 + C * CHUTE_H + 78, "O2 CELL passes end-on (5.0 x 5.0) or lengthwise (14.0 x 5.0).", size=8.5, fill=INK)
    s.text(cx0 - 40, cy0 + C * CHUTE_H + 90, "ROPE COIL passes flat (10.0 x 2.5) or on edge (10.0 tall).", size=8.5, fill=INK)

    px0, py0 = 1150.0, 496.0
    P = 2.6
    s.view_label(px0 + 100, 432, "PLAN - OUTFITTER LANE (tape)", "2.6 px/in", "field below the wall line")
    s.rect(px0, py0, P * 120, P * 4, fill=WALL, stroke=WALL_D, sw=1.4)
    s.rect(px0 + P * 45, py0, P * CHUTE_W, P * 4, fill="#E8A33D", stroke="#B57718", sw=1.5)
    s.text(px0 + P * 60, py0 - 10, "chute opening 30.0", size=8.5, fill="#7A4E0C", anchor="middle")
    s.rect(px0 + P * 42, py0 + P * 4, P * LANE_TAPE[0], P * LANE_TAPE[1],
           fill="#E8A33D", stroke="#B57718", sw=1.8, dash="6 4", op=0.25)
    s.text(px0 + P * 60, py0 + P * 26, "OUTFITTER LANE", size=9.5, fill="#7A4E0C", anchor="middle")
    s.text(px0 + P * 60, py0 + P * 34, "no-defense zone", size=8, fill="#7A4E0C", anchor="middle")
    s.dim_h(px0 + P * 42, px0 + P * 78, py0 + P * 58, "36.0", ext_from=py0 + P * 54,
            size=9, critical=True)
    s.dim_v(py0 + P * 4, py0 + P * 52, px0 + P * 88, "48.0", ext_from=px0 + P * 82,
            size=9, critical=True, side="right")
    s.text(px0, py0 + P * 74, "Tape 2.0 in wide, line edge on the stated coordinate.", size=8.5, fill=MUTED)
    s.text(px0, py0 + P * 84, "Stock per alliance: 7 CACHE CRATES, 7 O2 CELLS, 7 ROPE COILS across", size=8.5, fill=INK)
    s.text(px0, py0 + P * 94, "the two stations; robot preloads are drawn from this stock.", size=8.5, fill=INK)

    s.titleblock(NOTES)
    return s


# =====================================================================
# SHEET 5 - GAME PIECES
# =====================================================================
def sheet_pieces():
    s = Sheet(1560, 1000, "DRAWING 5 OF 6 - SUPPLIES (GAME PIECES)", 5, 6,
              "21 of each per MATCH, 63 total - model rigid at nominal size - possession limit 2")
    E = 8.0

    ax, ay = 250.0, 200.0
    s.view_label(ax, 96, "CACHE CRATE", "8.0 px/in", "cube, ~2.0 lb, expedition violet #7B3FA0")
    hs = E * CRATE_S / 2
    cr = E * CRATE_CROWN
    s.path("M %.1f %.1f q %.1f %.1f %.1f 0 q %.1f %.1f 0 %.1f q %.1f %.1f %.1f 0 q %.1f %.1f 0 %.1f z"
           % (ax - hs, ay - hs, hs, -cr * 2, 2 * hs, cr * 2, hs, 2 * hs,
              -hs, cr * 2, -2 * hs, -cr * 2, -hs, -2 * hs),
           fill=CRATE, stroke=CRATE_D, sw=2.4)
    s.line(ax, ay - hs - 30, ax, ay + hs + 30, stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.dim_h(ax - hs, ax + hs, ay + hs + 38, "12.0 (all three axes)", ext_from=ay + hs + 6,
            critical=True)
    s.dim_v(ay - hs, ay + hs, ax - hs - 34, "12.0", ext_from=ax - hs - 6, critical=True)
    s.leader(ax + hs * 0.5, ay - hs - cr, ax + hs + 34, ay - hs + 8, "face crown 0.5 (ref)")
    s.text(ax, ay + hs + 66, "Maximum envelope across the crown: 13.0 in", size=9, fill=DIM, anchor="middle")
    s.text(ax, ay + hs + 80, "edge fillets R1.0 (ref) - sewn ripstop skin over a PU foam core",
           size=8.5, fill=MUTED, anchor="middle")

    bx, by = 770.0, 200.0
    s.view_label(bx, 96, "O2 CELL", "8.0 px/in", "cylinder, ~1.5 lb, body #F2F2F0 with #2E8B57 caps")
    L, D = E * CELL_L, E * CELL_D
    body = E * (CELL_L - 2 * CELL_DOME)
    s.rect(bx - body / 2, by - D / 2, body, D, fill=CELL, stroke="#8A8F94", sw=2.0)
    s.path("M %.1f %.1f a %.1f %.1f 0 0 0 0 %.1f" % (bx - body / 2, by - D / 2, E * CELL_DOME, D / 2, D),
           fill=CELL_CAP, stroke="#1F5E3C", sw=1.8)
    s.path("M %.1f %.1f a %.1f %.1f 0 0 1 0 %.1f" % (bx + body / 2, by - D / 2, E * CELL_DOME, D / 2, D),
           fill=CELL_CAP, stroke="#1F5E3C", sw=1.8)
    s.line(bx - L / 2 - 26, by, bx + L / 2 + 26, by, stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.dim_h(bx - L / 2, bx + L / 2, by + D / 2 + 44, "14.0 overall", ext_from=by + D / 2 + 6,
            critical=True)
    s.dim_h(bx - body / 2, bx + body / 2, by - D / 2 - 24, "11.0 arc endpoints (ref)",
            ext_from=by - D / 2 - 6, size=9)
    s.dim_v(by - D / 2, by + D / 2, bx + L / 2 + 40, "5.0 dia", ext_from=bx + L / 2 + 8,
            critical=True, side="right")
    s.text(bx, by + D / 2 + 70, "domes 1.5 each (ref), R1.0 fillet at each cap/body junction (ref):",
           size=8.5, fill=MUTED, anchor="middle")
    s.text(bx, by + D / 2 + 82, "the cap arc meets the wall at a 28.1 deg break, so full 5.0 dia runs 10.44, not 11.0.",
           size=8.5, fill=MUTED, anchor="middle")
    s.text(bx, by + D / 2 + 94, "4.0 OD rigid core, 0.5 EVA sleeve (ref). Fillet band is #4D4D4D.",
           size=8.5, fill=MUTED, anchor="middle")
    s.text(bx, by + D / 2 + 110, "rolls when dropped - orientation control is the design problem",
           size=9, fill=INK, anchor="middle")

    cx, cy = 1260.0, 200.0
    s.view_label(cx, 96, "ROPE COIL", "8.0 px/in", "torus, ~1.0 lb, amber #D9A441")
    s.circle(cx, cy, E * COIL_OD / 2, fill=COIL, stroke=COIL_D, sw=2.4)
    s.circle(cx, cy, E * COIL_ID / 2, fill="#FFFFFF", stroke=COIL_D, sw=2.0)
    s.dim_h(cx - E * COIL_OD / 2, cx + E * COIL_OD / 2, cy + E * COIL_OD / 2 + 38, "10.0 OD",
            ext_from=cy + E * COIL_OD / 2 + 6, critical=True)
    s.dim_h(cx - E * COIL_ID / 2, cx + E * COIL_ID / 2, cy - 8, "5.0 ID", critical=True, size=9)
    s.rect(cx + E * COIL_OD / 2 + 54, cy - E * COIL_TUBE / 2, E * COIL_TUBE, E * COIL_TUBE,
           fill=COIL, stroke=COIL_D, sw=1.6, rx=E * COIL_TUBE / 2)
    s.dim_v(cy - E * COIL_TUBE / 2, cy + E * COIL_TUBE / 2,
            cx + E * COIL_OD / 2 + 54 + E * COIL_TUBE + 28, "2.5 tube",
            ext_from=cx + E * COIL_OD / 2 + 54 + E * COIL_TUBE + 6, size=9,
            critical=True, side="right")
    s.text(cx, cy + E * COIL_OD / 2 + 64, "solid molded rubber/foam - semi-compliant",
           size=8.5, fill=MUTED, anchor="middle")

    s.line(60, 386, 1500, 386, stroke=RULE, sw=1.0)
    s.text(780, 412, "CLEARANCE STUDIES - the four fits every mechanism is designed against",
           size=12, fill=ACCENT, weight="bold", anchor="middle")

    def note_col(x, y, lines):
        for i, t in enumerate(lines):
            s.text(x, y + i * 12, t, size=8.5, fill=INK if i < 2 else MUTED)

    # 1 - crate in shelf slot
    x1, y1 = 220.0, 580.0
    s.view_label(x1, 434, "1 - CRATE IN SHELF SLOT", "8.0 px/in")
    s.rect(x1 - E * SLOT_W / 2, y1, E * SLOT_W, E * 0.75, fill=SHELF, stroke=CRAG_EDGE, sw=1.4)
    for sgn in (-1, 1):
        s.rect(x1 + sgn * E * SLOT_W / 2 - (E * FENCE_W if sgn > 0 else 0), y1 - E * FENCE_H,
               E * FENCE_W, E * FENCE_H, fill=SHELF, stroke=CRAG_EDGE, sw=1.0)
    s.rect(x1 - E * CRATE_S / 2, y1 - E * CRATE_S, E * CRATE_S, E * CRATE_S,
           fill=CRATE, stroke=CRATE_D, sw=2.0, rx=E * 0.8, op=0.85)
    s.dim_h(x1 - E * SLOT_W / 2, x1 + E * SLOT_W / 2, y1 + 34, "14.0 slot",
            ext_from=y1 + 10, size=9, critical=True)
    s.dim_h(x1 - E * CRATE_S / 2, x1 + E * CRATE_S / 2, y1 - E * CRATE_S - 22, "12.0 crate",
            ext_from=y1 - E * CRATE_S - 6, size=9, critical=True)
    note_col(x1 - 150, y1 + 62, [
        "0.78 in clear per side at the fence tops - the binding width.",
        "A CRATE rests on its bottom crown, so its side faces reach the",
        "full 0.5 bulge at 6.5 up: 12.44 wide at h = 2.0, 13.00 at h = 6.5.",
        "The 13.0 crown clears the 2.0 fences by 4.5 and touches nothing.",
        "Slot centers -15.5 / 0 / +15.5; neighbours clear each other by 2.5.",
        "Four 1.5 x 2.0 fences: 4 x 1.5 + 3 x 14.0 = 48.0 exactly."])

    # 2 - crate through chute
    x2, y2 = 570.0, 580.0
    C = 6.0
    s.view_label(x2, 434, "2 - CRATE THROUGH CHUTE", "6.0 px/in")
    s.rect(x2 - C * CHUTE_W / 2, y2 - C * CHUTE_H, C * CHUTE_W, C * CHUTE_H,
           fill="#EDEFF2", stroke=INK, sw=2.0)
    env = CRATE_S + 2 * CRATE_CROWN
    s.rect(x2 - C * env / 2, y2 - C * CHUTE_H + (C * CHUTE_H - C * env) / 2, C * env, C * env,
           fill=CRATE, stroke=CRATE_D, sw=2.0, rx=C * 1.0, op=0.85)
    s.dim_h(x2 - C * CHUTE_W / 2, x2 + C * CHUTE_W / 2, y2 + 32, "30.0", ext_from=y2 + 8,
            size=9, critical=True)
    s.dim_v(y2 - C * CHUTE_H, y2, x2 + C * CHUTE_W / 2 + 34, "16.0",
            ext_from=x2 + C * CHUTE_W / 2 + 6, size=9, critical=True, side="right")
    note_col(x2 - 150, y2 + 62, [
        "13.0 crowned envelope vs a 16.0 opening: 3.0 in clear.",
        "The tightest piece/aperture pair on the FIELD.",
        "A cube's minimum width is its edge, so tilting does not help."])

    # 3 - cell in socket
    x3, y3 = 930.0, 524.0
    s.view_label(x3, 434, "3 - CELL IN SOCKET", "8.0 px/in")
    s.line(x3 - 96, y3 - 20, x3 - 96, y3 + 190, stroke=CRAG_EDGE, sw=3)
    s.text(x3 - 104, y3 + 150, "face", size=8.5, fill=INK, anchor="end")
    rimx, rimy = x3 - 96 + E * SOCK_STANDOFF, y3 + 30
    s.add('<g transform="rotate(%g %.2f %.2f)">' % (SOCK_TILT, rimx, rimy))
    s.rect(rimx - E * SOCK_OD / 2, rimy, E * SOCK_OD, E * SOCK_TUBE, fill="none",
           stroke=BLUE_D, sw=2.2)
    s.line(rimx - E * SOCK_OD / 2, rimy + E * SOCK_TUBE, rimx + E * SOCK_OD / 2,
           rimy + E * SOCK_TUBE, stroke=BLUE_D, sw=4)
    s.rect(rimx - E * CELL_D / 2, rimy + E * SOCK_TUBE - E * CELL_L, E * CELL_D, E * CELL_L,
           fill=CELL, stroke=CELL_CAP, sw=1.8, rx=E * 1.5)
    s.add('</g>')
    s.ellipse(rimx, rimy, E * SOCK_OD / 2, E * SOCK_OD / 6, fill="none", stroke=BLUE_D,
              sw=2.2, rot=SOCK_TILT)
    s.dim_h(x3 - 96, rimx, rimy - 74, "8.0 standoff", ext_from=rimy - 58, size=9, critical=True)
    note_col(x3 - 150, y3 + 210, [
        "ID 6.50 +/- 0.125 vs a 5.0 CELL: 0.75 in radial clearance",
        "per side (1.50 on diameter).",
        "Tube 7.0 deep, so a 14.0 CELL protrudes 7.0 along the axis",
        "and stands 4.39 in above the rim's uphill lip.",
        "The seated CG sits below the rim, so it cannot tip out."])

    # 4 - coil on peg
    x4, y4 = 1290.0, 512.0
    s.view_label(x4, 434, "4 - COIL ON PEG", "8.0 px/in")
    root = (x4 - 60, y4 + 120)
    s.line(root[0] - 34, root[1] - 130, root[0] - 34, root[1] + 40, stroke=CRAG_EDGE, sw=3)
    s.text(root[0] - 40, root[1] + 32, "face", size=8.5, fill=INK, anchor="end")
    s.add('<g transform="rotate(-45 %.1f %.1f)">' % root)
    s.rect(root[0], root[1] - E * PEG_OD / 2, E * PEG_EXP, E * PEG_OD, fill="#999999",
           stroke="#333333", sw=1.6, rx=E * PEG_OD / 2)
    s.add('</g>')
    s.circle(root[0] + 10, root[1] - 8, E * COIL_OD / 2, fill="none", stroke=COIL_D, sw=2.2)
    s.circle(root[0] + 10, root[1] - 8, E * COIL_ID / 2, fill="none", stroke=COIL_D, sw=1.6)
    s.angle(root[0], root[1], 46, 0, -45, "45 deg", lx=root[0] + 66, ly=root[1] - 22)
    note_col(x4 - 150, y4 + 210, [
        "5.0 hole over a 1.5 peg at 45 deg, 10.0 exposed.",
        "Max tilt from perpendicular-to-peg is about 48 deg;",
        "a vertical hang needs 45 deg, so the COIL wedges",
        "near-vertical and is captured, not balanced.",
        "Center rests about 1 in above the peg root."])

    tx, ty = 90, 800
    s.rect(tx, ty - 16, 1380, 112, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(tx + 8, ty, "SUPPLY SUMMARY", size=10, fill=ACCENT, weight="bold")
    hdr = ("SUPPLY", "Shape", "Nominal size", "Max envelope", "Weight", "Color", "Scores on")
    colx = [tx + 8, tx + 130, tx + 250, tx + 430, tx + 570, tx + 660, tx + 850]
    for cxx, cell in zip(colx, hdr):
        s.text(cxx, ty + 20, cell, size=8.5, fill=ACCENT, weight="bold")
    s.line(tx + 6, ty + 25, tx + 1372, ty + 25, stroke=RULE, sw=0.8)
    rows = [("CACHE CRATE", "cube, pillowed faces", "12.0 cube", "13.0 across the crown",
             "~2.0 lb", "#7B3FA0 violet", "Shelf 1, Shelf 2, BASE DEPOT"),
            ("O2 CELL", "domed cylinder, R1.0", "5.0 dia x 14.0", "5.0 x 14.0",
             "~1.5 lb", "#F2F2F0 / #2E8B57 / #4D4D4D", "Low / Mid / Summit Socket, BASE DEPOT"),
            ("ROPE COIL", "torus", "10.0 OD, 2.5 tube, 5.0 ID", "10.0 x 2.5",
             "~1.0 lb", "#D9A441 amber", "Low / Mid / High Peg, BASE DEPOT")]
    for i, r in enumerate(rows):
        for cxx, cell in zip(colx, r):
            s.text(cxx, ty + 44 + i * 16, cell, size=8.5, fill=INK)
    s.text(tx + 8, ty + 98,
           "No SUPPLY is colored in or near an alliance color, so none can be mistaken for an alliance element by a referee, a driver, or a vision pipeline.",
           size=8.5, fill=MUTED)

    s.titleblock(NOTES)
    return s


# =====================================================================
def main():
    made = []
    for fn, name in ((sheet_field, "field-top-view.svg"),
                     (sheet_crag, "crag.svg"),
                     (sheet_headwall, "headwall.svg"),
                     (sheet_outfitter, "outfitter.svg"),
                     (sheet_pieces, "game-pieces.svg"),
                     (sheet_tags, "apriltag-map.svg")):
        fn().save(os.path.join(HERE, name))
        made.append(name)
    print("wrote: " + ", ".join(made))


if __name__ == "__main__":
    main()
