# -*- coding: utf-8 -*-
"""
Independent checks of the AprilTag panels and their 36h11 decals (26 tags).

Expected values come from the package documents only — never from src/:
  * 04-vision/apriltag-field-layout.json            (poses, metres + quaternions; parsed here)
  * 02-manual/sections/02-arena.md §3.7             (tag table; parsed here)
  * 04-vision/VISION-GUIDE.md §1, §3, §6.6          (tag table parsed here; panel geometry,
                                                     mounting, occlusion budget, tag->target offsets)
  * 03-field/FIELD-CAD-PACKAGE.md §0, §2-§5, §7, §10 (panel 9.0 x 0.25, target 8.125, body 6.5,
                                                     Z 17.5 / 12 / 52, pairs +/-14, plane P, DEPOT)
  * 03-field/MATERIALS-AND-COLORS.md §1-§3          (neutral-white #F5F5F5, tag black #111111,
                                                     printed vinyl on rigid backer, matte)
  * the official tag36h11 images (AprilRobotics/apriltag-imgs tag36h11/tag36_11_000NN.png,
    10 x 10 px, decoded below; they agree bit for bit with tag36h11.c + apriltag_to_image()).

Frames: a tag frame T has its origin at the tag centre on the front face, x = the facing normal
(yaw from the JSON quaternion), z = up, y = z x x (the WPILib tag frame).  A viewer facing the
tag looks along -x; his right is +y and up is +z.

Low Socket tube in the occlusion budget (the documents disagree by the socket's bottom-plate
thickness; DESIGN-SPEC governs): DESIGN-SPEC §3 makes the 7.0 socket length the depth a CELL seats
at ("a seated 14.0-in O2 CELL therefore stands 7.0 in proud"), so the 0.09 closed bottom lies beyond
it.  FIELD-CAD §2.3 / §7 and VISION-GUIDE §1.3 print the tube's lowest point as Z 22.27 (0.71 above
the target) and its span as 1.61-10.89 outboard, taking the 7.0 to the outer bottom; with the plate
they are Z 22.19 (0.63 above the target) and 1.5625-10.89.  The budget's conclusion is unchanged.

Construction reading (naming only): pegs and side sockets are named "... (guardrail side)" /
"... (centre side)".
"""
import json
import math
import os
import re

import numpy as np

import kernel_occ as K
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Ax1, gp_Dir, gp_Pnt, gp_Trsf, gp_Vec

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
JSON_PATH = os.path.join(REPO, "04-vision", "apriltag-field-layout.json")
MANUAL_PATH = os.path.join(REPO, "02-manual", "sections", "02-arena.md")
VISION_PATH = os.path.join(REPO, "04-vision", "VISION-GUIDE.md")

M_PER_IN = 0.0254
SIDED = (" (guardrail side)", " (centre side)")

# ---- document values ------------------------------------------------------------------------
PANEL = 9.0           # FIELD-CAD §7, §10 #14; VISION-GUIDE §1; manual §3.7
PANEL_T = 0.25        # FIELD-CAD §7 (ref); MATERIALS §2 "9.0 in sq x 0.25 in"
TARGET = 8.125        # FIELD-CAD §7; VISION-GUIDE §1
BODY = 6.5            # FIELD-CAD §7; VISION-GUIDE §1 (black square, outer edge of black border)
CELLS = 10            # tag36h11 total_width 10, width_at_border 8  ->  8.125 / 10 = 6.5 / 8
Z_CRAG, Z_HW, Z_OUT = 17.5, 12.0, 52.0
CRAG_BLUE, CRAG_RED = (324.0, 240.0), (324.0, 84.0)     # FIELD-CAD §1.1
CRAG_HALF = 24.0                                        # 48 x 48 footprint
PAIR_LAT = 14.0                                         # +/-14 from the face centreline
CHUTE_Y_BLUE = (30.0, 294.0)                            # FIELD-CAD §5
CHUTE_SILL, CHUTE_H = 24.0, 16.0                        # opening Z 24-40
LANE_Y_BLUE = (114.0, 162.0, 210.0)                     # FIELD-CAD §4.1
HW_TAG_X_BLUE = 39.0
P_X_BLUE, P_LEAN = 48.0, 15.0                           # plane P
FIELD_C = (324.0, 162.0)
RGB_WHITE = (0xF5, 0xF5, 0xF5)                          # MATERIALS §1.1 neutral-white
RGB_BLACK = (0x11, 0x11, 0x11)                          # MATERIALS §2 tag black
CLEAR_DEPTH = 12.0                                      # "nothing within 12 in along the normal"
SIGHT_DEPTH = 48.0                                      # longer sightline (info)

# Official tag36h11 images for IDs 1..26, row 0 = top, '1' = white (decoded from the PNGs).
OFFICIAL = {
    1: "1111111111/1000000001/1011011001/1001011101/1011110001/1001100001/1010110101/1000100101/1000000001/1111111111",
    2: "1111111111/1000000001/1011011101/1001001001/1010000001/1000100101/1000010001/1000111001/1000000001/1111111111",
    3: "1111111111/1000000001/1011100101/1000011101/1010011101/1010100101/1011001001/1001100001/1000000001/1111111111",
    4: "1111111111/1000000001/1011101001/1011110001/1010111101/1000101001/1010000001/1010001001/1000000001/1111111111",
    5: "1111111111/1000000001/1011110001/1011000101/1011011001/1010101101/1000111001/1010110001/1000000001/1111111111",
    6: "1111111111/1000000001/1000000101/1001011001/1010100101/1001110101/1000001001/1000010101/1000000001/1111111111",
    7: "1111111111/1000000001/1000010001/1000011001/1001010001/1010111001/1000011101/1001010001/1000000001/1111111111",
    8: "1111111111/1000000001/1000100001/1010101101/1000011101/1001111101/1011101001/1010110101/1000000001/1111111111",
    9: "1111111111/1000000001/1000100101/1010010101/1010101101/1001000001/1001000101/1011001001/1000000001/1111111111",
    10: "1111111111/1000000001/1000110101/1000111101/1011101001/1001000101/1010111001/1000011001/1000000001/1111111111",
    11: "1111111111/1000000001/1000111101/1011111101/1010010101/1010001001/1011001101/1001010101/1000000001/1111111111",
    12: "1111111111/1000000001/1001000001/1011101001/1000100101/1001001101/1000101001/1001101001/1000000001/1111111111",
    13: "1111111111/1000000001/1001000101/1011010001/1010110101/1000001101/1010000101/1001111101/1000000001/1111111111",
    14: "1111111111/1000000001/1001001101/1010100101/1011010001/1010010001/1000111101/1010100101/1000000001/1111111111",
    15: "1111111111/1000000001/1001010001/1010010001/1001100001/1001010001/1010011001/1010111001/1000000001/1111111111",
    16: "1111111111/1000000001/1001011001/1001100101/1001111101/1011010101/1001010001/1011100001/1000000001/1111111111",
    17: "1111111111/1000000001/1001101001/1000001101/1010111001/1011011001/1011000101/1000110001/1000000001/1111111111",
    18: "1111111111/1000000001/1001101001/1011111001/1001001001/1010011101/1000100001/1001000101/1000000001/1111111111",
    19: "1111111111/1000000001/1001111101/1010001101/1000010101/1001100001/1011101101/1010101001/1000000001/1111111111",
    20: "1111111111/1000000001/1010000001/1001110101/1010100101/1000100101/1001001001/1010111101/1000000001/1111111111",
    21: "1111111111/1000000001/1010000101/1001100001/1000110001/1011100101/1010100101/1011010001/1000000001/1111111111",
    22: "1111111111/1000000001/1010001101/1000110101/1001010001/1001101001/1001011101/1011111001/1000000001/1111111111",
    23: "1111111111/1000000001/1010011101/1011001001/1000011101/1000110001/1000101101/1001011101/1000000001/1111111111",
    24: "1111111111/1000000001/1010100001/1010110001/1010101001/1011110001/1010001001/1001110001/1000000001/1111111111",
    25: "1111111111/1000000001/1010101101/1001110001/1001011001/1000110101/1010011101/1010101101/1000000001/1111111111",
    26: "1111111111/1000000001/1010110001/1001011001/1011100101/1011110101/1011111001/1011000001/1000000001/1111111111",
}


