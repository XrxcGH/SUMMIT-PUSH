# 3 ARENA

The SUMMIT PUSH ARENA includes all elements of the game infrastructure required to play a MATCH: the FIELD, two CRAGS, two HEADWALLS, four OUTFITTERS, 63 SUPPLIES, and the equipment for scorekeeping, field control, and MATCH lighting. This section is the authoritative physical description of the ARENA. Where an illustration in any other document disagrees with a dimension given here, this section governs.

> *Commentary:* The ARENA is illustrated throughout this manual with nominal dimensions. Fields are built by hand, so teams should expect variation of up to ±1 in and ±1° on non-critical dimensions and design accordingly. Dimensions flagged as toleranced (the O2 socket inside diameter, §3.3.2, and the CRAG tag center height, §3.7) are held to the stated tolerance on every official field. Every element is fully dimensioned for CAD reproduction in the FIELD CAD PACKAGE (`03-field/FIELD-CAD-PACKAGE.md`), and its appearance is specified in `03-field/MATERIALS-AND-COLORS.md`.

## 3.1 The FIELD

The FIELD is a 54 ft × 27 ft (648 in × 324 in) carpeted area bounded by guardrails and alliance walls. The guardrail is a 20-in-tall barrier along the long sides of the FIELD. Each short end of the FIELD is closed by an alliance wall: a solid barrier containing three standard driver stations, one per team on the ALLIANCE. Each driver station provides a shelf, a clear polycarbonate window, the standard FMS connection point for the OPERATOR CONSOLE, and FIELD-provided **E-STOP** and **A-STOP** buttons. The E-STOP renders that team's ROBOT inoperable for the remainder of the MATCH. The A-STOP ends that ROBOT's AUTO immediately; the ROBOT may then be enabled normally at the start of TELEOP. Any DRIVE TEAM member may press either button at any time (see **G401**). Each alliance wall has two OUTFITTER chute openings near its corners (Section 3.5).

*Figure 3-1. FIELD layout in plan view, Blue alliance wall at left. Dimensioned drawing: Plate 1 of the field drawing set.*

![FIELD layout, plan view](../figures/field-plan.png)

### 3.1.1 Coordinate Frame

All coordinates in this manual, in the FIELD drawings, and in the AprilTag layout file use a single always-blue-origin NWU convention:

- **Origin:** the right-hand corner of the Blue alliance wall as seen from the Blue driver stations looking down-field, where the Blue alliance wall meets the guardrail at Y = 0.
- **+X** points down-field from the Blue alliance wall toward the Red alliance wall.
- **+Y** points to the left from the Blue drivers' perspective.
- **+Z** points up from the carpet.

The FIELD centerline is the line X = 324. The FIELD center is (324, 162). Heights ("Z") are measured from the carpet surface. The FIELD layout is 180° rotationally symmetric about the FIELD center: every Red element is the Blue element rotated 180° about (324, 162). Both ALLIANCES use this one coordinate frame; it is never flipped for Red.

### 3.1.2 FIELD LEDs

Each long-side guardrail (Y = 0 and Y = 324) carries a continuous 1.0-in-wide LED band set into its top rail, with a frosted lens facing inward and the lens center 19.0 in above the carpet. Each band is divided at the FIELD centerline into two 324-in ALLIANCE segments, so each ALLIANCE has two segments, one on each side of the FIELD. Segment states:

- **Green:** the FIELD is safe for team members to enter or reach over (**G101**).
- **White:** the FORECAST, displayed in both ALLIANCES' segments from T=0 until the end of AUTO (Section 4.3.1). One lit block means WHITEOUT, two ICEFALL, three GALE.
- **ALLIANCE color:** that ALLIANCE's declared ROUTE, from the "field ready" signal until T=0, when the FORECAST replaces it (Section 4.2.3, **G304**). One lit block means LOW ROUTE, two MID ROUTE, three HIGH ROUTE.
- **Dark:** at all other times.

FIELD LEDs are indicators only and are never the scoring or safety authority. FIELD STAFF direction governs FIELD entry, and referee-recorded state governs scoring.

