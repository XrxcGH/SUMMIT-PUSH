# SUMMIT PUSH — Review & Revision Progress

Status tracker for the revision passes. Every substantive change is itemized
with its reasoning in `REVISION-LOG.md`: sections A–I cover v1.0 → v2.0,
J covers a self-review of v2.0, K and L cover the adversarial re-audit of v2.0
that produced v2.1, and M covers a third pass that audited those fixes and
produced v2.2.

**Current version: v2.2.**

## Workstreams

| # | Workstream | Status |
|---|---|---|
| 1 | Editorial: de-brand, de-team, third-person professional voice | DONE |
| 2 | Geometry fixes (depot, sockets, Summit Socket, beacon, HEADWALL, chute, apron) | DONE |
| 3 | Rules coherence + completeness (G/R rules, tournament, glossary) | DONE |
| 4 | AUTO / TELEOP / ENDGAME depth + balance | DONE |
| 5 | Materials / colors / naming specification | DONE — `03-field/MATERIALS-AND-COLORS.md` |
| 6 | SVG drawing sheets: regenerated from the dimension ledger | DONE — `03-field/renderings/generate_drawings.py` |
| 7 | Vision guide + AprilTag JSON alignment | DONE |
| 8 | Manual typesetting and formatting guide (for the later PDF edition) | DONE — `06-style/MANUAL-STYLE-GUIDE.md` |
| 9 | Cross-document consistency sweep | DONE — 0 failures |
| 10 | Adversarial re-audit of v2.0 and its findings | DONE — `REVISION-LOG.md` §K, §L |
| 12 | Third pass: audit of the v2.1 fixes themselves | DONE — `REVISION-LOG.md` §M |
| 11 | Verification suite moved into the package | DONE — `_verify/` |

## Build and verification

```bash
bash _verify/run-all.sh
```

That rebuilds `02-manual/GAME-MANUAL.md` and all six drawing sheets, then runs
the five checks described in `_verify/README.md`. To rebuild without checking:

```bash
bash 02-manual/build.sh
python 03-field/renderings/generate_drawings.py
```

The suite currently reports **0 failures** across all five checks: 0 numeric
failures, 0 dangling rule or section cross-references (89 rule IDs, 77 numbered
sections), 0 ALL-CAPS terms in the manual body without a glossary entry, 0 superseded
values anywhere outside the revision log, 0 text collisions across the six
drawing sheets, and every decoded drawing dimension matching the ledger.

## How to send changes

Feedback can name any of:
- a rule number (`G412`), a section (`§4.5.4`), or a glossary term;
- a ledger row in `03-field/FIELD-CAD-PACKAGE.md` §10;
- a constant at the top of `03-field/renderings/generate_drawings.py`.

Editing order for a geometry change: DESIGN-SPEC → FIELD-CAD-PACKAGE ledger →
manual section → generator constant → regenerate drawings → regenerate the tag
JSON if tag poses moved → rebuild the manual → `bash _verify/run-all.sh`.

## Notes
- `02-manual/GAME-MANUAL.md` is COMPILED output. Edit `02-manual/sections/*.md`.
- `04-vision/apriltag-field-layout.json` is GENERATED from the locked tag table.
- The SVGs are build output. Edit the generator, not the SVGs.
- The PDF edition has not been produced yet. `06-style/MANUAL-STYLE-GUIDE.md`
  specifies how it should look when it is.