# ---- small geometry helpers -----------------------------------------------------------------
def rot180(p):
    return (2 * FIELD_C[0] - p[0], 2 * FIELD_C[1] - p[1]) + tuple(p[2:])


def box_solid(F, lo, hi):
    """Axis-aligned box in frame F between local corners lo and hi, as a world solid."""
    b = BRepPrimAPI_MakeBox(gp_Pnt(*[float(v) for v in lo]), gp_Pnt(*[float(v) for v in hi])).Shape()
    return BRepBuilderAPI_Transform(b, F.trsf(), True).Shape()


def rec_of(shape):
    return {"solids": K._solids(shape), "name": "virtual"}


def common_vol(shape, solids):
    tot = 0.0
    for s in solids:
        c = BRepAlgoAPI_Common(shape, s)
        tot += K._volume(K._solids(c.Shape()))
    return tot


def bbox_overlap(a, b, pad=1e-6):
    return all(a[i] <= b[i + 3] + pad and b[i] <= a[i + 3] + pad for i in range(3))


def fmt(v, n=4):
    return ("%%.%df" % n) % v


class Ctx:
    """Per-run cache: world bboxes of every body record."""

    def __init__(self, f):
        self.f = f
        self.recs = f.records()
        self.bb = {id(r): f.bbox([r]) for r in self.recs}

    def near(self, shape, exclude=()):
        b = K.Bnd_Box()
        K.BRepBndLib.AddOptimal_s(shape, b, False, False)
        sb = K._box6(b)
        ex = {id(r) for r in exclude}
        return [r for r in self.recs if id(r) not in ex and bbox_overlap(self.bb[id(r)], sb)]

    def intruders(self, shape, exclude=(), tol=1e-6):
        out = []
        for r in self.near(shape, exclude):
            v = common_vol(shape, r["solids"])
            if v > tol:
                out.append((r["name"], v))
        return out


# ---- document parsing -----------------------------------------------------------------------
def load_json():
    with open(JSON_PATH) as fh:
        js = json.load(fh)
    out = {}
    for t in js["tags"]:
        tr = t["pose"]["translation"]
        q = t["pose"]["rotation"]["quaternion"]
        out[t["ID"]] = {"xyz_m": (tr["x"], tr["y"], tr["z"]), "q": (q["W"], q["X"], q["Y"], q["Z"]),
                        "xyz": tuple(v / M_PER_IN for v in (tr["x"], tr["y"], tr["z"])),
                        "yaw": math.degrees(2 * math.atan2(q["Z"], q["W"])) % 360.0}
    return js, out


def _num(s):
    return float(s.replace("−", "-").strip())


def parse_manual():
    txt = open(MANUAL_PATH, encoding="utf-8").read()
    sec = txt[txt.index("## 3.7 AprilTags"):]
    rows = {}
    rx = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*\(([^,]+),\s*([^)]+)\)\s*\|\s*([\d.]+) in\s*\|\s*([+−-][XY])\s*\|", re.M)
    for m in rx.finditer(sec):
        face = m.group(6).replace("−", "-")
        yaw = {"+X": 0.0, "+Y": 90.0, "-X": 180.0, "-Y": 270.0}[face]
        rows[int(m.group(1))] = {"where": m.group(2), "xyz": (_num(m.group(3)), _num(m.group(4)), _num(m.group(5))), "yaw": yaw}
    return rows


def parse_vision():
    txt = open(VISION_PATH, encoding="utf-8").read()
    sec = txt[txt.index("## 3. Tag Placement Table"):txt.index("### 3.3")]
    rows = {}
    rx = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|", re.M)
    for m in rx.finditer(sec):
        rows[int(m.group(1))] = {"where": m.group(2) + " " + m.group(3),
                                 "xyz": (float(m.group(4)), float(m.group(5)), float(m.group(6))),
                                 "yaw": float(m.group(7))}
    return rows


def rules_table():
    """FIELD-CAD §7 mounting table turned into poses (Blue), Red by the 180-degree rotation."""
    blue = {}
    blue[1] = (0.0, CHUTE_Y_BLUE[0], Z_OUT, 0.0)
    blue[2] = (0.0, CHUTE_Y_BLUE[1], Z_OUT, 0.0)
    for i, y in enumerate(LANE_Y_BLUE):
        blue[3 + i] = (HW_TAG_X_BLUE, y, Z_HW, 0.0)
    cx, cy = CRAG_BLUE
    blue[6] = (cx - CRAG_HALF, cy - PAIR_LAT, Z_CRAG, 180.0)   # shelf face X = 300, -Y side first
    blue[7] = (cx - CRAG_HALF, cy + PAIR_LAT, Z_CRAG, 180.0)
    blue[8] = (cx - PAIR_LAT, cy + CRAG_HALF, Z_CRAG, 90.0)    # +Y socket face, alliance-wall side
    blue[9] = (cx + PAIR_LAT, cy + CRAG_HALF, Z_CRAG, 90.0)
    blue[10] = (cx - PAIR_LAT, cy - CRAG_HALF, Z_CRAG, 270.0)
    blue[11] = (cx + PAIR_LAT, cy - CRAG_HALF, Z_CRAG, 270.0)
    blue[12] = (cx + CRAG_HALF, cy - PAIR_LAT, Z_CRAG, 0.0)    # peg face X = 348
    blue[13] = (cx + CRAG_HALF, cy + PAIR_LAT, Z_CRAG, 0.0)
    out = dict(blue)
    for i, p in blue.items():
        r = rot180(p[:3])
        out[i + 13] = (r[0], r[1], r[2], (p[3] + 180.0) % 360.0)
    return out


