# Judging Report: Buildability

> This is a design-phase document kept for reference. The current game is defined by `01-design/DESIGN-SPEC.md` and the Game Manual (`02-manual/GAME-MANUAL.md`).

## Scores
| Concept | Watch | Interact | Floor/Ceil | Strategy | Auto | Endgame | Build | Teach | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| FIRST ASCENT | 8 | 8 | 9 | 8 | 8 | 7 | 8 | 8 | 64 |
| SUMMIT SIGNAL | 9 | 7 | 8 | 8 | 7 | 7 | 9 | 8 | 63 |
| HIGHBALL | 8 | 7 | 8 | 8 | 7 | 8 | 6 | 8 | 60 |
| MAINLINE | 8 | 7 | 7 | 8 | 7 | 7 | 7 | 8 | 59 |
| RELIQUARY | 7 | 6 | 7 | 7 | 7 | 7 | 7 | 8 | 56 |

## Ranking
1. FIRST ASCENT
2. SUMMIT SIGNAL
3. HIGHBALL
4. MAINLINE
5. RELIQUARY

## Verdict
Greenlight FIRST ASCENT, with SUMMIT SIGNAL a close second that merits one revision cycle.

FIRST ASCENT wins on the criteria this judge weighs most heavily. Its scoring definitions are simple latch-and-settle rules that six volunteers can call. Scoring only on the alliance's own structure removes every pollution and denial exploit by design. Its field breaks down into the cheapest element set and the easiest to CAD, with round dimensions and standard angles throughout, so student teams can realistically both CAD a robot against it and build practice elements in 9 days. Its fixes are a matter of tuning (protection apron, socket tolerance, RP thresholds) rather than redesign.

SUMMIT SIGNAL has the best buildability and the best spectator moment of the set, but it has a real rules hole. Capping an opponent's bare post with a Flare permanently kills that beacon for a gift of ~15 points, which is positive math in elims. The one-sentence completion-gate fix must close it before the game can be trusted.

HIGHBALL has the best-drafted rulebook, but its ten-car field build and relay refereeing on the scale of the 2014 assists make it the wrong scope for this event. MAINLINE's continuous accrual scoring and its knock-off causation fouls fail the volunteer-referee test as written. RELIQUARY puts six robots on one structure and relies on a protection rule based on judged distance, which makes it the design most likely to produce contact disputes of the five.

## Details
### FIRST ASCENT
- Strengths: The cleanest rules package of the five. Scoring only on the alliance's own crag, with no descoring, removes junk-feeding and pollution exploits outright. 'Scored = supported + no alliance robot contact, latched at settle' can be called by 6 volunteer referees with no possession tracking, no ownership timers and no attribution of causation. Camp bonuses latch, so disputes about mid-match state do not arise. It has the best-documented low floor in the set (a published kitbot path with an upgrade ladder). The field breaks down best: one crag = 2 sheets, headwall = 1 sheet + A-frames, all angles 15/30/45, all heights on round inches. The pieces are durable on the dog-toy model and can be sourced at hardware stores (PVC + pipe insulation, rubber rings, Power Up cubes). The Forecast mechanic ties one game-data read to both the auto doubling and the match-long Storm Tier.
- Concerns: The endgame is heavier than claimed. A max alliance climb of 90 against typical supply scores of 100-160 is ~40-45% of a strong match, more than the stated minority share, and an ASCENT RP of 40 at regionals means two real extending climbers, above the 'two robots mid-tier' calibration if the Camp rung (54 in, swinging) proves hard. The intentional absence of crag-face protection, combined with 78-in ring hangs under legal defense, gives the concept its highest exposure to tip-overs and contact disputes; a robot bumped mid-placement at full extension is a likely yellow-card argument. The O2 socket tolerance (0.75 in/side) will decide s-neff compliance and is unvalidated. The Depot rule ('ANY piece, any orientation, 4-in lip') needs a definition for overflow outside the tray (pieces heaped above the lip, pieces bridging the lip).
- Fixes:
  1. Add line-based placement protection: no opponent contact while a robot's bumpers intersect a taped 3-ft apron on any crag face. Referees can make this line call, unlike judged-distance rules, and the corridor and Center Cache stay fully open for defense.
  2. Drop the regional ASCENT RP threshold to 32 (Camp + Ledge) until week-1 data is available.
  3. Freeze the socket ID only after a kitbot-grade arm reaches 80%+ insertion in testing; publish the socket as a strictly toleranced dimension.
  4. Define Depot scoring as 'fully below the plane of the lip' and give field staff a leveling rule.
  5. Publish the dice/card Forecast fallback in the manual itself.

