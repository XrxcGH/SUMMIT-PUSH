# MAINLINE

> Design-phase archive. This document was written before the design specification (`01-design/DESIGN-SPEC.md`), which supersedes the geometry and scoring it describes. The current game is defined by that specification and the Game Manual (`02-manual/GAME-MANUAL.md`).

**Theme:** Transcontinental rail in its golden age. Two rival railway companies race to claim junctions, light the signals, and keep freight moving down a contested mainline.

**Narrative:** A single line of track joins the frontier, and two railway companies both claim the right-of-way. In MAINLINE, alliances of three robots load freight, raise fuel drums to the depot shelves, and hang signal lanterns high on the Union Tower to take control of the line; whoever holds the signals controls the railroad. As the final whistle nears, robots climb the signal gantries and throw the semaphore switches, turning the boards to their alliance's color.

## Game Pieces
### FREIGHT CRATE
- Shape/dims: Cube, 12.0 in x 12.0 in x 12.0 in, slightly compliant faces, ~2.0 lb
- Material: Ballistic-nylon fabric skin over a laser-cut corrugated-plastic internal frame with foam corner blocks (the 2018 Power Up cube construction, proven durable, ~$15 to fabricate; team version: cardboard box wrapped in duct tape)
- Handling challenge: Large, with floppy faces. It forces wide claws or top-down pinchers, tuning of squeeze force, and stack placement without toppling the crates below. Stacking to Level 3 (35 in) demands an elevator or 4-bar with controlled release.
- Count/staging: 30 total: 10 staged per alliance half (6 in a taped FREIGHT YARD zone beside the siding, 4 along the wing near midfield) plus 5 behind each alliance's Loading Dock for human-player feed. No crate preloads.
- Scoring role: The volume currency and the low floor. Crates score fixed points on flatcar stacks (uncontested, own side) and can be pushed into Depot ground bays, where each crate adds +1 Signal Weight toward depot ownership, so a kitbot pushing crates is fighting for territory.

### FUEL DRUM
- Shape/dims: Cylinder, 8.0 in diameter x 12.0 in tall, rigid with rolled top rim, ~3.0 lb
- Material: Roto-molded HDPE drum with molded rim lip (vendor-supplied; team version: 8 in concrete form tube with plywood end caps and gaffer tape)
- Handling challenge: It rolls when dropped and MUST be scored standing upright on a shelf, which forces a wrist or reorientation mechanism or clever passive funneling. A ground intake for a rolling cylinder, plus 90-degree reorientation to vertical, is the signature mechanism problem of the game.
- Count/staging: 12 total: 3 staged upright per alliance half beside each Depot face, 3 behind each Loading Dock. No preloads.
- Scoring role: The mid-value territory piece. Upright drums on Depot shelves score fixed points AND carry the heaviest depot Signal Weight (+2 low shelf, +3 high shelf), so drum specialists have the largest effect on depot ownership.

### SIGNAL LANTERN
- Shape/dims: Torus (ring), 10.0 in outer diameter, 3.0 in round cross-section (4.0 in inner hole), ~1.0 lb
- Material: Dense closed-cell foam ring with embedded fabric skin (the same construction as a gym or pool foam ring; team version: pool noodle bent into a hoop with fiber tape, under $5)
- Handling challenge: The smallest piece, and it must be HUNG on hooks angled 15 degrees up at heights up to 72 in. It demands a precise end effector, a tall elevator or extending arm, and AprilTag auto-alignment, because a 4 in hole over a 1.315 in hook leaves little error budget at full extension.
- Count/staging: 14 total: up to 3 preloaded per alliance (one per robot), 4 NEUTRAL lanterns staged on the centerline 4 ft either side of the Union Tower (contested in auto), 2 behind each Loading Dock.
- Scoring role: The premium currency. Lanterns on Union Tower hooks score the highest fixed points and are the ONLY source of Tower Signal Weight; the alliance with more weight owns the Tower and its 1 pt/sec accrual. Every lantern hung can visibly change the Headlamp.

## Field Layout
Standard 27 ft x 54 ft carpeted field, rotationally symmetric through 180 degrees.