## 3.2 Zones and Markings

All zone boundaries are marked with tape on the carpet. ALLIANCE-specific zones are marked in the owning ALLIANCE's color; neutral marks are white. The tape is part of the zone it bounds: a zone extends to the outer edge of its tape.

**Table 3-1: Zones and markings**

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

BASECAMP is the taped area between each alliance wall and its HEADWALL. ROBOTS begin every MATCH in their BASECAMP (Section 3.2.1). The same taped area is also the HEADWALL ZONE: during the ENDGAME period and the climb assessment that follows it, opponent contact with a ROBOT in this zone is penalized (**G412**). BASECAMP describes its starting and parking role, and HEADWALL ZONE its ENDGAME protection role.

OUTFITTER LANES are protected loading corridors: opponents may not enter them or contact ROBOTS in them (**G410**). The CRAG APRON is a line-call placement protection at each ALLIANCE's own CRAG: a ROBOT whose BUMPERS intersect its own ALLIANCE's APRON may not be contacted by an opponent (**G407**). The APRON does not restrict an opponent's movement through the area when no protected ROBOT is present.

The APRON offset is 36 in on the SHELF FACE and the PEG FACE and 20 in on the two SOCKET FACES. At a SOCKET FACE, the shallower offset limits protection. A socket rim stands 8.0 in out from its face, so a ROBOT using the full 18-in extension has its FRAME PERIMETER 26 in out and its BUMPERS 23 in out: 3 in beyond the 20-in tape, and unprotected. To be protected at a SOCKET FACE, a ROBOT must engage the rim with 15 in of extension or less. At the SHELF FACE and PEG FACE, with their 36-in offset, every reachable position is protected.

The SOCKET FACE offset is reduced for space. The corridor between the two CRAGS is 108 in wide (Y 108–216), and the staged CENTER CACHE occupies Y 131.5–192.5 of it, measured across the crowned 13.0-in crate envelope. Two 36-in APRONS would leave only 36 in of corridor and would cover the staged SUPPLIES. With 20-in APRONS on the SOCKET FACES, the two APRONS occupy Y 108–128 and Y 196–216, leaving a 68-in open corridor that contains the whole CENTER CACHE with 3.5 in of clearance at each end. That corridor, and every transit lane on the FIELD, remains fully open to defense.

> *Example:* A Red ROBOT drives through the Blue CRAG APRON while no Blue ROBOT is nearby. No rule is violated. The APRON restricts contact with a protected ROBOT and places no limit on movement through it.

### 3.2.1 Starting Positions

Immediately before the MATCH, each ROBOT must be positioned entirely within its ALLIANCE's BASECAMP and in contact with its alliance wall. Each ROBOT may hold up to one preloaded SUPPLY of any type (Section 3.6.1).

> *Commentary:* BASECAMP is the wedge under the leaning HEADWALL, so the clear height available to a ROBOT falls as it moves down-field. The lower face of the truss lies at X = 41.79 − 0.268·Z for Blue, so the clear height at any X is H(X) = 3.732 × (41.79 − X), and the lower crossbeam limits it to 10.8 in between X = 34.2 and 38.6. A ROBOT has 42.0 in of clearance anywhere up to X = 30.5. A ROBOT at the 42-in starting height of **R104** therefore stages against the alliance wall, which is why the contact requirement names the wall rather than the truss. At each lane center the HEADWALL tag panel hangs to Z = 7.5 across its 9.0-in width, so between X = 38.75 and 39.0 the clear height there is 7.5 in. The full clear-volume curve is published in the FIELD CAD PACKAGE §4.1.

## 3.3 The CRAG

Each ALLIANCE owns one CRAG: a rock-spire scoring structure straddling the FIELD centerline. The Blue CRAG is centered at (324, 240) and the Red CRAG at (324, 84). Each CRAG has a 48 × 48 in footprint and rises to a spire top 90 in above the carpet. The body of the CRAG presents four vertical scoring faces around the footprint; a central spire carries the highest scoring features and the SUMMIT BEACON.

