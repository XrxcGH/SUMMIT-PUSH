# HIGHBALL

> This is a design-phase document kept for reference. The current game is defined by `01-design/DESIGN-SPEC.md` and the Game Manual (`02-manual/GAME-MANUAL.md`).

**Theme:** Transcontinental railroading in its golden age. Two rival freight lines race to load their trains, run the mail, and get their crews aboard before the departure whistle.

**Narrative:** Two freight lines receive the same order from the dispatch board: the overland express leaves at midnight, full or not. Crews haul crates to the flatcars, roll fuel barrels to the tankers, and pass mailbags hand to hand down the line to make the mail hooks in time. Each full car lights a lamp, and when the whistle blows, the crews board the train. ("Highball" is the railroad signal to proceed at full speed.)

## Game Pieces
### CARGO CRATE
- Shape/dims: Cube, 11 in x 11 in x 11 in, slightly crowned faces, ~2.0 lb
- Material: Molded EPP foam core with a ballistic-nylon/vinyl cover and cross-stitched seams (the POWER UP cube construction, which is proven durable and cheap to replicate with a foam block + fabric cover)
- Handling challenge: Flat-faced and grippy, so it is easy to hold but awkward to orient. It forces a wide compliant claw or a wheeled top-down intake, plus a wrist to seat it flat on decks and through the 18-in stock car door. The 'looks hard but is easy' entry piece.
- Count/staging: 20 total: 6 in each alliance DEPOT (preloads drawn from this allotment, 1 per robot, any piece type), 6 contested at the midfield JUNCTION, 1 staged dockside at each train
- Scoring role: Volume currency. Accepted by the Caboose (1), Flatcar (2) and Stock Car (5). Drives the Freight RP piece count and the cheap full-car bonuses.

### FUEL BARREL
- Shape/dims: Rigid cylinder, 8 in diameter x 12 in tall, with 1-in rolled rim lips at both ends, ~1.5 lb
- Material: Blow-molded HDPE drum (hardware-store 2-gal utility pail blank / off-the-shelf HDPE drum with capped ends); team version: 8-in SDR-35 PVC pipe section with glued end caps
- Handling challenge: It rolls when dropped and must be scored UPRIGHT in the tank hatch. This forces orientation control: rollers that stand it back up, or a cradle intake plus indexing. The rims give claws a purchase line at 12 in spacing.
- Count/staging: 16 total: 4 in each alliance DEPOT, 4 at the JUNCTION, 2 staged dockside at each train
- Scoring role: Mid- and high-value currency. Accepted by the Caboose (1), Flatcar (2, standing in a stanchion pocket), Stock Car (5) and the 52-in Tank Car hatch (7). The hatch is the premium drop that separates elevator robots from claw robots.

### MAILBAG
- Shape/dims: Soft stuffed duffel, 16 in long x 7 in diameter, with one 5-in-inside-diameter webbing loop handle sewn to one end, ~1.2 lb
- Material: 1000D Cordura shell, foam-bead fill, bar-tacked 2-in seatbelt webbing handle (a sewn piece in the dog-toy class: floppy, cheap, nearly indestructible; the team version is a stuffed duffel from any fabric store)
- Handling challenge: Floppy and conforming. It defeats rigid claws and rewards compliant wheeled intakes. The handle must end up presented so that it can hang on a 15-degree peg at up to 60 in, and the mailbag is the piece designed for robot-to-robot handoffs in the Mail Relay.
- Count/staging: 12 total: 3 in each alliance DEPOT, 4 at the JUNCTION, 1 staged dockside at each train
- Scoring role: The teamwork piece. It hangs only on Mail Car hooks (40 in = 4 pts, 60 in = 7 pts) and scores +3 MAIL RELAY when two or more alliance robots possessed it during the delivery, HIGHBALL's equivalent of the Aerial Assist mechanic.

## Field Layout
Standard 27 ft x 54 ft carpeted field, rotationally symmetric (180 degrees). Key structures:

