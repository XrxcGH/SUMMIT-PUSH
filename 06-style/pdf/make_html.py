# -*- coding: utf-8 -*-
"""
Build the HTML that Paged.js paginates into the Game Manual PDF.

    python 06-style/pdf/make_html.py [--total N --plates-from P]

Reads 02-manual/manual-header.md (title, version) and 02-manual/sections/*.md, applies the
structure of 06-style/MANUAL-STYLE-GUIDE.md, and writes:

    06-style/pdf/build/manual.html   cover, front matter, the nine sections, the plate index
    06-style/pdf/build/plates.html   the six drawing sheets on ANSI C (22 x 17 in) plates

The Markdown conventions it relies on are the ones in the style guide (§9.3):
    **G412** *Headline.* Body          a rule paragraph
    *Violation:* ...                   the rule's violation line
    > *Example:* / > *Commentary:*     binding example / non-binding commentary box
    # 5 Game Rules (G)                 a section (number, title, optional rule letter)
    *Figure 3-1. Caption.*             a figure caption, directly above ![alt](image)
    **Table 6-2: Title**               a table caption, directly above the table

build.sh runs this twice: the first pass counts the manual's pages, the second writes the
final "N of TOTAL" footers and the plate page numbers.
"""
import argparse
import datetime
import html
import json
import os
import re

from markdown_it import MarkdownIt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MANUAL = os.path.join(ROOT, "02-manual")
SHEETS = os.path.join(ROOT, "03-field", "renderings")
BUILD = os.path.join(HERE, "build")

# The six drawing sheets, in plate order (MANUAL-STYLE-GUIDE.md §7.4).
PLATES = [
    ("field-top-view.svg", "FIELD top view"),
    ("crag.svg", "CRAG"),
    ("headwall.svg", "HEADWALL"),
    ("outfitter.svg", "OUTFITTER"),
    ("game-pieces.svg", "SUPPLIES and clearance studies"),
    ("apriltag-map.svg", "AprilTag map"),
]

RULE_RE = re.compile(r"^<strong>([GR]\d{3})</strong>")
POINT_HEADERS = {"AUTO", "TELEOP", "Points", "Pts", "AUTO points", "TELEOP points"}
NUMERIC_CELL = re.compile(r"^[\s+\-−–±~≈<>≤≥]*(\d[\d.,]*|\.\d+)(\s*(×|x|/|–|-|:)\s*\d[\d.,]*)*"
                          r"\s*(in|lb|s|sec|pts?|points?|%|°|ft|mm|kg|m|V|A)?\s*[*†]?\s*$")


def md():
    return MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table").enable("strikethrough")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def inline_text(tok):
    return "".join(c.content for c in (tok.children or []) if c.type in ("text", "code_inline"))


# ----------------------------------------------------------------------------------------
# sources
# ----------------------------------------------------------------------------------------
def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def header_info():
    text = read(os.path.join(MANUAL, "manual-header.md"))
    title = re.search(r"^#\s+(.+)$", text, re.M).group(1).strip()
    version = re.search(r"Version\s+(\d+(?:\.\d+)*)", text)
    sub = re.search(r"^\*([^*\n]+)\*\s*$", text, re.M)
    subtitle = sub.group(1) if sub else ""
    subtitle = re.sub(r"\s*·\s*Version\s+[\d.]+\s*$", "", subtitle)
    return {"title": title, "version": version.group(1) if version else "", "subtitle": subtitle}


def revisions():
    with open(os.path.join(HERE, "revisions.json"), encoding="utf-8") as fh:
        return json.load(fh)


# ----------------------------------------------------------------------------------------
# Markdown -> chapters
# ----------------------------------------------------------------------------------------
class Chapter:
    def __init__(self, num, title, letter):
        self.num, self.title, self.letter = num, title, letter
        self.id = "s-%s" % num
        self.h2 = []          # (id, number, title)
        self.html = ""
        self.tables = 0
        self.figures = 0

    @property
    def footer(self):
        return "%s  %s%s" % (self.num, self.title, " (%s)" % self.letter if self.letter else "")


def split_heading(text):
    m = re.match(r"^(\d+(?:\.\d+)*)\s+(.*)$", text.strip())
    return (m.group(1), m.group(2)) if m else (None, text.strip())


