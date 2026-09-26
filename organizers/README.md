# SUMMIT PUSH — Organizer Materials

This folder is for the people who run a SUMMIT PUSH CADathon and maintain the game package. It is not part of the participant kit: squads receive `participants/` only. Because this repository is public, anyone can read this folder; see `moderation/ORGANIZER-GUIDE.md` §2 for how to keep it from squads.

| Path | Contents |
|---|---|
| `moderation/ORGANIZER-GUIDE.md` | Running the event: roles, what to release and when, kickoff printing, Q&A and Team Updates, judging, the results show. |
| `design/DESIGN-SPEC.md` | The locked design specification. Every number, name and rule decision in the package comes from it. |
| `design/REVISION-LOG.md` | Every change from v1.0 through v2.2, with the reasoning and the arithmetic behind it. Paths in its sections A–N refer to the layout before the reorganization recorded in N28. |
| `source/manual/` | The manual's source: one Markdown file per section in `sections/`, the front matter in `manual-header.md`, and `build.sh`, which compiles them into `participants/01-game-manual/GAME-MANUAL.md`. |
| `source/drawings/` | `generate_drawings.py` and its drawing library `_drawlib.py`, which write the six sheets in `participants/03-field/drawings/` from the ledger values. |
| `source/featurescript/` | The Onshape field generator's sources, its build (`build.py`, which writes `participants/03-field/onshape/SummitPushField.fs`) and its off-line verification. See its `README.md` and `AUTHORING.md`. |
| `source/vision/make_layout.py` | Generates `participants/04-vision/apriltag-field-layout.json` from the tag table in the vision guide. |
| `source/typesetting/` | `MANUAL-STYLE-GUIDE.md` (the typesetting standard), `research-notes.md` (the research behind it), `pdf/` (the PDF build and figure renderer) and `figure-callouts/` (callout positions for the manual's figures). |
| `source/verify/` | The verification suite for the documents and drawings. See its `README.md`. |
| `archive/research/` | Design research: community opinion of past competition games, game history, educational value, technical standards, a comparable design challenge, and a gap analysis. |
| `archive/concepts/` | The design-phase archive: five game concepts and three judges' reports, written before the specification. `FIRST-ASCENT.md` became SUMMIT PUSH. |
| `discord/` | Discord server setup: channel structure, roles, message templates, and the server icon and banner in `brand/`. |

## Building and verifying

The manual build, the drawing generator and the verification suite need only bash and Python 3 (standard library). From the repository root:

```bash
bash organizers/source/verify/run-all.sh
```

This rebuilds `participants/01-game-manual/GAME-MANUAL.md` and the six drawing sheets, runs the five checks described in `source/verify/README.md` (the numbers, cross-references and superseded values, cross-document agreement, drawing layout, and drawing geometry), and confirms that the layout JSON matches the vision guide's tag table. On a clean run every check reports zero failures: `RESULT: 0 failure(s)` from `verify.py`, `crossdoc.py` and `svg_geom.py`, `TOTAL layout issues: 0` from `svg_collide.py`, and, in the `consist.py` report, no dangling references, no missing glossary entries, every restated rule `ok` and every `STALE` line `CLEAN`; the layout check prints `apriltag-field-layout.json matches VISION-GUIDE.md §3`. The script's last line says only whether every check ran to completion, so read each check's summary.

To rebuild without checking:

```bash
bash organizers/source/manual/build.sh                     # compile the manual
python3 organizers/source/drawings/generate_drawings.py    # regenerate the six drawing sheets
python3 organizers/source/vision/make_layout.py            # regenerate the AprilTag layout JSON
```

The PDF edition needs Python 3 with `markdown-it-py`, `pypdf` and `Pillow`, Node 18 or later, and Chromium; the figure renderer also needs `cadquery-ocp` and `numpy` (see `source/typesetting/pdf/README.md`):

```bash
bash organizers/source/typesetting/pdf/build.sh            # -> participants/01-game-manual/SUMMIT-PUSH-Game-Manual.pdf
bash organizers/source/typesetting/pdf/render_figures.sh   # re-render the manual's figures after a geometry change
```

The Onshape field generator has its own build and off-line checks, which `run-all.sh` does not run:

```bash
python3 organizers/source/featurescript/build.py              # assemble SummitPushField.fs and lint it
python3 organizers/source/featurescript/verify/run.py         # build the field off-line and check it
python3 organizers/source/featurescript/verify/run_checks.py  # the independent per-element checks
```

### Generated files

Everything in `participants/` except the Markdown documents in `02-cadathon/`, `03-field/` and `04-vision/` is generated. Edit the source and rebuild:

| Participant file | Source | Built by |
|---|---|---|
| `01-game-manual/GAME-MANUAL.md` | `source/manual/sections/*.md`, `manual-header.md` | `source/manual/build.sh` |
| `01-game-manual/SUMMIT-PUSH-Game-Manual.pdf` | the same, plus `source/typesetting/pdf/` | `source/typesetting/pdf/build.sh` |
| `01-game-manual/figures/*.png` | the field model and `source/typesetting/pdf/figure-shots.json` | `source/typesetting/pdf/render_figures.sh` |
| `03-field/drawings/*.svg` | the constants in `source/drawings/generate_drawings.py` | that script |
| `03-field/onshape/SummitPushField.fs` | `source/featurescript/src/*.fs` | `source/featurescript/build.py` |
| `04-vision/apriltag-field-layout.json` | the tag table in `participants/04-vision/VISION-GUIDE.md` §3 | `source/vision/make_layout.py` |

### Making a change

Take a geometry change through the documents in order of authority:

1. `design/DESIGN-SPEC.md`.
2. The master dimension ledger in `participants/03-field/FIELD-CAD-PACKAGE.md` §10, and the element's section.
3. The manual section that states the value (`source/manual/sections/`).
4. The constant in `source/drawings/generate_drawings.py`; then regenerate the drawings.
5. The constant in `source/featurescript/src/20_ledger.fs`; then rebuild and check the generator.
6. If a tag pose moved: the tag table in `participants/04-vision/VISION-GUIDE.md` §3; then regenerate the layout JSON.
7. Rebuild the manual, run `run-all.sh`, re-render the figures, rebuild the PDF, and record the change in `design/REVISION-LOG.md`.

During an event, rule changes reach squads as Team Updates (`moderation/ORGANIZER-GUIDE.md` §4). Reports and change requests are easiest to act on when they cite a rule number (G412), a manual section (Section 4.5.4), a glossary term, a ledger row in the Field CAD Package §10, or a constant in `generate_drawings.py`.
