# SUMMIT PUSH — Manual Typesetting Style Guide

**Document:** `06-style/MANUAL-STYLE-GUIDE.md` · **Applies to:** the PDF edition compiled from `02-manual/sections/*.md`
**Background:** `06-style/research-notes.md` holds the full research pass this guide was distilled from, including the reference values that were examined and deliberately *not* adopted.

---

## 1. Scope and Intent

This is the binding typographic and structural specification for producing a print-ready PDF edition of the SUMMIT PUSH Game Manual from its Markdown sources. The Markdown remains the working format; the PDF is the presentation format.

The target is the **genre convention** of a modern competitive-robotics rulebook: a single-column, print-first document with hanging-indent rule numbering, colored rule headlines, tinted commentary boxes, demoted violation lines, and a running footer that carries section identity and revision state. That structure is what is being matched.

**What is deliberately not copied.** No logos, wordmarks, lockups, or banner artwork of any organization. No organization or program names. No corporate palette. No boilerplate legal text. Layout geometry and structural convention are not anyone's property; identity is. The palette, typefaces, and wordmark treatment below are original to this package.

| Adopted | Not adopted |
|---|---|
| Page size, margins, measure, indent ladder | Logos, wordmarks, banner artwork |
| Rule numbering scheme, hanging indents, footer anatomy | Organization and program names |
| Typographic *relationships* (11 pt body, colored 13 pt H2, 9 pt italic captions) | Any real organization's brand hex values |
| Semantic color-coding as an idea | Trademarked color/type pairings |

### 1.1 Design goals, in priority order

1. **Unambiguous rule addressing.** A reader must be able to say "G412" aloud and find it in seconds.
2. **Visual demotion of non-normative text.** Commentary and violation consequences must never be mistaken for rule text.
3. **Print fidelity first.** The PDF is the commanding version; screen rendering is a courtesy.
4. **Reproducibility.** Every value here is a token. No magic numbers in source files.
5. **Legal cleanliness.** Nothing in the output requires anyone's permission to distribute.

---

## 2. Page Setup

| Property | Value |
|---|---|
| Page size | **US Letter, 8.5 × 11 in (612 × 792 pt)**, portrait throughout |
| Bleed | **0.125 in on every page.** The header band and its rule bleed on all four page types, so body pages need it too; a full-bleed element on a page without bleed trims to a white hairline. |
| Color space | sRGB |
| Margins (body pages) | top **1.30 in**, bottom **0.85 in**, left/right **0.75 in** |
| Live measure | **7.00 in (504 pt)** — about 95–100 characters at 11 pt |
| Columns | **Single column, ragged right, never justified** |

An A4 variant (210 × 297 mm) is permitted as a secondary build; keep the same measure and let the extra height fall into the bottom margin. Letter is canonical.

### 2.1 The indent ladder

Below the heading level, hierarchy is carried entirely by indentation — never by columns and never by size jumps.

| Level | Left indent | Hanging | Used for |
|---|---|---|---|
| 0 | 0.00 in | — | Body paragraphs |
| 1 | 0.50 in | −0.50 in | Rule numbers (the number hangs into the margin) |
| 1c | 0.50 in | 0 | Rule continuation paragraphs, `Violation:` lines |
| 2 | 1.00 in | −0.25 in | Lettered sub-clauses (a., b., c.) |
| 3 | 1.25 in | −0.25 in | Bullets inside sub-clauses |
| Box | 1.00 in both sides | — | Example and Commentary boxes (measure 5.00 in) |

The box is inset deeper on *both* sides than any text indent. That double inset is what makes it read as an aside without a heavy border.

### 2.2 Header

A **1.19 in (86 pt) full-bleed band** across the top of every page except the cover:

