# -*- coding: utf-8 -*-
"""
Independent check: SCREE, the 18 SCREE PATCHES of half-round ridges on the carpet (both halves).

Expected values come from the package documents only (never from src/20_ledger.fs or the part code):

  DESIGN-SPEC §3 SCREE /  SCREE PATCH: 30.0 x 30.0 square footprint (CRITICAL), sides parallel to the
  FIELD-CAD-PACKAGE §1.4  field axes, directly on the carpet with no base plate.  Four ridges per patch,
                          each a half-round of radius 1.75, so 1.75 tall (CRITICAL) and 3.5 wide at the
                          base, straight across the patch and cut square at its boundary; centerlines at
                          +/-4.0 and +/-12.0 from the patch center along the ridge normal, an 8.0 pitch
                          (CRITICAL) with 4.5 of flat carpet between ridges.  Ridge direction: "+45" =
                          direction (1, 1), "-45" = (1, -1), "Y" = the Y axis; a Red patch has the
                          direction of its Blue twin.  Patch-center table (CRITICAL), Red twin =
                          (648 - x, 324 - y); each half mirror-symmetric about Y = 162.  Layout: near
                          column X 90-120 (S1-S3), far column X 185-215 (S4-S7), inner pair X 219-249
                          (S8, S9), staging marks at X 144 between the near and far columns; passable
                          gaps 44.0 (S1-S2, S2-S3, S5-S6), 58.0 (S4-S5, S6-S7), 41.2 corner to corner
                          (S4-S8, S7-S9), 65.4-68.3 between the near and far columns; closed gaps 4.0
                          (S5-S8, S6-S9) and 22.0 from S4 / S7 to the guardrail; flat ground kept clear:
                          X 48-90 across Y 90-234 in front of the HEADWALL, a 36 x 24 pad at each staging
                          mark, each OUTFITTER LANE mouth (X 48-90), and X >= 252 up to the CRAG APRON
                          line at X = 264 (Red mirrored); non-linear: one clear straight 28-in path from
                          the BASECAMP front, centerline Y ~175 at X = 48 (upper edge Y ~189), to the far
                          (+Y) corner of the SHELF FACE approach at X = 264 (Y ~265-269), about 0.4 in to
                          spare over the 14 in each side, and every other drivable straight 28-in path
                          from an OUTFITTER LANE mouth or the BASECAMP front to the SHELF FACE or a
                          SOCKET FACE approach crosses a patch; outside every protected zone (CRAG APRONS,
                          BASECAMP / HEADWALL ZONES, OUTFITTER LANES) and the CENTER CACHE; no AprilTag
                          occluded (every tag at 12 in or higher).  HDPE half-round rod, matte, color
                          token `scree` #5C5650.  BUMPER ZONE unchanged: a bumper bottom at 2.5 clears a
                          ridge by 0.75.
  FIELD-CAD-PACKAGE §0    always-blue-origin NWU, inches, carpet top at Z = 0; Red = Blue rotated 180 deg
                          about (324, 162).
  FIELD-CAD-PACKAGE §1.1, BASECAMP / HEADWALL ZONE X 0-48, Y 90-234; OUTFITTER LANES 36 wide x 48 deep,
  §1.2, §5, §6            centred on Y 30 and 294; staging marks X 144, Y 108 / 162 / 216; CENTER CACHE
                          band X 300-348, Y 108-216; CRAG APRON 36 off the SHELF and PEG FACES, 20 off the
                          SOCKET FACES (Blue CRAG (324, 240): X 264-384, Y 196-284; Red (324, 84):
                          X 264-384, Y 40-128).
  MATERIALS-AND-COLORS    `scree` #5C5650 (checked against DESIGN-SPEC when the token is listed there).
  Manual R403             BUMPER bottom edge 1.25-2.5 in above the floor.

Every patch is checked against a reference solid built here from those numbers (a half-cylinder of
R1.75 on Z = 0 along the table direction at each offset, intersected with the 30 x 30 square prism):
the built ridge and the reference must coincide (symmetric-difference volume ~0).  All zone
coordinates are written for Blue; Red is checked with every probe rotated 180 deg about (324, 162).

Construction reading (naming only): each ridge is one body named "<A> SCREE PATCH Sn ridge k".

Reading of the non-linear paths (the package does not define the sampling): a path is the straight
segment traced by a 28-in-wide ROBOT's centerline, clear when it stays 14.0 in from every measured
30 x 30 patch square.  Starts: the BASECAMP front X = 48, Y 90-234, and each OUTFITTER LANE mouth at
X = 48 with the ROBOT inside the 36-in lane (centerline Y 26-34 / 290-298).  Ends: the SHELF FACE
approach, the APRON line X = 264 across the APRON's width (Y 196-284), and each SOCKET FACE approach,
the APRON line Y = 196 / 284 in front of the face (X 300-348).  Every 0.5 in is sampled.  The check
confirms the published corridor (centerline start Y 174-176.5, end Y 264-270, 0.4 +/- 0.1 in to spare),
that no other path from the BASECAMP front reaches the SHELF FACE approach, that a centerline at the
corridor's upper edge (Y 189) has no clear path, and that no path from an OUTFITTER LANE mouth is clear.  (The BASECAMP front also
has a path, centerline Y ~106, to the SHELF FACE end of the -Y SOCKET FACE approach, X 300-301.5, with
0.1 in to spare.  It is not drivable: a 28-in ROBOT centred on the Y = 196 line overlaps the DEPOT
chamfer, whose edge is at Y 198.25, and with the ROBOT's centre held 14 in clear of that edge (Y 184)
no path from the BASECAMP front to that face clears the patches.  The package therefore says "every
other drivable" path, and that part is not checked for SOCKET FACE ends.)
"""
import math
import os
import re

