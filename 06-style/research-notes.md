# SUMMIT PUSH Manual Typesetting: Research Notes

> Draft version 1.0. These notes are the full research draft behind `06-style/MANUAL-STYLE-GUIDE.md`, including the reference values that were examined and not adopted. The style guide is the binding version. Where the two differ (for example in the section inventory, the rule and box conventions, and the toolchain), the style guide governs.

---

## 1. Scope and Intent

### 1.1 What this document is

This draft specifies the typography and structure of the SUMMIT PUSH Game Manual, a fictional robotics-competition rulebook. It covers how to write the Markdown sources and how to typeset them into a print-ready US Letter PDF.

The target look is the genre convention of a modern competitive-robotics game manual: a single-column, print-first rulebook descended from word-processor documents, with hanging-indent rule numbering, color-coded rule headlines, tinted commentary boxes, demoted violation lines, and a running footer that carries section identity and revision state. We match the *structure* of that genre.

### 1.2 What this document is not

We are not producing a counterfeit, a parody trading on someone else's marks, or a document that could be mistaken for an official publication of *FIRST*®, its FIRST Robotics Competition program, or any real organization. Section 10 states the exclusions in full and is normative.

The distinction we hold throughout:

| We copy | We do not copy |
|---|---|
| Layout geometry (page size, margins, measure, indent ladder) | Logos, wordmarks, lockups, banner artwork |
| Structural conventions (rule numbering scheme, hanging indents, footer anatomy) | Organization names, program names, sponsor names |
| Typographic *relationships* (11 pt body, 13 pt colored H2, 9 pt italic captions) | Brand-mandated exact hex values as our own palette |
| Semantic color-coding *as an idea* (stable rules one color, seasonal another) | The specific corporate palette that identifies a real entity |
| The reading contract (literalism, defined terms in caps, glossary) | Boilerplate legal text lifted verbatim |

Facts about layout (that US Letter is 8.5 × 11 in, or that a 0.5 in hanging indent reads well for numbered rules) are not anyone's intellectual property. Identity is. We take the former and invent the latter.

### 1.3 Design goals, in priority order

1. **Unambiguous rule addressing.** A reader must be able to say "G214" out loud and find it in seconds.
2. **Visual demotion of non-normative text.** Commentary and consequences must never be mistaken for rule text.
3. **Print fidelity first.** The PDF is the commanding version. Screen rendering is a courtesy.
4. **Reproducibility.** Every value in this guide is a token. No magic numbers in source files.
5. **Legal cleanliness.** Nothing in the output package requires anyone's permission to distribute.

### 1.4 Reading contract we adopt (paraphrased, not quoted)

The manual should state, in its own words, that the text means what it says and nothing more; that there are no hidden requirements; that commentary boxes explain but do not command; and that where a commentary box conflicts with a rule, the rule wins. Write this in original prose. Do not lift phrasing from any existing manual.

---

## 2. Page Setup

### 2.1 Trim, orientation, and bleed

| Property | Value | Notes |
|---|---|---|
| Page size | US Letter, 8.5 × 11 in (612 × 792 pt) | Every page, including the cover. |
| Orientation | Portrait throughout | No landscape pages, no page rotation. If a table cannot fit portrait, restructure it (see §6.6). |
| Bleed | 0.125 in (9 pt) on all four edges, cover and section-opener pages only | Body pages need no bleed. |
| Color space | sRGB for screen PDF; convert to CMYK only if physically printing. | Ship sRGB. |
| Optional metric edition | A4 (210 × 297 mm) variant is permitted as a secondary build. Keep the same measure in inches; A4's extra height absorbs into the bottom margin. | Letter is canonical. |

### 2.2 Margins and the live text column

The reference manual runs an unusually wide measure: a 7.5 in text column on an 8.5 in page. That is a Word artifact, and at 11 pt it produces roughly 105–115 characters per line, which is past the comfortable reading limit. We deviate from it.

| Margin | Body pages | Front matter | Rationale |
|---|---|---|---|
| Top | 1.30 in | 1.30 in | Clears the header band. |
| Bottom | 0.85 in | 0.85 in | Footer baseline sits at 0.50 in. |
| Left | 0.75 in | 0.90 in | |
| Right | 0.75 in | 0.90 in | |
| **Live measure** | 7.00 in (504 pt) | 6.70 in | ~95–100 chars at 11 pt. |

> **Deviation noted.** The genre standard is a 0.50 in side margin / 7.50 in measure. We use 0.75 in / 7.00 in. This improves legibility, moves the design visibly away from a clone, and costs roughly 4% more pages. If you must match the source geometry for a comparison build, set `--measure-wide` in the build script; do not make it the default.

### 2.3 Columns

**Single column, full measure, left-aligned, ragged right.** No justification: justified 11 pt Roboto-class type at this measure opens rivers. No multi-column body text anywhere in the document.

Hierarchy below the heading level is expressed entirely by the indent ladder, never by columns:

| Level | Left indent | Hanging indent | Used for |
|---|---|---|---|
| 0 | 0.00 in | — | Body paragraphs, H1 title text |
| 1 | 0.50 in | −0.50 in | Rule numbers (number hangs into margin) |
| 1c | 0.50 in | 0 | Rule continuation paragraphs, Violation lines |
| 2 | 1.00 in | −0.25 in | Lettered sub-clauses (A., B., C.) |
| 3 | 1.25 in | −0.25 in | Bullets inside sub-clauses |
| Box | 1.00 in both sides | — | Commentary boxes (measure 5.00 in) |

The commentary box is inset deeper on *both* sides than any text indent. That double inset makes the box read as an aside without a heavy border.

### 2.4 Header

The header is a 1.19 in (86 pt) full-bleed band across the top of every page except the cover.

Compose it as a vector or flat-color band that we author ourselves, never a borrowed banner image:

- Ground: solid `--summit-ink` (see §3).
- Left: the SUMMIT PUSH wordmark, set as *type* in Roboto Condensed Bold, 14 pt, `--paper`, letterspaced 0.5 pt, ALL CAPS. Not a logo file. If a logo is later commissioned, it drops in here.
- A 1 pt vertical rule in `--accent` at x = 2.60 in, running from y = 0.28 in to y = 0.91 in.
- Right, right-aligned: `SUMMIT PUSH — Game Manual` in 9 pt Roboto Regular, `--paper-dim`; below it, the project URL in 8 pt italic if one exists.
- A 2.2 pt horizontal rule in `--accent-bright` flush against the band's bottom edge, full bleed. (The reference documents use a 543 × 2.2 pt divider; we make ours full-bleed and part of the band.)

**No running header text.** All wayfinding lives in the footer. This is borrowed from the genre on purpose: it keeps the header a constant graphic and lets the footer do the variable work.

### 2.5 Footer

Three variants. The baseline sits 0.50 in from trim, set in Roboto Bold 10 pt in `--ink`, spanning the full measure with three tab-stop cells (left / center / right).

**Body-page footer:**

```
Section 7 Game Rules (G)          Revision: TU-14          63 of 148
```

- **Left cell:** the literal string `Section N Title`, as the H1 reads, including any parenthetical rule letter. It changes at each section boundary and is the reader's primary wayfinding device.
- **Center cell:** revision stamp, format `Revision: TU-NN` (see §8.4).
- **Right cell:** `N of TOTAL`. Bare number, no "Page" prefix.

**Front-matter footer:** page number only, right-aligned, no section name, no revision stamp.

**Cover footer:** revision stamp only, centered.

**Adopt the per-section revision stamp.** The reference corpus shows two behaviors across years: a single document-wide stamp, and a per-section stamp in which each section shows its own revision level. The per-section behavior is more useful to a reader, and the research flags it as the better design. We use per-section stamps: `Revision: S7-v4`. A reader scanning the footer can see at once whether the current section has changed.

### 2.6 Page numbering

- **Continuous across the whole document.** No per-section restart. No section-prefixed numbers (never `7-3`).
- Format: `N of TOTAL`.
- **The cover counts as page 1.** Contents is 2–3. Section 1 opens on printed page 4.
- No roman numerals for front matter. One arabic sequence throughout.
- Every top-level section starts on a fresh page, with the heading baseline at 1.47 in from trim (105.7 pt). Blank versos are acceptable; do not force even-page starts.

### 2.7 Widow/orphan and break control

| Rule | Setting |
|---|---|
| Widows / orphans | 2 lines minimum, both ends |
| Headings | `break-after: avoid` on all levels |
| Rule blocks | Keep rule number + headline + first line together (`break-inside: avoid` on the first 3 lines) |
| Violation line | Never separated from its rule. Keep-with-previous. |
| Commentary boxes | `break-inside: avoid` if under 15 lines; otherwise allow break but repeat nothing |
| Captions | Keep-with-next (captions sit *above* their figure; §7.2) |
| Table header rows | Repeat on continuation pages |

---

## 3. Color Palette

### 3.1 Method and the legal line

The reference documents use a specific corporate palette (black `#231F20`, red `#ED1C24`, blue `#0066B3`, gray `#9A989A`, program blue `#009CD7`) plus per-season accents (`#0083AE` teal, `#00B050` green, `#ABD8E7` box tint). Those values are recorded below as research context only. They function as identifiers of a real organization, and we do not adopt them.

**The SUMMIT PUSH palette below is our own.** It is built to be *structurally analogous* (one deep accent that survives at 11 pt bold on white, one saturated stable-rule color, one light tint of the accent for boxes) while being visibly a different family. Where the reference sits in cyan-teal, ours sits in deep slate-indigo with a copper secondary. The two palettes do the same job and are not easily confused.

### 3.2 Reference values (documented, not used)

