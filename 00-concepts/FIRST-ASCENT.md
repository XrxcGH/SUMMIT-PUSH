# FIRST ASCENT

> This is a design-phase document kept for reference. The current game is defined by `01-design/DESIGN-SPEC.md` and the Game Manual (`02-manual/GAME-MANUAL.md`).

**Theme:** High-alpine mountaineering. Two expedition alliances race up opposite flanks of the same peak, stock their high camps with supplies before a storm closes the mountain, and then make the summit push themselves.

**Narrative:** Two rival expeditions have 2 minutes and 30 seconds to ferry crates, oxygen and rope up the mountain, establish their camps before the storm arrives, and rope up for the final push up the headwall.

## Game Pieces
### CACHE CRATE
- Shape/dims: Cube, 12.0 in on each side, slightly pillowed faces, ~2.0 lb
- Material: Sewn ripstop-nylon skin over a polyurethane foam core (the Power Up cube construction, which has proven durable; teams can sew their own or build practice versions from upholstery foam + duct tape for under $10)
- Handling challenge: Large and compliant. It forces a wide ground intake or clamping claw and a flat, controlled placement onto shelves. It is too big to hoard more than one under a 120 in frame perimeter with other mechanisms aboard, so robots cycle one at a time.
- Count/staging: 20 total: 3 in the neutral Center Cache on the centerline, 2 staged per alliance side at taped marks, up to 1 preloaded per robot, and the remainder (8+ per alliance) stocked at the alliance's two Outfitter chutes
- Scoring role: The volume piece. It has the cheapest points per second, is the backbone of the Supply Line RP, and is the required 'shelter' component of every Camp bonus. The kitbot piece.

### O2 CELL
- Shape/dims: Cylinder, 5.0 in diameter x 14.0 in long, domed foam end caps, ~1.5 lb
- Material: 4 in Schedule-40 PVC core wrapped in a 0.5 in EVA foam sleeve with molded foam caps (team version: 4 in PVC + pipe-insulation foam + tape, ~$8)
- Handling challenge: It rolls on the carpet and must be reoriented from horizontal to near-vertical and inserted into an angled socket. This forces a wrist or end effector with orientation control and vision-assisted alignment. Insertion clearance is a forgiving 0.75 in per side (6.5 in ID sockets), so the task looks harder than it is.
- Count/staging: 20 total: 3 in the neutral Center Cache, 2 staged per alliance side, up to 1 preloaded per robot, remainder at Outfitter chutes
- Scoring role: The precision piece. It has the highest points per slot at mid level, gates the High Camp through the Summit Socket, and is the 'oxygen' component of every Camp bonus.

### ROPE COIL
- Shape/dims: Torus (ring), 10.0 in outside diameter, 2.5 in tube cross-section, ~1.0 lb
- Material: Solid molded rubber/foam ring (the class of large rubber tug-ring dog toys: durable, cheap, and able to survive being driven over; team version: pool foam ring or garden-hose coil wrapped in tape)
- Handling challenge: Thin and floppy relative to the other pieces. It needs a dedicated hook, spear or pinch gripper and a precise hang onto a 1.5 in peg angled 45 deg upward, including the 78 in high pegs at the extension ceiling, where robot stability and pose control matter.
- Count/staging: 20 total: 3 in the neutral Center Cache, 2 staged per alliance side, up to 1 preloaded per robot, remainder at Outfitter chutes
- Scoring role: The altitude piece. It is the only piece that scores at the 78 in tier, dominates High Camp math, and is the 'rope' component of every Camp bonus. Its 45 deg pegs echo a climber clipping into protection, which keeps the theme legible.

## Field Layout
Standard 27 ft x 54 ft carpeted field, rotationally symmetric (Rapid React style).

Midfield (the CRAGS): each alliance owns one CRAG, a plywood-and-pipe rock spire with a 4 ft x 4 ft footprint, 7 ft 6 in tall, centered on the field centerline and offset 7 ft from opposite long guardrails (Red Crag 7 ft from the scoring-table rail, Blue Crag 7 ft from the far rail). The 9 ft band between the two Crags is the CENTER CACHE: 9 neutral pieces (3 of each type) staged at taped marks straddling the centerline. Because both alliances score at midfield, all six robots cycle through and cross paths in the same central corridor, so the geometry creates contested space without forcing collisions. Each Crag scores on ALL FOUR faces, so a defender cannot block every approach.

Alliance ends: each alliance wall has three driver stations. The two wall corners each hold an OUTFITTER chute (human-player feed); the 3 ft wide taped Outfitter Lane in front of each chute is a no-defense zone. Centered 4 ft in front of each alliance wall stands the HEADWALL, a 12 ft wide climbing truss inclined 15 deg (endgame), with the taped BASECAMP zone (12 ft x 4 ft) beneath it. The Headwall is physically separated from the midfield scoring flow, so endgame traffic does not collide with late cycles. Each alliance side also has 6 staged pieces (2 of each type) at taped marks 12 ft from its wall.