def annotate(tokens, chapters, figures):
    """Attach ids/classes to tokens and cut the stream into chapters.  Returns [(chapter, tokens)]."""
    out = []
    cur = None
    in_rule = False
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.level == 0 and t.type in ("heading_open", "blockquote_open", "table_open", "hr"):
            in_rule = False
        if t.type == "heading_open":
            text = inline_text(tokens[i + 1])
            num, title = split_heading(text)
            if t.tag == "h1":
                m = re.match(r"^(.*?)\s*\(([A-Z])\)$", title)
                title, letter = (m.group(1), m.group(2)) if m else (title, None)
                cur = Chapter(num, title, letter)
                chapters.append(cur)
                out.append((cur, []))
                i += 3
                continue
            hid = "s-" + num.replace(".", "-") if num else "%s-%s" % (cur.id, slug(title))
            t.attrSet("id", hid)
            if num:
                tokens[i + 1].children[0].content = title
                t.meta = {"num": num}
            if t.tag == "h2":
                cur.h2.append((hid, num, title))
        elif t.type == "paragraph_open":
            inl = tokens[i + 1]
            ch = [c for c in (inl.children or []) if not (c.type == "text" and c.content == "")]
            if len(ch) >= 3 and ch[0].type == "strong_open" and re.fullmatch(r"[GR]\d{3}", ch[1].content or ""):
                t.attrSet("class", "rule")
                t.attrSet("id", ch[1].content)
                in_rule = True
            elif len(ch) >= 3 and ch[0].type == "em_open" and ch[1].content.strip() == "Violation:":
                t.attrSet("class", "violation")
                in_rule = False
            elif (len(ch) == 3 and ch[0].type == "em_open" and re.match(r"^(Figure|Table) \d+-\d+\.", ch[1].content)):
                t.attrSet("class", "caption")
            elif len(ch) == 3 and ch[0].type == "strong_open" and re.match(r"^Table \d+-\d+:", ch[1].content):
                pass                          # a table's caption line: caption_tables() needs it unclassed
            elif in_rule and t.level == 0:
                t.attrSet("class", "rule-cont")
        elif t.type in ("bullet_list_open", "ordered_list_open") and t.level == 0 and in_rule:
            t.attrSet("class", "rule-cont")
        elif t.type == "blockquote_open":
            j = i + 1
            while tokens[j].type != "inline":
                j += 1
            ch = [c for c in (tokens[j].children or []) if not (c.type == "text" and c.content == "")]
            label = ch[1].content.strip() if len(ch) >= 2 and ch[0].type == "em_open" else ""
            kind = {"Example:": "example", "Commentary:": "commentary",
                    "Caution:": "caution", "Warning:": "warning"}.get(label, "note")
            t.attrSet("class", "box " + kind)
        elif t.type == "table_open":
            style_table(tokens, i)
        if cur is not None:
            out[-1][1].append(t)
        i += 1
    return out


def style_table(tokens, i):
    """Right-align numeric columns, tint alliance cells, zebra long tables (style guide §6)."""
    j = i
    rows, row = [], None
    while tokens[j].type != "table_close":
        tk = tokens[j]
        if tk.type == "tr_open":
            row = []
            rows.append(row)
        elif tk.type in ("th_open", "td_open"):
            row.append((tk, inline_text(tokens[j + 1]).strip()))
        j += 1
    if len(rows) < 2:
        return
    body = rows[1:]
    ncol = len(rows[0])
    for c in range(ncol):
        vals = [r[c][1] for r in body if c < len(r)]
        filled = [v for v in vals if v not in ("", "—", "–", "-")]
        points = rows[0][c][1] in POINT_HEADERS
        if filled and all(NUMERIC_CELL.match(v) for v in filled):
            cls = "num"
        elif points and filled and sum(bool(NUMERIC_CELL.match(v)) for v in filled) * 2 >= len(filled):
            cls = "pts"                       # a scoring column that also holds a few notes
        else:
            continue
        for r in rows:
            if c < len(r):
                r[c][0].attrSet("class", cls)
        if points:                            # §6: point values bold
            for r in body:
                if c < len(r) and re.fullmatch(r"[+\-−]?\d+", r[c][1]):
                    r[c][0].attrSet("class", cls + " pv")
    for r in body:
        for tk, v in r:
            m = re.match(r"^(Blue|Red)\b", v)
            if m and len(v) <= 24:
                cls = (tk.attrGet("class") or "") + " tint-" + m.group(1).lower()
                tk.attrSet("class", cls.strip())
    if len(body) > 8:
        tokens[i].attrSet("class", "zebra")


