# 8 Tournament

A SUMMIT PUSH event has three phases: Practice MATCHES, Qualification MATCHES, and Playoff MATCHES. Practice MATCHES do not count toward rankings. Qualification MATCHES determine each team's seeding, and Playoff MATCHES determine the event winner.

## 8.1 Qualification MATCHES

The Field Management System (FMS) assigns each team a schedule of Qualification MATCHES. In each Qualification MATCH, a team plays as part of a randomly assigned three-team ALLIANCE. ALLIANCE partners and opponents change from MATCH to MATCH.

Teams earn RANKING POINTS (RP) in each Qualification MATCH as follows:

**Table 8-1: Qualification RANKING POINTS**

| Achievement | RP |
|---|---|
| Win the MATCH | 3 |
| Tie the MATCH | 1 |
| Lose the MATCH | 0 |
| SUPPLY LINE RP: the ALLIANCE scores the threshold number of SUPPLIES (BASE DEPOT included) | 1 |
| EXPEDITION RP: the ALLIANCE establishes the threshold CAMP set | 1 |
| ASCENT RP: the ALLIANCE earns the threshold ENDGAME points | 1 |

A team can earn at most 6 RP in a single Qualification MATCH. Bonus RP thresholds escalate by event tier; the thresholds and the definition of full capacity are given in Section 4.7. Where this section and Section 4.7 differ, Section 4.7 governs.

Bonus RPs are awarded independently of the MATCH outcome, so a losing ALLIANCE can still earn all three. A team that is DISQUALIFIED in a Qualification MATCH receives 0 RP for that MATCH. A team that is BYPASSED (**G301**, **G305**) receives the RP its ALLIANCE earns, and the MATCH counts as played for RANKING SCORE purposes.

> *Commentary:* All three bonus RPs reward more of the core game: scoring SUPPLIES, establishing CAMPS, and climbing. None requires a separate task. A team's qualification strategy and its MATCH-winning strategy should therefore align and differ only at the margins, for example by feeding the BASE DEPOT late in a decided MATCH to secure the SUPPLY LINE RP.

## 8.2 RANKING SCORE and Tiebreakers

Teams are ranked by RANKING SCORE (RS): the average number of RANKING POINTS earned per Qualification MATCH played, excluding SURROGATE appearances. When the number of teams does not divide evenly into the MATCH schedule, the FMS assigns some teams one extra Qualification MATCH as a SURROGATE, published with the schedule. A SURROGATE appearance is played and scored normally for both ALLIANCES, but the surrogate team earns no RP from it, and the MATCH is excluded from both the numerator and the denominator of that team's RS.

The ranking order and its tiebreakers are given in Section 4.7. Where this section and Section 4.7 differ, Section 4.7 governs.

> *Example:* Two teams both finish qualifications with a RANKING SCORE of 3.40. Both have 1,012 cumulative MATCH points, so the second sort does not separate them. The first team's cumulative AUTO points (188) exceed the second's (171), so the first team seeds higher. The ENDGAME comparison and the random sort are never reached.

## 8.3 ALLIANCE Selection

At the end of Qualification MATCHES, the top eight (8) ranked teams become ALLIANCE Captains, seeded 1 through 8. ALLIANCE selection proceeds in two rounds using the standard serpentine draft:

- **Round 1:** Captains pick in seed order 1 → 8. Each Captain invites one eligible team, and the invited team may accept or decline. A team that declines an invitation remains eligible to be, or become, a Captain, but may not be invited again by any ALLIANCE. If a Captain invites a lower-seeded Captain and that Captain accepts, all lower-seeded Captains move up one seat and the next-highest ranked team is promoted to Captain.
- **Round 2:** Picks proceed in reverse seed order, 8 → 1.

Each ALLIANCE therefore consists of three teams. At the organizer's discretion, an event may hold a third round, in 1 → 8 order, in which each ALLIANCE selects one BACKUP ROBOT. A BACKUP ROBOT may substitute for one ROBOT of its ALLIANCE between Playoff MATCHES. The ALLIANCE Captain declares the substitution to the HEAD REFEREE before the "field ready" signal (**G305**). The substitution is permanent, and the replaced ROBOT may not play again for the remainder of the event. Like any ROBOT, a BACKUP ROBOT must have passed INSPECTION (**G301**).

## 8.4 Playoff MATCHES

