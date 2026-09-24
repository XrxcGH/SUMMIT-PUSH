# 3 ARENA

The SUMMIT PUSH ARENA includes all elements of the game infrastructure required to play a MATCH: the FIELD, two CRAGS, two HEADWALLS, four OUTFITTERS, 63 SUPPLIES, and the equipment needed for scorekeeping, field control, and MATCH lighting. This section is the authoritative physical description of the ARENA. Where an illustration in any other document disagrees with a dimension printed here, this section governs.

> *Commentary:* The ARENA is illustrated throughout this manual with nominal dimensions. Real fields are built by humans; teams should expect variation of up to ±1 in and ±1° on non-critical dimensions and should design accordingly. Dimensions explicitly flagged as toleranced (the O2 socket inside diameter, §3.3.2) are held to the stated tolerance on every official field. Every element is fully dimensioned in the FIELD CAD PACKAGE (`03-field/FIELD-CAD-PACKAGE.md`) for exact reproduction in CAD, and its appearance is specified in `03-field/MATERIALS-AND-COLORS.md`.

## 3.1 The FIELD

The FIELD is a 54 ft × 27 ft (648 in × 324 in) carpeted area bounded by guardrails and alliance walls. The guardrail is a 20-in-tall barrier around the long sides and portions of the short sides of the FIELD. Each short end of the FIELD is closed by an alliance wall: a solid barrier containing three standard driver stations, one per team on the ALLIANCE. Each driver station provides a shelf, a clear polycarbonate window, the standard FMS connection point for the OPERATOR CONSOLE, and FIELD-provided **E-STOP** and **A-STOP** buttons. The E-STOP renders that team's ROBOT inoperable for the remainder of the MATCH; the A-STOP ends that ROBOT's AUTO immediately, after which the ROBOT may be enabled normally at the start of TELEOP. Either button may be pressed by any DRIVE TEAM member at any time (see **G401**). The two OUTFITTER chute openings (§3.5) pierce each alliance wall near its corners.

### 3.1.1 Coordinate frame

All coordinates in this manual, in the FIELD drawings, and in the AprilTag layout file use a single always-blue-origin NWU convention:

- **Origin:** the right-hand corner of the Blue alliance wall, as seen from the Blue driver stations looking down-field — the corner where the Blue alliance wall meets the guardrail at Y = 0.
- **+X** points down-field from the Blue alliance wall toward the Red alliance wall.
- **+Y** points to the left from the Blue drivers' perspective.
- **+Z** points up from the carpet.

The FIELD centerline is the line X = 324. The FIELD center is (324, 162). Heights ("Z") are measured from the carpet surface. The FIELD layout is 180° rotationally symmetric about the FIELD center: every Red element is the Blue element rotated 180° about (324, 162). There is one coordinate frame for both ALLIANCES; it never flips.

### 3.1.2 FIELD LEDs

Each long-side guardrail (Y = 0 and Y = 324) carries a continuous 1.0-in-wide LED band let into its top rail, frosted lens facing inward, lens center 19.0 in above the carpet. Each band is divided at the FIELD centerline into two 324-in ALLIANCE segments, so each ALLIANCE has two segments, one on each side of the FIELD. Segment states:

- **Green** — the FIELD is safe for team members to enter or reach over (**G101**).
- **White** — the FORECAST, displayed in both ALLIANCES' segments at T = 0 of AUTO (§4.3.1): one lit block for WHITEOUT, two for ICEFALL, three for GALE.
- **ALLIANCE color** — that ALLIANCE's declared ROUTE, from the "field ready" signal through MATCH start (§4.2.3, **G304**): one lit block for LOW ROUTE, two for MID ROUTE, three for HIGH ROUTE.
- **Dark** — at all other times.

FIELD LEDs are indicators only. They are never the scoring or safety authority; FIELD STAFF direction governs FIELD entry, and referee-recorded state governs scoring.

## 3.2 Zones and markings

All zone boundaries are marked with tape on the carpet. ALLIANCE-specific zones are marked in the owning ALLIANCE's color; neutral marks are white. The tape is part of the zone it bounds: a zone extends to the outer edge of its tape.