| Reference role | Reference hex | Our position |
|---|---|---|
| Corporate black | `#231F20` | Not used. We use `#1A1D21`. |
| Corporate red | `#ED1C24` | Not used. |
| Corporate blue | `#0066B3` | Not used. |
| Corporate gray | `#9A989A` | Not used. We use `#6E7378`. |
| Program blue | `#009CD7` | Not used. |
| Season accent teal | `#0083AE` / `#0080A9` | Replaced by `--accent` `#1F4E79`. |
| Evergreen green | `#00B050` | Replaced by `--stable` `#1E7A4C`. |
| Box tint | `#ABD8E7` | Replaced by `--box-fill` `#DCE6F1`. |
| Word hyperlink blue | `#0563C1` | Replaced by `--link` `#245C9E`. |

> Two of the reference teals (`#0083AE` and `#0080A9`) differ by 3/255 and are a conversion artifact between two source applications, not a design decision. We do not reproduce that inconsistency; one accent value is used everywhere.

### 3.3 The SUMMIT PUSH palette (normative)

| Token | Hex | RGB | Role | Contrast on `--paper` |
|---|---|---|---|---|
| `--ink` | `#1A1D21` | 26, 29, 33 | Body text, H1, H3, rule numbers | 16.9:1 ✅ |
| `--paper` | `#FFFFFF` | 255, 255, 255 | Page ground | — |
| `--paper-dim` | `#F4F5F7` | 244, 245, 247 | Zebra row fill, subtle panels | — |
| `--accent` | `#1F4E79` | 31, 78, 121 | Primary heading color (H2), table header fill, box border, glossary rules | 8.7:1 ✅ |
| `--accent-bright` | `#2E6FA8` | 46, 111, 168 | Header band divider rule and decorative rules only; never body text | 5.3:1 ⚠️ large text only |
| `--accent-deep` | `#16385A` | 22, 56, 90 | Section-opener wash, cover band | 12.0:1 ✅ |
| `--stable` | `#1E7A4C` | 30, 122, 76 | Persistent-rule headlines (bold, asterisk-prefixed) | 5.3:1 ✅ at bold 11 pt |
| `--seasonal` | `#1F4E79` | 31, 78, 121 | Season-specific rule headlines (bold); the same as `--accent` by design | 8.7:1 ✅ |
| `--muted` | `#6E7378` | 110, 115, 120 | Violation lines (italic), captions' secondary text, TOC leaders | 4.8:1 ✅ |
| `--rule-line` | `#C8CCD1` | 200, 204, 209 | Table body rules, thin dividers, hairlines | — |
| `--rule-line-strong` | `#8A9199` | 138, 145, 153 | Table outer border, section dividers | — |
| `--box-fill` | `#DCE6F1` | 220, 230, 241 | Commentary box tint (tint of `--accent`) | ink on it: 13.4:1 ✅ |
| `--box-border` | `#1F4E79` | 31, 78, 121 | Commentary box 1.5 pt border (= `--accent`) | — |
| `--warn-fill` | `#FBEBD2` | 251, 235, 210 | Caution box tint | ink on it: 14.4:1 ✅ |
| `--warn-border` | `#B26A12` | 178, 106, 18 | Caution box border, caution icon | 4.2:1 ⚠️ large text only |
| `--danger-fill` | `#F7DEDE` | 247, 222, 222 | Warning box tint (safety-critical only) | ink on it: 13.3:1 ✅ |
| `--danger-border` | `#A32A2A` | 163, 42, 42 | Warning box border | 7.2:1 ✅ |
| `--change-add` | `#FFF3A8` | 255, 243, 168 | Revision-note addition highlight | — |
| `--change-del` | `#6E7378` | 110, 115, 120 | Revision-note deletion (strikethrough, muted) | — |
| `--link` | `#245C9E` | 36, 92, 158 | Cross-references and URLs, underlined | 6.8:1 ✅ |
| `--table-head-fill` | `#1F4E79` | 31, 78, 121 | Table header band (= `--accent`) | white on it: 8.7:1 ✅ |
| `--table-head-text` | `#FFFFFF` | 255, 255, 255 | Reversed table header type | — |
| `--table-group-fill` | `#E4E9EF` | 228, 233, 239 | Sub-header / row-group band | — |

### 3.4 Alliance colors

The reference documents publish no official hex for alliance red or blue. Field renders use saturated sRGB primaries (`#FF0000` / `#0000FF`); tables use pastel tints (`#FFCCCC` / `#CCECFF`). Since no standard exists to copy, we define our own, chosen to be distinguishable in grayscale print and to survive red-green color deficiency (red vs. blue is the safest pair available).

| Token | Hex | Role |
|---|---|---|
| `--alliance-red` | `#C62828` | Red alliance: figure fills, keylines, callout boxes |
| `--alliance-red-lit` | `#E53935` | Lit/top faces in isometric renders |
| `--alliance-red-shade` | `#8E1F1F` | Shaded faces in isometric renders |
| `--alliance-red-tint` | `#F6DADA` | Table cell tint, column-group shading |
| `--alliance-red-wash` | `rgba(198,40,40,0.38)` | Zone overlay wash over carpet |
| `--alliance-blue` | `#1B54A8` | Blue alliance: figure fills, keylines, callout boxes |
| `--alliance-blue-lit` | `#2C6BC9` | Lit/top faces |
| `--alliance-blue-shade` | `#123A75` | Shaded faces |
| `--alliance-blue-tint` | `#D9E4F5` | Table cell tint |
| `--alliance-blue-wash` | `rgba(27,84,168,0.38)` | Zone overlay wash |
| `--neutral-zone-wash` | `rgba(214,178,42,0.35)` | Neutral zone overlay |
| `--carpet` | `#666A6E` | Field carpet in top-down renders |
| `--carpet-lit` | `#74787C` | Carpet in isometric renders |
| `--figure-ground` | `#101214` | Background outside the field in renders |
| `--callout-leader` | `#E100E1` | Leader lines and arrowheads in figures |

**On zone washes:** do not pick a flat muted color. Composite the alliance hue at 38% opacity over `--carpet` and let the compositor produce the value. The result is a wash that stays visibly related to the saturated alliance color used elsewhere. Give every washed region a 1.5 pt keyline in the fully saturated hue so the boundary stays crisp at print resolution.

**On the magenta leader color:** `#E100E1` appears nowhere else in the field palette: not in carpet gray, alliance red, alliance blue or game-piece gold. That is its purpose, so that a callout can never be mistaken for field hardware. Keep it reserved; never use it for anything but leaders, arrowheads and geometry-highlight strokes.

### 3.5 Color usage rules