- Ground: solid `--accent-deep`.
- Left: the SUMMIT PUSH wordmark set as **type** — Roboto Condensed Bold, 14 pt, `--paper`, +0.5 pt tracking, ALL CAPS. Not an image file.
- A 1 pt vertical rule in `--accent-bright` at x = 2.60 in, from y = 0.28 in to y = 0.91 in.
- Right, right-aligned: `SUMMIT PUSH — Game Manual` in 9 pt Roboto Regular, `--paper-dim`.
- A 2.2 pt full-bleed horizontal rule in `--accent-bright` flush to the band's bottom edge.

No running header text. All wayfinding lives in the footer.

### 2.3 Footer

Baseline **0.50 in** from trim, Roboto Bold 10 pt, `--ink`, three tab cells across the full measure:

```
5  Game Rules (G)                      Revision: TU-00               52 of 104
```

- **Left:** the H1 line verbatim — number, title, and any parenthetical rule letter — because that is exactly what `string-set: section-title content()` captures (§9.2). There is no "Section" prefix; adding one means prepending it in the CSS, not in the source. This is the reader's primary wayfinding device.
- **Center:** revision stamp, `Revision: TU-NN`, incremented per Team Update.
- **Right:** `N of TOTAL`. Bare numbers, no "Page" prefix.

Front matter uses a page number only. The cover uses the revision stamp only, centered.

### 2.4 Break control

- Every top-level section starts on a fresh page.
- Never break between a rule number and its first line, between a rule's last line and its `Violation:` line, or between a caption and its object.
- Widows and orphans: minimum 2 lines.
- Tables under 12 rows do not break; longer tables repeat the header row.

---

## 3. Color Palette (normative)

The manual palette is deliberately distinct from any real organization's. It is a deep slate-indigo family with warm secondaries.

| Token | Hex | Role | Contrast on paper |
|---|---|---|---|
| `--ink` | `#1A1D21` | Body text, H1, H3–H6, rule numbers | 16.9 : 1 |
| `--paper` | `#FFFFFF` | Page ground | — |
| `--paper-dim` | `#F4F5F7` | Zebra row fill, code ground | — |
| `--accent` | `#1F4E79` | **H2 headings**, table header fill, box border, rule headlines | 8.7 : 1 |
| `--accent-bright` | `#2E6FA8` | Decorative rules only — **never body text** | 5.3 : 1 (large only) |
| `--accent-deep` | `#16385A` | Header band, cover band, section-opener wash | 12.0 : 1 |
| `--muted` | `#6E7378` | `Violation:` lines, caption secondary text, TOC leaders | 4.8 : 1 |
| `--rule-line` | `#C8CCD1` | Table body rules, hairlines | — |
| `--rule-line-strong` | `#8A9199` | Table outer border, section dividers | — |
| `--box-fill` | `#DCE6F1` | Commentary and Example box tint | ink 13.4 : 1 |
| `--box-border` | `#1F4E79` | Box 1.5 pt border | — |
| `--warn-fill` / `--warn-border` | `#FBEBD2` / `#B26A12` | Caution box | ink 14.4 : 1 |
| `--danger-fill` / `--danger-border` | `#F7DEDE` / `#A32A2A` | Safety-critical warning box | ink 13.3 : 1 |
| `--change-add` | `#FFF3A8` | Team Update addition highlight | — |
| `--link` | `#245C9E` | Cross-references and URLs, underlined | 6.8 : 1 |

### 3.1 Alliance colors

These match the drawing set and `03-field/MATERIALS-AND-COLORS.md` exactly. Do not introduce a second alliance palette for the manual.

One token deliberately does not match the drawing set: `--carpet` is `#6E6A63`, the physical carpet, while `_drawlib.py` renders the carpet as `#F4F2EE` so that linework stays readable as ink on paper. Every other token above is identical in both.