| Zone / mark | Alliance | Boundary (coordinates) | Size |
|---|---|---|---|
| **BASECAMP** (= **HEADWALL ZONE**) | Blue | X 0–48, Y 90–234 | 48 in deep × 144 in wide |
| | Red | X 600–648, Y 90–234 | mirror |
| **OUTFITTER LANE** (×2 per alliance) | Blue | 36 in wide, centered on each chute (Y = 30 and Y = 294), extending 48 in into the FIELD from the alliance wall (X 0–48) | 36 × 48 in each |
| | Red | X 600–648, centered Y = 294 and Y = 30 | mirror |
| **CRAG APRON** | Blue | offset **36 in** outward from the SHELF FACE and the PEG FACE, **20 in** outward from each SOCKET FACE, corners swept as 20-in-radius arcs | band around the CRAG |
| | Red | mirror | mirror |
| **CLIMB LINE** | alliance color, dashed outside BASECAMP | the X = 48 (Blue) / X = 600 (Red) line carried across the full FIELD width, Y 0–324; over Y 90–234 it coincides with the BASECAMP boundary and needs no second line | the plane **G416** is called against |
| **FIELD centerline** | neutral white | 2-in line at X = 324 running the full width, Y 0–324, interrupted where the two CRAG footprints cross it (the BASE DEPOT trays stop 8 in short of the line) | the line **G402** and **G502** are both called against |
| **CENTER CACHE band** | neutral | X 300–348, Y 108–216 | 48 × 108 in |
| **CENTER CACHE staging marks** | neutral | 9 white taped marks in a 3 × 3 grid, 24 in spacing, centered on (324, 162) | grid at X = 300/324/348 × Y = 138/162/186 |
| **Alliance staging marks** | Blue | 3 taped marks at X = 144; Y = 108, 162, 216 | 12 ft from the Blue alliance wall |
| | Red | X = 504; Y = 108, 162, 216 | mirror |

BASECAMP is the taped area between each alliance wall and its HEADWALL. ROBOTS begin every MATCH in their BASECAMP (§3.2.1). The same taped area is also the HEADWALL ZONE: during the ENDGAME period and the climb assessment that follows it, opponent contact with a ROBOT in this zone is penalized (see Game Rules, Section 5). The two names refer to one and the same taped region; BASECAMP describes its starting and parking role, HEADWALL ZONE its ENDGAME-protection role.

OUTFITTER LANES are protected loading corridors; opposing ROBOTS may not contact ROBOTS in them (see Game Rules). CRAG APRONS give each ALLIANCE a line-call placement protection at its own CRAG: a ROBOT whose BUMPERS intersect its *own* ALLIANCE's APRON may not be contacted by an opponent. The APRON does not restrict an opponent's movement through the area when no protected ROBOT is present. Note the consequence of the shallower SOCKET FACE offset: a socket rim stands 8.0 in out from its face, so a ROBOT using the full 18-in extension has its FRAME PERIMETER 26 in out and its BUMPERS 23 in out — 3 in beyond the 20-in tape, and unprotected. Protection at a SOCKET FACE requires engaging the rim with **15 in of extension or less**; at the 36-in SHELF and PEG faces no reachable position is unprotected.

The APRON offset is 36 in on the SHELF FACE and the PEG FACE and 20 in on the two SOCKET FACES. The reduced offset on the SOCKET FACES is dimensional, not tactical: the corridor between the two CRAGS is 108 in wide (Y 108–216), the staged CENTER CACHE occupies Y 131.5–192.5 of it across the crowned 13.0-in crate envelope, leaving 3.5 in of clearance at each end, and two 36-in aprons would leave only 36 in of corridor and would swallow the staged SUPPLIES. With 20-in socket-face aprons, the two APRONS occupy Y 108–128 and Y 196–216, leaving a 68-in open corridor that contains the whole CENTER CACHE. That corridor, and every transit lane on the FIELD, remains fully open to defense.

> *Example:* A Red ROBOT drives through the Blue CRAG APRON while no Blue ROBOT is nearby. No rules are violated — the APRON is a contact-protection boundary, not a keep-out zone.

### 3.2.1 Starting positions