1. **Only H2 is colored.** H1 is `--ink`. H3–H6 are `--ink`. Color enters at level 2 and nowhere else in the heading stack.
2. **Rule numbers are never colored.** Bold `--ink`, always, including for persistent rules. The color lives on the *headline* that follows. (The reference manuals' own prose gets this wrong and claims the number is colored; their actual typesetting does not. We follow the typesetting.)
3. **Three semantic colors, three meanings, no overlap:** `--stable` = rule persists across seasons; `--seasonal` = rule is specific to this game; `--muted` = this text is a consequence or a caption, subordinate to the rule.
4. **Never encode meaning in color alone.** Persistent rules carry a literal leading asterisk in addition to the green. Violation lines carry the literal word "Violation:" in addition to the gray italic. Print the manual in grayscale as an acceptance test; every distinction must survive.
5. **Minimum contrast: 4.5:1** for all body-size text, 3:1 for ≥14 pt bold. `--accent-bright` is reserved for decorative rules and banned from body text.

---

## 4. Typography

### 4.1 Typeface selection

All faces below are free, open-licensed (SIL OFL 1.1) and redistributable. Vendor them into `assets/fonts/` and embed them in the PDF. Never rely on a system font being present.

| Role | Family | License | Weights needed |
|---|---|---|---|
| **Body, headings, tables (primary)** | Roboto | OFL 1.1 | Regular 400, Italic 400, Medium 500, Bold 700, Bold Italic 700 |
| **Condensed (header band, tight table cells, drawing sheets)** | Roboto Condensed | OFL 1.1 | Regular 400, Bold 700 |
| **Monospace (code, coordinates, part numbers)** | JetBrains Mono | OFL 1.1 | Regular 400, Bold 700 |
| **Numeric tabular fallback** | Roboto has tabular figures via `font-feature-settings: "tnum"` | — | — |

Roboto is used because it is the correct genre signal, is licensed under the SIL OFL 1.1, and is free for any use, including commercial use; using it raises no trademark issue. A typeface choice is not a brand asset.

**Full CSS stacks:**

```css
--font-sans:  "Roboto", "Arimo", "Liberation Sans", "Helvetica Neue", Arial, sans-serif;
--font-cond:  "Roboto Condensed", "Liberation Sans Narrow", "Arial Narrow", sans-serif;
--font-mono:  "JetBrains Mono", "DejaVu Sans Mono", "Liberation Mono", Consolas, monospace;
```

*Arimo* and *Liberation Sans* are metric-compatible with Arial and freely licensed; they are the correct open fallbacks and will not shift line breaks meaningfully.

### 4.2 Type scale (normative)

All sizes in points. Line heights given as unitless multipliers *and* absolute leading.

| Style | Family / weight | Size | Line height | Space before | Space after | Color | Other |
|---|---|---|---|---|---|---|---|
| **Cover title** | Roboto Bold | 40 pt | 1.05 / 42 pt | — | 12 pt | `--ink` | centered |
| **Cover superline** | Roboto Regular | 18 pt | 1.20 / 21.6 pt | — | 6 pt | `--ink` | centered |
| **Cover subtitle** | Roboto Regular | 14 pt | 1.25 / 17.5 pt | — | 8 pt | `--muted` | centered, +0.5 pt tracking |
| **Section opener number** | Roboto Bold | 40 pt | 1.00 | — | — | `--accent-deep` | in the opener wash |
| **H1** (section title) | Roboto Bold | 16 pt | 1.20 / 19.2 pt | 12 pt | 12 pt | `--ink` | +1 pt letterspacing, hanging indent −0.50 in |
| **H2** (subsection) | Roboto Bold | 13 pt | 1.25 / 16.25 pt | 12 pt | 2 pt | `--accent` | hanging indent −0.40 in |
| **H3** | Roboto Bold | 11 pt | 1.35 / 14.85 pt | 10 pt | 0 | `--ink` | hanging indent −0.50 in |
| **H4** | Roboto Italic 400 | 11 pt | 1.35 | 8 pt | 0 | `--ink` | hanging indent −0.60 in |
| **H5** | Roboto Regular | 11 pt | 1.35 | 6 pt | 0 | `--ink` | indent 0.70 in |
| **H6** | Roboto Regular | 11 pt | 1.35 | 4 pt | 0 | `--muted` | indent 0.80 in |
| **Body** | Roboto Regular | 11 pt | 1.38 / 15.2 pt | 6 pt | 0 | `--ink` | ragged right |
| **Rule number** | Roboto Bold | 11 pt | 1.38 | 6 pt | 0 | `--ink` | hanging −0.50 in |
| **Rule headline** | Roboto Bold | 11 pt | 1.38 | inline | — | `--stable` / `--seasonal` | not italic |
| **Rule body** | Roboto Regular | 11 pt | 1.38 | inline | — | `--ink` | |
| **Violation line** | Roboto Italic | 11 pt | 1.38 | 6 pt | 0 | `--muted` | indent 0.50 in, entire line italic |
| **Lettered sub-clause** | Roboto Regular | 11 pt | 1.38 | 6 pt | 0 | `--ink` | indent 1.00 in, hanging −0.25 in |
| **Commentary box body** | Roboto Regular | 11 pt | 1.38 | 6 pt | 0 | `--ink` | inset 1.00 in both sides |
| **Box caption** | Roboto Italic | 9 pt | 1.30 | 4 pt | 0 | `--ink` | centered |
| **Figure / table caption** | Roboto Italic | 9 pt | 1.30 / 11.7 pt | 6 pt | 10 pt | `--ink` | placed ABOVE the object |
| **Table body** | Roboto Regular | 10 pt | 1.30 / 13 pt | — | — | `--ink` | tabular figures on |
| **Table header** | Roboto Bold | 10 pt | 1.25 | — | — | `--table-head-text` | on `--accent` fill |
| **Table footnote** | Roboto Regular | 8.5 pt | 1.28 | 4 pt | 0 | `--muted` | |
| **TOC level 1** | Roboto Bold | 11 pt | 1.60 | 6 pt | 0 | `--ink` | |
| **TOC level 2** | Roboto Regular | 10 pt | 1.50 | 0 | 0 | `--ink` | indent 0.15 in |
| **Footer** | Roboto Bold | 10 pt | 1.20 | — | — | `--ink` | 3 tab cells |
| **Header band, wordmark** | Roboto Condensed Bold | 14 pt | 1.00 | — | — | `--paper` | +0.5 pt tracking, caps |
| **Inline code** | JetBrains Mono | 9.5 pt | 1.35 | — | — | `--ink` | `--paper-dim` ground, 2 pt pad |
| **Code block** | JetBrains Mono | 9 pt | 1.40 / 12.6 pt | 6 pt | 6 pt | `--ink` | `--paper-dim` ground, 1 pt `--rule-line` border, 6 pt pad |
| **Glossary term** | Roboto Bold | 10 pt | 1.30 | — | — | `--ink` | ALL CAPS |
| **Glossary definition** | Roboto Regular | 10 pt | 1.30 | — | — | `--ink` | |

### 4.3 The paragraph spacing model

Space-before only: zero space-after on every style except captions.

This is the most important typographic decision in the document, and it is inherited directly from the genre. Every paragraph carries 6 pt above and 0 below. Consequences:

- Spacing never doubles at a paragraph boundary.
- A rule, its sub-clauses, and its violation line stack at a consistent 6 pt rhythm with no accumulation.
- Headings carry their own larger space-before (10–12 pt) and near-zero space-after, so a heading sits *tight* to the text it introduces and *loose* from the text above it. That asymmetry is what makes the hierarchy legible without extra rules or size jumps.

The one exception: figure and table captions carry 6 pt above and 10 pt below, because the caption sits above its object and needs to separate from it.

### 4.4 Hierarchy below H2

H3, H4, H5 and H6 are all 11 pt, the same size as body text. They differ only by weight (H3 bold), style (H4 italic), color (H6 muted) and their position on the indent ladder. This is intentional: it keeps a 150-page rulebook from turning into a staircase of size jumps. Do not "fix" it by scaling H3 up.

### 4.5 Miscellaneous typographic rules

- **Never justify.** Ragged right throughout.
- **Hyphenation off** in body text and rule text. On in table cells narrower than 1.2 in.
- **Tabular figures on** (`font-feature-settings: "tnum" 1`) in all tables, coordinate lists, and the TOC page-number column.
- **Ligatures:** standard on, discretionary off.
- **Em dashes** unspaced (`word—word`). En dashes for ranges (`10–20 in`).
- **Non-breaking space** between a number and its unit (`24&nbsp;in`). A non-breaking space between a rule letter and its digits is unnecessary, because rule IDs are single tokens (`G214`).
- **Small caps: never.** Defined terms are hard-typed capitals (§5.5).
- **Dimensions:** imperial first, metric in parentheses, as in `36 in (91 cm)`. State once in §1 that imperial governs and metric is a convenience. Round metric so that it stays rule-compliant: maximums round down, minimums round up.

---

## 5. Structural Conventions

### 5.1 Section numbering and inventory

Fifteen top-level sections. Each starts on a fresh page. Sections that carry rules append their rule letter, in parentheses, to the section title itself, which makes the footer self-documenting.

| # | Title | Rule letter |
|---|---|---|
| 1 | Introduction | — |
| 2 | Season Overview | — |
| 3 | Sponsor Recognition | — |
| 4 | Game Overview | — |
| 5 | Arena | — |
| 6 | Game Details | — |
| 7 | Game Rules (G) | G |
| 8 | Robot Construction Rules (R) | R |
| 9 | Inspection & Eligibility (I) | I |
| 10 | Tournaments (T) | T |
| 11 | District Events | — |
| 12 | Regional Events | — |
| 13 | Championship (C) | C |
| 14 | Event Rules (E) | E |
| 15 | Glossary | — |

Heading numbering goes to three levels in the body (`5.9.2`), but the TOC shows only two (§8.2).

### 5.2 Rule numbering bands

**Format: `LETTER` + `SUBSECTION DIGIT` + `TWO POSITION DIGITS`.**

```
G214
│└┴┴─ position 14 within subsection 2
└──── Section 7, Game Rules
```

| Letter | Section | Band |
|---|---|---|
| `Q` | 6.7.1 Question Box | Q101– |
| `G` | 7 Game Rules | G101–G4xx |
| `R` | 8 Robot Construction Rules | R101–R5xx |
| `I` | 9 Inspection & Eligibility | I101– |
| `T` | 10 Tournaments | T101– |
| `C` | 13 Championship | C101– |
| `E` | 14 Event Rules | E101– |

**Allocation policy:**

1. Position digits start at `01` in each subsection and increment by 1. Never renumber.
2. Persistent rules occupy the low positions. Every subsection places its persistent (cross-season) rules first, so `G201`–`G206` stay stable year over year and only the higher numbers change.
3. Leave a gap of at least 3 positions between the last persistent rule and the first season-specific rule in each subsection.
4. A withdrawn rule's number is retired and never reused. Replace its body with a single line, `G217 Withdrawn.`, in `--muted` italic.
5. Include a figure in §1 diagramming the numbering scheme itself. A document that explains its own addressing system in a picture is a genre hallmark worth keeping.

### 5.3 Rule anatomy

A rule is one paragraph containing three runs, optionally followed by sub-clauses, a violation line and a commentary box.

```
[Rule number]  [Headline sentence]  [Rule body text]
```

| Run | Typeset as | Notes |
|---|---|---|
| **Rule number** | Roboto Bold 11 pt `--ink` | Hangs in the left margin at 0.00 in; rule text block aligns at 0.50 in. Never colored. |
| **Headline** | Roboto Bold 11 pt, `--stable` or `--seasonal` | A short colloquial sentence. Bold and colored, not italic. Ends with a period. Persistent rules prefix a literal `*`. |
| **Body** | Roboto Regular 11 pt `--ink` | The normative text. Begins with a single space after the headline's period, in the same paragraph. |

> **Correction to a common misreading.** The headline is bold and colored, not italic, and the rule *body* is not bold; only the number and the headline are. The only italic in a rule block is the Violation line. If you have seen a spec calling for italic headlines, it is wrong; do not follow it.

**Rendered example:**

> **G214** **No de-scoring.** A ROBOT may not remove a CARGO unit from an opponent's SUMMIT RACK, either directly or by causing the RACK to release it.
>
> *Violation: MAJOR FOUL per displaced CARGO, and the opposing ALLIANCE is awarded the SUMMIT RP.*

**Markdown source form:**

```markdown
::: rule {#G214 .seasonal}
**G214** [No de-scoring.]{.headline} A ROBOT may not remove a CARGO unit from an
opponent's SUMMIT RACK, either directly or by causing the RACK to release it.

::: violation
MAJOR FOUL per displaced CARGO, and the opposing ALLIANCE is awarded the SUMMIT RP.
:::
:::
```

The build filter emits the literal word `Violation:`; authors never type it.

**Persistent rule, rendered:**

> **G101** **\*Humans stay off the field until the light is green.** No team member may enter the FIELD until the ARENA status light is green.

The asterisk is inside the colored headline run. It is not a footnote marker, and there is no corresponding footnote anywhere.

### 5.4 Sub-clauses, continuations, and violation lines

| Element | Indent | Style |
|---|---|---|
| Rule continuation paragraph | 0.50 in, no hang | Body 11 pt, 6 pt above |
| Lettered sub-clause | 1.00 in, hang −0.25 in | `A.` `B.` `C.`: uppercase letter, period, tab |
| Bulleted sub-item | 1.25 in, hang −0.25 in | En-dash bullet `–`, not `•` |
| **Violation line** | 0.50 in | Roboto Italic 11 pt `--muted`, whole line including the word "Violation:" |

**Violation lines are prose.** They are never tables or bullets. Escalating consequences are written as a single running sentence, relying on ALL-CAPS defined terms to carry the structure. Never build a consequence table.

Acceptable patterns:

- `Violation: MINOR FOUL.`
- `Violation: VERBAL WARNING. YELLOW CARD if the violation repeats during the event.`
- `Violation: MAJOR FOUL, or MAJOR FOUL and YELLOW CARD if the contact is CONTINUOUS.`
- `Violation: MAJOR FOUL and YELLOW CARD, or if the opposing ROBOT is rendered unable to drive, MAJOR FOUL and RED CARD.`

The word `Violation:` is not bolded and is not a separate run; the entire paragraph is uniformly gray italic. This visual demotion of the consequence below the rule is the most distinctive typographic move in the genre. Keep it.

### 5.5 Defined terms

Defined terms are hard-typed in ALL CAPS, with no color, weight change, letterspacing, small caps or `text-transform`.

Type `ROBOT`, not `Robot` wrapped in a caps class. The caps inherit the surrounding run's font, size, weight and color, so a defined term inside a bold headline is bold, one inside a gray violation line is gray, and one inside a figure callout takes the callout's style.

Rules:

1. Every ALL-CAPS term must have a §15 Glossary entry. Every glossary entry must appear in ALL CAPS somewhere in the body. Enforce this with a build-time lint (§9.6).
2. Ordinary emphasis uses *italic*, never caps.
3. Acronyms that are not defined terms (`CAD`, `PDF`, `LED`) are in caps but are exempt from the glossary requirement; maintain an allowlist in `build/acronyms.txt`.
4. Figure callout labels use the same ALL-CAPS string as the glossary term, so a label and a body mention are visually and textually identical.
5. Do not pluralize a defined term by changing its case. `ROBOTS` is fine; `ROBOTs` is not.

### 5.6 Cross-references

Cross-references use `--link` `#245C9E`, underlined, in all three cases: internal section links, rule references and external URLs. The treatment is uniform.

| Target | Written as | Renders as |
|---|---|---|
| Section | `section [6.7](#s-6-7)` | section <u>6.7</u> |
| Rule | `(see [R405](#R405))` | (see <u>R405</u>) |
| Figure | `[Figure 5-4](#fig-5-4)` | <u>Figure 5-4</u> |
| Table | `[Table 6-3](#tbl-6-3)` | <u>Table 6-3</u> |
| Glossary | `[CARGO](#g-cargo)` | <u>CARGO</u>; link only the first occurrence per section |
| External | `[full URL as link text](https://…)` | Print builds append nothing; the text *is* the URL |

State in §1 that cross-references and links appear in blue underlined text.

**Anchor ID scheme (stable, machine-generated):**

```
#G214        rule
#s-6-7       section 6.7
#fig-5-4     figure
#tbl-6-3     table
#g-cargo     glossary term (lowercased, spaces → hyphens)
```

Anchors are contractual. Once published, an anchor never changes, because other documents deep-link to it.

### 5.7 Commentary boxes

Our name for them, used in lowercase running prose, is **note boxes**. (The genre calls its equivalent "blue boxes". We do not use that name, because it is tied to one document's color. Ours are a different color and get a different name.)

**Default (note) box:**

| Property | Value |
|---|---|
| Fill | `--box-fill` `#DCE6F1` |
| Border | 1.5 pt solid `--box-border` `#1F4E79` |
| Padding | 4 pt left/right, 3 pt top/bottom |
| Left inset | 1.00 in |
| Right inset | 1.00 in |
| Body | Roboto Regular 11 pt `--ink`, 6 pt space-before |
| Lettered list inside | left 2.00 in, right 1.00 in, hang −0.25 in |
| Bulleted list inside | left 1.25 in, right 1.00 in, hang −0.25 in |
| Box caption | Roboto Italic 9 pt, centered, on the box fill |
| Icon | None. No icon, no label chip, no "NOTE:" prefix. |

**Design rule to preserve:** the box border color always equals the season-specific headline color, and the fill is a light tint of it. One accent drives both the headline and the callout chrome, so changing the accent re-themes the whole system coherently.

**Severity variants (an intentional deviation).** The genre uses one box for warnings, cautions and notes and does not color-code severity. We add two more, because SUMMIT PUSH includes physical-safety content where undifferentiated commentary is a real hazard:

| Variant | Fill | Border | When |
|---|---|---|---|
| `.note` (default) | `--box-fill` | `--box-border` 1.5 pt | Rationale, best practice, interpretation. ~90% of boxes. |
| `.caution` | `--warn-fill` | `--warn-border` 1.5 pt | Common failure mode, inspection gotcha, likely-to-be-violated. |
| `.warning` | `--danger-fill` | `--danger-border` 2 pt | Physical safety only. Injury or equipment damage. Use ≤ 6 times in the whole manual. |

`.caution` and `.warning` carry a bold ALL-CAPS label as the first run of the first paragraph (`CAUTION.` / `WARNING.`) in the border color, so severity survives grayscale printing. `.note` carries no label.

**Every variant is non-normative.** State once in §1, in original prose, that note boxes explain but do not command; that they are part of the manual but do not carry the weight of a rule; and that where a box and a rule conflict, the rule governs.

**Markdown source form:**

```markdown
::: note
The ARENA is assembled and disassembled many times across a season. Small
variations occur between venues. Design ROBOTS that tolerate them.
:::

::: caution
**CAUTION.** BUMPER fasteners are the most common inspection failure. Verify
torque after every transport.
:::
```

---

## 6. Tables

### 6.1 Standard table style

| Property | Value |
|---|---|
| Width | Full measure (7.00 in) unless the content is narrow; then size to content and left-align the table, never center it |
| Header row | `--table-head-fill` `#1F4E79`, text Roboto Bold 10 pt `#FFFFFF`, vertically centered |
| Header padding | 6 pt top/bottom, 7 pt left/right |
| Body cell padding | 4 pt top/bottom, 7 pt left/right |
| Body text | Roboto Regular 10 pt `--ink`, tabular figures |
| **Zebra rows** | `--paper-dim` `#F4F5F7` on even body rows |
| Horizontal rules | 0.5 pt `--rule-line` between body rows |
| Vertical rules | None in standard tables. Use whitespace. |
| Outer border | 0.75 pt `--rule-line-strong` |
| Row-group band | `--table-group-fill`, Roboto Bold 10 pt `--ink`, spanning all columns |
| Header repeat | Yes, on every continuation page |
| Caption | Roboto Italic 9 pt, above the table (§7.2) |

> **Deviation noted.** The reference documents use a fully ruled grid (colored rules on every cell boundary) with no zebra striping. We use zebra striping with horizontal rules only and no verticals. This improves readability in wide tables and visibly differentiates the design. The glossary table (§8.6) is the one place where we keep the fully ruled treatment.

### 6.2 Alignment

| Content | Alignment | Notes |
|---|---|---|
| Text | Left | Always. |
| Integers, point values | Right | Tabular figures mandatory. |
| Decimals | Decimal-aligned, or right-aligned with a fixed decimal count | Pick one per table and hold it. |
| Dimensions with units | Right | Unit in the column header, not repeated per cell. |
| Yes/No, ✓/– | Center | |
| Mixed prose + number in one cell | Left | Split into two columns instead if it happens twice. |
| Header text | Match the body alignment of its own column | A right-aligned number column gets a right-aligned header. |

### 6.3 Units

1. Units belong in the column header, in parentheses: `Height (in)`. Never repeat a unit in every cell.
2. If a column mixes units, it is two columns.
3. Dual dimensioning in tables: give imperial in the primary column and metric in a separate adjacent column headed `(cm)`. Do not put `36 in (91 cm)` in one cell; it destroys numeric alignment.
4. Currency, percentages, and counts each get their own column type. Never mix.

### 6.4 Scoring table conventions

The scoring table is the most-read table in the manual. Build it as a matrix crossing scoring action against game phase, with thresholds broken out into a separate table.

Structure of **Table 6-4 · SUMMIT PUSH point values**:

- **Merged two-level header.** Top level: a `Match points` group spanning the `Auto` and `Teleop` columns, plus a separate `Ranking Points` column. Second level: the individual column labels.
- **Rows grouped by scoring element**, with the group name in a `--table-group-fill` band spanning the width (`CARGO`, `SUMMIT RACK`, `ENDGAME`).
- **Non-scoring cases get an em dash `—`, never a zero.** `CARGO delivered to an inactive RACK | — | —`. A zero implies the action scores nothing; an em dash correctly says the action does not appear in scoring at all.
- **Ranking-point rows are written as full sentences**, prefixed with `*` where the RP is persistent:
  `*SUMMIT RP — CARGO delivered to an active RACK is at or above threshold. | 1`
- **Win/tie/loss rows spell out the condition in lowercase prose:**
  `completing a MATCH with more MATCH points than your opponent | 3`

**Table 6-5 · SUMMIT PUSH bonus RP thresholds** is a separate table, with columns `Regional & District Events | District Championships | Championship` and one row per RP. Numeric thresholds never appear in the points table. This separation is intentional and load-bearing: it lets thresholds be revised by a Revision Note (§8.4) without touching the scoring *structure*, which is the part teams have memorized.

Add a footnote and a `.note` box flagging that thresholds may increase at championship tiers.

### 6.5 Alliance-differentiated tables

When and only when alliance identity is the axis of the table, tint paired column groups:

- Red column group: `--alliance-red-tint` `#F6DADA`
- Blue column group: `--alliance-blue-tint` `#D9E4F5`

Use this sparingly; expect one or two instances in the entire manual. Because it is direct formatting rather than a defined style, treat it as a convention. Always pair the tint with an explicit `RED ALLIANCE` / `BLUE ALLIANCE` header label so the distinction survives grayscale.

### 6.6 When a table will not fit

In priority order:

1. Shorten header labels; move units to the header.
2. Drop the table body to 9 pt (the floor; never below 9 pt).
3. Split into two stacked tables sharing a caption (`Table 6-7a`, `Table 6-7b`).
4. Transpose rows and columns.
5. Convert to a definition list.

Never rotate a table 90°, never insert a landscape page, and never shrink below 9 pt.

---

## 7. Figures

### 7.1 Numbering

**Format: `Figure <section>-<n>`, sequence restarting at 1 in each section.** Figure 1-1, 1-2, 1-3, then Figure 5-1 … Figure 5-26, then 6-1, and so on. Tables use the same scheme: `Table 6-4`.

Numbers are generated by the build, never typed by hand. Authors write `![](fig/arena-overview.png){#fig-arena-overview}` and reference `[Figure @fig-arena-overview]`; the filter assigns and renders the number.

### 7.2 Captions

| Property | Value |
|---|---|
| Style | Roboto Italic 9 pt `--ink` |
| Alignment | Centered |
| **Position** | ABOVE the figure. Always. Same for tables. |
| Spacing | 6 pt above the caption, 10 pt below it (i.e. between caption and object) |
| Separator | `Figure 5-4 Title`: a space, no colon |
| Keep | Caption keeps-with-next; never orphaned from its object |

> **Deviation noted: we fix an inconsistency.** The reference documents use a space and a colon interchangeably, sometimes on the same page (`Figure 5-5 HUB` vs `Figure 5-6: HUB distance…`). We standardize on the space with no colon, and lint for it. Consistency is worth more than fidelity to someone else's typo.

**Caption content rules:**

- Repeat the defined term in ALL CAPS as it appears in the glossary.
- Parenthetical scope notes are standard and encouraged, in sentence case:
  `Figure 5-1 SUMMIT PUSH ARENA (queue area, technician area, and media area not pictured)`
  `Figure 5-8 SUMMIT RACK exits (approximation)`
  `Figure 10-2 Playoff MATCH bracket (RED ALLIANCE tops each pairing)`
- Captions are sentence-case after the defined terms, no terminal period.

### 7.3 Figure image specifications

| Property | Value |
|---|---|
| Format | PNG for CAD renders and line art; SVG for diagrams we author (preferred); JPEG only for photographs |
| **Effective resolution** | ≥ 200 dpi at placed size. 300 dpi for anything with fine linework. |
| Max placed width | 7.00 in (full measure) |
| Max placed height | 7.50 in (leaves room for caption + a line of text) |
| Color profile | sRGB |
| Alt text | Mandatory on every figure. |

> **Deviation noted.** The reference figures are raster CAD screen captures at 114–223 dpi (median ~150), which do not survive zooming. We require ≥200 dpi and prefer SVG for anything we author, so that our figures are sharper than the ones we are modeling.

### 7.4 Field render conventions

| Element | Treatment |
|---|---|
| Background outside the field | `--figure-ground` `#101214` in top-down views |
| Carpet, orthographic top view | Flat `--carpet` `#666A6E` |
| Carpet, isometric view | `--carpet-lit` `#74787C` |
| Alliance elements, lit faces | `--alliance-red-lit` / `--alliance-blue-lit` |
| Alliance elements, shaded faces | `--alliance-red-shade` / `--alliance-blue-shade` |
| Game pieces | A single reserved hue, distinct from both alliances and the callout magenta. Default: `#E8C33A` gold. |
| Isometric projection | True isometric/axonometric. No perspective convergence, no cast shadows, no ground plane beyond the carpet slab. Consistent viewing angle: ~30° down from a corner, long axis left-to-right. |

### 7.5 Zone tinting

1. Composite the zone hue at 38% opacity over the carpet color. Do not pick a flat muted value; let the compositor produce it.
2. Give every zone a 1.5 pt keyline in the fully saturated hue so the boundary stays crisp.
3. Set the zone name inside the wash, in bold white ALL CAPS, rotated 90° where the region is tall and narrow.
4. Regions that are lines rather than areas (CENTER LINE, STARTING LINE) are not shaded; they get external callouts with leader lines instead.
5. Neutral / shared zones use `--neutral-zone-wash`.

### 7.6 Callouts and leader lines

| Element | Specification |
|---|---|
| Leader line | 1.5 pt `--callout-leader` `#E100E1` |
| Arrowhead | Filled triangle, same magenta, for edges and surfaces |
| **Dot terminator** | Filled circle, same magenta; use when pointing at an area rather than an edge |
| Label box | White fill, 0.75 pt `--ink` border, 3 pt padding, square corners |
| Label text | Roboto Bold 9 pt `--ink`, ALL CAPS, matching the glossary term |
| Explanatory note in a label | Sentence case, in parentheses, below the term: `(highlighted for visibility; CARGO hidden for clarity)` |
| Geometry highlight | Same `#E100E1` as a heavy 3 pt stroke traced over unmodified render geometry |
| Placement | Label boxes go outside the model silhouette, connected inward by leaders. Never overlay a label on geometry. |

### 7.7 The orientation banner

Every top-down field diagram carries a single reusable icon that answers two questions at once: which long edge is the scoring-table side, and which end belongs to which alliance.

**Specification:** a rounded bar, fill `--ink`, height 0.22 in, containing `SCORING TABLE` in Roboto Bold 8 pt `--paper` with +1 pt letterspacing, flanked by a left-pointing and a right-pointing solid triangle. Each arrow is filled in the alliance color of the end it points toward. In SUMMIT PUSH, RED is on the left: red arrow left, blue arrow right. Hold this orientation across every figure in the manual; the banner is the field diagram's compass rose, and its meaning depends on its being invariant.

### 7.8 Drawing sheets

If the package includes engineering drawings, they are a separate PDF from the manual, not bound into it.

| Property | Value |
|---|---|
| Sheet size | ANSI C, 22 × 17 in, landscape (house default). ANSI B (17 × 11) for detail sheets; ANSI D (34 × 22) for large assemblies. |
| Zone grid | 4 columns × 4 rows. Columns numbered 4-3-2-1 left to right (origin bottom-right, ASME convention), printed on top and bottom borders. Rows lettered A (bottom) to D (top), printed on left and right borders. |
| Border | Single thin rectangular frame around the drawing area |
| Units | Inches. Single dimensioning; no dual dimensioning on sheets. |

**Title block** (bottom-right, three bands):

- **Left band (notes stack):**
  `UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES` / `.XX = ±1.00` / `.XXX = ±0.250` / `ANGULAR = ±5°`, then `DO NOT SCALE DRAWING`, then `BREAK ALL SHARP EDGES AND REMOVE BURRS`.
- **Middle band:** `DRAWN | initials | date` row and a `MATERIAL` row.
- **Right band:** the SUMMIT PUSH wordmark set as type (no logo), then `TITLE: SUMMIT PUSH PLAYING FIELD`, then a bottom strip: `SIZE: C | DWG. NO.: SP-FE-01 | REV: B` and `SCALE: 1:50 | SHEET: 1 of 11`.

> **We do not reproduce the "PROPRIETARY AND CONFIDENTIAL / sole property of…" boilerplate.** It is inherited CAD-template text, it contradicts itself on a publicly distributed build document, and reproducing it verbatim while naming a real organization would be a misrepresentation. If a notice is wanted, write an original one, or better, state the actual license (§10.5).

**Dimension line conventions:**

| Convention | Rule |
|---|---|
| **Reference dimensions** | Parenthesized, as in `(119.16)`; carries no tolerance. |
| **Controlled dimensions** | Unparenthesized, with stacked bilateral limits: `4x 119.16 +2.00/−2.00`. |
| Sheet subtitle | Two-line heading, upper-left of the drawing area: `REFERENCE DIMENSIONS:` / `WELDED PERIMETER` |
| Sheet note (required, once per package) | Original prose stating that parenthesized values are reference dimensions provided for convenience, carry no tolerance, and that toleranced dimensions appear only on sheets labeled *Controlled Dimensions*. |
| Extension line gap | 0.06 in from the object |
| Arrowheads | Filled, 3:1 length:width |
| Dimension text | Roboto Condensed Regular, 10 pt, above the line, unrotated |

**Part numbering:** `SP-FE-###` field elements, `SP-GE-###` game elements, `SP-TE-###` team-buildable elements, with `SP-EV-#####` for evergreen (carried-forward) parts. Mirror game-element and team-element numbers (`SP-GE-300` HUB ⇄ `SP-TE-300` HUB) so the correspondence is obvious.

**Dates: ISO 8601 everywhere, as in `2026-02-26`.** Both the title block and the revision table use it. The reference documents mix US format in the title block with ISO in the revision table; that is an inconsistency, not a convention.

**Revisions:** single letters (A, B, C), one line each in a sheet-1 revision table (`REV | DESCRIPTION | DATE | DRAWN`). The whole package revs together: the rev letter appears in every sheet's title block. Flag changed features in the drawing area with a triangular revision balloon containing the rev letter.

---

## 8. Front Matter and Back Matter

### 8.1 Cover (page 1)

Full-page composition. Type stack, all Roboto, all centered, over an authored background (an abstract geometric field, a photographic plate, or a flat `--accent-deep` ground; never a borrowed image):

| Line | Content | Style | Baseline from top |
|---|---|---|---|
| 1 | `SUMMIT PUSH` game wordmark | Roboto Bold 40 pt `--ink` (or `--paper` on a dark ground) | 4.85 in |
| 2 | `Game Manual` | Roboto Regular 18 pt | 5.45 in |
| 3 | `2026 Season` | Roboto Regular 14 pt `--muted`, +0.5 pt tracking | 6.10 in |
| 4 | Revision stamp `Revision: TU-14` | Roboto Regular 10 pt `--muted` | 10.20 in |

No table of contents on the cover. No sponsor lockups. No logos of any kind.

### 8.2 Contents (pages 2–3)

- Title `Contents` in Roboto Bold 16 pt `--ink`, left-aligned at the front-matter left margin.
- **Exactly two pages.** If it overflows, tighten level-2 leading before adding a page.
- **Two levels only:** section (`7`) and subsection (`7.2`). Third-level headings (`5.9.2`) exist in the body and are left out of the TOC on purpose, because a three-level TOC for a 15-section rulebook becomes an index that nobody reads.
- **Two-column tab structure:** number in its own left cell, title in the second cell, dot leaders to a right-aligned page number.
- Level 1: Roboto Bold 11 pt. Level 2: Roboto Regular 10 pt, indented 0.15 in.
- Dot leaders in `--muted`, generated by the layout engine, never typed.
- Page numbers use tabular figures, right-aligned to the measure.
- Every entry is a live internal link in the digital PDF.

### 8.3 Introduction (Section 1)

Section 1 must include, in original prose:

1. **1.1** What this manual is and who it binds.
2. **1.2** Game overview in one paragraph.
3. **1.3** Season timeline.
4. **1.4** How to read this document: the conventions passage. Here, state that defined terms are ALL CAPS and collected in the Glossary; that cross-references and links appear in blue underlined text; that note boxes explain but do not command and never override a rule; that persistent rules are marked with a leading asterisk and a green headline, while season-specific rules use a blue headline; that imperial dimensions govern and metric is a convenience; and that the text means what it says, with nothing hidden.
5. **1.5** The rule numbering scheme, with a figure (`Figure 1-3 Rule numbering method`) diagramming it.
6. **1.6** Revision Notes: the cadence and markup convention (§8.4).
7. **1.7** Versions and precedence: which file is canonical.

> Refer to this passage by title ("How to Read This Document"), never by number, when citing it elsewhere. Section numbers for conventions text drift between editions; titles do not.

### 8.4 Revision history

**Decision: we deviate.** The reference manuals contain no revision history page, no changelog and no appendices. Version state lives only in the footer stamp, and enumerated changes live in separately published update documents. That externalization works for an organization with a distribution website and a mailing list. It does not work for a standalone fictional PDF that will circulate as a single file.

SUMMIT PUSH therefore includes an in-document revision history, placed in the front matter on page 3 or 4, immediately after the Contents.

**Table format:**

| Revision | Date | Sections touched | Summary |
|---|---|---|---|
| TU-14 | 2026-03-03 | 6.5, 7.2 | Raised SUMMIT RP threshold at Championship; clarified G214 de-scoring. |
| TU-13 | 2026-02-24 | 8.4 | Corrected BUMPER height tolerance in R405. |

- Newest first.
- ISO 8601 dates.
- The `Sections touched` cell lists section numbers, comma-separated, and is a live link.
- The `Summary` cell is one sentence. Full detail belongs in the rule text, not here.

**Revision markup convention** (used in separately published Revision Note documents, and optionally in a redline build of the manual):

- **Additions** highlighted in `--change-add` `#FFF3A8`.
- **Deletions** rendered with a strikethrough in `--change-del` `#6E7378`.
- Both are applied inline within the reproduced paragraph, so the reader sees the amended text in context rather than a before/after pair.

**Revision stamping format:** `Revision: TU-NN` document-wide on the cover; `Revision: SN-vM` per-section in the body footer (§2.5).

### 8.5 Version precedence statement

State once, in §1.7, in original prose: which file is canonical (the English PDF), that other formats and translations are conveniences that do not override it, and that where they conflict the canonical PDF governs.

### 8.6 Glossary (Section 15)

The final section, running to the last page.

**Two-column table:**

| Property | Value |
|---|---|
| Header row | `--accent` fill, `Term` and `Definition` in Roboto Bold 10 pt white |
| Term column width | 2.20 in |
| Definition column width | 4.80 in |
| Cell borders | 1 pt solid `--accent`, all cells (the glossary keeps the fully ruled treatment; §6.1) |
| Cell padding | 0 top/bottom, 5.4 pt left/right |
| Paragraph space-after in cells | 3 pt |
| Term style | Roboto Bold 10 pt, ALL CAPS |
| Definition style | Roboto Regular 10 pt |
| Zebra striping | None in the glossary |

**Definition writing convention:** definitions are sentence fragments that complete an implied "X is…". They start lowercase and take no terminal period.

- ✅ `ALLIANCE | a cooperative of up to 3 SUMMIT PUSH teams`
- ❌ `ALLIANCE | An ALLIANCE is a cooperative of up to 3 teams.`

Alphabetize by the term string. Cross-reference related terms with a linked `see also` at the end of a definition, in `--muted` italic.

### 8.7 Index

**Decision: no back-of-book index.** Rationale: the rule-ID addressing scheme (`G214`) plus the glossary plus a two-level TOC plus full-text search in the PDF cover every retrieval path an index would serve, and a hand-maintained index goes stale after the second revision.

**Instead, ship a "Rule Finder" as the last two pages**: a compact three-column list of every rule ID in the manual with its headline text and page number, sorted by ID. Generate it from the source; never maintain it by hand. Set it in Roboto Condensed 8.5 pt to fit.

### 8.8 What we do NOT include

- **No copyright footer on every page.** The genre does not carry one, and neither do we. One license statement on the back page is sufficient (§10.5).
- **No appendices.** If content is important enough to include, it is important enough to be a numbered section.
- **No "all rights reserved" block**, no trademark attribution table.
- **No sponsor recognition content** beyond the section stub. Section 3 exists for structural parity and states that SUMMIT PUSH is a fictional game with no sponsors.

---

## 9. Production Recipe

### 9.1 Toolchain decision

**Recommended: Typst.**

| Option | Verdict |
|---|---|
| **Typst** | ✅ Recommended. Native, precise page geometry. Real running-header/footer logic with per-section state, which our per-section revision stamp needs. Fast (sub-second rebuilds on a 150-page document). Modern scripting for rule numbering and figure numbering. A single self-contained binary that is easy to install in CI. Embeds fonts cleanly. |
| **Pandoc → LaTeX (`xelatex`)** | ✅ Solid fallback. Best-in-class typesetting; `fancyhdr`, `tcolorbox`, `longtable`, `enumitem` cover every requirement. Cost: slow, and the error messages are hostile. Choose this if the team already knows LaTeX. |
| **Paged.js + Chrome headless** | ⚠️ Viable. Best if the same CSS must serve web and print. Cost: fragile pagination on tables and boxes, weak widow/orphan control, heavyweight CI. |
| **wkhtmltopdf** | ❌ Do not use. Ancient WebKit, no CSS Paged Media support, no `break-inside`, no running elements. It cannot produce this document. |
| **Word / InDesign** | ❌ Not reproducible from Markdown sources. |

We specify a Typst primary build and a Pandoc/LaTeX reference build, both driven from the same Markdown sources through the same Pandoc AST filters.

### 9.2 Repository layout

```
summit-push/
├─ src/
│  ├─ 00-cover.md
│  ├─ 00-revisions.md
│  ├─ 01-introduction.md
│  ├─ 05-arena.md
│  ├─ 07-game-rules.md          # rules as fenced divs
│  ├─ …
│  └─ 15-glossary.yml           # glossary is DATA, not prose
├─ assets/
│  ├─ fonts/                    # Roboto, Roboto Condensed, JetBrains Mono
│  ├─ fig/                      # PNG/SVG figures
│  └─ header-band.svg           # authored, not borrowed
├─ style/
│  ├─ tokens.yml                # single source of truth for §3 colors
│  ├─ manual.typ                # Typst template
│  ├─ manual.tex                # LaTeX fallback template
│  └─ print.css                 # Paged.js / HTML preview
├─ build/
│  ├─ filters/
│  │  ├─ rules.lua              # rule divs → numbered blocks
│  │  ├─ crossref.lua           # figure/table/rule numbering + anchors
│  │  ├─ glossary.lua           # YAML → table; caps linting
│  │  └─ tokens.lua             # inject tokens.yml into templates
│  ├─ lint.py                   # §9.6 checks
│  └─ acronyms.txt
├─ Makefile
└─ out/
   ├─ SummitPush-GameManual.pdf
   └─ SummitPush-GameManual.html
```

`style/tokens.yml` is the single source of truth for color. Every template reads from it, so a palette change is a one-file edit.

### 9.3 Markdown authoring conventions

Use Pandoc Markdown with fenced divs and bracketed spans.

```markdown
# Game Rules (G) {#s-7}

## Robot Interaction {#s-7-2}

::: rule {#G201 .persistent}
**G201** [*Keep your hands to yourself.]{.headline} A ROBOT may not deliberately
damage or entangle an opponent ROBOT.

  A. Contact incidental to a scoring attempt is not a violation of this rule.
  B. Contact with an opponent's BUMPER is not by itself damage.

::: violation
MAJOR FOUL. YELLOW CARD if the contact is repeated during the MATCH.
:::
:::

::: note
This rule exists to keep MATCHES competitive rather than attritional. REFEREES
judge deliberateness by the approach, not the outcome.
:::

![SUMMIT PUSH ARENA (queue area not pictured)](fig/arena.svg){#fig-arena width=7in}

Refer to [Figure @fig-arena] and rule [@G201] before reading section [@s-7-2].
```

Author rules: authors type the rule ID and the headline. They never type the word `Violation:`, a figure number, a table number or a page reference; the build generates all of those.

### 9.4 Typst template sketch

```typst
#let tok = (
  ink: rgb("#1A1D21"), paper: rgb("#FFFFFF"), paperdim: rgb("#F4F5F7"),
  accent: rgb("#1F4E79"), accentbright: rgb("#2E6FA8"), accentdeep: rgb("#16385A"),
  stable: rgb("#1E7A4C"), seasonal: rgb("#1F4E79"), muted: rgb("#6E7378"),
  ruleline: rgb("#C8CCD1"), boxfill: rgb("#DCE6F1"), boxborder: rgb("#1F4E79"),
  warnfill: rgb("#FBEBD2"), warnborder: rgb("#B26A12"),
  dangerfill: rgb("#F7DEDE"), dangerborder: rgb("#A32A2A"),
  link: rgb("#245C9E"),
)

#let section-state = state("section", "")
#let rev-state     = state("rev", "")

#set document(title: "SUMMIT PUSH Game Manual")
#set page(
  paper: "us-letter",
  margin: (top: 1.30in, bottom: 0.85in, left: 0.75in, right: 0.75in),
  header: header-band(),                       // authored SVG + type, full bleed
  footer: context {
    set text(font: "Roboto", weight: "bold", size: 10pt, fill: tok.ink)
    grid(columns: (1fr, 1fr, 1fr),
      align(left)[#section-state.get()],
      align(center)[Revision: #rev-state.get()],
      align(right)[#counter(page).display("1 of 1", both: true)])
  },
)

#set text(font: ("Roboto", "Arimo", "Liberation Sans"), size: 11pt, fill: tok.ink)
#set par(justify: false, leading: 0.52em, spacing: 6pt)   // space-BEFORE model
#show link: it => text(fill: tok.link, underline(it))

// ── Headings ────────────────────────────────────────────────────────────
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  section-state.update(it.body)
  block(above: 12pt, below: 12pt)[
    #set text(size: 16pt, weight: "bold", tracking: 1pt, fill: tok.ink)
    #it
  ]
}
#show heading.where(level: 2): it => block(above: 12pt, below: 2pt)[
  #set text(size: 13pt, weight: "bold", fill: tok.accent); #it
]
#show heading.where(level: 3): it => block(above: 10pt, below: 0pt)[
  #set text(size: 11pt, weight: "bold", fill: tok.ink); #it
]
#show heading.where(level: 4): it => block(above: 8pt, below: 0pt)[
  #set text(size: 11pt, weight: "regular", style: "italic"); #it
]

// ── Rule block ──────────────────────────────────────────────────────────
#let rule(id, headline, persistent: false, body) = block(
  above: 6pt, below: 0pt, breakable: true,
)[
  #set par(hanging-indent: 0.5in)
  #pad(left: 0.5in)[
    #text(weight: "bold")[#id]#h(0.5em)
    #text(weight: "bold", fill: if persistent { tok.stable } else { tok.seasonal })[
      #if persistent [*] #headline
    ]
    #h(0.35em) #body
  ]
]

#let violation(body) = block(above: 6pt, below: 0pt)[
  #pad(left: 0.5in)[
    #text(style: "italic", fill: tok.muted)[Violation: #body]
  ]
]

// ── Note boxes ──────────────────────────────────────────────────────────
#let notebox(kind: "note", body) = {
  let (fill, stroke, label) = if kind == "warning" {
    (tok.dangerfill, 2pt + tok.dangerborder, [*WARNING.* ])
  } else if kind == "caution" {
    (tok.warnfill, 1.5pt + tok.warnborder, [*CAUTION.* ])
  } else { (tok.boxfill, 1.5pt + tok.boxborder, []) }
  block(above: 6pt, below: 0pt, width: 100%)[
    #pad(left: 1in, right: 1in)[
      #block(fill: fill, stroke: stroke, inset: (x: 4pt, y: 3pt), width: 100%)[
        #label#body
      ]
    ]
  ]
}

// ── Tables ──────────────────────────────────────────────────────────────
#set table(stroke: none, inset: (x: 7pt, y: 4pt))
#show table.cell.where(y: 0): set text(
  weight: "bold", size: 10pt, fill: white,
)
#let mtable(..args) = table(
  fill: (_, y) => if y == 0 { tok.accent }
                  else if calc.even(y) { tok.paperdim } else { none },
  stroke: (_, y) => if y > 0 { (top: 0.5pt + tok.ruleline) },
  ..args,
)

// ── Captions: ABOVE the object, italic 9pt, centered ────────────────────
#show figure: it => block(above: 6pt, below: 6pt)[
  #align(center)[
    #block(above: 6pt, below: 10pt)[
      #text(size: 9pt, style: "italic")[
        #it.supplement #context it.counter.display("1-1") #h(0.35em) #it.caption.body
      ]
    ]
    #it.body
  ]
]
#set figure(numbering: (..n) => numbering("1-1", counter(heading).get().first(), ..n))
```

### 9.5 Print CSS sketch (Paged.js / HTML preview)

```css
:root{
  --ink:#1A1D21; --paper:#fff; --paper-dim:#F4F5F7;
  --accent:#1F4E79; --accent-bright:#2E6FA8; --accent-deep:#16385A;
  --stable:#1E7A4C; --seasonal:#1F4E79; --muted:#6E7378;
  --rule-line:#C8CCD1; --box-fill:#DCE6F1; --box-border:#1F4E79;
  --warn-fill:#FBEBD2; --warn-border:#B26A12;
  --danger-fill:#F7DEDE; --danger-border:#A32A2A; --link:#245C9E;
  --font-sans:"Roboto","Arimo","Liberation Sans",Arial,sans-serif;
  --font-cond:"Roboto Condensed","Liberation Sans Narrow",sans-serif;
  --font-mono:"JetBrains Mono","DejaVu Sans Mono",monospace;
}

@page{
  size:8.5in 11in;
  margin:1.30in .75in .85in .75in;
  @top-left-corner{content:"";}
  @bottom-left  { content:string(section);  font:700 10pt var(--font-sans); color:var(--ink);}
  @bottom-center{ content:"Revision: " string(revision); font:700 10pt var(--font-sans);}
  @bottom-right { content:counter(page) " of " counter(pages); font:700 10pt var(--font-sans);}
}
@page:first{ margin:0; @bottom-left{content:"";} @bottom-right{content:"";} }

html{font:400 11pt/1.38 var(--font-sans); color:var(--ink);
     font-feature-settings:"tnum" 0;}
p{margin:6pt 0 0 0; text-align:left; hyphens:none;}

h1{font:700 16pt/1.2 var(--font-sans); letter-spacing:1pt; margin:12pt 0 12pt 0;
   padding-left:.5in; text-indent:-.5in;
   break-before:page; break-after:avoid; string-set:section content();}
h2{font:700 13pt/1.25 var(--font-sans); color:var(--accent);
   margin:12pt 0 2pt 0; padding-left:.4in; text-indent:-.4in; break-after:avoid;}
h3{font:700 11pt/1.35 var(--font-sans); margin:10pt 0 0 0;
   padding-left:.5in; text-indent:-.5in; break-after:avoid;}
h4{font:400 italic 11pt/1.35 var(--font-sans); margin:8pt 0 0 0;
   padding-left:.6in; text-indent:-.6in; break-after:avoid;}

.rule{margin:6pt 0 0 .5in; text-indent:-.5in; break-inside:auto;}
.rule > :first-child{break-after:avoid;}
.rule-num{font-weight:700; color:var(--ink);}
.headline{font-weight:700; color:var(--seasonal); font-style:normal;}
.persistent .headline{color:var(--stable);}
.subclause{margin:6pt 0 0 1in;  text-indent:-.25in;}
.subitem  {margin:6pt 0 0 1.25in; text-indent:-.25in;}

.violation{margin:6pt 0 0 .5in; font-style:italic; color:var(--muted);
           break-before:avoid;}
.violation::before{content:"Violation: ";}

.note,.caution,.warning{
  margin:6pt 1in 0 1in; padding:3pt 4pt; break-inside:avoid;}
.note   {background:var(--box-fill);   border:1.5pt solid var(--box-border);}
.caution{background:var(--warn-fill);  border:1.5pt solid var(--warn-border);}
.warning{background:var(--danger-fill);border:2pt   solid var(--danger-border);}
.caution > p:first-child::before{content:"CAUTION. "; font-weight:700;
                                 color:var(--warn-border);}
.warning > p:first-child::before{content:"WARNING. "; font-weight:700;
                                 color:var(--danger-border);}
.box-caption{font:italic 400 9pt/1.3 var(--font-sans); text-align:center;
             margin:4pt 0 0 0;}

figure{margin:0; break-inside:avoid;}
figcaption{font:italic 400 9pt/1.3 var(--font-sans); text-align:center;
           margin:6pt 0 10pt 0; break-after:avoid;}
figure > figcaption{order:-1;}          /* caption ABOVE the object */
figure{display:flex; flex-direction:column;}
figure img{max-width:100%; align-self:center;}

table{width:100%; border-collapse:collapse; font:400 10pt/1.3 var(--font-sans);
      font-feature-settings:"tnum" 1; border:.75pt solid #8A9199;
      break-inside:auto;}
thead{display:table-header-group;}      /* repeat header across pages */
th{background:var(--accent); color:#fff; font-weight:700;
   padding:6pt 7pt; text-align:left;}
td{padding:4pt 7pt; border-top:.5pt solid var(--rule-line);}
tbody tr:nth-child(even) td{background:var(--paper-dim);}
td.num,th.num{text-align:right;}
tr.group td{background:#E4E9EF; font-weight:700;}

a{color:var(--link); text-decoration:underline;}
code{font:400 9.5pt var(--font-mono); background:var(--paper-dim); padding:0 2pt;}
pre{font:400 9pt/1.4 var(--font-mono); background:var(--paper-dim);
    border:1pt solid var(--rule-line); padding:6pt; margin:6pt 0;
    break-inside:avoid;}

.glossary td{border:1pt solid var(--accent); padding:0 5.4pt;}
.glossary tbody tr:nth-child(even) td{background:transparent;}
.glossary td:first-child{font-weight:700; width:2.2in;}

p,li{orphans:2; widows:2;}
```

### 9.6 Build pipeline

```makefile
FONTS := assets/fonts
SRC   := $(wildcard src/*.md)

pdf: lint
	typst compile --font-path $(FONTS) \
	  --input rev=$(REV) style/manual.typ out/SummitPush-GameManual.pdf

pdf-latex: lint
	pandoc $(SRC) \
	  --lua-filter=build/filters/rules.lua \
	  --lua-filter=build/filters/crossref.lua \
	  --lua-filter=build/filters/glossary.lua \
	  --template=style/manual.tex --pdf-engine=xelatex \
	  -o out/SummitPush-GameManual.pdf

html:
	pandoc $(SRC) --lua-filter=build/filters/crossref.lua \
	  -s --css=style/print.css -o out/SummitPush-GameManual.html

lint:
	python build/lint.py $(SRC)
```

**`build/lint.py` must enforce, as build-blocking errors:**

1. Every ALL-CAPS token in the body (≥2 chars, not in `acronyms.txt`) has a glossary entry.
2. Every glossary entry appears in ALL CAPS at least once in the body.
3. Every rule ID is unique, matches `^[QGRITCE][1-9][0-9]{2}$`, and is monotonic within its subsection.
4. Every rule has exactly one headline span and at most one violation block.
5. Every persistent rule's headline starts with `*`; no season-specific headline does.
6. Every figure and table has a caption, and no caption contains a colon after the number.
7. Every cross-reference resolves to an existing anchor.
8. No hard-typed figure number, table number, or page reference anywhere in `src/`.
9. No color literal appears outside `style/tokens.yml`.
10. No hyphen used where an en dash or em dash is required in a numeric range.

**Acceptance tests before shipping a build:**

- Print pages 1 and 2 and one page from each rule-bearing section in grayscale. Every semantic distinction must still be readable.
- Confirm that all fonts are embedded: `pdffonts out/SummitPush-GameManual.pdf` should list Roboto, Roboto Condensed and JetBrains Mono, all subset-embedded, and nothing else.
- Confirm no page scrolls horizontally in the HTML build at 1024 px.
- Spot-check that no violation line is orphaned from its rule and no caption is orphaned from its figure.
- Confirm the PDF has no `Producer`/`Creator` string naming an unintended tool or organization.

---

## 10. What We Do Not Copy

This section is normative. A build that violates it does not ship.

### 10.1 Names and marks

Do not place any of the following in the manual, the drawings, the file metadata, the filenames, the repository, or the alt text:

- **FIRST**, *FIRST*®, FIRST Robotics Competition, FRC, FIRST Tech Challenge, FTC, FIRST LEGO League, FLL, FIRST Championship, or any abbreviation or stylization of them.
- Program season names or game names: REBUILT, REEFSCAPE, CRESCENDO, or any other.
- Slogans and registered phrases: *Gracious Professionalism*®, *Coopertition*®, *More than Robots*®, and equivalents.
- Any sponsor name appearing in a real manual, including in a "presented by" construction, which is the construction that implies sponsorship.
- Any real organization's name in a way that implies endorsement, affiliation, origin, or approval.

Published text does not describe SUMMIT PUSH as "FRC-style". The shipped manual describes it as an original game for competitive-robotics design training.

### 10.2 Artwork and assets

- **No logos, wordmarks, or lockups** of any real organization, program or sponsor: not in the header band, not on the cover, not in a drawing title block, and not scaled down, recolored or partially cropped.
- **No header banner artwork** from any real manual. Ours is authored from scratch: a flat color band, a type-set wordmark, and two rules. Nothing is traced, sampled, or re-drawn from an existing banner.
- **No cover artwork** from any real manual or season asset package.
- **No field renders, figures, photographs, or CAD screen captures** originating from a real competition. Every figure in SUMMIT PUSH is authored for SUMMIT PUSH.
- **No AprilTag layouts, coordinate tables, or field drawings** copied from a real package. If SUMMIT PUSH uses fiducial markers, generate our own layout with our own coordinate origin and our own IDs.

### 10.3 Verbatim text

- **No verbatim rule text**, from any season, in any section. Rules are written for SUMMIT PUSH from scratch. Structural *shape* is fine; sentences are not.
- **No verbatim conventions passage.** Write "How to Read This Document" in original prose. Do not paraphrase closely; write it fresh.
- **No verbatim glossary definitions.** Even for a term as generic as ALLIANCE, write our own.
- **No verbatim disclaimers**, precedence statements, or accuracy notices.
- **No "PROPRIETARY AND CONFIDENTIAL / sole property of…" boilerplate** on drawing sheets. That text names a specific owner and asserts a specific restriction. Ours would be false. Omit it or write an original notice.
- **No copyright line naming anyone but us.**

### 10.4 Reference colors (documented, not adopted)

The corporate palette (`#231F20`, `#ED1C24`, `#0066B3`, `#9A989A`), the program blue (`#009CD7`), and the season accents (`#0083AE`, `#00B050`, `#ABD8E7`) appear in §3.2 as research annotation only. They must not appear in `style/tokens.yml`, in any template, in any figure, or in any shipped asset. Lint rule 9 enforces this; add all of them to a build-time denylist.

A single color is rarely protectable on its own, but a *palette* deployed in the *same layout* on a *similar document* is how trade dress confusion is established. We change the palette so that no such argument is available.

### 10.5 What we affirmatively do

1. **Use our own name throughout.** SUMMIT PUSH, its own wordmark set as type, its own part-number prefix (`SP-`).
2. **Use our own palette** (§3.3), a different hue family from any real program.
3. **Use freely licensed fonts only** (Roboto, Roboto Condensed and JetBrains Mono, all under the SIL OFL 1.1). Typeface choice is not a trademark issue; a typeface is a tool.
4. **Author every figure.** SVG or original render, made for this manual.
5. **Write every rule, definition, and disclaimer from scratch.**
6. **Carry a disclaimer on the cover verso or the last page**, in plain original prose, to this effect:

   > SUMMIT PUSH is a fictional game. This manual is an original work of design and writing. It is not affiliated with, endorsed by, sponsored by, or connected to any real robotics competition, organization, or program, and it does not describe any real event. Any resemblance to the structure of real competition documents is a matter of shared genre convention, not shared origin.

7. **Ship an explicit license** for our own content on the last page (CC BY-SA 4.0 recommended, or "all rights reserved" if the project prefers). Say what people may do with it.
8. **Keep PDF metadata clean.** `Title: SUMMIT PUSH Game Manual`, `Author:` the project name, `Producer:` whatever the toolchain writes. No borrowed strings.

### 10.6 The test to apply

Before shipping any page, ask whether a stranger who saw the page with no context could reasonably believe that a real organization produced it.

If yes, something on that page is doing identity work it should not be doing. Find it and change it. It will almost always be one of three things: a mark, an image, or a palette.

---

## Appendix A. Quick Reference Card

| Thing | Value |
|---|---|
| Page | US Letter 8.5 × 11 in portrait |
| Margins | 1.30 / 0.85 / 0.75 / 0.75 in (T/B/L/R) |
| Measure | 7.00 in, single column, ragged right |
| Body | Roboto Regular 11 pt / 1.38, 6 pt space-before, 0 after |
| H1 / H2 / H3 / H4 | 16 pt bold `--ink` +1pt track / 13 pt bold `--accent` / 11 pt bold / 11 pt italic |
| Rule number | Bold 11 pt `--ink`, hanging −0.50 in |
| Persistent headline | Bold 11 pt `--stable` `#1E7A4C`, leading `*` |
| Seasonal headline | Bold 11 pt `--seasonal` `#1F4E79` |
| Violation | Italic 11 pt `--muted` `#6E7378`, indent 0.50 in, whole line |
| Note box | `#DCE6F1` fill, 1.5 pt `#1F4E79` border, 1.00 in both insets |
| Caption | Italic 9 pt, centered, ABOVE, 6 pt above / 10 pt below, no colon |
| Table header | `#1F4E79` fill, bold 10 pt white |
| Zebra | `#F4F5F7`, even rows |
| Link | `#245C9E` underlined |
| Footer | Bold 10 pt: `Section N Title` · `Revision: SN-vM` · `N of TOTAL` |
| Page numbering | Continuous, cover = 1, `N of TOTAL` |
| Toolchain | Typst primary, Pandoc + xelatex fallback |