| Token | Hex | Role |
|---|---|---|
| `--alliance-blue` | `#1D63C8` | Blue alliance fills, keylines, callout boxes |
| `--alliance-blue-dark` | `#0E3F86` | Blue outlines, shaded faces |
| `--alliance-blue-tint` | `#D9E4F5` | Table cell tint |
| `--alliance-red` | `#CC3333` | Red alliance fills, keylines, callout boxes |
| `--alliance-red-dark` | `#8E2020` | Red outlines, shaded faces |
| `--alliance-red-tint` | `#F6DADA` | Table cell tint |
| `--neutral-wash` | `rgba(214, 178, 42, 0.35)` | Neutral zone overlay |
| `--carpet` | `#6E6A63` | Field carpet in renders |
| `--callout-leader` | `#E100E1` | Leader lines and arrowheads in figures — **reserved, never used elsewhere** |

Zone washes are composited: alliance hue at 38% opacity over `--carpet`, with a 1.5 pt keyline in the fully saturated hue so the boundary stays crisp.

### 3.2 Color usage rules

1. **Only H2 is colored.** H1 and H3–H6 are `--ink`.
2. **Rule numbers are never colored.** Bold `--ink`, always. Color lives on the headline that follows.
3. **Never encode meaning in color alone.** `Violation:` lines carry the literal word in addition to the gray italic; alliance-tinted table cells carry a literal "Red"/"Blue" label. Print in grayscale as an acceptance test — every distinction must survive.
4. **Minimum contrast 4.5 : 1** for body-size text, 3 : 1 for ≥ 14 pt bold. `--accent-bright` is banned from body text.

---

## 4. Typography

All faces are freely licensed and must be vendored into `assets/fonts/` and embedded in the PDF.

| Role | Family | License |
|---|---|---|
| Body, headings, tables | **Roboto** (400, 400i, 500, 700, 700i) | Apache 2.0 |
| Condensed (header band, drawing sheets) | **Roboto Condensed** (400, 700) | Apache 2.0 |
| Monospace (code, coordinates, part numbers) | **JetBrains Mono** (400, 700) | OFL 1.1 |

```css
--font-sans: "Roboto", "Arimo", "Liberation Sans", Arial, sans-serif;
--font-cond: "Roboto Condensed", "Liberation Sans Narrow", "Arial Narrow", sans-serif;
--font-mono: "JetBrains Mono", "DejaVu Sans Mono", Consolas, monospace;
```

### 4.1 Type scale

| Style | Family / weight | Size | Line height | Space before | Color | Notes |
|---|---|---|---|---|---|---|
| Cover title | Roboto Bold | 40 pt | 1.05 | — | `--ink` | centered |
| Cover subtitle | Roboto Regular | 14 pt | 1.25 | 8 pt | `--muted` | centered, +0.5 pt tracking |
| Section-opener number | Roboto Bold | 40 pt | 1.00 | — | `--accent-deep` | in the opener wash |
| **H1** (section) | Roboto Bold | **16 pt** | 1.20 | 12 pt | `--ink` | +1 pt tracking, hanging −0.50 in |
| **H2** (subsection) | Roboto Bold | **13 pt** | 1.25 | 12 pt | **`--accent`** | hanging −0.40 in |
| **H3** | Roboto Bold | 11 pt | 1.35 | 10 pt | `--ink` | hanging −0.50 in |
| **H4** | Roboto Italic | 11 pt | 1.35 | 8 pt | `--ink` | hanging −0.60 in |
| **Body** | Roboto Regular | **11 pt** | **1.38** | **6 pt** | `--ink` | ragged right |
| **Rule number** | Roboto Bold | 11 pt | 1.38 | 6 pt | `--ink` | hanging −0.50 in |
| **Rule headline** | Roboto Bold | 11 pt | inline | — | `--accent` | not italic |
| **Violation line** | Roboto Italic | 11 pt | 1.38 | 6 pt | **`--muted`** | indent 0.50 in, whole line italic |
| Lettered sub-clause | Roboto Regular | 11 pt | 1.38 | 6 pt | `--ink` | indent 1.00 in, hanging −0.25 in |
| Box body | Roboto Regular | 11 pt | 1.38 | 6 pt | `--ink` | inset 1.00 in both sides |
| Figure / table caption | Roboto Italic | **9 pt** | 1.30 | 6 pt (10 pt after) | `--ink` | **above** the object |
| Table body | Roboto Regular | **10 pt** | 1.30 | — | `--ink` | tabular figures on |
| Table header | Roboto Bold | 10 pt | 1.25 | — | `--paper` on `--accent` | |
| Footer | Roboto Bold | 10 pt | 1.20 | — | `--ink` | three tab cells |
| Header wordmark | Roboto Condensed Bold | 14 pt | 1.00 | — | `--paper` | caps, +0.5 pt tracking |
| Inline code | JetBrains Mono | 9.5 pt | 1.35 | — | `--ink` | `--paper-dim` ground |
| Code block | JetBrains Mono | 9 pt | 1.40 | 6 pt | `--ink` | `--paper-dim` ground, 1 pt border |
| Glossary term | Roboto Bold | 10 pt | 1.30 | — | `--ink` | ALL CAPS |

