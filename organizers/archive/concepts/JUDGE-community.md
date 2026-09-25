# Judging Report: Community

> Design-phase archive. This document was written before the design specification (`01-design/DESIGN-SPEC.md`), which supersedes the geometry and scoring it describes. The current game is defined by that specification and the Game Manual (`02-manual/GAME-MANUAL.md`).

## Scores
| Concept | Watch | Interact | Floor/Ceil | Strategy | Auto | Endgame | Build | Teach | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| HIGHBALL | 8 | 7 | 8 | 7 | 7 | 8 | 6 | 8 | 59 |
| MAINLINE | 6 | 8 | 7 | 9 | 7 | 8 | 8 | 8 | 61 |
| RELIQUARY | 6 | 6 | 7 | 7 | 7 | 7 | 6 | 8 | 54 |
| FIRST ASCENT | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 64 |
| SUMMIT SIGNAL | 9 | 7 | 7 | 8 | 7 | 7 | 8 | 8 | 61 |

## Ranking
1. FIRST ASCENT
2. SUMMIT SIGNAL
3. MAINLINE
4. HIGHBALL
5. RELIQUARY

## Verdict
Greenlight FIRST ASCENT. It is the only concept with no catastrophic failure mode. Scoring is visible and latched; defense is legal but cannot blockade, because of the structure; the kitbot path is honest; and the endgame banks partial credit at every tier. Its worst problems (luck from the global Forecast, RP lockout by alliance draw) can be fixed with one-line rule changes instead of field rebuilds. During refinement, take SUMMIT SIGNAL's two best ideas: the visual language of beacon ignition (the Camp LEDs already half-implement it) and the anti-pollution rule that 'pieces score for the structure's owner regardless of who placed them'.

SUMMIT SIGNAL is the runner-up on the strength of its spectacle, but it stakes its identity on an unproven capping tolerance at 82 inches and a nine-path auto that nobody will run. MAINLINE has the deepest strategy in the set, but points-per-second accrual is the most consistently divisive mechanic in FRC history and would need a fundamental rework (discrete visible ticks) before it is safe. HIGHBALL is a strong design held back by relay refereeing in the style of the 2014 assists, 45-foot sightlines and the largest field build. RELIQUARY's single central structure hides its own scoring and funnels all traffic into a protected bubble that will attract fouls; it would top the least-favorite poll.

## Details
### HIGHBALL
- Strengths: The best score legibility of the set (amber FULL CAR lamps and clear stock and tank walls; the lamp count gives the score). The 3/8/15 endgame with the free-swinging Brakeman's Bar has the right difficulty curve: no Steamworks cliff, and the drama of a 2022 traversal. The caboose's zero-lip ramp is an honest kitbot job. Diagonal traffic that crosses gives Aerial Assist-style flow without forced collisions.
- Concerns: Far-side scoring is the hidden risk for the least-favorite poll. Your train is 45+ ft from your glass, and the 2019 complaints about far rockets suggest that teams with weak vision will dislike every match. MAIL RELAY revives the tracking of the 2014 assists; referees disliked it then, and the 'possession' wording will attract protests. Three piece geometries plus manifest branching plus relay choreography make the heaviest cognitive load of the five. The field build is the largest here: two 16-ft five-car trains, two gantries and grade crossings. Venues and offseason organizers will object, and the 'dead space' behind each train uses up floor area. The concept admits that the stock car door can jam, so its stated capacity is not reliable.
- Fixes:
  1. Cut the MAIL RELAY entirely, or convert it to a zone-based handoff (a bag scored within N seconds of leaving a taped transfer zone earns the bonus), so referees track location instead of possession.
  2. Move each train 8-10 ft closer to its own driver station, or allow a driver-side camera feed; AprilTags alone cannot fix the sightline problem for median teams.
  3. Reduce the manifest from 6 orderings to a 2-way branch (2018 showed that 2-3 branches is the right number).
  4. Slope the stock car floor and widen the door to 22 in before week zero.

### MAINLINE
- Strengths: The deepest strategy of the five. The Signal Weight ownership economy with capacity locking is new, the endgame math of the 'race to fill your face' is on the level of backgammon, and the MAINLINE RP (hold all three structures) is the best stretch RP in the set. The lever-clack finish to the climb is a strong photo moment. Because kitbot crates carry Signal Weight, the floor robot fights for ownership. It has the cheapest field build (~$250).
- Concerns: Points-per-second accrual is the most divisive mechanic in FRC history. The 2018 scale led half of CD to call it a chess match and the other half to call it unwatchable, and this concept has THREE accruing structures. A spectator can read the state (lamps, paddles) but cannot read the SCORE: knowing who is ahead and by how much requires integrating ownership time mentally, which is hidden scoring under another name. With additive-only counterplay, locked depot faces become mathematically dead mid-match, and the designers admit that the territory contest can collapse. The 4.5-ft chokepoints will generate pin fouls, and a refereeing burden like the 2026 G415 is built into the geometry. If the 1 pt/sec Tower rate is even slightly too high, one lantern robot decides every match and the freight game becomes irrelevant.
- Fixes:
  1. Convert accrual to discrete, visible ticks: award a fixed amount (e.g. 5 pts) for every 5 seconds of ownership, with an audible and visual pulse, so the audience sees points land.
  2. Add counterplay for locked faces that stops short of descoring, e.g. a once-per-match 'switching order' that reopens one row, so dead territory can revive.
  3. Widen the chokepoint lanes to 6 ft, and write the placement-protection rule with a clear line (bumpers within 6 in of a face = protected) before playtests.
  4. Playtest the pts/sec rate with an alliance built entirely around lanterns, and tune it until that alliance loses to a balanced one.