def kind_of(tid):
    b = tid if tid <= 13 else tid - 13
    return "outfitter" if b <= 2 else ("headwall" if b <= 5 else "crag")


def is_red(tid):
    return tid > 13


def tag_frame(f, xyz, yaw):
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    return f.frame(xyz, (c, s, 0.0), (0.0, 0.0, 1.0))


def angdiff(a, b):
    return abs((a - b + 180.0) % 360.0 - 180.0)


# ---- the checks -----------------------------------------------------------------------------
def run(f):
    out = []

    def ck(label, ok, detail):
        out.append((label, bool(ok), detail))

    C = Ctx(f)
    js, jt = load_json()
    man = parse_manual()
    vis = parse_vision()
    rules = rules_table()

    # ============ A. the documents agree with each other (inputs) ===========================
    ck("docs: JSON has exactly IDs 1..26", sorted(jt) == list(range(1, 27)), "IDs %s" % sorted(jt))
    ck("docs: JSON field 16.4592 x 8.2296 m (648 x 324 in)",
       abs(js["field"]["length"] - 648 * M_PER_IN) < 1e-9 and abs(js["field"]["width"] - 324 * M_PER_IN) < 1e-9,
       "field %s" % js["field"])
    ck("docs: manual §3.7 table parsed (26 rows)", sorted(man) == list(range(1, 27)), "rows %s" % sorted(man))
    ck("docs: VISION-GUIDE §3 tables parsed (26 rows)", sorted(vis) == list(range(1, 27)), "rows %s" % sorted(vis))
    bad = []
    for tid, t in jt.items():
        W, X, Y, Z = t["q"]
        if abs(X) > 1e-12 or abs(Y) > 1e-12 or abs(W * W + Z * Z - 1) > 1e-12:
            bad.append(tid)
    ck("docs: every JSON rotation is a unit pure-yaw quaternion (plumb)", not bad, "bad IDs %s" % bad)
    bad = []
    for tid in range(1, 27):
        if tid not in jt:
            continue
        ref = rules[tid]
        for src, row in (("manual", man.get(tid)), ("VISION-GUIDE", vis.get(tid)), ("JSON", {"xyz": jt[tid]["xyz"], "yaw": jt[tid]["yaw"]})):
            if row is None:
                bad.append("%d missing in %s" % (tid, src))
                continue
            if max(abs(a - b) for a, b in zip(row["xyz"], ref[:3])) > 1e-6 or angdiff(row["yaw"], ref[3]) > 1e-6:
                bad.append("%d %s %s yaw %s vs §7 %s" % (tid, src, row["xyz"], row["yaw"], ref))
    ck("docs: JSON == manual §3.7 == VISION-GUIDE §3 == FIELD-CAD §7 rules (all 26 poses)", not bad, "; ".join(bad) or "all agree")
    bad = []
    for b in range(1, 14):
        pb, pr = jt[b], jt[b + 13]
        r = rot180(pb["xyz"])
        if max(abs(a - c) for a, c in zip(r, pr["xyz"])) > 1e-6 or angdiff(pb["yaw"] + 180, pr["yaw"]) > 1e-6:
            bad.append("%d->%d" % (b, b + 13))
    ck("docs: JSON Red tag N+13 = Blue tag N rotated 180 deg about (324, 162)", not bad, "bad %s" % bad)

    # ============ B. each built panel ======================================================
    panels = {}
    for tid in range(1, 27):
        rs = [r for r in C.recs if re.match(r"^AprilTag %d( |$|-)" % tid, r["name"] or "")]
        ok = len(rs) == 1 and len(rs[0]["solids"]) == 1
        ck("tag %d: exactly one single-solid body named 'AprilTag %d ...'" % (tid, tid), ok,
           "%d bodies, names %s" % (len(rs), [r["name"] for r in rs]))
        if rs:
            panels[tid] = rs[0]
    extra = [r["name"] for r in C.recs if (r["name"] or "").startswith("AprilTag") and r not in panels.values()]
    ck("26 AprilTag bodies, no strays", len(panels) == 26 and not extra, "found %d, strays %s" % (len(panels), extra))

    frames = {}
    for tid, rec in sorted(panels.items()):
        t = jt[tid]
        T = tag_frame(f, t["xyz"], t["yaw"])
        frames[tid] = T
        # name / location (manual §3.7 "Location" column)
        want = man[tid]["where"].replace(",", "").replace("−", "-").lower()
        got = rec["name"].split(" - ", 1)[1].lower() if " - " in rec["name"] else ""
        ck("tag %d: name carries its manual §3.7 location" % tid, got == want,
           "name %r, manual %r" % (rec["name"], man[tid]["where"]))
        # panel box in the JSON tag frame: centre, facing, plumb, square, 9.0 x 9.0 x 0.25
        bb = f.bbox([rec], T)
        want_bb = [-PANEL_T, -PANEL / 2, -PANEL / 2, 0.0, PANEL / 2, PANEL / 2]
        err = max(abs(a - b) for a, b in zip(bb, want_bb))
        ck("tag %d: panel 9.0 x 9.0 x 0.25, front face in the tag plane, centred on the JSON pose, plumb and square (bbox in tag frame)" % tid,
           err < 1e-4, "bbox %s want %s (max err %.2e)" % ([fmt(v) for v in bb], want_bb, err))
        vol = f.volume([rec])
        ck("tag %d: panel volume = 9.0 x 9.0 x 0.25 = 20.25 in^3 (a plain slab)" % tid, abs(vol - PANEL * PANEL * PANEL_T) < 1e-4,
           "volume %.5f" % vol)
        # world centre of the front face vs the JSON translation (metres, exact)
        wb = f.bbox([rec])
        n = np.array([math.cos(math.radians(t["yaw"])), math.sin(math.radians(t["yaw"])), 0.0])
        ax = int(np.argmax(np.abs(n)))
        c = [(wb[i] + wb[i + 3]) / 2 for i in range(3)]
        c[ax] = wb[ax + 3] if n[ax] > 0 else wb[ax]
        dm = max(abs(c[i] * M_PER_IN - t["xyz_m"][i]) for i in range(3))
        ck("tag %d: built tag centre == apriltag-field-layout.json (metres)" % tid, dm < 1e-9,
           "built %s in -> %s m, JSON %s m" % ([fmt(v) for v in c], [fmt(v * M_PER_IN, 6) for v in c], t["xyz_m"]))
        # appearance and material
        rgb, alpha = f.color([rec])
        ck("tag %d: panel neutral-white #F5F5F5, opaque" % tid, tuple(rgb) == RGB_WHITE and alpha == 1,
           "rgb %s alpha %s" % (rgb, alpha))
        mat = f.material([rec]) or {}
        mname = (mat.get("name") or "").lower()
        ck("tag %d: material is printed vinyl on a rigid backer (MATERIALS §2)" % tid,
           "vinyl" in mname and "backer" in mname and 900 <= mat.get("density", 0) <= 2000,
           "material %s" % mat)

        # decal
        d = rec.get("decal")
        if not d:
            ck("tag %d: 36h11 decal present" % tid, False, "no decal recorded")
            continue
        o, dn, dx = np.array(d["origin"], float), np.array(d["normal"], float), np.array(d["x"], float)
        s, cells = d["s"], d["cells"]
        ck("tag %d: decal grid 10 x 10 cells of 0.8125 -> target 8.125, body (8 cells) 6.5" % tid,
           cells == CELLS and abs(cells * s - TARGET) < 1e-9 and abs(8 * s - BODY) < 1e-9,
           "cells %s, s %s -> target %.4f body %.4f" % (cells, s, cells * s, 8 * s))
        right = np.cross([0, 0, 1.0], n)
        ok = (np.linalg.norm(o - np.array(t["xyz"])) < 1e-9 and np.linalg.norm(dn - n) < 1e-9
              and np.linalg.norm(dx - right) < 1e-9)
        ck("tag %d: decal centred on the tag centre, on the front face, normal = facing, u-axis = viewer's right" % tid, ok,
           "origin %s normal %s x %s (want x = %s)" % ([fmt(v) for v in o], [fmt(v) for v in dn], [fmt(v) for v in dx], [fmt(v) for v in right]))
        # render the decal as a viewer facing the tag sees it, using tagDecal's placement rule
        # (cell [r, c] centre at u = (c + 0.5 - h) s along x, v = (h - r - 0.5) s along n x x)
        h = cells / 2.0
        vy = np.cross(dn, dx)
        img = [["1"] * cells for _ in range(cells)]
        okcells = True
        for (r, cc) in d["black"]:
            p = o + dx * (cc + 0.5 - h) * s + vy * (h - r - 0.5) * s
            rel = p - o
            col = int(math.floor(np.dot(rel, right) / s + h))
            row = int(math.floor(h - np.dot(rel, [0, 0, 1.0]) / s))
            if 0 <= row < cells and 0 <= col < cells:
                img[row][col] = "0"
            else:
                okcells = False
        seen = "/".join("".join(rw) for rw in img)
        diff = [(r, c) for r in range(cells) for c in range(cells) if seen.split("/")[r][c] != OFFICIAL[tid].split("/")[r][c]]
        ck("tag %d: decal as seen from the field == official tag36_11_%05d image (row 0 top, col 0 left)" % (tid, tid),
           okcells and not diff, "differing cells %s" % diff[:12])

    # ============ C. mounting: flush with the structure ====================================
    def fit_in_pocket(tid, host_rs, label, through):
        T = frames[tid]
        rec = panels[tid]
        hb = f.bbox(host_rs, T)
        ck("tag %d: %s face plane coincides with the tag plane" % (tid, label), abs(hb[3]) < 1e-6,
           "%s extends to x = %.6f along the tag normal (want 0)" % (label, hb[3]))
        solids = f.solids(host_rs)
        g = 0.1
        outer = box_solid(T, (-PANEL_T, -PANEL / 2 - g, -PANEL / 2 - g), (0, PANEL / 2 + g, PANEL / 2 + g))
        inner = box_solid(T, (-PANEL_T, -PANEL / 2, -PANEL / 2), (0, PANEL / 2, PANEL / 2))
        ring_want = ((PANEL + 2 * g) ** 2 - PANEL ** 2) * PANEL_T
        v_out, v_in = common_vol(outer, solids), common_vol(inner, solids)
        ck("tag %d: pocket in the %s is exactly 9.0 x 9.0 x 0.25 around the panel (no gap, no overlap)" % (tid, label),
           abs(v_in) < 1e-6 and abs(v_out - ring_want) < 1e-4,
           "host inside pocket %.6f in^3 (want 0); host in 0.1-in ring round it %.5f (want %.5f)" % (v_in, v_out, ring_want))
        pv = common_vol(rec["solids"][0], solids)
        ck("tag %d: panel does not interfere with the %s" % (tid, label), pv < 1e-6, "common volume %.6f" % pv)
        if not through:
            back = box_solid(T, (-PANEL_T - 0.1, -PANEL / 2, -PANEL / 2), (-PANEL_T, PANEL / 2, PANEL / 2))
            vb = common_vol(back, solids)
            ck("tag %d: pocket floor 0.25 deep, backed by %s material (not through)" % (tid, label),
               abs(vb - PANEL * PANEL * 0.1) < 1e-4, "material behind the panel %.5f of %.5f" % (vb, PANEL * PANEL * 0.1))
            ck("tag %d: panel seated on the pocket floor" % tid, f.dist([rec], host_rs) < 1e-6, "gap %.6f" % f.dist([rec], host_rs))

    for tid in sorted(panels):
        k = kind_of(tid)
        side = "RED" if is_red(tid) else "BLUE"
        if k == "crag":
            fit_in_pocket(tid, f.find("%s CRAG tower" % side), "CRAG tower", through=False)
            # facing outward, perpendicular to its face, 24 from the crag centre, +/-14 along the face
            cc = CRAG_RED if is_red(tid) else CRAG_BLUE
            T = frames[tid]
            loc = T.to_local((cc[0], cc[1], Z_CRAG))
            ck("tag %d: faces outward, square to its CRAG face (crag centre 24 behind, on the pair axis +/-14)" % tid,
               abs(loc[0] + CRAG_HALF) < 1e-9 and abs(abs(loc[1]) - PAIR_LAT) < 1e-9 and abs(loc[2]) < 1e-9,
               "crag centre in tag frame %s" % [fmt(v) for v in loc])
        elif k == "outfitter":
            fit_in_pocket(tid, f.find("%s alliance wall glazing" % side), "alliance-wall glazing", through=True)
            pv = common_vol(panels[tid]["solids"][0], f.solids(f.find("%s alliance wall lower panel" % side)))
            ck("tag %d: panel clear of the alliance-wall lower panel" % tid, pv < 1e-6, "common %.6f" % pv)
        else:
            T = frames[tid]
            wedges = f.find("%s HEADWALL tag wedge bracket" % side)
            mine = [w for w in wedges if f.dist([w], [panels[tid]]) < 1e-6]
            ck("tag %d: panel stands on exactly one HEADWALL tag wedge bracket (contact)" % tid, len(mine) == 1,
               "%d wedges touch the panel" % len(mine))
            if not mine:
                continue
            w = mine[0]
            wv = common_vol(panels[tid]["solids"][0], w["solids"])
            wbb = f.bbox([w], T)
            ck("tag %d: wedge behind the panel, inside its 9.0 x 9.0 outline, no overlap" % tid,
               wv < 1e-6 and wbb[3] <= -PANEL_T + 1e-6 and wbb[1] >= -PANEL / 2 - 1e-6 and wbb[4] <= PANEL / 2 + 1e-6
               and wbb[2] >= -PANEL / 2 - 1e-6 and wbb[5] <= PANEL / 2 + 1e-6,
               "overlap %.6f; wedge bbox in tag frame %s" % (wv, [fmt(v) for v in wbb]))
            beam = f.find("%s HEADWALL lower crossbeam" % side)
            bv = common_vol(w["solids"][0], f.solids(beam))
            ck("tag %d: wedge seated on the lower crossbeam (contact, no overlap)" % tid,
               f.dist([w], beam) < 1e-6 and bv < 1e-6, "gap %.6f overlap %.6f" % (f.dist([w], beam), bv))
            # wedge face against the crossbeam: 15 deg from vertical, top toward the alliance wall
            # (parallel to plane P).  Measure the wedge's back (-x) extent at two heights.
            zs = []
            for zl in (wbb[2] + 0.2, wbb[5] - 0.2):
                sl = box_solid(T, (-10, -PANEL / 2, zl - 0.005), (0, PANEL / 2, zl + 0.005))
                cs = K._solids(BRepAlgoAPI_Common(sl, w["solids"][0]).Shape())
                b = K.Bnd_Box()
                for sx in cs:
                    K.BRepBndLib.AddOptimal_s(BRepBuilderAPI_Transform(sx, T.trsf().Inverted(), True).Shape(), b, False, False)
                zs.append((zl, K._box6(b)[0]))
            slope = (zs[1][1] - zs[0][1]) / (zs[1][0] - zs[0][0])   # d(back x)/dz in the tag frame
            ang = math.degrees(math.atan(abs(slope)))
            ck("tag %d: wedge is a 15-deg wedge whose beam face leans with plane P (thicker at the top)" % tid,
               abs(ang - P_LEAN) < 0.05 and slope < 0, "beam-face angle %.3f deg, back x %s" % (ang, [(fmt(a, 3), fmt(b, 3)) for a, b in zs]))

    # ============ D. clearance / occlusion in front of every panel ============================
    for tid in sorted(panels):
        T = frames[tid]
        rec = panels[tid]
        prism_t = box_solid(T, (1e-4, -TARGET / 2, -TARGET / 2), (CLEAR_DEPTH, TARGET / 2, TARGET / 2))
        hits = C.intruders(prism_t, exclude=[rec])
        ck("tag %d: 8.125 target unobstructed - nothing within %.0f in along its normal" % (tid, CLEAR_DEPTH), not hits,
           "intruders %s" % [(n, round(v, 4)) for n, v in hits])
        prism_p = box_solid(T, (1e-4, -PANEL / 2, -PANEL / 2), (CLEAR_DEPTH, PANEL / 2, PANEL / 2))
        hits = C.intruders(prism_p, exclude=[rec])
        ck("tag %d: whole 9.0 panel face clear for %.0f in along its normal" % (tid, CLEAR_DEPTH), not hits,
           "intruders %s" % [(n, round(v, 4)) for n, v in hits])
        prism_l = box_solid(T, (1e-4, -TARGET / 2, -TARGET / 2), (SIGHT_DEPTH, TARGET / 2, TARGET / 2))
        hits = C.intruders(prism_l, exclude=[rec])
        ck("tag %d: head-on sightline to the target clear for %.0f in (staged field)" % (tid, SIGHT_DEPTH), not hits,
           "intruders %s" % [(n, round(v, 4)) for n, v in hits])
        others = C.intruders(rec["solids"][0], exclude=[rec])
        ck("tag %d: panel interferes with no other body" % tid, not others, "overlaps %s" % [(n, round(v, 5)) for n, v in others])

    # ============ E. occlusion budget (FIELD-CAD §7, VISION-GUIDE §1.3) =======================
    tb = TARGET / 2
    for side, pair in (("BLUE", (6, 7, 8, 9, 10, 11, 12, 13)), ("RED", (19, 20, 21, 22, 23, 24, 25, 26))):
        zs = [f.bbox([panels[t]])[2] for t in pair] + [f.bbox([panels[t]])[5] for t in pair]
        ck("%s CRAG panels span Z 13.00-22.00 (§7)" % side,
           all(abs(v - 13.0) < 1e-6 for v in zs[:8]) and all(abs(v - 22.0) < 1e-6 for v in zs[8:]),
           "zmin %s zmax %s" % (sorted({fmt(v) for v in zs[:8]}), sorted({fmt(v) for v in zs[8:]})))
        tz = [(panels[t]["decal"]["origin"][2] - tb, panels[t]["decal"]["origin"][2] + tb) for t in pair if panels[t].get("decal")]
        ck("%s CRAG targets span Z 13.44-21.56 (13.4375-21.5625)" % side,
           all(abs(a - 13.4375) < 1e-6 and abs(b - 21.5625) < 1e-6 for a, b in tz), "spans %s" % sorted(set((fmt(a), fmt(b)) for a, b in tz)))
        F = f.crag_frame(side)
        floor = f.find("%s CRAG BASE DEPOT floor" % side)
        ftop = f.bbox(floor)[5]
        ck("%s BASE DEPOT tray floor top at Z 0.25 (§3, the occlusion budget's datum)" % side, abs(ftop - 0.25) < 1e-6, "floor top %.4f" % ftop)
        s1 = f.bbox(f.find("%s CRAG Shelf 1" % side))[2]
        ck("%s Shelf 1 underside Z 23.25 = 1.25 above the panel top (§7)" % side, abs(s1 - 23.25) < 1e-4 and abs(s1 - 22.0 - 1.25) < 1e-4,
           "underside %.4f -> %.4f above the panel" % (s1, s1 - 22.0))
        lows = [r for sfx in SIDED for r in f.find("%s CRAG Low Socket%s" % (side, sfx))]
        lz = min(f.bbox([r])[2] for r in lows)
        # §2.3: rim 30, 8.0 out, 30 deg, outer radius 3.34; 7.0 bore + 0.09 closed bottom (docstring)
        s30, c30 = 0.5, math.sqrt(3) / 2
        lz_want = 30.0 - (7.0 + 0.09) * c30 - 3.34 * s30
        ck("%s Low Socket tube lowest point Z %.2f, %.2f above the target top (§2.3, §7)" % (side, lz_want, lz_want - 21.5625),
           abs(lz - lz_want) < 0.005 and lz - 21.5625 > 0.5,
           "lowest %.4f -> %.4f above target top (§2.3 / §7 print 22.27 and 0.71: the tube taken to the 7.0 seat, "
           "without the 0.09 closed bottom)" % (lz, lz - 21.5625))
        span = []
        for r in lows:
            b = f.bbox([r], F)
            span.append((abs(b[1] if b[1] > 0 else b[4]) - CRAG_HALF, abs(b[4] if b[4] > 0 else b[1]) - CRAG_HALF))
        in_want = 8.0 - (7.0 + 0.09) * s30 - 3.34 * c30
        ck("%s Low Socket tubes span %.2f-10.89 in outboard of their faces (§7, VISION-GUIDE §1.3)" % (side, in_want),
           len(span) == 2 and all(abs(a - in_want) < 0.005 and abs(b - 10.89) < 0.01 for a, b in span),
           "spans %s (the documents print 1.61 for the inboard edge, at the 7.0 seat)" % [(fmt(a, 3), fmt(b, 3)) for a, b in span])
        # Shelf 1 gussets: above Z 22.0 inside the prisms over the SHELF FACE panels (§2.2)
        shelf_tags = (6, 7) if side == "BLUE" else (19, 20)
        gus = f.find("%s CRAG Shelf 1 gusset" % side)
        bad = []
        for t in shelf_tags:
            T = frames[t]
            prism = box_solid(T, (0, -PANEL / 2, -30), (14.0, PANEL / 2, 22.0 - Z_CRAG))
            v = common_vol(prism, f.solids(gus))
            if v > 1e-6:
                bad.append((t, v))
        ck("%s Shelf 1 gussets stay above Z 22.0 over the SHELF FACE tag panels (§2.2)" % side, not bad, "violations %s" % bad)

    # virtual SUPPLIES in the BASE DEPOT in front of the tray-side tags
    crates = f.find("re:^CACHE CRATE")
    crate = max(crates, key=lambda r: f.bbox([r])[5] - f.bbox([r])[2])
    cb = f.bbox([crate])
    crate_h = cb[5] - cb[2]
    cells = f.find("re:^O2 CELL - CENTER CACHE")
    cell = cells[0]
    eb = f.bbox([cell])
    coils = f.find("re:^ROPE COIL - CENTER CACHE")
    coil = coils[0]
    ob = f.bbox([coil])

    def place(shape, bb, T, local_centre, rot=None):
        c0 = gp_Pnt((bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2, (bb[2] + bb[5]) / 2)
        tr = gp_Trsf()
        if rot is not None:
            tr.SetRotation(gp_Ax1(c0, gp_Dir(*rot[0])), rot[1])
        sh = BRepBuilderAPI_Transform(shape, tr, True).Shape()
        dst = T.pt(local_centre)
        mv = gp_Trsf()
        mv.SetTranslation(gp_Vec(float(dst[0] - c0.X()), float(dst[1] - c0.Y()), float(dst[2] - c0.Z())))
        return BRepBuilderAPI_Transform(sh, mv, True).Shape()

    ck("model CACHE CRATE crowned envelope 13.0 tall (§9.1; sets the DEPOT margin)", abs(crate_h - 13.0) < 0.01,
       "tallest model crate %.4f (%s)" % (crate_h, crate["name"]))
    tray_tags = (6, 7, 8, 10, 19, 20, 21, 23)       # SHELF FACE pair + alliance-wall-side SOCKET FACE tags
    for tid in tray_tags:
        side = "RED" if is_red(tid) else "BLUE"
        T = frames[tid]
        zf = 0.25
        target = box_solid(T, (1e-4, -tb, -tb), (CLEAR_DEPTH, tb, tb))
        tray = f.find("%s CRAG BASE DEPOT floor" % side) + f.find("%s CRAG BASE DEPOT lip" % side)
        tower = f.find("%s CRAG tower" % side)
        # crate: square to the axes, crowned face against the CRAG face (lateral fit inside the arm for socket tags)
        lat = 0.0
        if tid in (8, 10, 21, 23):
            # the corner arm runs 16 along the SOCKET FACE from the SHELF FACE plane and the tag
            # sits 10 from that plane: shift the 13-in crate 2 in toward the shelf face so it
            # lies inside the arm (it still covers the whole 8.125 target width)
            shelf_n = np.array([1.0, 0, 0]) if is_red(tid) else np.array([-1.0, 0, 0])
            lat = 2.0 * float(np.sign(np.dot(T.y, shelf_n)))
        cr = place(crate["solids"][0], cb, T, (6.5 + 1e-3, lat, zf + crate_h / 2 - Z_CRAG))
        top = zf + crate_h
        v = common_vol(cr, f.solids([rec_of(target)]))
        vs = common_vol(cr, f.solids(tray + tower))
        ck("tag %d: crowned CRATE standing in the DEPOT tops out at Z %.2f, %.2f below the target - clear (§7: 13.25 / 0.19)" % (tid, top, 13.4375 - top),
           v < 1e-6 and vs < 1e-6 and abs(top - 13.25) < 0.01 and abs((13.4375 - top) - 0.19) < 0.01,
           "apex %.4f, margin %.4f, overlap with target prism %.6f, with tray/tower %.6f" % (top, 13.4375 - top, v, vs))
        # O2 CELL stood on its end against the face, centred on the tag (the documented exception)
        up = place(cell["solids"][0], eb, T, (2.5 + 1e-3, 0.0, zf + 7.0 - Z_CRAG),
                   rot=((0.0, 1.0, 0.0), math.pi / 2) if (eb[3] - eb[0]) > (eb[5] - eb[2]) + 1 else None)
        b = K.Bnd_Box()
        K.BRepBndLib.AddOptimal_s(up, b, False, False)
        ub = K._box6(b)
        vt = common_vol(up, f.solids([rec_of(target)]))
        clear_struct = common_vol(up, f.solids(tray + tower))
        ck("tag %d: upright O2 CELL in the DEPOT: apex Z 14.25, 0.81 into the target band - the one documented exception (VISION-GUIDE §1.3)" % tid,
           abs(ub[5] - 14.25) < 0.01 and abs(ub[5] - 13.4375 - 0.8125) < 0.01 and vt > 0 and clear_struct < 1e-6,
           "apex %.4f, into band %.4f, target overlap %.4f in^3, overlap with tray/tower %.6f" % (ub[5], ub[5] - 13.4375, vt, clear_struct))
        # ROPE COIL on edge, parallel to the face
        oc = place(coil["solids"][0], ob, T, (1.25 + 1e-3, 0.0, zf + 5.0 - Z_CRAG), rot=(tuple(T.y), math.pi / 2))
        b = K.Bnd_Box()
        K.BRepBndLib.AddOptimal_s(oc, b, False, False)
        obb = K._box6(b)
        vc = common_vol(oc, f.solids([rec_of(target)]))
        ck("tag %d: ROPE COIL on edge in the DEPOT tops out at Z 10.25, 3.19 below the target - clear" % tid,
           vc < 1e-6 and abs(obb[5] - 10.25) < 0.01, "top %.4f, overlap %.6f" % (obb[5], vc))

    # ============ F. HEADWALL: behind plane P, clear of the rungs ==========================
    for side in ("BLUE", "RED"):
        red = side == "RED"
        tids = (16, 17, 18) if red else (3, 4, 5)
        A = f.alliance_frame(side)
        # plane P in the alliance frame: through (48, y, 0), field-side normal (cos15, 0, sin15)
        nP = np.array([math.cos(math.radians(P_LEAN)), 0.0, math.sin(math.radians(P_LEAN))])
        for tid in tids:
            T = frames[tid]
            ds = []
            for y in (-PANEL / 2, PANEL / 2):
                for z in (-PANEL / 2, PANEL / 2):
                    for x in (-PANEL_T, 0.0):
                        a = A.to_local(T.pt((x, y, z)))
                        ds.append(((a - np.array([P_X_BLUE, 0, 0])) @ nP, z, x))
            front_top = max(d for d, z, x in ds if z > 0 and x == 0.0)
            front_bot = max(d for d, z, x in ds if z < 0 and x == 0.0)
            worst = max(d for d, z, x in ds)
            ck("tag %d: whole panel >= 4.4 behind plane P (4.42 at the top edge, 6.75 at the bottom; §4.1, VISION-GUIDE §3.3)" % tid,
               worst <= -4.4 and abs(-front_top - 4.42) < 0.005 and abs(-front_bot - 6.75) < 0.005,
               "top edge %.4f, bottom edge %.4f, worst %.4f behind P" % (-front_top, -front_bot, -worst))
            mine = [w for w in f.find("%s HEADWALL tag wedge bracket" % side) if f.dist([w], [panels[tid]]) < 1e-6]
            if mine:
                wb = f.bbox(mine, frame_P(f, A))
                ck("tag %d: tag wedge bracket >= 4.0 behind plane P (truss rule, §4.1)" % tid, wb[3] <= -4.0 + 1e-6,
                   "wedge front at %.4f normal to P" % wb[3])
            rungs = f.find("re:^%s HEADWALL lane \\d (LEDGE|CAMP|SUMMIT) RUNG$" % side)
            dmin = min(f.dist([panels[tid]], [r]) for r in rungs)
            rz = min(f.bbox([r])[2] for r in rungs)
            ck("tag %d: panel band (Z 7.5-16.5) clear of every rung" % tid, rz > 16.5 and dmin > 0,
               "lowest rung Z %.3f, nearest rung %.3f in" % (rz, dmin))

    # ============ G. tag -> target transforms (VISION-GUIDE §6.6) =============================
    for side in ("BLUE", "RED"):
        red = side == "RED"
        o = 13 if red else 0
        # SHELF FACE pair midpoint frame: x = outward, y = toward the higher-numbered tag
        t_lo, t_hi = jt[6 + o]["xyz"], jt[7 + o]["xyz"]
        mid = [(a + b) / 2 for a, b in zip(t_lo, t_hi)]
        n = frames[6 + o].x
        yl = np.array(t_hi) - np.array(t_lo)
        yl = yl / np.linalg.norm(yl)
        M = f.frame(mid, n, (0, 0, 1))
        flip = float(np.dot(M.y, yl))           # +1 or -1: lateral sign convention of §6.6
        for sh in (1, 2):
            fences = f.find("%s CRAG Shelf %d slot fence" % (side, sh))
            fb = sorted([f.bbox([r], M) for r in fences], key=lambda b: (b[1] + b[4]) / 2)
            ctrs = [flip * ((fb[i][4] + fb[i + 1][1]) / 2) for i in range(3)]
            slab = f.bbox(f.find("%s CRAG Shelf %d" % (side, sh)), M)
            up = 24.0 - Z_CRAG if sh == 1 else 42.0 - Z_CRAG
            ok = (sorted(round(c, 6) for c in ctrs) == [-15.5, 0.0, 15.5] and abs((slab[0] + slab[3]) / 2 - 7.0) < 1e-6
                  and abs(slab[5] - up) < 1e-6)
            ck("%s Shelf %d slot centres at -15.5/0/+15.5 lateral, +7.0 out, +%.1f up from the tag-pair midpoint" % (side, sh, up), ok,
               "centres %s, out %.4f, up %.4f" % ([fmt(c) for c in sorted(ctrs)], (slab[0] + slab[3]) / 2, slab[5]))
        sb = f.bbox(f.find("%s CRAG Summit Socket" % side), M)
        ck("%s Summit Socket on the shelf-face pair midline (lateral 0)" % side, abs((sb[1] + sb[4]) / 2) < 1e-6,
           "lateral %.5f" % ((sb[1] + sb[4]) / 2))
        # sockets directly above one tag of each SOCKET FACE pair
        for low_t, mid_t in ((8 + o, 9 + o), (10 + o, 11 + o)):
            for nm, t in (("Low", low_t), ("Mid", mid_t)):
                T = frames[t]
                hits = []
                for r in [r for sfx in SIDED for r in f.find("%s CRAG %s Socket%s" % (side, nm, sfx))]:
                    b = f.bbox([r], T)
                    if b[0] > -1:     # on this face (outboard of it)
                        hits.append(b)
                ok = len(hits) == 1 and abs((hits[0][1] + hits[0][4]) / 2) < 1e-6
                ck("tag %d: %s Socket directly above it (VISION-GUIDE §6.6)" % (t, nm), ok,
                   "sockets on this face %d, lateral offset %s" % (len(hits), [fmt((h[1] + h[4]) / 2) for h in hits]))
        for t in (12 + o, 13 + o):
            T = frames[t]
            for nm, up in (("Low", 30.0 - Z_CRAG), ("Mid", 54.0 - Z_CRAG)):
                hits = [f.bbox([r], T) for sfx in SIDED for r in f.find("%s CRAG %s Peg%s" % (side, nm, sfx))]
                hits = [b for b in hits if abs((b[1] + b[4]) / 2) < 3]
                ok = len(hits) == 1 and abs((hits[0][1] + hits[0][4]) / 2) < 1e-6
                ck("tag %d: %s Peg root directly above it (+%.1f up)" % (t, nm, up), ok,
                   "pegs over this tag %d, lateral %s" % (len(hits), [fmt((h[1] + h[4]) / 2) for h in hits]))
        # HEADWALL rungs relative to each lane tag, in the tag frame
        want = {"LEDGE": (1.2, 17.25, -12.0), "CAMP": (-5.3, 41.25, 12.0), "SUMMIT": (-11.7, 65.25, -12.0)}
        tids = (16, 17, 18) if red else (3, 4, 5)
        for li, tid in enumerate(tids):
            T = frames[tid]
            lane = li + 1
            got = {}
            for rn in want:
                b = f.bbox(f.find("%s HEADWALL lane %d %s RUNG" % (side, lane, rn)), T)
                got[rn] = ((b[0] + b[3]) / 2, (b[2] + b[5]) / 2, (b[1] + b[4]) / 2)
            ok = all(abs(got[k][0] - want[k][0]) < 0.06 and abs(got[k][1] - want[k][1]) < 1e-4 and abs(got[k][2] - want[k][2]) < 1e-4
                     for k in want)
            ck("tag %d: rungs of HEADWALL lane %d at the §6.6 offsets (out 1.2/-5.3/-11.7, up 17.25/41.25/65.25, lateral -12/+12/-12 in the tag frame)" % (tid, lane),
               ok, "; ".join("%s out %.3f up %.3f lat %.3f" % (k, *got[k]) for k in want))
        # OUTFITTER: chute opening centre 20 in directly below the tag
        wall = f.find("%s alliance wall lower panel" % side) + f.find("%s alliance wall glazing" % side)
        for t in (1 + o, 2 + o):
            T = frames[t]

            def solid_at(z, y=0.0, x=-0.1):
                return f.inside(wall, (x, y, z), T)

            def edge(a, b, fn):       # a inside the opening, b in material
                for _ in range(40):
                    m = (a + b) / 2
                    if fn(m):
                        b = m
                    else:
                        a = m
                return (a + b) / 2
            zc = -20.0
            ztop = edge(zc, -6.0, lambda z: solid_at(z))      # -6: glazing below the tag pocket
            # sill and jambs probed 0.6 deep in the 0.75 lower panel, behind the R0.5 (ref) sill roundover
            zbot = edge(zc, -40.0, lambda z: solid_at(z, 0.0, -0.6))
            yl_ = edge(0.0, -25.0, lambda y: solid_at(zc, y, -0.6))
            yr_ = edge(0.0, 25.0, lambda y: solid_at(zc, y, -0.6))
            ok = (abs((ztop + zbot) / 2 + 20.0) < 1e-4 and abs((yl_ + yr_) / 2) < 1e-4 and abs(ztop - zbot - CHUTE_H) < 1e-4
                  and abs(-PANEL / 2 - ztop - 7.5) < 1e-4)
            ck("tag %d: OUTFITTER opening centred 20 in directly below the tag; panel clears the opening top by 7.50 (§5)" % t, ok,
               "opening Z %.4f..%.4f (tag frame), lateral %.4f..%.4f, panel bottom above opening top by %.4f"
               % (zbot, ztop, yl_, yr_, -PANEL / 2 - ztop))

    # ============ H. Red = Blue rotated 180 degrees (geometry and decal) =====================
    R = f.frame((2 * FIELD_C[0], 2 * FIELD_C[1], 0), (-1, 0, 0), (0, 0, 1))
    for b in range(1, 14):
        if b not in panels or b + 13 not in panels:
            continue
        bb_b = f.bbox([panels[b]])
        bb_r = f.bbox([panels[b + 13]], R)
        ok = max(abs(x - y) for x, y in zip(bb_b, bb_r)) < 1e-6
        db, dr = panels[b].get("decal"), panels[b + 13].get("decal")
        ok_d = bool(db and dr) and np.linalg.norm(R.dir(db["x"]) - np.array(dr["x"])) < 1e-9 and \
            np.linalg.norm(R.dir(db["normal"]) - np.array(dr["normal"])) < 1e-9
        ck("tag %d is tag %d rotated 180 deg about (324, 162), decal frame included" % (b + 13, b), ok and ok_d,
           "blue %s red(rotated back) %s" % ([fmt(v) for v in bb_b], [fmt(v) for v in bb_r]))

    # ============ I. palette used for the decal black ========================================
    pal = f.ns.get("PAL", {})
    ck("decal black is tag black #111111 (MATERIALS §2)", tuple(pal.get("tag-black", ())) == RGB_BLACK, "tag-black %s" % (pal.get("tag-black"),))
    ck("decals are on in the default build", bool(f.opts.get("decals")) and bool(f.opts.get("tags")), "opts %s" % f.opts)
    return out


def frame_P(f, A):
    """Frame with origin on plane P's carpet line, x = P's field-side normal, z = up the plane."""
    s, c = math.sin(math.radians(P_LEAN)), math.cos(math.radians(P_LEAN))
    o = A.pt((P_X_BLUE, 0.0, 0.0))
    return f.frame(o, A.dir((c, 0.0, s)), A.dir((-s, 0.0, c)))