Immediately before the MATCH, each ROBOT must be positioned entirely within its ALLIANCE's BASECAMP and in contact with its alliance wall. Each ROBOT may hold up to one preloaded SUPPLY of any type (§3.6.1).

> *Commentary:* BASECAMP is the wedge under the leaning HEADWALL, so the clear height available to a ROBOT falls as it moves down-field. The field-side face of the truss lies at X = 43.86 − 0.268·Z for Blue, so the clear height at any X is H(X) = 3.732 × (43.86 − X): 42.0 in of clearance is available anywhere up to X = 32.6, and the last 4.1 in of the taped zone is occupied by truss structure. A ROBOT at the R104 42-in starting height therefore stages against the alliance wall, which is why the contact requirement names the wall and not the truss. The full clear-volume curve is published in the FIELD CAD PACKAGE §4.1.

## 3.3 The CRAG

Each ALLIANCE owns one CRAG: a rock-spire scoring structure straddling the FIELD centerline. The Blue CRAG is centered at (324, 240); the Red CRAG at (324, 84). Each CRAG has a 48 × 48 in footprint and rises to a spire top 90 in above the carpet. The body of the CRAG presents four vertical scoring faces around the footprint; a central spire carries the highest scoring features and the SUMMIT BEACON.

Face names are assigned from the owning ALLIANCE's approach:

| Element | Blue CRAG | Red CRAG | Features |
|---|---|---|---|
| **SHELF FACE** | −X face (plane X = 300), faces the Blue alliance wall | +X face (plane X = 348), faces the Red alliance wall | Shelf 1, Shelf 2, the Summit Socket, the BASE DEPOT |
| **SOCKET FACE** ×2 | ±Y faces (planes Y = 216 and Y = 264) | ±Y faces (planes Y = 60 and Y = 108) | one Low Socket and one Mid Socket per face |
| **PEG FACE** | +X face (plane X = 348), faces the Red alliance wall | −X face (plane X = 300), faces the Blue alliance wall | Low and Mid Pegs |
| **spire** | top of structure | top of structure | High Pegs, SUMMIT BEACON |

Because each CRAG scores on all four of its faces, a defender can never blockade every approach at once.

### 3.3.1 SHELF FACE

The SHELF FACE carries two horizontal shelves spanning the width of the face:

- **Shelf 1:** shelf top surface at 24 in, divided into 3 slots, each 14.0 in wide, separated by slot fences 1.5 in wide and 2.0 in tall. Slot centers lie at −15.5, 0, and +15.5 in from the face centerline.
- **Shelf 2:** shelf top surface at 42 in, same slot layout.

Shelves are 14.0 in deep and accept CACHE CRATES only, placed flat. A CACHE CRATE rests on its bottom crown, so its side faces reach their full 0.5-in bulge 6.5 in up — well above the 2.0-in fences. At the fence tops the crate is 12.44 in across, giving a placement **0.78 in of lateral tolerance per side**, and its 13.0-in crown clears the fences entirely; crates in adjacent slots clear each other by 2.5 in. Each shelf slot SCORES at most one SUPPLY (six crates per CRAG on shelves); extra SUPPLIES resting in or on an occupied slot are not SCORED and satisfy no requirement (see Match Play, Section 4).

### 3.3.2 SOCKET FACES and the Summit Socket

Each of the two SOCKET FACES carries two open-topped cylindrical sockets, inserted from above. Every socket's rim center stands **8.0 in out from its face plane**, measured normal to the face, on a bracket beneath the tube:

- **Low Socket:** rim at 30 in, ±14.0 in lateral on the shelf-face side of the face centerline, tube tilted 30° from vertical, tilting outward toward the approaching ROBOT. One per SOCKET FACE (2 per CRAG).
- **Mid Socket:** rim at 54 in, ±14.0 in lateral on the peg-face side, tube tilted 30° from vertical. One per SOCKET FACE (2 per CRAG).
- **Summit Socket:** one per CRAG, on the SHELF FACE, on the CRAG's centerline, rim at 72 in, tube tilted 15° from vertical, tilting outward toward the owning ALLIANCE. A SCORED O2 CELL leans out of it toward the owning ALLIANCE's driver stations.