import numpy as np

import kernel_occ as K
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

# ---- document values (inches) -------------------------------------------------------------
FL, FW = 648.0, 324.0
CX, CY = 324.0, 162.0
S = 30.0                        # patch footprint (CRITICAL)
HS = S / 2
R = 1.75                        # ridge radius = height (CRITICAL)
OFFS = (-12.0, -4.0, 4.0, 12.0)  # ridge centerlines along the ridge normal
PITCH = 8.0                     # (CRITICAL)
FLAT = 4.5                      # flat carpet between adjacent ridges
DIRS = {"+45": (1.0, 1.0), "-45": (1.0, -1.0), "Y": (0.0, 1.0)}
# (patch, Blue center, ridge direction, Red center as printed in the table)
TABLE = [("S1", (105.0, 88.0), "+45", (543.0, 236.0)), ("S2", (105.0, 162.0), "Y", (543.0, 162.0)),
         ("S3", (105.0, 236.0), "-45", (543.0, 88.0)), ("S4", (200.0, 37.0), "+45", (448.0, 287.0)),
         ("S5", (200.0, 125.0), "+45", (448.0, 199.0)), ("S6", (200.0, 199.0), "-45", (448.0, 125.0)),
         ("S7", (200.0, 287.0), "-45", (448.0, 37.0)), ("S8", (234.0, 108.0), "+45", (414.0, 216.0)),
         ("S9", (234.0, 216.0), "-45", (414.0, 108.0))]
COLUMNS = {"near": ((90.0, 120.0), ("S1", "S2", "S3")), "far": ((185.0, 215.0), ("S4", "S5", "S6", "S7")),
           "inner": ((219.0, 249.0), ("S8", "S9"))}
STAGE_X, STAGE_Y = 144.0, (108.0, 162.0, 216.0)
PAD = (36.0, 24.0)              # flat pad at each staging mark
GAPS = [(("S1", "S2"), 44.0), (("S2", "S3"), 44.0), (("S5", "S6"), 44.0), (("S4", "S5"), 58.0),
        (("S6", "S7"), 58.0), (("S4", "S8"), 41.2), (("S7", "S9"), 41.2), (("S5", "S8"), 4.0), (("S6", "S9"), 4.0)]
