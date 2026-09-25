# SUMMIT PUSH — Manual Typesetting Style Guide

**Document:** `organizers/source/typesetting/MANUAL-STYLE-GUIDE.md` · **Applies to:** the PDF edition compiled from `organizers/source/manual/sections/*.md` · **Implemented by:** `organizers/source/typesetting/pdf/`
**Background:** `organizers/source/typesetting/research-notes.md` records the research behind this guide, including reference values that were considered and not adopted.

---

## 1. Scope and Intent

This guide is the binding typographic and structural specification for the print-ready PDF edition of the SUMMIT PUSH Game Manual, which the build in `organizers/source/typesetting/pdf/` typesets from the Markdown sources (§9). The Markdown is the working format; the PDF is the presentation format.

The model is the genre convention of a modern competitive-robotics rulebook: a single-column, print-first document with hanging rule numbers, colored rule headlines, tinted commentary boxes, demoted violation lines, and a running footer that carries the section and the revision.

**What is not copied.** No organization's logos, wordmarks, lockups or banner artwork; no organization or program names; no corporate palette; no boilerplate legal text. Page geometry and structural conventions are common to the genre, and this guide adopts them. The palette and the wordmark treatment below are original to this package, and the typefaces are open-licensed (§4).

| Adopted | Not adopted |
|---|---|
| Page size, margins, measure, indent ladder | Logos, wordmarks, banner artwork |
| Rule numbering scheme, hanging indents, footer anatomy | Organization and program names |
| Typographic *relationships* (11 pt body, colored 13 pt H2, 9 pt italic captions) | Any real organization's brand hex values |
| Semantic color-coding as an idea | Trademarked color/type pairings |

### 1.1 Design goals, in priority order

1. **Rule addressing.** A reader must be able to say "G412" aloud and find the rule in seconds.
2. **Visual demotion of non-normative text.** Commentary and violation consequences must not be mistaken for rule text.
3. **Print fidelity.** The PDF is designed for print; screen rendering is a courtesy.
4. **Reproducibility.** Every value here is a token. No magic numbers in source files.
5. **Legal cleanliness.** Nothing in the output requires anyone's permission to distribute.

---

## 2. Page Setup

| Property | Value |
|---|---|
| Page size | **US Letter, 8.5 × 11 in (612 × 792 pt)**, portrait throughout |
| Bleed | **0.125 in on every page.** The header band and its rule bleed on every page except the cover, which has its own full-bleed band, so body pages need bleed too; a full-bleed element on a page without bleed trims to a white hairline. |
| Color space | sRGB |
| Margins (body pages) | top **1.30 in**, bottom **0.85 in**, left/right **0.75 in** |
| Live measure | **7.00 in (504 pt)** — about 95–100 characters at 11 pt |
| Columns | **Single column, ragged right, never justified** |

The six drawing plates (§7.4) are the one exception to this page setup: each is a landscape ANSI C page without bleed.

An A4 variant (210 × 297 mm) is permitted as a secondary build; keep the same measure and let the extra height fall into the bottom margin. Letter is canonical, and the build produces Letter only.

### 2.1 The indent ladder

Below the headings, indentation alone carries hierarchy. Do not use columns or changes of size for it.

| Level | Left indent | Hanging | Used for |
|---|---|---|---|
| 0 | 0.00 in | — | Body paragraphs |
| 1 | 0.50 in | −0.50 in | Rule numbers (the number hangs to the left edge of the measure) |
| 1c | 0.50 in | 0 | Rule continuation paragraphs, `Violation:` lines |
| 2 | 1.00 in | −0.25 in | Lettered sub-clauses (a., b., c.); reserved, as no current rule has them |
| 3 | 1.25 in | −0.25 in | Bullets inside sub-clauses; reserved |
| Box | 1.00 in both sides | — | Example and Commentary boxes (measure 5.00 in) |

The box is inset on both sides, deeper than any text indent. The double inset marks it as an aside without a heavy border.

### 2.2 Header

A 1.19 in (86 pt) full-bleed band runs across the top of every page except the cover. `furniture.js` draws it (§9.1).

