# SUMMIT PUSH — Field Element CAD Package

**Document:** `03-field/FIELD-CAD-PACKAGE.md` · **Rules authority:** the Game Manual (`01-game-manual/`) · Version 2.2

**Audience:** CAD modelers building the complete field. Every element is fully dimensioned here and in the drawing set (`03-field/drawings/`), so no length or angle has to be guessed. Appearance (material, color, finish) is specified in `03-field/MATERIALS-AND-COLORS.md`.

## 0. Conventions

- **Units:** inches unless noted. **Coordinate frame:** always-blue-origin NWU, with the origin at the right corner of the Blue alliance wall (from Blue's perspective), +X toward the Red wall, +Y left, +Z up. The field carpet is **648 in × 324 in**; guardrails are **20 in** tall; the centerline is at X = 324; field center is (324, 162). The layout is 180° rotationally symmetric about field center: **model the Blue half once, then rotate-pattern it 180° about (324, 162)**.
- **CRITICAL** flags a robot-interaction dimension: hold it exactly, to the tolerance where one is given. **(ref)** marks reference geometry that may float ±0.25 in without gameplay effect.
- Every angle on the field is **15°, 30°, or 45°**. Any other angle in the model is an error.
- **Heights are to the robot-interaction surface**: shelf top surface, socket rim center, peg root, rung **top**, tag center.
- The drawing set in `03-field/drawings/` illustrates this document. Where a drawing and this text disagree, this text governs; report the drawing.

---

## 1. Field Assembly Overview

### 1.1 Placement coordinates (locked; from spec §3)

| Element | Position (center) | Footprint / span |
|---|---|---|
| BLUE CRAG | (324, 240) | 48 × 48 in footprint, spire top 90 in; with its BASE DEPOT ring, an 81.5-in square, X 283.25–364.75, Y 199.25–280.75 |
| RED CRAG | (324, 84) | 48 × 48 in footprint, spire top 90 in; with its BASE DEPOT ring, an 81.5-in square, X 283.25–364.75, Y 43.25–124.75 |
| CENTER CACHE band | X 300–348, Y 108–216 | 9 taped marks, 3×3 grid, 24-in spacing, centered (324, 162) |
| BLUE HEADWALL | plane P crosses carpet at X = 48, Y 90–234 | 144 in wide, leaned 15° from vertical, top toward alliance wall, 3 × 48-in lanes |
| RED HEADWALL | X = 600, Y 90–234 | mirror |
| BLUE BASECAMP zone | X 0–48, Y 90–234 | taped zone (= HEADWALL ZONE) |
| RED BASECAMP zone | X 600–648, Y 90–234 | mirror |
| BLUE OUTFITTERS | chutes centered (0, 30) and (0, 294) | opening 30 W × 16 H, sill 24; lane 36 wide × 48 deep |
| RED OUTFITTERS | (648, 294) and (648, 30) | mirror |
| Alliance staging marks | Blue X = 144; Red X = 504 | marks at Y = 108 / 162 / 216 |
| SCREE | 18 SCREE PATCHES, 9 per half; centers in §1.4 | 30.0 × 30.0 in each, four ridges 1.75 in tall |

CRAG orientation: each CRAG's SHELF FACE faces its owning alliance wall (Blue CRAG shelf-face normal −X; Red +X), the PEG FACE faces the opponent wall, and the SOCKET FACES are the two ±Y side faces.

### 1.2 Taping plan (model tape as surface geometry)

All lines are 2-in tape geometry, with the line edge on the stated coordinate. Model tape as thin surface splines or decals so that renders match the manual and the zone rules are visible in screenshots.

| Marking | Color | Geometry |
|---|---|---|
| BASECAMP / HEADWALL ZONE boundary | alliance color | Blue: lines at X = 48 (Y 90–234) and Y = 90, Y = 234 (X 0–48); Red mirror. The wall closes the fourth side. |
| CLIMB LINE | alliance color, dashed outside BASECAMP | the X = 48 (Blue) / X = 600 (Red) line carried across the **full field width, Y 0–324**. Over Y 90–234 it coincides with the BASECAMP boundary (row above) and needs no second line; outside that band it is dashed and marks only the **G416** climb-entry plane. Without it, G416 would be a line call against an unmarked line on the open carpet beside BASECAMP, from which a ROBOT can reach lane 1's SUMMIT RUNG (Y 92). |
| OUTFITTER LANE (×4) | alliance color | 36 in wide, centered on the chute Y, extending 48 in into the field from the alliance wall |
| CRAG APRON (×2) | alliance color | offset **36 in** from the SHELF FACE and the PEG FACE and **20 in** from each SOCKET FACE (CRITICAL; the line call for the placement-protection rule), corners joined with 20-in-radius arcs tangent to both offset lines. No trim is applied: the two aprons and the staged CENTER CACHE all fit inside the 108-in corridor. The tape is laid inside the offset line, so its inner edge is 18.0 in off each SOCKET FACE; the BASE DEPOT ring lies inside it with only 0.25 in to spare along the SOCKET FACES and 0.16 in at the corner arcs (§3, APRON clearance check). |
| FIELD centerline | white | 2-in line at X = 324 running the full width, Y 0–324, broken where each CRAG and its BASE DEPOT ring cross it. The break runs between the inner edges of that CRAG's APRON tape, **Blue Y 198–282, Red Y 42–126**, so that no stub of line is left between the APRON tape and the DEPOT's entry chamfer (plan envelope Blue Y 198.25–281.75, Red Y 42.25–125.75). **G402** and **G502** are both line calls against it. |
| CENTER CACHE band | white | 48 × 108 in, X 300–348, Y 108–216. Its end edges coincide with the two CRAG SOCKET FACE planes, which lie under the BASE DEPOT rings, so no end lines are laid. Its two side lines (X 300–302 and X 346–348) stop, like the FIELD centerline, at the inner edges of the two APRON tapes, so they run Y 126–198. It is the reference marking for the **G402** AUTO exception; the outer 20 in at each end lie inside a CRAG APRON, whose tape governs there. |
| CENTER CACHE marks (×9) | white | 12-in "X" marks, 3×3 grid, 24-in pitch, centered (324, 162) |
| Alliance staging marks (×6) | white with alliance-color border | 12-in "X" at (144, 108/162/216) and (504, 108/162/216) |

**Apron corridor check (verify in CAD):** Blue's −Y socket-face apron occupies Y 196–216; Red's +Y socket-face apron occupies Y 108–128. The open corridor is Y 128–196 (68 in). The staged CENTER CACHE spans Y 131.5–192.5 across the crowned 13.0-in crate envelope, leaving 3.5 in of clearance at each end. No staged piece touches an apron, and the corridor is continuous through X 300–348, between the two CRAGS.

### 1.3 Perimeter and field lighting

- Guardrails: 20 in tall, transparent panel on a low frame of 2 × 1 in tube, along both long edges **(ref)**.
- **FIELD LED bands:** a 1.0-in-wide frosted LED band let into the top rail of each long-side guardrail, lens center **19.0 in** above the carpet, running the full 648 in and divided at X = 324 into two 324-in alliance segments. The section is **(ref)**; the 19.0-in height is CRITICAL only in that the band must clear the 20-in guardrail top.
- Alliance walls: full width, **78 in tall and 2.0 in thick throughout (ref)**; solid to Z = 39, glazed 39 → 78. Each wall has three driver stations, **96 in wide on 108-in centers (Y = 54 / 162 / 270)**, each with a 0.75-in shelf topping out at **36 in**, a window in the glazed band, and an E-STOP and an A-STOP button **(ref)**. The OUTFITTER chutes penetrate the wall at the coordinates above.

### 1.4 SCREE

SCREE is rough terrain on top of the carpet, laid in the open floor around each alliance's staging marks: **18 SCREE PATCHES**, nine per half, in a staggered, non-linear pattern. A ROBOT either drives over a patch, which is slow and a tip risk for a tall ROBOT with a raised or extended mechanism, or slows down and weaves between patches. SCREE is part of the FIELD: ROBOTS may drive over it, **G202** applies to it, and a SUPPLY that comes to rest on it stays in play and is not restaged (the Game Manual governs).

| Feature | Dimension | Status |
|---|---|---|
| Patch footprint | **30.0 × 30.0 in** square, sides parallel to the field axes, sitting directly on the carpet (no base plate) | CRITICAL |
| Ridges per patch | **4**, straight, running across the whole patch and cut square (vertically) at the patch boundary | CRITICAL |
| Ridge profile | half-round, **radius 1.75 in**: **1.75 in tall** and 3.5 in wide at the base, flat side on the carpet | CRITICAL |
| Ridge centerlines | **±4.0 and ±12.0 in** from the patch center, measured along the ridge normal: an **8.0-in pitch**, with 4.5 in of flat carpet between adjacent ridges | CRITICAL |
| Ridge direction | per patch (table below): **+45** = parallel to direction (1, 1), the line X = Y; **−45** = parallel to (1, −1); **Y** = parallel to the Y axis, across the main +X direction of travel | CRITICAL |
| Material | HDPE half-round rod fastened to the carpet, matte, color `scree` (`MATERIALS-AND-COLORS.md`) | (ref) |

**SCREE PATCH table (centers CRITICAL).** Red twin = (648 − x, 324 − y). A 180° rotation preserves line direction, so a Red patch has the same ridge direction as its Blue twin.

| Patch | Blue center | Blue footprint | Ridges | Red center (twin) |
|---|---|---|---|---|
| S1 | (105, 88) | X 90–120, Y 73–103 | +45 | (543, 236) |
| S2 | (105, 162) | X 90–120, Y 147–177 | Y | (543, 162) |
| S3 | (105, 236) | X 90–120, Y 221–251 | −45 | (543, 88) |
| S4 | (200, 37) | X 185–215, Y 22–52 | +45 | (448, 287) |
| S5 | (200, 125) | X 185–215, Y 110–140 | +45 | (448, 199) |
| S6 | (200, 199) | X 185–215, Y 184–214 | −45 | (448, 125) |
| S7 | (200, 287) | X 185–215, Y 272–302 | −45 | (448, 37) |
| S8 | (234, 108) | X 219–249, Y 93–123 | +45 | (414, 216) |
| S9 | (234, 216) | X 219–249, Y 201–231 | −45 | (414, 108) |

Each half is also mirror-symmetric about Y = 162: S1/S3, S4/S7, S5/S6 and S8/S9 are mirror pairs with opposite ridge directions, and S2 lies on the axis. Both OUTFITTERS of an alliance therefore face identical SCREE.

**Layout checks (verify in CAD).** These properties were checked numerically against the table; a model that disagrees with them is misplaced. Coordinates are Blue; Red is the 180° rotation.

- **Columns:** near column X 90–120 (S1–S3), far column X 185–215 (S4–S7), inner pair X 219–249 (S8, S9). The staging marks at X = 144 lie between the near and far columns.
- **Passable gaps**, through which a ROBOT can weave: 44.0 in (S1–S2, S2–S3, S5–S6), 58.0 in (S4–S5, S6–S7), 41.2 in corner to corner (S4–S8, S7–S9), and 65.4–68.3 in between the near and far columns.
- **Closed gaps:** 4.0 in (S5–S8, S6–S9, which read as two L-shaped clusters) and 22.0 in between S4 / S7 and the guardrail.
- **Flat ground kept clear of SCREE:** X 48–90 across Y 90–234 in front of the HEADWALL (42 in for squaring up to climb); a 36 × 24 in pad at each staging mark; each OUTFITTER LANE mouth (X 48–90); and X ≥ 252 up to the CRAG APRON line at X = 264. Red is mirrored: X 558–600 in front of its HEADWALL, and X ≤ 396 back to its APRON line at X = 384.
- **Non-linear:** one narrow corridor gives a clear straight path 28 in wide from the BASECAMP front to a CRAG approach: path centerline Y ≈ 175 at the BASECAMP front (X = 48; upper edge Y ≈ 189), running to the far (+Y) corner of the SHELF FACE approach at X = 264 (centerline Y ≈ 265–269), with about 0.4 in to spare over the 14 in of clearance each side of the centerline. Every other drivable straight 28-in path from an OUTFITTER LANE mouth or the BASECAMP front to the SHELF FACE or either SOCKET FACE approach crosses a patch, so every other cycle route must weave or cross SCREE.
- **Zones and tags:** SCREE lies outside every protected zone (the CRAG APRONS, the BASECAMP / HEADWALL ZONES and the OUTFITTER LANES) and outside the CENTER CACHE. It occludes no AprilTag: its ridges stand 1.75 in tall, and the lowest tag panel edge on the FIELD is at Z = 7.50 (the HEADWALL lane panels, §7).

**Robot interaction (reference).** A BUMPER with its bottom edge at 2.5 in, the top of the range **R403** allows, clears a ridge by 0.75 in on flat carpet and by about 0.5 in with a wheel riding a ridge; **R403** also allows a bottom edge as low as 1.25 in, which meets the ridges. Crossing SCREE needs at least 2.0 in of clearance under the whole frame and wheels of about 6 in or larger. Conventional swerve (3–4-in wheels, about 1.25–1.5 in of frame clearance) high-centers on it, so low-clearance ROBOTS, including a stock kit chassis, weave between the patches instead.

**CAD notes:** model each ridge as a half-round extrusion (R1.75 profile, flat side on the carpet) long enough to cross the patch at its offset and direction, then clip it to its 30 × 30 in patch square with a vertical cut. Model S1, S2, S4, S5 and S8, mirror S1, S4, S5 and S8 about Y = 162 for S3, S7, S6 and S9 (the mirror flips +45 to −45), then rotate-pattern the Blue half 180° about (324, 162) for Red. Robot-driving dims: **patch 30.0, ridge height 1.75 (R1.75), pitch 8.0, offsets ±4.0 / ±12.0, patch centers and ridge directions per the table**.

---

## 2. CRAG (×2)

A four-faced scoring structure, one per alliance, both on the centerline. All dimensions below appear on drawing sheets `crag.svg` (multi-view) and `field-top-view.svg` (placement).

### 2.1 Envelope

- **Tower body:** 48 × 48 in square footprint at carpet, rising to **60 in** (top plate).
- **Spire:** **20 × 20 in square prism (CRITICAL)**, centered on the tower's vertical axis, from **60 in to 90 in** overall height. The spire is a straight prism with no taper, so every published height is exact at every face.
- **SUMMIT BEACON lantern:** the top **12 in** of the spire (Z 78 → 90) is a translucent section with its luminous center at **84 in** (see §8). It is a section of the spire prism rather than an added dome, so the 90-in overall height is exact.
- Base perimeter kick-guard flush to carpet **(ref)**. All four faces are robot-facing scoring surfaces.
- **BASE DEPOT ring:** the tray (§3) surrounds the tower on all four faces, so in plan each CRAG with its DEPOT occupies an **81.5-in square** over the lip (83.5 in over the entry chamfer), centered on the CRAG.

### 2.2 SHELF FACE (faces the owning alliance wall)

| Feature | Dimension | Status |
|---|---|---|
| Shelf 1 top surface | **24 in** above carpet | CRITICAL |
| Shelf 2 top surface | **42 in** above carpet | CRITICAL |
| Slots per shelf | 3, each **14.0 in wide** | CRITICAL |
| Slot lateral centers | **−15.5 / 0 / +15.5 in** from the face centerline | CRITICAL |
| Slot fences | 4 per shelf, **1.5 in wide × 2.0 in tall**, at 0 / 15.5 / 31.0 / 46.5 in from the left face edge (4 × 1.5 + 3 × 14.0 = 48.0 exactly) | (ref) |
| Shelf depth (face to front edge) | **14.0 in** | CRITICAL (a 12-in CRATE is fully supported) |
| Shelf front-edge roundover | 0.25 in | (ref) |
| Shelf thickness | 0.75 in | (ref) |
| Shelf gusset envelope | free **(ref)** within the shelf's plan footprint, above an absolute floor stated per shelf (see Shelf gusset floors, below) | (ref) |

**Shelf gusset floors.** The shelf pitch is only 18.0 in (24 → 42), while a CACHE CRATE standing on a shelf reaches 13.0 in above it across its crown. A gusset envelope stated as an offset from the gusset's own shelf cannot express that constraint, so the floor is stated per shelf:

- **Under Shelf 2:** entirely above **Z = 38.0**. A crowned CRATE on Shelf 1 tops out at 37.0 (24.0 + 0.5 crown under + 12.0 cube + 0.5 crown over), which leaves 1.0 in of clearance and 3.25 in of gusset depth below the shelf's 41.25-in underside.
- **Under Shelf 1:** entirely above **Z = 19.0**, and above **Z = 22.0** within the vertical prisms over the two SHELF FACE tag panels (for Blue, Y 221.5–230.5 and Y 249.5–258.5, each ±4.5 in either side of a panel center), so that no gusset can stand in front of a CRAG tag. There is no lower band: Shelf 1's whole plan footprint (Blue X 286–300) sits inside the 16-in DEPOT channel (X 284–300), and SUPPLIES are pushed in beneath it. Z = 19.0 leaves 5.75 in over a crowned CRATE standing on the tray floor (top at Z = 13.25) and still allows a 4.25-in-deep gusset, which is ample for a 14-in cantilever carrying about 6 lb.

Neither floor is a CRITICAL dimension. Both are bounds on the (ref) gusset geometry, and the package's published clearances hold only if the gussets stay inside them.

The SHELF FACE also carries the Summit Socket (§2.4). The BASE DEPOT's SHELF FACE leg (§3) runs along its base, as a DEPOT leg does along every face.

### 2.3 SOCKET FACES (both ±Y faces; one Low Socket and one Mid Socket per face)

| Feature | Dimension | Status |
|---|---|---|
| Low Socket rim center height | **30 in** | CRITICAL |
| Mid Socket rim center height | **54 in** | CRITICAL |
| Socket lateral positions | rim centers at **±14.0 in from the face centerline**: Low Socket on the **shelf-face side** (−14.0), Mid Socket on the **peg-face side** (+14.0) | CRITICAL (each socket sits directly above one tag of the face's pair) |
| Rim-center standoff from face plane | **8.0 in**, measured normal to the face | CRITICAL |
| Tube axis tilt | **30° from vertical**, tilting **outward** (away from the face, in the vertical plane containing the face normal), open end up | CRITICAL |
| Tube inside diameter | **6.50 ± 0.125 in** | CRITICAL; the strictest tolerance on the field |
| Tube length along axis | **7.0 in** from the rim to the closed bottom's inner floor | CRITICAL (sets the 7.0-in protrusion of a seated 14-in CELL and the tag-occlusion budget of §7) |
| Tube wall and closed bottom | 0.09 in (the bottom lies beyond the 7.0-in bore: 7.09 in overall) | (ref) |

**Clearance check (verify in CAD):** with a 7.0-in bore at 30°, the tube's floor center lies 8.0 − 7.0·sin30° = **4.50 in** outboard of the face plane. The 0.09-in bottom takes the tube to 7.09 in overall, so its inboard edge is 8.0 − 7.09·sin30° − 3.34·cos30° = **1.56 in** outboard. Nothing penetrates the tower shell, so no relief pocket is required. The tube's lowest surface point is at **Z = 22.19** for a Low Socket, 0.63 in above the CRAG tag target's top edge (Z = 21.56), which stays unobstructed from a camera 10–20 in high (§7). A seated 14.0-in O2 CELL protrudes **7.0 in** along the axis. Its apex stands 7.0·cos30° = 6.06 in above the rim center, against the rim's uphill lip at 1.67 in, so the CELL clears the socket mouth by **4.39 in** and a SCORED call never requires looking down the tube.

**Robot standoff: both sockets on a face are reached across the BASE DEPOT.** The DEPOT's SOCKET FACE leg (§3) runs the full 48-in length of each SOCKET FACE, and both sockets stand directly above it. A ROBOT servicing either socket therefore parks against the leg's outer lip: the lip outer face is 16.75 in off the face, the BUMPER face is there, and the FRAME PERIMETER is 3.0 in behind it at **19.75 in**, so each rim (8.0 in outboard of the face) is **11.75 in of horizontal extension** away, the same for the Low Socket and the Mid Socket (reach table in §3). Both tubes overhang the leg, and a SUPPLY cannot be dropped into the tray where a tube overhangs it (§3, open-to-sky check). Model the SOCKET FACE leg and both sockets together.

The tube attaches to the face below the rim by a bracket, a gusset, or a pocket let into the face. The attachment geometry is free **(ref)** provided no part of it breaks the rim plane (the plane through the rim, normal to the tube axis) or projects outboard of the tube's own silhouette. The wedge under the tube is the natural place for it.

### 2.4 Summit Socket (×1 per CRAG, on the SHELF FACE)

| Feature | Dimension | Status |
|---|---|---|
| Rim center height | **72 in** | CRITICAL |
| Rim center lateral | **on the CRAG's centerline** (zero lateral offset) | CRITICAL |
| Rim-center standoff from the SHELF FACE plane | **8.0 in**, measured normal to the face | CRITICAL |
| Tube axis tilt | **15° from vertical**, tilting outward toward the owning alliance, open end up | CRITICAL |
| Tube ID / bore length / wall and bottom | **6.50 ± 0.125 in** / **7.0 in** / 0.09 in | CRITICAL / CRITICAL / (ref) |
| Support | a mast rising from the tower top plate within **4.0 in** of its shelf-face edge and leaning outward to the tube's closed bottom (floor center 6.19 in outboard, Z = 65.24); above **Z = 62** no part may lie outside the socket's plan silhouette plus 2.0 in | (ref) |

There is **no spire recess**. The spire is a clean prism, and the Summit Socket is carried on a mast off the tower top plate, with its rim 12 in above that plate. It does not cantilever off the SHELF FACE, which ends at the 60-in top plate; the spire's own face is 14 in inboard of it.

**Clearance checks (verify in CAD):**
- Tube floor center: 8.0 − 7.0·sin15° = **6.19 in** outboard of the face plane, at Z = 72 − 7.0·cos15° = **65.24 in**. With the 0.09-in bottom beyond it, the inboard edge is 8.0 − 7.09·sin15° − 3.34·cos15° = **2.94 in** outboard, so the tube is entirely in free air outboard of the tower.
- A crowned CACHE CRATE on Shelf 2 tops out at **Z = 55.0** and reaches X out to the shelf front edge. The tube's lowest point is at Z = 64.29, which gives **9.29 in** of clearance. Over that shelf, the binding overhead constraint is the mast (next item).
- A seated CELL's apex is at Z = 72 + 7.0·cos15° = **78.76 in**, 5.90 in above the rim's uphill lip, and is visible from the owning alliance's driver stations.
- **The socket and its mast stand in plan over Shelf 2's center slot** (X 286.8–299.0 × Y 234.7–245.3 on the Blue CRAG, against a center slot of X 286–300 × Y 233–247). The mast rises from the tower top plate at Z = 60 and a crowned CRATE on Shelf 2 tops out at Z = 55.0, so that slot has **5.0 in** of overhead clearance. It cannot be loaded by a vertical drop or an over-the-top gripper and must be loaded from the front. Shelf 2's two outer slots (Y centers ±15.5) stay open to the sky. Publish this restriction; no other slot on the CRAG has it.
- Robot reach: a robot with its bumpers against the DEPOT lip has its FRAME PERIMETER 19.75 in from the shelf face plane, so the rim is **11.75 in** of horizontal extension away, inside the 18-in limit (reach table in §3). The limiting requirement is the 72-in lift.

### 2.5 PEG FACE (faces the opponent wall)

| Feature | Dimension | Status |
|---|---|---|
| Low Peg roots (×2) | height **30 in**, lateral **±14.0 in from face centerline** | CRITICAL |
| Mid Peg roots (×2) | height **54 in**, lateral **±14.0 in** | CRITICAL |
| High Peg roots (×2) | height **78 in** on the spire's peg face, lateral **±7.0 in from the spire centerline** (14.0 in apart) | CRITICAL |
| Peg outside diameter | **1.5 in** | CRITICAL |
| Peg angle | **45° upward** from the face, in the vertical plane containing the face normal | CRITICAL |
| Peg exposed length | **10.0 in** along the peg axis, rounded tip (0.75-in spherical radius) | CRITICAL |
| Peg root fillet | 0.25 in at the face | (ref) |

**ROPE COIL rest pose (model this; it defines every hook and spear end effector).** The coil is a torus: core radius 3.75 in, tube radius 1.25 in (10.0 OD, 5.0 hole, 2.5 tube). Dropped over a 1.5-in peg, it can tilt up to acos(2.0/3.75) = **57.8°** away from perpendicular-to-the-peg before the peg binds inside the ring, the point where the peg axis comes within 2.0 in (1.25 + 0.75) of the core circle. A vertical hang needs 45°, which leaves **12.8° of margin**, so the coil settles **plumb, in a plane parallel to the CRAG face, hanging from the top of its hole**. With its inner face 1.25 in outboard of the CRAG face, its center rests about **1.6 in** (1.58) above the peg root; how far along the peg it comes to rest depends on where it is released and on friction. Draw both bounding poses on the drawing sheet: the near-vertical wedged pose and the perpendicular-to-peg pose.

Two coils on adjacent pegs do not interfere: Low and Mid Pegs are 28 in apart and High Pegs 14 in apart, against a 10-in coil OD.

**High Peg root mounting (ref).** The roots cross the lantern joint. A 45° peg meets the spire face in an ellipse 1.5 in wide and 1.5/sin45° = **2.12 in** tall, so a root at Z = 78 spans **Z 76.94–79.06**, with 1.06 in of it above the SUMMIT BEACON lantern joint at Z = 78. A ROPE COIL hangs on that peg, so the translucent lantern must carry no part of the load: carry each root on a structural boss let into the opaque spire, and back the lantern's lower edge with opaque material over the 3.0 in of face width at each peg. The 78-in tier ring is interrupted at the same two places.

**Robot approach.** A 45° peg with 10.0 in exposed projects 10·cos45° = **7.07 in** horizontally off its face. The BASE DEPOT's PEG FACE leg (§3) runs along this face, so BUMPERS stop at its lip, 16.75 in off the face, and the Low and Mid Peg tips stop 9.68 in short of the lip's outer face. From the FRAME PERIMETER, 3.0 in behind the BUMPER face at **19.75 in**, a Low or Mid Peg tip is **12.68 in** of horizontal extension away and its root **19.75 in**. The High Pegs' roots sit on the spire's peg face, **14.0 in inboard** of the tower's, so a High Peg tip is **26.68 in** away and its root **33.75 in**. **The binding reach on the CRAG is the High Peg tip, at 26.68 of the 30 in allowed** while any part of the ROBOT's BUMPERS intersects its own ALLIANCE's CRAG APRON (**G404**, **R105**), which it always does with its BUMPERS at the lip. The High Peg root is beyond reach, so a ROPE COIL is placed on a High Peg by releasing it over the tip and letting it drop onto the peg, where it settles in the rest pose above; release from rest is not LAUNCHING (**G502**).

### 2.6 LED indicators (cosmetic; see §8)

Tier rings wrap the tower and spire at **30 / 54 / 78 in**, band width 1.0 in (ref). The 30 and 54 rings are centered on those heights; the 78 ring is hung with its top edge on the lantern joint (band Z 77.0–78.0) so that it stays on the opaque spire (see §8). The **SUMMIT BEACON** is the translucent top 12 in of the spire (Z 78 → 90), luminous center **84 in**, visible on all four spire faces.

### 2.7 CAD modeling notes

- **Feature order:** tower body → spire prism (with the top 12 in as a separate translucent body) → shelf sub-assembly (model one, pattern to 24/42) → socket sub-assembly (model one; place 4× on the ±Y faces at ±14, plus the Summit instance on the shelf face at 15°) → peg sub-assembly (one peg, 6 placements) → depot ring (§3) → LED rings as cosmetic sweeps on a suppressible layer.
- **Symmetry:** the CRAG is mirror-symmetric about its own X–Z plane, including the Summit Socket, which is why that socket sits on the CRAG centerline. The second CRAG is a 180° rotate-pattern of the first about field center; do not model it twice.
- **Model these first and exactly:** shelf heights 24/42; slot width 14 and slot centers ±15.5/0; shelf depth 14; socket rims 30/54/72; socket angles 30/30/15; socket lateral ±14 (side faces) and 0 (summit); socket standoff 8.0; socket tube length 7.0; **socket ID 6.50 ± 0.125**; peg heights 30/54/78; peg laterals ±14 (low/mid) and ±7 (high); peg OD 1.5; peg angle 45; peg exposed length 10; spire prism 20 × 20 × (60→90); apron offsets 36/20.

---

## 3. BASE DEPOT (ring tray, ×1 per CRAG)

A floor-level tray surrounding the CRAG on all four faces: a closed square ring in plan, 16.0 in wide throughout. Its named parts are used consistently across this package:

- four **legs**, 16 × 48 in, one directly outboard of each face: the **SHELF FACE leg** (Blue: X 284–300, Y 216–264), the two **SOCKET FACE legs** (Blue: X 300–348, Y 200–216 and Y 264–280) and the **PEG FACE leg** (Blue: X 348–364, Y 216–264);
- four **corner squares**, 16 × 16 in, one at each CRAG corner (Blue: X 284–300 and X 348–364, each at Y 200–216 and Y 264–280).

The eight rectangles form one continuous channel, Blue X 284–364 × Y 200–280 less the CRAG footprint. There are no corner arms. Two opposite legs and the four corner squares form two straight 16 × 80 in runs, joined by the other two legs.

| Feature | Dimension | Status |
|---|---|---|
| Lip top height | **4.0 in** above carpet, i.e. **3.75 in above the tray floor** | CRITICAL: robots must clear it. DEPOT scoring is a floor-support test. |
| Lip top-edge radius | 0.25 in; as built, R0.25 is applied to **every outside face of the tray** (sides, top and bottom) | CRITICAL (lip-crossing geometry) |
| Channel depth (CRAG face to lip inner wall) | **16.0 in**, off **every** face | CRITICAL |
| Ring layout | four 16 × 48 in legs, one along each face (SHELF FACE, both SOCKET FACES, PEG FACE), and **four 16 × 16 in corner squares**, one at each corner, closing the ring (Blue channel: X 284–364 × Y 200–280, less the CRAG footprint X 300–348 × Y 216–264) | CRITICAL |
| Lip thickness | 0.75 in, **no plus tolerance (+0 / −0.25)** | held for APRON tape clearance (APRON clearance check below); not free to float like a (ref) value |
| Outer footprint | **81.5 in square** over the lip's outer faces (48 + 2 × 16.75), centered on the CRAG: Blue X 283.25–364.75, Y 199.25–280.75; Red X 283.25–364.75, Y 43.25–124.75. The entry chamfer strip brings the plan envelope to an **83.5-in square**: Blue X 282.25–365.75, Y 198.25–281.75; Red X 282.25–365.75, Y 42.25–125.75. | (ref): follows from the CRITICAL channel and the lip (+0 / −0.25), so it may shrink by up to 0.5 in but never grow |
| Tray floor | 0.25 in thick, laid on the carpet so that its **top surface is at Z = 0.25**. Every SUPPLY in the DEPOT stands 0.25 in higher than the carpet, which the occlusion budget in §7 accounts for. A 45° entry chamfer strip with a 1.0-in leg runs outside the lip all the way around, mitred at the four corners. | CRITICAL: it sets the standing height of everything in the tray |
| Capacity | single layer only (manual §4.4.1): about **18 CACHE CRATES** one abreast in the 16-in channel, or about **27 SUPPLIES** in a mixed load, in 80² − 48² = **4096 in²** of tray. Crates cannot sit two abreast (2 × 13.0 > 16.0), so the crate count is set by length: each 80-in run holds six crates and each 48-in leg between the runs three. | gameplay reference |

**Piece-fit check (why the channel is 16.0 in):** a CACHE CRATE's crowned envelope is **13.0 in**, and a square's minimum width in any orientation is its side, so the channel must exceed 13.0 in for a crate to lie inside the channel's vertical projection at all. At 16.0 in a crate has 3.0 in to spare; at 12.0 in no crate could ever be SCORED in the DEPOT.

**APRON clearance check (verify in CAD).** The ring lies inside every CRAG APRON, but with little room along the SOCKET FACES. The chamfer strip's outer edge is **17.75 in** off each face. The 2-in APRON tape is laid inside its 20-in offset line, so the tape's inner edge is **18.0 in** off each SOCKET FACE. That leaves **0.25 in** along the SOCKET FACES and **0.16 in** at the four corner arcs, where the chamfer corner lies 17.84 in from the arc center (Blue (284, 216) at the SHELF FACE / −Y SOCKET FACE corner) against the tape's R18 inner arc. A lip built 0.25 in over its nominal 0.75 in would bring the chamfer onto the tape along the SOCKET FACES and about 0.11 in over it at the corner arcs, so the lip thickness carries no plus tolerance (+0 / −0.25): model it at its nominal 0.75 in. Off the SHELF FACE and the PEG FACE the tape's inner edge is 34.0 in out, far from the ring.

**Open-to-sky check.** The shelves cantilever 14.0 in from the SHELF FACE and span only that face's 48-in width, the socket tubes overhang both SOCKET FACE legs, and only the thin Low and Mid Pegs cross the PEG FACE leg. The parts of the ring differ in what they accept from above:

- the **SHELF FACE leg**: only its outer **2.0 in** is open, a 48 × 2 in strip too narrow for any SUPPLY. The rest is loaded by pushing SUPPLIES in over the lip and under the shelves: the Shelf 1 underside is at **Z = 23.25**, and no gusset descends below **Z = 19.0** (the gusset floors in §2.2), against a crowned CRATE's top at Z = 13.25 on the tray floor.
- all four **16 × 16 in corner squares**: **fully open to the sky**.
- both **SOCKET FACE legs**: open except where the two socket tubes overhang them. On the Blue +Y face the Low Socket tube's plan silhouette covers X 306.7–313.3 × Y 265.6–274.9 from Z 22.19 upward, and the Mid Socket tube's covers X 334.7–341.3 over the same Y band from Z 46.19 upward. Beside each tube the clear columns are only 1.56 in wide toward the face and 5.11 in toward the lip, and a SUPPLY cannot be dropped into the tray where a tube overhangs it. The leg is open between the two tubes (a 21.32-in column, Blue X 313.34–334.66) and beyond each tube, where a 6.66-in column joins the adjacent corner square into a 22.66 × 16 in opening.
- the **PEG FACE leg**: open except under the four 1.5-in Low and Mid Pegs (Blue Y 226 and Y 254), which reach 7.07 in out over its inner edge. The clear column between the two pegs of a tier is 26.5 in wide.

A crate still fits inside the channel's vertical projection everywhere. The **G502** launch exception (BUMPERS in the SHELF FACE half of the own CRAG APRON, Blue X < 324) covers a SUPPLY that comes to rest anywhere in the tray. That half of the APRON contains the SHELF FACE, the SHELF FACE leg and its two corner squares, and it runs along both SOCKET FACES up to the centerline. From the SOCKET FACE parts of it, the SOCKET FACE legs and the PEG FACE corner squares (Blue X 348–364.75, Y 199.25–216 and Y 264–280.75) are in direct line along the face. Only the middle of the PEG FACE leg (Blue X 348–364.75, Y 216–264) lies behind the CRAG, and the 60-in tower body blocks it.

**Robot standoff and reach (reference; all horizontal).** The lip's outer face is 16.75 in off **every** CRAG face. With the BUMPER face there, the FRAME PERIMETER is 3.0 in behind it at **19.75 in**, and every scoring position on the CRAG is reached across the tray:

| Scoring position | Out from its face | Extension from the FRAME PERIMETER |
|---|---|---|
| Shelf slot center (Shelf 1 and Shelf 2; mid-depth of the 14.0-in shelf) | 7.0 | 12.75 |
| Summit Socket rim center | 8.0 | 11.75 |
| Low and Mid Socket rim centers | 8.0 | 11.75 |
| Low and Mid Peg tips / roots | 7.07 / 0 | 12.68 / 19.75 |
| High Peg tips / roots (on the spire's peg face, 14.0 in inboard) | −6.93 / −14.0 | **26.68** / 33.75 |

A ROBOT with its BUMPERS at its own CRAG's lip always has them inside its own CRAG APRON, so the 30-in extension limit of **G404** and **R105** applies there, for reach over that APRON (every CRAG scoring position is inside it); the 18-in limit applies everywhere else on the FIELD. **The binding reach is the High Peg tip, at 26.68 of the 30 in allowed.** The High Peg root is beyond reach, so a ROPE COIL is placed on a High Peg by releasing it over the tip and letting it drop onto the peg (§2.5). Every other position is within 20 in, and all but the Low and Mid Peg roots are within 18 in.

**CAD notes:** model the tray as its own sub-assembly mated to the CRAG base, because entrants will study lip-crossing geometry in isolation. The floor, the lip and the chamfer strip are each a square ring (an outer square less an inner square) centered on the CRAG's vertical axis. The tray is symmetric under a 90° rotation about that axis, so one leg and one corner square can be patterned four times. Robot-driving dims: **lip height 4.0, lip radius 0.25, channel width 16.0 off every face, corner square 16.0**.

---

## 4. HEADWALL (×2)

### 4.1 Geometry definition

Everything about the HEADWALL derives from one reference plane. Define it first:

> **PLANE P (per alliance):** contains the horizontal line {X = 48 (Blue) / X = 600 (Red), Z = 0} running Y 90–234, tilted **15° from vertical** with the **top leaning toward the alliance wall**. Robots climb the field side of P.

| Feature | Dimension | Status |
|---|---|---|
| Width | **144 in** (Y 90–234), three **48-in lanes** (Blue lane centers Y = 114 / 162 / 210) | CRITICAL |
| Incline | **15° from vertical** (plane P) | CRITICAL |
| Rung centerlines | lie **in plane P** | CRITICAL |
| Rung-top heights (vertical, from carpet) | **LEDGE 30 · CAMP 54 · SUMMIT 78** | CRITICAL |
| Rung OD | **1.5 in** | CRITICAL |
| Rung length | **20.0 in** | CRITICAL |
| Lateral stagger from the lane centerline | **LEDGE −12.0 · CAMP +12.0 · SUMMIT −12.0, identical in all three lanes.** The sign alternates by rung only. Opposite signs in adjacent lanes would put their rungs 24 in apart center-to-center at every height, closer than two hanging ROBOTS are wide. Red is the 180° rotation about (324, 162). | CRITICAL |
| Structure clearance behind rungs | all truss structure ≥ **4.0 in** behind plane P (measured normal to P, on the wall side), **except the two rung end brackets**, which may enter the band within 2.0 in of each rung end | CRITICAL (hook wrap over the middle 16.0 in of every rung) |
| Structure top | truss chords end at **84 in** vertical | (ref) |
| Chord/upright section | 2-in square tube | (ref) |
| Lane tag panels | carried on the lower crossbeam: panels **plumb**, tag centers at **Z = 12 in**, panel face plane **X = 39.0 (Blue) / 609.0 (Red)** | CRITICAL for vision |
| Lower crossbeam | 2 × 2 in tube, centerline **Z = 12.0**, in a layer **8.0–10.0 in behind plane P** (measured normal to P), held off the lane frames by a 2 × 2 standoff at each upright. Its field-side face (X = 36.50 at Z = 12) lies behind the tag panel back at **X = 38.75**, so the plumb panels and their wedges sit in front of the beam rather than inside it | (ref) |
| Tag wedge bracket | 15° aluminum wedge, 9.0 in wide, filling the gap between the crossbeam's field-side face and the plumb panel back at X = 38.75 over the face's height (Z 11.29–13.22): **2.25 in** thick at Z = 12, 2.06 in at the bottom edge, 2.58 in at the top | (ref) |

**Derived rung positions (reference; do NOT drive these. Dimension plane P and the vertical heights, and let CAD derive them):** rung center Z = top − 0.75. Blue rung center X = 48 − Z·tan 15°: LEDGE (Z 29.25) X ≈ **40.16** · CAMP (Z 53.25) X ≈ **33.73** · SUMMIT (Z 77.25) X ≈ **27.30**. Horizontal setback between successive rungs ≈ **6.4 in** (24 × tan 15°). Red mirrors about the field center.

**Derived rung end positions (Blue, reference):**

| Rung | Lane 1 (ctr 114) | Lane 2 (ctr 162) | Lane 3 (ctr 210) |
|---|---|---|---|
| LEDGE | Y 92 – 112 | Y 140 – 160 | Y 188 – 208 |
| CAMP | Y 116 – 136 | Y 164 – 184 | Y 212 – 232 |
| SUMMIT | Y 92 – 112 | Y 140 – 160 | Y 188 – 208 |

Every rung sits at least 2 in inside its lane boundary, and no lateral position engages two successive rungs: LEDGE spans lane-center −22 to −2 while CAMP spans +2 to +22. Because the stagger is the same in every lane, rungs at the same height in adjacent lanes are 48.0 in apart center-to-center and **28.0 in end to end**, so three ROBOTS at the 120-in frame-perimeter limit hang side by side without touching.

**Tag panel clearance check:** a 9.0-in panel centered at Z = 12 spans Z 7.50–16.50. Its most forward point is the top edge at (39.0, 16.50), whose normal distance behind plane P is (48 − 16.50·tan15° − 39.0)·cos15° = **4.42 in**. The panel therefore satisfies the ≥ 4.0-in rule over its whole height and sits behind the truss's own field-side face. It mounts on the set-back crossbeam through the 15° wedge bracket given in the table above. No part of the panel enters the climbing volume.

**BASECAMP clear volume (publish this; it governs starting configurations).** The truss leans back over BASECAMP, so a robot there stands under the lower, wall-side face of the lane frames. With the 2-in members of the front layer (4.0–6.0 in behind plane P), that face lies at X_b(Z) = 41.788 − 0.26795·Z (Blue), and the clear height under it is

> **H(X) = 3.7321 × (41.788 − X)** inches

except between X = 34.2 and 38.6, where the lower crossbeam (§4.1, 8.0–10.0 in behind plane P) limits the clear height to 10.8 in. At each lane center the tag panel hangs to Z = 7.5 across its 9.0-in width, so between X = 38.75 and 39.0 the clear height there is 7.5 in (Red: X 609.0–609.25).

| X (in) | 0 | 12 | 24 | 30.5 | 32.6 | 34.2–38.6 | 40 | 41.79 |
|---|---|---|---|---|---|---|---|---|
| **H (in)** | 156.0 | 111.2 | 66.4 | **42.1** | 34.3 | 10.8 (crossbeam) | 6.7 | 0 |

A robot at the 42-in starting-configuration limit fits anywhere up to X = 30.5, which is why **G302** stages robots against the alliance wall rather than against the truss. The curve depends on the (ref) member depth: a deeper frame moves it toward the wall.

**Climb reach (reference; the arithmetic behind G416).** Extensions below are given to the rung **centerline**. A hook has to wrap past the far face of a 1.5-in OD rung, so **add 0.75 in** for the reach that engages it. A robot obeying **G416** has all of its bumpers at X ≥ 48, so its FRAME PERIMETER is at X ≥ 51 and its 18-in reach ends at X = 33.0. The HEADWALL is far from every CRAG APRON, so the 18-in limit always applies here; the 30-in allowance of **G404** and **R105** applies only while a ROBOT's BUMPERS intersect its own CRAG APRON.

| Rung | Rung center X | To the centerline | To wrap the rung | Within R105? |
|---|---|---|---|---|
| LEDGE | 40.16 | 10.84 in | **11.59 in** | yes, by 6.41 in |
| CAMP | 33.73 | 17.27 in | **18.02 in** | **no** (over by 0.02 in) |
| SUMMIT | 27.30 | 23.70 in | **24.45 in** | **no** (over by 6.45 in) |

Only the LEDGE RUNG is reachable from the carpet. The CAMP RUNG misses by 0.02 in at the minimum legal BUMPER thickness, and by more with any real bumper, so every rung above the LEDGE is reached from a hang, which is what the HEADWALL is designed to require.

### 4.2 CAD modeling notes

- **Feature order:** plane P → one lane frame (uprights behind P at the 4.0-in clearance) → rung + bracket sub-assembly → place 3 rungs by vertical height and lateral stagger → linear-pattern the lane ×3 at 48 in (a straight pattern with no mirroring, because every lane carries the same stagger) → lower crossbeam + plumb tag panels.
- **Rung end brackets** must fit within 2.0 in of the lane boundary at the closest approach. They are the one exception to the 4.0-in behind-P rule: every rung centerline lies in plane P, so an end support must cross the band. Model brackets only within the outer **2.0 in of each rung end**, leaving the middle **16.0 in** of every rung with a clear 4.0 in behind it for hook wrap.
- **Robot-driving dims:** rung OD 1.5; rung length 20; rung-top heights 30/54/78; stagger ±12; lane width 48; incline 15°; 4.0-in wrap clearance. These drive every climber hook, arm reach, and CG analysis; hold them exactly.
- Anchor geometry to the wall or guardrail is free **(ref)** provided it stays behind plane P. Anchors forward of P are prohibited because they would intrude on the climbing space.

---

## 5. OUTFITTER stations (×4, two per alliance)

A human-player feed chute built into the alliance wall.

| Feature | Dimension | Status |
|---|---|---|
| Wall opening | **30 in wide × 16 in tall** (spans Z 24–40) | CRITICAL |
| Sill height (opening bottom edge) | **24 in** | CRITICAL |
| Sill edge radius | 0.5 in | (ref) |
| Chute centers | Blue (0, 30) and (0, 294); Red (648, 294) and (648, 30) | CRITICAL |
| Alliance wall thickness at the chute | 2.0 in | (ref) |
| Chute ramp | smooth ramp from the human-player side down to the sill, **30° from horizontal (ref)**, width 30 in, ramp run 40 in, side cheek funnels flaring to 36 in at the loading end | (ref; behind-wall geometry is non-interactive) |
| AprilTag panel | centered above each chute, tag center at **52 in**, plumb, on the field-side wall plane | CRITICAL for vision |
| OUTFITTER LANE (tape) | **36 in wide × 48 in into the field**, centered on the chute Y | CRITICAL (no-defense zone line call) |

**Piece-pass check:** the CACHE CRATE's maximum envelope is 13.0 in (12.0 cube + 0.5 face crown per side), so the 16-in opening clears it by 3.0 in. The O2 CELL passes end-on (5.0 × 5.0) or lengthwise (14.0 × 5.0 through a 30-in width). The ROPE COIL passes flat (10.0 × 2.5) or on edge (10.0 tall). The 9.0-in tag panel spans Z 47.50–56.50 and clears the opening top at Z = 40 by 7.50 in.

**CAD notes:** model one station; the other three are mirror/rotate instances. Robot-driving dims: **opening 30 × 16, sill 24** (they set intake-from-chute geometry), plus tag height 52.

---

## 6. CENTER CACHE and staging marks (taping and staging plan)

There is no structure here, only tape and game pieces. Model the marks anyway so that renders and the tag map are exact.

- **CENTER CACHE:** 9 white taped marks in a **3×3 grid, 24-in spacing, centered (324, 162)** (grid points at X = 300/324/348, Y = 138/162/186). Staging: 3 CACHE CRATES, 3 O2 CELLS, 3 ROPE COILS, all field-neutral. **O2 CELLS lie horizontal with their axis along +X**; ROPE COILS lie flat; CRATES sit square to the axes.
- **Alliance staging marks:** at Blue X = 144 and Red X = 504, marks at Y = 108 / 162 / 216; **2 pieces of one type per mark**, assigned per the FIELD SETUP CHART.

### FIELD SETUP CHART

**(a) CENTER CACHE assignment.** Each piece type appears once per row and once per column (a Latin square), so no type is staged nearer one alliance's CRAG than the other's:

| | X = 300 | X = 324 | X = 348 |
|---|---|---|---|
| **Y = 186** | CACHE CRATE | O2 CELL | ROPE COIL |
| **Y = 162** | ROPE COIL | CACHE CRATE | O2 CELL |
| **Y = 138** | O2 CELL | ROPE COIL | CACHE CRATE |

> *Rotational note:* the 3×3 grid has one point fixed by the 180° rotation about (324, 162), plus four swapped pairs, so no 3/3/3 assignment can be strictly rotation-invariant. This Latin square is the best achievable balance: the CACHE CRATE set is itself rotation-invariant, and the aggregate haul distance from all nine marks to each CRAG is identical for the two alliances (725.0 in each). Per type, the two alliances differ by at most 2.3 in (under 1%).

**(b) Alliance staging marks.** 2 pieces of ONE type per mark; the Red assignment is the 180° rotation of Blue:

| Mark | BLUE (X = 144) | RED (X = 504) |
|---|---|---|
| Y = 108 | 2 CACHE CRATES | 2 ROPE COILS |
| Y = 162 | 2 O2 CELLS | 2 O2 CELLS |
| Y = 216 | 2 ROPE COILS | 2 CACHE CRATES |

**(c) OUTFITTER stock.** Each alliance's OUTFITTER stations hold **7 of each type** (14 per type across both alliances). Robot preloads are drawn from the alliance's OUTFITTER stock during setup; they are not additional pieces.

**Count check (per type):** 3 (CENTER CACHE) + 2 × 2 (alliance staging, both sides) + 2 × 7 (OUTFITTER stock) = **21 per type, 63 total on the field**.

**Extent check:** the staged CENTER CACHE spans Y 131.5–192.5 across the crowned 13.0-in crate envelope (a crate on the Y = 186 row reaches Y = 192.5; on the Y = 138 row, Y = 131.5) and X 293–355 (an O2 CELL on the X = 300 column reaches X = 293). It sits entirely inside the 68-in open corridor between the two aprons (Y 128–196), with 3.5 in of clearance at each end.

**CAD modeling notes:** put the marks and staged pieces in a separate "staging" configuration so that field drawings can toggle them. Auto-path planners consume the staged-piece poses, so place piece models exactly on mark centers.

---

## 7. AprilTag panels (×26)

Family **36h11**, **26 tags**. Panel geometry (all CRITICAL for vision): **tag body 6.5 in** square on an **8.125-in** printed target, centered on a **9.0-in** square panel, panel thickness 0.25 in (ref). All panels are plumb (tag plane vertical, ±1°) and square to their stated facing (±1°), and CRAG panel center heights are held to ±0.15 in (occlusion budget below). Mounting:

| IDs | Location | Z center | Facing |
|---|---|---|---|
| 1, 2 | Blue OUTFITTER chutes (Y = 30, Y = 294), wall plane X = 0 | 52 in | +X (into field) |
| 3, 4, 5 | Blue HEADWALL lanes (Y = 114, 162, 210), panel plane **X = 39.0** | 12 in | +X |
| 6–13 | Blue CRAG: pairs at ±14.0 in from the face centerline — 6/7 shelf face (X = 300), 8/9 +Y socket face (Y = 264), 10/11 −Y socket face (Y = 216), 12/13 peg face (X = 348) | 17.5 in | outward, ⟂ face |
| 14, 15 | Red OUTFITTER chutes (Y = 294, Y = 30), wall plane X = 648 | 52 in | −X |
| 16, 17, 18 | Red HEADWALL lanes (Y = 210, 162, 114), panel plane **X = 609.0** | 12 in | −X |
| 19–26 | Red CRAG: 180° rotation of Blue (Red ID = Blue ID + 13) | 17.5 in | outward |

**Occlusion budget (this sets the 17.5-in CRAG tag height).** A 9.0-in panel centered at 17.5 in spans Z 13.00–22.00, and its 8.125-in target spans Z 13.44–21.56. Against that band:

- A CACHE CRATE standing on the BASE DEPOT tray floor tops out at **13.25 in** (the tray floor's 0.25 plus 13.0 across its crown: 0.5 bottom crown + 12.0 cube + 0.5 top crown), **0.19 in** below the target. The tray runs beneath the tag panels on **all four faces**, so this margin applies to every CRAG tag. It is the tightest occlusion margin in the package, so the CRAG tag panel center height is held to **±0.15 in** at field setup, against ±0.25 in for tag position elsewhere (VISION-GUIDE §1.3).
- The underside of Shelf 1 sits at 23.25 in, 1.25 in above the panel.
- The lowest point of a Low Socket tube is at Z 22.19, 0.63 in above the target's top edge, and the tube spans 1.56 to 10.89 in outboard of the face, clear of every sightline from a camera 10–20 in high. A camera 24–36 in high looks down past the tube, which can hide part of the target of the tag beneath it (tags 8, 10, 21 and 23), and most of it from close range.

From a camera 10–20 in high, no field structure, and no SUPPLY other than the single case below, can occlude a CRAG tag. The one SUPPLY anywhere on the FIELD that reaches into the target band is an O2 CELL stood on its end in the DEPOT, in front of any of the four faces (its top at 14.25 in, tray floor 0.25 plus 14.0, against a 13.44-in target bottom, so it covers the bottom 0.81 in of the target); VISION-GUIDE §1.3 covers that case and gives the camera-height rule for it. HEADWALL lane tags sit at 12 in because that band is clear of every rung and stays ≥ 4.4 in behind plane P. SCREE (§1.4) occludes no tag: its ridges stand 1.75 in tall, and the lowest panel edge on the FIELD is a HEADWALL lane panel's, at Z = 7.50.

Panel poses must match `04-vision/apriltag-field-layout.json` exactly. The JSON is generated from the tag table in VISION-GUIDE §3 and drives every simulation.

**CAD notes:** one panel part with a decal appearance per ID; place instances by the coordinate table. Vision-driving dims: body 6.5 on an 8.125 target on a 9.0 panel, center heights 17.5 (CRAG) / 12 (HEADWALL) / 52 (OUTFITTER), CRAG pair offset ±14, facing normals. Keep the full 8.125-in white border unobstructed as seen from the field side, and verify it with a clearance check.

---

## 8. LED indicators (cosmetic)

- **Tier rings** (per CRAG): three bands **1.0 in wide × 0.25 in deep, let flush into the face** so that nothing projects into a robot-interaction envelope (ref). The **30** and **54** rings are centered on their tier heights and wrap the 48 × 48 tower. The **78** ring wraps the 20 × 20 spire and is hung with its **top edge on the lantern joint** (band Z 77.0–78.0, center 77.5) so that it stays entirely on the opaque spire. It is the one ring not centered on its tier height: the SUMMIT BEACON lantern begins at Z = 78, and a centered band would straddle the joint between two bodies with different appearances. On the PEG FACE it is interrupted where the two High Peg root bosses cross it. The rings display alliance color when CAMP I / CAMP II / HIGH CAMP is established and latch; a lit ring never goes dark. They carry **no other signal**: the FORECAST and the declared ROUTE are shown on the guardrail FIELD LEDs, not on the CRAG (manual §3.1.2).
- **SUMMIT BEACON** (per CRAG): the translucent top 12 in of the spire (Z 78 → 90), luminous center **84 in**, visible on all four spire faces. It ignites when all three CAMPS are established (+10, latched).
- **FIELD LED bands** (per guardrail): see §1.3.
- LEDs are decorative confirmation only; referee state is the authority. Keep all indicator geometry outside robot-interaction envelopes.

**CAD notes:** model the tier rings as cosmetic swept bands (the 30 and 54 centered on their heights, the 78 with its top edge at Z = 78) on a suppressible "cosmetics" layer. Model the beacon as a separate translucent body forming the spire's top 12 in.

---

## 9. Game pieces (×3 types, 21 each, 63 total)

Colors and materials are specified in `03-field/MATERIALS-AND-COLORS.md` and repeated here for convenience.

### 9.1 CACHE CRATE

- Cube, **12.0 in** per side (CRITICAL), pillowed faces with **0.5-in face crown (ref)** and **1.0-in edge fillets on all twelve edges (ref)**, **~2.0 lb**. The fillets remove material at the edges, so they do not change the envelope; they let a CRATE roll up over the 4-in BASE DEPOT lip when pushed and enter the OUTFITTER chute without catching a corner. The maximum envelope across the crown is **13.0 in**, the dimension the OUTFITTER chute is sized against. Skinned-foam construction, **compliant**: compression tolerance **2.0 in** across any pair of opposing faces (13.0-in crowned envelope → **11.0 in**) under a squeeze of up to **15 lbf** between flat plates; the crowns flatten first, and the CRATE recovers fully when released. Model rigid at nominal size. Every fit and clearance in this package is computed uncompressed, so compression is margin, not budget: the 0.78-in slot clearance below does not count on it.
- Color: expedition violet `#7B3FA0`.
- **CAD notes:** one part, a 12-in cube with face bulges and fillets. Robot-driving dims: the **13.0 crowned envelope vs the 16.0-in chute opening** (3.0 in clear), and the shelf slot, which needs the crown profile rather than the nominal cube. A CRATE rests on its bottom crown, so the cube's bottom plane sits 0.5 in above the shelf and each side face reaches its full 0.5 bulge at **6.5 in** above it. The binding width is at the top of the 2.0-in slot fences, where the crate is about **12.44 in** wide, leaving **0.78 in of clearance per side** rather than the 1.00 in the nominal cube suggests. That 0.78 in is the lateral placement tolerance available to a scoring mechanism. The 13.0 crown sits 4.5 in above the fences and touches nothing; two CRATES in adjacent slots (15.5-in pitch) clear each other by 2.5 in. Put the crown profile and both clearances on the same drawing view.

### 9.2 O2 CELL

- Cylinder, **5.0 in dia × 14.0 in overall length** (CRITICAL), **~1.5 lb**, with domed end caps (dome height **1.5 in** each, ref) blended to the body by a **1.0-in fillet at each cap/body junction (ref)**. The cap arc is struck through the pole and the equator, so it is not tangent to the cylinder: it meets the wall at a **28.1° tangent break**, and the fillet is what makes the surface continuous. The fillet also moves the shoulder: the full 5.0-in diameter runs **10.44 in**, not the 11.0 in between the arc endpoints. Rigid molded shell (thick-wall ABS tube with rigid molded ABS domed caps, no foam): **rigid, zero compression tolerance**. Model rigid at nominal size; a gripper must supply its own compliance.
- Color: body `#F2F2F0`, domed caps `#2E8B57`.
- **CAD notes:** one revolved profile. Robot-driving dims: **5.0 OD and 14.0 length vs socket ID 6.50 ± 0.125** (0.75-in radial clearance per side, 1.50 in on diameter) and vs the 7.0-in socket tube depth (7.0 in of CELL protrudes when seated). Show the clearance stack on the drawing.

### 9.3 ROPE COIL

- Torus, **10.0 in OD, 2.5-in tube section, 5.0-in ID hole** (all CRITICAL), **~1.0 lb**. As built it is one revolve: a 2.5-in-diameter profile circle whose outer edge is 5.0 in from the axis, which puts its center at r = 3.75. All three published numbers follow from that single sketch. Molded rubber/foam ring, **compliant**: the tube section compresses up to **0.5 in** (2.5 → **2.0 in**) under a pinch of up to **10 lbf**, and the ring ovalizes up to **1.0 in** across the OD (10.0 → **9.0 in**) under a diametral squeeze of up to **5 lbf**, which narrows the hole by the same 1.0 in (5.0 → 4.0 in, still 2.5 in larger than the 1.5-in peg). It recovers fully when released. Model rigid at nominal size.
- Color: amber `#D9A441`.
- **CAD notes:** one revolved torus. Robot-driving dims: **5.0 ID hole vs 1.5-in peg OD** on the 45° peg. The drawing shows both bounding rest poses (§2.5), because that geometry defines every hook and spear end effector.

---

## 10. Master dimension ledger (every CRITICAL dimension on one page)

| # | Element | Dimension | Value |
|---|---|---|---|
| 1 | Field | carpet | 648 × 324 |
| 2 | CRAG | footprint / body height / spire | 48 × 48 · 60 · spire 20 × 20 prism, 60→90 (top 12 in translucent) |
| 3 | CRAG placement | centers | Blue (324, 240) · Red (324, 84) |
| 4 | Shelves | top heights / slot width / slot centers / depth | 24, 42 · 14.0 · ±15.5, 0 · 14.0 |
| 5 | Sockets (side faces) | rim heights / lateral / standoff / tilt / tube length | 30, 54 · ±14.0 · 8.0 · 30° from vertical · 7.0 |
| 6 | Socket bore | ID | **6.50 ± 0.125** |
| 7 | Summit Socket | rim height / lateral / standoff / tilt / tube length | 72 · on CRAG centerline · 8.0 from the SHELF FACE · 15° outward · 7.0 |
| 8 | Pegs | root heights / laterals / OD / angle / exposed | 30, 54, 78 · ±14.0 (low/mid), ±7.0 (high) · 1.5 · 45° · 10.0 |
| 9 | BASE DEPOT | lip height / lip radius / channel width / layout / tray floor top | 4.0 · 0.25 · 16.0 off every face · closed ring around all four faces: four 16 × 48 legs + four 16 × 16 corner squares (81.5 square over the lip, (ref)) · Z = 0.25 |
| 10 | HEADWALL | width / lanes / incline | 144 · 3 × 48 · 15° from vertical (plane P at X = 48 / 600) |
| 11 | Rungs | top heights / OD / length / stagger / wrap clearance | 30, 54, 78 · 1.5 · 20.0 · ±12.0 alternating by rung, same in every lane · ≥ 4.0 behind plane P |
| 12 | OUTFITTER | opening / sill / chute centers | 30 × 16 · 24 · (0/648, 30/294) |
| 13 | Zones | apron offsets / lane tape / basecamp | 36 (shelf & peg faces), 20 (socket faces), R20 corners · 36 × 48 · X 0–48 (600–648), Y 90–234 |
| 14 | AprilTags | body / target / panel / centers / CRAG lateral | 6.5 · 8.125 · 9.0 · Z = 17.5 ± 0.15 (CRAG) / 12 (HEADWALL, panel plane X = 39/609) / 52 (OUTFITTER) · CRAG pairs at **±14.0** from each face centerline |
| 15 | Game pieces | crate / cell / coil | 12.0 cube (13.0 crowned envelope) · ⌀5.0 × 14.0 · 10.0 OD, 2.5 tube, 5.0 ID |
| 16 | Staging | cache grid / staging marks | 3×3 at 24-in pitch, center (324, 162), Latin-square types · X = 144/504, Y = 108/162/216 |
| 17 | SCREE PATCH | footprint / ridges / ridge height / pitch / ridge centerlines | 30.0 × 30.0, sides parallel to the field axes · 4, half-round R1.75, cut square at the boundary · 1.75 · 8.0 · ±4.0, ±12.0 from the patch center |
| 18 | SCREE placement | Blue centers (ridge direction) · Red | S1 (105, 88) +45 · S2 (105, 162) Y · S3 (105, 236) −45 · S4 (200, 37) +45 · S5 (200, 125) +45 · S6 (200, 199) −45 · S7 (200, 287) −45 · S8 (234, 108) +45 · S9 (234, 216) −45 · Red = (648 − x, 324 − y), same ridge direction |

---

## Drawing set

Dimensioned multi-view SVG drawing sheets in `03-field/drawings/` (**6 files**), drawn to scale with every driving dimension labeled. The sheets are generated from the master dimension ledger (§10), so a sheet and the ledger should never disagree; if they do, the ledger governs and the organizers correct the sheet. Every sheet carries a title block with sheet number, units note, tolerance convention, revision, and the governing document. CRITICAL dimensions are boxed; reference dimensions are suffixed `(ref)`.

1. **`field-top-view.svg`**: full 648 × 324 field plan with element placements, zones, tape, the cache grid with the Latin-square type assignment, staging marks, apron offsets, axes, coordinate callouts, and a SCREE panel with the patch table and a ridge section.
2. **`crag.svg`**: CRAG multi-view sheet with shelf-face, socket-face, and peg-face elevations, a top (plan) view, and detail views: socket geometry (rim height, ±14 lateral, 8.0 standoff, 30° tilt, 7.0 tube, ID 6.50 ± 0.125), Summit Socket (rim 72, 8.0 standoff, 15°), peg geometry (45°, OD 1.5, exposed 10.0, laterals, both coil rest poses), shelf slots (3 × 14.0 + 1.5 fences, centers ±15.5), and depot section (lip 4.0, channel 16.0, crate-fit study).
3. **`headwall.svg`**: front elevation, side profile with the plane-P definition, the derived rung table, the BASECAMP clear-volume formula and table, the climb-reach table, a top view of the three lanes, and a rung/stagger detail (OD 1.5, length 20, ±12 stagger, 4.0 wrap clearance, tag panel at X = 39 / Z = 12).
4. **`outfitter.svg`**: field-side elevation (opening 30 × 16, sill 24, tag at 52), section through the chute (30° ramp), plan view with the 36 × 48 lane tape, and the crate-through-chute clearance study.
5. **`game-pieces.svg`**: orthographic views and sections of all three pieces with four clearance studies: crate-in-slot (12 vs 14), crate-through-chute (13 vs 16), cell-in-socket (5.0 vs 6.50 ± 0.125, 7.0 tube, 7.0 protrusion), and coil-on-peg (5.0 ID vs 1.5 OD at 45°, both rest poses).
6. **`apriltag-map.svg`**: top-view tag map with all 26 IDs, positions, Z centers, and facing normals, matching `apriltag-field-layout.json`.
