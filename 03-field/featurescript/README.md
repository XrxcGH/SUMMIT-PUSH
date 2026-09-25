# SUMMIT PUSH — Onshape FeatureScript field generator

`SummitPushField.fs` is a single Onshape Feature Studio that builds the complete SUMMIT PUSH field
from this package: every field element, tape line, AprilTag and SUPPLY, in the package's
always-blue-origin NWU frame, with the names, colours, materials and densities of
`03-field/MATERIALS-AND-COLORS.md`. Every CRITICAL dimension in `03-field/FIELD-CAD-PACKAGE.md`
comes from the constants in `src/20_ledger.fs`, and every one is measured again after the build.

## Install and use (no Onshape API calls needed)

1. In an Onshape document, create a **Feature Studio** (＋ → Create Feature Studio).
2. Replace its contents with `SummitPushField.fs` and commit (the Studio targets FeatureScript
   **2960**, the May 2026 standard library; Onshape will offer to update it — accept or not, either works).
3. Open a **Part Studio**. The toolbar now has **SUMMIT PUSH Field** and **SUMMIT PUSH Game Piece**
   (they are in the custom-features menu if the toolbar is full). Add **SUMMIT PUSH Field** and
   click ✓. The Part Studio origin is the right corner of the Blue alliance wall; +X runs toward
   Red, +Y to the left from Blue, +Z up; units are inches.
4. With **Run dimension self-check** on (the default), the feature measures what it built against the
   master dimension ledger and reports `SUMMIT PUSH self-check: all N dimension checks pass`, or a
   warning with every failure listed in the FeatureScript console.

Pasting code into a Feature Studio is ordinary document editing; it does not use the Onshape REST
API allocation.

### Feature options

| Option | Default | Builds |
|---|---|---|
| Carpet, guardrails and FIELD LEDs | on | carpet (top at Z 0), both 20-in guardrails with 2 × 1 frame, polycarbonate bays, and the four 324-in FIELD LED segments |
| Alliance walls, driver stations, OUTFITTERS | on | both 78-in walls (solid to 39, glazed to 78), three driver-station shelves with E-STOP / A-STOP each, four OUTFITTER chutes with ramp, cheek funnels and leg |
| CRAGS and BASE DEPOTS | on | both CRAGS: tower, spire, SUMMIT BEACON lantern, tier rings, kick-guard, Shelf 1/2 with slot fences and gussets, 4 side sockets + Summit Socket with brackets/mast, 6 pegs with High Peg bosses, 8 flush tag pockets, and the U-shaped BASE DEPOT (floor, lip, entry chamfer) |
| HEADWALLS | on | both HEADWALLS: 3 independent lanes of uprights, rails and rung carriers, 9 rungs with end brackets, lower crossbeam, tag wedges |
| Tape | on | BASECAMP, CLIMB LINE (dashed outside BASECAMP), OUTFITTER LANES, CRAG APRONS, FIELD centerline, CENTER CACHE band and 9 marks, 6 alliance staging marks |
| AprilTag panels / 36h11 decals | on / on | 26 panels at their published poses, each carrying its 36h11 pattern as split, painted faces |
| Staged SUPPLIES | on | 9 CENTER CACHE pieces (Latin square) and 12 on the alliance staging marks |
| OUTFITTER stock | on | 7 of each type per alliance behind the walls (42 pieces) |
| CRAG tier rings and SUMMIT BEACON | Unlit | *Lit* paints all rings and beacons in alliance colour (the "fully lit mountain") |
| FIELD LED state | Dark | Green / White (FORECAST) / alliance colour (ROUTE) |
| Pieces on each alliance staging mark | Side by side | *Stacked* puts both pieces on the mark centre |
| Run dimension self-check | on | the measurement pass described above |

**SUMMIT PUSH Game Piece** places one CACHE CRATE, O2 CELL or ROPE COIL at the origin (optionally
resting on the Top plane) with its official colour and weight — for robot Part Studios.

## Materials and mass

Every body carries a material. Structure uses nominal densities for the material named in
MATERIALS-AND-COLORS §2; tubes modelled as solid bars use an *effective* density scaled by the tube's
wall-area fraction, so their mass is right. SUPPLIES get the density that makes each piece weigh
exactly its published weight, computed from its modelled volume at regeneration.

| Material key | Name in Onshape | Density (kg/m³) | Used for |
|---|---|---|---|
| plywood | Plywood, painted | 600 | CRAG panels, shelves, wall panels, DEPOT, OUTFITTER cheeks and leg, station shelves |
| hardwood | Hardwood (maple), painted | 705 | slot fences |
| uhmw-ply | UHMW-faced plywood | 650 | OUTFITTER chute ramps |
| aluminum | Aluminum 6061 | 2700 | socket tubes and brackets, gussets, kick-guard, tag wedges |
| steel | Steel, mild | 7850 | rungs, pegs, High Peg bosses, rung end brackets |
| polycarbonate | Polycarbonate | 1200 | glazing, SUMMIT BEACON lantern |
| acrylic | Acrylic (PMMA), frosted | 1190 | tier rings, FIELD LED lenses |
| tape | Gaffer tape | 830 | all tape (2 in × 0.01 in) |
| tag | Printed vinyl on rigid PVC backer | 1400 | AprilTag panels |
| abs | ABS, molded | 1050 | E-STOP / A-STOP |
| carpet | Event carpet, low pile | 220 | carpet (0.25 in thick, below Z 0) |
| al-tube-2x1 | Aluminum 2 × 1 × 0.125 tube (effective solid) | 928.1 | guardrail rails and posts |
| steel-tube-2x2 | Steel 2 × 2 × 0.120 tube (effective solid) | 1771 | HEADWALL lane frames and lower crossbeam, Summit Socket mast |
| steel-frame | Steel 2 × 1.25 × 0.083 tube (effective solid) | 1608 | alliance-wall frame |

| SUPPLY | Modelled volume | Density set | Mass |
|---|---|---|---|
| CACHE CRATE | 1901.8 in³ | 29.1 kg/m³ | 2.000 lb |
| O2 CELL | 248.7 in³ | 166.9 kg/m³ | 1.500 lb |
| ROPE COIL | 115.7 in³ | 239.3 kg/m³ | 1.000 lb |

The modelled field weighs about 3,930 lb in total.