CENTERLINE (the "MAINLINE"): three contested structures form a chokepoint band from wall to wall.
1. UNION TOWER at field center: a plywood-and-lumber tower with a 3.5 ft x 3.5 ft footprint, 8 ft tall. Each alliance-facing side carries 6 SEMAPHORE HOOKS for lanterns (two each at 36 in, 54 in and 72 in, angled 15 degrees up). The top carries the HEADLAMP, a 360-degree lamp that glows red, blue or white (neutral) to show ownership.
2. Two DEPOTS (Depot WEST and Depot EAST) on the centerline, each 5 ft wide x 2 ft deep x 5 ft tall, centered 4.5 ft from each side wall. Each Depot has a red face and a blue face. Each face has 4 ground-level crate bays (floor push-in slots 13 in wide), 3 low drum shelves at 18 in and 2 high drum shelves at 42 in (shelf surfaces tilted 15 degrees back toward the structure so drums settle inward). A 6 ft SIGNAL MAST on each depot swings a counterweighted semaphore paddle toward the owning alliance.
3. Travel lanes: two 4.5 ft gaps between the Tower and each Depot, and 4.5 ft between each Depot and the side wall. These are real chokepoints, each passable by one robot.

NEUTRAL ZONE staging: 4 neutral lanterns on the centerline, two 4 ft to each side of the Tower.

ALLIANCE HALVES: each alliance has (a) a FLATCAR SIDING 10 ft from its alliance wall, parallel to the right side wall, made of three 36 in x 36 in flatcar decks at 11 in height with a 1.5 in retaining lip, accepting crate stacks up to 3 high (L3 placed at 35 in); and (b) the SIGNAL GANTRY, an overhead truss 8 ft from the alliance wall spanning 20 ft, with three physically separated CLIMB STATIONS on 6 ft centers (rung details under Endgame) and a 4 ft x 4 ft BOARDING PLATFORM (2 in raised plywood) under each station.

LOADING DOCKS: each alliance's two human-player docks are in the corners of the OPPOSING alliance wall (2018-portal style), each a 14 in x 14 in delivery chute at 24 in height. This guarantees that every cycle crosses the centerline chokepoints.

AprilTags (36h11): 2 per Tower face, 1 per Depot face, 1 per Loading Dock, 1 per Gantry climb station, 2 on each alliance wall.

## Scoring Locations
| # | Location | Structure | Height | Approach angle | Pieces accepted | AUTO pts | TELEOP pts | Signal Weight |
|---|----------|-----------|--------|----------------|-----------------|----------|------------|---------------|
| 1 | Flatcar Level 1 | Siding (own side) | 11 in deck | Any of 3 open sides, flat approach | Crate | 4 | 2 | — |
| 2 | Flatcar Level 2 | Siding | place at 23 in | Same | Crate (stacked) | 6 | 3 | — |
| 3 | Flatcar Level 3 | Siding | place at 35 in | Same | Crate (stacked) | 8 | 4 | — |
| 4 | Depot ground bay (x4/face) | Depot W or E, your face | 0 in floor slot | Straight-in push, 13 in opening | Crate | 4 | 2 | +1 |
| 5 | Depot low shelf (x3/face) | Depot, your face | 18 in, 15-deg back-tilt | Straight-on, drum must be upright | Drum | 6 | 3 | +2 |
| 6 | Depot high shelf (x2/face) | Depot, your face | 42 in, 15-deg back-tilt | Straight-on at height | Drum | 10 | 5 | +3 |
| 7 | Tower low hooks (x2/face) | Union Tower, your face | 36 in, hook angled 15 deg up | Face-on, hang | Lantern | 8 | 4 | +1 |
| 8 | Tower mid hooks (x2/face) | Union Tower | 54 in | Face-on, hang | Lantern | 12 | 6 | +2 |
| 9 | Tower high hooks (x2/face) | Union Tower | 72 in | Face-on, hang | Lantern | 16 | 8 | +3 |

OWNERSHIP ACCRUAL (territory scoring, evaluated continuously):
- UNION TOWER: the alliance with strictly greater total Tower Signal Weight owns it and scores 2 pts/sec in AUTO and 1 pt/sec in TELEOP. On a tie, or with the Tower empty, it is neutral and nobody scores.
- EACH DEPOT: the alliance with strictly greater Depot Signal Weight on its face owns it and scores 1 pt per full 2 seconds of ownership (per depot).
- Max weight per depot face = 16 (4 crates + 3 low drums + 2 high drums); max Tower weight per face = 12. When a face is FULL, that side's weight is locked, so the territory war becomes a race to fill your face before the opponent out-weighs you.

