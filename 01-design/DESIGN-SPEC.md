# SUMMIT PUSH — Locked Design Specification (v2.2)

This specification is the single source of truth for every document in the package. Every number, name, and rule decision in it is final unless the game designer changes it. Where this specification and another document disagree, **this specification governs**.

**Revision:** v2.2, superseding v2.1, v2.0 and v1.0. Every change since v1.0 is itemized, with rationale, in `REVISION-LOG.md` at the package root.

---

## 0. Identity

- **Game name:** SUMMIT PUSH
- **Setting:** High-alpine mountaineering. Two expedition ALLIANCES race up opposite flanks of the same peak, stocking their high camps with SUPPLIES before the storm closes the mountain, and then make the summit push themselves.
- **Format:** 3v3, standard competitive-robotics conventions, published as an offseason design-challenge release. The game is not team-specific and has no sponsor.
- **Match:** 2:30 total, made up of **AUTO 0:15** and **TELEOP 2:15**; the final **0:30 is the ENDGAME period** (HEADWALL protection active). Scores are assessed after a 3-second settle window following AUTO and following the final buzzer (climbs: robots at rest or T+5 s).

## 1. Locked design decisions

1. **CRAG APRON (placement protection; a line call).** A taped apron extends **36 in** out from the SHELF FACE and the PEG FACE and **20 in** out from each SOCKET FACE, with 20-in-radius arcs sweeping the four corners. An opponent may not contact a robot whose bumpers intersect its own alliance's apron (MAJOR FOUL; + YELLOW CARD if contact causes a robot then extended above 60 in to tip); contact that the protected robot initiates is not a violation (**G205**). The 68-in inter-CRAG corridor (Y 128–196), the nine staged CENTER CACHE marks, and all transit lanes remain open to defense; the outer 20 in at each end of the CENTER CACHE band lie inside an APRON. Defense is otherwise legal everywhere except the opponent's OUTFITTER LANES and the opponent's HEADWALL ZONE during ENDGAME.
   *(The SOCKET FACE offset is reduced to 20 in so that the two aprons and the staged CENTER CACHE fit inside the 108-in corridor between the CRAGS. A uniform 36-in offset, trimmed at the CENTER CACHE band, would remove APRON protection from one SOCKET FACE of every CRAG.)*
2. **Randomness and strategy are separated into two mechanics:**
   - **FORECAST (random, FMS game data):** at T=0 of AUTO, FMS broadcasts `W` (WHITEOUT), `I` (ICEFALL), or `G` (GALE) and lights the white FIELD LEDs. The FORECAST sets the **PRIORITY SUPPLY** (WHITEOUT = CACHE CRATES, ICEFALL = O2 CELLS, GALE = ROPE COILS), which (a) scores **double AUTO placement value** and (b) is required in quantity by ROPED UP (§4). The effect applies in AUTO only, and autonomous routines must branch on it. Offseason fallback: a published card draw and manually set LEDs, specified in the manual body.
   - **ROUTE DECLARATION (chosen, strategic):** during setup each alliance declares its ROUTE: **LOW ROUTE**, **MID ROUTE**, or **HIGH ROUTE** (LOW if none is declared). The alliance's corresponding CAMP bonus pays its **declared value** for the whole match (CAMP I 6→**18**, CAMP II 10→**24**, HIGH CAMP 15→**35**). The declared ROUTE is shown on the FIELD LEDs at match start, so it can be scouted. The uplifts are scaled by tier difficulty so that no ROUTE is dominant: each declaration is the best choice for some alliances and none is best for all, so the right choice depends on the alliance's demonstrated capability (manual §4.7 works the numbers).
