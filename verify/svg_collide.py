# -*- coding: utf-8 -*-
"""Layout check for the six generated drawing sheets (03-field/renderings/*.svg).

The sheets print on landscape ANSI C plates with the image 21 in wide
(06-style/pdf/plates.css), so one SVG user unit prints at 1512 / viewBox-width pt.
For every sheet this script models each <text> element as an oriented box
(advance widths of Arial / Liberation Sans, the face the plates are rendered
with; rotate/translate/matrix transforms on the text and on enclosing groups are
applied), samples the outline of every stroked or filled shape, and reports:

  OVERLAP     two text boxes overlap
  OFF-SHEET   a text box leaves the viewBox
  HIDDEN      a text is painted over by an opaque shape drawn after it
  CROSSES     a line, arrowhead, shape edge or panel border runs through a text box
              (geometry painted before a text that masks it - a white halo or a
              CRITICAL value box - does not count; the mask is drawn over it)
  SMALL       text prints below 7 pt, or a dimension value (#C02020) or a bold
              label below 8 pt (MANUAL-STYLE-GUIDE.md sets a hard 6-pt floor)
  LEADER      a callout leader (#E100E1) crosses another leader or a dimension or
              extension line, has no label at its tail, or has its arrowhead at the
              label end instead of the feature end (MANUAL-STYLE-GUIDE.md §7.3)
  ARROWHEAD   a filled arrowhead prints smaller than 3 pt in length or width

Deterministic, standard library only, silent apart from one summary line per
sheet on a clean set.
"""
import glob
import io
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

PLATE_PT = 21.0 * 72.0
MIN_PT, MIN_PT_DIM, MIN_PT_BOLD = 7.0, 8.0, 8.0
MIN_HEAD_PT = 3.0
DIM, LEADER = '#c02020', '#e100e1'
NS = '{http://www.w3.org/2000/svg}'

# Arial / Liberation Sans advance widths, 1/1000 em
_CH = (" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"
       "abcdefghijklmnopqrstuvwxyz{|}~")
_REG = dict(zip(_CH, [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278]
                + [556] * 10 + [278, 278, 584, 584, 584, 556, 1015,
                                667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
                                722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611,
                                278, 278, 278, 469, 556, 333,
                                556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
                                556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500,
                                334, 260, 334, 584]))
_BOLD = dict(zip(_CH, [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278]
                 + [556] * 10 + [333, 333, 584, 584, 584, 611, 975,
                                 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833,
                                 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611,
                                 333, 278, 333, 584, 556, 333,
                                 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889,
                                 611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500,
                                 389, 280, 389, 584]))
DESC = set("gjpqy(),;[]{}|_")


def text_width(s, size, bold):
    tab = _BOLD if bold else _REG
    return sum(tab.get(c, 1000 if ord(c) > 0x2000 else 600) for c in s) * size / 1000.0


# ------------------------------------------------------------ affine helpers
def mul(a, b):
    return (a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1],
            a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3],
            a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5])


def apply(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


IDENT = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def parse_transform(t):
    m = IDENT
    for name, args in re.findall(r'(\w+)\s*\(([^)]*)\)', t or ''):
        v = [float(a) for a in re.split(r'[\s,]+', args.strip()) if a]
        if name == 'rotate':
            a = math.radians(v[0])
            c, s = math.cos(a), math.sin(a)
            r = (c, s, -s, c, 0.0, 0.0)
            if len(v) == 3:
                r = mul(mul((1, 0, 0, 1, v[1], v[2]), r), (1, 0, 0, 1, -v[1], -v[2]))
            m = mul(m, r)
        elif name == 'translate':
            m = mul(m, (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0.0))
        elif name == 'scale':
            m = mul(m, (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0))
        elif name == 'matrix':
            m = mul(m, tuple(v))
    return m


def fnum(e, k, d=0.0):
    try:
        return float(str(e.get(k, d)).replace('px', ''))
    except ValueError:
        return d


# ------------------------------------------------------------ outlines
def arc_points(x1, y1, rx, ry, phi, fa, fs, x2, y2):
    """SVG elliptical arc (endpoint form) sampled to points."""
    if rx == 0 or ry == 0:
        return [(x2, y2)]
    cp, sp = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (x1 - x2) / 2.0, (y1 - y2) / 2.0
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    rx, ry = abs(rx), abs(ry)
    lam = (x1p / rx) ** 2 + (y1p / ry) ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    co = math.sqrt(max(0.0, num / den)) if den else 0.0
    if fa == fs:
        co = -co
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx = cp * cxp - sp * cyp + (x1 + x2) / 2.0
    cy = sp * cxp + cp * cyp + (y1 + y2) / 2.0

    def ang(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a
    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    n = max(4, int(abs(dt) * max(rx, ry)))
    out = []
    for i in range(1, n + 1):
        t = t1 + dt * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cp * x - sp * y + cx, sp * x + cp * y + cy))
    return out


