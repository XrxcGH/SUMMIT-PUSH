# -*- coding: utf-8 -*-
"""
Independent checks: field carpet, long-side guardrails and FIELD LED bands.

Expected values come from the package documents, never from src/20_ledger.fs:

  FIELD-CAD-PACKAGE §0   carpet 648 x 324; guardrails 20 in tall; centerline X = 324;
                         layout 180-degree rotationally symmetric about (324, 162);
                         every angle on the field is 15, 30 or 45 degrees.
  FIELD-CAD-PACKAGE §1.3 guardrails: 20 in tall, transparent panel on a low frame of 2 x 1 in
                         tube, along both long edges (ref).  FIELD LED bands: 1.0-in-wide
                         frosted band let into the top rail of each long-side guardrail, lens
                         centre 19.0 in above the carpet, running the full 648 in and divided at
                         X = 324 into two 324-in alliance segments; the 19.0 height must clear
                         the 20-in guardrail top.
  Manual §3.1 / §3.1.1   FIELD bounded by guardrails and alliance walls; origin where the Blue
                         alliance wall meets the guardrail at Y = 0; heights from the carpet.
  Manual §3.1.2          bands on the long-side guardrails at Y = 0 and Y = 324, lens facing
                         inward, lens centre 19.0; each ALLIANCE has two segments, one on each
                         side; states Green (FIELD safe), White (FORECAST, 1/2/3 lit blocks),
                         ALLIANCE colour (ROUTE, 1/2/3 lit blocks), Dark.  So each segment
                         carries three blocks.
  Manual §4.3.1          FORECAST W / I / G -> 1 / 2 / 3 lit blocks (both alliances' segments).
  Manual R207            the FIELD LED indication is "a horizontal row of one, two, or three equal,
                         discrete, separated lit blocks"; a continuous strip is not a countable
                         block pattern.  -> three equal blocks per 324-in segment, each lit block
                         separated from the next (and from the other segment's at X 324) by a
                         stretch of the band that stays dark.
  (ref, generator)       the package leaves the block layout free.  The generator puts the three
                         blocks on a 108-in pitch (324 / 3) counted from each alliance's own wall
                         (block 1 nearest the wall); each pitch is a lit block followed, on the
                         field-centre side, by a dark gap body ("... segment gap n"), so blocks and
                         gaps together tile the continuous band.  Unlit blocks are dark.
                         Guardrail posts turn the 2-in side of the 2 x 1 tube along the rail.
                         Shared names (posts, glazing bays) carry a creation-order " n" suffix.
  MATERIALS-AND-COLORS   carpet `carpet` #6E6A63; guardrail frame aluminium extrusion `wall`
                         #9AA4B2, 2 x 1 in tube; guardrail glazing polycarbonate `glazing`
                         #DCE8FA at 25 %, 0.25 in; FIELD LED band frosted acrylic lens,
                         state-dependent, 1.0 in wide; led-green #3FBF4F; neutral-white #F5F5F5;
                         alliance-blue #1D63C8; alliance-red #CC3333.

Bodies are found by name only to classify them; every property is measured.
"""
import math
import os
import re

import kernel_occ as K
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Pnt

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

# ---- document values (inches) -------------------------------------------------------------
FIELD_L, FIELD_W = 648.0, 324.0          # §0 / §10 #1
CX, CY = 324.0, 162.0                    # §0 centerline / field centre
GUARD_H = 20.0                           # §0, §1.3
LED_W = 1.0                              # §1.3, manual §3.1.2, M&C §2
LED_Z = 19.0                             # §1.3 lens centre
SEG_L = 324.0                            # §1.3 two 324-in alliance segments
LED_BLOCKS = 3                           # manual §3.1.2: one, two or three lit blocks per segment
BLOCK_PITCH = SEG_L / LED_BLOCKS         # (ref) R207 "equal" blocks, one per 108 in of the segment
FRAME_SEC = (1.0, 2.0)                   # §1.3 / M&C §2 "2 x 1 in tube"
GLAZE_T = 0.25                           # M&C §2 guardrail glazing
EPS = 1e-6
TOL = 1e-3

PERIM_RX = r"re:^Guardrail \(|^Field carpet"


def _hex_tokens():
    """Palette tokens straight from MATERIALS-AND-COLORS.md."""
    with open(os.path.join(PKG, "participants", "03-field", "MATERIALS-AND-COLORS.md"), encoding="utf-8") as fh:
        md = fh.read()
    tok = {}
    for m in re.finditer(r"`([a-z0-9-]+)`\s*\|\s*`(#[0-9A-Fa-f]{6})`(?:\s*at\s*(\d+)%\s*opacity)?", md):
        tok[m.group(1)] = (tuple(int(m.group(2)[i:i + 2], 16) for i in (1, 3, 5)),
                           (int(m.group(3)) / 100.0) if m.group(3) else 1.0)
    return tok


def _box(p0, p1):
    return BRepPrimAPI_MakeBox(gp_Pnt(*[float(v) for v in p0]), gp_Pnt(*[float(v) for v in p1])).Shape()


_BB = {}


