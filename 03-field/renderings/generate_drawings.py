# -*- coding: utf-8 -*-
"""
Generate the six SUMMIT PUSH field drawing sheets from the locked
dimension ledger. Run from anywhere:

    python 03-field/renderings/generate_drawings.py

Every dimension below comes from 03-field/FIELD-CAD-PACKAGE.md §10
(the master dimension ledger). Change a number here only after the
ledger has changed.
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


def _crag_plan(s, fx, fy, SC, cx, cy, d, col, cold, name, label_below=False):
    """Draw one CRAG in plan; d = +1 if its SHELF FACE is the +X face."""
    half = CRAG_S / 2.0
    shelf_plane = cx + d * half
    peg_plane = cx - d * half

    def R(x0, x1, y0, y1, **kw):
        s.rect(min(fx(x0), fx(x1)), min(fy(y0), fy(y1)),
               abs(fx(x1) - fx(x0)), abs(fy(y1) - fy(y0)), **kw)

    # BASE DEPOT: the outer leg with its two corner squares, then the two corner arms
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
    s.text(fx(cx), fy(cy) + 0.36 * s.LABEL, "SPIRE", size=s.LABEL - 0.5, fill=cold,
           weight="bold", anchor="middle")
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
    # name on the outboard side of the APRON (the CENTER CACHE is on the inboard side)
    if label_below:
        s.text(fx(cx), fy(ay0) + 5 + 0.74 * s.LABEL, name, size=s.LABEL, fill=cold,
               weight="bold", anchor="middle", halo=True)
    else:
        s.text(fx(cx), fy(ay1) - 6, name, size=s.LABEL, fill=cold, weight="bold",
               anchor="middle", halo=True)


def sheet_field():
    s = Sheet(1460, 950, "DRAWING 1 OF 6 - FIELD TOP VIEW (PLAN)", 1, 6,
              "Field 648 x 324 in (54 ft x 27 ft) - scale 1.8 px/in - Blue alliance at left")
    SC = 1.8
    OX, OY = 112, 74
    L, N = s.LABEL, s.NOTE
    AMBER_T = "#6B440A"

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
    # FIELD centerline: 2-in white tape, broken where the two CRAG footprints cross
    # it (the DEPOT trays stop 8 in short). G402 and G502 are line calls against it.
    for _y0, _y1 in ((324.0, 264.0), (216.0, 108.0), (60.0, 0.0)):
        s.line(fx(FL / 2), fy(_y0), fx(FL / 2), fy(_y1), stroke="#FFFFFF", sw=3.0)
        s.line(fx(FL / 2), fy(_y0), fx(FL / 2), fy(_y1), stroke=MUTED, sw=0.7, dash="10 6")
    s.text(fx(FL / 2) + 6, fy(FW) + 7 + 0.72 * N, "FIELD CENTERLINE X = 324 (2-in white tape)",
           size=N, fill=INK)

    # CENTER CACHE band first, so the CRAG sockets that overhang it stay crisp
    s.rect(fx(300), fy(216), SC * 48, SC * 108, fill="#FFFFFF", stroke=MUTED,
           sw=1.3, dash="7 4", op=0.5)
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
        # CLIMB LINE: the G416 plane, carried across the full field width. Over
        # Y 90-234 the BASECAMP boundary drawn above already marks it.
        for _y0, _y1 in ((0.0, 90.0), (234.0, 324.0)):
            s.line(fx(X(48.0)), fy(Y(_y0)), fx(X(48.0)), fy(Y(_y1)),
                   stroke=cold, sw=1.4, dash="5 5")
        s.text(fx(X(19.5)), fy(Y(162)), "BASECAMP = HEADWALL ZONE", size=N,
               fill=cold, weight="bold", anchor="middle", rot=-90 if not mir else 90)

        htop = HW_X - TRUSS_TOP * T15
        s.rect(min(fx(X(htop)), fx(X(HW_X))), min(fy(Y(90.0)), fy(Y(234.0))),
               abs(fx(X(HW_X)) - fx(X(htop))), SC * HW_W,
               fill=TRUSS, stroke=TRUSS_D, sw=1.6, op=0.85)
        for yb in (138.0, 186.0):
            s.line(fx(X(htop)), fy(Y(yb)), fx(X(HW_X)), fy(Y(yb)), stroke=TRUSS_D, sw=1.2)
        # HEADWALL name: in open carpet beside the truss top, with a leader to it
        s.leader(fx(X(44)), fy(Y(229)), fx(X(54)), fy(Y(243)), "%s HEADWALL" % nm,
                 anchor="start" if not mir else "end", fill=TRUSS_D, weight="bold")
        for i, ly in enumerate(LANE_Y):
            s.text(fx(X(36.75)), fy(Y(ly)) + 0.36 * L, "L%d" % (i + 1), size=L, fill="#FFFFFF",
                   weight="bold", anchor="middle")

        for cy_ in CHUTE_Y:
            s.rect(min(fx(X(0)), fx(X(48))),
                   min(fy(Y(cy_ - 18)), fy(Y(cy_ + 18))), SC * 48, SC * 36,
                   fill="#E8A33D", stroke="#B57718", sw=1.5, dash="6 4", op=0.28)
            s.rect(fx(X(0)) - (6 if mir else 0),
                   min(fy(Y(cy_ - 15)), fy(Y(cy_ + 15))), 6, SC * 30,
                   fill="#E8A33D", stroke="#B57718", sw=1.3)
            lx = fx(X(25.5))
            ly = fy(Y(cy_)) - 1.2 * N + 0.36 * N
            s.lines(lx, ly, ["OUTFITTER", "LANE 36 x 48", "chute (%d, %d)" % (X(0), Y(cy_))],
                    size=N, fill=AMBER_T, anchor="middle", pitch=1.2 * N)

        sx_ = STAGE_X_R if mir else STAGE_X_B
        for ty_, t in zip(STAGE_Y, ("2 CRATES", "2 O2 CELLS", "2 ROPE COILS")):
            s.line(fx(sx_) - 9, fy(Y(ty_)) - 9, fx(sx_) + 9, fy(Y(ty_)) + 9, stroke=cold, sw=1.6)
            s.line(fx(sx_) - 9, fy(Y(ty_)) + 9, fx(sx_) + 9, fy(Y(ty_)) - 9, stroke=cold, sw=1.6)
            s.text(fx(sx_), fy(Y(ty_)) - 14, t, size=N, fill=cold, anchor="middle")
        s.text(fx(sx_), fy(Y(258)), "%s STAGING MARKS  X = %d" % (nm, sx_), size=L,
               fill=cold, weight="bold", anchor="middle")

        ccx, ccy = (CRAG_R if mir else CRAG_B)
        _crag_plan(s, fx, fy, SC, ccx, ccy, 1 if mir else -1, col, cold,
                   "%s CRAG (%d, %d)" % (nm, ccx, ccy), label_below=mir)

    LATIN = {(300, 186): ("CRATE", CRATE), (324, 186): ("O2", CELL_CAP), (348, 186): ("COIL", COIL),
             (300, 162): ("COIL", COIL), (324, 162): ("CRATE", CRATE), (348, 162): ("O2", CELL_CAP),
             (300, 138): ("O2", CELL_CAP), (324, 138): ("COIL", COIL), (348, 138): ("CRATE", CRATE)}
    for (mx, my), (lbl, c) in sorted(LATIN.items()):
        s.line(fx(mx) - 7, fy(my) - 7, fx(mx) + 7, fy(my) + 7, stroke=MUTED, sw=1.4)
        s.line(fx(mx) - 7, fy(my) + 7, fx(mx) + 7, fy(my) - 7, stroke=MUTED, sw=1.4)
        s.circle(fx(mx), fy(my), 7.0, fill=c, stroke="#333333", sw=0.9)
    # the leader lands on the band edge between two marks, not on a mark
    s.leader(fx(300), fy(150), fx(276), fy(150), "CENTER CACHE  X 300-348, Y 108-216",
             anchor="end")

    # dimensions
    s.dim_h(fx(0), fx(FL), fy(0) + 44, "648.0", ext_from=fy(0) + 8, critical=True)
    s.dim_v(fy(FW), fy(0), fx(0) - 54, "324.0", ext_from=fx(0) - 12, critical=True)
    s.dim_h(fx(0), fx(48), fy(234) - 30, "48.0", ext_from=fy(234) - 6, critical=True)
    s.dim_v(fy(234), fy(90), fx(66), "144.0", ext_from=fx(58), critical=True, side="right")
    s.dim_h(fx(264), fx(384), fy(304), "120.0 apron span (36 + 48 + 36)",
            ext_from=fy(264) - 4, halo=True)
    s.dim_v(fy(264), fy(216), fx(410), "48.0", ext_from=fx(388), side="right", critical=True)
    s.dim_v(fy(216), fy(196), fx(438), "20.0", ext_from=fx(388), side="right", critical=True)
    s.dim_v(fy(128), fy(108), fx(438), "20.0", ext_from=fx(388), side="right", critical=True)
    s.dim_v(fy(196), fy(128), fx(466), "68.0 open corridor", ext_from=fx(442), side="right")

    # origin marker at the corner; the axis compass sits on open carpet beside it
    s.circle(fx(0), fy(0), 5, fill="none", stroke=INK, sw=1.6)
    s.circle(fx(0), fy(0), 1.6, fill=INK, stroke=INK, sw=0.6)
    s.text(fx(0) + 8, fy(0) + 6 + 0.74 * N + 4, "ORIGIN (0, 0), +Z up", size=N, fill=INK)
    c0x, c0y = fx(62), fy(8)
    s.circle(c0x, c0y, 2.2, fill=INK, stroke=INK, sw=0.6)
    s.arrow(c0x, c0y, c0x + 52, c0y, stroke=INK, sw=1.6)
    s.arrow(c0x, c0y, c0x, c0y - 52, stroke=INK, sw=1.6)
    s.text(c0x + 57, c0y + 0.36 * 10, "+X", size=10, fill=INK, weight="bold")
    s.text(c0x, c0y - 57, "+Y", size=10, fill=INK, weight="bold", anchor="middle")
    s.text(c0x + 8, c0y - 30, "always-blue-origin NWU", size=N, fill=INK)
    s.text(c0x + 8, c0y - 30 + 1.25 * N, "(+X toward Red, +Y left)", size=N, fill=INK)
    s.scalebar(fx(FL) - 300, fy(0) + 58, SC, 48, label="Scale 1.8 px/in")

    # ---- notes panels: sized to their content, spread across the sheet ----
    top = fy(0) + 88
    H = s.HEAD
    pitch = 1.42 * N
    y0 = top + 8 + 0.74 * H            # heading baseline
    tape = [("BASECAMP / HEADWALL ZONE  X 0-48, Y 90-234", BLUE, "6 4"),
            ("CLIMB LINE  X = 48 / 600, full width - G416 line call", BLUE, "5 5"),
            ("CRAG APRON  36 shelf & peg faces / 20 socket faces / R20", BLUE, "8 5"),
            ("OUTFITTER LANE  36 x 48, centered on the chute", "#B57718", "6 4"),
            ("FIELD CENTERLINE  2-in white at X = 324 - G402 / G502 line call", MUTED, "10 6"),
            ("CENTER CACHE band + nine white marks", MUTED, "7 4")]
    symbols = ["socket (LOW, MID; SUMMIT on the shelf face)", "Low / Mid Peg",
               "High Peg (on the spire)", "BASE DEPOT tray", "staging mark (alliance tape)",
               "HEADWALL truss, lanes L1-L3"]
    cache_notes = ["Each type appears once per row and once per column.",
                   "Aggregate haul distance is identical for both alliances (725.0 in each)."]
    plan_ink = ["All tape 2.0 in wide; the line edge sits on the stated coordinate.",
                "Alliance-colored tape for alliance zones; white for neutral marks."]
    plan_muted = ["CRAG plan tint is a drafting convention; the CRAG itself is tan",
                  "(see 03-field/MATERIALS-AND-COLORS.md).",
                  "Model the Blue half once, then rotate-pattern 180 deg about (324, 162)."]
    need = [40 + max(s.tw(t, N) for t, _, _ in tape),
            34 + max(s.tw(t, N) for t in symbols),
            max(290, max(s.tw(t, N) for t in cache_notes)),
            max(s.tw(t, N) for t in plan_ink + plan_muted)]
    need = [n + 16 for n in need]
    gapx = 12
    extra = (s.w - 40 - 3 * gapx - sum(need)) / 4.0
    assert extra >= 0, "field notes panels do not fit"
    widths = [n + extra for n in need]
    xs = [20]
    for wv in widths[:-1]:
        xs.append(xs[-1] + wv + gapx)
    ph = y0 + 0.6 * H + 7 * pitch - top          # tallest panel: heading + 6 rows
    assert top + ph <= s.tb_top - 6, "field notes panels run into the title block"

    def panel(i, heading):
        s.rect(xs[i], top, widths[i], ph, fill="#FFFFFF", stroke=RULE, sw=0.9)
        s.text(xs[i] + 8, y0, heading, size=H, fill=ACCENT, weight="bold")
        return xs[i] + 8

    def row(i):
        return y0 + 0.6 * H + (i + 1) * pitch

    # TAPE KEY
    lx = panel(0, "TAPE KEY")
    for i, (t, c, dsh) in enumerate(tape):
        yy = row(i)
        s.line(lx, yy - 0.32 * N, lx + 26, yy - 0.32 * N, stroke=c, sw=1.8, dash=dsh)
        s.text(lx + 32, yy, t, size=N, fill=INK)

    # PLAN SYMBOLS: every mark on the plan that is not tape
    sym = panel(1, "PLAN SYMBOLS") + 12
    for i, t in enumerate(symbols):
        yy = row(i) - 0.32 * N
        if i == 0:
            s.circle(sym, yy, SC * SOCK_OD / 2, fill=SOCKET_L, stroke=BLUE_D, sw=1.1)
        elif i in (1, 2):
            s.line(sym - 8, yy, sym + 5, yy, stroke="#555555", sw=3.0, cap="round",
                   dash="3 2" if i == 2 else None)
        elif i == 3:
            s.rect(sym - 7, yy - 5, 13, 10, fill=DEPOT, stroke=CRAG_EDGE, sw=1.1)
        elif i == 4:
            s.line(sym - 5, yy - 5, sym + 5, yy + 5, stroke=BLUE_D, sw=1.6)
            s.line(sym - 5, yy + 5, sym + 5, yy - 5, stroke=BLUE_D, sw=1.6)
        else:
            s.rect(sym - 7, yy - 5, 13, 10, fill=TRUSS, stroke=TRUSS_D, sw=1.2, op=0.85)
        s.text(sym + 14, row(i), t, size=N, fill=INK)

    # CENTER CACHE table: its coloured dots are the legend for the marks on the plan
    mx0 = panel(2, "CENTER CACHE - LATIN SQUARE STAGING")
    cw = (widths[2] - 16) / 4.0
    colx = [mx0 + cw * j for j in range(4)]
    for cxx, cell in zip(colx[1:], ("X = 300", "X = 324", "X = 348")):
        s.text(cxx, row(0), cell, size=N, fill=ACCENT, weight="bold")
    for i, yv in enumerate((186, 162, 138)):
        yy = row(i + 1)
        s.text(colx[0], yy, "Y = %d" % yv, size=N, fill=INK)
        for cxx, xv in zip(colx[1:], (300, 324, 348)):
            lbl, c = LATIN[(xv, yv)]
            s.circle(cxx + 5, yy - 0.34 * N, 5.0, fill=c, stroke="#333333", sw=0.8)
            s.text(cxx + 15, yy, lbl, size=N, fill=INK)
    s.lines(mx0, row(4) + 0.3 * N, cache_notes, size=N, fill=MUTED, pitch=pitch)

    # PLAN NOTES
    nx0 = panel(3, "PLAN NOTES")
    yy = s.lines(nx0, row(0), plan_ink, size=N, fill=INK, pitch=pitch)
    s.lines(nx0, yy, plan_muted, size=N, fill=MUTED, pitch=pitch)

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
    s = Sheet(1420, 960, "DRAWING 6 OF 6 - APRILTAG MAP", 6, 6,
              "26 tags, family 36h11 - body 6.5 in on an 8.125 in target on a 9.0 in panel - scale 1.8 px/in")
    SC = 1.8
    OX, OY = 96, 70
    L, N, H = s.LABEL, s.NOTE, s.HEAD

    def fx(X):
        return OX + SC * X

    def fy(Y):
        return OY + SC * (FW - Y)

    def tag_symbol(px, py, yaw):
        s.rect(px - 6, py - 6, 12, 12, fill="#F5F5F5", stroke="#666666", sw=0.9)
        s.rect(px - 3.6, py - 3.6, 7.2, 7.2, fill="#111111", stroke="none", sw=0)
        a = math.radians(yaw)
        nx, ny = math.cos(a), -math.sin(a)
        s.arrow(px + nx * 7, py + ny * 7, px + nx * 24, py + ny * 24, stroke=DIM, sw=1.3)
        return nx, ny

    s.rect(fx(0), fy(FW), SC * FL, SC * FW, fill=CARPET, stroke=INK, sw=2.4)
    s.line(fx(FL / 2), fy(FW), fx(FL / 2), fy(0), stroke=MUTED, sw=1.2, dash="12 4 3 4")
    for cc, col, cold, nm in ((CRAG_B, BLUE, BLUE_D, "BLUE CRAG"), (CRAG_R, RED, RED_D, "RED CRAG")):
        s.rect(fx(cc[0] - CRAG_S / 2), fy(cc[1] + CRAG_S / 2), SC * CRAG_S, SC * CRAG_S,
               fill=col, stroke=col, sw=1.2, op=0.16)
        s.text(fx(cc[0]), fy(cc[1]) + 0.36 * L, nm, size=L, fill=cold, weight="bold",
               anchor="middle", halo=True)
    for mir in (False, True):
        def X(v):
            return FL - v if mir else v

        def Y(v):
            return FW - v if mir else v
        htop = HW_X - TRUSS_TOP * T15
        s.rect(min(fx(X(htop)), fx(X(HW_X))), min(fy(Y(90.0)), fy(Y(234.0))),
               abs(fx(X(HW_X)) - fx(X(htop))), SC * HW_W,
               fill=TRUSS, stroke=TRUSS_D, sw=1.0, op=0.30)
        s.text(fx(X(16)), fy(162), "%s HEADWALL" % ("RED" if mir else "BLUE"), size=L,
               fill=TRUSS_D, weight="bold", anchor="middle", rot=90 if mir else -90)

    for (tid, x, y, z, yaw, lab) in TAGS:
        px, py = fx(x), fy(y)
        nx, ny = tag_symbol(px, py, yaw)
        # ID just beyond the arrow tip, clear of the arrowhead whichever way it points
        reach = 24 + 3 + abs(nx) * s.tw(str(tid), 10, True) / 2.0 + abs(ny) * 3.6
        s.text(px + nx * reach, py + ny * reach + 3.6, str(tid),
               size=10, fill=INK, weight="bold", anchor="middle")
        if lab == "OUTFITTER":
            s.text(px + nx * 40, py + 0.36 * N, "OUTFITTER", size=N, fill=INK,
                   anchor="start" if nx > 0 else "end")

    # legend line under the field
    ly = fy(0) + 24
    nx, ny = tag_symbol(fx(0) + 6, ly, 0)
    s.text(fx(0) + 40, ly + 0.36 * N,
           "Arrows show the tag FACE NORMAL (the direction a camera must look FROM to see it head-on is the opposite)",
           size=N, fill=INK)

    # table of heights
    top = ly + 22
    tx = 96
    rows = [("IDs", "Structure", "Z center", "Panel plane", "Facing"),
            ("1, 2 / 14, 15", "OUTFITTER (above chute)", "52.0", "X = 0 / 648 (wall)", "+X / -X"),
            ("3-5 / 16-18", "HEADWALL lane center", "12.0", "X = 39.0 / 609.0 (plumb)", "+X / -X"),
            ("6-13 / 19-26", "CRAG face pairs, +/-14.0 from the face centerline", "17.5",
             "the face plane", "outward")]
    foot = ["CRAG tags sit at 17.5 in so a crowned CACHE CRATE standing in the BASE DEPOT (apex Z = 13.25)",
            "clears the 8.125-in target (Z 13.44-21.56) by 0.19 in.",
            "HEADWALL panels are plumb at X = 39.0 - at least 4.42 in behind plane P over the whole panel,",
            "so nothing enters the climbing volume."]
    cw = [max(s.tw(r[j], N, False) for r in rows) + 26 for j in range(5)]
    colx = [tx + 8]
    for c in cw[:-1]:
        colx.append(colx[-1] + c)
    tw_ = max(colx[-1] + cw[-1] - tx, max(s.tw(t, N) for t in foot) + 16)
    pitch = 1.4 * N
    y0 = top + 8 + 0.74 * H
    fy0 = y0 + 0.5 * H + 4 * pitch + 1.6 * N           # first footnote baseline
    th = fy0 + (len(foot) - 1) * 1.25 * N + 0.9 * N - top
    s.rect(tx, top, tw_, th, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(tx + 8, y0, "TAG HEIGHTS AND PLANES", size=H, fill=ACCENT, weight="bold")
    for i, r in enumerate(rows):
        yy = y0 + 0.5 * H + (i + 1) * pitch
        for cxx, cell in zip(colx, r):
            s.text(cxx, yy, cell, size=N, fill=INK if i else ACCENT,
                   weight="bold" if i == 0 else None)
        if i == 0:
            s.line(tx + 6, yy + 0.4 * N, tx + tw_ - 6, yy + 0.4 * N, stroke=RULE, sw=0.8)
    s.lines(tx + 8, fy0, foot, size=N, fill=MUTED, pitch=1.25 * N)

    # panel detail
    k = 9.0
    dx = tx + tw_ + 70
    dy = s.view_label(dx + k * TAG_PANEL / 2, top + 0.74 * s.VIEW, "PANEL DETAIL", "9.0 px/in") + 4
    s.rect(dx, dy, k * TAG_PANEL, k * TAG_PANEL, fill="#F5F5F5", stroke="#666666", sw=1.2)
    o1 = (TAG_PANEL - TAG_TGT) / 2.0 * k
    s.rect(dx + o1, dy + o1, k * TAG_TGT, k * TAG_TGT, fill="#FFFFFF", stroke="#999999", sw=1.0)
    o2 = (TAG_PANEL - TAG_BODY) / 2.0 * k
    s.rect(dx + o2, dy + o2, k * TAG_BODY, k * TAG_BODY, fill="#111111", stroke="none", sw=0)
    pb = dy + k * TAG_PANEL
    # the smaller dimension sits nearer the part, so no extension line crosses a dimension line
    s.dim_h(dx + o1, dx + o1 + k * TAG_TGT, pb + 24, "8.125 target",
            ext_from=dy + o1 + k * TAG_TGT + 2, critical=True, tick=6)
    p2 = pb + 24 + 1.32 * s.DIM + 16
    s.dim_h(dx, dx + k * TAG_PANEL, p2, "9.00 panel",
            ext_from=pb + 3, tick=6)
    s.dim_v(dy + o2, dy + o2 + k * TAG_BODY, dx - 22, "6.50 body", ext_from=dx + o2 - 3,
            critical=True, tick=6)
    nx0 = dx + k * TAG_PANEL + 30
    yy = s.lines(nx0, dy + 0.74 * N, ["Vision software wants the BODY size:",
                                      "6.5 in = 0.1651 m. Never enter 8.125 or 9.0."], size=N, fill=INK)
    yy = s.lines(nx0, yy + 0.3 * N, ["Panels plumb +/-1 deg, square to facing +/-1 deg.",
                                     "Field build tolerance +/-0.25 in on tag centers;",
                                     "the CAD model must match the JSON exactly."], size=N, fill=MUTED)
    yy = s.lines(nx0, yy + 0.3 * N, ["Matte, non-glare finish. Keep the white border clear."],
                 size=N, fill=MUTED)
    assert nx0 + max(s.tw("Matte, non-glare finish. Keep the white border clear.", N),
                     s.tw("Panels plumb +/-1 deg, square to facing +/-1 deg.", N)) < s.w - 16
    assert top + th <= s.tb_top - 6 and p2 + 6 <= s.tb_top - 10

    s.titleblock(["Poses must match 04-vision/apriltag-field-layout.json exactly; the JSON is generated from this table and drives every simulation.",
                  NOTES[1], NOTES[2]])
    return s


# =====================================================================
# SHEET 2 - CRAG
# =====================================================================
def _notes(s, x, y, lines, w=None, title=None, size=None):
    """Note block: bold heading, then lines; lines in parentheses are muted.
    With w given, raises if a line would run past x + w."""
    size = size or s.NOTE
    yy = y
    if title:
        s.text(x, yy, title, size=s.HEAD, fill=ACCENT, weight="bold")
        yy += 1.35 * s.HEAD
    for t in lines:
        if w is not None and s.tw(t, size) > w:
            raise ValueError("note line too long for its column: %r" % t[:40])
        s.text(x, yy, t, size=size, fill=INK if not t.startswith("(") else MUTED)
        yy += s.PITCH * size
    return yy


def sheet_crag():
    s = Sheet(1960, 1340, "DRAWING 2 OF 6 - CRAG (x2 PER FIELD)", 2, 6,
              "Blue CRAG shown - Red is the 180 deg rotation about field center - main views 3.2 px/in, details as noted")
    K = 3.2
    GY = 470.0
    hw = K * CRAG_S / 2
    sw_ = K * SPIRE_S / 2
    L, N = s.LABEL, s.NOTE
    VY = 84                      # view-name baseline, row 1
    NY = GY + 80                 # note-block baseline, row 1
    COLW = 440                   # note column width

    def z(v):
        return GY - K * v

    s.line(40, GY, 1560, GY, stroke=INK, sw=2.0)
    s.text(42, GY + 4 + 0.74 * s.SUB, "carpet Z = 0", size=s.SUB, fill=MUTED)

    # ================= VIEW A - SHELF FACE =================
    ax = 250.0
    s.view_label(ax, VY, "VIEW A - SHELF FACE", "3.2 px/in", "faces the owning alliance wall")
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
    # slot-centre offset: between the Shelf 2 fence tops and the 54 tier ring
    s.dim_h(ax, ax + K * SLOT_CTRS[2], z(SHELF2) - 17, "15.5", ext_from=z(SHELF2) - 3,
            critical=True, tick=5)
    s.dim_h(ax - sw_, ax + sw_, z(SPIRE_TOP) - 16, "20.0", ext_from=z(SPIRE_TOP) - 2,
            critical=True)
    s.leader(ax + sw_ * 0.45, z(BEACON_Z), ax + hw + 26, z(BEACON_Z) - 12, "SUMMIT BEACON lantern")
    s.leader(ax + K * SOCK_OD / 2, z(SUM_SOCK_Z), ax + hw + 26, z(SUM_SOCK_Z) + 6,
             "Summit Socket (D2)")
    s.leader(ax - hw - K * SOCK_STANDOFF - 4, z(LOW_SOCK_Z) - 8, ax - hw - 40, z(LOW_SOCK_Z) - 30,
             "side-face sockets (D1)", anchor="end")
    s.leader(ax - K * SOCK_LAT - K * TAG_PANEL / 2, z(TAG_Z_CRAG), ax - hw - 26, z(TAG_Z_CRAG) + 8,
             "tags 6 / 7", anchor="end")
    _notes(s, 60, NY, [
        "Shelf 1 top 24.0, Shelf 2 top 42.0; 3 slots of 14.0 with four 1.5 x 2.0 fences.",
        "Slot centers -15.5 / 0 / +15.5 from the face centerline.",
        "Summit Socket rim Z = 72.0, on the crag centerline, 8.0 out from THIS face.",
        "Tags 6 / 7 (Blue): ctr Z = 17.5, +/-14.0 from the face centerline.",
        "BASE DEPOT lip 4.0 runs this face and wraps 16.0 onto both socket faces.",
        "(Dashed red lines: LED tier rings at 30 / 54 / 78, see VIEW C.)",
    ], title="VIEW A NOTES", w=COLW + 40)

    # ================= VIEW B - SOCKET FACE =================
    bx = 700.0
    s.view_label(bx, VY, "VIEW B - SOCKET FACE", "3.2 px/in",
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
    # socket names inside the tower face, beside their rims (the pegs sit outside it)
    s.text(bx + K * (-SOCK_LAT) + K * SOCK_OD / 2 + 5, z(LOW_SOCK_Z) + 0.36 * L,
           "Low Socket 30.0", size=L, fill=INK)
    s.text(bx + K * SOCK_LAT - K * SOCK_OD / 2 - 5, z(MID_SOCK_Z) + 0.36 * L,
           "Mid Socket 54.0", size=L, fill=INK, anchor="end")
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
        s.line(bx + K * 26, z(v), lx + 6, z(v), stroke=DIM, sw=s.SW_EXT)
        s.text(lx + 8, z(v) + 0.36 * s.DIM, lbl, size=s.DIM, fill=DIM)
        assert lx + 8 + s.tw(lbl, s.DIM) < 1150.0 - hw - 8, lbl
    s.arrow(lx - 2, GY, lx - 2, z(SPIRE_TOP), stroke=DIM, start=True, end=True)
    s.dim_h(bx + K * (-SOCK_LAT), bx, GY + 34, "14.0", ext_from=GY + 4, critical=True)
    s.dim_h(bx, bx + K * SOCK_LAT, GY + 34, "14.0", ext_from=GY + 4, critical=True)
    _notes(s, 560, NY, [
        "Socket rim centers sit +/-14.0 from the face centerline and 8.0 OUT",
        "from the face plane, measured normal to it (Detail D1).",
        "LOW is on the shelf-face side; MID is on the peg-face side, so each",
        "socket sits directly above one tag of the face pair.",
        "The Summit Socket, shown edge-on at the left, is on the SHELF FACE.",
        "Red ladder: heights above the carpet, Z = 0.",
    ], title="VIEW B NOTES", w=COLW)

    # ================= VIEW C - PEG FACE =================
    cx = 1150.0
    s.view_label(cx, VY, "VIEW C - PEG FACE", "3.2 px/in", "pegs project toward the viewer at 45 deg (D3)")
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
        s.text(cx + w + 8, z(tz) + 0.36 * L, "LED tier ring %g" % tz, size=L, fill=INK)
    for c in (-SOCK_LAT, SOCK_LAT):
        s.rect(cx + K * c - K * TAG_PANEL / 2, z(TAG_Z_CRAG + TAG_PANEL / 2),
               K * TAG_PANEL, K * TAG_PANEL, fill="#F5F5F5", stroke="#666666", sw=0.9)
        s.rect(cx + K * c - K * TAG_BODY / 2, z(TAG_Z_CRAG + TAG_BODY / 2),
               K * TAG_BODY, K * TAG_BODY, fill="#111111", stroke="none", sw=0)
    s.leader(cx + K * SOCK_LAT + K * TAG_PANEL / 2, z(TAG_Z_CRAG), cx + hw + 26, z(TAG_Z_CRAG) + 8,
             "tags 12 / 13")
    s.dim_h(cx, cx + K * PEG_LAT, z(LOW_PEG_Z) - 22, "14.0", ext_from=z(LOW_PEG_Z) - 6,
            critical=True)
    # High Peg offset dimensioned above the spire, clear of the lantern
    s.dim_h(cx, cx + K * HPEG_LAT, z(SPIRE_TOP) - 16, "7.0", ext_from=z(HIGH_PEG_Z) - 6,
            critical=True)
    s.dim_h(cx - hw, cx + hw, GY + 52, "48.0", ext_from=GY + 4, critical=True)
    _notes(s, 1010, NY, [
        "Low and Mid Peg roots +/-14.0 from the face centerline, Z 30.0 and 54.0.",
        "High Peg roots +/-7.0 from the spire centerline (14.0 apart), Z 78.0.",
        "All pegs OD 1.5, 45 deg up from the face, 10.0 exposed, tip R0.75.",
        "Tags 12 / 13 (Blue): ctr Z = 17.5, +/-14.0.",
        "Tier rings latch on CAMP establishment; the lantern is the SUMMIT BEACON.",
    ], title="VIEW C NOTES", w=COLW + 30)

    # ================= VIEW D - TOP (plan) =================
    dx, dy = 1660.0, 250.0
    s.view_label(dx, VY, "VIEW D - TOP (PLAN)", "3.2 px/in",
                 "shelf face LEFT, peg face RIGHT")
    h = K * CRAG_S / 2
    s.rect(dx - h - K * DEPOT_CH, dy - h - K * DEPOT_WRAP, K * DEPOT_CH,
           K * (CRAG_S + 2 * DEPOT_WRAP), fill=DEPOT, stroke=CRAG_EDGE, sw=1.3)
    for sgn in (-1, 1):
        s.rect(dx - h, dy + (sgn * h if sgn > 0 else -h - K * DEPOT_WRAP),
               K * DEPOT_WRAP, K * DEPOT_WRAP, fill=DEPOT, stroke=CRAG_EDGE, sw=1.3)
    # shelves above: dark dashes, readable over the grey DEPOT
    s.rect(dx - h - K * SHELF_DEPTH, dy - h, K * SHELF_DEPTH, K * CRAG_S,
           fill="none", stroke=INK, sw=1.3, dash="6 3")
    s.rect(dx - h, dy - h, 2 * h, 2 * h, fill=CRAG_BODY, stroke=CRAG_EDGE, sw=2.0)
    s.rect(dx - K * SPIRE_S / 2, dy - K * SPIRE_S / 2, K * SPIRE_S, K * SPIRE_S,
           fill=CRAG_SPIRE, stroke=CRAG_EDGE, sw=1.6)
    rs = K * SOCK_OD / 2
    for sgn in (-1, 1):
        for lat, nm in ((-SOCK_LAT, "LOW"), (SOCK_LAT, "MID")):
            pxx = dx + K * lat
            pyy = dy + sgn * (h + K * SOCK_STANDOFF)
            s.circle(pxx, pyy, rs, fill=SOCKET_L, stroke=BLUE_D, sw=1.5)
            s.text(pxx, pyy + (rs + 1.5 + 0.72 * L if sgn > 0 else -rs - 1.5), nm, size=L,
                   fill=INK, anchor="middle", halo=True)
    s.circle(dx - h - K * SOCK_STANDOFF, dy, rs, fill=SOCKET_L, stroke=BLUE_D, sw=1.8)
    s.leader(dx - h - K * SOCK_STANDOFF - rs, dy, dx - h - K * DEPOT_CH - 26, dy - 30,
             "SUMMIT socket", anchor="end")
    for sgn in (-1, 1):
        s.line(dx + h, dy + sgn * K * PEG_LAT, dx + h + K * PEG_EXP * 0.7071,
               dy + sgn * K * PEG_LAT, stroke="#666666", sw=4, cap="round")
        s.line(dx + K * SPIRE_S / 2, dy + sgn * K * HPEG_LAT,
               dx + K * SPIRE_S / 2 + K * PEG_EXP * 0.7071, dy + sgn * K * HPEG_LAT,
               stroke="#666666", sw=4, cap="round", dash="4 3")
    dep_b = dy + h + K * DEPOT_WRAP              # outer edge of the DEPOT leg
    s.dim_h(dx - h - K * DEPOT_CH, dx - h, dep_b + 20, "16.0", ext_from=dep_b + 3,
            critical=True)
    s.dim_h(dx - h, dx + h, dep_b + 20 + 1.32 * s.DIM + 18, "48.0", ext_from=dy + h + 3,
            critical=True)
    s.dim_v(dy - h - K * SOCK_STANDOFF, dy - h, dx + K * SOCK_LAT + 40, "8.0",
            ext_from=dx + K * SOCK_LAT + rs + 3, critical=True, side="right")
    s.dim_v(dy - h, dy + h, dx + h + 104, "48.0", ext_from=dx + h + 3, critical=True,
            side="right")
    _notes(s, 1500, NY, [
        "BASE DEPOT: channel 16.0 from the shelf face, wrapping 16.0 onto",
        "each socket face. Lip 4.0 tall, top edge R0.25 (Detail D4).",
        "Shelves overhang 14.0 and span only the 48-in face, so the outer 2.0",
        "of the shelf-face leg and both 16 x 16 corner SQUARES are open from above.",
        "The two corner ARMS are overhung by their Low Socket tubes: push, do not drop.",
        "Dashed rectangle = shelves above.",
    ], title="VIEW D NOTES", w=s.w - 16 - 1500)

    # ===================== ROW 2 DETAILS =====================
    R2 = 30.0                    # row-2 shift below the row-1 notes
    s.line(40, 650, 1920, 650, stroke=RULE, sw=1.0)
    VY2 = 664 + R2
    DNY = 1024 + R2 + 16         # detail-note baseline
    E = 9.0

    # ---- D1 socket section ----
    DD = 36.0                    # D1-D3 sections sit a little lower than their titles
    d1x, d1y = 250.0, 806.0 + R2 + DD
    s.view_label(d1x, VY2, "D1 - SOCKET SECTION", "9.0 px/in", "typical of all four side sockets")
    s.line(d1x - 120, d1y - 90, d1x - 120, d1y + 190, stroke=CRAG_EDGE, sw=3)
    s.text(d1x - 128, d1y + 80, "CRAG face plane", size=L, fill=INK, anchor="middle", rot=-90)
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
    s.ellipse(rimx, rimy, E * SOCK_ID / 2, E * SOCK_ID / 6, fill="none", stroke=BLUE_D,
              sw=1.2, rot=SOCK_TILT)
    # tilt: vertical through the rim centre vs the tube axis, measured below the tube
    ta = math.radians(SOCK_TILT)
    bot = (rimx - E * SOCK_TUBE * math.sin(ta), rimy + E * SOCK_TUBE * math.cos(ta))
    s.line(rimx, rimy - 16, rimx, rimy + 100, stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.line(bot[0], bot[1], rimx - 100 * math.sin(ta), rimy + 100 * math.cos(ta),
           stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.angle(rimx, rimy, 88, 90, 90 + SOCK_TILT, "30 deg", lx=rimx + 7, ly=rimy + 96,
            anchor="start")
    # standoff, below the section
    s.dim_h(d1x - 120, rimx, rimy + 150, "8.0", ext_from=rimy + 104, critical=True)
    # ID across the rim, carried out past the protruding CELL on extension lines
    ends = ((rimx - E * SOCK_ID / 2 * math.cos(ta), rimy + E * SOCK_ID / 2 * math.sin(ta)),
            (rimx + E * SOCK_ID / 2 * math.cos(ta), rimy - E * SOCK_ID / 2 * math.sin(ta)))
    s.dim_a(ends[0], ends[1], "ID 6.50 +/- 0.125", off=-70, critical=True, shift=92)
    s.leader(rimx - E * 2.2 * math.cos(ta) + 20, rimy - 40, rimx + 90, rimy - 30,
             "seated O2 CELL (dashed)", fill=GHOST_T)
    _notes(s, 60, DNY, [
        "Rim ctr Z = 30.0 (Low) / 54.0 (Mid). Standoff 8.0 normal to the face.",
        "Tube 7.0 along the axis, closed bottom, wall 0.09 (ref).",
        "Tilt 30 deg from vertical, tilting OUTWARD, open end up.",
        "Floor center lands 4.50 out from the face; inboard edge 1.56 out,",
        "so nothing enters the tower and no relief pocket is needed.",
        "A seated 14.0 O2 CELL protrudes 7.0 along the axis and stands",
        "4.39 above the rim's uphill lip - the SCORED call is a glance.",
        "The attachment lives in the wedge under the tube and may not break",
        "the rim plane (geometry otherwise free, ref).",
    ], title="D1 NOTES", w=COLW)

    # ---- D2 summit socket ----
    d2x, d2y = 700.0, 806.0 + R2 + DD
    s.view_label(d2x, VY2, "D2 - SUMMIT SOCKET", "9.0 px/in", "on the SHELF FACE, on the crag centerline")
    s.line(d2x + 90, d2y - 90, d2x + 90, d2y + 190, stroke=CRAG_EDGE, sw=3)
    rx2, ry2 = d2x + 90 - E * SOCK_STANDOFF, d2y
    s.add('<g transform="rotate(%g %.2f %.2f)">' % (-SUM_TILT, rx2, ry2))
    s.rect(rx2 - E * SOCK_OD / 2, ry2, E * SOCK_OD, E * SOCK_TUBE, fill=SOCKET,
           stroke=BLUE_D, sw=2.0)
    s.rect(rx2 - E * CELL_D / 2, ry2 + E * SOCK_TUBE - E * CELL_L, E * CELL_D, E * CELL_L,
           fill="none", stroke=GHOST, sw=2.0, rx=E * 1.5, dash="5 3")
    s.add('</g>')
    s.ellipse(rx2, ry2, E * SOCK_OD / 2, E * SOCK_OD / 6, fill=SOCKET_L, stroke=BLUE_D,
              sw=2.0, rot=-SUM_TILT)
    tb = math.radians(SUM_TILT)
    bot2 = (rx2 + E * SOCK_TUBE * math.sin(tb), ry2 + E * SOCK_TUBE * math.cos(tb))
    s.line(rx2, ry2 - 16, rx2, ry2 + 100, stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.line(bot2[0], bot2[1], rx2 + 100 * math.sin(tb), ry2 + 100 * math.cos(tb),
           stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.angle(rx2, ry2, 88, 90, 90 - SUM_TILT, "15 deg", lx=rx2 - 7, ly=ry2 + 96, anchor="end")
    s.dim_h(rx2, d2x + 90, ry2 + 150, "8.0", ext_from=ry2 + 104, critical=True)
    # tower top plate at Z = 60.0, 12.0 below the rim centre at this scale
    plate = ry2 + E * (SUM_SOCK_Z - BODY_H)
    s.rect(d2x + 90, plate, 130, 24, fill=CRAG_BODY, stroke=CRAG_EDGE, sw=1.6)
    s.text(d2x + 96, plate + 12 + 0.36 * L, "tower top plate Z = 60.0", size=L, fill=INK)
    s.text(d2x + 98, d2y - 90 + 0.74 * L, "SHELF FACE plane", size=L, fill=INK)
    s.leader(rx2 - 12, ry2 - 52, rx2 - 96, ry2 - 72, "seated O2 CELL (dashed)", anchor="end",
             fill=GHOST_T)
    _notes(s, 520, DNY, [
        "Rim ctr Z = 72.0, on the crag centerline, 8.0 OUT from the SHELF FACE.",
        "Tube 7.0 along the axis at 15 deg from vertical, tilting outward.",
        "Floor center 6.19 out from the face at Z = 65.24; inboard edge 2.94",
        "out - free air outboard of the tower, no pocket required.",
        "A crowned CRATE on Shelf 2 tops out at Z = 55.0; the tube bottom is",
        "Z = 64.29 - 9.29 clear.",
        "The MAST stands over Shelf 2's CENTER slot from Z = 60: only 5.0",
        "overhead, so that slot is loaded from the front. The two outer slots",
        "stay open to the sky.",
        "A seated CELL's apex reaches Z = 78.76, leaning toward the owning",
        "alliance's driver stations.",
        "THERE IS NO SPIRE RECESS - the spire is a clean 20 x 20 prism.",
        "Reach: a ROBOT at the DEPOT lip has its FRAME PERIMETER 19.75 from",
        "the face, so the rim is 11.75 of extension - inside the 18 in limit.",
    ], title="D2 NOTES", w=COLW + 40)

    # ---- D3 peg + coil ----
    d3x, d3y = 1150.0, 830.0 + R2 + DD
    F = 10.0
    s.view_label(d3x, VY2, "D3 - PEG AND COIL REST POSE", "10.0 px/in",
                 "the geometry every hook and spear is designed against")
    s.line(d3x - 130, d3y - 120, d3x - 130, d3y + 110, stroke=CRAG_EDGE, sw=3)
    s.text(d3x - 138, d3y + 100, "face", size=L, fill=INK, anchor="end")
    root = (d3x - 130, d3y + 20)
    tip = (root[0] + F * PEG_EXP * 0.7071, root[1] - F * PEG_EXP * 0.7071)
    s.add('<g transform="rotate(-45 %.2f %.2f)">' % root)
    s.rect(root[0], root[1] - F * PEG_OD / 2, F * PEG_EXP, F * PEG_OD, fill="#999999",
           stroke="#333333", sw=1.6, rx=F * PEG_OD / 2)
    s.add('</g>')
    s.line(root[0], root[1], root[0] + 66, root[1], stroke=MUTED, sw=0.9, dash="6 3")
    s.angle(root[0], root[1], 36, 0, -45, "45 deg", lx=root[0] + 72, ly=root[1] + 0.36 * s.DIM,
            anchor="start")
    # exposed length: dimension line clear of both COIL poses, value carried out past the tip
    s.dim_a(root, tip, "10.0 exposed", off=90, critical=True, shift=112)
    s.circle(root[0] + 12, root[1] - 10, F * COIL_OD / 2, fill="none", stroke=GHOST, sw=2.2)
    s.circle(root[0] + 12, root[1] - 10, F * COIL_ID / 2, fill="none", stroke=GHOST, sw=1.4)
    s.text(root[0] - 10, root[1] - 74, "REST POSE A", size=L, fill=GHOST_T, anchor="end")
    s.add('<g transform="rotate(-45 %.2f %.2f)">' % (root[0] + 74, root[1] - 74))
    s.ellipse(root[0] + 74, root[1] - 74, F * COIL_TUBE / 2, F * COIL_OD / 2, fill="none",
              stroke=MUTED, sw=1.4)
    s.add('</g>')
    s.text(root[0] + 118, root[1] - 106, "REST POSE B", size=L, fill=INK)
    _notes(s, 1010, DNY, [
        "Peg OD 1.5 (CRITICAL), 45 deg up from the face, 10.0 exposed, tip R0.75.",
        "Root heights Z = 30 / 54 / 78; roots +/-14.0 (low, mid) and +/-7.0 (high).",
        "POSE A (settled): the COIL hangs near-vertical in a plane parallel to",
        "the face and wedges on the peg. A 5.0 hole over a 1.5 peg permits at",
        "most about 48 deg (47.9) of tilt (2.5 tan t + 1.5 / cos t <= 5.0);",
        "a vertical hang needs 45 deg, so a SCORED COIL is captured, not balanced.",
        "The coil center rests about 1 in above the peg root, its inner face",
        "about 1.25 in outboard of the crag face.",
        "POSE B (as dropped, dashed): perpendicular to the peg; it settles to A.",
    ], title="D3 NOTES", w=COLW + 30)

    # ---- D4 shelf + depot ----
    d4x, d4y = 1700.0, 730.0 + R2
    G = 6.2
    s.view_label(d4x - 120, VY2, "D4 - SHELF AND DEPOT SECTION", "6.2 px/in",
                 "section normal to the SHELF FACE")
    base = d4y + 300

    def zz4(v):
        return base - G * v
    s.line(d4x - 250, base, d4x + 40, base, stroke=INK, sw=2.0)
    s.line(d4x, zz4(0), d4x, zz4(50), stroke=CRAG_EDGE, sw=3)
    s.text(d4x + 6, zz4(48) + 0.36 * L, "SHELF FACE", size=L, fill=INK)
    s.text(d4x - G * SHELF_DEPTH - 6, zz4(SHELF1) + 0.36 * L, "Shelf 1", size=L, fill=INK, anchor="end")
    s.text(d4x - G * SHELF_DEPTH - 6, zz4(SHELF2) + 0.36 * L, "Shelf 2", size=L, fill=INK, anchor="end")
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
    ccx = d4x - G * (SHELF_DEPTH - 1) + G * CRATE_S / 2
    s.lines(ccx, zz4(SHELF1 + CRATE_S / 2) - 0.25 * L, ["CRATE", "on Shelf 1"], size=L,
            fill=GHOST_T, anchor="middle", pitch=1.2 * L)
    s.rect(d4x - G * (DEPOT_CH + LIP_THK), zz4(DEPOT_LIP), G * LIP_THK, G * DEPOT_LIP,
           fill=DEPOT, stroke=CRAG_EDGE, sw=1.3)
    s.rect(d4x - G * DEPOT_CH, zz4(0.25), G * DEPOT_CH, G * 0.25, fill=DEPOT,
           stroke=CRAG_EDGE, sw=1.0)
    s.rect(d4x - G * (DEPOT_CH - 1), zz4(0.25 + 13.0), G * CRATE_S, G * 13.0,
           fill=CRATE, stroke=CRATE_D, sw=1.4, rx=G * 0.8, op=0.55)
    s.text(d4x - 6, zz4(13.25) - 6, "CRATE in the DEPOT", size=L, fill=CRATE_D, anchor="end")
    # crowned height: on the open side of the face, so it clears the lip dimension
    s.dim_v(zz4(0.25 + 13.0), zz4(0.25), d4x + 22, "13.0 crowned",
            ext_from=d4x - G * (DEPOT_CH - 1 - CRATE_S) + 2, side="right", tick=6)
    s.dim_h(d4x - G * SHELF_DEPTH, d4x, zz4(SHELF2) - 24, "14.0", ext_from=zz4(SHELF2) - 6,
            critical=True)
    s.dim_h(d4x - G * DEPOT_CH, d4x, base + 40, "16.0", ext_from=base + 4, critical=True)
    s.dim_v(zz4(DEPOT_LIP), base, d4x - G * (DEPOT_CH + LIP_THK) - 24, "4.0",
            ext_from=d4x - G * (DEPOT_CH + LIP_THK) - 4, critical=True)
    s.dim_v(zz4(SHELF1), base, d4x + 66, "24.0", ext_from=d4x + 4, critical=True, side="right")
    s.dim_v(zz4(SHELF2), base, d4x + 106, "42.0", ext_from=d4x + 4, critical=True, side="right")
    _notes(s, 1500, base + 40 + 1.32 * s.DIM + 30, [
        "Lip 4.0 tall, top edge R0.25; lip thickness 0.75 (ref);",
        "tray floor 0.25 with a 45 deg entry chamfer (ref).",
        "The floor top is at Z = 0.25, so a crowned CRATE apexes at 13.25 -",
        "only 0.19 below the CRAG tag target at 13.44. See VISION-GUIDE 1.3.",
        "A CRATE stands proud of the lip and is SCORED so long as the tray",
        "floor alone supports it.",
        "Robot standoff: bumper face 16.75 from the crag face,",
        "FRAME PERIMETER 19.75; a shelf slot center is 12.75 of extension.",
    ], title="D4 NOTES", w=s.w - 16 - 1500)

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
    L, N, H = s.LABEL, s.NOTE, s.HEAD

    def z(v):
        return GY - K * v

    def stag(lane_i, rung_i):
        # The stagger alternates by RUNG, never by lane. Alternating the sign per
        # lane would put adjacent lanes' rungs 24 in apart center-to-center,
        # closer than two hanging ROBOTS are wide. lane_i is therefore unused.
        return (-1, 1, -1)[rung_i] * RUNG_STAG

    # ---------- FRONT ELEVATION ----------
    fx0 = 90.0

    def fy_(Y):
        return fx0 + K * (Y - 90.0)

    s.view_label(fx0 + K * HW_W / 2, 92, "FRONT ELEVATION", "3.4 px/in",
                 "viewed from the FIELD, projected onto the vertical plane")
    s.line(50, GY, fx0 + K * HW_W + 60, GY, stroke=INK, sw=2.0)
    s.text(18, GY + 4 + 0.74 * s.SUB, "carpet Z = 0", size=s.SUB, fill=MUTED)
    s.rect(fx0, z(TRUSS_TOP), K * HW_W, K * TRUSS_TOP, fill="#EFE7D8", stroke=TRUSS_D, sw=2.4)
    for yb in (138.0, 186.0):
        s.line(fy_(yb), z(TRUSS_TOP), fy_(yb), GY, stroke=TRUSS_D, sw=1.6, dash="8 5")
    for i, ly in enumerate(LANE_Y):
        s.text(fy_(ly), z(TRUSS_TOP) - 8, "LANE %d (Y %d-%d)" % (i + 1, ly - 24, ly + 24),
               size=L, fill=INK, anchor="middle")
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
        s.text(fx0 + K * HW_W + 12, z(top) + 0.36 * L, lbl, size=L, fill=INK)
    s.text(fx0 + K * HW_W + 12, z(84.0) + 0.36 * s.DIM, "84.0 truss top (ref)", size=s.DIM, fill=DIM)
    l2 = LANE_Y[1]
    s.dim_h(fy_(l2), fy_(l2 + stag(1, 0)), z(30) + 34, "12.0", ext_from=z(30) + 6,
            critical=True)
    s.dim_h(fy_(l2 + stag(1, 1)), fy_(l2), z(54) + 34, "12.0", ext_from=z(54) + 6,
            critical=True)
    # rung length: the value is longer than the rung, so it hangs below its line,
    # slid clear of the truss edge
    s.dim_h(fy_(LANE_Y[0] + stag(0, 0) - RUNG_L / 2), fy_(LANE_Y[0] + stag(0, 0) + RUNG_L / 2),
            z(78) + 28, "20.0 rung length", ext_from=z(78) + 8, critical=True, above=False,
            tick=3, shift=14)
    # the lane dimension sits nearer the part than the overall one
    s.dim_h(fx0, fy_(138.0), GY + 34, "48.0", ext_from=GY + 4, critical=True)
    s.dim_h(fx0, fx0 + K * HW_W, GY + 70, "144.0 (three 48.0-in lanes)", ext_from=GY + 4,
            critical=True)
    lx = 66
    for v, lbl in ((30.0, "30.0"), (54.0, "54.0"), (78.0, "78.0")):
        s.line(fx0 - 6, z(v), lx + 6, z(v), stroke=DIM, sw=s.SW_EXT)
        s.text(lx - 2, z(v) + 0.36 * s.DIM, lbl, size=s.DIM, fill=DIM, anchor="end")
    s.line(fx0 - 6, z(84.0), lx + 6, z(84.0), stroke=DIM, sw=s.SW_EXT)
    s.arrow(lx + 10, GY, lx + 10, z(TRUSS_TOP), stroke=DIM, start=True, end=True)
    cx_ = fx0 + K * HW_W / 2
    yy = s.lines(cx_, GY + 104, [
        "Stagger from the lane centerline is the same in every lane: LEDGE -12.0, CAMP +12.0, SUMMIT -12.0.",
        "The sign alternates by rung, never by lane. Red = 180 deg rotation about (324, 162).",
        "AprilTags 3 / 4 / 5 sit on the lane centerlines, ctr Z = 12.0 (side profile)."],
        size=N, fill=INK, anchor="middle")
    s.lines(cx_, yy, [
        "A 20.0-in rung at +/-12.0 leaves NO lateral position that engages two successive rungs:",
        "LEDGE spans -22 to -2, CAMP spans +2 to +22."], size=N, fill=DIM, anchor="middle")

    # ---------- SIDE PROFILE ----------
    px0 = 660.0

    def sx(X):
        return px0 + K * (100.0 - X)

    s.view_label(sx(50), 92, "SIDE PROFILE - PLANE P", "3.4 px/in",
                 "field LEFT, alliance wall RIGHT")
    s.line(sx(110), GY, sx(-4), GY, stroke=INK, sw=2.0)
    s.rect(sx(0), z(78.0), 10, K * 78.0, fill=WALL, stroke=WALL_D, sw=1.6)
    s.text(sx(0) + 22, z(40), "ALLIANCE WALL (78 ref)", size=L, fill=WALL_D, rot=-90)
    s.line(sx(HW_X), GY, sx(HW_X - TRUSS_TOP * T15), z(TRUSS_TOP), stroke=BLUE_D, sw=2.4)
    pz = 66.0                                      # PLANE P name, set along the plane
    s.text(sx(HW_X - pz * T15) - 10, z(pz), "PLANE P", size=L + 0.5, fill=BLUE_D,
           weight="bold", anchor="middle", rot=-75)
    s.line(sx(HW_X), GY, sx(HW_X), z(TRUSS_TOP + 4), stroke=MUTED, sw=0.9, dash="12 4 3 4")
    s.line(sx(truss_face_x(0)), GY, sx(truss_face_x(TRUSS_TOP)), z(TRUSS_TOP),
           stroke=TRUSS, sw=5, cap="round")
    for lbl, top in (("LEDGE", 30.0), ("CAMP", 54.0), ("SUMMIT", 78.0)):
        cxx = rung_center_x(top)
        s.circle(sx(cxx), z(top - RUNG_OD / 2), 5.5, fill="#444444", stroke="#222222", sw=1.0)
        s.text(sx(cxx) - 12, z(top - RUNG_OD / 2) + 0.36 * L, lbl, size=L, fill=INK, anchor="end",
               halo=True)
    s.rect(sx(TAG_HW_X) - 3, z(TAG_Z_HW + TAG_PANEL / 2), 6, K * TAG_PANEL,
           fill="#111111", stroke="#666666", sw=0.8)
    s.rect(sx(HW_X), GY - 7, K * HW_X, 7, fill=BLUE, stroke=BLUE_D, sw=0.8, op=0.55)
    s.line(sx(0), z(42), sx(30.5), z(42), stroke=GHOST, sw=1.6, dash="6 4")
    # callouts live on the open field side, left of the plane, with leaders in
    fl = sx(HW_X) - 10                             # right edge of the field-side label column
    s.leader(sx(truss_face_x(84)) + 1, z(84) - 3.5, fl - 40, z(96), "truss structure, all >= 4.0 behind P",
             anchor="end", fill=TRUSS_D)
    s.lines(fl, z(42) - 8, ["42-in STARTING CONFIGURATION", "fits up to X = 30.5"],
            size=L, fill=GHOST_T, anchor="end", pitch=1.2 * L)
    s.leader(sx(26.0), z(42), fl + 3, z(42) - 8 - 0.34 * L, "", fill=GHOST_T)
    s.angle(sx(HW_X), GY, 74, -90, -75, "15 deg from vertical", lx=fl, ly=GY - 74 + 0.36 * s.DIM,
            anchor="end")
    ty_ = z(TAG_Z_HW) - 8
    s.lines(fl, ty_, ["tag panel PLUMB, face plane X = 39.0,", "ctr Z = 12.0"],
            size=L, fill=INK, anchor="end", pitch=1.2 * L)
    s.text(fl, ty_ + 2.4 * L, "4.42 in behind P at the panel top edge", size=N, fill=MUTED,
           anchor="end")
    s.leader(sx(TAG_HW_X) - 3, z(TAG_Z_HW), fl + 3, ty_ - 0.34 * L, "")
    s.dim_h(sx(HW_X), sx(0), GY + 34, "48.0", ext_from=GY + 4, critical=True)
    s.lines(sx(24), GY + 34 + 4 + 0.74 * L, ["BASECAMP / HEADWALL ZONE", "(X 0-48)"], size=L,
            fill=BLUE_D, anchor="middle", pitch=1.2 * L)

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
    s.text(tx(HW_X) - 4, ty(90) - 6, "P carpet line X = 48", size=L, fill=BLUE_D, anchor="end")
    for yb in (90.0, 138.0, 186.0, 234.0):
        s.line(tx(60), ty(yb), tx(0), ty(yb), stroke=TRUSS_D, sw=1.2,
               dash=None if yb in (90.0, 234.0) else "6 4")
    for li, ly in enumerate(LANE_Y):
        for ri, top in enumerate(RUNG_TOP):
            c = ly + stag(li, ri)
            cxx = rung_center_x(top)
            s.line(tx(cxx), ty(c - RUNG_L / 2), tx(cxx), ty(c + RUNG_L / 2),
                   stroke="#444444", sw=3.4, cap="round", op=0.9)
    # LEDGE and SUMMIT beside their tick lines, CAMP below, so no tick crosses a name
    for lbl, top, row, anc, dx_ in (("LEDGE", 30.0, 1, "end", -3), ("CAMP", 54.0, 2, "middle", 0),
                                    ("SUMMIT", 78.0, 1, "start", 3)):
        xr = tx(rung_center_x(top))
        lyy = ty(234) + 6 + row * 1.25 * L
        s.line(xr, ty(234) + 4, xr, lyy - (0.8 * L if row == 2 else 0.35 * L), stroke=MUTED, sw=0.6)
        s.text(xr + dx_, lyy, lbl, size=L, fill=INK, anchor=anc)
    s.dim_v(ty(90), ty(234), tx(0) - 30, "144.0", ext_from=tx(0) - 8, side="right")
    s.lines(tx0 + 66, ty(234) + 6 + 4 * 1.25 * L + 6, ["rungs step toward the wall",
                                                       "with height (15 deg lean)"],
            size=N, fill=MUTED, anchor="middle")

    # ---------- RUNG DETAIL ----------
    rx0, ry0 = 1400.0, 190.0
    R = 9.0
    s.view_label(rx0 + 100, 92, "RUNG DETAIL", "9.0 px/in", "section normal to plane P")
    px_ = rx0 + 60                                 # plane P
    s.line(px_, ry0, px_, ry0 + 190, stroke=BLUE_D, sw=2.0, dash="10 4")
    s.text(px_ - 8, ry0 + 150, "plane P", size=L, fill=BLUE_D, anchor="middle", rot=-90)
    s.circle(px_, ry0 + 90, R * RUNG_OD / 2, fill="#444444", stroke="#222222", sw=1.2)
    # OD above the hook; the value sits outside its short span, off plane P
    s.dim_h(px_ - R * RUNG_OD / 2, px_ + R * RUNG_OD / 2, ry0 + 30,
            "OD 1.5", ext_from=ry0 + 90 - R * RUNG_OD / 2 - 3, critical=True, shift=-30)
    s.rect(px_ + R * TRUSS_CLR, ry0, R * 2.0, 190, fill="#EFE7D8", stroke=TRUSS_D, sw=1.6)
    s.text(px_ + R * TRUSS_CLR + R, ry0 - 6, "truss chord 2 x 2 (ref)", size=L, fill=INK,
           anchor="middle")
    s.dim_h(px_, px_ + R * TRUSS_CLR, ry0 + 152, "4.0", ext_from=ry0 + 132, critical=True)
    s.path("M %.1f %.1f q 34 -2 34 28 q 0 24 -24 24" % (rx0 + 34, ry0 + 60),
           stroke=GHOST, sw=2.0, dash="5 3")
    s.leader(rx0 + 30, ry0 + 64, rx0 + 6, ry0 + 100, "climber hook wrap", anchor="end",
             fill=GHOST_T)
    s.lines(rx0 + 100, ry0 + 190 + 8 + 0.74 * N, [
        "structure >= 4.0 behind P except the end brackets -",
        "clear wrap over the middle 16.0 of 20.0"], size=N, fill=INK, anchor="middle")

    # ---------- TABLES ----------
    top = GY + 104 + 5 * s.PITCH * N + 8
    pitch = 1.45 * N
    y0 = top + 8 + 0.74 * H
    bx = 90
    pw = 760
    hdr = ("Rung", "Top Z", "Ctr Z", "Ctr X", "Lane-1 Y span", "Lane-2 Y span", "Lane-3 Y span")
    colx = [bx + 8, bx + 84, bx + 150, bx + 216, bx + 290, bx + 440, bx + 590]
    cells = [("0", "156.0"), ("12", "111.2"), ("24", "66.4"), ("30.5", "42.1"), ("32.6", "34.3"),
             ("34.2-38.6", "10.8"), ("40", "6.7"), ("41.79", "0.0")]
    rows_d = y0 + 0.5 * H + pitch                      # header row baseline
    body = rows_d + 3 * pitch
    notes_d = ["Rung ctr Z = top - 0.75. Blue rung ctr X = 48 - Z x tan 15. Setback between successive rungs = 24 x tan 15 = 6.43 in.",
               "Every rung sits at least 2.0 in inside its lane boundary; adjacent lanes are 48.0 apart center-to-center, 28.0 end to end."]
    cv = body + 0.4 * N + 2 * 1.25 * N + 1.4 * H       # clear-volume heading baseline
    xrow = cv + 1.2 * pitch
    foot = xrow + pitch + 0.3 * N
    # CLIMB REACH rows, computed first so both panels share one height
    cl0 = y0 + 0.5 * H + pitch
    hy = cl0 + 5 * 1.25 * N + 0.6 * N
    cl3 = hy + 4 * pitch + 0.3 * N
    park = cl3 + 3 * 1.25 * N + 0.1 * N
    ph = max(foot + 1.25 * N, park) + 0.8 * N - top
    s.rect(bx, top, pw, ph, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(bx + 8, y0, "DERIVED (do NOT drive these - dimension plane P and the vertical heights; let CAD compute)",
           size=H, fill=ACCENT, weight="bold")
    for cxx, cell in zip(colx, hdr):
        s.text(cxx, rows_d, cell, size=N, fill=ACCENT, weight="bold")
    s.line(bx + 6, rows_d + 0.45 * N, bx + pw - 8, rows_d + 0.45 * N, stroke=RULE, sw=0.8)
    for ri, (nm, topz) in enumerate((("LEDGE", 30.0), ("CAMP", 54.0), ("SUMMIT", 78.0))):
        zc = topz - RUNG_OD / 2
        row = [nm, "%.1f" % topz, "%.2f" % zc, "%.2f" % rung_center_x(topz)]
        for li, ly in enumerate(LANE_Y):
            c = ly + stag(li, ri)
            row.append("%.0f - %.0f" % (c - RUNG_L / 2, c + RUNG_L / 2))
        for cxx, cell in zip(colx, row):
            s.text(cxx, rows_d + (ri + 1) * pitch, cell, size=N, fill=INK)
    s.lines(bx + 8, body + 0.4 * N + 1.25 * N, notes_d, size=N, fill=MUTED, pitch=1.25 * N)
    s.text(bx + 8, cv, "BASECAMP CLEAR VOLUME:  H(X) = 3.7321 x (41.788 - X) inches, "
           "except 10.8 under the lower crossbeam (X 34.2-38.6)", size=H, fill=ACCENT, weight="bold")
    s.text(bx + 8, xrow, "X (in)", size=N, fill=ACCENT, weight="bold")
    s.text(bx + 8, xrow + pitch, "H (in)", size=N, fill=ACCENT, weight="bold")
    for i, (xv, hv) in enumerate(cells):
        cx0 = bx + 72 + i * 82
        s.text(cx0, xrow, xv, size=N, fill=INK)
        s.text(cx0, xrow + pitch, hv, size=N, fill=INK, weight="bold" if hv == "42.1" else None)
    s.text(bx + 8, foot + 1.25 * N,
           "A 42-in STARTING CONFIGURATION fits anywhere up to X = 30.5, which is why G302 stages ROBOTS against the alliance wall.",
           size=N, fill=MUTED)

    cx2 = bx + pw + 30
    pw2 = s.w - 20 - cx2
    s.rect(cx2, top, pw2, ph, fill="#FFFFFF", stroke=RULE, sw=0.9)
    s.text(cx2 + 8, y0, "CLIMB REACH (the arithmetic behind G416)", size=H, fill=ACCENT, weight="bold")
    s.lines(cx2 + 8, cl0, [
        "G416: no rung contact while any BUMPER is on the wall side of the CLIMB LINE (X = 48 Blue / 600 Red),",
        "unless the ROBOT is then supported solely by rungs, or is still touching a rung it took hold of while",
        "so supported within the preceding 5 s.",
        "The nearest bumper face is X = 48, so the FRAME PERIMETER is at X = 51 (R402: 0.75 backing + 2.25 foam)",
        "and an 18-in reach (R105) ends at X = 33.0."], size=N, fill=INK, pitch=1.25 * N)
    hdr2 = ("Rung", "Rung ctr X", "To centerline", "To wrap the rung", "Within R105 (18 in)?")
    colx2 = [cx2 + 8, cx2 + 90, cx2 + 190, cx2 + 310, cx2 + 450]
    for cxx, cell in zip(colx2, hdr2):
        s.text(cxx, hy, cell, size=N, fill=ACCENT, weight="bold")
    s.line(cx2 + 6, hy + 0.45 * N, cx2 + pw2 - 8, hy + 0.45 * N, stroke=RULE, sw=0.8)
    for i, (nm, topz) in enumerate((("LEDGE", 30.0), ("CAMP", 54.0), ("SUMMIT", 78.0))):
        cxx_ = rung_center_x(topz)
        ext = 51.0 - cxx_
        wrap = ext + RUNG_OD / 2.0          # a hook has to reach past the far face of the rung
        ok = "yes" if wrap <= 18.0 else "NO - from a hang only"
        for cX, cell in zip(colx2, (nm, "%.2f" % cxx_, "%.2f in" % ext,
                                    "%.2f in" % wrap, ok)):
            s.text(cX, hy + (i + 1) * pitch, cell, size=N,
                   fill=DIM if ext > 18 else INK, weight="bold" if ext > 18 else None)
    s.lines(cx2 + 8, cl3, [
        "From a hang on the LEDGE RUNG the CAMP RUNG is 6.43 in back, 24 in up, 24 in across (24.9 in plane P);",
        "the same step again reaches SUMMIT. LEDGE and SUMMIT share -12.0, so a direct LEDGE-SUMMIT",
        "reach (48 up, 12.86 back, 49.7 in plane P) is legal too - twice the reach, no traverse. Both count."],
        size=N, fill=MUTED, pitch=1.25 * N)
    s.text(cx2 + 8, park,
           "PARK 3 / LEDGE RUNG 12 / CAMP RUNG 20 / SUMMIT RUNG 30. Protection runs from the start of ENDGAME through climb assessment.",
           size=N, fill=INK)
    assert top + ph <= s.tb_top - 6, "headwall panels run into the title block"
    for t in notes_d:
        assert s.tw(t, N) < pw - 16, t[:30]

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
        "Slot centers -15.5 / 0 / +15.5; neighbors clear each other by 2.5.",
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