1. TRAINS (one per alliance, scored on by that alliance only): a 16-ft-long, 36-in-wide train of five cars (Caboose, Flatcar, Stock Car, Tank Car, Mail Car, each ~38 in long) parked parallel to a guardrail side wall, 36 in off that wall, spanning from 6 ft to 22 ft from the FAR end wall. Each alliance's train sits in the OPPOSITE half of the field from its driver stations: Red's train is in the Blue half along one side wall, and Blue's train is mirrored in the Red half along the other side wall. All scoring faces point into the open field. A 12-in-wide BOARDING PLATFORM strip (paint or tape) runs along the field side of each train and hosts the endgame SIGNAL GANTRY overhead.

2. DEPOTS (one per alliance): a human-player loading station in each alliance's own end wall, offset toward the corner diagonally opposite that alliance's train. Each has a 30-in-high delivery shelf and a floor chute; the taped 8 ft x 8 ft DEPOT ZONE in front is protected space. The run from depot to train is a ~45-ft diagonal across midfield, so the two alliances' shipping lanes cross at center by design.

3. THE JUNCTION (center field): two GRADE CROSSINGS on the centerline, each a plywood hump 6 ft wide with 15-degree ramps rising to a 6-in-high, 24-in-wide flat crown. They are placed to leave three open flat lanes (8 ft each side lane, 8 ft center lane). 14 neutral contested pieces (6 crates, 4 barrels, 4 mailbags) start staged on and beside the crossings. This is the game's contested ground and natural defensive chokepoint, with routes around it so that nothing forces collisions.

4. DOCKSIDE STAGING: 4 pieces (1 crate, 2 barrels, 1 mailbag) staged on the carpet 5 ft field-side of each train for fast auto deliveries.

5. STARTING LINES: each alliance has two, a HOME LINE 10 ft out from its own end wall and a TRACKSIDE LINE alongside its own train in the far half. Robots choose one at setup (see autonomous).

AprilTags (36h11): two per car face (10 per train), one at each depot shelf, one on each gantry upright, and one per grade-crossing crown post, giving full-perimeter pose coverage.

## Scoring Locations
All heights are measured from the carpet. All scoring faces point into the open field (approach is from the field side; the wall side is dead space, which keeps traffic one-sided and legible).

| Location | Height / Geometry | Approach | Pieces accepted | Capacity | Teleop | Auto (2x) |
|---|---|---|---|---|---|---|
| CABOOSE bay | Carpet level, entered up a 15-degree, 24-in-wide ramp with no lip | Drive-up push, any angle | Crate, Barrel, Mailbag | 10 | 1 | 2 |
| FLATCAR deck | 8-in-high deck, 12 in deep, 1-in retaining lip; 4 stanchion pockets for upright barrels | Side placement, wide angle | Crate, Barrel (upright) | 6 | 2 | 4 |
| STOCK CAR door | 18 in wide x 16 in tall opening, sill at 24 in; clear polycarbonate slatted walls so contents are fully visible | Square-up side insert | Crate, Barrel | 8 | 5 | 10 |
| TANK CAR hatch | 12-in-diameter funnel opening at 52 in, clear tank body | Top drop, field side, near-vertical release | Barrel (upright drop) | 6 | 7 | 14 |
| MAIL CAR low hooks | Four 6-in pegs (1.05-in OD) at 40 in, angled 15 degrees up | Hang by handle, straight-in | Mailbag | 4 | 4 | 8 |
| MAIL CAR high hooks | Three 6-in pegs at 60 in, angled 15 degrees up | Hang by handle, straight-in, high reach | Mailbag | 3 | 7 | 14 |