Sockets accept O2 CELLS only. Each socket SCORES at most one SUPPLY; extra SUPPLIES resting in or on an occupied socket are not SCORED and satisfy no requirement. The tube is 7.0 in long along its axis with a closed bottom, so a seated 14.0-in O2 CELL stands 7.0 in proud of the rim along the axis — clearly visible from the driver stations and from the referee positions.

The two sockets on a face are not approached from the same standoff. The BASE DEPOT's corner arm runs 16.0 in along each SOCKET FACE from the SHELF FACE, and the Low Socket sits directly above it, so a ROBOT servicing the Low Socket parks against the arm and reaches 11.75 in; the Mid Socket, on the PEG-FACE side, is clear of the arm and is 5.0 in of reach from BUMPERS on the face. Both are inside the **R105** limit.

**Toleranced dimension:** socket inside diameter 6.50 in ± 0.125 in. This dimension is held to the stated tolerance on every official field and is carried as a toleranced callout in the FIELD CAD PACKAGE drawing set. It provides 0.75 in of nominal radial clearance per side (1.50 in on diameter) for the 5.0-in O2 CELL.

> *Commentary:* The socket tolerance is called out explicitly because the insertion task lives or dies on it. At 6.50 in ID the task looks harder than it is; a field-build error that shrinks the mouth flips it from "achievable with alignment" to "frustrating." FIELD STAFF verify this dimension at field setup.

### 3.3.3 PEG FACE and High Pegs

The PEG FACE carries four pegs, and the spire carries two more:

- **Low Pegs** ×2, roots at 30 in, ±14.0 in from the face centerline
- **Mid Pegs** ×2, roots at 54 in, ±14.0 in from the face centerline
- **High Pegs** ×2 on the spire, roots at 78 in, ±7.0 in from the spire centerline

All pegs are 1.5 in OD, angled 45° upward from the face, with 10.0 in exposed and a fully rounded tip. Pegs accept ROPE COILS only, hung over the peg. Each peg SCORES at most one SUPPLY; extra SUPPLIES resting in or on an occupied peg are not SCORED and satisfy no requirement. Heights are measured to the peg root at the face.

A ROPE COIL dropped over a peg settles into a near-vertical plane parallel to the CRAG face and wedges there: the 5.0-in hole over a 1.5-in peg permits at most about 48° (47.9°) of tilt away from perpendicular, and a vertical hang requires 45°, so a SCORED COIL is captured rather than balanced. Its center comes to rest roughly 1 in above the peg root.

### 3.3.4 BASE DEPOT

The BASE DEPOT is a tray whose floor sits 0.25 in above the carpet, with a lip whose top is 4.0 in above the carpet, running along the base of the SHELF FACE and wrapping 16.0 in around both of that face's corners onto the SOCKET FACES. The channel is 16.0 in deep measured from the CRAG face. In plan it is a continuous open-topped U: a 16 × 80 in outer leg parallel to the SHELF FACE, closed at both ends by the corner squares, with a 16 × 16 in arm running back along each SOCKET FACE. Because the shelves overhang 14.0 in of that channel and span only the 48-in width of the SHELF FACE, the outer 2.0 in of the shelf-face leg is open from above, as are both outer corner squares and, in part, both corner arms — each arm is overhung by its Low Socket tube, so only the corner squares are wide enough to drop a CACHE CRATE or a ROPE COIL straight in; the shelf-face leg is otherwise loaded by pushing SUPPLIES in over the lip, with at least 19.0 in of clearance beneath Shelf 1 and its gussets against a crowned CACHE CRATE's 13.0 in. The DEPOT accepts any SUPPLY in any orientation, whether pushed, dropped, or placed. Because a SUPPLY resting on another is not SCORED (Section 4.4.1), capacity is a single-layer packing limit: roughly **8 CACHE CRATES**, or about **12 SUPPLIES** in a mixed load.

A SUPPLY is SCORED in the BASE DEPOT when it is at rest, its only support is the tray floor, and it lies entirely within the vertical projection of the DEPOT channel. A SUPPLY supported by the lip, by the carpet outside the tray, or by another SUPPLY is not SCORED. A SUPPLY that stands taller than the 4-in lip is SCORED so long as the tray floor alone supports it. FIELD STAFF may level heaped SUPPLIES during MATCH stoppages; they will not otherwise adjust DEPOT contents during a MATCH.