Scoring notes and wording:
- A piece SCORES when it is fully supported by the structure (a lantern supported solely by its hook; a drum upright with its full base on the shelf; a crate fully within a bay or fully atop the stack below) and not in contact with any robot of the scoring alliance.
- Robots can never descore pieces. Counterplay is additive only: an alliance retakes a structure by out-placing the opponent. Field staff return pieces knocked off by contact from the structure's owner to the nearest Loading Dock. An opponent-caused knock-off is a G-foul (+5 to the placing alliance), and the piece is restored.
- Pieces leaving the field are returned to the nearest Loading Dock.
- All fixed placement points bank permanently when scored (a visible tick on the audience display). Ownership accrual is banked every second and is never revoked retroactively.

## Match Flow
2:30 total: 0:15 AUTO and 2:15 TELEOP, with the final 0:30 as the ENDGAME window (Gantry levers unlock at T-30). A typical cycle: collect from your Loading Dock in the OPPONENT'S corner or from staged field pieces, pass through one of the four 4.5 ft centerline chokepoints (Tower gaps or wall gaps), and place on your Depot face or Tower face, or run freight home to your siding. Because both alliances' feed points are across the field, all six robots cross paths continuously in the chokepoint band. The geometry creates contested space without forcing intake-vs-intake contact: each alliance scores on its own face of every centerline structure, so scoring robots stand back to back.

Defense: a defender can camp a chokepoint or shadow the opposing lantern robot, but with two Tower gaps and two wall gaps, no defender can seal the centerline. The standard 5-sec pin count applies.

Spectator legibility (the fix for the chess-match problem): the score state is displayed physically. The Headlamp glows in the owning alliance's color, both Depot semaphore paddles point at their owners, and the gantry boards turn at the endgame. A spectator can read the field at a glance: "blue lamp, two red paddles: blue is bleeding points at both depots but holds the Tower." Momentum swings are visible as soon as a lantern or drum lands.

Expected scores: median alliance ~110-150; strong alliance ~230-280 (roughly 45% ownership accrual, 35% placement, 20% endgame), so the balance between territory and freight stays in play all match.

## Autonomous
AUTO lasts 0:15 and has five elements.
1. GAME DATA, the EXPRESS ORDER: at T=0 the FMS randomly designates Depot WEST or EAST as the EXPRESS DEPOT (its signal mast lamp strobes white, and the character "W" or "E" is delivered through the game data API). During AUTO only, placements at the Express Depot score DOUBLE fixed points and DOUBLE Signal Weight, and the alliance that owns the Express Depot when auto ends banks a +10 EARLY DISPATCH bonus. Every serious auto must branch left or right on the game data (2018 Power Up-style software forcing), with AprilTag re-localization mid-path.
2. CONTESTED NEUTRALS: the 4 neutral lanterns sit on the centerline, two on each side of the Tower, reachable by either alliance. They create a race for extra Tower weight. They are staged 4 ft apart with approach vectors from opposite faces, so contests are races rather than collisions.
3. ALLIANCE COORDINATION: with three robots, one Express-Depot lane, one Tower face and a siding, alliances must negotiate lane assignments in advance. They typically run a designated "signal bot" (lantern to Tower), "express bot" (drum or crate to the strobing depot) and "freight bot" (crates to siding). The key skill is collision-free coordination of the three robots.
4. LEAVE: each robot fully exiting its starting zone scores 3.
5. GREEN SIGNAL bonus: if all 3 robots Leave AND the alliance owns the Union Tower at T=15, it banks +8.

The Tower accrues 2 pts/sec during auto, so a lantern hung in auto is worth its 8-16 fixed points plus up to ~20 seconds of early ownership. Auto therefore sets up the teleop territory war directly.

## Endgame
THE SIGNAL GANTRY: robots climb the truss and throw the switch. Each alliance's gantry has three separate climb stations on 6 ft centers (avoiding the 2019 HAB and 2024 stage pileups; each station has its own AprilTag for auto-align). Rungs per station: LOW RUNG at 2 ft 6 in; MID RUNG at 4 ft 3 in, offset 15 in horizontally behind the low rung; HIGH RUNG at 6 ft 0 in, offset another 15 in behind the mid rung; all are 1.25 in schedule-40 steel pipe. The offsets force a traverse (swing, walk or two-hook handoff), which is the hardest part. A high climb is a mechanism and control problem in the class of the Rapid React traversal, and it looks as hard as it is (s-neff compliant: a rung-to-rung swing does not look easy).

PARTIAL CREDIT, with no cliff; every tier banks independently at the buzzer (3-second settle):
- PARK on the 4 ft x 4 ft Boarding Platform = 3
- hang supported solely by the LOW RUNG (bumpers fully off the carpet) = 6
- MID RUNG = 12
- HIGH RUNG = 18
- THE LEVER = +5: a robot supported by the HIGH rung may pull the station's SIGNAL LEVER (a 12 in handle at 6 ft 9 in), which mechanically turns a 3 ft plywood semaphore board to the alliance color with an audible clack. Max 23/robot, 69/alliance.

