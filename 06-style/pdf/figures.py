# -*- coding: utf-8 -*-
"""
Finish the rendered figures: trim, size for the page, and place the callouts.

    python 06-style/pdf/figures.py <render dir> <figure-shots.json> <out dir>

For every shot in figure-shots.json it takes <render dir>/<name>.png (written by the three.js
stage), trims the white margin, scales it to at most 2100 px wide (7 in at 300 dpi) and writes
<out dir>/<name>.png.  Shots with "callouts" also get <out dir>/<name>.callouts.json: each
callout's anchor, a point in field coordinates (inches, Z up), projected through the same
camera the stage used, and its label position: the anchor moved by "offset" [dx, dy], given as
fractions of the finished image's width, or the first nearby position that passes the layout
checks in layout().
make_html.py draws the callouts over the image as vector leaders and labels.
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops

MAX_W = 2100
PAD = 24


def three(p):
    """Field inches (x, y, z; Z up) -> the stage's glTF axes (x, z, -y; Y up)."""
    return np.array([p[0], p[2], -p[1]], dtype=float)


def project(shot, p):
    """Pixel position of field point p in the raw render, as three.js PerspectiveCamera.lookAt."""
    w, h = shot["width"], shot["height"]
    eye, tgt = three(shot["eye"]), three(shot["target"])
    z = eye - tgt
    z /= np.linalg.norm(z)
    x = np.cross([0.0, 1.0, 0.0], z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    d = three(p) - eye
    cx, cy, cz = d @ x, d @ y, d @ z
    if cz >= 0:
        raise ValueError("%s: callout point %s is behind the camera" % (shot["name"], p))
    t = math.tan(math.radians(shot.get("fov", 35)) / 2)
    nx = (cx / -cz) / (t * w / h)
    ny = (cy / -cz) / t
    return (nx + 1) / 2 * w, (1 - ny) / 2 * h


# Callouts as printed: the figure spans the 7.00-in (504-pt) column; labels are 8.5-pt Roboto
# Medium in a white box, leaders 1.5 pt with a 3-pt arrowhead (MANUAL-STYLE-GUIDE.md §7.3, §9.2).
COLUMN_PT = 504.0
LABEL_PT = 8.5
LEADER_PT = 1.5
BOX_PAD_PT = 2.5


def text_width_em(text):
    """Approximate advance width of Roboto Medium, in em."""
    w = 0.0
    for ch in text:
        if ch == " ":
            w += 0.25
        elif ch.isupper() or ch.isdigit():
            w += 0.64
        elif ch in "il.,:;'|!":
            w += 0.26
        else:
            w += 0.53
    return w


def _seg_intersect(p1, p2, p3, p4):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = orient(p3, p4, p1), orient(p3, p4, p2)
    d3, d4 = orient(p1, p2, p3), orient(p1, p2, p4)
    return d1 * d2 < 0 and d3 * d4 < 0


def _seg_hits_box(p, q, box):
    x0, y0, x1, y1 = box
    if x0 <= p[0] <= x1 and y0 <= p[1] <= y1 or x0 <= q[0] <= x1 and y0 <= q[1] <= y1:
        return True
    edges = [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
    return any(_seg_intersect(p, q, a, b) for a, b in edges)


def _conflicts(a, others, anchors, pad):
    """Problems between candidate label a and already placed labels, and a's box over any anchor."""
    probs = []
    for b in others:
        A, B = a["box"], b["box"]
        if A[0] < B[2] + pad and B[0] < A[2] + pad and A[1] < B[3] + pad and B[1] < A[3] + pad:
            probs.append("labels %r and %r overlap" % (a["text"], b["text"]))
        if _seg_intersect((a["sx"], a["sy"]), (a["x"], a["y"]), (b["sx"], b["sy"]), (b["x"], b["y"])):
            probs.append("leaders of %r and %r cross" % (a["text"], b["text"]))
        if _seg_hits_box((a["sx"], a["sy"]), (a["x"], a["y"]), B):
            probs.append("leader of %r runs through label %r" % (a["text"], b["text"]))
        if _seg_hits_box((b["sx"], b["sy"]), (b["x"], b["y"]), A):
            probs.append("leader of %r runs through label %r" % (b["text"], a["text"]))
    for text, (x, y) in anchors:
        bx = a["box"]
        if text != a["text"] and bx[0] - pad <= x <= bx[2] + pad and bx[1] - pad <= y <= bx[3] + pad:
            probs.append("label %r covers the anchor of %r" % (a["text"], text))
    return probs


def _place(text, ax, ay, lx, ly, bw, bh, w, h, pad, unit):
    lx = min(max(lx, bw / 2 + pad), w - bw / 2 - pad)
    ly = min(max(ly, bh / 2 + pad), h - bh / 2 - pad)
    vx, vy = ax - lx, ay - ly
    t = min(abs(bw / 2 / vx) if vx else 1e9, abs(bh / 2 / vy) if vy else 1e9)
    if t >= 1 or math.hypot(vx, vy) * (1 - t) < 8 * unit:
        return None                               # label on or too close to its own anchor
    return {"text": text, "x": ax, "y": ay, "lx": lx, "ly": ly, "bw": bw, "bh": bh,
            "sx": lx + vx * t, "sy": ly + vy * t, "box": (lx - bw / 2, ly - bh / 2, lx + bw / 2, ly + bh / 2)}


def compass_obstacles(shot, w, ox, oy, s, fs, pad):
    """The plan-view compass (drawn by make_html.py) as fixed items the labels must avoid: its two
    arrows as leaders, and the origin note and axis letters as label boxes."""
    if not shot.get("compass"):
        return []
    o, n = shot["compass"]["origin"], shot["compass"]["length"]
    pts = [project(shot, p) for p in (o, [o[0] + n, o[1], o[2]], [o[0], o[1] + n, o[2]])]
    (x0, y0), (xx, xy), (yx, yy) = [((x - ox) * s, (y - oy) * s) for x, y in pts]
    note = "origin (0, 0) · always-blue-origin NWU"
    nb = (x0 + fs * 0.6, y0 + fs * 0.5, x0 + fs * 0.6 + text_width_em(note) * fs * 0.9, y0 + fs * 1.6)
    items = [{"text": "compass note", "x": x0, "y": y0, "sx": x0, "sy": y0, "box": nb}]
    for ex, ey, t in ((xx, xy, "+X"), (yx, yy, "+Y")):
        lx, ly = ex + (ex - x0) * 0.25, ey + (ey - y0) * 0.25
        items.append({"text": "compass " + t, "x": ex, "y": ey, "sx": x0, "sy": y0,
                      "box": (lx - fs, ly - fs * 0.7, lx + fs, ly + fs * 0.7)})
    return items


def layout(shot, w, h, ox, oy, s):
    """Place the labels: each callout's "offset" is tried first, then a ring of alternatives, and
    the first position that breaks none of the rules is kept.  Rules: every label inside the image,
    no two labels overlapping, no two leaders crossing, no leader through a label, no label over
    an anchor, every leader at least 8 pt long.  Returns (callouts, problems left)."""
    unit = w / COLUMN_PT                      # image pixels per printed point
    fs, pad = LABEL_PT * unit, BOX_PAD_PT * unit
    anchors = []
    for c in shot["callouts"]:
        px, py = project(shot, c["at"])
        ax, ay = (px - ox) * s, (py - oy) * s
        if not (0 <= ax <= w and 0 <= ay <= h):
            raise ValueError("%s: callout %r anchor falls outside the image" % (shot["name"], c["text"]))
        anchors.append((c["text"], (ax, ay)))
    placed, probs = compass_obstacles(shot, w, ox, oy, s, fs, pad), []
    fixed = len(placed)
    for c, (_, (ax, ay)) in zip(shot["callouts"], anchors):
        bw, bh = text_width_em(c["text"]) * fs + 2 * pad, fs * 1.25 + pad
        dx0, dy0 = c["offset"]
        cands = [(dx0, dy0)]
        for r in (0.08, 0.11, 0.14, 0.18, 0.05):
            for k in range(16):
                a = math.atan2(dy0, dx0) + math.pi * k / 8 * (1 if k % 2 else -1) * 0.5
                cands.append((r * math.cos(a), r * math.sin(a)))
        best = None
        for dx, dy in cands:
            it = _place(c["text"], ax, ay, ax + dx * w, ay + dy * w, bw, bh, w, h, pad, unit)
            if it is None:
                continue
            bad = _conflicts(it, placed, anchors, pad)
            if best is None or len(bad) < len(best[1]):
                best = (it, bad)
            if not bad:
                break
        if best is None:
            raise ValueError("%s: no room for label %r" % (shot["name"], c["text"]))
        placed.append(best[0])
        probs += best[1]
    items = []
    for it in placed[fixed:]:
        items.append({k: (round(v, 1) if isinstance(v, float) else v) for k, v in it.items() if k != "box"})
    return items, probs


def finish(src, dst, shot):
    im = Image.open(os.path.join(src, shot["name"] + ".png")).convert("RGB")
    # tone mapping greys the stage's white background: map that flat colour back to white
    a = np.asarray(im).astype(int)
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    colours, counts = np.unique(border, axis=0, return_counts=True)
    bg = colours[np.argmax(counts)]
    flat = np.abs(a - bg).max(axis=2) <= 2
    a[flat] = 255
    im = Image.fromarray(a.astype(np.uint8))
    ox, oy = 0, 0
    box = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).point(lambda v: 255 if v > 8 else 0).getbbox()
    if box:
        pad = shot.get("pad", PAD)
        ox, oy = max(box[0] - pad, 0), max(box[1] - pad, 0)
        im = im.crop((ox, oy, min(box[2] + pad, im.width), min(box[3] + pad, im.height)))
    s = 1.0
    if im.width > MAX_W:
        s = MAX_W / im.width
        im = im.resize((MAX_W, round(im.height * s)), Image.LANCZOS)
    out = os.path.join(dst, shot["name"] + ".png")
    im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(out, optimize=True)
    side = os.path.join(dst, shot["name"] + ".callouts.json")
    if shot.get("callouts"):
        items, probs = layout(shot, im.width, im.height, ox, oy, s)
        data = {"width": im.width, "height": im.height, "font": round(LABEL_PT * im.width / COLUMN_PT, 2),
                "stroke": round(LEADER_PT * im.width / COLUMN_PT, 2), "callouts": items}
        if shot.get("compass"):
            # plan views carry a coordinate compass (MANUAL-STYLE-GUIDE.md §7.2)
            o, n = shot["compass"]["origin"], shot["compass"]["length"]
            pts = [project(shot, p) for p in (o, [o[0] + n, o[1], o[2]], [o[0], o[1] + n, o[2]])]
            data["compass"] = [[round((x - ox) * s, 1), round((y - oy) * s, 1)] for x, y in pts]
        with open(side, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1)
    else:
        probs = []
        if os.path.exists(side):
            os.remove(side)
    return out, im.size, probs


def main():
    src, shots_json, dst = sys.argv[1:4]
    with open(shots_json, encoding="utf-8") as fh:
        shots = json.load(fh)
    os.makedirs(dst, exist_ok=True)
    bad = 0
    for shot in shots:
        out, (w, h), probs = finish(src, dst, shot)
        print("%s  %dx%d  %d KB  %d callouts" % (os.path.relpath(out), w, h, os.path.getsize(out) // 1024,
                                                  len(shot.get("callouts", []))))
        for p in probs:
            print("  CALLOUT PROBLEM: %s" % p)
        bad += len(probs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