def render_chapter(parser, chap, toks, figures):
    html_ = parser.renderer.render(toks, parser.options, {})
    # numbered headings: <h2 id=..>title</h2> -> hanging number
    for t in toks:
        if t.type == "heading_open" and t.meta and "num" in t.meta:
            hid = t.attrGet("id")
            html_ = html_.replace('<%s id="%s">' % (t.tag, hid),
                                  '<%s id="%s"><span class="hnum">%s</span>' % (t.tag, hid, t.meta["num"]), 1)
    # rule numbers: mark the rule's own number so cross-reference linking skips it
    html_ = re.sub(r'(<p class="rule" id="[GR]\d{3}">)<strong>', r'\1<strong class="rule-no">', html_)
    # box labels
    html_ = re.sub(r'(<blockquote class="box (example|commentary|caution|warning)">\s*<p>)'
                   r'<em>(Example|Commentary|Caution|Warning):</em>\s*',
                   r'\1<span class="box-label">\3</span> ', html_)
    # horizontal rules inside sections are source separators only
    html_ = re.sub(r"<hr\s*/?>\n?", "", html_)
    # figures: caption paragraph followed by an image paragraph
    html_ = re.sub(r'<p class="caption"><em>((Figure|Table) (\d+-\d+))\.\s*(.*?)</em></p>\s*<p><img src="([^"]+)" alt="([^"]*)"\s*/?></p>',
                   lambda m: figure_html(m, figures), html_, flags=re.S)
    html_ = caption_tables(chap, html_)
    chap.html = html_


def figure_html(m, figures):
    label, caption, src, alt = m.group(1), m.group(4), m.group(5), m.group(6)
    fid = "fig-" + m.group(3)
    figures.append((fid, label, caption))
    art = '<img src="%s" alt="%s">' % (resolve_image(src), html.escape(alt))
    side = os.path.normpath(os.path.join(MANUAL, "sections", os.path.splitext(src)[0] + ".callouts.json"))
    if os.path.exists(side):
        with open(side, encoding="utf-8") as fh:
            art += callout_svg(json.load(fh))
    return ('<figure id="%s"><figcaption><span class="flabel">%s</span> %s</figcaption>'
            '<div class="figure-art">%s</div></figure>' % (fid, label, caption, art))


def callout_svg(c):
    """Vector callouts over a rendered figure (figures.py placed and checked them): leaders in the
    reserved callout colour with 3-pt arrowheads, labels in white boxes (MANUAL-STYLE-GUIDE.md §7.3, §9.2)."""
    w, h, fs, sw = c["width"], c["height"], c["font"], c["stroke"]
    arrow = 2 * sw
    out = ['<svg class="callouts" viewBox="0 0 %s %s" preserveAspectRatio="none" aria-hidden="true">' % (w, h),
           '<defs><marker id="co-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="%s" markerHeight="%s" '
           'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#E100E1"/></marker></defs>' % (arrow, arrow)]
    for k in c.get("callouts", []):
        out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#E100E1" stroke-width="%s" marker-end="url(#co-arrow)"/>'
                   % (k["sx"], k["sy"], k["x"], k["y"], sw))
        out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#FFFFFF" stroke="#E100E1" stroke-width="%s"/>'
                   % (round(k["lx"] - k["bw"] / 2, 1), round(k["ly"] - k["bh"] / 2, 1), k["bw"], k["bh"], round(sw / 2, 2)))
        out.append('<text x="%s" y="%s" font-size="%s" text-anchor="middle" dominant-baseline="central">%s</text>'
                   % (k["lx"], k["ly"], fs, html.escape(k["text"])))
    if c.get("compass"):
        (x0, y0), (xx, xy), (yx, yy) = c["compass"]
        ink = "#1A1D21"
        out.append('<defs><marker id="co-comp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="%s" markerHeight="%s" '
                   'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % (arrow, arrow, ink))
        for (ex, ey, t) in ((xx, xy, "+X"), (yx, yy, "+Y")):
            out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" marker-end="url(#co-comp)"/>'
                       % (x0, y0, ex, ey, ink, sw))
            out.append('<text class="compass" x="%s" y="%s" font-size="%s" text-anchor="middle" dominant-baseline="central">%s</text>'
                       % (ex + (ex - x0) * 0.25, ey + (ey - y0) * 0.25, fs, t))
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (x0, y0, sw * 1.6, ink))
        out.append('<text class="compass" x="%s" y="%s" font-size="%s" dominant-baseline="hanging">origin (0, 0) · always-blue-origin NWU</text>'
                   % (x0 + fs * 0.6, y0 + fs * 0.5, round(fs * 0.9, 1)))
    out.append("</svg>")
    return "".join(out)