def path_polylines(d):
    """Sub-paths of an SVG path as lists of points (M L H V Q C A Z, abs/rel)."""
    toks = re.findall(r'[MmLlHhVvQqCcAaZz]|-?\d*\.?\d+(?:e-?\d+)?', d)
    subs, cur, i = [], [], 0
    x = y = sx = sy = 0.0
    cmd = None
    while i < len(toks):
        if re.match(r'[A-Za-z]', toks[i]):
            cmd = toks[i]
            i += 1
            if cmd in 'Zz':
                cur.append((sx, sy))
                x, y = sx, sy
                continue
        rel = cmd.islower()
        c = cmd.upper()
        nargs = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'Q': 4, 'C': 6, 'A': 7}[c]
        v = [float(t) for t in toks[i:i + nargs]]
        i += nargs
        if c == 'M':
            if cur:
                subs.append(cur)
            x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1])
            sx, sy = x, y
            cur = [(x, y)]
            cmd = 'l' if rel else 'L'
        elif c == 'L':
            x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1])
            cur.append((x, y))
        elif c == 'H':
            x = x + v[0] if rel else v[0]
            cur.append((x, y))
        elif c == 'V':
            y = y + v[0] if rel else v[0]
            cur.append((x, y))
        elif c in 'QC':
            pts = [(x + v[k], y + v[k + 1]) if rel else (v[k], v[k + 1]) for k in range(0, nargs, 2)]
            ctrl = [(x, y)] + pts
            for k in range(1, 17):
                t = k / 16.0
                if c == 'Q':
                    (a, b), (p, q), (r, s_) = ctrl
                    cur.append(((1 - t) ** 2 * a + 2 * (1 - t) * t * p + t * t * r,
                                (1 - t) ** 2 * b + 2 * (1 - t) * t * q + t * t * s_))
                else:
                    (a, b), (p, q), (r, s_), (u, w) = ctrl
                    cur.append(((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * p + 3 * (1 - t) * t * t * r + t ** 3 * u,
                                (1 - t) ** 3 * b + 3 * (1 - t) ** 2 * t * q + 3 * (1 - t) * t * t * s_ + t ** 3 * w))
            x, y = pts[-1]
        elif c == 'A':
            ex, ey = (x + v[5], y + v[6]) if rel else (v[5], v[6])
            cur.extend(arc_points(x, y, v[0], v[1], v[2], int(v[3]), int(v[4]), ex, ey))
            x, y = ex, ey
    if cur:
        subs.append(cur)
    return subs


def outline(e, tag):
    """Outline of a shape in its own user space, as polylines."""
    if tag == 'line':
        return [[(fnum(e, 'x1'), fnum(e, 'y1')), (fnum(e, 'x2'), fnum(e, 'y2'))]]
    if tag == 'rect':
        x, y, w, h = fnum(e, 'x'), fnum(e, 'y'), fnum(e, 'width'), fnum(e, 'height')
        return [[(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]]
    if tag in ('circle', 'ellipse'):
        cx, cy = fnum(e, 'cx'), fnum(e, 'cy')
        rx = fnum(e, 'r') if tag == 'circle' else fnum(e, 'rx')
        ry = fnum(e, 'r') if tag == 'circle' else fnum(e, 'ry')
        n = max(16, int(2 * math.pi * max(rx, ry)))
        return [[(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n))
                 for k in range(n + 1)]]
    if tag == 'path':
        return path_polylines(e.get('d', ''))
    if tag in ('polygon', 'polyline'):
        v = [float(a) for a in re.split(r'[\s,]+', e.get('points', '').strip()) if a]
        pts = list(zip(v[0::2], v[1::2]))
        return [pts + (pts[:1] if tag == 'polygon' else [])]
    return []


def densify(poly, step=1.0):
    out = []
    for (x1, y1), (x2, y2) in zip(poly, poly[1:]):
        n = max(1, int(math.hypot(x2 - x1, y2 - y1) / step))
        for k in range(n):
            out.append((x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n))
    if poly:
        out.append(poly[-1])
    return out


# ------------------------------------------------------------ geometry tests
def quad_axes(q):
    return [(q[1][0] - q[0][0], q[1][1] - q[0][1]), (q[3][0] - q[0][0], q[3][1] - q[0][1])]


def sat(a, b, pad):
    for ax, ay in quad_axes(a) + quad_axes(b):
        L = math.hypot(ax, ay) or 1.0
        ax, ay = ax / L, ay / L
        pa = [p[0] * ax + p[1] * ay for p in a]
        pb = [p[0] * ax + p[1] * ay for p in b]
        if max(pa) - pad <= min(pb) or max(pb) - pad <= min(pa):
            return False
    return True


def in_quad(q, p, grow):
    ux, uy = q[1][0] - q[0][0], q[1][1] - q[0][1]
    vx, vy = q[3][0] - q[0][0], q[3][1] - q[0][1]
    lu, lv = math.hypot(ux, uy) or 1.0, math.hypot(vx, vy) or 1.0
    dx, dy = p[0] - q[0][0], p[1] - q[0][1]
    su, sv = (dx * ux + dy * uy) / lu, (dx * vx + dy * vy) / lv
    return -grow < su < lu + grow and -grow < sv < lv + grow


def seg_cross(p1, p2, p3, p4):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = orient(p3, p4, p1), orient(p3, p4, p2)
    d3, d4 = orient(p1, p2, p3), orient(p1, p2, p4)
    return (d1 * d2 < 0) and (d3 * d4 < 0)


def seg_dist(p, a, b):
    ax, ay = b[0] - a[0], b[1] - a[1]
    L2 = ax * ax + ay * ay or 1.0
    t = max(0.0, min(1.0, ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / L2))
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * ay)


