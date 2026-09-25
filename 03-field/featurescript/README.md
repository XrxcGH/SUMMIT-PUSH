# SUMMIT PUSH — Onshape FeatureScript field generator

`SummitPushField.fs` is a single Onshape Feature Studio that builds the SUMMIT PUSH field: every
field element, tape line, AprilTag panel and SUPPLY, in the package's always-blue-origin NWU
frame, with the names, colors, materials and densities of `03-field/MATERIALS-AND-COLORS.md`.
Its dimensions are the constants in `src/20_ledger.fs`, taken from `03-field/FIELD-CAD-PACKAGE.md`;
after building, the feature measures the geometry and compares it with those constants.

`SummitPushField.fs` is generated from `src/*.fs` by `build.py`. `AUTHORING.md` explains how the
sources are organized, the rules they follow, and the off-line OpenCascade build used to verify
them.

## Install and use

No Onshape API calls are needed: pasting code into a Feature Studio is ordinary document editing.

1. In an Onshape document, create a **Feature Studio** (＋ → Create Feature Studio).
2. Replace its contents with `SummitPushField.fs` and commit. The Studio targets FeatureScript
   version 2960 (the May 2026 standard library); if Onshape offers to update the version, either
   choice works.
3. Open a **Part Studio**. The toolbar now has **SUMMIT PUSH Field** and **SUMMIT PUSH Game Piece**
   (in the custom-features menu if the toolbar is full). Add **SUMMIT PUSH Field** and click ✓.
   The Part Studio origin is the right corner of the Blue alliance wall; +X runs toward Red, +Y to
   the left as seen from Blue, +Z up; units are inches.
4. With **Run dimension self-check** on (the default), the feature status reads
   `SUMMIT PUSH self-check: all N dimension checks pass`, or a warning giving the number of
   failed checks, each of which is printed in the FeatureScript console. A roundover or AprilTag
   decal that could not be applied is reported in the same status.

### Feature options

| Option | Default | Builds |
|---|---|---|
| Carpet, guardrails and FIELD LEDs | on | carpet (top at Z 0); both 20-in guardrails, a 2 × 1 tube frame with polycarbonate bays; the FIELD LED band in each top rail, split at X 324 into two alliance segments of three blocks, each block followed by a dark gap |
| Alliance walls, driver stations, OUTFITTERS | on | both 78-in walls (solid to Z 39, glazed to 78) on a welded steel frame; three driver-station shelves, each with an E-STOP and an A-STOP; four OUTFITTER chutes, each with a throat liner through the wall, a ramp, cheeks, funnel wings and a leg |
| CRAGS and BASE DEPOTS | on | both CRAGS: tower, spire, SUMMIT BEACON lantern, kick-guard, Shelf 1 and Shelf 2 with slot fences and gussets, four side sockets with brackets, the Summit Socket on its mast, six pegs (the High Pegs on root bosses), eight flush tag pockets; each CRAG's U-shaped BASE DEPOT (floor, lip, entry chamfer) |
| HEADWALLS | on | both HEADWALLS: three welded lane frames (uprights, rails, rung carriers), nine rungs with end brackets, the lower crossbeam with its standoffs, three tag wedges |
| Tape | on | BASECAMP, CLIMB LINE (dashed outside BASECAMP), OUTFITTER LANES, CRAG APRONS, FIELD centerline, CENTER CACHE band |
| AprilTag panels / 36h11 decals | on / on | 26 panels at their published poses; the decal option paints each panel's 36h11 pattern onto its face, split into cells |
| Staging: CENTER CACHE and staging marks with their SUPPLIES | on | the 9 CENTER CACHE marks and 6 alliance staging marks, with 9 CENTER CACHE pieces (Latin square) and 12 pieces on the alliance marks |
| OUTFITTER stock | on | 7 of each type per alliance behind the walls (42 pieces) |
| CRAG tier rings and SUMMIT BEACON | Unlit | *Lit* paints every tier ring and beacon in alliance color (all CAMPS established) |
| Cosmetics layer (tier rings) | on | off leaves out the tier rings; the tower and spire faces stay flush |
| FIELD LED state | Dark | Green, White (FORECAST: WHITEOUT / ICEFALL / GALE light 1 / 2 / 3 blocks) or Alliance color (each alliance's declared ROUTE: LOW / MID / HIGH light 1 / 2 / 3 blocks) |
| Pieces on each alliance staging mark | Side by side | *Stacked* puts both pieces on the mark center |
| Group each element into a composite part | on | one open composite part per element, so the parts list reads as the element list; SUPPLIES stay individual parts |
| Run dimension self-check | on | the measurement pass described above |

**SUMMIT PUSH Game Piece** places one CACHE CRATE, O2 CELL or ROPE COIL at the origin, optionally
resting on the Top plane, with its official color and weight, for use in robot Part Studios.

Parts are named `<ALLIANCE> <ELEMENT> <part>`, for example `BLUE CRAG Low Peg (guardrail side)`;
where several parts share a name they are numbered ` 1`, ` 2`, … in creation order.

## Materials and mass

Every body carries a material. Structure uses a nominal density for the material that
MATERIALS-AND-COLORS §2 names. Tubes modeled as solid bars use an *effective* density, scaled by
the tube's wall-area fraction, so that their mass is right. Each SUPPLY gets the density that
makes it weigh exactly its published weight, computed from its modeled volume during
regeneration.

| Material key | Name in Onshape | Density (kg/m³) | Used for |
|---|---|---|---|
| plywood | Plywood, painted | 600 | CRAG panels, shelves, wall panels, BASE DEPOT, OUTFITTER cheeks, funnel wings and leg, station shelves |
| hardwood | Hardwood (maple), painted | 705 | slot fences |
| uhmw-ply | UHMW-faced plywood | 650 | OUTFITTER chute ramps |
| aluminum | Aluminum 6061 | 2700 | socket tubes and brackets, gussets, kick-guard, OUTFITTER throat liners, tag wedges |
| steel | Steel, mild | 7850 | rungs, pegs, High Peg root bosses, rung end brackets |
| polycarbonate | Polycarbonate | 1200 | glazing, SUMMIT BEACON lantern |
| acrylic | Acrylic (PMMA), frosted | 1190 | tier rings, FIELD LED lenses |
| tape | Gaffer tape | 830 | all tape (2 in × 0.01 in) |
| tag | Printed vinyl on rigid PVC backer | 1400 | AprilTag panels |
| abs | ABS, molded | 1050 | E-STOP and A-STOP buttons |
| carpet | Event carpet, low pile | 220 | carpet (0.25 in thick, below Z 0) |
| al-tube-2x1 | Aluminum 2 x 1 x 0.125 tube (effective solid) | 928.1 | guardrail rails and posts |
| steel-tube-2x2 | Steel 2 x 2 x 0.120 tube (effective solid) | 1771 | HEADWALL lane frames and lower crossbeam, Summit Socket mast |
| steel-frame | Steel 2 x 1.25 x 0.083 tube (effective solid) | 1608 | alliance-wall frame |

| SUPPLY | Modeled volume | Density set | Mass |
|---|---|---|---|
| CACHE CRATE | 1901.8 in³ | 29.1 kg/m³ | 2.000 lb |
| O2 CELL | 248.7 in³ | 166.9 kg/m³ | 1.500 lb |
| ROPE COIL | 115.7 in³ | 239.3 kg/m³ | 1.000 lb |

The modeled field weighs about 3,960 lb, of which the 63 SUPPLIES are 94.5 lb.