def resolve_image(src):
    # sources live in 02-manual/sections/; the HTML is written to 06-style/pdf/build/
    p = os.path.normpath(os.path.join(MANUAL, "sections", src))
    return os.path.relpath(p, BUILD).replace(os.sep, "/")


def caption_tables(chap, html_):
    """Number every table 'Table <section>-<n>' and caption it above (style guide §7.1).  The
    caption is a bold label paragraph directly above the table when there is one, otherwise the
    title of the nearest heading.  A table inside an Example or Commentary box belongs to the box
    and is neither numbered nor captioned (§6)."""
    out, pos = [], 0
    last_heading = chap.title
    explicit = set(int(n) for n in re.findall(r"<p><strong>Table %s-(\d+):" % re.escape(chap.num), html_))
    auto = 0
    for m in re.finditer(r"<h[23][^>]*>(?:<span class=\"hnum\">[^<]*</span>)?(.*?)</h[23]>|<table( class=\"zebra\")?>", html_, re.S):
        if m.group(0).startswith("<h"):
            last_heading = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            continue
        before = html_[pos:m.start()]
        if html_.rfind("<blockquote", 0, m.start()) > html_.rfind("</blockquote>", 0, m.start()):
            out.append(before)
            out.append('<div class="table-wrap">' + m.group(0))
            pos = m.end()
            continue
        chap.tables += 1
        cap, n = None, None
        lm = re.search(r"<p><strong>(?:Table (\d+)-(\d+):\s*)?([^<]{2,100})</strong></p>\s*$", before)
        if lm:
            cap = lm.group(3).rstrip(":. ")
            n = int(lm.group(2)) if lm.group(2) else None
            before = before[:lm.start()]
        if not cap:
            cap = last_heading
        if n is None:
            auto += 1
            while auto in explicit:
                auto += 1
            n = auto
        label = "Table %s-%d" % (chap.num, n)
        out.append(before)
        out.append('<div class="table-wrap" id="tbl-%s-%d"><p class="tcaption"><span class="flabel">%s</span> %s</p>%s'
                   % (chap.num, n, label, cap, m.group(0)))
        pos = m.end()
    out.append(html_[pos:])
    joined = "".join(out).replace("</table>", "</table></div>")

    # style guide §2.4: tables under 12 rows do not break; longer ones repeat their header row
    def keep(m):
        rows = m.group(0).count("<tr")
        return m.group(0) if rows - 1 >= 12 else m.group(0).replace('<div class="table-wrap"', '<div class="table-wrap keep"', 1)
    return re.sub(r'<div class="table-wrap".*?</table></div>', keep, joined, flags=re.S)


# ----------------------------------------------------------------------------------------
# cross-references
# ----------------------------------------------------------------------------------------
DOC_BEFORE = re.compile(r"(PACKAGE|SPEC|GUIDE|COLORS|BRIEF|LOG|\.md|\.json)[`\s]*$")


def link_refs(doc, ids):
    parts = re.split(r"(<[^>]+>)", doc)
    depth_a = 0
    in_head = 0
    for k, p in enumerate(parts):
        if p.startswith("<"):
            if re.match(r"<a\b", p):
                depth_a += 1
            elif p.startswith("</a"):
                depth_a -= 1
            elif re.match(r"<h[1-6]\b", p):
                in_head += 1
            elif re.match(r"</h[1-6]", p):
                in_head -= 1
            continue
        if depth_a or in_head:
            continue

        def sec(m):
            # include the element just before, so "<code>…PACKAGE.md</code> §6" is not linked
            pre = re.sub(r"<[^>]+>", "", "".join(parts[max(0, k - 3):k])) + parts[k][:m.start()]
            tid = "s-" + m.group(2).replace(".", "-")
            if tid not in ids or DOC_BEFORE.search(pre[-30:]):
                return m.group(0)
            return '%s<a class="xref" href="#%s">%s</a>' % (m.group(1), tid, m.group(2))

        p = re.sub(r"((?:Sections?|§)\s?)(\d+(?:\.\d+)*)(?![\d.]*\d)", sec, p)
        parts[k] = p
    doc = "".join(parts)
    # rule references are bold in the source
    doc = re.sub(r"<strong>([GR]\d{3})</strong>",
                 lambda m: '<a class="xref rule-ref" href="#%s"><strong>%s</strong></a>' % (m.group(1), m.group(1))
                 if m.group(1) in ids else m.group(0), doc)
    return doc