PASSABLE = 28.0                 # a gap narrower than a 28-in robot is closed
COLUMN_GAP = (65.4, 68.3)       # between the near and far columns
GUARD_GAP = 22.0                # S4 / S7 to the guardrail
HW_FRONT = (48.0, 90.0, 90.0, 234.0)
# non-linear layout: straight 28-in robot paths (see the docstring for the reading)
HW_X, APRON_X = 48.0, 264.0
BASECAMP_Y = (90.0, 234.0)
LANE_Y, LANE_PLAY = (30.0, 294.0), 4.0          # a 28-in robot centred within a 36-in lane
SHELF_APPROACH = (196.0, 284.0)                 # X 264 across the APRON's width
SOCK_APPROACH_X, SOCK_APPROACH_Y = (300.0, 348.0), (196.0, 284.0)
PATH_HALF, PATH_STEP = 14.0, 0.5
CORRIDOR_START, CORRIDOR_END, CORRIDOR_SPARE = (174.0, 176.5), (264.0, 270.0), 0.4
EDGE_Y = 189.0                   # the corridor's upper edge
LANE_MOUTHS = ((48.0, 12.0, 90.0, 48.0), (48.0, 276.0, 90.0, 312.0))
APRON_STRIP = (252.0, 0.0, 264.0, FW)
# protected zones and the CENTER CACHE, world coordinates (both halves)
ZONES = [("BLUE BASECAMP", (0.0, 90.0, 48.0, 234.0)), ("RED BASECAMP", (600.0, 90.0, 648.0, 234.0)),
         ("BLUE OUTFITTER LANE (Y 30)", (0.0, 12.0, 48.0, 48.0)), ("BLUE OUTFITTER LANE (Y 294)", (0.0, 276.0, 48.0, 312.0)),
         ("RED OUTFITTER LANE (Y 294)", (600.0, 276.0, 648.0, 312.0)), ("RED OUTFITTER LANE (Y 30)", (600.0, 12.0, 648.0, 48.0)),
         ("BLUE CRAG APRON", (264.0, 196.0, 384.0, 284.0)), ("RED CRAG APRON", (264.0, 40.0, 384.0, 128.0)),
         ("CENTER CACHE band", (300.0, 108.0, 348.0, 216.0))]
SCREE_HEX = "#5C5650"
HDPE_DENSITY = (930.0, 970.0)   # kg/m^3, the HDPE range
BUMPER_BOTTOM_MAX = 2.5         # R403
BUMPER_CLEAR = 0.75
TAG_MIN_CENTER, TAG_PANEL = 12.0, 9.0
TOL = 1e-6
VTOL = 1e-4                     # in^3

WF = K.Frame((0, 0, 0), (1, 0, 0), (0, 0, 1))
NAME_RX = re.compile(r"^(BLUE|RED) SCREE PATCH (S\d) ridge (\d)$")


# ---- helpers ------------------------------------------------------------------------------
def rp(side, p):
    """Blue world point -> the same point on `side` (Red = 180 deg about (324, 162))."""
    return (p[0], p[1]) if side == "BLUE" else (FL - p[0], FW - p[1])


def rbox(side, x0, y0, x1, y1):
    """Blue plan box -> world plan box on `side`."""
    a, b = rp(side, (x0, y0)), rp(side, (x1, y1))
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))


def box(x0, y0, z0, x1, y1, z1):
    return BRepPrimAPI_MakeBox(gp_Pnt(x0, y0, z0), gp_Pnt(x1, y1, z1)).Shape()


def bb(shapes):
    b = K.Bnd_Box()
    K.BRepBndLib.AddOptimal_s(K._compound(shapes), b, False, False)
    return K._box6(b)


def overlaps(a, b, pad=0.0):
    return (a[0] < b[3] + pad and b[0] < a[3] + pad and a[1] < b[4] + pad and b[1] < a[4] + pad
            and a[2] < b[5] + pad and b[2] < a[5] + pad)


def cvol(a, b):
    tot = 0.0
    for x in a:
        for y in b:
            tot += K._volume(K._solids(K.BRepAlgoAPI_Common(x, y).Shape()))
    return tot


def unit(v):
    n = math.hypot(v[0], v[1])
    return (v[0] / n, v[1] / n)


def ref_ridge(c, dname, d):
    """The documented ridge: half-round R1.75 on the carpet, centerline at offset d along the ridge
    normal from patch center c, running along the table direction, cut square at the patch square."""
    ux, uy = unit(DIRS[dname])
    nx, ny = uy, -ux
    reg = K.Registry()
    K.mkCyl(reg, K.Id(("ref",)), WF, [[c[0] + d * nx, c[1] + d * ny, 0.0], [ux, uy, 0.0], [0.0, 0.0, 1.0]], [0, 0], R, -S, S)
    cyl = []
    for rec in reg.bodies.values():
        cyl += rec["solids"]
    clip = box(c[0] - HS, c[1] - HS, 0.0, c[0] + HS, c[1] + HS, R + 1.0)
    out = []
    for s in cyl:
        out += K._solids(K.BRepAlgoAPI_Common(s, clip).Shape())
    return out