- Ground: solid `--accent-deep`.
- Left: the SUMMIT PUSH wordmark, set as type rather than an image: Roboto Condensed Bold, 14 pt, `--paper`, +0.5 pt tracking, ALL CAPS.
- A 1 pt vertical rule in `--accent-bright` at x = 2.60 in, from y = 0.28 in to y = 0.91 in.
- Right, right-aligned: `SUMMIT PUSH — Game Manual` in 9 pt Roboto Regular, `--paper-dim`.
- A 2.2 pt full-bleed horizontal rule in `--accent-bright` along the band's bottom edge.

The header carries no running text. All wayfinding is in the footer.

### 2.3 Footer

Baseline 0.50 in from trim, Roboto Bold 10 pt, `--ink`, three tab cells across the full measure:

```
5  Game Rules (G)                      Revision: TU-00               52 of 104
```

- **Left:** the H1 line as written (number, title and any parenthetical rule letter), which is what `string-set: section-title content()` captures (§9.3). There is no "Section" prefix; if one is ever wanted, add it in the CSS and leave the source alone. This cell is the reader's primary wayfinding device.
- **Center:** the revision stamp, `Revision: TU-NN`, incremented with each Team Update.
- **Right:** `N of TOTAL`, bare numbers with no "Page" prefix. TOTAL includes the six drawing plates.

Front matter carries a page number only. The cover carries the revision stamp and its date, centered.

### 2.4 Break control

- Every top-level section starts on a fresh page.
- Never break between a rule number and its first line, between a rule's last line and its `Violation:` line, or between a caption and its object.
- Widows and orphans: minimum 2 lines.
- Tables under 12 rows do not break; longer tables repeat the header row.

---

## 3. Color Palette (normative)

The manual palette is distinct from any real organization's: a deep slate-indigo family with warm secondaries.

| Token | Hex | Role | Contrast on paper |
|---|---|---|---|
| `--ink` | `#1A1D21` | Body text, H1, H3–H6, rule numbers | 16.9 : 1 |
| `--paper` | `#FFFFFF` | Page ground | — |
| `--paper-dim` | `#F4F5F7` | Zebra row fill, code ground, plain note box ground, header title | — |
| `--accent` | `#1F4E79` | **H2 headings**, table header fill, box labels, rule headlines | 8.7 : 1 |
| `--accent-bright` | `#2E6FA8` | Decorative rules only — **never body text** | 5.3 : 1 (large only) |
| `--accent-deep` | `#16385A` | Header band, cover band, section-opener wash | 12.0 : 1 |
| `--muted` | `#6E7378` | `Violation:` lines, cover subtitle, deleted text, TOC leaders | 4.8 : 1 |
| `--rule-line` | `#C8CCD1` | Table body rules, hairlines | — |
| `--rule-line-strong` | `#8A9199` | Table outer border, section dividers | — |
| `--box-fill` | `#DCE6F1` | Commentary and Example box tint | ink 13.4 : 1 |
| `--box-border` | `#1F4E79` | Box 1.5 pt border | — |
| `--warn-fill` / `--warn-border` | `#FBEBD2` / `#8A520D` | Caution box | ink 14.4 : 1 |
| `--danger-fill` / `--danger-border` | `#F7DEDE` / `#A32A2A` | Safety-critical warning box | ink 13.3 : 1 |
| `--change-add` | `#FFF3A8` | Team Update addition highlight (`<ins>` in the source) | — |
| `--link` | `#245C9E` | Cross-references and URLs; not underlined in print | 6.8 : 1 |

### 3.1 Alliance colors

The alliance hues match the drawing set and `participants/03-field/MATERIALS-AND-COLORS.md`. Do not introduce a second alliance palette for the manual.