3. **EXPEDITION RP lockout softened:** at Regional tier only, a missing piece-type requirement of **CAMP I** may be satisfied by **4 pieces of that type SCORED in the BASE DEPOT**.
4. **ASCENT RP thresholds: 32 / 52 / 60.** The Championship threshold is 60 so that "all three robots reach the CAMP RUNG" (3 × 20) earns the RP.
5. **O2 socket tolerance published:** socket ID **6.50 in ± 0.125 in**, the tightest tolerance on the field, with a callout in the manual. The field CAD model and its drawing set must hold it.
6. **BASE DEPOT scoring definition (a support test):** a piece is SCORED in the BASE DEPOT when it is at rest, its only support is the tray floor, and it lies entirely within the vertical projection of the DEPOT channel. A piece supported by the lip, by the carpet outside the tray, or by another piece is not SCORED. *(A height test requiring a piece to lie fully below the 4-in lip plane cannot be met by the 12-in CACHE CRATE or the 5-in-diameter O2 CELL.)*
7. **Anti-pollution:** any game piece SCORED on a CRAG scores **for that CRAG's alliance regardless of which robot placed it**. Robots may never remove a SCORED piece from either CRAG (MAJOR FOUL per piece, plus restoration).
8. **Beacon ignition:** CAMP completion is announced physically. Each CRAG carries LED **tier rings** at 30 / 54 / 78 in that light in alliance color when the corresponding CAMP is established (latched: a lit ring never goes dark), plus the **SUMMIT BEACON**, a translucent lantern forming the top 12 in of the spire (Z 78→90, luminous center 84 in), which ignites when all three CAMPS are established and banks **+10 (latched)**. A CAMP is established when its required pieces are simultaneously SCORED. The LEDs are decorative confirmation and never the scoring authority.
9. **No-fault knock-offs:** any piece that leaves a scoring position **without direct robot contact on the piece** is restored by field staff at the next safe opportunity; referees make no causation attribution. Direct de-scoring contact on the piece is a MAJOR FOUL plus restoration (see §1.7). Contact with the CRAG structure that shakes a piece loose is a no-fault knock-off; deliberately striking a CRAG to dislodge pieces is separately prohibited as ARENA abuse.
10. **The FORECAST fallback, settle timing, out-of-bounds handling, score finality, ARENA faults, timeouts, and replays are all specified in the manual body**; none is deferred to an appendix.

## 2. Game pieces (three types, each a different size and shape)

| | CACHE CRATE | O2 CELL | ROPE COIL |
|---|---|---|---|
| Shape | Cube | Cylinder | Torus (ring) |
| Dimensions | 12.0 in cube, pillowed faces (0.5 in face crown) | 5.0 in dia × 14.0 in long, domed caps, R1.0 cap/body fillets | 10.0 in OD, 2.5 in tube (5.0 in ID hole) |
| Weight | ~2.0 lb | ~1.5 lb | ~1.0 lb |
| Official material | Sewn ripstop-nylon skin over PU foam core | 4.0-in OD rigid tube core, 0.5-in EVA foam sleeve, molded foam caps | Solid molded rubber/foam ring |
| Official color | Expedition violet `#7B3FA0` | Body `#F2F2F0`, caps `#2E8B57` | Amber `#D9A441` |
| Handling problem | Wide compliant intake, flat controlled placement | Ground pickup of a roller + 90° reorientation + socket insertion | Hook/spear or pinch gripper, precise hang on a 45° peg at height |
| Count | 21 | 21 | 21 |

Piece colors are chosen far from both alliance colors (in hue, violet is 62° from alliance blue and 83° from alliance red) so that no piece can be mistaken for an alliance element in a render, a broadcast frame, or a vision pipeline.

**Staging (per alliance unless noted):** 3 of each type in the neutral **CENTER CACHE** (9 pieces total, field-neutral, arranged so that each type appears once per row and once per column of the 3 × 3 grid; see §3); 2 of each type at taped alliance-side marks 12 ft from the alliance wall; and **7 of each type per alliance** stocked at the alliance's two **OUTFITTER** chutes for human-player feed (3 + 2×2 + 2×7 = 21 per type). Each robot may carry up to 1 preload (any type), drawn from the alliance's OUTFITTER stock during setup.

