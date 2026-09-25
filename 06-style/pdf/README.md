# PDF edition of the Game Manual

This folder typesets `02-manual/sections/*.md` into `02-manual/SUMMIT-PUSH-Game-Manual.pdf`,
following `06-style/MANUAL-STYLE-GUIDE.md`.

```bash
bash 06-style/pdf/build.sh           # the PDF
bash 06-style/pdf/render_figures.sh  # the figures in 02-manual/figures (after a field geometry change)
```

## Requirements

- Python 3 with `markdown-it-py` and `pypdf` (`pip install markdown-it-py pypdf`).
- Node 18 or later. `build.sh` runs `npm ci` here on first use, which installs Paged.js,
  `playwright-core` and the Fontsource packages pinned in `package-lock.json`.
- Chromium: set `CHROME_PATH` to a Chromium or Chrome binary, or run
  `npx playwright install chromium` once.
- `render_figures.sh` also needs the field model's off-line build and Pillow: `pip install cadquery-ocp numpy pillow`.

## How it works

| Step | File | What it does |
|---|---|---|
| 1 | `make_html.py` | Parses the manual sources and writes `build/manual.html` (cover, contents, revision history, the nine sections, Appendix A) and `build/plates.html` (the six drawing sheets). Rule paragraphs, violation lines, Example and Commentary boxes, captions, figures and cross-references get the classes and links the stylesheet expects. |
| 2 | `manual-print.css`, `furniture.js` | The print stylesheet (page, type, color, tables, boxes) and the Paged.js handlers that draw the header band on every page but the cover and repeat a table's header row on each page it runs onto. |
| 3 | `render.mjs` | Serves the pages locally, paginates the manual with Paged.js in headless Chromium, prints both PDFs, and records the page of every section for the bookmarks. |
| 4 | `postprocess.py` | Appends the plates, sets the print boxes (0.125-in bleed kept in the MediaBox and BleedBox; TrimBox and CropBox at Letter size), and adds the bookmarks and metadata. |

`build.sh` runs steps 1–3 twice: the first pass counts the manual's pages, the second prints the
final `N of TOTAL` footers and the plate page numbers.

Figures: `render_figures.sh` builds the field with the OpenCascade twin of the Onshape generator,
exports it to glTF and renders the views in `figure-shots.json` with the three.js stage in
`03-field/featurescript/verify/webrender`. `figures.py` trims each image, projects each callout's
anchor (a point in field inches) through the same camera, places the labels inside the image, and
fails if an anchor falls outside the image, or if a label overlaps another label or anchor or has
a leader that crosses another leader or label. `make_html.py` draws the callouts as vector leaders and labels over the image.

The revision stamp and the revision history table come from `revisions.json`: add a row for each
Team Update.

## Fonts

Roboto, Roboto Condensed, JetBrains Mono and Noto Sans Math (all SIL Open Font License 1.1) are
vendored in `fonts/` with their license files, in the weights and Unicode subsets the manual uses.
Noto Sans Math supplies only the arrows block (U+2190–21FF), which Roboto lacks; it sits second in
the sans and condensed stacks. `vendor_fonts.py` regenerates the fonts and `fonts.css` from the
Fontsource packages.
