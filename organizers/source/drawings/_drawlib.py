# -*- coding: utf-8 -*-
"""
Minimal SVG drawing library for the SUMMIT PUSH field drawing sheets.

Everything is authored in sheet pixels (SVG user units); each view supplies its
own inches-to-pixels mapping. Dimension lines, extension lines, leaders, title
blocks, and view labels follow one convention, so the six sheets read as one set.

Every sheet is printed on a landscape ANSI C plate with its image 21 in wide
(organizers/source/typesetting/pdf/plates.css), so one user unit prints at 1512 / sheet-width pt.
Type sizes and line weights are therefore set in PRINTED POINTS and converted
per sheet (Sheet.pt): a 1960-unit sheet needs bigger numbers than a 1420-unit
one to print the same size. Floors (MANUAL-STYLE-GUIDE.md §7.4 sets a hard 6 pt;
this set aims higher so every sheet reads easily):

  notes                 >= 7.5 pt        dimension values      >= 8.6 pt
  labels, leader text   >= 8.5 pt        view names            >= 11 pt

Conventions (organizers/source/typesetting/MANUAL-STYLE-GUIDE.md §7.3 and §7.4):
  dimension lines and dimension text  #C02020, arrowheads at both ends
  extension lines                     0.7 pt
  CRITICAL dimensions                 boxed
  reference dimensions                suffixed "(ref)"
  leader lines                        #E100E1 (reserved for leaders), 1.5 pt,
                                      arrowhead on the feature end
  vertical dimension values           read from the bottom (rotated -90)

Arrowheads are drawn as explicit filled triangles rather than SVG markers, so
they survive import into CAD and PDF tools that drop markers, and so the
layout checker (organizers/source/verify/svg_collide.py) sees them as geometry.
"""
import math

# ---------------------------------------------------------------- palette
INK = "#1A1D21"
MUTED = "#6E7378"          # --muted; 4.8:1 on white, so keep it off tinted grounds
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
DEPOT = "#7F7F7F"         # `depot`, MATERIALS-AND-COLORS.md §1.2 (REVISION-LOG M44)
WALL = "#9AA4B2"
WALL_D = "#4A5462"
GHOST = "#2E8B57"
GHOST_T = "#1F6B40"        # GHOST-coloured text: 6.4:1 on white
CRATE = "#7B3FA0"
CRATE_D = "#4A2263"
CELL = "#F2F2F0"
CELL_CAP = "#2E8B57"
COIL = "#D9A441"
COIL_D = "#8A6414"
BEACON = "#FFF3D0"
RULE = "#C8CCD1"
RULE_S = "#8A9199"

PLATE_PT = 21.0 * 72.0     # printed width of every sheet image, in pt

# Advance widths (1/1000 em) of Arial / Liberation Sans, the face the plates are
# rendered with. Used to size CRITICAL boxes and to check that text fits.
_REG = dict(zip(
    " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"
    "abcdefghijklmnopqrstuvwxyz{|}~",
    [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278]
    + [556] * 10 + [278, 278, 584, 584, 584, 556, 1015,
                    667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
                    722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611,
                    278, 278, 278, 469, 556, 333,
                    556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
                    556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500,
                    334, 260, 334, 584]))
_BOLD = dict(zip(
    " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"
    "abcdefghijklmnopqrstuvwxyz{|}~",
    [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278]
    + [556] * 10 + [333, 333, 584, 584, 584, 611, 975,
                    722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833,
                    722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611,
                    333, 278, 333, 584, 556, 333,
                    556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889,
                    611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500,
                    389, 280, 389, 584]))
_REG[u"—"] = _BOLD[u"—"] = 1000