| Token | Hex | Role |
|---|---|---|
| `--alliance-blue` | `#1D63C8` | Blue alliance fills and keylines |
| `--alliance-blue-dark` | `#0E3F86` | Blue outlines, shaded faces |
| `--alliance-blue-tint` | `#D9E4F5` | Table cell tint |
| `--alliance-red` | `#CC3333` | Red alliance fills and keylines |
| `--alliance-red-dark` | `#8E2020` | Red outlines, shaded faces |
| `--alliance-red-tint` | `#F6DADA` | Table cell tint |
| `--neutral-wash` | `rgba(214, 178, 42, 0.35)` | Neutral zone overlay |
| `--carpet` | `#6E6A63` | Field carpet in renders |
| `--callout-leader` | `#E100E1` | Leader lines and arrowheads in figures — **reserved, never used elsewhere** |

One token differs from the drawing set by design: `--carpet` is `#6E6A63`, the physical carpet in `participants/03-field/MATERIALS-AND-COLORS.md`, while `organizers/source/drawings/_drawlib.py` draws the carpet as `#F4F2EE` so that linework stays readable as ink on paper. The drawing set also uses `--callout-leader`; the tints and `--neutral-wash` belong to the manual only.

On the drawing sheets a zone is a light wash of the alliance hue (10% opacity on the FIELD top view) inside a dashed 1.5 pt keyline in the dark alliance hue, so the boundary stays crisp over the light carpet.

### 3.2 Color usage rules

1. **Only H2 is colored.** H1 and H3–H6 are `--ink`.
2. **Rule numbers are never colored.** They are always bold `--ink`; the headline that follows carries the color.
3. **Never encode meaning in color alone.** `Violation:` lines carry the literal word as well as the gray italic; alliance-tinted table cells carry a literal "Red" or "Blue" label. Print in grayscale as an acceptance test (§9.4): every distinction must survive.
4. **Minimum contrast 4.5 : 1** for body-size text, 3 : 1 for ≥ 14 pt bold. `--accent-bright` is never used for body text.

---

## 4. Typography

All faces are licensed under the SIL Open Font License 1.1, vendored in `organizers/source/typesetting/pdf/fonts/` with their license files, and embedded in the PDF.

| Role | Family | License |
|---|---|---|
| Body, headings, tables | **Roboto** (400, 400i, 500, 700, 700i) | OFL 1.1 |
| Condensed (header band, drawing sheets) | **Roboto Condensed** (400, 700) | OFL 1.1 |
| Monospace (code, coordinates, part numbers) | **JetBrains Mono** (400, 700) | OFL 1.1 |

```css
--font-sans: "Roboto", "Noto Sans Math", "Arimo", "Liberation Sans", Arial, sans-serif;
--font-cond: "Roboto Condensed", "Noto Sans Math", "Liberation Sans Narrow", "Arial Narrow", sans-serif;
--font-mono: "JetBrains Mono", "DejaVu Sans Mono", Consolas, monospace;
```

Roboto has no arrows, so the build also vendors the arrows block (U+2190–21FF) of Noto Sans Math (400, OFL 1.1) and places it second in the sans and condensed stacks, directly after the primary face. `organizers/source/typesetting/pdf/vendor_fonts.py` regenerates the font files and `fonts.css`, copying only the weights and Unicode subsets the manual uses.

### 4.1 Type scale