Playoffs use an eight-ALLIANCE double-elimination bracket followed by a best-of-three Finals. An ALLIANCE is eliminated after its second loss. Bonus RPs are not awarded in Playoff MATCHES; only the MATCH outcome matters.

**Table 8-2: Playoff bracket**

| MATCH | Round | Red ALLIANCE | Blue ALLIANCE |
|---|---|---|---|
| Match 1 | Round 1 (Upper) | Alliance 1 | Alliance 8 |
| Match 2 | Round 1 (Upper) | Alliance 4 | Alliance 5 |
| Match 3 | Round 1 (Upper) | Alliance 2 | Alliance 7 |
| Match 4 | Round 1 (Upper) | Alliance 3 | Alliance 6 |
| Match 5 | Round 2 (Lower) | Loser of Match 1 | Loser of Match 2 |
| Match 6 | Round 2 (Lower) | Loser of Match 3 | Loser of Match 4 |
| Match 7 | Round 2 (Upper) | Winner of Match 1 | Winner of Match 2 |
| Match 8 | Round 2 (Upper) | Winner of Match 3 | Winner of Match 4 |
| Match 9 | Round 3 (Lower) | Loser of Match 7 | Winner of Match 6 |
| Match 10 | Round 3 (Lower) | Loser of Match 8 | Winner of Match 5 |
| Match 11 | Round 4 (Upper Final) | Winner of Match 7 | Winner of Match 8 |
| Match 12 | Round 4 (Lower) | Winner of Match 10 | Winner of Match 9 |
| Match 13 | Round 5 (Lower Final) | Loser of Match 11 | Winner of Match 12 |
| Finals | Best of 3 | Winner of Match 11 | Winner of Match 13 |

The winner of Match 11, undefeated in the upper bracket, advances directly to the Finals. The winner of Match 13 reaches the Finals with one loss. The Finals are best-of-three: the first ALLIANCE to win two Finals MATCHES is the event winner. The double-elimination rule does not carry into the Finals; Finals MATCH wins are counted on their own, regardless of earlier bracket record.

If a Playoff MATCH ends in a tie, the MATCH is replayed.

> *Commentary:* Because a single Playoff loss does not end an ALLIANCE's event, DRIVE TEAMS should plan for up to two MATCHES in quick succession in the lower bracket. Battery logistics, climb-mechanism checks between MATCHES, and a rehearsed plan for playing a ROBOT short are part of a complete playoff strategy, and they belong in a complete technical binder (see §8.5).

## 8.5 Applying the Tournament Structure to a Design Challenge

SUMMIT PUSH is published as an offseason design release, and no physical tournament is played. The tournament structure above still governs the design problem:

- **Entries are judged against the Championship column.** Where bonus RP thresholds escalate by tier, a judging rubric evaluates a design's credible performance against the Championship column of the Section 4.7 table. A design that can reach only the Regional thresholds is judged as a Regional-level design.
- **Strategy sections of technical binders should model both phases.** A complete binder presents a qualification model and an elimination model. The qualification model gives expected RP per MATCH with a random partner draw, including which bonus RPs the design can secure alone and which need help. The elimination model gives cycle counts, CAMP arithmetic, and ENDGAME contribution alongside two strong partners, where bonus RPs do not apply and MATCH points alone decide.
- **Entries should state their ALLIANCE ROLE.** Designs should state which ALLIANCE ROLE they fill (CRATE FREIGHTER, O2 SURGEON, RING ALPINIST, or HYBRID; see Section 4.10) and how that role would be valued in the serpentine draft described in Section 8.3.

## 8.6 ARENA Faults, Stoppages, Timeouts, and Replays

**ARENA FAULT.** An ARENA FAULT is any failure of the FIELD, the FMS, the FIELD network, the scoring system, or FIELD-provided equipment that affects the play or the scoring of a MATCH. A ROBOT failure, a ROBOT battery failure, a driver-station computer failure, and an OPERATOR CONSOLE failure are not ARENA FAULTS.

**Stopping a MATCH.** The HEAD REFEREE may stop a MATCH at any time for safety, for an ARENA FAULT, or to clear a hazard. When a MATCH is stopped, the FMS disables all ROBOTS and the MATCH clock halts. FIELD STAFF may then restore SUPPLIES per **G504**, clear hazards, or repair the FIELD. A ROBOT supported off the carpet by its own HEADWALL at the moment of a stoppage is recorded in that state by the HEAD REFEREE and is credited that rung's value at climb assessment, whether or not it holds position once disabled. A stopped MATCH resumes from the stop point if the FMS supports it. Otherwise, it is replayed in full only if the Replays paragraph below permits a replay, and is scored as played if it does not.