Reward: three high climbs with levers can swing 69 points, enough to decide a close match, but a median alliance still banks 12-24 from parks and low hangs, so two minutes of freight work is never invalidated. The endgame is ~20-25% of a strong score, which corrects Crescendo's undervaluation without Steamworks' all-or-nothing. Climbing is legal at any time; levers unlock at T-30. The layout prevents traffic: three stations, 6 ft apart, each one robot wide. The lever flip is intended as the most visible moment of the match.

## Ranking Points
Win = 3 RP, Tie = 1 RP, plus up to 3 bonus RPs that all reinforce the core loop (no side quests). Thresholds escalate by event tier:

| Bonus RP | Definition | Regional | DCMP | Champs |
|---|---|---|---|---|
| FREIGHT RP (entry volume, target 40-60% of median alliances) | Combined total of placed pieces (crates + drums + lanterns, any location) | >= 20 | >= 25 | >= 30 |
| MAINLINE RP (stretch, ~3-3.5x entry difficulty, elite coordination only) | Hold ALL THREE centerline structures (Union Tower + both Depots) SIMULTANEOUSLY | >= 15 continuous seconds | >= 20 s | >= 25 s |
| GANTRY RP (endgame = "two robots do the mid-tier action") | Alliance Gantry points | >= 24 (two MID hangs, or one HIGH+lever plus a low/park) | >= 30 | >= 36 |

- FREIGHT is pure volume of the primary action; a kitbot's flatcar crates count fully.
- MAINLINE requires a lantern robot, a drum robot and a crate-bay defender working together while the opponents counter-place. The RP amounts to winning the territory war outright for a sustained period, and the crowd sees it as the lamp and both paddles in one color.
- All three RPs are read directly from the physical indicators and the placed-piece counter on the audience display, with no hidden bookkeeping.

## Low Floor
A kitbot chassis with a simple roller claw, or even a plywood plow, contributes throughout the match:
1. It pushes staged crates into Depot ground bays (floor level, 13 in openings, no lift required). Every crate is +2 and +1 Signal Weight, so the simplest robot on the field is fighting for territory ownership.
2. It shuttles crates onto Flatcar Level 1 (11 in deck, forgiving lip) on its own uncontested side for a steady 2 points each.
3. It ferries pieces from its Loading Dock to teammates staging near the centerline.
4. It parks on the Boarding Platform for 3, or adds a simple hook for the 2 ft 6 in LOW RUNG (a static hook + winch, the classic first climber project) for 6.

Perceived difficulty matches actual difficulty: pushing a box into a floor slot looks easy and is easy, and no task hides a precision requirement (unlike the 35-degree reef branches). A pure drivetrain robot can also legally camp a chokepoint lane on defense in elims. Median rookie contribution: ~30-45 points plus ownership swings, visible on the depot paddle every time.

## High Ceiling
Elite teams chase territory math weighted by throughput, which is never fully solved:
1. The three piece geometries (floppy 12 in cube, rolling 8x12 cylinder that needs reorientation, 10 in foam ring that needs precise hangs) cannot all be handled excellently under 115 lb. A robot that handles all three gives up climb speed or drivetrain, so archetypes persist: Lantern Specialist (tall elevator + ring wrist + traversal climb), Drum/Freight Superbot (fast ground intake + reorienting wrist, mid-height only), Chokepoint Defender/Crate Flooder, and Climb-Anchor.
2. The ownership economy has live tradeoffs. Is a 72 in lantern (8 pts + 3 weight) worth 9 seconds of cycle time, compared with two ground crates (4 pts + 2 weight) in 7 seconds? The answer changes with the match state, the opponent's composition and how full each face is. Capacity locking (16 weight max/face) creates real endgame calculations about territory, similar to bearing off in backgammon.
3. A late-season meta shift is built in. As climbs become common, value moves from holding accrual to racing to fill faces and denying levers by speed. The Express Depot randomization keeps auto development going all season (branching multi-piece autos that also take neutral lanterns).
4. The MAINLINE RP forces coordination scouting that matters in elims: who can hold structures as well as score.

No single robot is optimal, because holding all three structures requires three different mechanisms. Physics imposes this without any rule text.