def transformed(solids, trsf):
    return [K.BRepBuilderAPI_Transform(s, trsf, True).Shape() for s in solids]


def rot180():
    t = K.gp_Trsf()
    t.SetRotation(K.gp_Ax1(K.gp_Pnt(CX, CY, 0), K.gp_Dir(0, 0, 1)), math.pi)
    return t


def mirror_y():
    t = K.gp_Trsf()
    t.SetMirror(gp_Ax2(gp_Pnt(0.0, CY, 0.0), gp_Dir(0.0, 1.0, 0.0)))
    return t


def rect_gap(a, b):
    dx = max(0.0, a[0] - b[2], b[0] - a[2])
    dy = max(0.0, a[1] - b[3], b[1] - a[3])
    return math.hypot(dx, dy)


def path_clearance(A, B, rects):
    """Least plan distance from each straight segment A[i]-B[i] to the rectangles (x0, y0, x1, y1),
    0 where the segment crosses one: Liang-Barsky crossing test, otherwise the least of the end
    points to the rectangle and the rectangle corners to the segment."""
    out = np.full(len(A), np.inf)
    d = B - A
    L2 = np.maximum((d ** 2).sum(1), 1e-12)
    for x0, y0, x1, y1 in rects:
        t0, t1 = np.zeros(len(A)), np.ones(len(A))
        ok = np.ones(len(A), bool)
        for p, q in ((-d[:, 0], A[:, 0] - x0), (d[:, 0], x1 - A[:, 0]), (-d[:, 1], A[:, 1] - y0), (d[:, 1], y1 - A[:, 1])):
            zero = np.abs(p) < 1e-12
            ok &= ~(zero & (q < 0))
            t = np.where(zero, 0.0, q / np.where(zero, 1.0, p))
            t0 = np.where(~zero & (p < 0), np.maximum(t0, t), t0)
            t1 = np.where(~zero & (p > 0), np.minimum(t1, t), t1)
        crossed = ok & (t0 <= t1)

        def to_rect(P):
            return np.hypot(np.maximum(np.maximum(x0 - P[:, 0], 0), P[:, 0] - x1),
                            np.maximum(np.maximum(y0 - P[:, 1], 0), P[:, 1] - y1))
        dist = np.minimum(to_rect(A), to_rect(B))
        for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            t = np.clip(((cx - A[:, 0]) * d[:, 0] + (cy - A[:, 1]) * d[:, 1]) / L2, 0, 1)
            dist = np.minimum(dist, np.hypot(A[:, 0] + t * d[:, 0] - cx, A[:, 1] + t * d[:, 1] - cy))
        out = np.minimum(out, np.where(crossed, 0.0, dist))
    return out


def sweep(starts, ends, rects):
    """Every straight path from a start to an end: (clearance, start, end) arrays."""
    S_, E_ = np.array(starts, float), np.array(ends, float)
    A, B = np.repeat(S_, len(E_), 0), np.tile(E_, (len(S_), 1))
    return path_clearance(A, B, rects), A, B


def doc_hex(path, rx):
    try:
        with open(path, encoding="utf-8") as fh:
            m = re.search(rx, fh.read())
    except OSError:
        return None
    return m.group(1).upper() if m else None


def fmt(v):
    return "[" + ", ".join("%.4f" % x for x in v) + "]"