### SUMMIT SIGNAL
- Strengths: The best buildability of the set: trimmed traffic cones, pool-noodle rings, Sonotube spools and PVC posts with chamfered couplers, for a full practice field in 8 sheets with no exotic parts, and the easiest field for a student team to CAD in 9 days. Beacon ignition is the strongest single spectator moment across all five concepts, and the referee fallback definition ('Flare seated above at least one Ring and one Cell,' visible from the stands) is the right way to word a score backed by a sensor. 'Any piece on a post scores for that post's alliance' is good anti-pollution wording. The ring-toss post geometry (6-in bore over a 1.9-in chamfered post) is forgiving at the floor.
- Concerns: The Flare-cap denial exploit is a real rules hole. Because posts take max 4 pieces with 'Flare always last' and removal is a tech foul, an opponent can seat a cheap Flare on your bare post, giving you ~5-7 points while permanently killing that post's beacon. At ~15 points spent to deny the Network RP (4 beacons at regionals), the trade is strongly positive in elims and turns the signature mechanic into a denial game. Second, 'regardless of who placed it' with no launch restriction invites lobbing onto Low posts and hooks; the risks section admits this but does not resolve it. Summit posts 48 in apart are the closest robot-to-robot proximity of any concept, and the protected-contact wording does not exist yet. Flare capping at 76-82 in with a 3-in socket over a 1.9-in post (~0.55-in radial clearance) is tighter than it reads and sets the precision ceiling for the whole Network RP. Cell foam durability under 82-in drops is unproven.
- Fixes:
  1. Close the cap exploit with one sentence: 'A Flare is only scored when the post below it holds at least one Ring and one Cell; otherwise it is returned by field staff at the next stoppage and does not lock the post.' Capping then becomes strictly an act of completion.
  2. Add a launch rule: a piece must leave robot contact with the robot's bumpers within 3 ft of the target tower base (a line call).
  3. Enlarge the Flare socket to 4 in or add an internal guide cone; validate at 82 in with a prototype before the freeze.
  4. Write the Summit protected-contact rule now: no contact with an opponent whose bumpers intersect its own taped Summit approach box.
  5. Drop-test Cells from 84 in for x500 cycles before the piece spec is frozen.

### HIGHBALL
- Strengths: The most complete drafting of scoring definitions of the five: settle timing (3 s), out-of-bounds return, descored pieces counting as scored, and the observation that junk-feeding the opponent's train is self-defeating are all handled in the text. The 3/8/15 swinging-bar endgame, with full credit to the victim as protection, is the best endgame design here: partial credit everywhere, a real test of mastery and a clear foul. FULL CAR marker lamps and clear car walls make the match legible from the stands. The kitbot path (zero-lip ramp, 8-in deck, footboard) is honest about difficulty.
- Concerns: The field build is the heaviest by a wide margin: ten distinct car structures (5 cars x 2 trains, each with different geometry), two gantries, two depots and two grade crossings. For a 9-day CADathon that is 2-3x the element CAD of any other concept, and at real events it is the most expensive field and the slowest to reset. Refereeing is the second problem. Mail Relay possession tracking is a workload like the 2014 assists, which referees disliked even with 3 balls, and 12 bags is worse. Capacity counts for each of 10 cars, verification of manifest order in a 15-second auto, and lamp triggering also fall on volunteers. The 48-in gantry station spacing with a free-swinging 72-in bar is a robot-to-robot contact risk that the concept admits but does not resolve. The mailbag handle is a single point of durability failure with no replacement rule yet. Far-side scoring punishes teams with weak vision hard despite the mitigations.
- Fixes:
  1. Cut the train to 3 cars (merge the Caboose ramp and Flatcar deck into one 'Freight Car'; turn Stock/Tank/Mail into one combined mid car and one tall car). This halves field CAD, reset time and referee counting, with minimal strategic loss.
  2. Replace judged Mail Relay possession with a taped TRANSFER ZONE: a mailbag counts as relayed only if it is handed off while both robots' bumpers are in the zone. This turns a possession judgment into a line call.
  3. Widen the gantry stations to 60 in before any field testing.
  4. Add the 5-deg stock-car settling floor and the torn-handle replacement rule to the base spec now.
  5. Let the FMS score manifest order from scorekeeper entry, and make the car lamps sensor-driven (piece-count microswitch), never toggled by volunteers.