### 4.2 The paragraph spacing model

**Space-before only. Zero space-after on every style except captions.** Every paragraph carries 6 pt above and 0 below. Consequences: spacing never doubles at a paragraph boundary; a rule, its sub-clauses, and its violation line stack at a consistent 6 pt rhythm; headings carry a larger space-before (10–12 pt) and near-zero after, so a heading sits tight to what it introduces and loose from what precedes it. Captions are the one exception: 6 pt above, 10 pt below.

### 4.3 Below H2, hierarchy is indentation, not size

H3 and H4 are both 11 pt — the same size as body text. They differ by weight, style, and position on the indent ladder. This is deliberate and is what keeps a long rulebook from becoming a size-jump staircase. Do not "fix" it by scaling H3 up.

### 4.4 Miscellaneous

- Never justify. Hyphenation off in body and rule text, on in table cells narrower than 1.2 in.
- Tabular figures on in every table, coordinate list, and the TOC page-number column.
- Em dashes unspaced; en dashes for ranges (`10–20 in`).
- Non-breaking space between a number and its unit (`24 in`).
- Small caps: never. Defined terms are hard-typed capitals.
- Dimensions imperial first, metric in parentheses. State once in Section 1 that imperial governs. Round metric so it stays rule-compliant: **maximums round down, minimums round up.**

---

## 5. Structural Conventions

### 5.1 Section inventory

Nine top-level sections; each starts on a fresh page. Sections that carry rules append their rule letter to the title so the footer is self-documenting.

| # | Title | Rule letter |
|---|---|---|
| 1 | Introduction | — |
| 2 | Game Overview | — |
| 3 | ARENA | — |
| 4 | Match Play & Scoring | — |
| 5 | Game Rules | (G) |
| 6 | Robot Construction Rules | (R) |
| 7 | Inspection & Eligibility | — |
| 8 | Tournament | — |
| 9 | Glossary | — |

### 5.2 Rule anatomy

A rule is one paragraph beginning with a hanging rule number, followed by a headline sentence — italic in the Markdown source, set **bold** and `--accent` in the PDF (§4.1, §9.2) — followed by the rule body, followed by an indented `Violation:` line set in `--muted` italic.

```
G412   The HEADWALL ZONE is protected during ENDGAME — line call.
       From the start of the ENDGAME period until climb assessment is
       complete (Section 4.5.3), a ROBOT may not …

       Violation: MAJOR FOUL per instance. …
```

- The **number** is Roboto Bold 11 pt `--ink`, hanging 0.50 in into the margin.
- The **headline** is a short imperative or descriptive sentence, bold, `--accent`, ending in a period, on the same line as the number.
- The **body** is regular weight, `--ink`, and starts on the same line as the headline.
- The **`Violation:` line** is a separate paragraph, indented 0.50 in, entirely italic, `--muted`, beginning with the literal word "Violation:".
- Rules never nest. Sub-clauses are lettered `a.`, `b.`, `c.` at indent level 2.

### 5.3 Defined terms

