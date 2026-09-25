# Verification suite

Four checks that hold the package together. Run them after any edit; run them
before publishing anything.

```bash
bash verify/run-all.sh
```

That rebuilds the compiled manual and all six drawing sheets first, then runs
all five checks. To run one on its own, invoke it from anywhere — each script
locates the package relative to its own path:

```bash
python verify/verify.py
```

| Script | What it proves |
|---|---|
| `verify.py` | The **numbers**. All 26 AprilTag poses against the manual's table, 180° rotational symmetry, every tag-to-target transform in the vision guide, HEADWALL rung positions and tag-panel clearance behind plane P, the CRAG tag occlusion budget, DEPOT channel fit, every published robot standoff and reach, socket tube clearances and CELL protrusion, the rung stagger's no-common-band property and inter-lane gaps, scoring ceilings by piece type, RP threshold reachability, the Championship EXPEDITION requirement sets, piece accounting, and CENTER CACHE haul balance between ALLIANCES. |
| `consist.py` | The **cross-references**. Every `Gxxx`/`Rxxx` cited in the manual is defined, every rule band is numbered without gaps or duplicates, every `Section N.M` reference resolves to a real heading, every ALL-CAPS term used in the body has a glossary entry, no superseded value from an earlier revision survives anywhere in the package **including the drawing set and the generator**, and every sentence that restates a load-bearing rule outside its own definition still carries the qualifier that makes the rule mean what it means. |
| `crossdoc.py` | **Cross-document agreement.** `consist.py` asks whether a superseded value survives; this asks whether a value that must appear in several documents actually appears in all of them. A fix can be applied correctly in one place and simply never written in another, and no stale-text scan can see that — the absence looks like clean text. |
| `svg_collide.py` | The **drawing layout**. Estimates a bounding box for every unrotated `<text>` element in all six sheets and reports overlapping pairs and text escaping the sheet. A dimension that lands on top of a label is a dimension somebody guesses. |
| `svg_geom.py` | The **drawing geometry**. Decodes SVG pixels back through each view's px/in scale to field inches and compares against the ledger: plan rectangles stay on the carpet, both BASECAMPS and all four OUTFITTER lanes land where the spec puts them, and the socket tubes in the CRAG elevations lean the right way (bottoms at 4.50 in and 6.19 in outboard of their faces). |

## The restatement check

Three of the worst defects this package ever had were one shape: a rule or a
dimension corrected where it is *defined*, and left stale in one of the places
that *restates* it. G416 was stated three different ways across three documents;
the rung stagger four ways. Nothing structural caught either, because every
document was internally coherent — the contradiction only existed between them.

`consist.py` now keeps a small table of load-bearing rules and the phrases their
restatements must carry (G416: `CLIMB LINE` and `not driven`; G415: `borne by`;
G501: `MAJOR FOUL`). Any sentence elsewhere in the package that cites the rule
*and states its test* — "may not", "unless", "must not" — must contain them.
Rationale, cross-references and the term's own glossary row are excluded.

Add a rule to that table whenever a fix has to land in more than one document.

## Why these five

Each catches a class of defect the others structurally cannot. `verify.py`
checks arithmetic but every individual number can be right while a *rule* is
wrong — hence the set-theoretic EXPEDITION model it now carries. `consist.py`
catches text that stopped agreeing with the spec. The two SVG checks exist
because the drawing sheets are what entrants model from, and a sheet can be
internally beautiful and still say the wrong thing: both classes it tests for
(a mirrored rectangle anchored at the wrong edge, a tube rotated the wrong way)
shipped in v2.0 and were invisible to every text-level check.

A check that reports noise gets ignored, so each is tuned to be quiet when the
package is correct: `consist.py` skips `REVISION-LOG.md` when scanning for
stale values, because the log quotes superseded text on purpose, and
`svg_collide.py` skips rotated text rather than mismodelling its transform.

## Adding a check

Put it here, make it print `PASS`/`FAIL` lines and a `RESULT: n failure(s)`
tail, and add it to the loop in `run-all.sh`. The bar for adding one: a defect
got through, and no existing check could have caught it.
