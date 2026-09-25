# Verification suite

The verification suite is five scripts that check the SUMMIT PUSH documents, drawing sheets and AprilTag layout against each other and against the design specification. They need bash and Python 3 (standard library only). Run the suite after any edit and before publishing anything:

```bash
bash verify/run-all.sh
```

`run-all.sh` first rebuilds `02-manual/GAME-MANUAL.md` (with `02-manual/build.sh`) and the six drawing sheets (with `03-field/renderings/generate_drawings.py`), then runs `verify.py`, `consist.py`, `crossdoc.py`, `svg_collide.py` and `svg_geom.py`, in that order. Each script can also be run on its own, from any directory, because it locates the package relative to its own path:

```bash
python verify/verify.py
```

A script run on its own checks the files as they are. It does not rebuild the manual or the drawings, so run the build first if you changed a manual section or the generator.

The FeatureScript field generator in `03-field/featurescript/` has its own build and checks (see its `README.md` and `AUTHORING.md`). `run-all.sh` does not run them.

## Reading the results

The scripts report failures in their output, not in their exit status: each one exits 0 whether its checks pass or fail, and exits non-zero only if it stops with an error. The last line of `run-all.sh` ("all checks ran ..." or "a check exited non-zero ...") therefore says only whether every script ran to completion. Read each script's summary:

| Script | Clean result | What a failure looks like |
|---|---|---|
| `verify.py` | `RESULT: 0 failure(s)` | A `FAIL` line with the computed value. Failed checks are listed again after the `RESULT` line. |
| `consist.py` | `DANGLING rule refs: none`, `DANGLING section refs: none`, no band marked `<-- GAP/DUP`, `... with no glossary entry: 0`, every restated rule `ok`, and every `STALE` line `CLEAN` | The count, followed by the offending items with file and line. |
| `crossdoc.py` | `RESULT: 0 failure(s)` | A `FAIL` line naming the documents that lack the value or still carry the stale wording. |
| `svg_collide.py` | `TOTAL layout issues: 0` | `OVERLAP`, `OFF-SHEET`, `HIDDEN`, `CROSSES`, `SMALL`, `LEADER` or `ARROWHEAD` lines under the sheet's summary line. |
| `svg_geom.py` | `RESULT: 0 failure(s)` | A `FAIL` line with the decoded values. |

`consist.py` also writes its report to `verify/consist.txt`.

## What each script checks

| Script | Checks |
|---|---|
| `verify.py` | **Numbers.** All 26 AprilTag positions in the JSON against the manual's tag table; 180° rotational symmetry of the layout; pure-yaw, unit-norm quaternions; the vertical tag-to-target offsets used in the vision guide; HEADWALL rung positions and tag-panel clearance behind plane P; the CRAG tag occlusion budget, including the camera-height table for an upright O2 CELL; shelf gusset floors; CACHE CRATE clearance in the shelf slots; DEPOT channel fit and every published ROBOT standoff and reach; socket tube clearances and CELL protrusion; the rung stagger (no lateral position engages two successive rungs; spacing between lanes) and the rung tables in the manual and the CAD package; climb reach from the CLIMB LINE; scoring ceilings by piece type; RP threshold reachability; the Championship EXPEDITION requirement sets; the ROPE COIL profile; piece accounting; and CENTER CACHE haul balance between ALLIANCES. |
| `consist.py` | **Cross-references and superseded values.** Every G or R rule cited in the compiled manual is defined; each rule band is numbered without gaps or duplicates; every `Section N.M` reference resolves to a heading; every ALL-CAPS term used three or more times in the manual body has a glossary entry; restated rules keep their qualifiers (see below); and no superseded value from an earlier revision survives in the scanned files. |
| `crossdoc.py` | **Cross-document agreement.** `consist.py` looks for superseded values that survive. `crossdoc.py` checks the opposite case: that a value required in several documents appears in each of them. A fix applied in one document and never written in another leaves no stale text for `consist.py` to find. Each row of its table names a value, the documents that must carry it, and any stale wording that must be gone from them. A second list checks the drawing sheets for notes that contradict the documents. |
| `svg_collide.py` | **Drawing layout.** Models every `<text>` element on the six sheets as a box, transforms included, at the printed plate size (21 in wide), and samples the outline of every drawn shape. Reports text that overlaps other text, runs off the sheet, is painted over by a later shape, or has a line, arrowhead or panel border running through it; text below 7 pt (8 pt for dimension values and bold labels); callout leaders that cross each other or a dimension line, lack a label, or put the arrowhead at the label end; and arrowheads under 3 pt. |
| `svg_geom.py` | **Drawing geometry.** Decodes SVG coordinates back to field inches through each view's scale and compares them with the ledger: plan rectangles stay on the carpet; both BASECAMPS and all four OUTFITTER lanes are where the specification puts them; the socket tubes in the CRAG elevations lean outward, with bottoms 4.50 in (side sockets) and 6.19 in (Summit Socket) outboard of their faces; and the HEADWALL sheet draws nine 20.0-in rungs with the same stagger in every lane, 48 in between adjacent lanes, and a 6.43-in setback per rung. |