| Style | Family / weight | Size | Line height | Space before | Color | Notes |
|---|---|---|---|---|---|---|
| Cover title | Roboto Bold | 40 pt | 1.05 | — | `--ink` | centered |
| Cover subtitle | Roboto Regular | 14 pt | 1.25 | 8 pt | `--muted` | centered, +0.5 pt tracking |
| Section-opener number | Roboto Bold | 40 pt | 1.00 | — | `--accent-deep` | in the opener wash |
| **H1** (section) | Roboto Bold | **16 pt** | 1.20 | — | `--ink` | +1 pt tracking, beside the opener number |
| **H2** (subsection) | Roboto Bold | **13 pt** | 1.25 | 12 pt | **`--accent`** | hanging −0.40 in |
| **H3** | Roboto Bold | 11 pt | 1.35 | 10 pt | `--ink` | hanging −0.50 in |
| **H4** | Roboto Italic | 11 pt | 1.35 | 8 pt | `--ink` | hanging −0.60 in |
| **Body** | Roboto Regular | **11 pt** | **1.38** | **6 pt** | `--ink` | ragged right |
| **Rule number** | Roboto Bold | 11 pt | 1.38 | 6 pt | `--ink` | hanging −0.50 in |
| **Rule headline** | Roboto Bold | 11 pt | inline | — | `--accent` | not italic |
| **Violation line** | Roboto Italic | 11 pt | 1.38 | 6 pt | **`--muted`** | indent 0.50 in, whole line italic |
| Lettered sub-clause | Roboto Regular | 11 pt | 1.38 | 6 pt | `--ink` | indent 1.00 in, hanging −0.25 in |
| Box body | Roboto Regular | 11 pt | 1.38 | 6 pt | `--ink` | inset 1.00 in both sides |
| Figure / table caption | Roboto Italic | **9 pt** | 1.30 | 8–10 pt (4–6 pt after) | `--ink` | **above** the object; label Bold Italic |
| Table body | Roboto Regular | **10 pt** | 1.30 | — | `--ink` | tabular figures on |
| Table header | Roboto Bold | 10 pt | 1.25 | — | `--paper` on `--accent` | |
| Footer | Roboto Bold | 10 pt | 1.20 | — | `--ink` | three tab cells |
| Header wordmark | Roboto Condensed Bold | 14 pt | 1.00 | — | `--paper` | caps, +0.5 pt tracking |
| Inline code | JetBrains Mono | 9.5 pt | 1.35 | — | `--ink` | `--paper-dim` ground; 8.5 pt in table cells |
| Code block | JetBrains Mono | 9 pt | 1.40 | 6 pt | `--ink` | `--paper-dim` ground, 1 pt border |
| Glossary term | Roboto Bold | 10 pt | 1.30 | — | `--ink` | ALL CAPS |

### 4.2 Paragraph spacing

Space before only: apart from captions and the 2 pt under H2, no style has space after. A paragraph carries 6 pt above and 0 below, so spacing never doubles at a paragraph boundary, and a rule, its sub-clauses and its violation line stack at an even 6 pt rhythm. Headings carry a larger space before (8–12 pt) and almost none after, and the first paragraph under a heading takes 3 pt instead of 6 pt, so a heading sits close to the text it introduces and apart from the text above it. Captions are the one exception: a table caption has 8 pt above and 4 pt below, a figure caption 10 pt above and 6 pt below.

### 4.3 Hierarchy below H2

H3 and H4 are both 11 pt, the same size as body text. They differ by weight, style and position on the indent ladder. This keeps a long rulebook from turning into a staircase of type sizes. Do not enlarge H3.

### 4.4 Miscellaneous

- Never justify. Hyphenation off. A word too long for a narrow table cell gets a soft hyphen (`&shy;`) in the source.
- Tabular figures on in every table, coordinate list, and the TOC page-number column.
- Em dashes unspaced; en dashes for ranges (`10–20 in`).
- Non-breaking space between a number and its unit (`24 in`), and after "Section", "Table", "Figure" and "Plate" before their numbers. The build inserts both.
- No small caps. Defined terms are hard-typed capitals.
- Dimensions imperial first, metric in parentheses. State once, in the front matter, that imperial governs. Round metric so that it stays rule-compliant: **maximums round down, minimums round up.**

---

## 5. Structural Conventions

### 5.1 Section inventory

The manual has nine top-level sections, each starting on a fresh page. Sections that contain rules append their rule letter to the title, so the footer identifies the rule series.

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

The PDF edition adds Appendix A, Field Drawing Plates, after Section 9 (§8).

### 5.2 Rule anatomy

A rule is one paragraph: a hanging rule number, then a headline sentence (italic in the Markdown source, set bold in `--accent` in the PDF; §4.1, §9.3), then the rule body. An indented `Violation:` line in `--muted` italic follows as a separate paragraph.

```
G412   The HEADWALL ZONE is protected during ENDGAME (line call).
       From the start of the ENDGAME period until climb assessment is
       complete (Section 4.5.3), a ROBOT may not …

       Violation: MAJOR FOUL per instance. …
```