NBSP_UNIT = re.compile(r"(\d) (in|ft|lb|lbs|oz|s|sec|min|ms|mm|cm|m|kg|g|V|W|A|Hz|pt|pts|RP)(?![\w-])")
NBSP_LABEL = re.compile(r"\b(Section|Sections|Table|Figure|Plate|Appendix|§) (?=[\dA-Z]|$)")


def nbsp(doc):
    """Style guide §4.4: a no-break space between a number and its unit, and after the words
    that introduce a cross-reference number.  Text only: tags, code, SVG and style are skipped."""
    parts = re.split(r"(<[^>]+>)", doc)
    skip = 0
    for k, p in enumerate(parts):
        if p.startswith("<"):
            m = re.match(r"<(/?)(pre|code|svg|style|script)\b", p)
            if m:
                skip += -1 if m.group(1) else 1
            continue
        if not skip and p:
            parts[k] = NBSP_LABEL.sub("\\1\u00a0", NBSP_UNIT.sub("\\1\u00a0\\2", p))
    return "".join(parts)


# ----------------------------------------------------------------------------------------
# page furniture
# ----------------------------------------------------------------------------------------
MOUNTAIN_SVG = """<svg class="cover-art" viewBox="0 0 850 420" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
  <polygon points="0,420 0,300 120,215 205,262 330,120 420,190 470,160 610,40 700,120 760,95 850,170 850,420" fill="#1F4E79"/>
  <polygon points="0,420 0,345 150,262 250,318 360,205 470,285 560,215 690,300 850,238 850,420" fill="#2E6FA8" opacity="0.55"/>
  <polygon points="330,120 368,152 350,160 382,188 420,190 470,160 610,40 560,95 520,108 488,150 450,168 402,150" fill="#DCE6F1" opacity="0.9"/>
  <polygon points="610,40 640,68 626,76 660,98 700,120 760,95 700,96 668,78" fill="#DCE6F1" opacity="0.9"/>
  <polygon points="0,420 0,392 200,338 380,372 560,330 850,368 850,420" fill="#0F2740"/>
  <line x1="610" y1="40" x2="610" y2="4" stroke="#FFFFFF" stroke-width="3"/>
  <polygon points="610,4 648,14 610,24" fill="#CC3333"/>
  <line x1="330" y1="120" x2="330" y2="88" stroke="#FFFFFF" stroke-width="3"/>
  <polygon points="330,88 364,97 330,106" fill="#1D63C8"/>
</svg>"""


def cover(info, rev):
    return """<section class="cover">
  <div class="cover-band">
    <div class="cover-kicker">Offseason Design Challenge</div>
    <div class="cover-wordmark">SUMMIT PUSH</div>
    %s
  </div>
  <div class="cover-body">
    <h1 class="cover-title">Game Manual</h1>
    <p class="cover-sub">%s</p>
    <p class="cover-version">Version %s</p>
  </div>
  <p class="cover-rev">Revision: %s &middot; %s</p>
  <span class="revision-stamp">%s</span>
</section>""" % (MOUNTAIN_SVG, html.escape(info["subtitle"]), info["version"], rev["id"],
                 date_long(rev["date"]), rev["id"])


def date_long(iso):
    d = datetime.date.fromisoformat(iso)
    return "%s %d, %d" % (d.strftime("%B"), d.day, d.year)


def contents(chapters, appendix):
    rows = []
    for c in chapters:
        rows.append('<li class="toc1"><a href="#%s"><span class="tnum">%s</span><span class="ttl">%s</span></a>'
                    '<span class="dots"></span><a class="pg" href="#%s"></a></li>'
                    % (c.id, c.num, html.escape(c.title + (" (%s)" % c.letter if c.letter else "")), c.id))
        for hid, num, title in c.h2:
            rows.append('<li class="toc2"><a href="#%s"><span class="tnum">%s</span><span class="ttl">%s</span></a>'
                        '<span class="dots"></span><a class="pg" href="#%s"></a></li>'
                        % (hid, num or "", html.escape(title), hid))
    rows.append('<li class="toc1"><a href="#%s"><span class="tnum">A</span><span class="ttl">%s</span></a>'
                '<span class="dots"></span><a class="pg" href="#%s"></a></li>' % (appendix, "Field Drawing Plates", appendix))
    return """<section class="front" id="contents">
  <h1 class="front-h1">Contents</h1>
  <ol class="toc">
%s
  </ol>
</section>""" % "\n".join("    " + r for r in rows)