Face names are assigned from the owning ALLIANCE's approach:

**Table 3-2: CRAG faces by ALLIANCE**

| Element | Blue CRAG | Red CRAG | Features |
|---|---|---|---|
| **SHELF FACE** | −X face (plane X = 300), faces the Blue alliance wall | +X face (plane X = 348), faces the Red alliance wall | Shelf 1, Shelf 2, the Summit Socket, the BASE DEPOT |
| **SOCKET FACE** ×2 | ±Y faces (planes Y = 216 and Y = 264) | ±Y faces (planes Y = 60 and Y = 108) | one Low Socket and one Mid Socket per face |
| **PEG FACE** | +X face (plane X = 348), faces the Red alliance wall | −X face (plane X = 300), faces the Blue alliance wall | Low and Mid Pegs |
| **spire** | top of structure | top of structure | High Pegs, SUMMIT BEACON |

Because each CRAG has scoring features on all four faces, no defender can block every approach at once.

*Figure 3-2. The Blue CRAG, seen from its SHELF FACE and −Y SOCKET FACE. Dimensioned drawing: Plate 2 of the field drawing set.*

![The Blue CRAG](../figures/crag.png)

### 3.3.1 SHELF FACE

The SHELF FACE carries two horizontal shelves spanning the width of the face:

- **Shelf 1:** shelf top surface at 24 in, divided into 3 slots, each 14.0 in wide, separated by slot fences 1.5 in wide and 2.0 in tall. Slot centers lie at −15.5, 0, and +15.5 in from the face centerline.
- **Shelf 2:** shelf top surface at 42 in, same slot layout.

Shelves are 14.0 in deep and accept CACHE CRATES only, placed flat. A CACHE CRATE rests on its bottom crown, so its side faces reach their full 0.5-in bulge 6.5 in up, well above the 2.0-in fences. At the fence tops the crate is 12.44 in across, which gives a placement 0.78 in of lateral tolerance per side, and its 13.0-in crown clears the fences entirely. Crates in adjacent slots clear each other by 2.5 in. Each shelf slot SCORES at most one SUPPLY (six crates per CRAG on shelves). Extra SUPPLIES resting in or on an occupied slot are not SCORED and satisfy no requirement (Section 4.4.1).

### 3.3.2 SOCKET FACES and the Summit Socket

Each of the two SOCKET FACES carries two open-topped cylindrical sockets, loaded from above. Every socket's rim center stands 8.0 in out from its face plane, measured normal to the face, on a support beneath the tube:

- **Low Socket:** rim at 30 in, 14.0 in lateral on the shelf-face side of the face centerline, tube tilted 30° from vertical, tilting outward toward the approaching ROBOT. One per SOCKET FACE (2 per CRAG).
- **Mid Socket:** rim at 54 in, 14.0 in lateral on the peg-face side, tube tilted 30° from vertical. One per SOCKET FACE (2 per CRAG).
- **Summit Socket:** one per CRAG, on the SHELF FACE, on the CRAG's centerline, rim at 72 in, tube tilted 15° from vertical, tilting outward toward the owning ALLIANCE. A SCORED O2 CELL leans out of it toward the owning ALLIANCE's driver stations.

Sockets accept O2 CELLS only. Each socket SCORES at most one SUPPLY; extra SUPPLIES resting in or on an occupied socket are not SCORED and satisfy no requirement. The tube is 7.0 in long along its axis with a closed bottom, so a seated 14.0-in O2 CELL stands 7.0 in proud of the rim along the axis, where it is visible from the driver stations and the referee positions.

The two sockets on a face have different approach standoffs. The BASE DEPOT's corner arm runs 16.0 in along each SOCKET FACE from the SHELF FACE, and the Low Socket sits directly above it, so a ROBOT servicing the Low Socket parks against the arm and reaches 11.75 in. The Mid Socket, on the PEG FACE side, is clear of the arm and is 5.0 in of reach from BUMPERS on the face. Both are inside the **R105** limit.

