# Judging Report: Educator

> Design-phase archive. This document was written before the design specification (`01-design/DESIGN-SPEC.md`), which supersedes the geometry and scoring it describes. The current game is defined by that specification and the Game Manual (`02-manual/GAME-MANUAL.md`).

## Scores
| Concept | Watch | Interact | Floor/Ceil | Strategy | Auto | Endgame | Build | Teach | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| FIRST ASCENT | 8 | 7 | 9 | 8 | 8 | 9 | 9 | 9 | 67 |
| HIGHBALL | 8 | 8 | 7 | 9 | 9 | 9 | 7 | 9 | 66 |
| MAINLINE | 7 | 9 | 7 | 9 | 8 | 8 | 9 | 8 | 65 |
| SUMMIT SIGNAL | 9 | 7 | 7 | 8 | 8 | 8 | 8 | 7 | 62 |
| RELIQUARY | 7 | 7 | 8 | 8 | 8 | 7 | 8 | 8 | 61 |

## Ranking
1. FIRST ASCENT
2. HIGHBALL
3. MAINLINE
4. SUMMIT SIGNAL
5. RELIQUARY

## Verdict
Greenlight FIRST ASCENT. It is the only concept with a documented kitbot path and a real upgrade ladder. Its s-neff discipline is complete: every easy task looks easy, and the Summit looks as hard as it is. The Forecast keeps the meta rotating all season, and its field is among the cheapest and cleanest to reproduce. It is the safest choice for keeping mid-tier students engaged for a full CADathon while still separating elite archetypes.

HIGHBALL is a close second and probably the richer pure design exercise (the floppy mailbag handle and the relay handoff are the most novel mechanism problems in the field). However, its sightline problem with the far-side train penalizes the rookies its floor claims to serve, and the relay refereeing and the five-car field build add risk that a mentor-run offseason event does not need. If possible, bring its negotiated starting-line auto and its 3/8/15 swinging-bar endgame into FIRST ASCENT.

MAINLINE has the best interaction model but stakes the whole game on accrual tuning, a single-point-of-failure balance problem that no CADathon has the playtest capacity to solve. SUMMIT SIGNAL has the best hook but the narrowest mechanism debate (everything is a vertical drop-on), and RELIQUARY's traffic, with six faces on one structure, is likely to attract fouls. If FIRST ASCENT goes ahead, carry out fixes 1 and 2 (socket tolerance prototype, softening the Expedition RP lockout) before publishing the manual.

## Details
### FIRST ASCENT
- Strengths: The most honest floor of the five. A PUBLISHED kitbot path (crates only, depot + 24-in shelf) with an explicit upgrade ladder (add wrist -> sockets, add elevator -> mid tier, add hooks -> Ledge) is how to keep mid-tier students engaged instead of demoralized. Strict s-neff discipline everywhere: whole-inch dimensions, only 15/30/45-deg angles, easy tasks that look easy, and a Summit that looks as hard as it is. The Forecast rotates the doubled Storm Tier so the meta never freezes. Camp bonuses make mixed alliances worth more than a monoculture by design (the answer to 2015). The 15-deg inclined, laterally staggered Headwall is the freshest climb geometry in the field: a real traversal with a no-cliff 3/12/20/30 ladder in front of the crowd. Buildability is excellent (crag <$180, a single-lane headwall, angles set with a single speed square). For a CADathon, the geometry leaves the elevator-versus-arm decision open (flat shelves vs 30-deg sockets vs 45-deg pegs vs the 78-in ceiling), which produces real student debates with numbers.
- Concerns: Interaction is the weakest axis. Scoring is on the alliance's own crag only, so all cross-alliance play is defense and the contested Center Cache, with less counterplay than MAINLINE's territory war. The Expedition RP can be mathematically locked out by qualification-schedule luck if you draw no O2 or ring partner. The Summit traversal may see <10% success in weeks 1-2. The O2 socket tolerance (0.75 in/side) is one field-build variance away from an s-neff violation. The Forecast needs a fallback without the FMS for offseason play.
- Fixes:
  1. Prototype the socket ID and the 12-in rung stagger BEFORE freezing dimensions; publish the socket ID as a strictly toleranced field dimension with a +/- callout.
  2. Soften the Expedition lockout: let a Depot piece of the right type satisfy the Camp I slot for that type, or add a lower alternative, 'Camp I via any 3 pieces on the low band', at Regionals only.
  3. Publish the offseason Forecast fallback now (card draw + manual LED) so autos on practice fields do not degrade to scripts.
  4. Add a contact rule limited to bumper height within 3 ft of crag faces, to discourage targeting high-CG robots at the 78-in pegs for tip-overs.
  5. Give the defender role an incentive, e.g. a small neutral respawn at the Center Cache that matters for denial, so the debate over the third robot has a real defensive option.