def point_in_poly(p, poly):
    x, y = p
    inside = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


# ------------------------------------------------------------ sheet model
def load(path):
    src = io.open(path, encoding='utf-8').read()
    root = ET.fromstring(src)
    vb = [float(v) for v in root.get('viewBox').split()]
    texts, shapes = [], []
    order = [0]

    def walk(e, m, inherited):
        tag = e.tag.replace(NS, '')
        if tag == 'defs':
            return
        mm = mul(m, parse_transform(e.get('transform')))
        order[0] += 1
        idx = order[0]
        style = dict(inherited)
        for k in ('fill', 'stroke', 'stroke-width', 'font-size', 'font-weight', 'text-anchor',
                  'paint-order', 'opacity'):
            if e.get(k) is not None:
                style[k] = e.get(k)
        if tag == 'text':
            body = ''.join(e.itertext())
            if body.strip():
                texts.append(dict(el=e, s=body, m=mm, idx=idx, style=style))
            return
        if tag in ('line', 'rect', 'circle', 'ellipse', 'path', 'polygon', 'polyline'):
            shapes.append(dict(el=e, tag=tag, m=mm, idx=idx, style=style))
        for c in list(e):
            walk(c, mm, style)

    walk(root, IDENT, {})
    return vb, texts, shapes


def text_quad(t):
    e, st = t['el'], t['style']
    size = float(str(st.get('font-size', '10')).replace('px', ''))
    bold = st.get('font-weight') in ('bold', '700', '800', '900')
    x, y = fnum(e, 'x'), fnum(e, 'y')
    w = text_width(t['s'], size, bold)
    anch = st.get('text-anchor', 'start')
    x0 = x - w / 2.0 if anch == 'middle' else (x - w if anch == 'end' else x)
    trim = 0.03 * size                       # side bearings
    top = y - 0.73 * size                    # cap height and parentheses
    bot = y + (0.2 * size if any(c in DESC for c in t['s']) else 0.02 * size)
    pts = [(x0 + trim, top), (x0 + w - trim, top), (x0 + w - trim, bot), (x0 + trim, bot)]
    t['q'] = [apply(t['m'], px, py) for px, py in pts]
    t['size'], t['bold'] = size, bold
    t['anchor_pt'] = apply(t['m'], x, y)
    return t