**Toleranced dimension:** socket inside diameter 6.50 in ± 0.125 in. This dimension is held to the stated tolerance on every official field and is carried as a toleranced callout in the FIELD CAD PACKAGE drawing set. It provides 0.75 in of nominal radial clearance per side (1.50 in on diameter) for the 5.0-in O2 CELL.

> *Commentary:* The socket tolerance is called out because the insertion task depends on it. At 6.50 in ID the task is achievable with reasonable alignment; a field-build error that narrows the mouth makes it much harder. FIELD STAFF verify this dimension at field setup.

### 3.3.3 PEG FACE and High Pegs

The PEG FACE carries four pegs, and the spire carries two more:

- **Low Pegs** ×2, roots at 30 in, ±14.0 in from the face centerline
- **Mid Pegs** ×2, roots at 54 in, ±14.0 in from the face centerline
- **High Pegs** ×2 on the spire, roots at 78 in, ±7.0 in from the spire centerline

All pegs are 1.5 in OD, angled 45° upward from the face, with 10.0 in exposed and a fully rounded tip. Pegs accept ROPE COILS only, hung over the peg. Each peg SCORES at most one SUPPLY; extra SUPPLIES resting in or on an occupied peg are not SCORED and satisfy no requirement. Peg heights are measured to the peg root at the face.

A ROPE COIL dropped over a peg settles plumb, in a plane parallel to the CRAG face, hanging from the top of its hole. The coil can tilt up to 57.8° away from perpendicular to the peg before the peg binds inside the ring, and a vertical hang requires 45°, so a SCORED ROPE COIL is held captive rather than balanced. With its inner face 1.25 in outboard of the CRAG face, its center rests about 1.6 in above the peg root (FIELD CAD PACKAGE §2.5).

### 3.3.4 BASE DEPOT

The BASE DEPOT is a floor tray running along the base of the SHELF FACE and wrapping 16.0 in around both of that face's corners onto the SOCKET FACES. Its floor sits 0.25 in above the carpet, and its lip top is 4.0 in above the carpet. The channel is 16.0 in deep, measured from the CRAG face. In plan it is a continuous open-topped U: a 16 × 80 in outer run parallel to the SHELF FACE (the 16 × 48 in shelf-face leg plus a 16 × 16 in corner square at each end), with a 16 × 16 in corner arm running back along each SOCKET FACE.

The shelves overhang 14.0 in of the channel and span only the 48-in width of the SHELF FACE. From above, the outer 2.0 in of the shelf-face leg is open, as are both outer corner squares and part of each corner arm. Each arm is overhung by its Low Socket tube, so only the corner squares are wide enough to drop a CACHE CRATE or a ROPE COIL straight in. The rest of the shelf-face leg is loaded by pushing SUPPLIES in over the lip; Shelf 1 and its gussets stay above Z = 19.0, clear of a crowned CACHE CRATE standing on the tray floor (top at Z = 13.25).

The DEPOT accepts any SUPPLY in any orientation, whether pushed, dropped, or placed. Because a SUPPLY resting on another is not SCORED (Section 4.4.1), capacity is a single-layer packing limit: roughly 8 CACHE CRATES, or about 12 SUPPLIES in a mixed load.

A SUPPLY is SCORED in the BASE DEPOT when it is at rest, its only support is the tray floor, and it lies entirely within the vertical projection of the DEPOT channel. A SUPPLY supported by the lip, by the carpet outside the tray, or by another SUPPLY is not SCORED. A SUPPLY that stands taller than the 4-in lip is SCORED as long as the tray floor alone supports it. FIELD STAFF may level heaped SUPPLIES during MATCH stoppages; they do not otherwise adjust DEPOT contents during a MATCH, except to restore a SUPPLY under **G504**.

> *Example:* A ROPE COIL lands draped over the DEPOT lip, half in and half out. It is not SCORED, because the lip carries part of its weight. A second ROPE COIL thrown onto a full tray comes to rest on other ROPE COILS rather than on the tray floor, so it is not SCORED either. A CACHE CRATE standing on the tray floor rises well above the lip and is SCORED.