- The **number** is Roboto Bold 11 pt `--ink`, hanging 0.50 in left of the rule text, at the left edge of the measure.
- The **headline** is a short imperative or descriptive sentence, bold, `--accent`, ending in a period, on the same line as the number.
- The **body** is regular weight, `--ink`, and starts on the same line as the headline.
- The **`Violation:` line** is a separate paragraph, indented 0.50 in, set entirely in `--muted` italic, and begins with the literal word "Violation:".
- Rules never nest. Sub-clauses are lettered `a.`, `b.`, `c.` at indent level 2.

### 5.3 Defined terms

Defined terms are hard-typed in capitals in the source (`ROBOT`, `SCORED`, `CRAG APRON`) and are not restyled at typesetting: no small caps, no color, no bold. Feature names that are not defined terms (Low Socket, Shelf 1, slot fence) stay in title case. The Glossary decides which is which.

### 5.4 Cross-references

- Rule references: bold, `--link`, no underline in print (`**G412**` in the source).
- Section references: `Section 4.5.3` in running text, `§4.5.3` inside tables and boxes. Both are hyperlinked in the PDF.
- Figure and table references: `Figure 3-4`, `Table 6-1`, giving the section number and then the sequence within the section.

### 5.5 Boxes

Two box types, both inset 1.00 in on each side (5.00 in measure), with a 1.5 pt `--box-border` border, `--box-fill` ground, 8 pt internal padding and 8 pt of space above:

- **Example:** a binding interpretation. The label is Roboto Bold Italic 10 pt `--accent`, followed by the text.
- **Commentary:** non-binding design rationale, set the same way. Only the label differs.

A **Caution** box (`--warn-fill` / `--warn-border`) is reserved for procedural warnings, and a **Warning** box (`--danger-fill` / `--danger-border`) for safety-critical text. Neither is used for rules. In the source, each is a block quote that opens with its italic label (`*Caution:*`, `*Warning:*`), like the Example and Commentary boxes, and the label takes the border color.

---

## 6. Tables

- Every table has a numbered caption above it, `Table <section>-<sequence>`, set like a figure caption (§4.1, §7.1). A table inside an Example or Commentary box belongs to the box and has no caption; it is set at 9.5 pt with 5 pt side padding to fit the box.
- Header row: `--accent` fill, `--paper` bold 10 pt type, no vertical rules.
- Body rows: 10 pt, 0.5 pt `--rule-line` horizontal rules only; zebra fill `--paper-dim` on even rows for tables over 8 rows.
- Outer border: 1 pt `--rule-line-strong`.
- Cell padding 4 pt vertical, 6 pt horizontal.
- **Alignment:** text left; integers and point values right; dimensions right on the decimal; units in the column header, not in every cell.
- **Scoring tables:** one row per scoring position or tier, AUTO and TELEOP as separate right-aligned columns, point values bold. Never merge the AUTO and TELEOP columns. The build treats a column headed AUTO, TELEOP or Points as a scoring column when at least half its cells are numbers.
- **Alliance-differentiated tables:** tint the cell with `--alliance-*-tint` and label it "Blue" or "Red". A tint alone is not sufficient.
- A table that does not fit the measure is restructured: transposed, split by tier, or moved to a landscape figure. Never rotate a page.

---

## 7. Figures and Drawing Sheets

### 7.1 Numbering and captions

Figures are numbered `Figure <section>-<sequence>` and captioned above the image in Roboto Italic 9 pt, with 10 pt above and 6 pt below; the `Figure N-M` label is Bold Italic. Every figure has a caption; an image that needs no caption is not set as a figure.

### 7.2 Field renders

- Drawn plan views (the drawing sheets) use the drawing set's light carpet (`#F4F2EE`), light alliance zone washes inside keylines (§3.1), and white neutral marks. The rendered figures in the body are views of the CAD model and show the field as built: tape lines on carpet, CRAGS in their physical tan.
- A drawn plan view may tint the CRAGS in alliance color for legibility; the physical CRAG is tan (`participants/03-field/MATERIALS-AND-COLORS.md` §3, rule 2). The sheet says so in a note; a figure says so in its caption.
- Every plan view carries a coordinate compass: origin marker, +X arrow, +Y arrow, and the words "always-blue-origin NWU".