> *Example:* A ROPE COIL lands draped over the DEPOT lip, half in and half out. It is not SCORED — the lip carries part of its weight. A second COIL thrown on top of a full tray comes to rest on other COILS rather than on the tray floor; it is likewise not SCORED. A CACHE CRATE standing on the tray floor rises well above the lip and is SCORED.

### 3.3.5 Tier LED rings and SUMMIT BEACON

Each CRAG carries three LED tier rings wrapping the structure at 30 in, 54 in, and 78 in, and a SUMMIT BEACON: the top 12 in of the spire (Z 78 to 90) is a translucent lantern with its luminous center at 84 in.

- A tier ring lights in the owning ALLIANCE's color when the corresponding CAMP is established (30 in → CAMP I, 54 in → CAMP II, 78 in → HIGH CAMP). Tier rings latch: once lit, a ring stays lit for the remainder of the MATCH, even if SUPPLIES are later dislodged.
- The SUMMIT BEACON lights when all three CAMPS are established.
- The FORECAST (white) and each ALLIANCE's declared ROUTE are displayed on the FIELD LEDs (§3.1.2), not on the tier rings (see Match Play, Section 4). A tier ring carries latched CAMP state only, which is why it never needs to change colour or pattern once lit.

The LEDs are decorative confirmation only; they are never the scoring authority. A CAMP is established at the moment its required SUPPLIES are simultaneously SCORED, as determined by referees and the scoring system, whether or not the corresponding ring lights. If lighting and the SCORED state ever disagree, the SCORED state governs.

### 3.3.6 CRAG APRON

The CRAG APRON (§3.2) is the taped boundary offset 36 in outward from the SHELF FACE and the PEG FACE and 20 in outward from each SOCKET FACE, with 20-in-radius arcs sweeping the corners. Each APRON is taped in its CRAG's ALLIANCE color. Its sole rules function is opponent-contact protection for ROBOTS of the owning ALLIANCE whose BUMPERS intersect it; see Game Rules, Section 5.

## 3.4 The HEADWALL

Each ALLIANCE has one HEADWALL: a climbing truss standing in front of its alliance wall. All HEADWALL geometry derives from one reference plane:

> **PLANE P** contains the horizontal line {X = 48 (Blue) / X = 600 (Red), Z = 0} spanning Y 90–234, tilted **15° from vertical with the top leaning toward the alliance wall**. ROBOTS climb the FIELD side of plane P.

Each HEADWALL is 144 in wide and divided into three independent 48-in lanes (Blue lane centers at Y = 114, 162, 210). Lanes are structurally independent: load or motion in one lane does not disturb the others. One ROBOT per lane (see Game Rules).

Each lane carries three rungs of 1.5 in OD and 20.0 in length, with their centerlines lying in plane P:

| Rung | Height (carpet to top of rung) | Lateral offset from the lane centerline |
|---|---|---|
| **LEDGE RUNG** | 30 in | **−12.0 in** — identical in all three lanes |
| **CAMP RUNG** | 54 in | **+12.0 in** — identical in all three lanes |
| **SUMMIT RUNG** | 78 in | **−12.0 in** — identical in all three lanes, same as the LEDGE RUNG |

Because of the 15° lean, each rung sits approximately 6.4 in horizontally behind (toward the alliance wall from) the rung below it. The lateral stagger is the same in every lane — LEDGE −12, CAMP +12, SUMMIT −12 — so successive rungs within a lane are 24.0 in apart centre-to-centre while rungs at the same height in adjacent lanes stay 48.0 in apart (28.0 in end to end, room for three ROBOTS to hang side by side), and a 20.0-in rung at ±12.0 in leaves **no lateral position that engages two successive rungs**: the LEDGE RUNG spans lane-centerline −22 to −2 while the CAMP RUNG spans +2 to +22. A climber therefore cannot follow the rung line with one fixed hook pair. The stagger alternates with period two, so the LEDGE and SUMMIT RUNGS share the −12.0 offset while the CAMP RUNG sits at +12.0, and there are exactly two routes to the top: the **two-handoff traversal**, LEDGE → CAMP → SUMMIT, each step 24 in up, 6.4 in back and 24 in across; or a **direct LEDGE → SUMMIT reach** at one lateral position, 48 in up and 12.9 in back — 49.7 in measured in plane P against 24.9 in for a single step. Both are legal. The direct route trades all the lateral motion for twice the vertical reach in one move, which is the harder mechanism; the traversal is the one most climbers will build. Only two non-overlapping lateral positions fit a 20.0-in rung in a 48-in lane, so the LEDGE and SUMMIT RUNGS sharing an offset is a consequence of the rung geometry, not a choice.