### 3.3.5 Tier LED Rings and SUMMIT BEACON

Each CRAG carries three LED tier rings around the structure at 30 in, 54 in, and 78 in, and a SUMMIT BEACON: the top 12 in of the spire (Z 78–90) is a translucent lantern with its luminous center at 84 in.

- A tier ring lights in the owning ALLIANCE's color when the corresponding CAMP is established (30 in → CAMP I, 54 in → CAMP II, 78 in → HIGH CAMP). Tier rings latch: once lit, a ring stays lit for the remainder of the MATCH, even if SUPPLIES are later dislodged.
- The SUMMIT BEACON lights when all three CAMPS are established.
- The FORECAST (white) and each ALLIANCE's declared ROUTE are displayed on the FIELD LEDs (Section 3.1.2), not on the tier rings (see Section 4.2.3 and Section 4.3.1). A tier ring shows latched CAMP state only, so it never changes color or pattern once lit.

The LEDs are decorative confirmation only and are never the scoring authority. A CAMP is established at the moment its required SUPPLIES are simultaneously SCORED, as determined by referees and the scoring system, whether or not the corresponding ring lights. If lighting and the SCORED state ever disagree, the SCORED state governs.

### 3.3.6 CRAG APRON

The CRAG APRON (Section 3.2) is the taped boundary offset 36 in outward from the SHELF FACE and the PEG FACE and 20 in outward from each SOCKET FACE, with 20-in-radius arcs sweeping the corners. Each APRON is taped in its CRAG's ALLIANCE color. It protects ROBOTS of the owning ALLIANCE whose BUMPERS intersect it from opponent contact (**G407**). **G402**, **G403**, **G501**, and **G502** also refer to it.

## 3.4 The HEADWALL

Each ALLIANCE has one HEADWALL: a climbing truss standing in front of its alliance wall. All HEADWALL geometry derives from one reference plane, PLANE P. PLANE P contains the horizontal line {X = 48 (Blue) / X = 600 (Red), Z = 0} spanning Y 90–234, and is tilted 15° from vertical with its top leaning toward the alliance wall. ROBOTS climb on the FIELD side of PLANE P.

Each HEADWALL is 144 in wide and divided into three independent 48-in lanes (Blue lane centers at Y = 114, 162, 210). The lanes are structurally independent: load or motion in one lane does not disturb the others. One ROBOT per lane (**G415**).

*Figure 3-3. The Blue HEADWALL: three independent lanes, each with a LEDGE RUNG, a CAMP RUNG and a SUMMIT RUNG. Dimensioned drawing: Plate 3 of the field drawing set.*

![The Blue HEADWALL](../figures/headwall.png)

Each lane carries three rungs of 1.5 in OD and 20.0 in length, with their centerlines lying in PLANE P:

**Table 3-3: HEADWALL rungs**

| Rung | Height (carpet to top of rung) | Lateral offset from the lane centerline (identical in all three lanes) |
|---|---|---|
| **LEDGE RUNG** | 30 in | −12.0 in |
| **CAMP RUNG** | 54 in | +12.0 in |
| **SUMMIT RUNG** | 78 in | −12.0 in |

Because of the 15° lean, each rung sits approximately 6.4 in horizontally behind (toward the alliance wall from) the rung below it. The lateral stagger is the same in every lane: LEDGE −12, CAMP +12, SUMMIT −12. Successive rungs within a lane are therefore 24.0 in apart laterally, center to center, while rungs at the same height in adjacent lanes stay 48.0 in apart (28.0 in end to end, which leaves room for three ROBOTS to hang side by side).

A 20.0-in rung centered 12.0 in off the lane centerline leaves no lateral position that engages two successive rungs: the LEDGE RUNG spans lane-centerline −22 to −2 while the CAMP RUNG spans +2 to +22. A climber therefore cannot follow the rung line with one fixed hook pair. Only two non-overlapping lateral positions fit a 20.0-in rung in a 48-in lane, so the stagger alternates with period two, and the LEDGE and SUMMIT RUNGS share the −12.0 offset while the CAMP RUNG sits at +12.0.