Defined terms are hard-typed in capitals in the source (`ROBOT`, `SCORED`, `CRAG APRON`) and are **not** restyled at typeset time — no small caps, no color, no bold. Feature names that are not defined terms (Low Socket, Shelf 1, slot fence) stay title case. The Glossary is the authority for which is which.

### 5.4 Cross-references

- Rule references: bold, `--link`, no underline in print — `**G412**`.
- Section references: `Section 4.5.3` in running text, `§4.5.3` inside tables and boxes. Both hyperlink in the PDF.
- Figure and table references: `Figure 3-4`, `Table 6-1` — section number, then sequence within the section.

### 5.5 Boxes

Two box types, both inset 1.00 in on each side (5.00 in measure), 1.5 pt `--box-border` border, `--box-fill` ground, 8 pt internal padding:

- **Example** — a binding interpretation. Label in Roboto Bold Italic 10 pt `--accent`, then the text.
- **Commentary** — non-binding design rationale. Same treatment; the label is the only difference.

A **Caution** box (`--warn-fill` / `--warn-border`) is reserved for procedural warnings, and a **Warning** box (`--danger-fill` / `--danger-border`) for safety-critical text. Neither is used for rules.

---

## 6. Tables

- Header row: `--accent` fill, `--paper` bold 10 pt type, no vertical rules.
- Body rows: 10 pt, 0.5 pt `--rule-line` horizontal rules only; zebra fill `--paper-dim` on even rows for tables over 8 rows.
- Outer border: 1 pt `--rule-line-strong`.
- Cell padding 4 pt vertical, 6 pt horizontal.
- **Alignment:** text left; integers and point values right; dimensions right on the decimal; units in the column header, not in every cell.
- **Scoring tables:** one row per scoring position or tier, AUTO and TELEOP as separate right-aligned columns, point values bold. Never merge the AUTO and TELEOP columns.
- **Alliance-differentiated tables:** tint the cell with `--alliance-*-tint` **and** label it "Blue"/"Red". Tint alone is not sufficient.
- A table that will not fit the measure is restructured — transposed, split by tier, or moved to a landscape figure. Never rotate a page.

---

## 7. Figures and Drawing Sheets

### 7.1 Numbering and captions

Figures are numbered `Figure <section>-<sequence>` and captioned **above** the image, Roboto Italic 9 pt, 6 pt above and 10 pt below. Every figure has a caption; a figure that needs no caption does not need to be a figure.

### 7.2 Field renders

- Top-down plan views use `--carpet` ground, alliance zone washes at 38% opacity with saturated keylines, and white neutral marks.
- Isometric renders use lit/shade variants of the alliance colors on angled faces.
- The manual's plan views tint the CRAGS in alliance color for legibility; the physical CRAG is tan (`03-field/MATERIALS-AND-COLORS.md` §3, rule 2). Say so in the caption the first time.
- Every plan view carries a coordinate compass: origin marker, +X arrow, +Y arrow, and the words "always-blue-origin NWU".

### 7.3 Callouts

Leader lines and arrowheads use `--callout-leader` (`#E100E1`), 1.5 pt, with a 3 pt arrowhead. That color appears nowhere else in the field palette, so a callout can never be mistaken for field hardware. Leaders never cross each other and never cross a dimension line.

### 7.4 Drawing sheets

The six sheets in `03-field/renderings/` are reproduced on dedicated **landscape ANSI C (22 × 17 in) plates, one per sheet, at not less than 20.5 in of image width** — the standard sheet size for a drawing set, and the smallest that satisfies the 6-pt floor below. They cannot be run at the 7.00-in body measure: `crag.svg` is 1960 user units wide, so at 504 pt its 8-unit note text prints at about 2 pt and its largest type at about 5.4 pt. The other five sheets fall in the same range — smallest type 2.3 to 3.0 pt at body width — and a 6-pt floor needs 13.9 in (`apriltag-map`) to 20.4 in (`crag`) of image width — which is why the plate is ANSI C rather than 11 × 17: at 15 in five of the six sheets would still fall below 6 pt, and 20.4 in does not fit on a tabloid plate at any margin. A thumbnail may appear inline in the body, cross-referenced to the full-size plate. Each sheet carries its own title block, so no figure caption is added — only a `Figure 3-N` label line above it. Sheet conventions:

