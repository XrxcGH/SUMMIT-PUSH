# -*- coding: utf-8 -*-
"""
Minimal SVG drawing library for the SUMMIT PUSH field drawing sheets.

Everything is authored in sheet pixels; each view supplies its own
inches-to-pixels mapping. Dimension lines, extension lines, leaders,
title blocks, and view labels all follow one convention so the six
sheets read as one set.

Conventions (match 06-style/MANUAL-STYLE-GUIDE.md 7.4):
  dimension lines and dimension text  #C02020
  extension lines                     0.7 px
  CRITICAL dimensions                 boxed
  reference dimensions                suffixed "(ref)"
  leader lines                        #E100E1 (reserved)
"""
import math

# ---------------------------------------------------------------- palette
INK = "#1A1D21"
MUTED = "#6E7378"
ACCENT = "#1F4E79"
DIM = "#C02020"
LEADER = "#E100E1"
BLUE = "#1D63C8"
BLUE_D = "#0E3F86"
RED = "#CC3333"
RED_D = "#8E2020"
CARPET = "#F4F2EE"
CRAG_BODY = "#E9E2D4"
CRAG_SPIRE = "#DDD3C0"
CRAG_EDGE = "#4A3B22"
TRUSS = "#8A6D3B"
TRUSS_D = "#5C4823"
RUNG = "#9AA0A6"
SHELF = "#8A6D3B"
SOCKET = "#9DB8D6"
SOCKET_L = "#EAF1FC"
DEPOT = "#B8A888"
WALL = "#9AA4B2"
WALL_D = "#4A5462"
GHOST = "#2E8B57"
CRATE = "#7B3FA0"
CRATE_D = "#4A2263"
CELL = "#F2F2F0"
CELL_CAP = "#2E8B57"
COIL = "#D9A441"
COIL_D = "#8A6414"
BEACON = "#FFF3D0"
RULE = "#C8CCD1"
RULE_S = "#8A9199"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Sheet(object):
    """One drawing sheet."""

    def __init__(self, w, h, title, number, total, subtitle="", rev="2.2"):
        self.w, self.h = w, h
        self.title, self.number, self.total = title, number, total
        self.subtitle, self.rev = subtitle, rev
        self.parts = []

    def add(self, s):
        self.parts.append(s)
        return self

    # ---------------------------------------------------------- primitives
    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=1.0, rx=None,
             dash=None, op=None):
        a = 'x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" stroke="%s" stroke-width="%.2f"' % (
            x, y, w, h, fill, stroke, sw)
        if rx is not None:
            a += ' rx="%.2f"' % rx
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        if op is not None:
            a += ' opacity="%.2f"' % op
        return self.add("<rect %s/>" % a)

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.0, dash=None, cap=None, op=None):
        a = 'x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"' % (
            x1, y1, x2, y2, stroke, sw)
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        if cap:
            a += ' stroke-linecap="%s"' % cap
        if op is not None:
            a += ' opacity="%.2f"' % op
        return self.add("<line %s/>" % a)

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=1.0):
        return self.add('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="%s" stroke-width="%.2f"/>'
                        % (cx, cy, r, fill, stroke, sw))

    def ellipse(self, cx, cy, rx, ry, fill="none", stroke=INK, sw=1.0, rot=None):
        a = 'cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="%s" stroke="%s" stroke-width="%.2f"' % (
            cx, cy, rx, ry, fill, stroke, sw)
        if rot is not None:
            a += ' transform="rotate(%.3f %.2f %.2f)"' % (rot, cx, cy)
        return self.add("<ellipse %s/>" % a)

    def path(self, d, fill="none", stroke=INK, sw=1.0, dash=None, op=None):
        a = 'd="%s" fill="%s" stroke="%s" stroke-width="%.2f"' % (d, fill, stroke, sw)
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        if op is not None:
            a += ' opacity="%.2f"' % op
        return self.add("<path %s/>" % a)

    def text(self, x, y, s, size=10, fill=INK, anchor="start", weight=None,
             italic=False, rot=None, family=None):
        a = 'x="%.2f" y="%.2f" font-size="%.1f" fill="%s"' % (x, y, size, fill)
        if anchor != "start":
            a += ' text-anchor="%s"' % anchor
        if weight:
            a += ' font-weight="%s"' % weight
        if italic:
            a += ' font-style="italic"'
        if family:
            a += ' font-family="%s"' % family
        if rot is not None:
            a += ' transform="rotate(%.2f %.2f %.2f)"' % (rot, x, y)
        return self.add("<text %s>%s</text>" % (a, esc(s)))

    # -------------------------------------------------------- dimensioning
    def _dimtext(self, x, y, s, anchor="middle", critical=False, size=10.5, rot=None):
        if critical:
            wpx = 0.60 * size * len(str(s)) + 7
            bx = x - wpx / 2.0 if anchor == "middle" else (x - wpx if anchor == "end" else x)
            g = []
            if rot is None:
                g.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="#ffffff" stroke="%s" stroke-width="0.8"/>'
                         % (bx, y - size + 1.0, wpx, size + 4.0, DIM))
            self.add("".join(g))
        self.text(x, y, s, size=size, fill=DIM, anchor=anchor, rot=rot)

    def dim_h(self, x1, x2, y, label, ext_from=None, critical=False, size=10.5,
              above=True, tick=8):
        """Horizontal dimension between x1 and x2 at height y."""
        self.add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.1" marker-start="url(#arr)" marker-end="url(#arr)"/>'
                 % (x1, y, x2, y, DIM))
        if ext_from is not None:
            for xx in (x1, x2):
                self.line(xx, ext_from, xx, y + (tick if ext_from < y else -tick),
                          stroke=DIM, sw=0.7)
        self._dimtext((x1 + x2) / 2.0, y - 4 if above else y + size + 2, label,
                      critical=critical, size=size)

    def dim_v(self, y1, y2, x, label, ext_from=None, critical=False, size=10.5,
              side="left", tick=8):
        self.add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.1" marker-start="url(#arr)" marker-end="url(#arr)"/>'
                 % (x, y1, x, y2, DIM))
        if ext_from is not None:
            for yy in (y1, y2):
                self.line(ext_from, yy, x + (tick if ext_from < x else -tick), yy,
                          stroke=DIM, sw=0.7)
        my = (y1 + y2) / 2.0
        self._dimtext(x - 4 if side == "left" else x + 4, my, label,
                      anchor="middle", critical=critical, size=size,
                      rot=-90 if side == "left" else 90)

    def dim_a(self, p1, p2, label, off=12, critical=False, size=10.5):
        """Aligned dimension between two points, offset perpendicular."""
        (x1, y1), (x2, y2) = p1, p2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        ax1, ay1 = x1 + nx * off, y1 + ny * off
        ax2, ay2 = x2 + nx * off, y2 + ny * off
        self.line(x1, y1, ax1, ay1, stroke=DIM, sw=0.7)
        self.line(x2, y2, ax2, ay2, stroke=DIM, sw=0.7)
        self.add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.1" marker-start="url(#arr)" marker-end="url(#arr)"/>'
                 % (ax1, ay1, ax2, ay2, DIM))
        mx, my = (ax1 + ax2) / 2.0 + nx * 6, (ay1 + ay2) / 2.0 + ny * 6
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90:
            ang -= 180
        if ang < -90:
            ang += 180
        self._dimtext(mx, my, label, critical=critical, size=size, rot=ang)

    def leader(self, px, py, tx, ty, label, size=9.5, anchor="start"):
        self.add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.2" marker-start="url(#lead)"/>'
                 % (tx, ty, px, py, LEADER))
        self.text(tx + (4 if anchor == "start" else -4), ty + 3.5, label,
                  size=size, fill=INK, anchor=anchor)

    def angle(self, cx, cy, r, a0, a1, label, lx=None, ly=None, size=10):
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        big = 1 if abs(a1 - a0) > 180 else 0
        sweep = 1 if a1 > a0 else 0
        self.path("M %.2f %.2f A %.2f %.2f 0 %d %d %.2f %.2f" % (x0, y0, r, r, big, sweep, x1, y1),
                  stroke=DIM, sw=1.0)
        am = math.radians((a0 + a1) / 2.0)
        self.text(lx if lx is not None else cx + (r + 12) * math.cos(am),
                  ly if ly is not None else cy + (r + 12) * math.sin(am),
                  label, size=size, fill=DIM, anchor="middle")

    # ------------------------------------------------------------- framing
    def view_label(self, x, y, name, scale=None, sub=None):
        self.text(x, y, name, size=13, fill=ACCENT, weight="bold", anchor="middle")
        if scale:
            self.text(x, y + 13, scale, size=9, fill=MUTED, anchor="middle")
        if sub:
            self.text(x, y + (25 if scale else 13), sub, size=9, fill=MUTED, anchor="middle")

    def scalebar(self, x, y, pxperin, inches=24, label=None):
        w = pxperin * inches
        self.rect(x, y, w / 2.0, 6, fill=INK, stroke=INK, sw=0.6)
        self.rect(x + w / 2.0, y, w / 2.0, 6, fill="#ffffff", stroke=INK, sw=0.6)
        self.text(x, y + 18, "0", size=8, fill=MUTED, anchor="middle")
        self.text(x + w, y + 18, "%d in" % inches, size=8, fill=MUTED, anchor="middle")
        if label:
            self.text(x + w + 34, y + 6, label, size=8, fill=MUTED)

    def titleblock(self, notes):
        bx, by = 8, self.h - 74
        bw, bh = self.w - 16, 66
        self.rect(bx, by, bw, bh, fill="#FFFFFF", stroke=RULE_S, sw=1.0)
        self.line(bx, by + 20, bx + bw, by + 20, stroke=RULE, sw=0.8)
        self.line(bx + bw - 250, by, bx + bw - 250, by + bh, stroke=RULE, sw=0.8)
        self.text(bx + 8, by + 14, "SUMMIT PUSH — FIELD DRAWING SET", size=11,
                  fill=ACCENT, weight="bold")
        self.text(bx + 250, by + 14, self.title, size=11, fill=INK, weight="bold")
        yy = by + 33
        for n in notes[:3]:
            self.text(bx + 8, yy, n, size=8.5, fill=MUTED)
            yy += 11
        rx = bx + bw - 242
        self.text(rx, by + 14, "SHEET %d OF %d" % (self.number, self.total), size=10,
                  fill=INK, weight="bold")
        self.text(rx, by + 33, "Units: INCHES   |   Scale: as noted per view", size=8.5, fill=MUTED)
        self.text(rx, by + 44, "Geometry authority: 03-field/FIELD-CAD-PACKAGE.md", size=8.5, fill=MUTED)
        self.text(rx, by + 55, "Spec: 01-design/DESIGN-SPEC.md v%s" % self.rev, size=8.5, fill=MUTED)
        self.text(bx + bw - 8, by + 14, "REV %s" % self.rev, size=10, fill=INK,
                  weight="bold", anchor="end")

    # -------------------------------------------------------------- output
    def render(self):
        head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
                'font-family="Segoe UI, Roboto, Arial, sans-serif">\n' % (self.w, self.h))
        defs = (
            '  <defs>\n'
            '    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">\n'
            '      <path d="M0,0 L10,5 L0,10 z" fill="%s"/>\n'
            '    </marker>\n'
            '    <marker id="lead" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">\n'
            '      <path d="M0,0 L10,5 L0,10 z" fill="%s"/>\n'
            '    </marker>\n'
            '    <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">\n'
            '      <line x1="0" y1="0" x2="0" y2="6" stroke="#9AA0A6" stroke-width="1"/>\n'
            '    </pattern>\n'
            '  </defs>\n' % (DIM, LEADER))
        bg = '  <rect width="%d" height="%d" fill="#ffffff"/>\n' % (self.w, self.h)
        title = ('  <text x="%d" y="30" text-anchor="middle" font-size="21" font-weight="bold" fill="%s">%s</text>\n'
                 % (self.w // 2, INK, esc("SUMMIT PUSH — " + self.title)))
        sub = ""
        if self.subtitle:
            sub = ('  <text x="%d" y="50" text-anchor="middle" font-size="11.5" fill="%s">%s</text>\n'
                   % (self.w // 2, MUTED, esc(self.subtitle)))
        body = "\n".join("  " + p for p in self.parts)
        return head + defs + bg + title + sub + body + "\n</svg>\n"

    def save(self, path):
        import io
        io.open(path, "w", encoding="utf-8", newline="\n").write(self.render())
        return path