**Possession limit: 2 game pieces** (any combination).

## 3. Field layout (coordinates locked)

Field: **54 ft × 27 ft (648 in × 324 in)** carpet, 20-in guardrails, standard 3-station alliance walls. Coordinate frame: **always-blue-origin NWU**, with the origin at the right corner of the Blue alliance wall (from Blue's perspective), +X toward the Red wall, +Y left, +Z up. Centerline X = 324. Field center (324, 162). The layout is 180° rotationally symmetric about field center.

| Element | Position (center) | Footprint / span |
|---|---|---|
| **BLUE CRAG** | (324, 240) | 48 × 48 in footprint, spire top 90 in |
| **RED CRAG** | (324, 84) | 48 × 48 in footprint, spire top 90 in |
| **CENTER CACHE band** | X 300–348, Y 108–216 | 9 neutral pieces at 9 taped marks (3×3 grid, 24 in spacing, centered 324, 162) |
| **BLUE HEADWALL** | plane P crosses carpet at X = 48, Y 90–234 | 144 in wide truss, leaned 15° from vertical (top leans toward alliance wall), 3 independent 48-in lanes |
| **RED HEADWALL** | X = 600, Y 90–234 | mirror |
| **BLUE BASECAMP zone** | X 0–48, Y 90–234 | taped; robots start here |
| **BLUE OUTFITTERS** | chutes centered (0, 30) and (0, 294) | wall opening 30 in wide × 16 in tall, sill 24 in; taped OUTFITTER LANE 36 in wide extending 48 in into the field (no-defense zone) |
| **RED OUTFITTERS** | (648, 294) and (648, 30) | mirror |
| **Alliance staging marks** | Blue: X = 144; Red: X = 504 | 2 of each piece type at taped marks, Y = 108 / 162 / 216 |

### CRAG faces (per CRAG; face names from the owning alliance's approach)
- **SHELF FACE** (faces the owning alliance's wall): Shelf 1 top surface at **24 in** (3 slots, 14.0 in wide, slot centers at **±15.5 / 0** from the face centerline), Shelf 2 at **42 in** (same slot layout). Shelf depth 14.0 in. CACHE CRATES only, flat placement. The SHELF FACE also carries the **Summit Socket** (below) and the **BASE DEPOT**.
- **SOCKET FACES** (the two ±Y faces): each face carries one **Low Socket** rim at **30 in** and one **Mid Socket** rim at **54 in**, with rim centers **8.0 in** out from the face plane at **±14.0 in** lateral (Low on the shelf-face side, Mid on the peg-face side). Tubes are tilted **30° from vertical**, tilting outward, open end up. O2 CELLS only, inserted from above.
- **Summit Socket**, ×1 per CRAG: rim center on the CRAG's centerline, **8.0 in out from the SHELF FACE plane**, rim height **72 in**, tube tilted **15° from vertical**, tilting outward toward the owning alliance. O2 CELLS only.
- **All sockets:** tube length **7.0 in** along the axis, closed bottom, **ID 6.50 ± 0.125 in**. A seated 14.0-in O2 CELL therefore stands 7.0 in proud of the rim along the tube axis.
- **PEG FACE** (faces the opponent wall): two **Low Pegs** at **30 in** and two **Mid Pegs** at **54 in**, roots at ±14.0 in from the face centerline; two **High Pegs** on the spire at **78 in**, roots at ±7.0 in from the spire centerline. All pegs are 1.5 in OD, angled **45° upward**, with 10.0 in exposed. ROPE COILS only.
- **BASE DEPOT**: a tray with its floor 0.25 in above the carpet and its lip top 4.0 in above the carpet. Channel depth is **16.0 in** from the SHELF FACE, and the channel wraps **16.0 in** around both shelf-face corners onto the SOCKET FACES. The two outer corner squares are included, so the tray is one continuous U in plan (Blue: a 16 × 80 leg at X 284–300, Y 200–280, plus arms at X 300–316, Y 200–216 and Y 264–280). The tray accepts any piece in any orientation, in a single layer. A SUPPLY resting on another is not SCORED, so capacity is a packing limit: about **8 CACHE CRATES**, or about **12 SUPPLIES** in a mixed load, in 1792 in² of tray. Because the channel is deeper than the 14.0-in shelf, the outer 2 in of the shelf-face leg, both outer corner squares, and the unobstructed parts of both corner arms are open from above. Only the two corner squares are wide enough to drop a 13.0-in crowned CACHE CRATE straight in, because each arm is overhung by its Low Socket tube; a crate still fits inside the channel's vertical projection everywhere.
- **LED tier rings** at 30 / 54 / 78 in. The 78 ring is hung with its top edge on the lantern joint (band Z 77.0–78.0) so that it stays on the opaque spire. SUMMIT BEACON lantern Z 78→90, luminous center 84 in.

### HEADWALL (per alliance)
- **Truss and plane P:** a 15° inclined truss. **PLANE P** contains the horizontal line {X = 48 (Blue) / 600 (Red), Z = 0} spanning Y 90–234 and is tilted 15° from vertical, with the top leaning toward the alliance wall.
- **Rungs:** each 48-in lane has three 1.5-in OD rungs with centerlines in plane P: **LEDGE RUNG 30 in**, **CAMP RUNG 54 in**, **SUMMIT RUNG 78 in** (heights above carpet to rung top). Rung length **20.0 in**. The 15° lean sets each rung **6.4 in** horizontally behind the one below (24 × tan 15°).
- **Stagger:** **±12.0 in** from the lane centerline, alternating by rung and **identical in all three lanes**: LEDGE −12.0, CAMP +12.0, SUMMIT −12.0. No lateral position engages two successive rungs within a lane, and rungs at the same height in adjacent lanes stay a full 48 in apart center-to-center (28 in end to end). Alternating the sign by lane instead would bring adjacent lanes' rungs to 24 in apart, closer than two hanging ROBOTS are wide.
- **Structure clearance:** all truss structure is ≥ 4.0 in behind plane P, except the two end brackets of each rung, which may enter that band within 2.0 in of the rung end. Hook wrap is clear over the middle **16.0 in** of every 20.0-in rung.
- **Lanes and zone:** one robot per lane. HEADWALL ZONE = the taped BASECAMP area. An opponent contacting a robot in this zone during ENDGAME commits a MAJOR FOUL, unless the protected robot initiated the contact (**G205**); a contact that blocks or displaces a climb, including one that makes a hanging robot fall, adds one MAJOR FOUL and a YELLOW CARD.

**Climb entry rule (CLIMB LINE):** a robot may not contact a HEADWALL rung while any part of its bumpers is on the alliance-wall side of the plane **X = 48 (Blue) / X = 600 (Red)**, across the full width of the field, unless it is at that moment supported solely by one or more HEADWALL rungs, or **is still touching a rung it took hold of while so supported** within the preceding 5 s. The test is the plane. BASECAMP spans only Y 90–234 while lane 1's SUMMIT RUNG reaches Y 92, so a test against the BASECAMP zone would leave a strip beside BASECAMP from which a vertical mast reaches the SUMMIT RUNG. The currency requirement closes a second gap: without it, a brief early hang would earn a one-time exemption that reopens the same play. Together, the two requirements make every climb begin from the field side of the truss.

## 4. Scoring (locked values)

A piece is **SCORED** when it is at rest, supported by the scoring element alone, and not in contact with any robot of the scoring alliance. AUTO values apply to pieces whose last placing robot contact occurred before the end of AUTO.

Placement values are **uniform by tier**: every scoring position at a given tier is worth the same, whatever the piece type.

| Tier | Positions | Heights | AUTO | TELEOP |
|---|---|---|---|---|
| **Low** | Shelf 1 ×3, Low Sockets ×2, Low Pegs ×2 (7) | 24 / 30 / 30 in | **7** | **4** |
| **Mid** | Shelf 2 ×3, Mid Sockets ×2, Mid Pegs ×2 (7) | 42 / 54 / 54 in | **10** | **7** |
| **High** | Summit Socket ×1, High Pegs ×2 (3) | 72 / 78 in | **13** | **10** |
| **BASE DEPOT** | ~12, any type, any orientation | floor (4 in lip) | **4** | **2** |
| **LEAVE** (auto) | — | — | **3**/robot | — |

**CAMP bonuses (latched when established; tier LED ignites):**

| CAMP | Requirement (simultaneously SCORED) | Base | Declared |
|---|---|---|---|
| **CAMP I** | ≥1 crate on Shelf 1 + ≥1 Low-Socket O2 + ≥1 Low-Peg rope | +6 | **+18** (LOW ROUTE) |
| **CAMP II** | ≥1 crate on Shelf 2 + ≥1 Mid-Socket O2 + ≥1 Mid-Peg rope | +10 | **+24** (MID ROUTE) |
| **HIGH CAMP** | Summit Socket filled + ≥1 High Peg | +15 | **+35** (HIGH ROUTE) |
| **SUMMIT BEACON** | all three CAMPS established | +10 | never uplifted |

- Regional-tier CAMP I substitution: one missing piece-type slot may be satisfied by 4 BASE DEPOT pieces of that type.
- HIGH CAMP requires only O2 CELLS and ROPE COILS; CACHE CRATES are not hauled above CAMP II.

**AUTO extras:** FORECAST doubles the PRIORITY SUPPLY's AUTO placement points. **ROPED UP** = all 3 robots LEAVE **and** the alliance scores ≥5 pieces in AUTO, including **≥2 PRIORITY SUPPLY pieces and ≥1 of each of the other two types** → **+10**. The PRIORITY SUPPLY requirement makes the FORECAST branch worth preparing: four of the five pieces are fixed by type (two of the priority type plus one of each other type), and which type is doubled is not known until T = 0.

**ENDGAME (assessed at rest, or T+5 s):** PARK in BASECAMP **3**; supported solely by the LEDGE RUNG **12**; CAMP RUNG **20**; SUMMIT RUNG **30**. Maximum alliance climb score 90. Climbing is legal at any time; protection applies from the start of ENDGAME through climb assessment.

**Fouls:** MINOR FOUL **+3** to the opponent; MAJOR FOUL **+8**. VERBAL WARNING, YELLOW CARD, and RED CARD follow the manual taxonomy; a second YELLOW CARD in a tournament phase is a RED CARD.

## 5. Ranking Points (locked)

Win 3 / Tie 1, plus three bonus RPs (maximum 6 per match). The manual publishes the escalation columns; design entries are judged against the **Championship** column.

| Bonus RP | Regional | DCMP | Championship |
|---|---|---|---|
| **SUPPLY LINE** (total pieces SCORED, BASE DEPOT included) | ≥15 | ≥19 | ≥23 |
| **EXPEDITION** (CAMPS established) | 2 CAMPS incl. the declared ROUTE's CAMP | All 3 CAMPS | All 3 CAMPS + the declared ROUTE's tier at full capacity |
| **ASCENT** (alliance endgame points) | ≥32 | ≥52 | ≥60 |

**Full capacity** is 7 SCORED positions for every ROUTE. The three requirement sets are distinct and cost 12 / 12 / 11 CRAG positions in total (LOW / MID / HIGH), which is 4 / 4 / 3 beyond the three CAMPS that every ROUTE needs anyway. HIGH asks for one position fewer because one of its three, the second High Peg, is the hardest position on the CRAG:
- **LOW:** Shelf 1 ×3, Low Sockets ×2, Low Pegs ×2
- **MID:** Shelf 2 ×3, Mid Sockets ×2, Mid Pegs ×2
- **HIGH:** Summit Socket ×1, High Pegs ×2, Mid Sockets ×2, Mid Pegs ×2

Ranking order: Ranking Score (avg RP) → cumulative match points → cumulative AUTO → cumulative ENDGAME → random. Playoffs: 8-alliance double elimination.

## 6. AprilTags (locked layout — 26 tags, 36h11)

Tag body 6.5 in on an 8.125 in target, mounted on a 9.0 in panel. Each CRAG face carries two tags (centered ±14 in from the face centerline) at **center height 17.5 in**, held to ±0.15 in at field setup. That height is above the 13.25-in crowned apex of a CACHE CRATE standing in the BASE DEPOT (tray floor 0.25 plus 13.0) and below the 23.25-in underside of Shelf 1, so no field structure and no SCORED piece can occlude a CRAG tag from a camera 10–20 in high, with one exception: an O2 CELL stood on its end in the DEPOT (its top at 14.25 in, tray floor 0.25 plus 14.0, against a 13.44-in target bottom). VISION-GUIDE §1.3 gives the camera-height rule for that case, and notes that a camera 24–36 in high can see the Low Socket tube in front of part of the tag beneath it. HEADWALL lane tags are at **center height 12 in**, plumb, on the truss lower crossbeam at tag plane **X = 39 (Blue) / 609 (Red)**, at least 4.4 in behind plane P at every point of the panel, so nothing intrudes into the climbing volume. OUTFITTER tags are centered above the chutes at **52 in**.

| IDs | Location | Z center | Facing |
|---|---|---|---|
| 1, 2 | Blue Outfitter chutes (Y=30, Y=294) | 52 in | +X (into field) |
| 3, 4, 5 | Blue Headwall lanes (Y=114, 162, 210), X = 39 | 12 in | +X |
| 6–13 | Blue Crag: pairs on Shelf face (−X), Socket faces (±Y), Peg face (+X) | 17.5 in | outward, ⟂ face |
| 14, 15 | Red Outfitter chutes (Y=294, Y=30) | 52 in | −X |
| 16, 17, 18 | Red Headwall lanes (Y=210, 162, 114), X = 609 | 12 in | −X |
| 19–26 | Red Crag: Blue pairs rotated 180° about field center (Red ID = Blue ID + 13) | 17.5 in | outward |

Deliverable: a WPILib-schema `apriltag-field-layout.json` (meters, always-blue-origin NWU), so that entrants can run PhotonVision/Limelight simulation directly. There is one canonical layout.

## 7. Robot construction constraints (modern-convention baseline)

Weight ≤ **115 lb** (excluding bumpers and battery); bumpers ≤ 20 lb. Frame perimeter ≤ **120 in**, fixed frame, measured by string wrap. Starting configuration ≤ **42 in** tall, within the frame perimeter apart from the bumpers. Horizontal extension ≤ **18 in** beyond the frame perimeter. **No in-match height limit** (the 78-in targets and the climbs depend on it). Propulsion cap: ≤ **4 motors** delivering torque to elements contacting the carpet (azimuth/steering motors exempt). Bumpers: full perimeter, each gap < 1.25 in, 2.25 in foam depth, 4.5 in tall cross-section filling a floor-referenced BUMPER ZONE from 2.5 to 5.75 in, corners filled, no wedges, red/blue covers, white numbers ≥ 3.75 in tall in ≥ 3 locations.

**Electronics:** 1× roboRIO / roboRIO 2.0; 1× Vivid-Hosting VH-109 radio; 1× 12 V SLA battery 17–18.2 Ah; 120 A main breaker; ≥ 6 AWG main run, Anderson SB; power distribution from CTRE PDP / PDP 2.0, REV PDH, or AndyMark AMPD; branch protection ≤ 40 A, manual-reset only. One ROBOT SIGNAL LIGHT. Motors and controllers per the manual's Tables 6-2 and 6-4. Pneumatics: one compressor ≤ 1.1 cfm under closed-loop pressure-switch control through a legal pneumatics controller, store ≤ 120 psi, work ≤ 60 psi, single relieving regulator. All CAN actuation commands originate from the roboRIO.

## 8. Package deliverables and file map

```
SUMMIT-PUSH/
  README.md                          — package guide
  LICENSE.md                         — SUMMIT PUSH Training Use License
  REVISION-LOG.md                    — every change from v1.0, with rationale
  01-design/DESIGN-SPEC.md           — this file
  02-manual/GAME-MANUAL.md           — full manual (compiled; do not hand-edit)
  02-manual/SUMMIT-PUSH-Game-Manual.pdf — typeset manual (built by 06-style/pdf/)
  02-manual/sections/*.md            — manual source sections
  02-manual/manual-header.md         — compiled-manual front matter
  02-manual/build.sh                 — compiles sections into GAME-MANUAL.md
  02-manual/figures/                 — manual figures rendered from the field model
  03-field/FIELD-CAD-PACKAGE.md      — per-element CAD geometry spec + master dimension ledger
  03-field/MATERIALS-AND-COLORS.md   — appearance specification for every ARENA element
  03-field/renderings/*.svg          — 6 dimensioned drawing sheets
  03-field/renderings/generate_drawings.py — generates the drawing sheets
  03-field/featurescript/            — Onshape FeatureScript field generator
  04-vision/VISION-GUIDE.md          — tag table, placement geometry, simulation guidance
  04-vision/apriltag-field-layout.json
  04-vision/make_layout.py           — generates the layout JSON from the tag table
  05-cadathon/CADATHON-BRIEF.md      — challenge structure, timeline, deliverables, judging rubric
  06-style/MANUAL-STYLE-GUIDE.md     — typesetting standard for the PDF edition
  06-style/pdf/                      — PDF build
  verify/                            — verification suite
  00-research/, 00-concepts/         — design-phase research and concept archive
```

## 9. Authoring guardrails

- Rule numbering: G1xx personal safety, G2xx conduct, G3xx pre-match, G4xx in-match robot rules, G5xx piece rules; R1xx size/weight, R2xx safety/materials, R3xx budget/fabrication, R4xx bumpers, R5xx motors, R6xx power, R7xx control, R8xx pneumatics. Each rule carries a `Violation:` line using the VERBAL WARNING / MINOR / MAJOR / YELLOW / RED taxonomy.
- Glossary terms are ALL CAPS: CRAG, HEADWALL, BASECAMP, OUTFITTER, CENTER CACHE, CACHE CRATE, O2 CELL, ROPE COIL, CAMP (I/II/HIGH), SUMMIT BEACON, FORECAST, PRIORITY SUPPLY, ROUTE (LOW/MID/HIGH), APRON, LEDGE RUNG / CAMP RUNG / SUMMIT RUNG, SCORED, LEAVE, ROPED UP, SUPPLY LINE / EXPEDITION / ASCENT RP, LAST ROBOT CONTACT, E-STOP, A-STOP, OPERATOR CONSOLE, ARENA FAULT, SURROGATE, BACKUP ROBOT. Feature names that are not glossary terms (Low Socket, Mid Socket, Summit Socket, Low Peg, Mid Peg, High Peg, Shelf 1, Shelf 2) are title case everywhere; the generic "slot fence" stays lower case.
- Contact rules are written by outcome (damage / functional impairment / tipping) rather than by geometry. The protected zones are the intended line calls: the CRAG APRON, the OUTFITTER LANES, the ENDGAME HEADWALL ZONE, and during AUTO the opponent's side of the centerline.
- Every field element must be fully dimensioned for CAD reproduction from the drawing set; all robot-critical dimensions are on round or half-inch values; all angles are 15/30/45° only.
- Tone: third-person competition-manual voice. No sponsor, no team identity, no first-person plural, no marketing register. Examples and commentary are rendered as blockquotes that open with *Example:* or *Commentary:*, which the PDF edition sets as tinted boxes.