- Dimension lines and text in `#C02020`; extension lines 0.7 pt; arrowheads at both ends.
- Each sheet's primary view carries its scale in the sheet subtitle; every additional view carries its own name and px/in scale, and the title block repeats "Scale: as noted per view".
- Every sheet carries a title block: sheet name, sheet number of six, units note, scale note, tolerance note, revision, and the governing document reference.
- CRITICAL dimensions are boxed; reference dimensions are suffixed `(ref)`.

---

## 8. Front and Back Matter

| Page | Content |
|---|---|
| Cover | Title, subtitle, version, revision stamp. `--accent-deep` band, no logo. |
| Contents | Two levels deep, dot leaders, tabular page numbers. |
| Revision history | One row per Team Update: number, date, sections touched, one-line summary. |
| Version precedence | One paragraph stating that the manual plus all Team Updates is the current ruleset, and that the design specification governs any discrepancy. |
| Glossary | Section 9. Two-column table, terms in Roboto Bold 10 pt ALL CAPS, definitions 10 pt regular, alphabetical. |

No index. A well-cross-referenced 100-page manual with a hyperlinked TOC does not need one, and a bad index is worse than none. (The compiled Markdown is 1,579 lines and 30,917 words — about 52 pages of running text at 11 pt on a 7.00-in measure, and roughly 100 once its 32 tables, callout boxes and section openers are set.)

---

## 9. Production Recipe

### 9.1 Recommended toolchain

**Pandoc → HTML → Paged.js → headless Chromium → PDF.** Reasons: the sources are Markdown with tables and blockquotes, which Pandoc handles natively; the whole spec above is expressible in a CSS print stylesheet; Paged.js implements running headers/footers, page counters, and break control; and the result is inspectable in a browser during development.

```bash
# 1. compile the manual sources
bash 02-manual/build.sh

# 2. Markdown -> standalone HTML with the print stylesheet
pandoc 02-manual/GAME-MANUAL.md \
  --from=gfm --to=html5 --standalone \
  --metadata title="SUMMIT PUSH — Official Game Manual" \
  --css=06-style/manual-print.css \
  --output=build/manual.html

# 3. paginate and render
#    (paged.js polyfill is included by manual-print.css; any headless
#     Chromium with --print-to-pdf and --no-margins produces the PDF)
```

`06-style/manual-print.css`, `assets/fonts/` and `build/` are **not shipped with this package**: §9.2 is the sketch from which to author the stylesheet, the three families are downloaded from Google Fonts, and `build/` must be created before step 2. The recipe is a specification, not a turnkey script.

A LaTeX route (`pandoc --pdf-engine=lualatex` with a custom class) is a viable alternative and produces better hyphenation and float control, at the cost of expressing the palette and boxes in TeX rather than CSS. A Typst route is the third option and is the fastest to iterate. Pick one and commit; do not maintain two.

### 9.2 Starter stylesheet sketch