def text_width(s, size, bold=False):
    """Advance width of s at font-size size, in the same units as size."""
    tab = _BOLD if bold else _REG
    return sum(tab.get(c, 1000 if ord(c) > 0x2000 else 600) for c in str(s)) * size / 1000.0


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Sheet(object):
    """One drawing sheet."""

    def __init__(self, w, h, title, number, total, subtitle="", rev="2.2"):
        self.w, self.h = w, h
        self.title, self.number, self.total = title, number, total
        self.subtitle, self.rev = subtitle, rev
        self.parts = []
        # printed pt per user unit, and the type/line scale that follows from it
        self.k = PLATE_PT / float(w)
        P = self.pt
        self.NOTE = max(8.5, P(7.5))       # note text
        self.LABEL = max(9.0, P(8.5))      # labels on the drawing, leader text
        self.DIM = max(9.0, P(8.6))        # dimension values
        self.DIM_L = max(10.5, P(9.4))     # overall (envelope) dimension values
        self.HEAD = max(9.5, P(9.0))       # note-block and table headings
        self.SUB = max(9.0, P(8.0))        # view scale and view sub-caption
        self.VIEW = max(13.0, P(11.0))     # view names
        self.PITCH = 1.32                  # note line pitch, x size
        self.SW_LEADER = P(1.5)
        self.SW_EXT = max(0.7, P(0.7))
        self.SW_DIM = max(1.1, P(0.85))
        self.ARROW = (P(6.0), P(3.4))      # dimension arrowhead: length, width
        self.ARROW_LD = (P(7.0), P(4.2))   # leader arrowhead
        # title block geometry (the drawing area ends above tb_top)
        self.TB_HEAD = max(10.0, P(9.5))
        self.tb_lead = self.PITCH * self.NOTE
        self.tb_h = 1.9 * self.TB_HEAD + 3 * self.tb_lead + 0.7 * self.NOTE
        self.tb_top = self.h - 8 - self.tb_h

    def pt(self, p):
        """User units that print at p points on the plate."""
        return p / self.k

    def add(self, s):
        self.parts.append(s)
        return self

    # ---------------------------------------------------------- primitives
    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=1.0, rx=None,
             dash=None, op=None, rot=None):
        a = 'x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" stroke="%s" stroke-width="%.2f"' % (
            x, y, w, h, fill, stroke, sw)
        if rx is not None:
            a += ' rx="%.2f"' % rx
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        if op is not None:
            a += ' opacity="%.2f"' % op
        if rot is not None:
            a += ' transform="rotate(%.2f %.2f %.2f)"' % rot
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
             italic=False, rot=None, family=None, halo=False):
        """halo=True paints a white outline under the glyphs, so a label that has
        to sit on a line (a centerline, a tape edge) stays readable."""
        if not str(s).strip():
            return self
        a = 'x="%.2f" y="%.2f" font-size="%.2f" fill="%s"' % (x, y, size, fill)
        if anchor != "start":
            a += ' text-anchor="%s"' % anchor
        if weight:
            a += ' font-weight="%s"' % weight
        if italic:
            a += ' font-style="italic"'
        if family:
            a += ' font-family="%s"' % family
        if halo:
            a += (' stroke="#FFFFFF" stroke-width="%.2f" stroke-linejoin="round" paint-order="stroke"'
                  % max(2.0, 0.3 * size))
        if rot is not None:
            a += ' transform="rotate(%.2f %.2f %.2f)"' % (rot, x, y)
        return self.add("<text %s>%s</text>" % (a, esc(s)))

    def lines(self, x, y, rows, size=None, fill=INK, pitch=None, anchor="start",
              weight=None, halo=False):
        """A block of text lines; returns the y of the next line."""
        size = size or self.NOTE
        pitch = pitch or self.PITCH * size
        for t in rows:
            if t:
                self.text(x, y, t, size=size, fill=fill, anchor=anchor, weight=weight, halo=halo)
            y += pitch
        return y

    def tw(self, s, size, bold=False):
        return text_width(s, size, bold)

    # ------------------------------------------------------------- arrows
    def _head(self, x, y, ux, uy, L, W, fill):
        """Filled arrowhead, tip at (x, y), pointing along the unit vector (ux, uy)."""
        bx, by = x - ux * L, y - uy * L
        nx, ny = -uy * W / 2.0, ux * W / 2.0
        self.add('<path d="M %.2f %.2f L %.2f %.2f L %.2f %.2f Z" fill="%s" stroke="none"/>'
                 % (x, y, bx + nx, by + ny, bx - nx, by - ny, fill))

    def arrow(self, x1, y1, x2, y2, stroke=INK, sw=None, start=False, end=True,
              head=None, dash=None):
        """Line from (x1, y1) to (x2, y2) with arrowheads whose tips land exactly
        on the end points. The shaft stops inside each head, so its butt end never
        pokes past the point."""
        sw = sw if sw is not None else self.SW_DIM
        hl, hw = head or self.ARROW
        L = math.hypot(x2 - x1, y2 - y1) or 1.0
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        pull = 0.55 * hl
        ax1, ay1 = (x1 + ux * pull, y1 + uy * pull) if start else (x1, y1)
        ax2, ay2 = (x2 - ux * pull, y2 - uy * pull) if end else (x2, y2)
        self.line(ax1, ay1, ax2, ay2, stroke=stroke, sw=sw, dash=dash)
        if end:
            self._head(x2, y2, ux, uy, hl, hw, stroke)
        if start:
            self._head(x1, y1, -ux, -uy, hl, hw, stroke)

    def _dimline(self, x1, y1, x2, y2):
        """Dimension line with arrowheads at both ends. When the span is too short
        for two heads, the heads go outside, pointing in (ASME Y14.5 practice)."""
        hl, hw = self.ARROW
        L = math.hypot(x2 - x1, y2 - y1)
        if L >= 2.6 * hl:
            self.arrow(x1, y1, x2, y2, stroke=DIM, start=True, end=True)
            return
        ux, uy = (x2 - x1) / (L or 1.0), (y2 - y1) / (L or 1.0)
        tail = hl + self.pt(5.0)
        self.line(x1, y1, x2, y2, stroke=DIM, sw=self.SW_DIM)
        self.arrow(x1 - ux * tail, y1 - uy * tail, x1, y1, stroke=DIM)
        self.arrow(x2 + ux * tail, y2 + uy * tail, x2, y2, stroke=DIM)

    # -------------------------------------------------------- dimensioning
    def _dsize(self, size, big=False):
        base = self.DIM_L if big else self.DIM
        return base if size is None else max(size, self.DIM)

    def _dimlabel(self, mx, my, ang, label, critical=False, size=None, below=False,
                  halo=False, span=None, shift=0.0):
        """Value centred on the dimension line through (mx, my), which runs at
        angle ang (deg). It sits beside the line, above it in the line's own
        frame (below=True puts it on the other side), never on it. CRITICAL
        values are boxed; the box is rotated with the text. shift slides the
        value along the line; where it then overhangs the arrowheads the
        dimension line is carried on under it."""
        size = self._dsize(size)
        w = text_width(label, size)
        gap = max(1.6, self.pt(1.2))
        bw = w + 0.9 * size if critical else w
        hl, hwid = self.ARROW
        if span is not None and (abs(shift) + bw / 2.0 > span / 2.0 - 1.2 * hl):
            gap += hwid / 2.0          # value runs alongside an arrowhead: clear it
        if span is not None and abs(shift) + bw / 2.0 > span / 2.0:
            # carry the dimension line on under the value
            c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            far = shift + (bw / 2.0 if shift >= 0 else -bw / 2.0)
            near = span / 2.0 if shift >= 0 else -span / 2.0
            self.line(mx + c * near, my + s_ * near, mx + c * far, my + s_ * far,
                      stroke=DIM, sw=self.SW_DIM)
        cx = mx + shift * math.cos(math.radians(ang))
        cy = my + shift * math.sin(math.radians(ang))
        # draw in the line's frame about (cx, cy)
        tr = ' transform="rotate(%.2f %.2f %.2f)"' % (ang, cx, cy) if ang else ''
        if critical:
            bh = 1.32 * size
            top = cy - gap - bh if not below else cy + gap
            self.add('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="#ffffff" stroke="%s" stroke-width="%.2f"%s/>'
                     % (cx - bw / 2.0, top, bw, bh, DIM, max(0.8, self.pt(0.6)), tr))
            base = top + bh - 0.33 * size
        else:
            base = cy - gap - 0.24 * size if not below else cy + gap + 0.74 * size
        a = 'x="%.2f" y="%.2f" font-size="%.2f" fill="%s" text-anchor="middle"' % (cx, base, size, DIM)
        if halo and not critical:
            a += (' stroke="#FFFFFF" stroke-width="%.2f" stroke-linejoin="round" paint-order="stroke"'
                  % max(2.0, 0.3 * size))
        self.add("<text %s%s>%s</text>" % (a, tr, esc(label)))

    def _overhangs(self, label, critical, size, span, shift):
        """True when the value, centred on its dimension line, is wider than the
        span between the extension lines (so it would sit on them)."""
        if abs(shift) > 1e-9:
            return False
        sz = self._dsize(size, size is None)
        bw = text_width(label, sz) + (0.9 * sz if critical else 0.0)
        return bw / 2.0 > span / 2.0 - 1.0

    def _ext(self, x1, y1, x2, y2):
        self.line(x1, y1, x2, y2, stroke=DIM, sw=self.SW_EXT)

    def dim_h(self, x1, x2, y, label, ext_from=None, critical=False, size=None,
              above=True, tick=8, halo=False, shift=0.0):
        """Horizontal dimension between x1 and x2 at height y; extension lines
        run from y = ext_from to just past the dimension line."""
        self._dimline(x1, y, x2, y)
        if ext_from is not None:
            far_below = ext_from < y                      # ticks run away from the part
            if self._overhangs(label, critical, size, abs(x2 - x1), shift):
                above = not far_below                     # value on the tick side...
                tick = min(tick, 2.0)                     # ...with short ticks
            for xx in (x1, x2):
                self._ext(xx, ext_from, xx, y + (tick if far_below else -tick))
        self._dimlabel((x1 + x2) / 2.0, y, 0, label, critical, self._dsize(size, size is None),
                       below=not above, halo=halo, span=abs(x2 - x1),
                       shift=shift if x2 >= x1 else -shift)

    def dim_v(self, y1, y2, x, label, ext_from=None, critical=False, size=None,
              side="left", tick=8, halo=False, shift=0.0):
        """Vertical dimension between y1 and y2 at x. The value reads from the
        bottom of the sheet and sits on the given side of the line."""
        self._dimline(x, y1, x, y2)
        if ext_from is not None:
            far_right = ext_from < x
            if self._overhangs(label, critical, size, abs(y2 - y1), shift):
                side = "right" if far_right else "left"
                tick = min(tick, 2.0)
            for yy in (y1, y2):
                self._ext(ext_from, yy, x + (tick if far_right else -tick), yy)
        self._dimlabel(x, (y1 + y2) / 2.0, -90, label, critical, self._dsize(size, size is None),
                       below=(side != "left"), halo=halo, span=abs(y2 - y1), shift=shift)

    def dim_a(self, p1, p2, label, off=12, critical=False, size=None, ext_pad=3.0, shift=0.0):
        """Aligned dimension between two points, offset perpendicular by off."""
        (x1, y1), (x2, y2) = p1, p2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        ax1, ay1 = x1 + nx * off, y1 + ny * off
        ax2, ay2 = x2 + nx * off, y2 + ny * off
        sg = 1.0 if off >= 0 else -1.0
        e0 = ext_pad * sg
        e1 = sg * 8.0
        self._ext(x1 + nx * e0, y1 + ny * e0, ax1 + nx * e1, ay1 + ny * e1)
        self._ext(x2 + nx * e0, y2 + ny * e0, ax2 + nx * e1, ay2 + ny * e1)
        self._dimline(ax1, ay1, ax2, ay2)
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90:
            ang -= 180
        if ang <= -90:
            ang += 180
        # "above" in the rotated frame points along (sin a, -cos a); keep the value on
        # the far side of the line from the measured feature
        up = (math.sin(math.radians(ang)), -math.cos(math.radians(ang)))
        away = (nx * sg, ny * sg)
        below = (up[0] * away[0] + up[1] * away[1]) < 0
        # shift is measured from p1 toward p2; the label frame may run the other way
        sd = shift if (math.cos(math.radians(ang)) * dx + math.sin(math.radians(ang)) * dy) >= 0 else -shift
        self._dimlabel((ax1 + ax2) / 2.0, (ay1 + ay2) / 2.0, ang, label, critical,
                       self._dsize(size), below=below, span=L, shift=sd)

    def leader(self, px, py, tx, ty, label, size=None, anchor="start", halo=False,
               fill=INK, weight=None):
        """Callout: label anchored at (tx, ty), leader running to the arrowhead
        whose tip touches the feature at (px, py)."""
        size = max(size or 0, self.LABEL)
        self.arrow(tx, ty, px, py, stroke=LEADER, sw=self.SW_LEADER, head=self.ARROW_LD)
        gap = max(3.0, self.pt(2.5))
        self.text(tx + (gap if anchor == "start" else -gap), ty + 0.34 * size, label,
                  size=size, fill=fill, anchor=anchor, halo=halo, weight=weight)

    def angle(self, cx, cy, r, a0, a1, label, lx=None, ly=None, size=None, anchor="middle",
              halo=False):
        """Angular dimension: arc of radius r from a0 to a1 (deg, SVG sense) with
        an arrowhead at each end, value at (lx, ly)."""
        size = self._dsize(size)
        hl, hw = self.ARROW
        sgn = 1.0 if a1 > a0 else -1.0

        def P(a):
            return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        span = abs(a1 - a0)
        dth = math.degrees(hl / r)
        heads = span > 2.2 * dth
        pull = math.degrees(0.55 * hl / r) if heads else 0.0
        b0, b1 = a0 + sgn * pull, a1 - sgn * pull
        x0, y0 = P(b0)
        x1, y1 = P(b1)
        big = 1 if abs(b1 - b0) > 180 else 0
        sweep = 1 if b1 > b0 else 0
        self.path("M %.2f %.2f A %.2f %.2f 0 %d %d %.2f %.2f" % (x0, y0, r, r, big, sweep, x1, y1),
                  stroke=DIM, sw=self.SW_DIM)
        if heads:
            for tip_a, base_a in ((a1, a1 - sgn * dth), (a0, a0 + sgn * dth)):
                tx_, ty_ = P(tip_a)
                bx_, by_ = P(base_a)
                L = math.hypot(tx_ - bx_, ty_ - by_) or 1.0
                self._head(tx_, ty_, (tx_ - bx_) / L, (ty_ - by_) / L, hl, hw, DIM)
        am = math.radians((a0 + a1) / 2.0)
        self.text(lx if lx is not None else cx + (r + 12) * math.cos(am),
                  ly if ly is not None else cy + (r + 12) * math.sin(am),
                  label, size=size, fill=DIM, anchor=anchor, halo=halo)

    # ------------------------------------------------------------- framing
    def view_label(self, x, y, name, scale=None, sub=None):
        self.text(x, y, name, size=self.VIEW, fill=ACCENT, weight="bold", anchor="middle")
        yy = y + 0.2 * self.VIEW + 1.05 * self.SUB
        for t in (scale, sub):
            if t:
                self.text(x, yy, t, size=self.SUB, fill=MUTED, anchor="middle")
                yy += 1.25 * self.SUB
        return yy

    def scalebar(self, x, y, pxperin, inches=24, label=None):
        w = pxperin * inches
        sz = self.SUB
        self.rect(x, y, w / 2.0, 6, fill=INK, stroke=INK, sw=0.6)
        self.rect(x + w / 2.0, y, w / 2.0, 6, fill="#ffffff", stroke=INK, sw=0.6)
        self.text(x, y + 6 + 1.1 * sz, "0", size=sz, fill=MUTED, anchor="middle")
        self.text(x + w, y + 6 + 1.1 * sz, "%d in" % inches, size=sz, fill=MUTED, anchor="middle")
        if label:
            self.text(x + w + 0.6 * sz + self.tw("%d in" % inches, sz) / 2.0, y + 6, label,
                      size=sz, fill=MUTED)

    def titleblock(self, notes):
        H, N = self.TB_HEAD, self.NOTE
        bx, by = 8, self.tb_top
        bw, bh = self.w - 16, self.tb_h
        hh = 1.9 * H
        right = ("Units: INCHES   |   Scale: as noted per view",
                 "Geometry authority: 03-field/FIELD-CAD-PACKAGE.md",
                 "© 2026 Eric Dean. SUMMIT PUSH Training Use License")
        rw = max(250.0, max(text_width(t, N) for t in right) + 24,
                 text_width("SHEET 6 OF 6    REV 2.2", H, True) + 36)
        self.rect(bx, by, bw, bh, fill="#FFFFFF", stroke=RULE_S, sw=1.0)
        self.line(bx, by + hh, bx + bw, by + hh, stroke=RULE, sw=0.8)
        self.line(bx + bw - rw, by, bx + bw - rw, by + bh, stroke=RULE, sw=0.8)
        base = by + 0.5 * hh + 0.36 * H
        setname = "SUMMIT PUSH — FIELD DRAWING SET"
        self.text(bx + 8, base, setname, size=H, fill=ACCENT, weight="bold")
        self.text(bx + 8 + text_width(setname, H, True) + 2.5 * H, base, self.title, size=H,
                  fill=INK, weight="bold")
        yy = by + hh + 0.5 * self.tb_lead + 0.36 * N
        room = bw - rw - 16
        for n in notes[:3]:
            if text_width(n, N) > room:
                raise ValueError("title-block note too long for %s: %r" % (self.title, n[:40]))
            self.text(bx + 8, yy, n, size=N, fill=MUTED)
            yy += self.tb_lead
        rx = bx + bw - rw + 8
        self.text(rx, base, "SHEET %d OF %d" % (self.number, self.total), size=H,
                  fill=INK, weight="bold")
        yy = by + hh + 0.5 * self.tb_lead + 0.36 * N
        for t in right:
            self.text(rx, yy, t, size=N, fill=MUTED)
            yy += self.tb_lead
        self.text(bx + bw - 8, base, "REV %s" % self.rev, size=H, fill=INK,
                  weight="bold", anchor="end")

    # -------------------------------------------------------------- output
    def render(self):
        head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
                'font-family="Segoe UI, Roboto, Arial, sans-serif">\n' % (self.w, self.h))
        bg = '  <rect width="%d" height="%d" fill="#ffffff"/>\n' % (self.w, self.h)
        ts = max(21.0, self.pt(16.0))
        ss = max(11.5, self.pt(9.5))
        title = ('  <text x="%d" y="%.1f" text-anchor="middle" font-size="%.2f" font-weight="bold" fill="%s">%s</text>\n'
                 % (self.w // 2, 8 + ts, ts, INK, esc("SUMMIT PUSH — " + self.title)))
        sub = ""
        if self.subtitle:
            sub = ('  <text x="%d" y="%.1f" text-anchor="middle" font-size="%.2f" fill="%s">%s</text>\n'
                   % (self.w // 2, 8 + ts + 1.6 * ss, ss, MUTED, esc(self.subtitle)))
        body = "\n".join("  " + p for p in self.parts)
        return head + bg + title + sub + body + "\n</svg>\n"

    def save(self, path):
        import io
        io.open(path, "w", encoding="utf-8", newline="\n").write(self.render())
        return path