There are two routes to the top, and both are legal:

- the two-handoff traversal, LEDGE → CAMP → SUMMIT, each step 24 in up, 6.4 in back, and 24 in across; or
- a direct LEDGE → SUMMIT reach at one lateral position, 48 in up and 12.9 in back (49.7 in measured in PLANE P, against 24.9 in for a single step).

The direct route replaces all the lateral motion with twice the vertical reach in one move, which requires the harder mechanism. Most climbers are expected to use the traversal.

All truss structure lies at least 4.0 in behind PLANE P, measured normal to PLANE P, except the two end brackets of each rung, which may enter that band within 2.0 in of the rung end. Hook wrap is therefore clear over the middle 16.0 in of every 20.0-in rung, and a hook must engage inside that band.

The taped HEADWALL ZONE (coincident with BASECAMP, Section 3.2) lies beneath and behind the HEADWALL, between the truss base and the alliance wall. From the start of the ENDGAME period until climb assessment is complete, an opponent that contacts a ROBOT in this zone commits a MAJOR FOUL, and an additional MAJOR FOUL and a YELLOW CARD if the contact blocks or displaces a climb, as when a hanging ROBOT falls (**G412**). Contact that the protected ROBOT initiates is not a violation (**G205**). Climbing is legal at any time in the MATCH; the zone protection applies only in that window. A ROBOT may not contact a rung while any part of its BUMPERS is on the alliance-wall side of the CLIMB LINE (X = 48 in for Blue, X = 600 in for Red) unless it is then supported solely by rungs, or is still touching a rung it took hold of while so supported within the preceding 5 seconds (**G416**).

> *Commentary:* The three-lane design lets all three ROBOTS of an ALLIANCE climb at the same time without traffic conflict. The difficulty comes from the 15° lean and the 24-in lateral alternation. **G416** exists because the truss leans back over BASECAMP: without it, a ROBOT could park under the SUMMIT RUNG and reach it with a purely vertical mast, and would never need to hang from a lower rung.

## 3.5 OUTFITTERS

Each ALLIANCE has two OUTFITTERS, one at each corner of its alliance wall. Each OUTFITTER consists of a chute opening through the alliance wall, a human-player station behind it, and the taped OUTFITTER LANE in front of it.

*Figure 3-4. A Blue OUTFITTER seen from behind the alliance wall: SUPPLIES are fed down the ramp and through the chute opening onto the FIELD. Dimensioned drawing: Plate 4 of the field drawing set.*

![A Blue OUTFITTER](../figures/outfitter.png)

- **Chute opening:** 30 in wide × 16 in tall, with the sill (bottom edge) at 24 in above the carpet, so the opening spans Z 24–40. Blue chutes are centered at (0, 30) and (0, 294); Red chutes at (648, 294) and (648, 30). The 16-in height clears the 12.0-in CACHE CRATE, whose pillowed faces give it a 13.0-in maximum envelope, with 3.0 in to spare.
- **Human players:** exactly one HUMAN PLAYER is stationed at each OUTFITTER, two per ALLIANCE. They may come from any of the ALLIANCE's three DRIVE TEAMS and are assigned before the "field ready" signal (**G307**). HUMAN PLAYERS feed SUPPLIES through the chute onto the FIELD. A SUPPLY may be slid, dropped, or rolled through the chute. HUMAN PLAYERS may break the plane of the chute opening with their hands, and no further (**G102**).
- **Stock:** all SUPPLIES not staged on the FIELD or preloaded (Section 3.6.1) begin the MATCH stocked at the ALLIANCE's two OUTFITTERS, divided between them at the ALLIANCE's discretion.
- **Restocking:** FIELD STAFF return any SUPPLY that leaves the FIELD, at the next safe opportunity, to the nearest OUTFITTER chute: the chute of the ALLIANCE on that side of the FIELD, which may be the opposing ALLIANCE's chute (**G507**). The SUPPLY re-enters play through normal human-player feeding. Returned SUPPLIES are never re-staged to FIELD marks during a MATCH.