## Teaching Value
The game is a full Rapid React/Power Up-class mechanism curriculum for a student team.
- MECHANICAL: ground intake design for three distinct geometries (compliant-wheel cube intake, cylinder capture, ring capture); indexing and transfer between intake and placement; a real elevator-versus-arm architecture decision (72 in hooks favor elevators; 42 in tilted shelves favor arms); a wrist or end effector for 90-degree drum reorientation; and a traversal climber (hook geometry, CG management, ratchet winches, spring-loaded passive hooks) with an optional lever manipulator.
- SOFTWARE: AprilTag 36h11 auto-alignment on Tower, Depot and Gantry faces (the small error budgets at height make this mandatory); full-field pose estimation through chokepoints; auto path planning with runtime branching on the W/E Express game data; deconfliction of multi-robot autos; and match-state strategy code (decision aids on the dashboard for owning versus placing).
- STRATEGY/SCOUTING: tracking ownership time teaches data-driven scouting beyond piece counts.

Every mechanism is used in every match (nothing like the 2020 control panel): the wrist, the elevator, the climber and the vision stack all earn points in quals and elims.

## Buildability
Every element breaks down into a team version from <= 2 sheets of plywood + hardware-store stock, with robot-critical dimensions on round or half-inch values (11 in deck, 18/36/42/54/72 in heights, 13 in bays, 1.25 in pipe rungs, all ramps and tilts at 15 degrees):
- UNION TOWER: four 2x4 corner posts and one sheet of 1/2 in ply for two faces. The hooks are 1.25 in schedule-40 pipe nipples in floor flanges, angled with 15-degree wedge blocks. The headlamp is optional (a colored work light, or even a painted flag on a pivot).
- DEPOT: one sheet of 3/4 in ply (shelves + face) on a 2x4 frame; the 15-degree shelf tilt comes from a single repeated wedge rip. The semaphore paddle is a plywood arm on a 3/8 in bolt pivot with a counterweight (teams can turn it by hand during practice).
- FLATCAR SIDING: half a sheet of ply per three decks on 2x4 legs with a 1.5 in lattice lip.
- GANTRY: two 4x4 posts + one 2x6 header per station, with three pipe rungs on floor-flange standoffs (the 15 in offsets are longer standoffs). The lever is a gate-hinge handle linked to a plywood board with rope.
- GAME PIECES: crate = taped cardboard box; drum = 8 in concrete form tube + ply caps (~$8); lantern = pool ring or taped pool-noodle hoop (~$5).

Nothing requires welding, CNC or purchased field electronics; a full practice field takes ~6 sheets of plywood and ~$250.

## Risks
- The balance between accrual and placement is the central tuning risk. If Tower pts/sec is even slightly too high, MAINLINE repeats the Power Up scale, where one lantern robot decides matches. The 1 pt/sec rate and the lantern weights need playtest tuning (mitigation: the capacity lock at 12 weight caps runaway ownership).
- The 4.5 ft chokepoint lanes concentrate defense. Pinning and incidental-contact fouls near the Depots could become a refereeing burden like the 2026 G415 problem. The back-to-back face geometry helps, but G-rules on 'contact while the opponent is placing' must be drafted tightly.
- Placing a drum upright on a 15-degree back-tilted shelf may become 'looks easy, is hard' for mid-tier teams if shelf tolerances are tight. Mitigate with a 1 in retaining lip and a generous 10 in shelf depth, and validate with a kitbot-grade arm before locking dimensions.
- Because counterplay is additive only, a filled, out-weighed Depot face becomes mathematically dead territory mid-match. If both depots lock early, the territory contest collapses into pure Tower play. A per-face capacity increase or a late-match 'second shelf row' unlock may be needed if playtests show early locking.
- The field indicator electronics (Headlamp, mast lamps, Express strobe) are the most failure-prone field components. Every ownership state must also be readable from the physical semaphore paddles, so that a dead lamp never hides the score.
- The traversal climb may be out of reach for median teams and make the GANTRY RP too rare at week-1 regionals (the Crescendo harmony risk in reverse). The 24-point regional threshold intentionally counts combinations that include parks and low hangs, but the thresholds must be rechecked against week-1 data.

## Spectator Hook
The final 30 seconds: the whole field state reads in color. The Headlamp and both semaphore paddles show one alliance's color while the other alliance's robots swing from rung to rung up the gantry trusses. A robot hanging six feet in the air pulls the signal lever, and a three-foot semaphore board swings over to its color as 23 points appear on the screen. Territory lamps changing in real time, plus robots throwing large switches overhead, give the audience a clear view of the match state.