def _bb_shape(s):
    """Bounding box of one shape, cached (the field's solids are measured many times)."""
    k = id(s)
    hit = _BB.get(k)
    if hit is not None and hit[0] is s:
        return hit[1]
    b = K.Bnd_Box()
    K.BRepBndLib.AddOptimal_s(s, b, False, False)
    bb = K._box6(b)
    _BB[k] = (s, bb)
    return bb


def _overlap(a, b, pad=0.0):
    return not (a[0] >= b[3] - pad or b[0] >= a[3] - pad or a[1] >= b[4] - pad or b[1] >= a[4] - pad
                or a[2] >= b[5] - pad or b[2] >= a[5] - pad)


def _common_vol(sa, sb):
    c = K.BRepAlgoAPI_Common(sa, sb)
    return K._volume(K._solids(c.Shape()))


def _fmt(b):
    return "[" + ", ".join("%.4f" % v for v in b) + "]"


def _close(a, b, tol=TOL):
    return abs(a - b) <= tol


def _rot_bb(b):
    """World bbox of the 180-degree rotation about (324, 162) of bbox b."""
    return [FIELD_L - b[3], FIELD_W - b[4], b[2], FIELD_L - b[0], FIELD_W - b[1], b[5]]


def _x_coverage(solids, z, y0, y1, x0=-2.0, x1=FIELD_L + 2.0, dz=0.01):
    """X intervals where the solids have material in the slab y0..y1 at height z."""
    probe = _box((x0, y0, z - dz), (x1, y1, z + dz))
    pb = _bb_shape(probe)
    iv = []
    for s in solids:
        if not _overlap(_bb_shape(s), pb):
            continue
        c = K.BRepAlgoAPI_Common(s, probe)
        for piece in K._solids(c.Shape()):
            bb = _bb_shape(piece)
            iv.append((bb[0], bb[3]))
    iv.sort()
    merged = []
    for a, b in iv:
        if merged and a <= merged[-1][1] + 1e-4:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return merged


def _gaps(merged, lo, hi):
    gaps = []
    cur = lo
    for a, b in merged:
        if b <= lo or a >= hi:
            continue
        if a > cur + 1e-3:
            gaps.append((cur, a))
        cur = max(cur, b)
    if cur < hi - 1e-3:
        gaps.append((cur, hi))
    return gaps


def _lin_mass_range_2x1_al():
    """lb per inch of a 2 x 1 in aluminium tube, wall 1/16 .. 1/8 in (2700 kg/m^3)."""
    rho = 2700 * K.IN3 / K.LB   # lb/in^3
    out = []
    for t in (0.0625, 0.125):
        area = 2 * 1 - (2 - 2 * t) * (1 - 2 * t)
        out.append(area * rho)
    return out