def masks(t, shapes_by_idx):
    """Does this text paint an opaque mask (halo, or a CRITICAL value box) over
    geometry drawn before it?"""
    if t['style'].get('paint-order', '').startswith('stroke') and t['el'].get('stroke'):
        return True
    prev = shapes_by_idx.get(t['idx'] - 1)
    return (prev is not None and prev['tag'] == 'rect'
            and (prev['el'].get('fill') or '').lower() == '#ffffff'
            and (prev['el'].get('stroke') or '').lower() == DIM)


def check(path):
    vb, texts, shapes = load(path)
    k = PLATE_PT / vb[2]
    for t in texts:
        text_quad(t)
    by_idx = {s['idx']: s for s in shapes}
    issues = []

    # 1. text / text
    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            if sat(a['q'], b['q'], 0.3):
                issues.append(('OVERLAP', '%r  <->  %r' % (a['s'][:40], b['s'][:40])))
    # 2. off sheet
    for t in texts:
        if any(p[0] < vb[0] or p[1] < vb[1] or p[0] > vb[0] + vb[2] or p[1] > vb[1] + vb[3]
               for p in t['q']):
            issues.append(('OFF-SHEET', repr(t['s'][:56])))
    # 3. text / geometry
    for s in shapes:
        e, st = s['el'], s['style']
        stroke = (st.get('stroke') or 'none').lower()
        fill = (st.get('fill') or 'none').lower()
        if e.get('x') is None and s['tag'] == 'rect' and fnum(e, 'width') >= vb[2]:
            continue                                   # sheet background
        if stroke == 'none' and fill == 'none':
            continue
        sw = fnum(e, 'stroke-width', 1.0) if stroke != 'none' else 0.0
        pts = []
        for poly in outline(e, s['tag']):
            pts.extend(apply(s['m'], x, y) for x, y in densify(poly))
        s['pts'] = pts
        xs = [p[0] for p in pts] or [0]
        ys = [p[1] for p in pts] or [0]
        bb = (min(xs) - sw, min(ys) - sw, max(xs) + sw, max(ys) + sw)
        for t in texts:
            q = t['q']
            if (max(p[0] for p in q) < bb[0] or min(p[0] for p in q) > bb[2]
                    or max(p[1] for p in q) < bb[1] or min(p[1] for p in q) > bb[3]):
                continue
            if s['idx'] < t['idx'] and masks(t, by_idx):
                continue
            if any(in_quad(q, p, sw / 2.0) for p in pts):
                what = s['tag'] + ' ' + (stroke if stroke != 'none' else 'fill ' + fill)
                issues.append(('CROSSES', '%r  x  %s' % (t['s'][:48], what)))
    # 3b. text painted over by a later opaque shape
    for s in shapes:
        fill = (s['style'].get('fill') or 'none').lower()
        op = fnum(s['el'], 'opacity', 1.0) * fnum(s['el'], 'fill-opacity', 1.0)
        if fill == 'none' or op < 0.5 or s['tag'] == 'line' or 'pts' not in s:
            continue
        polys = [[apply(s['m'], x, y) for x, y in poly] for poly in outline(s['el'], s['tag'])]
        for t in texts:
            if t['idx'] > s['idx']:
                continue
            cx = sum(p[0] for p in t['q']) / 4.0
            cy = sum(p[1] for p in t['q']) / 4.0
            if any(point_in_poly((cx, cy), poly) for poly in polys):
                issues.append(('HIDDEN', '%r under a later %s fill %s' % (t['s'][:48], s['tag'], fill)))
    # 4. printed size
    for t in texts:
        pt = t['size'] * k
        fill = (t['style'].get('fill') or '').lower()
        need = MIN_PT_DIM if fill == DIM else (MIN_PT_BOLD if t['bold'] else MIN_PT)
        if pt < need - 0.01:                           # sizes are written to 0.01 unit
            issues.append(('SMALL', '%.2f pt < %.1f  %r' % (pt, need, t['s'][:48])))
    # 5. leaders
    leads = [s for s in shapes if s['tag'] == 'line'
             and (s['style'].get('stroke') or '').lower() == LEADER]
    heads = [s for s in shapes if s['tag'] == 'path'
             and (s['style'].get('fill') or '').lower() == LEADER]
    dimlines = [s for s in shapes if s['tag'] in ('line', 'path')
                and (s['style'].get('stroke') or '').lower() == DIM]

    def segs(s):
        out = []
        for poly in outline(s['el'], s['tag']):
            poly = [apply(s['m'], x, y) for x, y in poly]
            out.extend(zip(poly, poly[1:]))
        return out
    for i, a in enumerate(leads):
        sa = segs(a)[0]
        for b in leads[i + 1:]:
            if seg_cross(sa[0], sa[1], *segs(b)[0]):
                issues.append(('LEADER', 'two leaders cross near (%.0f, %.0f)' % sa[1]))
        for d in dimlines:
            if any(seg_cross(sa[0], sa[1], p, q) for p, q in segs(d)):
                issues.append(('LEADER', 'leader crosses a dimension/extension line near (%.0f, %.0f)' % sa[1]))
                break
        # which end carries the arrowhead? an SVG marker says so directly; a drawn
        # head is the filled triangle nearest one end
        if a['el'].get('marker-start') or a['el'].get('marker-end'):
            at_start = bool(a['el'].get('marker-start')) and not a['el'].get('marker-end')
            head_end, tail_end = (sa[0], sa[1]) if at_start else (sa[1], sa[0])
        else:
            cent = [tuple(sum(c) / 3.0 for c in zip(*path_polylines(h['el'].get('d'))[0][:3]))
                    for h in heads]
            dist = [min([math.hypot(c[0] - p[0], c[1] - p[1]) for c in cent] or [1e9]) for p in sa]
            head_end, tail_end = (sa[1], sa[0]) if dist[1] <= dist[0] else (sa[0], sa[1])
        near = [t for t in texts if min(math.hypot(p[0] - tail_end[0], p[1] - tail_end[1])
                                        for p in t['q'] + [t['anchor_pt']]) < 8.0
                or in_quad(t['q'], tail_end, 6.0)]
        if not near:
            issues.append(('LEADER', 'no label at the tail of the leader ending (%.0f, %.0f)' % head_end))
        if any(in_quad(t['q'], head_end, 1.0) for t in texts):
            issues.append(('LEADER', 'arrowhead lands on text at (%.0f, %.0f)' % head_end))
    # 6. arrowheads: filled triangles
    for s in shapes:
        if s['tag'] != 'path' or (s['style'].get('fill') or 'none').lower() == 'none':
            continue
        subs = path_polylines(s['el'].get('d', ''))
        if len(subs) != 1 or len(subs[0]) != 4:
            continue
        a, b, c = [apply(s['m'], *p) for p in subs[0][:3]]
        sides = sorted([(math.hypot(b[0] - c[0], b[1] - c[1]), a, b, c),
                        (math.hypot(a[0] - c[0], a[1] - c[1]), b, a, c),
                        (math.hypot(a[0] - b[0], a[1] - b[1]), c, a, b)])
        base, tip, p, q = sides[0]
        length = math.hypot(tip[0] - (p[0] + q[0]) / 2.0, tip[1] - (p[1] + q[1]) / 2.0)
        if length * k < MIN_HEAD_PT - 1e-6 or base * k < MIN_HEAD_PT - 1e-6:
            issues.append(('ARROWHEAD', '%.1f x %.1f pt at (%.0f, %.0f)' % (length * k, base * k, tip[0], tip[1])))
    sizes = [t['size'] * k for t in texts]
    return vb, len(texts), (min(sizes) if sizes else 0.0), issues


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    fails = 0
    for f in sorted(glob.glob('03-field/renderings/*.svg')):
        vb, n, mn, issues = check(f)
        kinds = {}
        for kind, _ in issues:
            kinds[kind] = kinds.get(kind, 0) + 1
        print("%-22s texts=%3d  min %.2f pt at 21 in  issues=%d%s"
              % (os.path.basename(f), n, mn, len(issues),
                 ("  (" + ", ".join("%s %d" % kv for kv in sorted(kinds.items())) + ")") if issues else ""))
        for kind, msg in issues[:40]:
            print("    %-10s %s" % (kind, msg))
        fails += len(issues)
    print("\nTOTAL layout issues: %d" % fails)
    sys.exit(0)


if __name__ == '__main__':
    main()