### HIGHBALL
- Strengths: The richest design-tradeoff space of the five for a CADathon. A rigid cube, a rolling barrel and a floppy handled bag make an intake problem for three geometries that nobody solves at 115 lb; presenting the mailbag handle to a 15-deg peg is a new end-effector problem; and the Mail Relay creates real passing plays (drive practice like a sports team, beyond cycling). It has the best auto of the field: negotiating starting lines in the queue, 6-way manifest branching and placement that requires vision are three linked decisions. The 3/8/15 free-swinging Brakeman's Bar, with damping as the test of mastery, is textbook 2022-traversal design. The lamp-count legibility is excellent, and having the FULL CONSIST RP consume the same scoring actions (only aimed) is sophisticated RP design.
- Concerns: The far-side train is the game's structural flaw. Every scoring action, including the 'easy' caboose push, happens 45+ ft from your own glass through crossing traffic. The task is easy but the context is not, which is a partial s-neff violation for rookies with weak vision that the authors only half mitigate. Mail Relay possession tracking will attract protests unless the wording is airtight. The 16-ft five-car train is the largest field build here (~$600). The mailbag handle is the most abused feature and needs a torn-handle rule. Six autos crossing midfield are an unsimulated collision risk.
- Fixes:
  1. Give each alliance one near-side low-tier outlet (a small 'siding' or transfer platform on its own half, worth caboose-level points), so a rookie limited by sightlines has a close option all match.
  2. Replace judged relay possession with a mechanical definition: relay credit if the bag is exchanged robot to robot with both robots' bumpers inside a taped RELAY ZONE band at midfield (zone-based, binary, one referee).
  3. Widen the gantry stations to 54-60 in now, before the field drawings.
  4. Run the traffic simulation for six robots in auto and, if needed, stagger the trackside start boxes so opposing trackside robots face away from each other.
  5. Specify the mailbag handle to abuse standards informed by the Crescendo note (a bar-tack pull-test value in the manual), plus a replacement rule during matches.

### MAINLINE
- Strengths: The best cross-alliance interaction in the field. Territory ownership with additive-only counterplay makes every placement both offense and denial, and the back-to-back face geometry creates contested space without intake-vs-intake scrums. The kitbot floor matters strategically: a crate pushed into a ground bay carries Signal Weight, so the simplest robot on the field is fighting the territory war. Capacity locking creates real endgame calculations about territory, like bearing off in backgammon. It is the cheapest and simplest field build of the five (~$250, 6 sheets). The lever-clack moment is a strong signature.
- Concerns: The balance between accrual and placement is a single point of failure that the authors themselves name. If pts/sec runs even slightly high, one lantern robot decides matches, which is the Power Up problem again. Per-second drift is also less watchable than pieces landing, because the scoreboard moves without visible events; the paddles help but do not fully fix this. The 4.5-ft single-robot chokepoint lanes will generate pins and fouls that demoralize mid-tier drivers, and G-rules on 'contact while placing' at the depots will be very hard to referee. Additive-only locking creates depots that are mathematically dead mid-match. Two currencies (points plus Signal Weight) plus accrual are a heavy cognitive load for students deriving robot requirements.
- Fixes:
  1. Quantize accrual into discrete 5-second ticks shown as physical or LED pips on each structure, which makes it easier to tune, easier to watch and easier to defend against protests.
  2. Merge the two currencies: make Signal Weight equal the piece's point value so students track one number.
  3. Widen the chokepoint lanes to 6 ft (shrinking the depot width) and add an explicit no-pin zone within 3 ft of depot faces.
  4. Build the mid-match unlock into v1 instead of holding it as a contingency: a second shelf row (or +4 bay capacity) unlocks at T-60 so locked depots return to play for the endgame push.
  5. Run the playtest on lantern-robot dominance first (one elite lantern specialist against a balanced trio) and tune the 72-in lantern weight before anything else.