### 7.3 Callouts

Leader lines and arrowheads use `--callout-leader` (`#E100E1`), 1.5 pt, with a 3 pt arrowhead. The color appears nowhere else in the field palette, so a callout cannot be mistaken for field hardware. Leaders do not cross each other or a dimension line. §9.2 gives the label treatment and the layout checks.

### 7.4 Drawing sheets

The six sheets in `participants/03-field/drawings/` are reproduced on dedicated landscape ANSI C (22 × 17 in) plates, one per sheet, at not less than 20.5 in of image width. ANSI C is the standard sheet size for a drawing set and the smallest that meets the 6-pt floor below. The build sets every sheet 21 in wide (`organizers/source/typesetting/pdf/plates.css`) and appends the plates after Appendix A, which lists them (§8).

The sheets cannot run at the 7.00-in body measure. `crag.svg` is 1960 user units wide, so at 504 pt its smallest text (about 9.7 units) prints at 2.5 pt and its largest at about 5.4 pt. The other five sheets fall in the same range, with smallest type of 2.5 to 3.0 pt at body width, and a 6-pt floor needs 13.9 in (`apriltag-map`) to 16.8 in (`crag`, `headwall`) of image width. That rules out an 11 × 17 plate: at 15 in, three of the six sheets would still fall below 6 pt, and a 16.8-in image leaves no margin on a 17-in tabloid sheet. At 21 in the smallest text on any sheet prints at 7.5 pt; `organizers/source/verify/svg_collide.py` holds every sheet to 7 pt at that width, and 8 pt for dimension values and bold labels.