**Replays.** A Qualification or Playoff MATCH is replayed only when an ARENA FAULT affected the MATCH outcome. Teams may not request a replay for a ROBOT failure of any kind. A Playoff MATCH that ends in a tie is replayed (Section 8.4). A replayed MATCH is scored from scratch, and the original MATCH is discarded.

**Timeouts.** Each ALLIANCE is entitled to one 6-minute TIMEOUT for the Playoff bracket, plus one additional TIMEOUT for the Finals. The ALLIANCE Captain requests a TIMEOUT from the HEAD REFEREE before the "field ready" signal for the MATCH the TIMEOUT precedes. TIMEOUTS are not available in Practice or Qualification MATCHES. FIELD reset and MATCH queuing continue during a TIMEOUT.

**DISABLED and removed ROBOTS.** A ROBOT that is DISABLED (**G411**, or at the HEAD REFEREE's discretion for a safety condition) may not be operated for the remainder of the MATCH, and remains on the FIELD until the MATCH ends unless FIELD STAFF determine that it must be removed for safety. A ROBOT removed from the FIELD during a MATCH earns no ENDGAME points.

---

# 9 Glossary

Defined terms appear in ALL CAPS throughout this manual. Where a definition below summarizes a rule, the rule text governs. Feature names that are not defined terms (Low Socket, Mid Socket, Summit Socket, Low Peg, Mid Peg, High Peg, Shelf 1, Shelf 2, slot fence) appear in title case.

**Table 9-1: Defined terms**

| Term | Definition |
|---|---|
| **ALLIANCE** | A group of three (3) teams that play a MATCH together as Red or Blue. |
| **ALLIANCE ROLE** | One of the four recurring ROBOT archetypes described in Section 4.10: CRATE FREIGHTER, O2 SURGEON, RING ALPINIST, or HYBRID. ALLIANCE ROLES are descriptive and impose no rules. |
| **APRON** (CRAG APRON) | A taped band extending 36 in out from a CRAG's SHELF FACE and PEG FACE and 20 in out from each SOCKET FACE, with 20-in-radius corner arcs. An opponent may not contact a ROBOT whose BUMPERS intersect its own ALLIANCE's APRON, unless that ROBOT initiated the contact (**G407**). |
| **ARENA** | All elements of the game infrastructure required to play SUMMIT PUSH: the FIELD, the CRAGS, the HEADWALLS, SUPPLIES, and all supporting hardware and control equipment. |
| **ARENA FAULT** | A failure of the FIELD, FMS, FIELD network, scoring system, or FIELD-provided equipment that affects play or scoring. It is the only basis for replaying a Qualification MATCH, and the only basis other than a tie for replaying a Playoff MATCH (§8.6). |
| **ASCENT RP** | The bonus RANKING POINT awarded when an ALLIANCE's total ENDGAME points meet or exceed the tier threshold (Section 4.7). |
| **A-STOP** | The FIELD-provided driver-station button that ends a ROBOT's AUTO immediately. The ROBOT may be enabled normally at the start of TELEOP (§3.1). |
| **AUTO** | The first 0:15 of a MATCH, during which ROBOTS operate solely under pre-programmed control with no driver input. |
| **BACKUP ROBOT** | A ROBOT selected in an optional third round of ALLIANCE selection that may permanently substitute for one ROBOT of its ALLIANCE between Playoff MATCHES (§8.3). |
| **BASE DEPOT** (short form: **DEPOT**) | The floor tray with a 4-in lip and a 16-in-deep channel that runs along the SHELF FACE and wraps 16 in around both of that face's corners onto the SOCKET FACES. It accepts any SUPPLY in any orientation in a single layer (roughly 8 CACHE CRATES, or about 12 SUPPLIES mixed), and a SUPPLY counts only when the tray floor alone supports it, wholly inside the channel's vertical projection. |
| **BASECAMP** | The taped zone (48 in deep, 144 in wide) at each alliance wall beneath the HEADWALL, in which ROBOTS start the MATCH and may PARK during the ENDGAME. |
| **BUMPER** | The protective assembly of wood backing, foam, and cloth cover that surrounds a ROBOT's FRAME PERIMETER and defines its position for every line call in this manual (**R401**–**R405**). |
| **BUMPER ZONE** | The volume between 2.5 in and 5.75 in above the floor that a ROBOT's BUMPERS must completely fill (**R403**). |
| **BYPASSED** | The state of a team whose ROBOT takes no part in a MATCH: the ROBOT is placed on the FIELD powered off, or left out entirely, and is not operated for that MATCH (**G301**, **G305**). The ALLIANCE plays the MATCH one ROBOT short; RP and RANKING SCORE treatment is given in §8.1. |
| **CACHE CRATE** | The cube SUPPLY: 12.0 in per side, pillowed faces, ~2.0 lb, expedition violet. SCORED on Shelf 1, on Shelf 2, or in the BASE DEPOT. |
| **CAMP** | Any of the three latched bonus states on an ALLIANCE's CRAG: CAMP I, CAMP II, or HIGH CAMP. A CAMP is established at the moment its required SUPPLIES are simultaneously SCORED; the state latches and its LED tier ring lights. |
| **CAMP I** | The low-tier CAMP: ≥1 CACHE CRATE on Shelf 1, ≥1 O2 CELL in a Low Socket, and ≥1 ROPE COIL on a Low Peg, simultaneously SCORED (+6; +18 under a LOW ROUTE declaration). At Regional tier only, one missing piece-type slot may be satisfied by 4 BASE DEPOT SUPPLIES of that type. |
| **CAMP II** | The mid-tier CAMP: ≥1 CACHE CRATE on Shelf 2, ≥1 O2 CELL in a Mid Socket, and ≥1 ROPE COIL on a Mid Peg, simultaneously SCORED (+10; +24 under a MID ROUTE declaration). |
| **CAMP RUNG** | The middle HEADWALL rung, 54 in above the carpet. A ROBOT supported solely by it at climb assessment earns 20 points. |
| **CENTER CACHE** | The neutral band at midfield (X 300–348, Y 108–216) holding 9 staged SUPPLIES (3 of each type) at 9 taped marks, each type once per row and once per column. |
| **CLIMB LINE** | The vertical plane at X = 48 in (Blue) / X = 600 in (Red) that contains its HEADWALL's carpet line and spans the full width of the FIELD. A ROBOT may not contact a rung while any part of its BUMPERS is on the alliance-wall side of this plane unless it is at that moment supported solely by rungs, or is still touching a rung it took hold of while so supported within the preceding 5 seconds (**G416**). |
| **COMPONENT** | An individual piece of a ROBOT, in the state in which it is used, such as a fastener, a gear, or a motor. A MECHANISM is an assembly of COMPONENTS. |
| **CONTROL** | Equivalent term for POSSESSION (**G501**): a ROBOT is in CONTROL of a SUPPLY when carrying it, herding it in a deliberate direction, or trapping it against a FIELD element or ROBOT. Plowing a SUPPLY incidentally, deflecting it in a single bounce, or driving over it is not CONTROL. |
| **COTS** | A Commercial-Off-The-Shelf item: a standard, unmodified part or assembly commonly available from a VENDOR and available to all teams (**R301**). |
| **CRAG** | An ALLIANCE's 48 × 48 in scoring structure at midfield, rising to a spire top 90 in above the carpet and carrying the shelves, sockets, pegs, BASE DEPOT, LED tier rings, and SUMMIT BEACON. SUPPLIES SCORED on a CRAG count for that CRAG's ALLIANCE regardless of which ROBOT placed them. |
| **DCMP** | District Championship: the middle event tier of the escalating bonus-RP thresholds in Section 4.7. |
| **DISABLED** | The state of a ROBOT made inoperable for the remainder of the MATCH, for example for fully exiting the FIELD (**G411**) or at the HEAD REFEREE's discretion for a safety condition. A DISABLED ROBOT may not be operated until the MATCH ends. |
| **DISQUALIFIED** | The state of a team that receives a RED CARD in a MATCH. The team earns 0 RANKING POINTS in a Qualification MATCH; in Playoffs, its ALLIANCE loses the MATCH. |
| **DRIVE COACH** | The one DRIVE TEAM member designated to guide and coordinate the team's DRIVERS/OPERATORS during a MATCH. The DRIVE COACH may not contact the OPERATOR CONSOLE at any time during a MATCH. |
| **DRIVE TEAM** | A team's crew of up to five people for a MATCH: 1 DRIVE COACH and up to 4 DRIVERS/OPERATORS/HUMAN PLAYERS. An ALLIANCE fields two HUMAN PLAYERS in total, one per OUTFITTER station (**G307**). |
| **DRIVER/OPERATOR** | A DRIVE TEAM member who operates the ROBOT from the team's driver station during TELEOP. |
| **ELECTRIC SOLENOID ACTUATOR** | A COTS linear electric actuator of ≤1 in stroke and ≤10 W, legal under Table 6-2 and powered per **R505** and **R703**. |
| **ENDGAME** | The final 0:30 of TELEOP, during which HEADWALL ZONE protection is active; the protection continues through climb assessment. ENDGAME climb points are assessed after the final buzzer, with ROBOTS at rest or at T+5 s, whichever comes first. |
| **E-STOP** | The FIELD-provided driver-station button that renders a ROBOT inoperable for the remainder of the MATCH (§3.1). |
| **EXPEDITION RP** | The bonus RANKING POINT awarded for establishing the tier-threshold set of CAMPS, and at Championship tier for also filling the declared ROUTE's tier to full capacity (Section 4.7). |
| **FABRICATED ITEM** | Any COMPONENT or MECHANISM altered, built, cast, printed, or assembled by or for a team into its final form (**R302**). |
| **FIELD** | The 648 in × 324 in carpeted playing surface bounded by the guardrails and the two alliance walls, together with the FIELD elements standing on it. The FIELD is the part of the ARENA on which the MATCH is played. |
| **FIELD LEDs** | The two guardrail-mounted LED bands, each split at the centerline into two ALLIANCE segments, that display FIELD-safe (green), the FORECAST (white), and each ALLIANCE's declared ROUTE (§3.1.2). They are indicators only and are never the scoring or safety authority. |
| **FIELD STAFF** | The volunteers who set the FIELD, restore SUPPLIES per **G504**, signal "field ready," and control FIELD access. |
| **FINAL** | The state of a MATCH score once the HEAD REFEREE has approved it (§4.9). A FINAL score may not be changed. |
| **FMS** | The Field Management System: the electronics and software that run the MATCH, broadcast the FORECAST, track time, and record scores. |
| **FORECAST** | The random game data broadcast at T=0 of AUTO: `W` (WHITEOUT), `I` (ICEFALL), or `G` (GALE). It sets the PRIORITY SUPPLY, whose AUTO placement points are doubled and of which ROPED UP requires two, and it has no effect outside AUTO. |
| **FRAME PERIMETER** | The fixed, non-articulated polygon outlining a ROBOT's frame in its STARTING CONFIGURATION, measured by string wrap; maximum 120 in. |
| **GAME PIECE** | Synonymous with **SUPPLY**: the CACHE CRATE, the O2 CELL, or the ROPE COIL. A rule stated in either term applies equally to the other. |
| **HEAD REFEREE** | The referee with final authority over rule interpretation, penalties, MATCH stoppages, and score approval at an event. |
| **HEADWALL** | An ALLIANCE's 144-in-wide climbing truss, leaned 15° from vertical and divided into three independent 48-in lanes, each carrying a LEDGE RUNG, a CAMP RUNG, and a SUMMIT RUNG. One ROBOT per lane. |
| **HEADWALL ZONE** | The taped BASECAMP area beneath an ALLIANCE's HEADWALL. From the start of ENDGAME through climb assessment, an opponent that contacts a ROBOT in this zone, or a ROBOT supported by that HEADWALL, commits a MAJOR FOUL unless the protected ROBOT initiated the contact (**G412**). |
| **HIGH CAMP** | The high-tier CAMP: an O2 CELL in the Summit Socket and a ROPE COIL on at least one High Peg, simultaneously SCORED (+15; +35 under a HIGH ROUTE declaration). |
| **HUMAN PLAYER** | A DRIVE TEAM member assigned to one of the ALLIANCE's two OUTFITTER stations, who introduces SUPPLIES onto the FIELD only through the chute opening (**G506**). Each ALLIANCE fields exactly two, one per station, drawn from any of its three DRIVE TEAMS (**G307**). |
| **INSPECTION** | The pre-MATCH verification that a ROBOT complies with every R-rule in the configuration it will play (Section 7). |
| **LAST ROBOT CONTACT** | For a given SUPPLY, the most recent instant at which any ROBOT was in contact with it while placing or moving it into its scoring position; contact that neither places nor displaces a SCORED SUPPLY does not count. It determines whether a SUPPLY SCORED during the AUTO settle earns AUTO or TELEOP values (§4.1). |
| **LAUNCH** | To shoot, throw, kick, or otherwise propel a SUPPLY so that it travels through the air under impetus imparted by the ROBOT after release (**G502**). LAUNCHING is prohibited except into the ROBOT's own BASE DEPOT from the half of its own APRON on its SHELF FACE's side of the FIELD centerline; releasing a SUPPLY from rest, or pushing one at drive speed, is not LAUNCHING. |
| **LEAVE** | An AUTO task in which a ROBOT's BUMPERS fully exit the BASECAMP zone during AUTO (3 points per ROBOT). |
| **LEDGE RUNG** | The lowest HEADWALL rung, 30 in above the carpet. A ROBOT supported solely by it at climb assessment earns 12 points. |
| **MAJOR FOUL** | A penalty crediting the opposing ALLIANCE with 8 points. |
| **MATCH** | One 2:30 game of SUMMIT PUSH: 0:15 AUTO followed by 2:15 TELEOP, of which the final 0:30 is the ENDGAME. |
| **MECHANISM** | An assembly of COMPONENTS that performs a function on a ROBOT, such as an intake, an elevator, or a climber. |
| **MINOR FOUL** | A penalty crediting the opposing ALLIANCE with 3 points. |
| **MOUNTAIN ETHIC** | The code of conduct binding every participant (Section 1.3): respect for opponents and partners, integrity toward referees, and safety before points. |
| **O2 CELL** | The cylinder SUPPLY: 5.0 in diameter × 14.0 in long, domed caps, ~1.5 lb, off-white body with green caps. SCORED by insertion into a Low, Mid, or Summit Socket (socket ID 6.50 ± 0.125 in) or in the BASE DEPOT. |
| **OPERATOR CONSOLE** | The assembly of controls, computers, and wiring a DRIVE TEAM connects to the FMS at its driver station (**R707**). |
| **OUTFITTER** | One of an ALLIANCE's two HUMAN PLAYER feed stations: a wall chute 30 in wide × 16 in tall with a 24-in sill, located at the alliance wall corners. |
| **OUTFITTER LANE** | The taped no-defense zone, 36 in wide, extending 48 in into the FIELD from each OUTFITTER chute. Opposing ROBOTS may not enter it or contact ROBOTS in it (**G410**). |
| **PARK** | An ENDGAME state: a ROBOT whose BUMPERS are fully within its BASECAMP at climb assessment and that is not supported solely by a rung (3 points). Contact with HEADWALL structure other than a rung is permitted; rung contact from the carpet is governed by **G416**. |
| **PEG FACE** | The CRAG face that faces the opponent's alliance wall, carrying the Low and Mid Pegs. |
| **PINNED** | The state of a ROBOT that an opponent ROBOT prevents from moving while it is in contact with a FIELD element, a guardrail, or a ROBOT other than the pinning ROBOT (**G408**). Pinning is legal for up to 5 seconds; the count ends only when the pinning ROBOT releases and separates by at least 6 ft. |
| **PLANE P** | The inclined plane that contains every rung centerline of a HEADWALL: it passes through the horizontal line {X = 48 (Blue) / 600 (Red), Z = 0} spanning Y 90–234 and is tilted 15° from vertical with its top leaning toward the alliance wall, unlike the vertical CLIMB LINE. All truss structure except the rung end brackets sits at least 4.0 in behind it. |
| **POSSESSION** | See CONTROL. A ROBOT may POSSESS at most 2 SUPPLIES in any combination. |
| **PRIORITY SUPPLY** | The SUPPLY type designated by the FORECAST (WHITEOUT: CACHE CRATES; ICEFALL: O2 CELLS; GALE: ROPE COILS). Its AUTO placement points are doubled, and ROPED UP requires two of it. |
| **RANKING POINT (RP)** | The unit of qualification credit: 3 for a win, 1 for a tie, plus up to 3 bonus RPs (SUPPLY LINE, EXPEDITION, ASCENT), for a maximum of 6 per MATCH. |
| **RANKING SCORE (RS)** | A team's average RANKING POINTS per Qualification MATCH played, excluding SURROGATE appearances; the primary qualification ranking sort. |
| **RED CARD** | The penalty for egregious behavior or a second YELLOW CARD in the same tournament phase. The team is DISQUALIFIED for the MATCH. |
| **ROBOT** | The electromechanical assembly, including all BUMPERS and all attached COMPONENTS and MECHANISMS, that a team places on the FIELD to play a MATCH. |
| **ROBOT SIGNAL LIGHT (RSL)** | The amber indicator required by **R706** that shows whether a ROBOT is enabled. |
| **ROPE COIL** | The torus SUPPLY: 10.0 in OD, 2.5 in tube (5.0 in ID hole), ~1.0 lb, amber. SCORED by hanging on a Low, Mid, or High Peg (1.5 in OD, angled 45° upward) or in the BASE DEPOT. |
| **ROPED UP** | An AUTO bonus (+10) earned when all 3 ALLIANCE ROBOTS LEAVE and the ALLIANCE scores ≥5 SUPPLIES in AUTO, including ≥2 of the PRIORITY SUPPLY and ≥1 of each other type. |
| **ROUTE** | An ALLIANCE's pre-MATCH declaration of LOW ROUTE, MID ROUTE, or HIGH ROUTE (LOW by default), which raises the corresponding CAMP bonus to its declared value for the entire MATCH (CAMP I +6→+18, CAMP II +10→+24, HIGH CAMP +15→+35). The declared ROUTE is shown on the FIELD LEDs at MATCH start. |
| **SCORED** | The state of a SUPPLY that is at rest, supported by a scoring element alone, and not in contact with any ROBOT of the scoring ALLIANCE (§4.4.1). AUTO values apply to SUPPLIES whose last placing ROBOT contact occurred before the end of AUTO. |
| **SCORING ERROR** | A correctable mistake in the recorded score: a miscounted or misattributed SUPPLY, an unrecorded CAMP or SUMMIT BEACON latch, a mis-entered ENDGAME state, or a foul credited to the wrong ALLIANCE (§4.9). Referee judgment about whether a violation occurred is never a SCORING ERROR. |
| **SHELF FACE** | The CRAG face that faces the owning ALLIANCE's wall, carrying Shelf 1, Shelf 2, the Summit Socket, and the BASE DEPOT. |
| **SOCKET FACE** | Either of the two CRAG faces perpendicular to the FIELD centerline, each carrying one Low Socket and one Mid Socket. |
| **STARTING CONFIGURATION** | The ROBOT's pre-MATCH state: no more than 42 in tall and, apart from its BUMPERS, entirely within its FRAME PERIMETER (**R104**). |
| **SUMMIT BEACON** | The translucent lantern forming the top 12 in of each CRAG's spire (Z 78–90, luminous center 84 in). It lights when all three CAMPS are established and banks a latched +10. |
| **SUMMIT RUNG** | The highest HEADWALL rung, 78 in above the carpet. A ROBOT supported solely by it at climb assessment earns 30 points. |
| **SUPPLY** (pl. **SUPPLIES**) | The collective term for the three GAME PIECES: the CACHE CRATE, the O2 CELL, and the ROPE COIL. |
| **SUPPLY LINE RP** | The bonus RANKING POINT awarded when the ALLIANCE's total SCORED SUPPLIES (BASE DEPOT included) meet the tier threshold (Section 4.7). |
| **SURROGATE** | A team assigned one extra Qualification MATCH by the FMS to balance the schedule. The MATCH is played and scored normally, but the surrogate team earns no RP from it and the MATCH is excluded from that team's RANKING SCORE (§8.2). |
| **TELEOP** | The 2:15 driver-controlled period following AUTO; its final 0:30 is the ENDGAME. |
| **TIMEOUT** | A 6-minute break: one per ALLIANCE for the Playoff bracket, plus one more for the Finals (§8.6). |
| **VENDOR** | A source from which a COTS item is generally available to all teams at published pricing (**R301**, **R303**). |
| **VERBAL WARNING** | A no-points penalty for a first-instance, low-impact infraction. A VERBAL WARNING is recorded and persists for the team for the remainder of the event. |
| **YELLOW CARD** | A warning for unsafe or uncivil behavior, egregious rule violations, or the specific violations for which a rule lists one. A second YELLOW CARD in the same tournament phase escalates to a RED CARD. |

> *Commentary:* LED tier rings and the SUMMIT BEACON confirm latched CAMP states; they are never the scoring authority. If a lighting fault occurs, referees score CAMPS from the SUPPLY states at the moment of completion, per the definitions above.
