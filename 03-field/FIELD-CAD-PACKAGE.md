# SUMMIT PUSH — Field Element CAD Package

**Document:** `03-field/FIELD-CAD-PACKAGE.md` · **Spec authority:** `01-design/DESIGN-SPEC.md` (v2.2, LOCKED)

**Audience:** CAD modelers building the complete field. Every element is fully dimensioned here and in the drawing set (`renderings/`), so no length or angle has to be guessed. Appearance (material, color, finish) is specified in `03-field/MATERIALS-AND-COLORS.md`.

## 0. Conventions

- **Units:** inches unless noted. **Coordinate frame:** always-blue-origin NWU, with the origin at the right corner of the Blue alliance wall (from Blue's perspective), +X toward the Red wall, +Y left, +Z up. The field carpet is **648 in × 324 in**; guardrails are **20 in** tall; the centerline is at X = 324; field center is (324, 162). The layout is 180° rotationally symmetric about field center: **model the Blue half once, then rotate-pattern it 180° about (324, 162)**.
- **CRITICAL** flags a robot-interaction dimension: hold it exactly, to the tolerance where one is given. **(ref)** marks reference geometry that may float ±0.25 in without gameplay effect.
- Every angle on the field is **15°, 30°, or 45°**. Any other angle in the model is an error.
- **Heights are to the robot-interaction surface**: shelf top surface, socket rim center, peg root, rung **top**, tag center.
- The drawing set in `renderings/` illustrates this document. Where a drawing and this text disagree, this text and the DESIGN-SPEC govern; report the drawing.

---

## 1. Field Assembly Overview

### 1.1 Placement coordinates (locked; from spec §3)

| Element | Position (center) | Footprint / span |
|---|---|---|
| BLUE CRAG | (324, 240) | 48 × 48 in footprint, spire top 90 in |
| RED CRAG | (324, 84) | 48 × 48 in footprint, spire top 90 in |
| CENTER CACHE band | X 300–348, Y 108–216 | 9 taped marks, 3×3 grid, 24-in spacing, centered (324, 162) |
| BLUE HEADWALL | plane P crosses carpet at X = 48, Y 90–234 | 144 in wide, leaned 15° from vertical, top toward alliance wall, 3 × 48-in lanes |
| RED HEADWALL | X = 600, Y 90–234 | mirror |
| BLUE BASECAMP zone | X 0–48, Y 90–234 | taped zone (= HEADWALL ZONE) |
| RED BASECAMP zone | X 600–648, Y 90–234 | mirror |
| BLUE OUTFITTERS | chutes centered (0, 30) and (0, 294) | opening 30 W × 16 H, sill 24; lane 36 wide × 48 deep |
| RED OUTFITTERS | (648, 294) and (648, 30) | mirror |
| Alliance staging marks | Blue X = 144; Red X = 504 | marks at Y = 108 / 162 / 216 |

CRAG orientation: each CRAG's SHELF FACE faces its owning alliance wall (Blue CRAG shelf-face normal −X; Red +X), the PEG FACE faces the opponent wall, and the SOCKET FACES are the two ±Y side faces.

### 1.2 Taping plan (model tape as surface geometry)

All lines are 2-in tape geometry, with the line edge on the stated coordinate. Model tape as thin surface splines or decals so that renders match the manual and the zone rules are visible in screenshots.

| Marking | Color | Geometry |
|---|---|---|
| BASECAMP / HEADWALL ZONE boundary | alliance color | Blue: lines at X = 48 (Y 90–234) and Y = 90, Y = 234 (X 0–48); Red mirror. The wall closes the fourth side. |
| CLIMB LINE | alliance color, dashed outside BASECAMP | the X = 48 (Blue) / X = 600 (Red) line carried across the **full field width, Y 0–324**. Over Y 90–234 it coincides with the BASECAMP boundary (row above) and needs no second line; outside that band it is dashed and marks only the **G416** climb-entry plane. Without it, G416 would be a line call against an unmarked line on the open carpet beside BASECAMP, from which a ROBOT can reach lane 1's SUMMIT RUNG (Y 92). |
| OUTFITTER LANE (×4) | alliance color | 36 in wide, centered on the chute Y, extending 48 in into the field from the alliance wall |
| CRAG APRON (×2) | alliance color | offset **36 in** from the SHELF FACE and the PEG FACE and **20 in** from each SOCKET FACE (CRITICAL; the line call for the placement-protection rule), corners joined with 20-in-radius arcs tangent to both offset lines. No trim is applied: the two aprons and the staged CENTER CACHE all fit inside the 108-in corridor. |
| FIELD centerline | white | 2-in line at X = 324 running the full width, Y 0–324, broken where the two CRAG footprints cross it (the BASE DEPOT trays stop 8 in short of the line). **G402** and **G502** are both line calls against it. |
| CENTER CACHE band | white | 48 × 108 in, X 300–348, Y 108–216. Its end edges coincide with the two CRAG SOCKET FACE planes, and it is interrupted where the BASE DEPOT trays cross it. It is the reference marking for the **G402** AUTO exception; the outer 20 in at each end lie inside a CRAG APRON, whose tape governs there. |
| CENTER CACHE marks (×9) | white | 12-in "X" marks, 3×3 grid, 24-in pitch, centered (324, 162) |
| Alliance staging marks (×6) | white with alliance-color border | 12-in "X" at (144, 108/162/216) and (504, 108/162/216) |

**Apron corridor check (verify in CAD):** Blue's −Y socket-face apron occupies Y 196–216; Red's +Y socket-face apron occupies Y 108–128. The open corridor is Y 128–196 (68 in). The staged CENTER CACHE spans Y 131.5–192.5 across the crowned 13.0-in crate envelope, leaving 3.5 in of clearance at each end. No staged piece touches an apron, and the corridor is continuous through X 300–348, between the two CRAGS.

### 1.3 Perimeter and field lighting

- Guardrails: 20 in tall, transparent panel on a low frame of 2 × 1 in tube, along both long edges **(ref)**.
- **FIELD LED bands:** a 1.0-in-wide frosted LED band let into the top rail of each long-side guardrail, lens center **19.0 in** above the carpet, running the full 648 in and divided at X = 324 into two 324-in alliance segments. The section is **(ref)**; the 19.0-in height is CRITICAL only in that the band must clear the 20-in guardrail top.
- Alliance walls: full width, **78 in tall and 2.0 in thick throughout (ref)**; solid to Z = 39, glazed 39 → 78. Each wall has three driver stations, **96 in wide on 108-in centers (Y = 54 / 162 / 270)**, each with a 0.75-in shelf topping out at **36 in**, a window in the glazed band, and an E-STOP and an A-STOP button **(ref)**. The OUTFITTER chutes penetrate the wall at the coordinates above.

---

## 2. CRAG (×2)

A four-faced scoring structure, one per alliance, both on the centerline. All dimensions below appear on drawing sheets `crag.svg` (multi-view) and `field-top-view.svg` (placement).

### 2.1 Envelope

- **Tower body:** 48 × 48 in square footprint at carpet, rising to **60 in** (top plate).
- **Spire:** **20 × 20 in square prism (CRITICAL)**, centered on the tower's vertical axis, from **60 in to 90 in** overall height. The spire is a straight prism with no taper, so every published height is exact at every face.
- **SUMMIT BEACON lantern:** the top **12 in** of the spire (Z 78 → 90) is a translucent section with its luminous center at **84 in** (see §8). It is a section of the spire prism rather than an added dome, so the 90-in overall height is exact.
- Base perimeter kick-guard flush to carpet **(ref)**. All four faces are robot-facing scoring surfaces.

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

The SHELF FACE also carries the Summit Socket (§2.4) and the BASE DEPOT (§3).

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

**Robot standoff: the two sockets on a face are reached from different distances.** The BASE DEPOT's corner arm runs 16.0 in along each SOCKET FACE from the SHELF FACE plane, and the Low Socket, at −14.0 lateral, sits directly above it. A ROBOT servicing the Low Socket therefore parks against the arm's outer lip: the lip outer face is 16.75 in off the face, the BUMPER face is there, and the FRAME PERIMETER is 3.0 in behind it at **19.75 in**, so the rim (8.0 in outboard of the face) is **11.75 in of horizontal extension** away. The Mid Socket, at +14.0 lateral, is clear of the arm: BUMPERS come to the face, the FRAME PERIMETER is 3.0 in off it, and the rim is **5.0 in** away. Both are inside the 18-in limit, but a mechanism designed only for the 5.0-in case cannot reach the Low Socket. Model the arm and the Low Socket together and check this before committing to an arm length.

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
- Robot reach: a robot with its bumpers against the DEPOT lip has its FRAME PERIMETER 19.75 in from the shelf face plane, so the rim is **11.75 in** of horizontal extension away, inside the 18-in limit. The limiting requirement is the 72-in lift.

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

**ROPE COIL rest pose (model this; it defines every hook and spear end effector).** A 10.0-in-OD coil with a 5.0-in hole and a 2.5-in tube section, dropped over a 1.5-in peg, can tilt at most about **48°** (47.9°) away from perpendicular-to-the-peg before the hole binds on the rod (2.5·tanθ + 1.5/cosθ ≤ 5.0). A vertical hang needs 45°, which leaves only **2.9° of margin**. The coil therefore settles **near-vertical, in a plane parallel to the CRAG face, wedged on the peg at two contact points**, with its center roughly 1 in above the peg root and its inner face about 1.25 in outboard of the CRAG face. Draw both bounding poses on the drawing sheet: the near-vertical wedged pose and the perpendicular-to-peg pose.

Two coils on adjacent pegs do not interfere: Low and Mid Pegs are 28 in apart and High Pegs 14 in apart, against a 10-in coil OD.

**High Peg root mounting (ref).** The roots cross the lantern joint. A 45° peg meets the spire face in an ellipse 1.5 in wide and 1.5/sin45° = **2.12 in** tall, so a root at Z = 78 spans **Z 76.94–79.06**, with 1.06 in of it above the SUMMIT BEACON lantern joint at Z = 78. A ROPE COIL hangs on that peg, so the translucent lantern must carry no part of the load: carry each root on a structural boss let into the opaque spire, and back the lantern's lower edge with opaque material over the 3.0 in of face width at each peg. The 78-in tier ring is interrupted at the same two places.

**Robot approach.** A 45° peg with 10.0 in exposed projects 10·cos45° = **7.07 in** horizontally off its face. With BUMPERS against the tower's PEG FACE, the FRAME PERIMETER sits 3.0 in off it, so the Low and Mid Peg tips reach **4.07 in inside** the FRAME PERIMETER's vertical projection at Z = 30 and Z = 54. That is legal, because the pegs are not a ROBOT extension, but a ROBOT approaching this face must either carry an open pocket above its BUMPERS at those heights or stand off until its FRAME PERIMETER clears the tips, at which point a peg root is 7.07 in of reach away. The High Pegs are the opposite case. Their roots sit on the spire's peg face, **14.0 in inboard** of the tower's, so from BUMPERS on the tower face a High Peg root is **17.0 in** away and its tip **9.93 in**. The High Peg root is the tightest horizontal reach on the CRAG, at 17.0 of the 18.0 in allowed.

### 2.6 LED indicators (cosmetic; see §8)

Tier rings wrap the tower and spire at **30 / 54 / 78 in**, band width 1.0 in (ref). The 30 and 54 rings are centered on those heights; the 78 ring is hung with its top edge on the lantern joint (band Z 77.0–78.0) so that it stays on the opaque spire (see §8). The **SUMMIT BEACON** is the translucent top 12 in of the spire (Z 78 → 90), luminous center **84 in**, visible on all four spire faces.

### 2.7 CAD modeling notes

- **Feature order:** tower body → spire prism (with the top 12 in as a separate translucent body) → shelf sub-assembly (model one, pattern to 24/42) → socket sub-assembly (model one; place 4× on the ±Y faces at ±14, plus the Summit instance on the shelf face at 15°) → peg sub-assembly (one peg, 6 placements) → depot tray (§3) → LED rings as cosmetic sweeps on a suppressible layer.
- **Symmetry:** the CRAG is mirror-symmetric about its own X–Z plane, including the Summit Socket, which is why that socket sits on the CRAG centerline. The second CRAG is a 180° rotate-pattern of the first about field center; do not model it twice.
- **Model these first and exactly:** shelf heights 24/42; slot width 14 and slot centers ±15.5/0; shelf depth 14; socket rims 30/54/72; socket angles 30/30/15; socket lateral ±14 (side faces) and 0 (summit); socket standoff 8.0; socket tube length 7.0; **socket ID 6.50 ± 0.125**; peg heights 30/54/78; peg laterals ±14 (low/mid) and ±7 (high); peg OD 1.5; peg angle 45; peg exposed length 10; spire prism 20 × 20 × (60→90); apron offsets 36/20.

---

## 3. BASE DEPOT (tray, ×1 per CRAG)

A floor-level tray wrapping the SHELF FACE and its two adjacent corners: an open-topped U in plan, 16.0 in wide throughout. Its three named parts are used consistently across this package:

- the **shelf-face leg**, 16 × 48 in, directly outboard of the SHELF FACE (Blue: X 284–300, Y 216–264);
- two **corner squares**, 16 × 16 in, continuing that leg past each SHELF FACE corner (Blue: X 284–300, Y 200–216 and Y 264–280); together with the leg they form one straight 16 × 80 in outer run;
- two **corner arms**, 16 × 16 in, turning back along each SOCKET FACE (Blue: X 300–316, same two Y bands).

The five rectangles form one continuous channel. Without the corner squares, the leg and the arms would meet only at points, which would be neither a U nor buildable as one weldment.

| Feature | Dimension | Status |
|---|---|---|
| Lip top height | **4.0 in** above carpet, i.e. **3.75 in above the tray floor** | CRITICAL: robots must clear it. DEPOT scoring is a floor-support test. |
| Lip top-edge radius | 0.25 in; as built, R0.25 is applied to **every outside face of the tray** (sides, top and bottom) | CRITICAL (lip-crossing geometry) |
| Channel depth (CRAG face to lip inner wall) | **16.0 in** | CRITICAL |
| Corner squares and arms | channel continues **16.0 in** along each SOCKET FACE, measured from the SHELF FACE plane, at the same 16.0-in depth out from that face, **plus the two 16 × 16 in outer corner squares that close the U** (Blue: X 284–300 × Y 200–216 and X 284–300 × Y 264–280) | CRITICAL |
| Lip thickness | 0.75 in | (ref) |
| Tray floor | 0.25 in thick, laid on the carpet so that its **top surface is at Z = 0.25**. Every SUPPLY in the DEPOT stands 0.25 in higher than the carpet, which the occlusion budget in §7 accounts for. A 45° entry chamfer strip with a 1.0-in leg runs outside the lip. | CRITICAL: it sets the standing height of everything in the tray |
| Capacity | single layer only (manual §4.4.1): about **8 CACHE CRATES** one abreast in the 16-in channel, or about **12 SUPPLIES** in a mixed load, in 1792 in² of tray. Twelve crowned crates would need 2028 in² and do not fit. | gameplay reference |

**Piece-fit check (why the channel is 16.0 in):** a CACHE CRATE's crowned envelope is **13.0 in**, and a square's minimum width in any orientation is its side, so the channel must exceed 13.0 in for a crate to lie inside the channel's vertical projection at all. At 16.0 in a crate has 3.0 in to spare; at 12.0 in no crate could ever be SCORED in the DEPOT.

**Open-to-sky check.** The shelves cantilever 14.0 in from the SHELF FACE and span only that face's 48-in width, so three regions of the tray are open from above. They differ in what they accept:

- the outer **2.0 in** of the shelf-face leg: a 48 × 2 in strip, too narrow for any SUPPLY;
- both **16 × 16 in outer corner squares** (Blue: X 284–300 × Y 200–216 and Y 264–280): **fully open to the sky**, and therefore the only places where any SUPPLY can be dropped straight in;
- both **16 × 16 in corner arms** along the SOCKET FACES: open except where the Low Socket tube overhangs them. On the Blue +Y face the tube's plan silhouette covers X 306.7–313.3 × Y 265.6–274.9 from Z 22.19 upward, almost centered in the arm, leaving clear vertical columns of only 6.66, 2.66, 5.11 and 1.56 in. A CACHE CRATE or a ROPE COIL cannot be dropped into an arm from above; it must be pushed in from the adjacent corner square, which is why the square has to be part of the channel.

The rest of the shelf-face leg is loaded by pushing SUPPLIES in over the lip and under the shelves: the Shelf 1 underside is at **Z = 23.25**, and no gusset descends below **Z = 19.0** (the gusset floors in §2.2), against a crowned CRATE's top at Z = 13.25 on the tray floor. The **G502** launch exception is exercised over the corner squares and the open outer strip.

**Robot standoff:** the lip outer face is 16.75 in from the CRAG face; with the bumper face there, the FRAME PERIMETER is 3.0 in behind it at **19.75 in**. Shelf slot centers are 7.0 in outboard of the face (mid-depth of the 14.0-in cantilevered shelf), so a shelf placement is **12.75 in** of extension; the Summit Socket rim, 8.0 in outboard of the face, is **11.75 in**. Both are inside the 18-in limit.

**CAD notes:** model the tray as its own sub-assembly mated to the CRAG base, because entrants will study lip-crossing geometry in isolation. Pattern the corner square and corner arm by mirroring one end. Robot-driving dims: **lip height 4.0, lip radius 0.25, channel width 16.0, corner square 16.0, corner arm 16.0**.

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

except between X = 34.2 and 38.6, where the lower crossbeam (§4.1, 8.0–10.0 in behind plane P) limits the clear height to 10.8 in.

| X (in) | 0 | 12 | 24 | 30.5 | 32.6 | 34.2–38.6 | 40 | 41.79 |
|---|---|---|---|---|---|---|---|---|
| **H (in)** | 156.0 | 111.2 | 66.4 | **42.1** | 34.3 | 10.8 (crossbeam) | 6.7 | 0 |

A robot at the 42-in starting-configuration limit fits anywhere up to X = 30.5, which is why **G302** stages robots against the alliance wall rather than against the truss. The curve depends on the (ref) member depth: a deeper frame moves it toward the wall.

**Climb reach (reference; the arithmetic behind G416).** Extensions below are given to the rung **centerline**. A hook has to wrap past the far face of a 1.5-in OD rung, so **add 0.75 in** for the reach that engages it. A robot obeying **G416** has all of its bumpers at X ≥ 48, so its FRAME PERIMETER is at X ≥ 51 and its 18-in reach ends at X = 33.0.

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

- A CACHE CRATE standing on the BASE DEPOT tray floor tops out at **13.25 in** (the tray floor's 0.25 plus 13.0 across its crown: 0.5 bottom crown + 12.0 cube + 0.5 top crown), **0.19 in** below the target. This is the tightest margin in the package, so the CRAG tag panel center height is held to **±0.15 in** at field setup, against ±0.25 in for tag position elsewhere (VISION-GUIDE §1.3).
- The underside of Shelf 1 sits at 23.25 in, 1.25 in above the panel.
- The lowest point of a Low Socket tube is at Z 22.19, 0.63 in above the target's top edge, and the tube spans 1.56 to 10.89 in outboard of the face, clear of every sightline from a camera 10–20 in high. A camera 24–36 in high looks down past the tube, which can hide part of the target of the tag beneath it (tags 8, 10, 21 and 23), and most of it from close range.

From a camera 10–20 in high, no field structure, and no SUPPLY other than the single case below, can occlude a CRAG tag. The one SUPPLY anywhere on the FIELD that reaches into the target band is an O2 CELL stood on its end in the DEPOT (its top at 14.25 in, tray floor 0.25 plus 14.0, against a 13.44-in target bottom); VISION-GUIDE §1.3 covers that case and gives the camera-height rule for it. HEADWALL lane tags sit at 12 in because that band is clear of every rung and stays ≥ 4.4 in behind plane P.

Panel poses must match `04-vision/apriltag-field-layout.json` exactly. The JSON is generated from the tag table in VISION-GUIDE §3 by `04-vision/make_layout.py` and drives every simulation.

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

- Cube, **12.0 in** per side (CRITICAL), pillowed faces with **0.5-in face crown (ref)** and **1.0-in edge fillets on all twelve edges (ref)**, **~2.0 lb**. The fillets remove material at the edges, so they do not change the envelope; they let a CRATE roll up over the 4-in BASE DEPOT lip when pushed and enter the OUTFITTER chute without catching a corner. The maximum envelope across the crown is **13.0 in**, the dimension the OUTFITTER chute is sized against. Skinned-foam construction; model rigid at nominal size.
- Color: expedition violet `#7B3FA0`.
- **CAD notes:** one part, a 12-in cube with face bulges and fillets. Robot-driving dims: the **13.0 crowned envelope vs the 16.0-in chute opening** (3.0 in clear), and the shelf slot, which needs the crown profile rather than the nominal cube. A CRATE rests on its bottom crown, so the cube's bottom plane sits 0.5 in above the shelf and each side face reaches its full 0.5 bulge at **6.5 in** above it. The binding width is at the top of the 2.0-in slot fences, where the crate is about **12.44 in** wide, leaving **0.78 in of clearance per side** rather than the 1.00 in the nominal cube suggests. That 0.78 in is the lateral placement tolerance available to a scoring mechanism. The 13.0 crown sits 4.5 in above the fences and touches nothing; two CRATES in adjacent slots (15.5-in pitch) clear each other by 2.5 in. Put the crown profile and both clearances on the same drawing view.

### 9.2 O2 CELL

- Cylinder, **5.0 in dia × 14.0 in overall length** (CRITICAL), **~1.5 lb**, with domed end caps (dome height **1.5 in** each, ref) blended to the body by a **1.0-in fillet at each cap/body junction (ref)**. The cap arc is struck through the pole and the equator, so it is not tangent to the cylinder: it meets the wall at a **28.1° tangent break**, and the fillet is what makes the surface continuous. The fillet also moves the shoulder: the full 5.0-in diameter runs **10.44 in**, not the 11.0 in between the arc endpoints. Rigid tube core with a foam sleeve; model rigid at nominal size.
- Color: body `#F2F2F0`, domed caps `#2E8B57`.
- **CAD notes:** one revolved profile. Robot-driving dims: **5.0 OD and 14.0 length vs socket ID 6.50 ± 0.125** (0.75-in radial clearance per side, 1.50 in on diameter) and vs the 7.0-in socket tube depth (7.0 in of CELL protrudes when seated). Show the clearance stack on the drawing.

### 9.3 ROPE COIL

- Torus, **10.0 in OD, 2.5-in tube section, 5.0-in ID hole** (all CRITICAL), **~1.0 lb**. As built it is one revolve: a 2.5-in-diameter profile circle whose outer edge is 5.0 in from the axis, which puts its center at r = 3.75. All three published numbers follow from that single sketch. Molded rubber/foam ring, semi-compliant; model rigid at nominal size.
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
| 9 | BASE DEPOT | lip height / lip radius / channel width / corner square / corner arm / tray floor top | 4.0 · 0.25 · 16.0 · 16.0 · 16.0 · Z = 0.25 |
| 10 | HEADWALL | width / lanes / incline | 144 · 3 × 48 · 15° from vertical (plane P at X = 48 / 600) |
| 11 | Rungs | top heights / OD / length / stagger / wrap clearance | 30, 54, 78 · 1.5 · 20.0 · ±12.0 alternating by rung, same in every lane · ≥ 4.0 behind plane P |
| 12 | OUTFITTER | opening / sill / chute centers | 30 × 16 · 24 · (0/648, 30/294) |
| 13 | Zones | apron offsets / lane tape / basecamp | 36 (shelf & peg faces), 20 (socket faces), R20 corners · 36 × 48 · X 0–48 (600–648), Y 90–234 |
| 14 | AprilTags | body / target / panel / centers / CRAG lateral | 6.5 · 8.125 · 9.0 · Z = 17.5 ± 0.15 (CRAG) / 12 (HEADWALL, panel plane X = 39/609) / 52 (OUTFITTER) · CRAG pairs at **±14.0** from each face centerline |
| 15 | Game pieces | crate / cell / coil | 12.0 cube (13.0 crowned envelope) · ⌀5.0 × 14.0 · 10.0 OD, 2.5 tube, 5.0 ID |
| 16 | Staging | cache grid / staging marks | 3×3 at 24-in pitch, center (324, 162), Latin-square types · X = 144/504, Y = 108/162/216 |

---

## Drawing set

Dimensioned multi-view SVG drawing sheets in `03-field/renderings/` (**6 files**), drawn to scale with every driving dimension labeled. The sheets are **generated** from the master dimension ledger by `03-field/renderings/generate_drawings.py` (helper library `_drawlib.py`). To change a number, change it in the ledger, change the matching constant at the top of the generator, and re-run:

```
python 03-field/renderings/generate_drawings.py
```

Do not hand-edit the SVGs. They are build output, and hand edits are lost on the next run. Every sheet carries a title block with sheet number, units note, tolerance convention, revision, and the governing document. CRITICAL dimensions are boxed; reference dimensions are suffixed `(ref)`.

1. **`field-top-view.svg`**: full 648 × 324 field plan with element placements, zones, tape, the cache grid with the Latin-square type assignment, staging marks, apron offsets, axes, and coordinate callouts.
2. **`crag.svg`**: CRAG multi-view sheet with shelf-face, socket-face, and peg-face elevations, a top (plan) view, and detail views: socket geometry (rim height, ±14 lateral, 8.0 standoff, 30° tilt, 7.0 tube, ID 6.50 ± 0.125), Summit Socket (rim 72, 8.0 standoff, 15°), peg geometry (45°, OD 1.5, exposed 10.0, laterals, both coil rest poses), shelf slots (3 × 14.0 + 1.5 fences, centers ±15.5), and depot section (lip 4.0, channel 16.0, crate-fit study).
3. **`headwall.svg`**: front elevation, side profile with the plane-P definition, the derived rung table, the BASECAMP clear-volume formula and table, the climb-reach table, a top view of the three lanes, and a rung/stagger detail (OD 1.5, length 20, ±12 stagger, 4.0 wrap clearance, tag panel at X = 39 / Z = 12).
4. **`outfitter.svg`**: field-side elevation (opening 30 × 16, sill 24, tag at 52), section through the chute (30° ramp), plan view with the 36 × 48 lane tape, and the crate-through-chute clearance study.
5. **`game-pieces.svg`**: orthographic views and sections of all three pieces with four clearance studies: crate-in-slot (12 vs 14), crate-through-chute (13 vs 16), cell-in-socket (5.0 vs 6.50 ± 0.125, 7.0 tube, 7.0 protrusion), and coil-on-peg (5.0 ID vs 1.5 OD at 45°, both rest poses).
6. **`apriltag-map.svg`**: top-view tag map with all 26 IDs, positions, Z centers, and facing normals, matching `apriltag-field-layout.json`.