A thumbnail may appear inline in the body, cross-referenced to the full-size plate. Each sheet carries its own title block, so a plate has no figure caption. It carries a label line above the sheet, `Plate N` (the form in which the manual's figure captions cite the plates) followed by the sheet name, and a three-cell footer like the one in §2.3.

Sheet conventions:

- Dimension lines and text in `#C02020`; extension lines 0.7 pt; arrowheads at both ends.
- Callout leaders in `--callout-leader` (§7.3), with the arrowhead on the feature, never at the label.
- Each sheet's primary view carries its scale in the sheet subtitle; every additional view carries its own name and px/in scale, and the title block repeats "Scale: as noted per view".
- Every sheet carries a title block: sheet name, sheet number of six, units note, scale note, tolerance note, revision, and the governing document reference.
- CRITICAL dimensions are boxed; reference dimensions are suffixed `(ref)`.

---

## 8. Front and Back Matter

| Page | Content |
|---|---|
| Cover | Title, subtitle, version, revision stamp and date. `--accent-deep` band, no logo. |
| Contents | Two levels deep, dot leaders, tabular page numbers. |
| Revision history | One row per Team Update: number, date, sections touched, one-line summary. |
| Version precedence | One paragraph stating that the manual plus all Team Updates is the current ruleset, and that the design specification governs any discrepancy. |
| Glossary | Section 9. Two-column table, terms in Roboto Bold 10 pt ALL CAPS, definitions 10 pt regular, alphabetical. |

The revision stamp and the revision-history rows come from `organizers/source/typesetting/pdf/revisions.json`; add a row for each Team Update. The build follows the version-precedence paragraph with three short statements: copyright and license, units, and independence from any competition organization. After Section 9 it sets Appendix A, Field Drawing Plates, which lists the six plates with their source files and page numbers (Table A-1); the plates themselves follow (§7.4). The PDF also carries a two-level bookmark outline.

There is no index. A 100-page manual with thorough cross-references and a hyperlinked table of contents does not need one, and a poor index is worse than none. The PDF edition runs to about 95 Letter pages plus the six drawing plates.

---

## 9. Production Recipe

### 9.1 Toolchain

The pipeline is Markdown → HTML → Paged.js → headless Chromium → PDF, implemented in `organizers/source/typesetting/pdf/` (see its `README.md`). The sources are Markdown with tables and blockquotes; every rule in this guide can be expressed in a CSS print stylesheet; Paged.js supplies running footers, page counters, cross-reference page numbers and break control; and every stage can be inspected in a browser.

```bash
bash organizers/source/typesetting/pdf/build.sh            # -> participants/01-game-manual/SUMMIT-PUSH-Game-Manual.pdf
bash organizers/source/typesetting/pdf/render_figures.sh   # -> participants/01-game-manual/figures/*.png (after a geometry change)
```

| Stage | File |
|---|---|
| Markdown to structured HTML (rule, violation, box, caption and cross-reference markup) | `make_html.py` |
| Print stylesheet: every token, size and rule in §2–§8 | `manual-print.css` |
| Header band (drawn on every page except the cover) | `furniture.js` |
| Pagination and printing in headless Chromium | `render.mjs` |
| Drawing plates, print boxes (bleed), bookmarks, metadata | `plates.css`, `postprocess.py` |
| Figure renders and callout placement | `render_figures.sh`, `figures.py`, `figure-shots.json` |

Every Letter page of the PDF carries 0.125 in of bleed. The MediaBox and BleedBox include it; the TrimBox and CropBox are set to the Letter page, so screen viewers and office printers show the trimmed page and a print shop still receives the bleed. The drawing plates have no bleed.

The alternatives considered were LaTeX (Pandoc with `xelatex`) and Typst (research notes §9.1). Maintain one route only.

### 9.2 Figure callouts

Rendered figures carry vector callouts drawn over the image: 8.5-pt Roboto Medium labels in white boxes with a 0.75-pt `--callout-leader` outline, and 1.5-pt `--callout-leader` leaders that end in a 3-pt arrowhead at the feature. `figures.py` places the callouts, keeping every label inside the image, and rejects a figure if an anchor falls outside the image, two labels overlap, a label covers another callout's anchor, a leader runs through a label, or two leaders cross. Plan views also get the §7.2 coordinate compass.

### 9.3 Source conventions

The Markdown sources follow these conventions, and the build depends on them:

- Rules are written `**G412** *Headline sentence.* Body text…` on one line, and the `Violation:` line is a separate paragraph written `*Violation:* …`.
- Examples and Commentary are blockquotes beginning `> *Example:*` / `> *Commentary:*` (Caution and Warning boxes likewise, §5.5). Any other blockquote is set as a plain gray note.
- Defined terms are hard-typed capitals in the source.
- Tables are GitHub-flavored pipe tables with a bare `|---|` separator row. The build applies §6's alignment rules by column type (numeric columns are right-aligned); the source carries no alignment. Every table has a bold caption line directly above it, `**Table 6-2: Legal Motors and Actuators**`, except a table inside a box.
- A Team Update marks added text `<ins>…</ins>` (highlighted in `--change-add`) and deleted text `~~…~~` (struck through in `--muted`).
- Figures are a caption paragraph `*Figure 3-2. The Blue CRAG, …*` directly above the image `![alt](../figures/crag.png)`.
- Section headings are written `# 5 Game Rules (G)`, with the number and title on the heading line, so `string-set: section-title` fills the footer without extra markup.

### 9.4 Acceptance checks before release

- [ ] Print one copy in grayscale; every color-coded distinction still reads.
- [ ] Every rule number and cross-reference resolves (the build fails on an unresolved link).
- [ ] No page breaks between a rule and its `Violation:` line.
- [ ] Every figure has a caption above it and a `Figure N-M` label.
- [ ] The footer section name changes at each section boundary and nowhere else.
- [ ] All fonts embedded; no system-font substitution warnings.
- [ ] Every drawing sheet is reproduced on its own landscape ANSI C plate at not less than 20.5 in of image width, so no type on any sheet sets below 6 pt.

---

## 10. What This Package Does Not Do

- It does not use any real organization's name, logo, wordmark, color palette, or boilerplate.
- It does not claim affiliation with or endorsement by any robotics competition organization.
- It does not reproduce any existing manual's text.
- Its typeface choices are open-licensed and are not brand assets.

Revisit this section first if any of this changes.