Most `verify.py` checks recompute a published figure from inputs written into the script, so a change to one of those figures means updating the script as well as the documents. The tag positions and the two rung tables are parsed from the documents themselves.

`consist.py` scans every Markdown file, every SVG sheet, and `generate_drawings.py`, except `REVISION-LOG.md` and the `00-concepts/` and `00-research/` archives. The glossary check counts singular, plural and possessive forms, and a short allow-list in the script covers acronyms and names that are not defined terms.

## The restatement check

A rule or dimension corrected where it is defined can stay stale where another document restates it. Each document is then consistent on its own and the contradiction exists only between documents, so no structural check can see it. G416 and the HEADWALL rung stagger both went wrong this way (`REVISION-LOG.md` M2, M21 and M37).

`consist.py` keeps a table (`RESTATED`) of load-bearing rules and the phrases their restatements must contain:

| Rule | Required phrases |
|---|---|
| G416 | `CLIMB LINE`, `took hold of` |
| G415 | `borne by` |
| G501 | `MAJOR FOUL` |

A sentence counts as a restatement when it cites the rule number in bold Markdown, states a test ("may not", "unless" or "must not"), and is at least 120 characters long. Such a sentence must contain every phrase listed for the rule. Shorter sentences, and sentences that cite the rule without stating a test (rationale and cross-references), are not checked, and a glossary row does not have to repeat its own headword. The compiled `GAME-MANUAL.md` is skipped; its source sections are scanned like any other file. This README is scanned too, so it describes the pattern instead of quoting it.

Add a rule to the table whenever a fix has to land in more than one document.

## Why five checks

Each script catches a class of defect the others cannot. `verify.py` checks arithmetic, but every number can be right while a rule is wrong; that is why it also models the Championship EXPEDITION requirement as sets of CRAG positions. `consist.py` finds text that has stopped agreeing with the specification, and `crossdoc.py` finds a required value that never reached a document. The two SVG checks exist because entrants model from the drawing sheets, and a sheet can be internally consistent and still wrong: a mirrored rectangle anchored at the wrong edge, or a socket tube rotated the wrong way, passes every text-level check.

## Keeping the checks quiet

A check that reports noise gets ignored, so each is tuned to report nothing when the package is correct:

- `consist.py` does not scan `REVISION-LOG.md`, because the log quotes superseded text on purpose, or the `00-concepts/` and `00-research/` archives, which were written before the specification.
- `svg_collide.py` does not count a line drawn under a white text halo or inside a boxed CRITICAL value, because the halo or box covers it on the printed sheet.

## Adding a check

- A value has been superseded: add a pattern to `STALE` in `consist.py`.
- A value must appear in several documents: add a row to `ROWS` in `crossdoc.py`.
- A rule is restated in several documents: add it to `RESTATED` in `consist.py`.
- A new class of defect: add a script to this directory that prints `PASS`/`FAIL` lines and ends with a `RESULT: n failure(s)` line, and add it to the loop in `run-all.sh`. Add a script only when a defect got through that no existing check could have caught.