Start zones: robots start in their Basecamp zone touching the alliance wall or Headwall.

AprilTags (36h11): 4 per Crag (one per face, centered 48 in high), 1 above each Outfitter chute, and 3 across each Headwall crossbeam, 22 tags in total, for full-field pose coverage. Tier LED rings wrap each Crag at 30 in, 54 in and 78 in and light in the alliance color when a Camp is established; a white LED band marks the pre-announced Storm Tier.

## Scoring Locations
All supply scoring is pick-and-place onto the alliance's own Crag (opponents cannot descore it). A piece is SCORED when it is fully supported by the scoring element and not in contact with any robot of that alliance; scores latch at the 5 s post-match settle.

| Location | Crag face | Count | Height | Angle / approach | Piece | AUTO | TELEOP |
|---|---|---|---|---|---|---|---|
| Base Depot tray | wraps 2 faces | ~12 capacity | floor, 4 in lip | push/drop in, any orientation | ANY | 4 | 2 |
| Shelf 1 | north | 3 slots (14 in wide) | 24 in | horizontal, flat placement | Crate | 6 | 3 |
| Shelf 2 | north | 3 slots | 42 in | horizontal, flat placement | Crate | 8 | 5 |
| Low Sockets | east + west | 2 | rim at 30 in | tube tilted 30 deg from vertical, insert from above | O2 Cell | 7 | 4 |
| Mid Sockets | east + west | 2 | rim at 54 in | 30 deg from vertical | O2 Cell | 10 | 7 |
| Summit Socket | spire top | 1 | rim at 66 in | 15 deg from vertical | O2 Cell | 13 | 10 |
| Low Pegs | south | 2 | 30 in | 1.5 in OD peg, 45 deg upward | Rope Coil | 7 | 4 |
| Mid Pegs | south | 2 | 54 in | 45 deg upward | Rope Coil | 9 | 6 |
| High Pegs | spire | 2 | 78 in | 45 deg upward | Rope Coil | 12 | 9 |