```css
@page {
  size: letter;
  margin: 1.30in 0.75in 0.85in 0.75in;
  @top-left-corner { content: ""; }
  @bottom-left   { content: string(section-title); font: bold 10pt var(--font-sans); }
  @bottom-center { content: "Revision: " string(revision); }
  @bottom-right  { content: counter(page) " of " counter(pages); }
}
:root {
  --ink:#1A1D21; --paper:#fff; --paper-dim:#F4F5F7;
  --accent:#1F4E79; --accent-bright:#2E6FA8; --accent-deep:#16385A;
  --muted:#6E7378; --rule-line:#C8CCD1; --rule-line-strong:#8A9199;
  --box-fill:#DCE6F1; --box-border:#1F4E79;
  --alliance-blue:#1D63C8; --alliance-red:#CC3333;
  --font-sans:"Roboto","Arimo","Liberation Sans",Arial,sans-serif;
  --font-cond:"Roboto Condensed","Liberation Sans Narrow",sans-serif;
  --font-mono:"JetBrains Mono","DejaVu Sans Mono",monospace;
}
body { font: 11pt/1.38 var(--font-sans); color: var(--ink); text-align: left; }
p    { margin: 6pt 0 0; }
h1   { font-size:16pt; font-weight:700; letter-spacing:1pt; margin:12pt 0 12pt;
       string-set: section-title content(); break-before: page; }
/* the revision stamp: a page-margin box has no originating element, so attr() has
   nothing to read there. Carry it in a named string set once in the front matter. */
.revision-stamp { string-set: revision content(); position: absolute; visibility: hidden; }
h2   { font-size:13pt; font-weight:700; color:var(--accent); margin:12pt 0 2pt; }
h3   { font-size:11pt; font-weight:700; margin:10pt 0 0; }

/* Rule paragraphs: the Markdown emits "**G412** *headline.* body" */
p:has(> strong:first-child)      { padding-left:.5in; text-indent:-.5in; }
p > strong:first-child + em      { font-style:normal; font-weight:700; color:var(--accent); }
p > em:only-child                { /* Violation: line */
  margin-left:.5in; color:var(--muted); font-style:italic; }

blockquote { margin:6pt 1in 0; padding:8pt; background:var(--box-fill);
             border:1.5pt solid var(--box-border); break-inside:avoid; }

table { width:100%; border-collapse:collapse; font-size:10pt;
        font-feature-settings:"tnum" 1; border:1pt solid var(--rule-line-strong); }
th    { background:var(--accent); color:#fff; font-weight:700; text-align:left;
        padding:4pt 6pt; }
td    { border-top:.5pt solid var(--rule-line); padding:4pt 6pt; }
tbody tr:nth-child(even) { background:var(--paper-dim); }

code, pre { font-family:var(--font-mono); background:var(--paper-dim); }
pre { font-size:9pt; line-height:1.40; padding:6pt; border:1pt solid var(--rule-line); }
```

### 9.3 Source conventions that make typesetting work

The Markdown already follows these; keep them:

- Rules are written `**G412** *Headline sentence.* Body text…` on one line, and the `Violation:` line is a separate paragraph written `*Violation:* …`.
- Examples and Commentary are blockquotes beginning `> *Example:*` / `> *Commentary:*`.
- Defined terms are hard-typed capitals in the source.
- Tables are GitHub-flavored pipe tables. They carry **no** alignment row — all 32 separator rows in the compiled manual are bare `|---|` — so Pandoc emits no per-cell alignment and §6's column rules are applied in CSS by column type, not from the source.
- Section headings are `# 5 Game Rules (G)` — number and title on the heading line, so `string-set: section-title` populates the footer with no extra markup.

### 9.4 Acceptance checks before release

- [ ] Print one copy in **grayscale**; every color-coded distinction still reads.
- [ ] Every rule number appears in the TOC-adjacent rule index (if built) and resolves.
- [ ] No page breaks between a rule and its `Violation:` line.
- [ ] Every figure has a caption above it and a `Figure N-M` label.
- [ ] Footer section name changes exactly at section boundaries.
- [ ] All fonts embedded; no system-font substitution warnings.
- [ ] Every drawing sheet is reproduced on its own landscape ANSI C plate at not less than 20.5 in of image width, so no type on any sheet sets below 6 pt.

---

## 10. What This Package Deliberately Does Not Do

- It does not use any real organization's name, logo, wordmark, color palette, or boilerplate.
- It does not claim affiliation with or endorsement by any robotics competition organization.
- It does not reproduce any existing manual's text.
- Its typeface choices are open-licensed and are not brand assets.

If any of that changes, this section is the first thing to revisit.