def run(f):
    out = []

    def add(label, ok, detail):
        out.append((label, bool(ok), detail))

    pal = _hex_tokens()
    for t in ("carpet", "wall", "glazing", "led-green", "neutral-white", "alliance-blue", "alliance-red"):
        add("M&C token %s parsed from the document" % t, t in pal, "tokens found: %d" % len(pal))

    allrecs = f.records()

    # =========================================================================================
    # CARPET
    # =========================================================================================
    carpet = f.find("re:(?i)carpet")
    add("carpet: exactly one body", len(carpet) == 1 and len(f.solids(carpet)) == 1,
        "%d bodies, %d solids" % (len(carpet), len(f.solids(carpet))))
    cb = f.bbox(carpet)
    want = [0, 0, None, FIELD_L, FIELD_W, 0]
    for i, ax in enumerate(("xmin", "ymin", "zmin", "xmax", "ymax", "zmax")):
        if want[i] is not None:
            add("carpet %s = %s (648 x 324, top at Z 0)" % (ax, want[i]), _close(cb[i], want[i], 1e-6),
                "got %.6f" % cb[i])
    t = cb[5] - cb[2]
    add("carpet thickness (ref) lies below Z 0 and is plausible (0 < t <= 1 in)", 0 < t <= 1.0 and cb[2] < 0,
        "zmin %.4f, thickness %.4f" % (cb[2], t))
    add("carpet is a flat rectangular slab (volume = 648 x 324 x t)",
        _close(f.volume(carpet), FIELD_L * FIELD_W * t, 1e-3 * FIELD_L * FIELD_W * t),
        "volume %.3f vs %.3f" % (f.volume(carpet), FIELD_L * FIELD_W * t))
    rgb, alpha = f.color(carpet)
    if "carpet" in pal:
        add("carpet colour = `carpet` %s" % str(pal["carpet"][0]), tuple(rgb) == pal["carpet"][0] and alpha == 1.0,
            "got %s alpha %s" % (rgb, alpha))
    mat = f.material(carpet)
    add("carpet material is carpet", "carpet" in mat["name"].lower(), mat["name"])
    # areal density of low-pile event carpet with backing: ~1-6 lb/yd^2
    ad = f.mass_lb(carpet) / (FIELD_L * FIELD_W / 1296.0)
    add("carpet areal mass plausible (1-6 lb/yd^2)", 1.0 <= ad <= 6.0,
        "%.2f lb/yd^2 (density %.0f kg/m^3, total %.0f lb)" % (ad, mat["density"], f.mass_lb(carpet)))

    # nothing sinks into the carpet (the carpet top is the Z = 0 datum for every height)
    csol = f.solids(carpet)[0]
    sinks = []
    for r in allrecs:
        if r is carpet[0]:
            continue
        for s in r["solids"]:
            if _overlap(_bb_shape(s), cb):
                v = _common_vol(csol, s)
                if v > 1e-6:
                    sinks.append("%s (%.4f in^3)" % (r["name"], v))
    add("no body penetrates the carpet (everything stands on Z 0)", not sinks, "; ".join(sinks[:10]))

    # =========================================================================================
    # GUARDRAILS
    # =========================================================================================
    sides = {}
    for key, label, y_edge, outward in (("Y0", "Y = 0", 0.0, -1), ("Y324", "Y = 324", FIELD_W, +1)):
        rs = f.find(r"re:^Guardrail \(%s\)" % re.escape(label))
        sides[key] = {"rs": rs, "label": label, "y": y_edge, "out": outward}

    # every body standing outside a long edge (within the field length) belongs to a guardrail
    stray = []
    for r in allrecs:
        bs = [_bb_shape(x) for x in r["solids"]]
        b = [min(q[i] for q in bs) for i in range(3)] + [max(q[i] for q in bs) for i in range(3, 6)]
        if (b[4] <= 0 + EPS or b[1] >= FIELD_W - EPS) and b[3] > 0 and b[0] < FIELD_L:
            if not (r["name"] or "").startswith("Guardrail ("):
                stray.append(r["name"])
    add("every body along the long edges is a named guardrail part", not stray, "; ".join(map(str, stray[:10])))

    lin_lo, lin_hi = _lin_mass_range_2x1_al()
    for key, sd in sides.items():
        rs, lab, y_edge, sgn = sd["rs"], sd["label"], sd["y"], sd["out"]
        tag = "guardrail %s" % lab
        bb = f.bbox(rs)
        add("%s: runs the full field length X 0-648" % tag, _close(bb[0], 0, 1e-6) and _close(bb[3], FIELD_L, 1e-6),
            "X %.4f..%.4f" % (bb[0], bb[3]))
        add("%s: stands on the carpet plane (zmin 0)" % tag, _close(bb[2], 0, 1e-6), "zmin %.6f" % bb[2])
        add("%s: 20 in tall (zmax 20)" % tag, _close(bb[5], GUARD_H, 1e-6), "zmax %.6f" % bb[5])
        # no intrusion into the 648 x 324 field
        if sgn < 0:
            inner, ok = bb[4], bb[4] <= y_edge + 1e-6
        else:
            inner, ok = bb[1], bb[1] >= y_edge - 1e-6
        add("%s: no part intrudes into the field (inner face at Y %g)" % (tag, y_edge), ok and _close(inner, y_edge, 1e-6),
            "inner face at Y %.6f" % inner)
        depth = (bb[4] - bb[1])
        add("%s: overall depth is the 1-in frame depth of a 2 x 1 tube" % tag, _close(depth, 1.0, 1e-6)
            or _close(depth, 2.0, 1e-6), "depth %.4f" % depth)

        # the barrier is continuous over X 0..648 at every height from the carpet to 20 in
        sols = f.solids(rs)
        y0, y1 = (y_edge - 3, y_edge) if sgn < 0 else (y_edge, y_edge + 3)
        bad = []
        for z in (0.02, 1.0, 1.99, 2.01, 5.0, 10.0, 15.0, 17.99, 18.01, 18.75, 19.0, 19.25, 19.75, 19.98):
            g = _gaps(_x_coverage(sols, z, y0, y1), 0.0, FIELD_L)
            if g:
                bad.append("Z %.2f gaps %s" % (z, ", ".join("%.3f-%.3f" % q for q in g[:4])))
        add("%s: continuous barrier, X 0-648, Z 0-20 (no gaps)" % tag, not bad, "; ".join(bad[:6]))

        # classify by name
        rails = [r for r in rs if re.search(r"(?i)\brail\b", r["name"]) and "LED" not in r["name"]]
        top = [r for r in rails if "top" in r["name"].lower()]
        bot = [r for r in rails if "bottom" in r["name"].lower()]
        posts = [r for r in rs if re.search(r"(?i)\bpost\b", r["name"])]
        glaze = [r for r in rs if re.search(r"(?i)glaz", r["name"])]
        leds = [r for r in rs if "FIELD LED" in r["name"]]          # every lens body: blocks and gaps
        blocks = [r for r in leds if re.search(r" segment block \d+$", r["name"])]
        gapb = [r for r in leds if re.search(r" segment gap \d+$", r["name"])]
        frame = top + bot + posts
        add("%s: has a top rail, a bottom rail, posts, glazing and LED segments" % tag,
            len(top) == 1 and len(bot) == 1 and posts and glaze and leds,
            "top %d bottom %d posts %d glazing %d LED %d" % (len(top), len(bot), len(posts), len(glaze), len(leds)))
        classified = set(id(r) for r in frame + glaze + blocks + gapb)
        add("%s: every body is frame, glazing, LED block or LED gap" % tag, all(id(r) in classified for r in rs),
            "; ".join(r["name"] for r in rs if id(r) not in classified))

        # 2 x 1 frame section for every frame member (sorted cross-section dims)
        for grp, nmx in ((top, "top rail"), (bot, "bottom rail")):
            for r in grp:
                b = f.bbox([r])
                sec = tuple(sorted((round(b[4] - b[1], 6), round(b[5] - b[2], 6))))
                add("%s %s: 2 x 1 in section" % (tag, nmx), sec == FRAME_SEC, "Y x Z = %s" % (sec,))
                add("%s %s: full 648-in length" % (tag, nmx), _close(b[3] - b[0], FIELD_L, 1e-6),
                    "length %.4f" % (b[3] - b[0]))
        badpost = []
        for r in posts:
            b = f.bbox([r])
            sec = tuple(sorted((round(b[3] - b[0], 6), round(b[4] - b[1], 6))))
            if sec != FRAME_SEC:
                badpost.append("X %.2f-%.2f: %g x %g" % (b[0], b[3], sec[1], sec[0]))
        add("%s posts: 2 x 1 in tube section (M&C §2 guardrail frame)" % tag, not badpost,
            "%d of %d posts are not 2 x 1: %s" % (len(badpost), len(posts), "; ".join(badpost[:3])))
        # orientation is free in the package (§1.3 '(ref)'): the generator turns the 2-in side along the rail
        badori = []
        for r in posts:
            b = f.bbox([r])
            if not (_close(b[3] - b[0], FRAME_SEC[1], 1e-6) and _close(b[4] - b[1], FRAME_SEC[0], 1e-6)):
                badori.append("%s: X %.4f x Y %.4f" % (r["name"], b[3] - b[0], b[4] - b[1]))
        add("%s posts (ref): 2 in along the rail (X), 1 in deep (Y) - same depth as the rails" % tag, not badori,
            "; ".join(badori[:3]) or "%d posts" % len(posts))
        if bot:
            b = f.bbox(bot)
            add("%s: frame is low - bottom rail sits on the carpet plane" % tag, _close(b[2], 0, 1e-6),
                "bottom rail Z %.4f..%.4f" % (b[2], b[5]))
        if top:
            b = f.bbox(top)
            add("%s: top rail top at 20 in" % tag, _close(b[5], GUARD_H, 1e-6), "top rail Z %.4f..%.4f" % (b[2], b[5]))

        # axis-aligned boxes only (no stray angles; the top rail is a box less the LED groove)
        nonbox = []
        for r in bot + posts + glaze + leds:
            b = f.bbox([r])
            bv = (b[3] - b[0]) * (b[4] - b[1]) * (b[5] - b[2])
            if not _close(f.volume([r]), bv, 1e-6 * max(1.0, bv)):
                nonbox.append(r["name"])
        add("%s: members are axis-aligned prisms (vertical/horizontal only)" % tag, not nonbox,
            "; ".join(nonbox[:5]))
        if top:
            b = f.bbox(top)
            env = (b[3] - b[0]) * (b[4] - b[1]) * (b[5] - b[2])
            filled = f.volume(top) + f.volume(leds)
            add("%s: LED lenses exactly fill the groove let into the top rail" % tag, _close(filled, env, 1e-4 * env),
                "rail + lenses %.4f vs rail envelope %.4f in^3" % (filled, env))

        # appearance / material of the frame
        fr_bad = []
        for r in frame:
            if tuple(r["rgb"]) != pal.get("wall", (None,))[0] or r["alpha"] != 1.0:
                fr_bad.append("%s rgb %s a %s" % (r["name"], r["rgb"], r["alpha"]))
            if "alumin" not in r["mat"]["name"].lower():
                fr_bad.append("%s material %s" % (r["name"], r["mat"]["name"]))
        add("%s frame: `wall` colour, aluminium" % tag, not fr_bad, "; ".join(fr_bad[:4]))
        for r in top + bot:
            b = f.bbox([r])
            lm = f.mass_lb([r]) / (b[3] - b[0])
            add("%s %s: mass per inch matches a 2 x 1 aluminium tube (1/16-1/8 wall)" % (tag, r["name"].split(") ")[-1]),
                lin_lo * 0.85 <= lm <= lin_hi * 1.02,
                "%.4f lb/in vs %.4f..%.4f" % (lm, lin_lo, lin_hi))

        # glazing: polycarbonate, 0.25 thick, glazing colour at 25 %, fills the bays between members
        gz_bad = []
        garea = 0.0
        for r in glaze:
            b = f.bbox([r])
            dims = sorted((b[3] - b[0], b[4] - b[1], b[5] - b[2]))
            if not _close(dims[0], GLAZE_T, 1e-6):
                gz_bad.append("%s thickness %.4f" % (r["name"], dims[0]))
            if not _close(b[4] - b[1], GLAZE_T, 1e-6):
                gz_bad.append("glazing not a vertical sheet in the rail plane (Y extent %.4f)" % (b[4] - b[1]))
            if "polycarbonate" not in r["mat"]["name"].lower() or not (1150 <= r["mat"]["density"] <= 1250):
                gz_bad.append("material %s %.0f" % (r["mat"]["name"], r["mat"]["density"]))
            if "glazing" in pal and (tuple(r["rgb"]) != pal["glazing"][0] or not _close(r["alpha"], pal["glazing"][1], 1e-9)):
                gz_bad.append("colour %s a %s" % (r["rgb"], r["alpha"]))
            if f.dist([r], frame) > 1e-6:
                gz_bad.append("%s X %.1f floats %.4f from the frame" % (r["name"], b[0], f.dist([r], frame)))
            garea += (b[3] - b[0]) * (b[5] - b[2])
        add("%s glazing: polycarbonate 0.25 in, `glazing` at 25 %%, held by the frame" % tag, not gz_bad,
            "; ".join(gz_bad[:4]))
        frac = garea / (FIELD_L * GUARD_H)
        add("%s: transparent panel is most of the face (>= 60 %% glazed)" % tag, frac >= 0.6,
            "glazed fraction %.3f" % frac)

        # ---- FIELD LED band on this rail ---------------------------------------------------
        # manual §3.1.2: a continuous band divided at X 324 into two 324-in ALLIANCE segments; a
        # segment shows one, two or three lit blocks, so it carries three blocks, and R207 describes
        # the indication as "equal, discrete, separated" blocks -> three equal blocks per segment with
        # a dark stretch after each (ref: on a 108-in pitch), blocks and gaps tiling the band.
        halves = {"BLUE": [], "RED": [], "straddles X 324": []}
        for r in blocks + gapb:
            b = f.bbox([r])
            k = "BLUE" if b[3] <= CX + 1e-6 else ("RED" if b[0] >= CX - 1e-6 else "straddles X 324")
            halves[k].append(r)
        nb = {al: len([r for r in halves[al] if r in blocks]) for al in ("BLUE", "RED")}
        ng = {al: len([r for r in halves[al] if r in gapb]) for al in ("BLUE", "RED")}
        add("%s: LED band = two alliance segments split at X 324, each of %d blocks and %d dark gaps (manual §3.1.2, R207)"
            % (tag, LED_BLOCKS, LED_BLOCKS),
            all(nb[al] == LED_BLOCKS and ng[al] == LED_BLOCKS for al in nb) and not halves["straddles X 324"],
            "%d LED bodies: Blue %d blocks + %d gaps, Red %d blocks + %d gaps, straddling %s" % (
                len(leds), nb["BLUE"], ng["BLUE"], nb["RED"], ng["RED"], [r["name"] for r in halves["straddles X 324"]]))
        leds_sorted = []
        for al, seg in (("BLUE", (0.0, CX)), ("RED", (CX, FIELD_L))):
            parts = sorted(halves[al], key=lambda r: f.bbox([r])[0])
            xs = [(f.bbox([r])[0], f.bbox([r])[3]) for r in parts]
            joins = all(_close(xs[i][1], xs[i + 1][0], 1e-6) for i in range(len(xs) - 1))
            add("%s LED %s segment: X %g-%g, one continuous band of abutting blocks and gaps (324-in segment, §1.3 / §3.1.2)"
                % (tag, al, seg[0], seg[1]),
                bool(xs) and _close(xs[0][0], seg[0], 1e-6) and _close(xs[-1][1], seg[1], 1e-6) and joins,
                "lens bodies X %s" % ", ".join("%.4f..%.4f" % q for q in xs))
            # blocks and gaps alternate, counted from the alliance's own wall: block, gap, block, gap, ...
            from_wall = parts if al == "BLUE" else parts[::-1]
            kinds = ["block" if r in blocks else "gap" for r in from_wall]
            add("%s LED %s segment: block, gap, block, gap, block, gap from the %s wall toward X 324 (ref)" % (tag, al, al),
                kinds == ["block", "gap"] * LED_BLOCKS, "order %s" % kinds)
            bl = [f.bbox([r])[3] - f.bbox([r])[0] for r in parts if r in blocks]
            gl = [f.bbox([r])[3] - f.bbox([r])[0] for r in parts if r in gapb]
            add("%s LED %s segment: %d blocks of equal length (R207 'equal' blocks)" % (tag, al, LED_BLOCKS),
                len(bl) == LED_BLOCKS and max(bl) - min(bl) <= 1e-6, "block lengths %s" % ["%.4f" % x for x in bl])
            add("%s LED %s segment: every block separated from the next by a dark gap of equal length (R207 'separated')"
                % (tag, al), len(gl) == LED_BLOCKS and min(gl) > 1.0 and max(gl) - min(gl) <= 1e-6,
                "gap lengths %s" % ["%.4f" % x for x in gl])
            add("%s LED %s segment (ref): each block + its gap spans one %.0f-in pitch (324 / 3)" % (tag, al, BLOCK_PITCH),
                len(bl) == len(gl) == LED_BLOCKS and all(_close(a + b, BLOCK_PITCH, 1e-6) for a, b in zip(bl, gl)),
                "block + gap %s" % ["%.4f" % (a + b) for a, b in zip(bl, gl)])
            for r in parts:
                leds_sorted.append((al, r))
        for al, r in leds_sorted:
            b = f.bbox([r])
            st = "%s LED %s" % (tag, r["name"].split(" FIELD LED, ", 1)[-1])
            # numbering (ref): the package leaves the lit order free; block k and the gap after it
            # occupy the k-th 108-in pitch counted from the alliance's own wall (Blue X 0, Red X 648)
            mm = re.search(r"\b(BLUE|RED) segment (block|gap) (\d+)$", r["name"])
            if mm and mm.group(1) == al:
                k = int(mm.group(3))
                d0 = (k - 1) * BLOCK_PITCH
                d = (b[0], b[3]) if al == "BLUE" else (FIELD_L - b[3], FIELD_L - b[0])
                inpitch = d[0] >= d0 - 1e-6 and d[1] <= d0 + BLOCK_PITCH + 1e-6
                edge = _close(d[0], d0, 1e-6) if mm.group(2) == "block" else _close(d[1], d0 + BLOCK_PITCH, 1e-6)
                add("%s (ref): %s %d in the %s wall's pitch %d (%.0f-%.0f in from the wall), %s" % (
                    st, mm.group(2), k, al, k, d0, d0 + BLOCK_PITCH,
                    "starting at the wall side" if mm.group(2) == "block" else "ending at the field-centre side"),
                    inpitch and edge, "%.4f-%.4f in from the %s wall" % (d[0], d[1], al))
            add("%s: body name names the %s alliance segment it occupies" % (st, al), bool(mm) and mm.group(1) == al,
                r["name"])
            add("%s: band width 1.0" % st, _close(b[5] - b[2], LED_W, 1e-6), "Z %.4f..%.4f" % (b[2], b[5]))
            add("%s: lens centre 19.0 above the carpet" % st, _close((b[2] + b[5]) / 2, LED_Z, 1e-6),
                "centre %.4f" % ((b[2] + b[5]) / 2))
            add("%s: clears the 20-in guardrail top (CRITICAL)" % st, b[5] < GUARD_H - 1e-6,
                "lens top %.4f, clearance %.4f" % (b[5], GUARD_H - b[5]))
            if top:
                tb = f.bbox(top)
                inside = all(tb[k] - 1e-6 <= b[k] for k in range(3)) and all(b[k] <= tb[k] + 1e-6 for k in range(3, 6))
                add("%s: let into the top rail (inside the rail envelope)" % st, inside,
                    "LED %s rail %s" % (_fmt(b), _fmt(tb)))
                add("%s: no interference with the top rail" % st, f.common_volume([r], top) < 1e-6,
                    "%.6f in^3" % f.common_volume([r], top))
                # rail material remains above the lens along its length (band let in, not cut through)
                ymid = (b[1] + b[4]) / 2
                pts = [(x, ymid, (b[5] + GUARD_H) / 2) for x in (b[0] + 1, (b[0] + b[3]) / 2, b[3] - 1)]
                add("%s: top rail continues above the lens" % st, all(f.inside(top, p) for p in pts),
                    "probe points %s" % pts)
            # inward-facing: the lens face lies on the field-side plane Y = y_edge
            face_y = b[4] if sgn < 0 else b[1]
            add("%s: lens face flush with the field-side face (Y %g), facing inward" % (st, y_edge),
                _close(face_y, y_edge, 1e-6), "lens face at Y %.6f" % face_y)
            xm = (b[0] + b[3]) / 2
            p_in = (xm, y_edge - sgn * 0.01, LED_Z)
            p_out = (xm, y_edge + sgn * 0.01, LED_Z)
            add("%s: lens is the surface seen from the field at Z 19" % st,
                _close(f.dist_point([r], p_in), 0.01, 1e-6) and f.inside([r], p_out),
                "dist from field side %.4f; lens behind face %s" % (f.dist_point([r], p_in), f.inside([r], p_out)))
            mt = r["mat"]
            add("%s: frosted acrylic lens material" % st,
                "acrylic" in mt["name"].lower() and 1150 <= mt["density"] <= 1220,
                "%s %.0f kg/m^3" % (mt["name"], mt["density"]))

        # nothing on the field side hides the band (a 12-in deep probe in front of the lens)
        if leds:
            yy = (y_edge, y_edge + 12) if sgn < 0 else (y_edge - 12, y_edge)
            probe = _box((0, yy[0], LED_Z - LED_W / 2), (FIELD_L, yy[1], LED_Z + LED_W / 2))
            pb = _bb_shape(probe)
            hide = []
            for r in allrecs:
                for s in r["solids"]:
                    if _overlap(_bb_shape(s), pb) and _common_vol(s, probe) > 1e-6:
                        hide.append(r["name"])
            add("%s: nothing stands in front of the LED band (12-in probe)" % tag, not hide, "; ".join(hide[:6]))

        # guardrail interferes with nothing
        hits = []
        mine = set(id(r) for r in rs)
        for r in rs:
            for s in r["solids"]:
                sb = _bb_shape(s)
                for o in allrecs:
                    if id(o) in mine:
                        continue
                    for so in o["solids"]:
                        if _overlap(sb, _bb_shape(so)) and _common_vol(s, so) > 1e-4:
                            hits.append("%s x %s" % (r["name"], o["name"]))
        add("%s: no interference with any other body" % tag, not hits, "; ".join(hits[:6]))

        # perimeter closure: the guardrail meets the carpet edge and both alliance walls
        add("%s: meets the carpet edge" % tag, f.dist(rs, carpet) < 1e-6, "gap %.6f" % f.dist(rs, carpet))
        for wn in ("BLUE", "RED"):
            try:
                w = f.find(r"re:^%s alliance wall" % wn)
            except KeyError:
                add("%s: meets the %s alliance wall" % (tag, wn), False, "wall not built")
                continue
            d = f.dist(rs, w)
            add("%s: meets the %s alliance wall (perimeter closed)" % (tag, wn), d < 1e-6, "gap %.6f" % d)

    # ---- symmetry: the Y = 324 guardrail is the Y = 0 guardrail rotated 180 deg about (324, 162)
    a = sides["Y0"]["rs"]
    b = sides["Y324"]["rs"]

    def sig(r, rot):
        bb = f.bbox([r])
        if rot:
            bb = _rot_bb(bb)
        nmx = r["name"].split(") ", 1)[-1]
        if "FIELD LED" in nmx:
            # blocks count from their own alliance wall, so the rotation maps BLUE block k onto
            # RED block k: swap the alliance names
            if rot:
                nmx = nmx.replace("BLUE", "#").replace("RED", "BLUE").replace("#", "RED")
        else:
            # " 1", " 2", ... is the creation-order suffix numberSharedNames gives shared names
            # (posts, glazing bays); it carries no position, so the rotation ignores it
            nmx = re.sub(r" \d+$", "", nmx)
        return (nmx, tuple(round(v, 4) for v in bb), round(f.volume([r]), 3))

    sa = sorted(sig(r, True) for r in a)
    sb = sorted(sig(r, False) for r in b)
    miss = [x for x in sa if x not in sb] + [x for x in sb if x not in sa]
    add("guardrail Y = 324 is the 180-degree rotation of guardrail Y = 0 (incl. LED alliance segments)",
        not miss and len(sa) == len(sb), "; ".join(str(m) for m in miss[:4]) or "%d parts each" % len(sa))

    # four segments in total: each alliance has one on each side of the field, three blocks each
    segs = f.find(r"re:FIELD LED, (BLUE|RED) segment block \d+$")
    gaps_all = f.find(r"re:FIELD LED, (BLUE|RED) segment gap \d+$")

    def seg_key(g, r):
        bb = g.bbox([r])
        return ("BLUE" if bb[3] <= CX + 1e-6 else "RED", "Y0" if bb[4] <= 0 + 1e-6 else "Y324")

    per = {}
    for r in segs:
        per.setdefault(seg_key(f, r), []).append(r)
    want_keys = [("BLUE", "Y0"), ("BLUE", "Y324"), ("RED", "Y0"), ("RED", "Y324")]
    add("FIELD LEDs: 4 alliance segments of %d blocks, each alliance one on each long side (manual §3.1.2)" % LED_BLOCKS,
        sorted(per) == want_keys and all(len(v) == LED_BLOCKS for v in per.values()),
        "; ".join("%s/%s: %d blocks" % (k[0], k[1], len(v)) for k, v in sorted(per.items())))
    total = sum(f.bbox([r])[3] - f.bbox([r])[0] for r in segs + gaps_all)
    add("FIELD LEDs: each band (blocks and gaps) runs the full 648 in (2 x 648 in total)", _close(total, 2 * FIELD_L, 1e-6),
        "total %.4f" % total)

    # =========================================================================================
    # FIELD LED states (manual §3.1.2, §4.3.1; R207) -- rebuild the perimeter with each option
    # =========================================================================================
    base = dict(walls=False, crags=False, headwalls=False, tape=False, tags=False, decals=False,
                staged=False, stock=False)
    dark_rgb = f.color(segs)[0]
    lum = 0.2126 * dark_rgb[0] + 0.7152 * dark_rgb[1] + 0.0722 * dark_rgb[2]
    lit_cols = [pal[k][0] for k in ("led-green", "neutral-white", "alliance-blue", "alliance-red") if k in pal]
    add("LED state DARK (default): all %d blocks and %d gaps dark and not a lit-state colour" % (len(segs), len(gaps_all)),
        len(set(tuple(r["rgb"]) for r in segs + gaps_all)) == 1 and lum < 64 and tuple(dark_rgb) not in lit_cols
        and all(r["alpha"] == 1.0 for r in segs + gaps_all),
        "rgb %s (luminance %.0f/255)" % (dark_rgb, lum))

    def wall_dist(al, bb):
        """distance of a block's near end from its own alliance wall"""
        return bb[0] if al == "BLUE" else FIELD_L - bb[3]

    from inspect_field import Field
    # manual §3.1.2 / §4.3.1: FORECAST W / I / G -> 1 / 2 / 3 white blocks in BOTH alliances' segments;
    # ROUTE LOW / MID / HIGH -> 1 / 2 / 3 blocks in that alliance's colour; GREEN -> the segment lit green
    cnt = {"WHITEOUT": 1, "ICEFALL": 2, "GALE": 3, "LOW": 1, "MID": 2, "HIGH": 3}
    cases = [("GREEN", {}, lambda al: (pal["led-green"][0], LED_BLOCKS), "#3FBF4F, all %d blocks" % LED_BLOCKS)]
    for fc in ("WHITEOUT", "ICEFALL", "GALE"):
        cases.append(("FORECAST", {"forecast": fc},
                      (lambda n: lambda al: (pal["neutral-white"][0], n))(cnt[fc]),
                      "%s: %d white #F5F5F5 block(s) per segment" % (fc, cnt[fc])))
    for rb, rr in (("LOW", "HIGH"), ("MID", "LOW"), ("HIGH", "MID")):
        cases.append(("ROUTE", {"routeBlue": rb, "routeRed": rr},
                      (lambda nb, nr: lambda al: (pal["alliance-blue"][0], nb) if al == "BLUE"
                       else (pal["alliance-red"][0], nr))(cnt[rb], cnt[rr]),
                      "BLUE %s: %d blue block(s), RED %s: %d red block(s)" % (rb, cnt[rb], rr, cnt[rr])))
    pattern = {}
    for state, extra, fn, what in cases:
        opt = dict(base)
        opt.update(extra)
        try:
            g = Field(fieldLed=state, **opt)
        except Exception as e:  # noqa: BLE001
            add("LED state %s %s: builds" % (state, what), False, "%s: %s" % (type(e).__name__, e))
            continue
        ss = g.find(r"re:FIELD LED, (BLUE|RED) segment block \d+$")
        gs = g.find(r"re:FIELD LED, (BLUE|RED) segment gap \d+$")
        bysg, gbysg = {}, {}
        for r in ss:
            bysg.setdefault(seg_key(g, r), []).append(r)
        for r in gs:
            gbysg.setdefault(seg_key(g, r), []).append(r)
        bad = [r["name"] + " lit" for r in gs if tuple(r["rgb"]) != tuple(dark_rgb)]
        for key in want_keys:
            al = key[0]
            on_rgb, n = fn(al)
            blks = sorted(bysg.get(key, []), key=lambda r: wall_dist(al, g.bbox([r])))
            if len(blks) != LED_BLOCKS:
                bad.append("%s/%s: %d blocks" % (key[0], key[1], len(blks)))
                continue
            for i, r in enumerate(blks):
                want = on_rgb if i < n else dark_rgb
                if tuple(r["rgb"]) != tuple(want) or r["alpha"] != 1.0:
                    bad.append("%s: %s a %s, want %s (%s)" % (r["name"], r["rgb"], r["alpha"], want,
                                                             "lit" if i < n else "dark"))
            # lit / dark runs along the segment, measured from the geometry over blocks and gaps
            # (abutting lit bodies read as one bar)
            runs = []
            for r in sorted(blks + gbysg.get(key, []), key=lambda r: wall_dist(al, g.bbox([r]))):
                bb = g.bbox([r])
                lit = tuple(r["rgb"]) != tuple(dark_rgb)
                lo_, hi_ = wall_dist(al, bb), wall_dist(al, bb) + (bb[3] - bb[0])
                if lit and runs and _close(runs[-1][1], lo_, 1e-6):
                    runs[-1][1] = hi_
                elif lit:
                    runs.append([lo_, hi_])
            short = extra.get("forecast") or extra.get("routeBlue" if al == "BLUE" else "routeRed") or state
            pattern.setdefault(state, []).append((short, key, n, runs))
        # across the whole band: no lit run straddles X 324, so the two segments stay separately countable
        for yk in ("Y0", "Y324"):
            band = sorted(bysg.get(("BLUE", yk), []) + gbysg.get(("BLUE", yk), []) + bysg.get(("RED", yk), [])
                          + gbysg.get(("RED", yk), []), key=lambda r: g.bbox([r])[0])
            lit_at = [(g.bbox([r])[0], g.bbox([r])[3]) for r in band if tuple(r["rgb"]) != tuple(dark_rgb)]
            cross = [q for q in lit_at if q[0] < CX - 1e-6 < q[1] or _close(q[1], CX, 1e-6) or _close(q[0], CX, 1e-6)]
            if cross:
                bad.append("%s: lit body at X 324: %s" % (yk, cross))
        add("LED state %s (%s): every block in the document colour, lit blocks counted from the own wall (ref)"
            % (state, what), not bad, "; ".join(bad[:4]) or "%d blocks" % len(ss))
        # other guardrail parts keep their appearance
        gr = [r for r in g.find(r"re:^Guardrail \(") if "FIELD LED" not in r["name"]]
        chg = [r["name"] for r in gr if tuple(r["rgb"]) not in (pal["wall"][0], pal["glazing"][0])]
        add("LED state %s (%s): only the LED lenses change colour" % (state, what), not chg, "; ".join(chg[:4]))

    # manual §3.1.2 / §4.3.1 and R207: FORECAST and ROUTE are shown as a countable row of one, two
    # or three "equal, discrete, separated lit blocks"; R207 contrasts that with a continuous strip.
    # Count the separated lit runs per segment (abutting lit blocks merge into one bar).
    for state in ("FORECAST", "ROUTE"):
        rows = pattern.get(state, [])
        bad = []
        for what, key, n, runs in rows:
            lens = [b - a for a, b in runs]
            if len(runs) != n or (lens and max(lens) - min(lens) > 1e-6):
                bad.append("%s %s/%s: %d lit block(s) wanted, %d separated lit run(s) %s in" % (
                    what, key[0], key[1], n, len(runs), "/".join("%.0f" % x for x in lens)))
        add("LED state %s: each segment shows a countable 1/2/3 pattern of equal, separated lit blocks "
            "(R207 / manual §3.1.2), not a continuous bar" % state, rows and not bad,
            "; ".join(bad[:6]) or "%d segment patterns" % len(rows))
    return out