### RELIQUARY
- Strengths: The coin-column thermometers are a good legibility device. The vault slot is an honest floor task that feeds the top-tier RP, which is rare and well judged: the kitbot's coins matter at Champs. The scaffold ladder (3/8/14/22) is properly tiered. The Curator's Bonus forces real alliance coordination in auto. The team version built from a single hex face is well thought through.
- Concerns: A single central scoring structure is the game's fatal geometry. The tower physically hides half of its own faces from any given seat, so scoring happens behind the set piece, hidden by the architecture. Six faces on one structure funnel all twelve cycles per minute into one 6-ft hex, and the 12-in Curation Zone no-contact bubble around it will attract fouls in the way the 2026 G415 did, as the designers themselves note. The urn is a frustration piece like the 2023 cone: tippy and tapered, with an 'upright within 15 degrees' judgment call that referees will be arguing on camera all season. In practice it is the least interactive of the five: the curation bubble and the protected dig sites reduce legal defense to shadowing on the open floor. The face-completion bookkeeping of the Masterpiece RP is the most complex RP accounting in the set.
- Fixes:
  1. Split the rotunda into two mirrored half-structures offset from center (or push the alliance faces to opposite ends), so scoring is visible from the stands and traffic splits.
  2. Replace the 15-degree judgment of urn uprightness with a physical definition: base fully within the pedestal lip = scored, anything else = tipped, with no referee discretion.
  3. Shrink or delete the Curation Zone, and rely on the 5-second pin count plus generous face width.
  4. Drop the urn from the Collection RP path entirely (already partly done) and add a mid-value urn target at 12-18 in so mid-tier teams handle the piece.

### FIRST ASCENT
- Strengths: The most coherent package of the five, with no single catastrophic risk. Latched Camp bonuses with LED tier rings are both legible and permanent: the mountain visibly lights up, momentum is readable, and nothing un-scores. Four-face crag scoring defeats blockade defense through the structure while keeping defense fully legal, the best balance of interaction and defense in the set. The published kitbot path (crates only, Depot + 24-in shelf, park) is the most honest low floor here, with a real upgrade ladder. Camp completion mathematically requires mixed alliances, so a 2015-style monoculture is impossible by design. The Forecast is a clean 3-way branch (instead of 6 or 9), which is the right amount to ask of software. The 3/12/20/30 endgame on an inclined, staggered wall is a Rapid React traversal with better partial credit.
- Concerns: The Forecast's global doubling of one Storm Tier adds variance between matchups. An alliance drafted around high-tier robots gets a free +30 lane in GALE matches and a dead one in WHITEOUT matches, and over a qualification schedule teams will notice this luck. The Expedition RP can be mathematically out of reach with a bad alliance draw at small regionals (the designers admit it). Ring hangs at 78 in under legal defense are a tip-over and safety flashpoint; 2016 showed that a high CG combined with contact produces both injuries and angry forum threads. Two crags at midfield plus the center cache could still clog under a committed two-defender strategy in elims. It is also the least novel concept here: a competent remix of Rapid React geometry and Charged Up piece logic.
- Fixes:
  1. Make the Storm Tier specific to each alliance (draw each alliance's forecast independently, or let alliances CHOOSE their storm tier at match start as a declared gambit) to turn luck into strategy.
  2. Add a Depot-based path into the Expedition RP (e.g. Camp I satisfied by N depot pieces of each type) so no alliance is out of reach by draw.
  3. Impose a no-contact rule on a robot that has its mechanism extended above 60 in within 3 ft of its own crag face. This is narrow enough to preserve defense and wide enough to stop deliberate tip-overs.
  4. Playtest the two-defender choke of the center corridor with real drive teams before locking the crag spacing.

### SUMMIT SIGNAL
- Strengths: The best single spectator hook of the five: beacons physically IGNITE as Flares seat, and 'the winning alliance is the brighter half of the mountain'. That is the kind of moment that wins the favorite-game poll. 'Any piece on a post scores for that post's alliance' is the cleanest anti-pollution rule in the set, removing a whole class of exploit in one sentence, with a fallback for the sensor that referees can see from the stands. Beacon completion ORDER as the skill teams study (caps lock stacks) gives subtle, real depth. Ring-toss post scoring is forgiving in the right way for mid-tier teams. The field is buildable (PVC posts, trimmed traffic cones).
- Concerns: The nine-path First Light auto suite is over-engineered. 2018 data shows that most teams shipped 2-3 branches, and a +12 that requires three teams' preloads and code to line up will turn into 'nobody attempts it' by week 3, taking the auto's identity with it. Flare capping at 76-82 in is the precision ceiling on which the entire Network RP depends; if the chamfer funnel is one inch less forgiving than drawn, the signature mechanic fails and beacons never light at regionals. Seat-sensor LEDs are a single point of failure in field reliability for the game's emotional core. The admitted ring-lobbing meta at the low posts would erode the primacy of pick-and-place and needs a rule, and launch-restriction rules have historically been hard to referee. The endgame is competent but the least distinctive of the five, and the 2-pt park undervalues the floor.
- Fixes:
  1. Reduce First Light to one randomized tower with only the +2 per-piece bonus (drop the 3x3 preload choreography), and let the +12 trigger on lighting ANY beacon in auto.
  2. Prototype the Flare socket fit first: make the socket 4 in over a 1.9-in post with a full-cone chamfer, and validate it with a kitbot-grade gripper before anything else is frozen. If capping success is under 60% for a decent arm, lower the High and Summit tips by 6 in.
  3. Settle the lobbing question in advance with a clone of a 'momentum rule' (the piece must be in contact with the robot within 1 ft of the post) instead of a launch-distance judgment call.
  4. Raise the park to 3, and make the beacon LED redundant (sensor + a flag that referees can confirm).