The OUTFITTER LANE (36 in wide × 48 in deep, Section 3.2) in front of each chute is a no-defense zone: opponents may not enter it or contact ROBOTS within it (**G410**).

## 3.6 SUPPLIES

SUMMIT PUSH is played with three SUPPLY types: 63 SUPPLIES per MATCH in total, 21 of each type. "SUPPLY" and "GAME PIECE" are synonymous; SUPPLY is the term used in the rules.

**Table 3-4: SUPPLY specifications**

| | **CACHE CRATE** | **O2 CELL** | **ROPE COIL** |
|---|---|---|---|
| Shape | cube, pillowed faces | cylinder, domed caps | torus (ring) |
| Dimensions | 12.0 in cube (13.0 in max envelope with the 0.5-in face crown) | 5.0 in dia × 14.0 in long | 10.0 in OD, 2.5 in tube (5.0 in ID hole) |
| Weight | ~2.0 lb | ~1.5 lb | ~1.0 lb |
| Official construction | sewn ripstop-nylon skin over PU foam core | rigid molded shell: thick-wall ABS tube with rigid molded ABS domed caps, no foam | solid molded rubber/foam ring |
| Compression tolerance | compliant: compresses up to 2.0 in across any pair of opposing faces (13.0-in crowned envelope → 11.0 in) under a squeeze of up to 15 lbf, crowns first; recovers fully when released | rigid: does not compress (zero compression tolerance) | compliant: tube section compresses up to 0.5 in (2.5 → 2.0 in) under a pinch of up to 10 lbf; the ring ovalizes up to 1.0 in across the OD (10.0 → 9.0 in) under a diametral squeeze of up to 5 lbf; recovers fully when released |
| Official color | expedition violet `#7B3FA0` | body `#F2F2F0`, domed caps `#2E8B57` | amber `#D9A441` |
| Scores on | Shelves, BASE DEPOT | Sockets, BASE DEPOT | Pegs, BASE DEPOT |
| Count per MATCH | 21 | 21 | 21 |

All three SUPPLY types are durable enough to be driven over. A SUPPLY damaged beyond play is removed and is not replaced during the MATCH.

The CACHE CRATE and the ROPE COIL are compliant: a ROBOT or a HUMAN PLAYER may squeeze either one within its compression tolerance in normal handling, and it recovers its shape when released. The O2 CELL is rigid, so a mechanism that grips it must supply its own compliance. Every fit, clearance and envelope in this manual and in the Field CAD Package is computed at nominal, uncompressed size: compression is margin, not budget. No SUPPLY is colored in either ALLIANCE's color, so a referee, a DRIVE TEAM, or a vision pipeline cannot mistake a SUPPLY for an ALLIANCE element.

### 3.6.1 Staging

At the start of each MATCH, SUPPLIES are staged as follows:

**Table 3-5: SUPPLY staging at the start of a MATCH**

| Location | Supplies | Detail |
|---|---|---|
| CENTER CACHE (neutral) | 3 CACHE CRATES, 3 O2 CELLS, 3 ROPE COILS | one SUPPLY per white mark of the 3 × 3 grid (§3.2), arranged so that each type appears once per row and once per column; the assignment is published in the FIELD SETUP CHART (`03-field/FIELD-CAD-PACKAGE.md` §6) |
| Alliance staging marks (per alliance) | 2 CACHE CRATES, 2 O2 CELLS, 2 ROPE COILS | at the three taped marks at X = 144 (Blue) / X = 504 (Red), Y = 108/162/216; two SUPPLIES of one type per mark |
| Robot preloads (per alliance) | up to 1 per ROBOT, any type | in contact with the ROBOT in its starting position |
| OUTFITTERS (per alliance) | 7 CACHE CRATES, 7 O2 CELLS, 7 ROPE COILS | divided between the ALLIANCE's two chutes at its discretion; preloads are drawn from this stock |