All truss structure lies at least 4.0 in behind plane P, measured normal to P, except the two end brackets of each rung, which may enter that band within 2.0 in of the rung end. Hook wrap is therefore clear over the middle **16.0 in** of every 20.0-in rung, and a hook must engage inside that band.

The taped HEADWALL ZONE (coincident with BASECAMP, §3.2) lies beneath and behind the HEADWALL, between the truss base and the alliance wall. From the start of the ENDGAME period until climb assessment is complete, opponents contacting a ROBOT in this zone commit a MAJOR FOUL, escalating to a YELLOW CARD if a hanging ROBOT falls as a result (see Game Rules). Climbing is legal at any time in the MATCH; the zone protection applies only in that window, and a ROBOT may not contact a rung while any part of its BUMPERS is on the alliance-wall side of the CLIMB LINE — X = 48 in for Blue, X = 600 in for Red — unless it is then supported solely by rungs, or is still touching a rung it took hold of while so supported within the preceding 5 seconds (**G416**).

> *Commentary:* The three-lane design exists so that all three ROBOTS of an ALLIANCE can climb simultaneously with zero traffic conflict. The 15° lean and the 24-in lateral alternation are the difficulty; the lane independence is the mercy. **G416** exists because the truss leans back over BASECAMP: without it, a ROBOT could park under the SUMMIT RUNG and reach it with a purely vertical mast, and the traversal would be decorative.

## 3.5 OUTFITTERS

Each ALLIANCE has two OUTFITTERS, one at each corner of its alliance wall. Each OUTFITTER consists of a chute opening through the alliance wall, a human-player station behind it, and the taped OUTFITTER LANE in front of it.

- **Chute opening:** 30 in wide × 16 in tall, with the sill (bottom edge) at 24 in above the carpet, so the opening spans Z 24–40. Blue chutes are centered at (0, 30) and (0, 294); Red chutes at (648, 294) and (648, 30). The 16-in height clears the 12.0-in CACHE CRATE, whose pillowed faces give it a 13.0-in maximum envelope, with 3.0 in to spare.
- **Human players:** exactly one HUMAN PLAYER is stationed at each OUTFITTER — two per ALLIANCE, drawn from any of the ALLIANCE's three DRIVE TEAMS and assigned before the "field ready" signal (see **G307**). HUMAN PLAYERS feed SUPPLIES through the chute into the FIELD. A SUPPLY may be slid, dropped, or rolled through the chute; HUMAN PLAYERS may not reach beyond the plane of the chute opening (**G102**).
- **Stock:** all SUPPLIES not staged on the FIELD or preloaded (§3.6.1) begin the MATCH stocked at the ALLIANCE's two OUTFITTERS, divided between them at the ALLIANCE's discretion.
- **Restocking:** any SUPPLY that leaves the FIELD is returned by FIELD STAFF to the nearest OUTFITTER chute at the next safe opportunity — the chute of the ALLIANCE on that side of the FIELD, which may be the opposing ALLIANCE's chute — and re-enters play through normal human-player feeding. SUPPLIES are never re-staged mid-MATCH to FIELD marks.

The OUTFITTER LANE (36 in wide × 48 in deep, §3.2) in front of each chute is a no-defense zone: opponents may not contact ROBOTS within it (see Game Rules).

## 3.6 SUPPLIES

SUMMIT PUSH is played with three SUPPLY types, 63 SUPPLIES per MATCH in total, 21 of each type. "SUPPLY" and "GAME PIECE" are synonymous; SUPPLY is the term used in the rules.

