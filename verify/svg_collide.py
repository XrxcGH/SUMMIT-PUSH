# -*- coding: utf-8 -*-
"""Detect text/text collisions and out-of-sheet text in the generated SVG sheets.

Estimates each <text> element's box from its x/y/font-size/text-anchor and the
mean glyph width of the sheet font (~0.52 em for Segoe UI at these sizes), then
reports overlapping pairs and any box escaping the viewBox.  Text inside a
rotated <g> is skipped (reported separately) because the transform is not
modelled.
"""
import glob, io, os, re, sys

MEAN_EM = 0.52          # mean advance width, conservative for mixed case
ASC, DESC = 0.78, 0.22  # cap-height / descender fractions of em

TEXT_RE = re.compile(
    r'<text\b([^>]*)>(.*?)</text>', re.S)
ATTR_RE = re.compile(r'([a-zA-Z-]+)\s*=\s*"([^"]*)"')


def boxes(path):
    src = io.open(path, encoding='utf-8').read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
    out, rotated = [], 0
    # mark spans that sit inside a transformed group
    spans = []
    depth = 0
    for m in re.finditer(r'<g\b([^>]*)>|</g>', src):
        if m.group(0) == '</g>':
            depth = max(0, depth - 1)
        else:
            if 'transform' in (m.group(1) or ''):
                spans.append([m.end(), None, depth])
            depth += 1
    # crude: a transformed group ends at the next </g> after its start
    for sp in spans:
        nxt = src.find('</g>', sp[0])
        sp[1] = nxt if nxt >= 0 else len(src)

    def in_transform(pos):
        return any(a <= pos <= b for a, b, _ in spans)

    for m in TEXT_RE.finditer(src):
        attrs = dict(ATTR_RE.findall(m.group(1)))
        body = re.sub(r'<[^>]+>', '', m.group(2))
        body = (body.replace('&amp;', '&').replace('&lt;', '<')
                    .replace('&gt;', '>').replace('&#176;', 'd'))
        if not body.strip():
            continue
        if in_transform(m.start()) or 'transform' in attrs:
            rotated += 1
            continue
        try:
            x = float(attrs.get('x', 0)); y = float(attrs.get('y', 0))
        except ValueError:
            continue
        size = float(attrs.get('font-size', '10').replace('px', ''))
        w = len(body) * size * MEAN_EM
        anch = attrs.get('text-anchor', 'start')
        x0 = x - w / 2 if anch == 'middle' else (x - w if anch == 'end' else x)
        out.append((x0, y - size * ASC, x0 + w, y + size * DESC, body, size))
    return vb, out, rotated


def overlap(a, b, pad=0.0):
    return (a[0] < b[2] - pad and b[0] < a[2] - pad and
            a[1] < b[3] - pad and b[1] < a[3] - pad)


fails = 0
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
for f in sorted(glob.glob('03-field/renderings/*.svg')):
    vb, bs, rot = boxes(f)
    name = os.path.basename(f)
    # out of sheet
    oob = [b for b in bs
           if b[0] < vb[0] - 1 or b[1] < vb[1] - 1
           or b[2] > vb[0] + vb[2] + 1 or b[3] > vb[1] + vb[3] + 1]
    # overlaps: require a real 2-px bite so kerning slop doesn't fire
    hits = []
    bs_sorted = sorted(bs, key=lambda b: b[1])
    for i, a in enumerate(bs_sorted):
        for b in bs_sorted[i + 1:]:
            if b[1] > a[3]:
                break
            if overlap(a, b, pad=2.0):
                hits.append((a, b))
    print("%-22s texts=%3d  (rotated skipped %d)  off-sheet=%d  overlaps=%d"
          % (name, len(bs), rot, len(oob), len(hits)))
    for b in oob[:6]:
        print("    OFF-SHEET  x0=%.0f y0=%.0f x1=%.0f y1=%.0f  %r"
              % (b[0], b[1], b[2], b[3], b[4][:56]))
    for a, b in hits[:10]:
        print("    OVERLAP    %r  <->  %r" % (a[4][:44], b[4][:44]))
    fails += len(oob) + len(hits)

print("\nTOTAL layout issues: %d" % fails)
sys.exit(0)