### MAINLINE
- Strengths: The physical display of score state (headlamp, semaphore paddles, lever clack) is the best legibility engineering of the five; the field itself is the scoreboard, and the lever flip is a memorable endgame act. The ownership economy with capacity locking is the deepest strategy layer in the set. The back-to-back face geometry on shared structures is the right way to create contested space without intake-vs-intake contact. Team-version buildability is strong (15-deg shelves from a wedge rip, pipe-flange hooks, a ~$250 field).
- Concerns: The game fails the six-volunteer test as written. Continuous per-second ownership accrual requires every placement's Signal Weight to be entered in real time with timestamps accurate to the second. A late scorer entry silently changes the score, and under 'strictly greater weight' single-piece events can flip ownership, which invites protests. Knock-off attribution ('owner-caused = returned, opponent-caused = G-foul + restoration') is a larger problem: it asks referees to assign causation for pieces falling off a contested centerline structure during a scrum, which cannot be enforced consistently. The 4.5-ft chokepoint lanes concentrate the pin and contact calls that the concept itself admits are risky. Additive-only counterplay plus face locking can end the territory contest mid-match (admitted, unresolved). The drum on a tilted shelf is a looks-easy-is-hard trap for mid-tier teams. The field electronics (headlamp, strobes, mast lamps) are the largest field-reliability exposure of any concept.
- Fixes:
  1. Replace continuous accrual with discrete OWNERSHIP CHECKS: every 15 s (and at T=0 of teleop and of the endgame), the alliance with greater weight on each structure banks a fixed bonus (e.g., Tower 12, Depot 6). Scorekeepers verify the state at known instants instead of streaming timestamps, and the paddles still show the story.
  2. Make all knock-offs no-fault: field staff restore any piece that leaves a structure. Delete the causation foul, and cover deliberate descoring with the existing tech-foul rule for robot contact with scored pieces.
  3. Widen the chokepoint lanes to 6 ft.
  4. Add a T-60 'second shelf row' unlock on locked depot faces to revive dead territory.
  5. Declare in the manual that the mechanical semaphore paddle is the sole authority and the lamps are decorative.

### RELIQUARY
- Strengths: The team-version breakdown to one face (1.5 sheets + $60 for a full practice face) is the best practice-field idea in any of the five concepts, and piece sourcing is excellent (hole-saw EVA medallions, planter-pot urns, XPS tablets under $4). The coin columns act as center-field thermometers and are strong for legibility. The Curator's Bonus is a clean way to force auto coordination. Partial credit for a tipped urn is a thoughtful guard against frustration.
- Concerns: The field geometry concentrates all six robots on one central structure from six directions, the worst traffic architecture of the set. The mitigation is a 12-in Curation Zone proximity rule, a continuous distance judgment that referees must make simultaneously on up to six faces; this restates the G415 problem without solving it. Floor pedestal urns (1-in lip, 18 in off a contested face, upright = within 15 deg of vertical) will be tipped constantly by incidental contact, forcing referees to decide who tipped them, the same causation trap as MAINLINE. The vault gravity column is a jam-prone field element with unlimited capacity, and a jam stops scoring on the signature low-floor task. Center congestion also hurts watchability, because the structure hides half its own faces from any seat. The risk of urns going unused in quals is admitted. The endgame is a competent but generic rung ladder, the least distinctive of the five.
- Fixes:
  1. Replace the 12-in judged zone with a painted hex APRON 30 in out from every face: opponent contact with any robot whose bumpers break the apron plane is the foul, which is a line call.
  2. Make urn tipping no-fault: field staff reset any urn that leaves the upright state on a pedestal at the next stoppage, with the score latching only at settle windows; deepen the pedestal lip to 2 in.
  3. Give the vault a clearing door that referees can reach, and cap vault capacity at 12 with an overflow tray for a full column, so a jam never stops scoring.
  4. Move the two floor pedestals from face A to standalone pedestals 4 ft off the rotunda, out of the scrum at the faces.
  5. Set the regional Masterpiece RP at 1 face + 8 vault coins, escalating later, as the concept's own risk note suggests.