Bonuses and notes:
- FULL CAR: when any car reaches capacity, the alliance scores +10 and a 12-in amber marker lamp on that car's roof lights, so scoring progress can be read from the last row of the stands.
- MAIL RELAY: +3 per scored mailbag possessed by 2+ alliance robots between leaving a depot, staging mark or the floor and being scored (referees track only the 12 mailbags, a workload similar to the 2014 assists).
- PRIORITY DELIVERY (auto only): +5 per delivery made in Dispatch Manifest order; +10 ON-TIME DEPARTURE for completing all three in auto (see autonomous).
- Scoring definitions: a piece is SCORED when it is at rest and fully supported by the car (or suspended by a hook), touching neither the floor nor any robot of the scoring alliance. Pieces in motion at the buzzer count if they settle scored within 3 seconds. Removing pieces from any car (either alliance's) is a tech foul, and the piece counts as scored. Field staff return pieces that leave the field to the nearest depot. Adding pieces to the opponent's train only helps the opponent, so there is no junk-feeding exploit.
- LEAVE (auto): 2 points per robot fully leaving its starting line.
- Tie-breaks: endgame points, then auto points, then fewest foul points.

## Match Flow
2:30 total: 0:15 AUTO and 2:15 TELEOP, with the final 0:45 as the boarding window. The core loop is a full-field freight cycle: load at your depot (or grab contested pieces at the Junction), run the ~45-ft diagonal through midfield, and place on your train at the far end. Because the two alliances' lanes are mirror-image diagonals, all six robots stream through the Junction in opposite directions all match. The result is constant crossing traffic, as in Aerial Assist, with no single forced collision point (three lanes plus two 15-degree hump routes). Defense concentrates at the Junction and on the contested neutral pieces there. Depots, boarding platforms and gantries are protected zones, so intake-vs-intake scrums do not happen at the structures. The Mail Relay creates real passing plays: one robot ferries mailbags across midfield and hands them (by the handle) to a tall partner stationed trackside, which turns a 7-point high hook into a 10-point relayed delivery. Spectators can read the match quickly: cars fill visibly (clear stock car and tank walls, mailbags silhouetted on hooks), and every FULL CAR lights an amber roof lamp, so the lamp count tracks the score. The endgame sends each alliance to the opposite end of the field, so the final 45 seconds hold two separate, simultaneous climbs with no cross-alliance traffic.

## Autonomous
Auto lasts 15 seconds and is built on three linked decisions:

1. STARTING LINE CHOICE (alliance coordination): each robot sets up on either its HOME LINE (near its depot, 1 preloaded piece, a long full-field auto) or its TRACKSIDE LINE (beside its own train in the far half, where 4 dockside pieces are staged). A trackside robot can realistically score 2 pieces in auto; a home robot runs one long delivery and takes up field position. Alliances must negotiate the split in the queue: three trackside robots starve (there are only 4 dockside pieces), and three home robots waste the staged pieces.

2. DISPATCH MANIFEST (game data): at T=0 the FMS reveals a randomized ordering of {STOCK, TANK, MAIL} on the arena screens (2018-style). The first piece your alliance scores in each of those three car types must follow the manifest order to earn +5 PRIORITY DELIVERY each; completing all three within auto scores +10 ON-TIME DEPARTURE and lights the locomotive headlamp. This forces branching auto routines (6 orderings), role assignment before the match ("you take tank if it's first, I take mail"), and re-sequencing in real time if a partner's auto fails, which is the kind of software depth for which 2018 was praised.

3. VISION-DEPENDENT PLACEMENT: every auto scoring action is a pick-and-place at a defined pose (52-in barrel drop, 60-in hook hang), practical only with AprilTag pose estimation and on-the-fly path planning to the tag on each car face.

Auto pieces score double, LEAVE is 2, and contested Junction pieces are legal to collect (auto contact is a tech foul, and the split between trackside and home starts means most alliances never meet in auto). Auto affects the rest of the match: pieces banked in auto count toward FULL CAR lamps and the Freight RP, and manifest completion feeds the stretch RP at higher event tiers, so a strong auto sets up the whole match instead of standing apart as a minigame.

## Endgame
CATCH THE TRAIN. A SIGNAL GANTRY, a 16-ft pipe truss on A-frame uprights, spans above each alliance's own train, with three independent boarding stations spaced 48 in apart (one per robot, so there are no traffic jams). Each alliance's endgame is at its own far end of the field, so the two alliances never share endgame space. Boarding is legal only in the final 45 seconds, and points are assessed 3 seconds after the buzzer. There are three tiers of partial credit per robot:

- FOOTBOARD (3 pts): park fully supported on the 12-in-deep, 6-in-high step plate running along the boarding platform. Any drivetrain can earn this; it is the floor of the endgame.
- GRAB IRON (8 pts): hang from a rigid 1.25-in-OD bar at 48 in, fully off the carpet. This is a climb in the class of the Rapid React mid rung, and it is the mid-tier action.
- BRAKEMAN'S BAR (15 pts): hang from a 1.25-in bar at 72 in that is HINGED from the truss and swings freely +/-20 degrees, reached either by direct extension or by transferring up from the Grab Iron. The swing is the test of mastery. Passive hooks that work on the rigid bar oscillate wildly here, and elite solutions damp the swing (dual hooks, timed transfer, active wrist) as in 2022's traversal. The task looks hard, is hard, and pays accordingly.

Rationale: 3/8/15 per robot means a failed high attempt still banks 8 or even 3, so there is no Steamworks cliff and no wasted two minutes. The maximum of 45 alliance points is enough to swing any close match (a lone Brakeman's Bar is a quick 15-point comeback) but is under a third of a good alliance's freight total, so cycling still decides matches. Contacting an opponent that is touching its gantry in the boarding window is a tech foul that awards the victim full Brakeman's Bar credit. Climbs are therefore protected, and the three swinging robots silhouetted against the lit marker lamps end every match.

## Ranking Points
Win = 3 RP, Tie = 1 RP, plus up to 3 bonus RPs that all reinforce the core freight and boarding game (no side quests):

| Bonus RP | Definition | Regional | DCMP | Champs |
|---|---|---|---|---|
| FREIGHT RP (entry volume) | Total pieces scored on your train (any car) >= threshold | 16 pieces | 20 | 24 |
| FULL CONSIST RP (stretch) | Number of cars at full capacity (lamps lit) >= threshold, AND at least 2 auto Priority Deliveries | 2 cars | 3 cars | 3 cars + ON-TIME DEPARTURE |
| ALL ABOARD RP (endgame) | Alliance endgame points >= threshold | 16 (two Grab Irons) | 19 (two Grab Irons + a Footboard) | 23 (Brakeman's + Grab Iron) |

Calibration against the rubric: FREIGHT at 16 pieces is ~50% achievable for a median regional alliance (three robots averaging ~5-6 cycles). FULL CONSIST demands coordinated car targeting and auto execution (~3x harder, the territory of elite alliances). It consumes the SAME scoring actions, only aimed, so chasing it never conflicts with winning the match. ALL ABOARD at 16 equals 'two robots do the mid-tier action.' The escalation columns keep the meta moving through the season so that it is not solved by week 3.

## Low Floor
A kitbot with a drivetrain and a simple pool-noodle roller intake plays all match. It can push or carry any piece up the zero-lip 15-degree ramp into the CABOOSE (1 pt each, capacity 10); place crates on the 8-in FLATCAR deck with the simplest hinged arm (2 pts); ferry mailbags across midfield and hand them to a tall partner for +3 MAIL RELAYS (contributing to 10-point deliveries without ever lifting above bumper height); bank a 2-pt LEAVE and a dockside caboose push in auto; and finish with a guaranteed 3-pt FOOTBOARD park. That is 15-25 points plus relay assists plus defense at the Junction. Every one of those tasks looks as easy as it is (the s-neff principle): the ramp, the 8-in deck and the step plate are visibly gentle, and no low-floor task has hidden difficulty.

## High Ceiling
Elite teams chase a set of compounding optimizations that are never finished:
- full-field cycles under 13 seconds that thread Junction traffic;
- an intake for three geometries (rigid cube, rolling cylinder, floppy sack) within one weight budget. No robot can handle all three pieces at all heights at 115 lb, so archetypes split (tank-hatch elevator specialists, mail-hook arm robots, caboose-volume floor sweepers, relay ferries) and alliance selection becomes real strategy;
- six branching manifest autos with re-sequencing mid-auto when a partner fails;
- choreographed Mail Relay chains that turn the 7-pt high hook into a 10-pt passing play;
- endgame mastery of the free-swinging Brakeman's Bar, with a damped transfer from the Grab Iron;
- the open late-season meta question: is the third robot better as a Junction defender denying contested pieces, a caboose volume robot feeding the Freight RP, or a dedicated relay ferry?

Pieces are scarce (48 pieces, 37 needed for a full consist), so control of the contested pieces at the Junction late in the match becomes a skirmish of its own, close to an endgame. No single robot design solves HIGHBALL.

## Teaching Value
The game forces the full spread of mechanisms seen in Rapid React and Power Up:
1. ground intakes for three geometries: compliant wheels for the mailbag, orientation-correcting rollers for the barrel, and a wide claw or top-down intake for the crate;
2. indexing and transfer from the intake to the placement pose, including standing a barrel back upright;
3. the elevator-versus-arm decision (the 52-in tank drop and 60-in hook favor elevators; the 24-in stock door and 8-in deck favor arms; students must argue the tradeoff with numbers);
4. a wrist or end effector that presents a floppy handle to a 15-degree peg;
5. climber engineering in three difficulty steps ending at a swinging bar: hook geometry, CG control, oscillation damping and sequencing.

Software: AprilTag pose estimation and auto-align to car faces (hanging on hooks is effectively impossible without it), full-field path planning through Junction traffic, six-way branching autos from FMS game data, and alliance-coordination logic (who starts trackside, who takes which manifest slot). Drive practice teaches passing plays and reading traffic, skills from team sports that go beyond cycling.

## Buildability
Every element breaks down into a team version from <=2 sheets of plywood plus hardware-store stock, with all robot-critical dimensions on whole or half inches and all ramps at 15 degrees:
- TRAIN CARS are 3/4-in plywood boxes on 2x4 skids. Caboose: half-sheet box + 15-degree ramp. Flatcar: 8-in-high platform with 1-in lattice lip and four 8.5-in-ID pockets from 8-in pipe couplings. Stock Car: plywood frame with an 18x16 door at a 24-in sill, and walls of clear polycarbonate (or chicken wire for the team version). Tank Car: a 52-in plywood tower topped with a 12-in-ID funnel cut from a bucket. Mail Car: a plywood face with 3/4-in Sch40 pipe pegs at 40 in and 60 in, angled 15 degrees in pipe flanges.
- SIGNAL GANTRY: two 2x6 A-frames + a 1.25-in rigid conduit crossbar. The Grab Iron is fixed conduit at 48 in; the Brakeman's Bar is conduit on two gate hinges at 72 in.
- GRADE CROSSING: one sheet of 3/4 plywood ripped into two 15-degree ramp faces over 2x6 crowns.
- Marker lamps: $10 battery puck lights toggled by a limit switch or by a volunteer.
- Game pieces: crate = foam block + sewn cover; barrel = 8-in PVC with caps; mailbag = fabric-store duffel with seatbelt webbing.

A full practice field costs under ~$600.

## Risks
- Scoring on the far side strains driver sightlines (your train is 45+ ft from your glass). AprilTag auto-align, large marker lamps and high-contrast car faces mitigate this, but teams with weak vision will feel it; the caboose and flatcar exist partly as fallbacks with no tight tolerances.
- MAIL RELAY tracking adds referee workload (mailbag possession across robots). It is capped at 12 bags in play and modeled on 2014 assist refereeing, but the wording on 'possession' must be airtight or it will attract protests.
- The mailbag handle is the most stressed feature on any piece (hung, yanked, handed off). It needs abuse testing at the level of the Crescendo note, and a torn handle mid-match needs a defined replacement rule.
- With the free-swinging Brakeman's Bar at 48-in station spacing, an oscillating robot could contact a neighbor's climb. The spacing may need to grow to 54-60 in after field testing, at the cost of gantry width.
- Auto traffic: trackside starters from both alliances and full-field home runners share the field in auto. The tech foul for contact and the lane geometry should prevent 2016-style auto collisions, but six aggressive autos crossing midfield need simulation before the starting-line positions are locked.
- The stock car door (18x16 at a 24-in sill) could jam if two partners feed it at the same time. The interior needs a settling floor slope (5 degrees) so pieces clear the doorway, or the effective capacity drops below 8.

## Spectator Hook
The final 30 seconds: five amber car lamps lit along a visibly loaded train, a last mailbag relayed from robot to robot through midfield traffic to the high hook, and then three robots reaching for the free-swinging Brakeman's Bars at once, swinging above their own train as the departure whistle sounds and the crowd counts the hangs.