Accounting per SUPPLY type: of each type's 21 SUPPLIES, 3 begin neutral in the CENTER CACHE, 2 begin on each ALLIANCE's staging marks (4 total), and 7 begin in each ALLIANCE's OUTFITTER stock (14 total). Preloads are drawn from an ALLIANCE's OUTFITTER stock during setup; preloads not taken remain at the OUTFITTERS.

The CENTER CACHE arrangement places one SUPPLY of each type in each row of the grid, so that neither ALLIANCE is materially nearer to any one type. An assignment of 3/3/3 that is unchanged by the 180° rotation is impossible on a 3 × 3 grid, because the rotation fixes one mark and pairs the other eight. The row-balanced arrangement is the closest achievable: the aggregate haul distance from the nine marks to each CRAG is identical for both ALLIANCES, and no single type differs by more than 1%.

*Figure 3-5. The CENTER CACHE at the start of a MATCH, seen from the Blue side. SUPPLY drawings: Plate 5 of the field drawing set.*

![The CENTER CACHE](../figures/center-cache.png)

## 3.7 AprilTags

The ARENA carries 26 AprilTags from the 36h11 family for ROBOT pose estimation and target alignment.

**Panel construction.** Each tag image is 6.5 in square (the 36h11 data body), printed on an 8.125-in-square target that includes its white border, and mounted on a 9.0-in-square panel. Table 3-6 gives tag centers; "Z center" is the height of the tag center above the carpet.

**Mounting heights.** Close-range tags are mounted low: the eight on each CRAG at a 17.5-in center height (held to ±0.15 in at field setup), and the three on each HEADWALL at 12 in. Both heights are in the frame of a single camera mounted 10–20 in above the carpet, which serves every precision approach on the FIELD. Each CRAG face carries a pair of tags centered ±14 in from the face centerline. The 17.5-in CRAG tag height is set against the tallest objects that can stand in front of a tag. A CACHE CRATE standing in the BASE DEPOT reaches 13.25 in (the tray floor's 0.25 plus 13.0 to its crowned apex) and tops out 0.19 in below the tag target, and the underside of Shelf 1 sits 1.25 in above the panel. One SUPPLY does reach into the target band: an O2 CELL standing on end in the DEPOT, its top at 14.25 in (the tray floor's 0.25 plus 14.0) against a 13.44-in target bottom. `04-vision/VISION-GUIDE.md` §1.3 covers that case and the camera height it implies.

**Table 3-6: AprilTag positions**

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

Red tag positions are the Blue positions rotated 180° about the FIELD center. The layout is one fixed map in the single always-blue-origin frame, and Red ID = Blue ID + 13. OUTFITTER tags are mounted on the alliance wall, centered above each chute. HEADWALL tags are mounted plumb on the lane centerline of the truss lower crossbeam, at tag plane X = 39 (Blue) / X = 609 (Red). That plane is behind PLANE P at every point of the panel, so nothing intrudes into the climbing volume. CRAG tags face outward, perpendicular to their face.

> *Commentary:* Every scoring approach on the FIELD has a tag pair, or a single tag square-on to it, at close range. Shelf placements, socket insertions, peg hangs, chute pickups, and lane alignment for the ENDGAME climb can all be vision-assisted without full-field pose. Full-field pose estimation is required only for contested CENTER CACHE AUTO routines. Because every close-range tag sits between 12 and 17.5 in, one camera mounted 10–20 in above the carpet serves all of them. If it is the ROBOT's only camera, it belongs toward the upper end of that band: an O2 CELL standing on end in the DEPOT is the one SUPPLY that reaches into a tag's target band, and its domed cap clips a low camera's view of the tag's bottom edge (vision guide §1.3).

A machine-readable layout in WPILib AprilTag field schema (meters, always-blue-origin NWU) is published at `04-vision/apriltag-field-layout.json`. Mounting details, calibration guidance, and simulation setup are in the vision guide (`04-vision/VISION-GUIDE.md`).