CAMP BONUSES (latched once earned; the tier's LED ring lights when the Camp is established):
- CAMP I (Low tier holds ≥1 crate on Shelf 1 + ≥1 low O2 + ≥1 low rope): +6
- CAMP II (Shelf 2 crate + mid O2 + mid rope): +10
- HIGH CAMP (Summit Socket + both high pegs): +15
- The forecast's STORM TIER camp pays double (+12 / +20 / +30).

Notes: every height band (0 / 24-30 / 42-54 / 66-78 in) and three approach angles (horizontal shelf, 30-45 deg insertion/hang, floor push) are represented, and all values sit on whole or half-foot dimensions. The Depot gives every robot a floor-level job; the 78 in tier sits at the extension ceiling.

## Match Flow
2:30 match = 15 s AUTO + 2:15 TELEOP (the final 30 s is the endgame window, with climb protection). A cycle is: collect at your Outfitter corner chute or from staged or loose floor pieces, drive ~20 ft to your midfield Crag, place, and return. Both alliances' cycles converge on the same central corridor between the Crags, so robots cross paths constantly. Defense is legal everywhere except in opponent Outfitter Lanes and against robots in contact with their own Headwall in the last 30 s, subject to pinning limits (5 s count). Because each Crag scores on all four faces, a single defender can delay a robot but cannot shut it out. Effective defenders shade the Center Cache and the corridor instead of camping a face, so there is no intake-vs-intake G415 trap. Spectators can read the match at a glance from the pieces accumulating on the two spires and the LED tier rings that light as Camps are established. Typical strong-alliance match: 25-35 auto, 20-28 teleop placements, 2-3 Camps (30-60 bonus), 40-65 climb; scores in the 160-220 range, with median-alliance matches near 100.

## Autonomous
Auto lasts 15 seconds. The FORECAST: when auto begins, the FMS pushes a game-data string (WHITEOUT, ICEFALL or GALE) and the field LEDs flash it. Each forecast fixes two things for the whole match: the PRIORITY SUPPLY (Whiteout=Crates, Icefall=O2, Gale=Ropes), which scores double auto points, and the STORM TIER (Whiteout=Low, Icefall=Mid, Gale=High), whose Camp bonus pays double all match and anchors the Expedition RP. Robots must read game data and branch their autos in code (2018-style, with at least three prepared paths), which teaches software branching.

Choices: score your own-side staged pieces safely, or race for the contested Center Cache on the centerline, where opposing autos arrive at the same time (higher risk, and the only way to run autos of 4+ pieces). LEAVE: 3 pts per robot for fully exiting Basecamp. ROPED UP bonus: if all three robots Leave and the alliance scores ≥4 pieces in auto, including at least one of each type, +10. This forces alliance coordination: who takes crates, who takes O2, who takes ropes, and deconflicted paths agreed in the queue.

Vision: AprilTags on every Crag face enable auto-align for socket insertion and peg hangs; Center Cache autos require full-field pose estimation. Auto has lasting consequences. The Storm Tier revealed at the start of auto dictates teleop Camp strategy, and Camp progress banked in auto (auto placements count toward Camps) sets up the race for the double Storm Camp.

## Endgame
The HEADWALL is a 12 ft wide truss inclined 15 deg from vertical, standing 4 ft in front of each alliance wall. It is divided into THREE independent 4 ft lanes, so all three robots climb side by side without traffic (no 2019 HAB pileups). Each lane carries three 1.5 in OD rungs at 30 in (LEDGE), 54 in (CAMP) and 78 in (SUMMIT). Because the wall leans 15 deg, each rung sits ~6.5 in behind the one below, and the rungs are staggered 12 in laterally within the lane. Reaching the Summit is therefore a two-handoff traversal on an inclined, offset ladder (a problem in the class of the 2022 traversal: hook geometry, CG management, swing damping, a sequencing state machine).

Points (multi-tier partial credit, no cliff): PARK in Basecamp = 3; supported by the Ledge rung = 12; Camp rung = 20; Summit rung = 30. A robot that attempts the Summit and falls back to Camp still scores 20, and a failed climber still parks for 3, so every stage of the attempt scores. Climbs are scored at match end + 5 s settle, by the highest rung solely supporting the robot (no carpet contact). Robots in contact with their own Headwall during the final 30 s are protected from opponent contact.

Difficulty: the 15-deg lean pushes the robot's CG away from the wall, the lateral stagger defeats simple telescoping hooks, and a 78 in reach sits at the extension ceiling. Reward: 30 points equals 6-10 placement cycles, enough to swing any close match, and three simultaneous traversals in front of each alliance wall are easy for the audience to follow. The climb can decide a match without invalidating two minutes of cycling (max alliance climb 90 vs. typical 100+ from supplies and camps).

## Ranking Points
Win = 3 RP, Tie = 1 RP, plus up to 3 bonus RPs that all reinforce the core game:

| Bonus RP | Regional | DCMP | Champs | Design intent |
|---|---|---|---|---|
| SUPPLY LINE RP — total supplies scored on Crag + Depot | ≥15 | ≥19 | ≥23 | Entry-volume RP: three median robots at ~5 pieces each reach it in ~50% of matches; every kitbot Depot piece counts |
| EXPEDITION RP — Camps established | 2 Camps incl. the Storm Tier camp | All 3 Camps | All 3 Camps AND Storm Tier at full capacity (every slot of that tier filled) | Stretch RP at ~3x entry difficulty: demands coordinated scoring of all three pieces at height; the forecast rotates the target from match to match, so it never collapses into one rehearsed pattern |
| ASCENT RP — alliance endgame climb points | ≥40 | ≥52 | ≥62 | Matches 'two robots do the mid-tier action' (2 x Camp rung = 40); escalates toward one Summit + support |

All three RPs are earned by doing more of the main game (placing supplies, completing tiers, climbing); none requires a side-quest mechanism.

## Low Floor
The documented KITBOT PATH (published like the 2024 KitBot) is an AM14U-class drivetrain + a fixed-height roller claw that handles only Cache Crates. That robot preloads a crate and scores it in auto (Depot, 4 pts) and Leaves (3). It then cycles crates all match into the Depot (2 each) and onto Shelf 1 at an accessible 24 in (3 each), and every one of those crates counts toward the Supply Line RP and the Camp I crate slot. It parks for 3 at the end. That is 20-30 points and an RP-relevant contribution in every match, with a natural upgrade path: add a wrist to unlock O2 sockets; add an elevator for Shelf 2 and the mid tiers; add hooks for the Ledge rung. Perceived difficulty matches actual difficulty everywhere (the s-neff test): the Depot and the 24 in shelf look easy and are easy; the Summit Socket and the traversal look hard and are hard. No task punishes a rookie for trying.

## High Ceiling
Elite teams chase four things.
1. The universal-versus-specialist end-effector problem. A gripper that handles a 12 in compliant cube, a 5 in cylinder that needs 90-deg reorientation and a floppy 10 in ring is heavy and slow, so weight forces archetypes: Crate Freighter (volume, low-mid), O2 Surgeon (socket insertion, Summit Socket owner), Ring Alpinist (78 in pegs + Summit rung) and a Hybrid mid-tier robot. No single robot covers the whole mountain under 115 lb.
2. Center Cache autos of 4-6 pieces, with path planning in contested space and forecast branching.
3. AprilTag-aligned socket insertions in under 4 seconds.
4. A repeatable 15-second Summit traversal.

The meta stays unsolved for three reasons. The Forecast rotates the doubled Storm Tier every match (so alliance value shifts from match to match). Camp completion makes MIXED alliances worth more than three copies of the best robot, so the 2015 monoculture is structurally impossible. The depot and low-tier economy leaves room for a late-season 'L1-style' revaluation once the high tiers saturate in champs-level play.

## Teaching Value
The game is designed to cover a full curriculum.
- Mechanical: ground intake (three geometries, which students must prototype and down-select), serializer/indexer (the piece must travel from the intake to the placement pose), the standard elevator-versus-arm decision (flat shelves favor elevators; 45-deg pegs and 30-deg sockets favor arms; the 78 in tier forces continuous elevators or two-stage arms), wrist and end-effector design (O2 reorientation is a classic 2-DOF wrist problem), and a real climber with hook geometry, ratchets and CG analysis for the staggered traversal.
- Software: game-data parsing and multi-branch autos (Forecast), AprilTag auto-align for socket and peg placement, full-field pose estimation for Center Cache races, mechanism state machines (modes by piece type), and climb sequencing.
- Strategy: scouting must track each robot's capability with each piece and its performance on the Storm Tier, which makes building a pick list a real exercise.

Every subsystem a student builds is used in every match; no mechanism is abandoned by week 3 the way the 2020 control panel was.

## Buildability
TEAM VERSIONS (each element ≤2 sheets of 3/4 in plywood + hardware-store stock):
- CRAG: 2 sheets of plywood (four faces + two shelves + depot tray), 1.5 in closet dowel or Schedule-40 pipe cut at 45 deg for pegs, three 18 in lengths of 6 in Sonotube concrete form (~$15) screwed on at 30/15 deg for sockets, and a 2x4 internal frame; total <$180.
- HEADWALL: one plywood sheet + 2x4 A-frame lumber leaned at 15 deg (a speed-square angle) + three 4 ft lengths of 1.25 in black iron pipe as rungs on stagger brackets. A single-lane practice version fits in any shop.
- GAME PIECES: crates from upholstery foam + duct tape or sewn ripstop (~$10); O2 cells from 4 in PVC + pipe insulation (~$8); rope coils from large rubber ring dog toys or foam pool rings (~$8). All are durable enough to be driven over, on the model of the 2022 dog-toy cargo and unlike the fragile 2024 note foam.

Every robot-critical dimension is a round or half-inch value (12 in cube, 5 in cylinder, 10 in ring, 1.5 in pegs and rungs, heights at 24/30/42/54/66/78 in), and angles occur ONLY at 15/30/45 deg. Nothing on the field repeats the 35-deg angle of the 2025 reef branches.

## Risks
- Midfield congestion around the Crags could strain the refereeing of pinning and contact in elims. Four-face scoring and wide corridors mitigate it, but a disciplined two-defender strategy might still choke the center corridor, which needs playtesting with real drive teams.
- Specialization forced by weight means a regional alliance drawn without an O2- or ring-capable partner may be mathematically locked out of the Expedition RP. The Depot 'any piece' path softens this, but qualification-schedule luck could hurt at small events.
- The Summit traversal may see <10% success in weeks 1-2 (the Steamworks climb-frustration pattern). The 12/20-point intermediate rungs relieve the pressure, but the stagger distance (12 in) and the rung diameter need physical prototyping before the numbers are locked.
- O2 socket insertion tolerance (0.75 in per side) is designed to be forgiving, but if field-build variance shrinks it, the task changes from 'looks hard, is achievable' to the kind that s-neff described as frustrating. The socket ID must be a strictly toleranced field dimension.
- The Forecast mechanic requires FMS game-data support. Offseason and practice-field play needs a published fallback (dice or card draw + manual LED), or the interactive auto degrades to a scripted one.
- Hanging rings on 78 in pegs at the 78 in extension ceiling invites high-CG tip-overs during defense. A no-contact rule near the Crag faces was intentionally left out to preserve defense, so tip-over frequency must be monitored at week-zero events.

## Spectator Hook
The final 30 seconds. Both mountains show their earned Camp LEDs while six robots climb the Headwalls at once: three per alliance, side by side, swinging up staggered rungs on a leaning wall, with each rung scoring as it is reached. A 30-point Summit grab at the buzzer can decide a close match. The format is Rapid React's traversal in three parallel lanes, directly in front of the audience.