| | **CACHE CRATE** | **O2 CELL** | **ROPE COIL** |
|---|---|---|---|
| Shape | cube, pillowed faces | cylinder, domed caps | torus (ring) |
| Dimensions | 12.0 in cube (13.0 in max envelope with the 0.5-in face crown) | 5.0 in dia × 14.0 in long | 10.0 in OD, 2.5 in tube (5.0 in ID hole) |
| Weight | ~2.0 lb | ~1.5 lb | ~1.0 lb |
| Official construction | sewn ripstop-nylon skin over PU foam core | 4.0-in OD rigid tube core, 0.5-in EVA foam sleeve, molded foam caps | solid molded rubber/foam ring |
| Official color | expedition violet `#7B3FA0` | body `#F2F2F0`, domed caps `#2E8B57` | amber `#D9A441` |
| Scores on | Shelves, BASE DEPOT | Sockets, BASE DEPOT | Pegs, BASE DEPOT |
| Count per MATCH | 21 | 21 | 21 |

All three SUPPLIES are durable enough to be driven over; a SUPPLY damaged beyond play is removed and not replaced mid-MATCH. No SUPPLY is colored in either ALLIANCE's color, so no SUPPLY can be mistaken for an ALLIANCE element by a referee, a DRIVE TEAM, or a vision pipeline.

### 3.6.1 Staging

At the start of each MATCH, SUPPLIES are staged as follows:

| Location | Supplies | Detail |
|---|---|---|
| CENTER CACHE (neutral) | 3 CRATES, 3 O2 CELLS, 3 ROPE COILS | one SUPPLY per white mark of the 3 × 3 grid (§3.2), arranged so that each type appears once per row and once per column; the assignment is published in the FIELD SETUP CHART (`03-field/FIELD-CAD-PACKAGE.md`, Section 6) |
| Alliance staging marks (per alliance) | 2 CRATES, 2 O2 CELLS, 2 ROPE COILS | at the three taped marks at X = 144 (Blue) / X = 504 (Red), Y = 108/162/216; two SUPPLIES of one type per mark |
| Robot preloads (per alliance) | up to 1 per ROBOT, any type | in contact with the ROBOT in its starting position |
| OUTFITTERS (per alliance) | 7 CRATES, 7 O2 CELLS, 7 ROPE COILS | divided between the ALLIANCE's two chutes at its discretion; preloads are drawn from this stock |

Accounting per SUPPLY type: of each type's 21 SUPPLIES, 3 begin neutral in the CENTER CACHE, 2 begin on each ALLIANCE's staging marks (4 total), and 7 begin in each ALLIANCE's OUTFITTER stock (14 total). Preloads are drawn from an ALLIANCE's OUTFITTER stock during setup; preloads not taken remain at the OUTFITTERS.

The CENTER CACHE arrangement places one SUPPLY of each type in each row of the grid, so that neither ALLIANCE is nearer to any one type than the other. A strictly rotation-invariant 3/3/3 assignment is impossible on a 3 × 3 grid — the 180° rotation fixes exactly one mark and pairs the other eight — and the row-balanced arrangement is the closest achievable: aggregate haul distance from the nine marks to each CRAG is identical for both ALLIANCES, and no single type differs by more than 1%.

## 3.7 AprilTags

The ARENA carries 26 AprilTags from the 36h11 family for ROBOT pose estimation and target alignment.

**Panel construction:** each tag image is 6.5 in square (the 36h11 data body), printed on an 8.125-in-square target including its white border, mounted on a 9.0-in-square panel. Tag centers are given below; "Z center" is the height of the tag center above the carpet. Close-range tags sit low: the eight on each CRAG at a 17.5-in center height, the three on each HEADWALL at 12 in. Both are inside the frame of a single camera mounted 10–20 in above the carpet, which serves every precision approach on the FIELD. A pair on each CRAG face is centered ±14 in from the face centerline. The 17.5-in CRAG height is chosen against the tallest things that can stand in front of a tag: a CACHE CRATE standing in the BASE DEPOT — 13.25 in, the tray floor's 0.25 plus 13.0 to its crowned apex — tops out 0.19 in below the tag target, and the underside of Shelf 1 sits 1.25 in above the panel. One SUPPLY does reach into the target band: an O2 CELL stood on its end in the DEPOT, 14.0 in against a 13.44-in target bottom. `04-vision/VISION-GUIDE.md` §1.3 carries that case and the camera height it implies.