### SUMMIT SIGNAL
- Strengths: The best single spectator moment of all five concepts. Beacons physically lighting up the mountainside are instantly legible and a strong promotional hook, and stacked posts make the score state countable from the stands. 'Any piece on a post scores for that post's alliance' is a well-written rule that removes exploits. The First Light auto (nine paths, preload negotiation in the queue) and the Cell-scarcity economy, with beacon ordering as a skill to study, give real depth. Trimmed traffic cones make a very buildable game piece.
- Concerns: Mechanism monoculture is the teaching weakness. Nearly every scoring action is a vertical drop-on, so the elevator wins the elevator-versus-arm debate almost by default and the CADathon's tradeoff space narrows: three piece geometries, but essentially one approach vector. Flare capping at 76-82 in is the precision ceiling that holds up the entire Network RP. If the chamfer funnel is less forgiving than hoped, the game's signature mechanic fails and mid-tier teams are frustrated at height. The floor is thinner than claimed: the 40-in hook 'kitbot task' still needs a fixed arm, and there is no documented kitbot path. Ring lobbing onto low posts could erode the primacy of pick-and-place. Seat-sensor LEDs are a single point of failure in field reliability at the game's most important moment.
- Fixes:
  1. Vary the approach geometry: convert the Mid Tower to a side-load shelf or angled cradle so arms have a real use and the architecture debate reopens.
  2. Prototype the flare socket now. If capping success for a well-built mid-tier arm is under ~70%, enlarge the socket to 3.5-4 in and deepen the tip chamfer before the freeze.
  3. Write the launch-distance rule into v1 instead of waiting for a lobbing meta.
  4. Publish an explicit kitbot path document in the style of FIRST ASCENT (drivetrain + one fixed hook arm: depot, 38-in posts, signal hooks, shelter park).
  5. Make the fallback that referees can see the primary definition: by rule, a beacon = a flare seated over a ring and a cell, and the LEDs are decorative, so a dead sensor never affects the score.

### RELIQUARY
- Strengths: The vault slot is the best rookie task in any of the five concepts: floor level, orientation-free, an 8-in target that feeds the entry RP AND the Champs stretch RP, and as trivial as it looks. The urn is the most novel piece here (tip control, neck gripping, partial credit when tipped), a real CAD problem that no recent FRC game has posed. The coin-column thermometers are good for legibility, the team version built from one face is smart, and the Curator's Bonus auto for all three pieces forces the same healthy alliance negotiation as the best concepts.
- Concerns: Six scoring faces on one central structure make the riskiest traffic architecture in the field. All twelve robot-minutes of scoring converge on a 6-ft hexagon, and the 12-in Curation Zone will be the most protested rule at every event; this is the 2026 G415 trap that the concept claims to avoid. Per-face capacity is tight (1 pedestal, 1 plinth, 1 easel, 3/peg), so elite alliances may fill the high-value positions mid-match and the game declines into vault grinding plus the endgame. The endgame is the most generic of the five, a competent but anonymous 3-tier offset climb with no signature moment. Frustration with the urn could leave the piece largely unused in quals.
- Fixes:
  1. Grow the rotunda to 8 ft across flats, and base the protection rule on bumper geometry (no contact with a robot whose bumpers break a taped arc) instead of a 12-in judgment call.
  2. Raise per-face capacity (2 plinth positions and pegs 4 deep) so elite teams do not exhaust the scoring surface by T-60.
  3. Give the endgame an identity: add a small artifact-placement action at the top of the high rung (cap the scaffold with a medallion for +5) to tie the climb to the museum theme.
  4. Add a mid-value urn cradle at ~12 in, between the tipped partial credit and the pedestal, so mid-tier teams have an intermediate step for urns.
  5. Commit in advance to the Masterpiece fallback (1 face + 8 vault coins) as a published week-3 trigger condition.