def front_matter(info, revs):
    trs = "\n".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                    % (r["id"], r["date"], html.escape(r["sections"]), html.escape(r["summary"])) for r in revs)
    return """<section class="front" id="revision-history">
  <h1 class="front-h1">Revision History</h1>
  <div class="table-wrap"><p class="tcaption"><span class="flabel">Team Updates</span> Changes to this manual since kickoff</p>
  <table class="revtable"><thead><tr><th>Update</th><th>Date</th><th>Sections</th><th>Summary</th></tr></thead>
  <tbody>
%s
  </tbody></table></div>
  <h2 class="front-h2">Version precedence</h2>
  <p>This manual and every Team Update issued after it together form the current ruleset. A Team Update
  amends the manual from the date it is published. Where this manual and the SUMMIT PUSH design
  specification (<code>01-design/DESIGN-SPEC.md</code>) disagree, the design specification governs, and the
  discrepancy is corrected in the next Team Update.</p>
  <h2 class="front-h2">Copyright and license</h2>
  <p>&copy; 2026 Eric Dean. All rights reserved. This manual may be copied, printed and shared unmodified
  for training and educational use, with credit, under the SUMMIT PUSH Training Use License
  (<code>LICENSE.md</code> at https://github.com/XrxcGH/SUMMIT-PUSH). Commercial use, modified versions
  and machine-learning use need the copyright holder's written permission.</p>
  <h2 class="front-h2">Units</h2>
  <p>Dimensions are in inches, weights in pounds and times in minutes and seconds. Imperial values govern.</p>
  <h2 class="front-h2">Independence</h2>
  <p>SUMMIT PUSH is an original game written for robotics design training. It is not affiliated with,
  sponsored by or endorsed by any robotics competition organization. This is Version %s of the manual.</p>
</section>""" % (trs, info["version"])


def appendix_page(appendix, first_plate):
    rows = []
    for k, (f, name) in enumerate(PLATES):
        page = str(first_plate + k) if first_plate else ""
        rows.append("<tr><td class=\"num\">%d</td><td>%s</td><td><code>03-field/renderings/%s</code></td><td class=\"num\">%s</td></tr>"
                    % (k + 1, name, f, page))
    return """<section class="chapter appendix" id="%s">
  <div class="opener"><span class="opener-num">A</span><h1><span class="footer-title">A  Field Drawing Plates</span>Field Drawing Plates</h1></div>
  <p>The six drawing sheets of the field drawing set follow this page, each on its own landscape ANSI C
  (22&nbsp;&times;&nbsp;17 in) plate so that no dimension or note prints smaller than 6 pt. Every sheet carries its
  own title block. The sheets are generated from the master dimension ledger in
  <code>03-field/FIELD-CAD-PACKAGE.md</code> Section 10; where a sheet and the ledger disagree, the
  ledger governs.</p>
  <div class="table-wrap"><p class="tcaption"><span class="flabel">Table A-1</span> Drawing plates</p>
  <table><thead><tr><th class="num">Plate</th><th>Sheet</th><th>Source</th><th class="num">Page</th></tr></thead>
  <tbody>
%s
  </tbody></table></div>
</section>""" % (appendix, "\n".join(rows))


def inline_svg(path, prefix):
    """A drawing sheet as inline SVG, so its text is set in the page's embedded fonts (an SVG
    loaded as an image cannot use them).  Ids are prefixed so six sheets can share one page."""
    text = read(path)
    text = re.sub(r"<\?xml[^>]*\?>\s*|<!DOCTYPE[^>]*>\s*", "", text)
    ids = set(re.findall(r'\bid="([^"]+)"', text))
    for i in sorted(ids, key=len, reverse=True):
        text = text.replace('id="%s"' % i, 'id="%s-%s"' % (prefix, i))
        text = text.replace("url(#%s)" % i, "url(#%s-%s)" % (prefix, i))
        text = re.sub(r'href="#%s"' % re.escape(i), 'href="#%s-%s"' % (prefix, i), text)
    return re.sub(r"<svg\b", '<svg class="sheet"', text, count=1)