| ID | Location | Position (X, Y) | Z center | Facing |
|---|---|---|---|---|
| 1 | Blue OUTFITTER chute | (0, 30) | 52 in | +X |
| 2 | Blue OUTFITTER chute | (0, 294) | 52 in | +X |
| 3 | Blue HEADWALL lane 1 | (39, 114) | 12 in | +X |
| 4 | Blue HEADWALL lane 2 | (39, 162) | 12 in | +X |
| 5 | Blue HEADWALL lane 3 | (39, 210) | 12 in | +X |
| 6 | Blue CRAG, SHELF FACE | (300, 226) | 17.5 in | −X |
| 7 | Blue CRAG, SHELF FACE | (300, 254) | 17.5 in | −X |
| 8 | Blue CRAG, +Y SOCKET FACE | (310, 264) | 17.5 in | +Y |
| 9 | Blue CRAG, +Y SOCKET FACE | (338, 264) | 17.5 in | +Y |
| 10 | Blue CRAG, −Y SOCKET FACE | (310, 216) | 17.5 in | −Y |
| 11 | Blue CRAG, −Y SOCKET FACE | (338, 216) | 17.5 in | −Y |
| 12 | Blue CRAG, PEG FACE | (348, 226) | 17.5 in | +X |
| 13 | Blue CRAG, PEG FACE | (348, 254) | 17.5 in | +X |
| 14 | Red OUTFITTER chute | (648, 294) | 52 in | −X |
| 15 | Red OUTFITTER chute | (648, 30) | 52 in | −X |
| 16 | Red HEADWALL lane 1 | (609, 210) | 12 in | −X |
| 17 | Red HEADWALL lane 2 | (609, 162) | 12 in | −X |
| 18 | Red HEADWALL lane 3 | (609, 114) | 12 in | −X |
| 19 | Red CRAG, SHELF FACE | (348, 98) | 17.5 in | +X |
| 20 | Red CRAG, SHELF FACE | (348, 70) | 17.5 in | +X |
| 21 | Red CRAG, −Y SOCKET FACE | (338, 60) | 17.5 in | −Y |
| 22 | Red CRAG, −Y SOCKET FACE | (310, 60) | 17.5 in | −Y |
| 23 | Red CRAG, +Y SOCKET FACE | (338, 108) | 17.5 in | +Y |
| 24 | Red CRAG, +Y SOCKET FACE | (310, 108) | 17.5 in | +Y |
| 25 | Red CRAG, PEG FACE | (300, 98) | 17.5 in | −X |
| 26 | Red CRAG, PEG FACE | (300, 70) | 17.5 in | −X |

Red tag positions are the Blue positions rotated 180° about the FIELD center: the layout is one fixed map in the single always-blue-origin frame, and Red ID = Blue ID + 13. OUTFITTER tags are mounted on the alliance wall centered above each chute; HEADWALL tags are mounted plumb on the lane centerline of the truss lower crossbeam at tag plane X = 39 (Blue) / X = 609 (Red), which is behind plane P at every point of the panel so that nothing intrudes into the climbing volume; CRAG tags face outward, perpendicular to their face.

> *Commentary:* Every scoring approach on the FIELD has a tag pair or a tag square-on to it at close range: shelf placements, socket insertions, peg hangs, chute pickup, and lane alignment for the ENDGAME climb are all vision-assistable without full-field pose. Full-field pose estimation is only *required* for contested CENTER CACHE autos. Because every close-range tag sits between 12 and 17.5 in, one camera mounted 10–20 in above the carpet serves all of them — toward the upper end of that band if it is the ROBOT's only camera, for the reason in the vision guide's §1.3 — an O2 CELL stood on end in the DEPOT is the one SUPPLY that reaches into a tag's target band, and its domed cap clips a low camera's view of the bottom edge.

A machine-readable layout in WPILib AprilTag field schema (meters, always-blue-origin NWU) is published at `04-vision/apriltag-field-layout.json`; mounting details, calibration guidance, and simulation setup are in the VISION GUIDE (`04-vision/VISION-GUIDE.md`).