# ---- the check ----------------------------------------------------------------------------
def run(f):
    out = []

    def add(label, ok, detail):
        out.append((label, bool(ok), detail))

    recs = f.records()
    rbb = {r["id"]: f.bbox([r]) for r in recs}
    scree = [r for r in recs if "SCREE" in (r["name"] or "")]
    ridges = {}
    odd = []
    for r in scree:
        m = NAME_RX.match(r["name"] or "")
        if not m:
            odd.append(r["name"])
            continue
        ridges.setdefault((m.group(1), m.group(2)), []).append(r)
    add("SCREE: 18 SCREE PATCHES of four ridge bodies each (72 ridges), nothing else (no base plate)",
        not odd and len(ridges) == 18 and all(len(v) == 4 for v in ridges.values()),
        "%d patches, ridge counts %s, other SCREE bodies %s"
        % (len(ridges), sorted({len(v) for v in ridges.values()}), odd[:4] or "none"))

    # ---------- appearance and material -------------------------------------------------------
    spec_hex = doc_hex(os.path.join(PKG, "organizers", "design", "DESIGN-SPEC.md"), r"`scree`\s*=\s*`(#[0-9A-Fa-f]{6})`")
    mc_hex = doc_hex(os.path.join(PKG, "participants", "03-field", "MATERIALS-AND-COLORS.md"),
                     r"`scree`\s*\|\s*`(#[0-9A-Fa-f]{6})`")
    want_hex = spec_hex or SCREE_HEX
    add("SCREE color token `scree` %s (DESIGN-SPEC §3; MATERIALS-AND-COLORS agrees where it lists the token)" % want_hex,
        want_hex == SCREE_HEX and (mc_hex is None or mc_hex == want_hex),
        "DESIGN-SPEC %s, MATERIALS-AND-COLORS %s" % (spec_hex, mc_hex or "not listed"))
    want_rgb = tuple(int(want_hex[i:i + 2], 16) for i in (1, 3, 5))
    bad_col, bad_mat = [], []
    for r in scree:
        if tuple(r["rgb"] or ()) != want_rgb or r["alpha"] != 1:
            bad_col.append((r["name"], r["rgb"], r["alpha"]))
        m = r["mat"] or {}
        if "hdpe" not in (m.get("name") or "").lower() or not (HDPE_DENSITY[0] <= (m.get("density") or 0) <= HDPE_DENSITY[1]):
            bad_mat.append((r["name"], m.get("name"), m.get("density")))
    add("SCREE ridges colored `scree` %s, opaque" % want_hex, scree and not bad_col, "%s" % (bad_col[:3] or "all %d" % len(scree)))
    add("SCREE ridges are HDPE (%.0f-%.0f kg/m^3), matte half-round rod" % HDPE_DENSITY, scree and not bad_mat,
        "%s" % (bad_mat[:3] or "%r at %s kg/m^3" % (scree[0]["mat"]["name"], scree[0]["mat"]["density"]) if scree else "none"))

    carpet = f.find("Field carpet")
    csol = f.solids(carpet)
    tags = f.find(r"re:^AprilTag \d+ - ")
    tag_floor = min(f.bbox([t])[2] for t in tags)
    centers = {}
    for side in ("BLUE", "RED"):
        for pname, cb_, dname, cr_ in TABLE:
            key = (side, pname)
            lab = "%s SCREE PATCH %s" % (side, pname)
            rs = ridges.get(key, [])
            if len(rs) != 4:
                add(lab + ": four ridges", False, "%d found" % len(rs))
                continue
            c = cb_ if side == "BLUE" else cr_
            sol = f.solids(rs)
            add(lab + ": each ridge is one solid", all(len(r["solids"]) == 1 for r in rs),
                "solids %s" % [len(r["solids"]) for r in rs])
            b = bb(sol)
            mc = ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2)
            centers[key] = mc
            add(lab + ": center at (%g, %g) (table%s)" % (c[0], c[1], "" if side == "BLUE" else ", Red twin"),
                abs(mc[0] - c[0]) < TOL and abs(mc[1] - c[1]) < TOL, "measured (%.4f, %.4f)" % mc)
            # footprint: inside the axis-parallel 30 x 30 square, reaching its sides
            ux, uy = unit(DIRS[dname])
            across_x = S if dname != "Y" else 2 * (max(OFFS) + R)
            want_b = [c[0] - across_x / 2, c[1] - HS, 0.0, c[0] + across_x / 2, c[1] + HS, R]
            add(lab + ": ridges fill the 30.0 x 30.0 footprint, sides parallel to the axes, cut square at its boundary (plan %s)"
                % ("X %.2f x Y 30.0" % across_x if dname == "Y" else "30.0 x 30.0"),
                all(abs(p - q) < TOL for p, q in zip(b, want_b)), "bbox %s want %s" % (fmt(b), fmt(want_b)))
            # the reference solids, one per documented offset, matched to the built ridges
            refs = [ref_ridge(c, dname, d) for d in OFFS]
            worst, unmatched = 0.0, []
            used = set()
            for d, rf in zip(OFFS, refs):
                rb = bb(rf)
                rc = ((rb[0] + rb[3]) / 2, (rb[1] + rb[4]) / 2)
                best = min(rs, key=lambda r: math.hypot((rbb[r["id"]][0] + rbb[r["id"]][3]) / 2 - rc[0],
                                                        (rbb[r["id"]][1] + rbb[r["id"]][4]) / 2 - rc[1]))
                if best["id"] in used:
                    unmatched.append(d)
                    continue
                used.add(best["id"])
                vb, vr, vc = K._volume(best["solids"]), K._volume(rf), cvol(best["solids"], rf)
                worst = max(worst, vb + vr - 2 * vc)
            add(lab + ": every ridge is the documented half-round R1.75 at its offset along the %s direction, cut square at the patch boundary"
                % dname, not unmatched and worst < VTOL, "worst symmetric-difference volume %.2e in^3%s"
                % (worst, "; no ridge for offsets %s" % unmatched if unmatched else ""))
            # measured in the patch frame: x along the ridge normal, y along the ridge
            PF = f.frame((c[0], c[1], 0.0), (uy, -ux, 0.0), (0.0, 0.0, 1.0))
            loc = sorted((f.bbox([r], PF) for r in rs), key=lambda q: q[0])
            cen = [(q[0] + q[3]) / 2 for q in loc]
            wid = [q[3] - q[0] for q in loc]
            hts = [(q[2], q[5]) for q in loc]
            add(lab + ": ridge centerlines at -12.0 / -4.0 / 4.0 / 12.0 along the ridge normal",
                all(abs(a - w) < TOL for a, w in zip(cen, OFFS)), "centerlines %s" % fmt(cen))
            add(lab + ": 8.0 pitch, 4.5 of flat carpet between ridges",
                all(abs((cen[i + 1] - cen[i]) - PITCH) < TOL for i in range(3))
                and all(abs((loc[i + 1][0] - loc[i][3]) - FLAT) < TOL for i in range(3)),
                "pitches %s, flats %s" % (fmt([cen[i + 1] - cen[i] for i in range(3)]), fmt([loc[i + 1][0] - loc[i][3] for i in range(3)])))
            add(lab + ": ridges run %s (3.5 wide across that direction) and stand 1.75 tall on the carpet" % dname,
                all(abs(w - 2 * R) < TOL for w in wid) and all(abs(z0) < TOL and abs(z1 - R) < TOL for z0, z1 in hts),
                "widths %s, Z %s" % (fmt(wid), [fmt(h) for h in hts]))
            # flat carpet on the ridge-normal offsets 0 and +/-8 (between ridges): no base plate
            probes = []
            for d in (-8.0, 0.0, 8.0):
                for t in (-6.0, 0.0, 6.0):
                    p = (c[0] + d * uy + t * ux, c[1] - d * ux + t * uy, 0.02)
                    if any(f.inside([r], p) for r in rs):
                        probes.append((round(p[0], 2), round(p[1], 2)))
            add(lab + ": bare carpet between the ridges (no base plate)", not probes, "material at %s" % probes[:4] if probes else "clear")
            # on the carpet, and nothing else shares the patch volume
            z0s = [rbb[r["id"]][2] for r in rs]
            dc = f.dist(rs, carpet)
            vcar = cvol(sol, csol)
            add(lab + ": stands on the carpet top (Z 0), touching it, not sunk into it",
                all(abs(z) < TOL for z in z0s) and dc < TOL and vcar < 1e-7, "zmin %s, gap %.2e, overlap %.2e" % (fmt(z0s), dc, vcar))
            prism = box(c[0] - HS, c[1] - HS, 1e-4, c[0] + HS, c[1] + HS, R + 0.5)
            pb = bb([prism])
            hits = []
            for r in recs:
                if "SCREE" in (r["name"] or "") or not overlaps(rbb[r["id"]], pb):
                    continue
                v = cvol(r["solids"], [prism])
                if v > 1e-7:
                    hits.append((r["name"], round(v, 5)))
            add(lab + ": no other field element (tape, SUPPLY, structure) inside the patch footprint up to Z 2.25",
                not hits, "%s" % (hits[:4] or "clear"))

    # ---------- symmetry ------------------------------------------------------------------------
    blue = [s for (sd, _), rs in ridges.items() if sd == "BLUE" for s in f.solids(rs)]
    red = [s for (sd, _), rs in ridges.items() if sd == "RED" for s in f.solids(rs)]
    if blue and red:
        vb, vr = K._volume(blue), K._volume(red)
        rb = transformed(blue, rot180())
        vc = cvol(rb, red)
        add("SCREE: Red is Blue rotated 180 deg about (324, 162) (same ridge directions)",
            abs(vb - vr) < VTOL and abs(vc - vr) < 10 * VTOL, "Blue %.4f, Red %.4f, common after rotation %.4f in^3" % (vb, vr, vc))
        for side, sol in (("BLUE", blue), ("RED", red)):
            mv = cvol(transformed(sol, mirror_y()), sol)
            v = K._volume(sol)
            add("SCREE: the %s half is mirror-symmetric about Y = 162 (both OUTFITTERS face identical SCREE)" % side,
                abs(mv - v) < 10 * VTOL, "volume %.4f, common with its mirror image %.4f in^3" % (v, mv))

    # ---------- layout (Blue-equivalent coordinates) -------------------------------------------
    for side in ("BLUE", "RED"):
        L = side + " SCREE: "
        sq = {}
        for pname, _, _, _ in TABLE:
            mc = centers.get((side, pname))
            if mc is None:
                continue
            c = rp(side, mc)
            sq[pname] = (c[0] - HS, c[1] - HS, c[0] + HS, c[1] + HS)
        if len(sq) != 9:
            add(L + "layout", False, "patches missing")
            continue
        for col, ((x0, x1), members) in COLUMNS.items():
            got = [(sq[p][0], sq[p][2]) for p in members]
            add(L + "%s column X %g-%g (%s)" % (col, x0, x1, ", ".join(members)),
                all(abs(a - x0) < TOL and abs(b - x1) < TOL for a, b in got), "X spans %s" % got)
        add(L + "staging marks (X 144) lie between the near and far columns",
            max(sq[p][2] for p in COLUMNS["near"][1]) < STAGE_X < min(sq[p][0] for p in COLUMNS["far"][1]), "")
        for (a, b), want in GAPS:
            g = rect_gap(sq[a], sq[b])
            real = f.dist(ridges[(side, a)], ridges[(side, b)])
            kind = "passable" if want >= PASSABLE else "closed"
            add(L + "%s gap %s-%s %.1f in" % (kind, a, b, want), abs(g - want) < 0.05 and real >= g - TOL,
                "footprint gap %.3f; ridge to ridge %.3f" % (g, real))
        cg = [rect_gap(sq[a], sq[b]) for a in COLUMNS["near"][1] for b in COLUMNS["far"][1]]
        near2 = [sorted(rect_gap(sq[a], sq[b]) for b in COLUMNS["far"][1])[:2] for a in COLUMNS["near"][1]]
        hi = max(g for pair in near2 for g in pair)
        add(L + "passable gaps between the near and far columns %.1f-%.1f in" % COLUMN_GAP,
            abs(min(cg) - COLUMN_GAP[0]) < 0.05 and abs(hi - COLUMN_GAP[1]) < 0.05,
            "closest %.3f; farthest of each near patch's two nearest %.3f" % (min(cg), hi))
        add(L + "closed 22.0-in gaps between S4 / S7 and the guardrails",
            abs(sq["S4"][1] - GUARD_GAP) < TOL and abs(FW - sq["S7"][3] - GUARD_GAP) < TOL,
            "S4 %.3f, S7 %.3f" % (sq["S4"][1], FW - sq["S7"][3]))
        own = [s for (sd, _), rs in ridges.items() if sd == side for s in f.solids(rs)]
        ob = bb(own)

        def clear(x0, y0, x1, y1):
            wb = rbox(side, x0, y0, x1, y1)
            pr = box(wb[0], wb[1], -0.5, wb[2], wb[3], 5.0)
            if not overlaps(bb([pr]), ob):
                return 0.0
            return cvol(own, [pr])
        v = clear(*HW_FRONT)
        add(L + "flat ground X 48-90 across Y 90-234 in front of the HEADWALL (42 in to square up)", v < 1e-9, "SCREE volume %.2e" % v)
        pads = []
        for y in STAGE_Y:
            vv = clear(STAGE_X - PAD[0] / 2, y - PAD[0] / 2, STAGE_X + PAD[0] / 2, y + PAD[0] / 2)
            if vv > 1e-9:
                pads.append((y, vv))
        add(L + "a 36 x 24 flat pad at each staging mark, either way round (the 36 x 36 square is clear)", not pads, "%s" % (pads or "clear"))
        mouths = [clear(*m) for m in LANE_MOUTHS]
        add(L + "each OUTFITTER LANE mouth (X 48-90) flat", all(m < 1e-9 for m in mouths), "%s" % mouths)
        v = clear(*APRON_STRIP)
        add(L + "flat ground from X 252 to the CRAG APRON line (X 264)", v < 1e-9, "SCREE volume %.2e" % v)
        # straight 28-in robot paths (clearance >= 14 to every measured patch square)
        rects = list(sq.values())
        front = [(HW_X, y) for y in np.arange(BASECAMP_Y[0], BASECAMP_Y[1] + 1e-9, PATH_STEP)]
        mouths = [(HW_X, y) for c_ in LANE_Y for y in np.arange(c_ - LANE_PLAY, c_ + LANE_PLAY + 1e-9, PATH_STEP)]
        shelf = [(APRON_X, y) for y in np.arange(SHELF_APPROACH[0], SHELF_APPROACH[1] + 1e-9, PATH_STEP)]
        socks = [(x, y) for y in SOCK_APPROACH_Y for x in np.arange(SOCK_APPROACH_X[0], SOCK_APPROACH_X[1] + 1e-9, PATH_STEP)]
        c, A, B = sweep(front, shelf, rects)
        k = int(np.argmax(c))
        good = c >= PATH_HALF
        in_corr = bool(good.any()) and CORRIDOR_START[0] <= A[good][:, 1].min() and A[good][:, 1].max() <= CORRIDOR_START[1] \
            and CORRIDOR_END[0] <= B[good][:, 1].min() and B[good][:, 1].max() <= CORRIDOR_END[1]
        add(L + "non-linear: one clear straight 28-in path from the BASECAMP front to the SHELF FACE approach, centerline Y ~175 "
            "at the front to its far (+Y) corner, about 0.4 in to spare",
            in_corr and abs(c[k] - PATH_HALF - CORRIDOR_SPARE) < 0.1 and CORRIDOR_START[0] <= A[k][1] <= CORRIDOR_START[1],
            "best clearance %.3f (%.3f to spare) from Y %.1f to Y %.1f; %d of %d sampled paths clear, starts Y %s, ends Y %s"
            % (c[k], c[k] - PATH_HALF, A[k][1], B[k][1], int(good.sum()), len(c),
               "%.1f-%.1f" % (A[good][:, 1].min(), A[good][:, 1].max()) if good.any() else "-",
               "%.1f-%.1f" % (B[good][:, 1].min(), B[good][:, 1].max()) if good.any() else "-"))
        c192 = sweep([(HW_X, EDGE_Y)], shelf + socks, rects)[0]
        add(L + "no clear 28-in path with its centerline at Y 189 (the corridor's upper edge, not its centerline)",
            c192.max() < PATH_HALF, "best clearance %.3f" % c192.max())
        cm = sweep(mouths, shelf + socks, rects)[0]
        add(L + "every straight 28-in path from an OUTFITTER LANE mouth to the SHELF FACE or a SOCKET FACE approach crosses a patch",
            cm.max() < PATH_HALF, "best clearance %.3f over %d paths" % (cm.max(), len(cm)))

    # ---------- zones, tags, BUMPERS -------------------------------------------------------------
    allsol = blue + red
    if allsol:
        ab = bb(allsol)
        bad = []
        for nm_, (x0, y0, x1, y1) in ZONES:
            pr = box(x0, y0, -0.5, x1, y1, 5.0)
            if overlaps(bb([pr]), ab):
                v = cvol(allsol, [pr])
                if v > 1e-9:
                    bad.append((nm_, v))
        add("SCREE lies outside every protected zone (CRAG APRONS, BASECAMPS, OUTFITTER LANES) and the CENTER CACHE",
            not bad, "%s" % (bad or "clear"))
        top = ab[5]
        add("SCREE occludes no AprilTag: ridge top %.2f below the lowest tag panel edge (tags at 12 in and higher)" % R,
            abs(top - R) < TOL and top < tag_floor and tag_floor >= TAG_MIN_CENTER - TAG_PANEL / 2 - TOL,
            "ridge top %.4f, lowest panel edge %.4f" % (top, tag_floor))
        add("BUMPER ZONE unchanged: a bumper bottom at 2.5 (R403) clears a ridge by 0.75",
            abs((BUMPER_BOTTOM_MAX - top) - BUMPER_CLEAR) < TOL, "clearance %.4f" % (BUMPER_BOTTOM_MAX - top))
    return out