def plates_html(info, rev, first_plate, total):
    pages = []
    for k, (f, name) in enumerate(PLATES):
        pg = "%d of %d" % (first_plate + k, total) if first_plate else ""
        pages.append("""<div class="plate">
  <div class="plate-label"><b>Plate %d</b> &nbsp;%s</div>
  <div class="plate-art">%s</div>
  <div class="plate-foot"><span>A  Field Drawing Plates</span><span>Revision: %s</span><span>%s</span></div>
</div>""" % (k + 1, html.escape(name), inline_svg(os.path.join(SHEETS, f), "p%d" % (k + 1)), rev["id"], pg))
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>%s — Drawing Plates</title>
<link rel="stylesheet" href="../fonts.css"><link rel="stylesheet" href="../plates.css"></head>
<body>
%s
</body></html>""" % (html.escape(info["title"]), "\n".join(pages))


# ----------------------------------------------------------------------------------------
def build(total=None, first_plate=None):
    info = header_info()
    revs = revisions()
    rev = revs[-1]
    parser = md()
    chapters, figures = [], []
    files = sorted(f for f in os.listdir(os.path.join(MANUAL, "sections")) if f.endswith(".md"))
    for f in files:
        toks = parser.parse(read(os.path.join(MANUAL, "sections", f)))
        for chap, ctoks in annotate(toks, chapters, figures):
            render_chapter(parser, chap, ctoks, figures)
    appendix = "appendix-a"
    body = []
    for c in chapters:
        mini = "".join('<li><span class="tnum">%s</span>%s</li>' % (num or "", html.escape(t)) for _, num, t in c.h2)
        body.append("""<section class="chapter" id="%s">
  <div class="opener"><span class="opener-num">%s</span><h1><span class="footer-title">%s</span>%s</h1>%s</div>
%s
</section>""" % (c.id, c.num, html.escape(c.footer), html.escape(c.title + (" (%s)" % c.letter if c.letter else "")),
                 ('<ul class="opener-list">%s</ul>' % mini) if mini else "", c.html))
    doc = "\n".join([cover(info, rev), contents(chapters, appendix), front_matter(info, revs)] + body
                    + [appendix_page(appendix, first_plate)])
    ids = set(re.findall(r'\bid="([^"]+)"', doc))
    doc = nbsp(link_refs(doc, ids))
    missing = sorted(set(re.findall(r'href="#([^"]+)"', doc)) - ids)
    if missing:
        raise SystemExit("unresolved links: %s" % missing)
    # the revision stamp and (second pass) the page total including the plates
    total_css = '<style>@page { @bottom-center { content: "Revision: %s"; } }' % rev["id"]
    if total:
        total_css += '\n@page { @bottom-right { content: counter(page) " of %d"; } }' % total
        total_css += '\n@page front { @bottom-right { content: counter(page); } }'
    total_css += "</style>"
    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>%s</title>
<link rel="stylesheet" href="../fonts.css">
<link rel="stylesheet" href="../manual-print.css">
%s
<script>window.PagedConfig = { auto: false };</script>
<script src="../node_modules/pagedjs/dist/paged.polyfill.js"></script>
<script src="../furniture.js"></script>
</head>
<body>
%s
</body></html>""" % (html.escape("%s — Version %s" % (info["title"], info["version"])), total_css, doc)
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "manual.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    with open(os.path.join(BUILD, "plates.html"), "w", encoding="utf-8") as fh:
        fh.write(plates_html(info, rev, first_plate, total))
    meta = {"title": info["title"], "version": info["version"], "revision": rev["id"],
            "chapters": [c.footer for c in chapters], "figures": len(figures),
            "tables": sum(c.tables for c in chapters), "rules": len(re.findall(r'<p class="rule"', doc))}
    with open(os.path.join(BUILD, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--total", type=int, help="total page count (manual + plates) for the footers")
    ap.add_argument("--plates-from", type=int, help="page number of the first plate")
    a = ap.parse_args()
    meta = build(a.total, a.plates_from)
    print("manual.html: %d sections, %d rules, %d tables, %d figures" % (len(meta["chapters"]), meta["rules"], meta["tables"], meta["figures"]))


if __name__ == "__main__":
    main()
