# 1 Introduction

## 1.1 About SUMMIT PUSH

SUMMIT PUSH is an original offseason game published as a design-training release for competitive robotics programs. This document is a complete, kickoff-quality game manual: it defines the game, the ARENA, the rules of play, robot construction requirements, and the tournament structure with the rigor a varsity robotics league applies to its season manual. SUMMIT PUSH is not played on a physical competition field, but every dimension, rule, and scoring value is written as though it were, because the design challenge is to develop robots against it as if it were a real season.

- **This manual is the authority.** Where any other document in the SUMMIT PUSH package (CAD packages, drawings, the vision guide) appears to conflict with this manual, this manual governs, with one exception: the locked design specification (`01-design/DESIGN-SPEC.md`) is the source document from which this manual was authored, and any discrepancy discovered between the two is reported to the event organizer and resolved in the specification's favor.
- **Defined terms matter.** Words in ALL CAPITAL LETTERS (e.g., CRAG, SCORED, MATCH) are defined terms with precise meanings, given at first use and collected in the Glossary. When a rule uses a defined term, the definition governs, not the everyday meaning of the word. Feature names that are not defined terms — Low Socket, Shelf 1, slot fence — appear in title case.
- **Rules are numbered and cited.** Game rules carry G numbers; robot construction rules carry R numbers. See Section 1.4 for the numbering scheme.
- **The game is played as written.** Referees, and in a design challenge the judges, enforce the text of the rules rather than presumed intent, which is why the text is written to be precise. An ambiguity is a question for the Q&A process, not an invitation to exploit (see Section 1.3).

## 1.2 Design Intent

SUMMIT PUSH is built around four deliberate commitments, stated here so that teams can read the rules in light of them.

**Three differently shaped GAME PIECES.** A cube, a cylinder, and a torus each force a distinct manipulation problem — compliant wide intake and flat placement; ground pickup of a rolling body plus reorientation and insertion; and precise hanging on an inclined peg. No single end effector handles all three well, so ALLIANCES must specialize and cooperate.

**Placement values are uniform by tier.** Every scoring position at a given altitude is worth the same, whatever the piece type. Height, not piece type, prices the task, so no piece is a second-class citizen and no archetype is a tax.

**Randomness shapes AUTO; strategy shapes the MATCH.** The FORECAST is random, applies only during AUTO, and is worth preparing for because ROPED UP requires two pieces of the PRIORITY SUPPLY — four of the five are pinned by type, and which type is doubled is not known until T = 0. The ROUTE DECLARATION is chosen before the MATCH and is public, so it can be scouted and countered. The three ROUTE uplifts are scaled by tier difficulty so that no declaration dominates: the correct choice depends on what an ALLIANCE can actually complete.

**An ENDGAME that adds without erasing.** HEADWALL climbs are worth enough to change a close MATCH and not enough to erase two minutes of cycling. Climbing is legal throughout the MATCH; only the contact protection is limited to the final thirty seconds and the climb assessment that follows it.

## 1.3 The MOUNTAIN ETHIC

Everyone who takes part in SUMMIT PUSH climbs under the MOUNTAIN ETHIC, this game's code of conduct. It has three parts.

**Respect for opponents and partners.** Teams play to win within the rules and their spirit, and do not hunt for wording loopholes to weaponize. On a real mountain, a rival expedition in trouble is still an expedition worth helping. Teams volunteer assistance to an ALLIANCE partner, or an opponent, whose ROBOT is down, and treat no one at the event as unimportant.

**Integrity toward referees.** Referees enforce the text of the rules under time pressure and without replay. Their calls are accepted with grace, including the close ones. Disagreements are raised through the question box and the Q&A process, not through argument at the FIELD.

**Safety first.** No point value in this manual is worth an injury. Where competitive advantage conflicts with the safety of people, ROBOTS, or the FIELD, safety wins without discussion.

SUMMIT PUSH includes defense, contested space, and high-stakes ENDGAME protection, all of which create moments of genuine competitive friction. The measure of a team is not whether friction occurs but how it behaves when it does. A team that wins a MATCH by exploiting an unintended reading of a rule, or by playing recklessly around a partner's climb, has lost more than the MATCH was worth.

> *Commentary:* SUMMIT PUSH is published as a design exercise, but the conduct rules are not simulated. In a design challenge the MOUNTAIN ETHIC governs how entrants treat competing entries, judges, and organizers.

## 1.4 Document Conventions

**Rule numbering.** Rules are grouped by number band:

| Band | Scope |
|---|---|
| **G1xx** | Personal safety |
| **G2xx** | Conduct |
| **G3xx** | Pre-MATCH (setup, starting configuration, ROUTE DECLARATION) |
| **G4xx** | In-MATCH robot rules (movement, contact, zones, ENDGAME) |
| **G5xx** | Game piece rules (possession, scoring, de-scoring) |
| **R1xx** | Robot size and weight |
| **R2xx** | Safety and materials |
| **R3xx** | Budget and fabrication |
| **R4xx** | Bumpers |
| **R5xx** | Motors and actuators |
| **R6xx** | Power distribution |
| **R7xx** | Control system |
| **R8xx** | Pneumatics |

**Violations.** Each rule that can be violated lists its consequence in a `Violation:` line. In-MATCH penalties use the taxonomy defined in Section 4.8; rules enforced at INSPECTION, and the few rules that forfeit a specific credit, state their consequence directly:

- **VERBAL WARNING** — no points; a recorded warning for a first-instance, low-impact infraction. Warnings persist for the team for the remainder of the event.
- **MINOR FOUL** — 3 points credited to the opposing ALLIANCE.
- **MAJOR FOUL** — 8 points credited to the opposing ALLIANCE.
- **YELLOW CARD** — a warning for egregious behavior or specific listed violations; a second YELLOW CARD in the same tournament phase escalates to a RED CARD.
- **RED CARD** — disqualification for the MATCH.

**Formatting.** Defined terms appear in ALL CAPS. Blockquotes beginning with *Example:* illustrate rule applications and are binding interpretations. Blockquotes beginning with *Commentary:* explain design intent and are not binding; the rule text always governs.

**Headers and cross-references.** Sections are numbered for citation (e.g., "per Section 4.3"). Rules are cited by number (e.g., "per **G405**").

## 1.5 Team Updates

The event organizer may issue Team Updates at any time during an event. Team Updates may correct errors, resolve ambiguities surfaced through the Q&A process, or, rarely, change rules or values. Each Team Update is numbered and dated; the most recent Team Update supersedes conflicting text in this manual and in prior updates. Teams are responsible for working against the manual as updated, and are expected to check for Team Updates before finalizing a design.

---

# 2 Game Overview

## 2.1 The Setting

Two expeditions have staged their gear at the foot of the same unclimbed peak. The weather service has issued a final bulletin: one clear window, two minutes and thirty seconds of it in the compressed time of the mountain, before the storm closes the mountain for the season. Whatever is carried up in that window is all either expedition will have.

At the horn, both expeditions move at once, up opposite flanks of the same mountain. Porters shuttle three kinds of SUPPLIES out of BASECAMP: CACHE CRATES of food and shelter, pressurized O2 CELLS, and ROPE COILS of climbing line. Each expedition stocks its own flank of the central rock spire, the CRAG: crates set onto ledges, oxygen cylinders seated into angled sockets, rope hung on protection pegs bolted up the face. As each CAMP is provisioned to the standard its altitude demands, its beacon ignites — a ring of light on the mountainside in expedition colors. Provision all three, from CAMP I through HIGH CAMP, and the SUMMIT BEACON at the top of the spire lights the whole peak.

Neither the mountain nor the sky treats the two expeditions equally. At the moment the window opens, the FORECAST arrives — whiteout, icefall, or gale — and dictates which SUPPLY matters most in the opening seconds. Before the push begins, each expedition has already committed to its ROUTE up the mountain: low, mid, or high. An expedition that provisions the CAMP on its declared ROUTE earns a larger bonus the higher it aims, and stakes its RANKING POINT on reaching that altitude.

As the storm wall appears on the horizon comes the moment every expedition trains for: the HEADWALL. SUPPLIES are stocked or they are not; now the climbers themselves go up, three abreast on a leaning face, hand over hand from the LEDGE RUNG to the CAMP RUNG to the SUMMIT RUNG, racing the buzzer. Every rung gained is banked.

## 2.2 The Match

SUMMIT PUSH is played by two ALLIANCES of three teams each on a 54 ft × 27 ft carpeted FIELD. Each MATCH is 2 minutes 30 seconds long: a 15-second AUTONOMOUS period (AUTO), in which ROBOTS operate only on pre-programmed instructions, followed immediately by a 2-minute-15-second TELEOPERATED period (TELEOP), in which DRIVE TEAMS take control. The final 30 seconds of TELEOP is the ENDGAME period, during which HEADWALL protection is active.

**The FIELD.** Each ALLIANCE owns one CRAG, a 48 in × 48 in structure rising to a spire top 90 in above the carpet near midfield, which is its sole placement structure for SUPPLIES. Between the two CRAGS lies the neutral CENTER CACHE: nine SUPPLIES staged on the centerline and contested by both ALLIANCES. Each ALLIANCE end holds the BASECAMP zone (where ROBOTS start), the HEADWALL (a 144-in-wide climbing truss leaned 15° from vertical, split into three independent lanes), and two OUTFITTER chutes in the wall corners where HUMAN PLAYERS feed additional SUPPLIES onto the FIELD.

**The SUPPLIES.** Three GAME PIECES, differently sized and shaped, each forcing a different manipulation problem:

| SUPPLY | Shape | Size | Scores on |
|---|---|---|---|
| **CACHE CRATE** | Cube | 12.0 in | Shelves (24 / 42 in) and BASE DEPOT |
| **O2 CELL** | Cylinder | 5.0 in dia × 14.0 in | Sockets (30 / 54 / 72 in) and BASE DEPOT |
| **ROPE COIL** | Torus | 10.0 in OD | 45° pegs (30 / 54 / 78 in) and BASE DEPOT |

ROBOTS may possess at most 2 SUPPLIES at a time. Every CRAG also has a floor-level BASE DEPOT tray that accepts any SUPPLY in any orientation; every ROBOT on the FIELD has a job.

**Placement values are uniform by tier.** Every scoring position at the Low tier is worth the same, every Mid-tier position is worth the same, and every High-tier position is worth the same, regardless of which SUPPLY it takes. Altitude prices the task.

**ROUTE DECLARATION.** During setup, each ALLIANCE declares its ROUTE: LOW ROUTE, MID ROUTE, or HIGH ROUTE (LOW by default if no declaration is made). The CAMP bonus matching the declared ROUTE pays its declared value for the entire MATCH (CAMP I +6→+18, CAMP II +10→+24, HIGH CAMP +15→+35). The declared ROUTE is shown on the FIELD LEDs at MATCH start, so scouting it is part of the game.

**The FORECAST.** At the instant AUTO begins, the Field Management System broadcasts one character of game data — `W` (WHITEOUT), `I` (ICEFALL), or `G` (GALE) — and the white FIELD LEDs display it. The FORECAST names the MATCH's PRIORITY SUPPLY (WHITEOUT = CACHE CRATES, ICEFALL = O2 CELLS, GALE = ROPE COILS), whose placement points are doubled during AUTO and of which ROPED UP requires two. ROBOTS must read game data and branch between at least three prepared autonomous routines. (An offseason fallback, a published card draw and manual LED, is specified in the Match Play section.)

**AUTO.** ROBOTS earn 3 points each for LEAVE (fully exiting BASECAMP), score staged and CENTER CACHE SUPPLIES at AUTO values with the PRIORITY SUPPLY doubled, and can bank the ROPED UP bonus: +10 if all three ROBOTS LEAVE and the ALLIANCE scores at least 5 SUPPLIES including at least two of the PRIORITY SUPPLY and at least one of each other type. AUTO scores are assessed after a 3-second settle window at the end of the period.

**TELEOP.** ALLIANCES cycle SUPPLIES from their OUTFITTER chutes, staged marks, and the contested CENTER CACHE to their CRAG. Establishing a CAMP (at least one of each required SUPPLY simultaneously SCORED at the corresponding tier) latches a bonus and ignites that tier's LED ring on the CRAG: CAMP I (+6), CAMP II (+10), HIGH CAMP (+15), each paying its declared value if it matches the declared ROUTE. Establishing all three ignites the SUMMIT BEACON for a latched +10. SUPPLIES SCORED on a CRAG score for that CRAG's ALLIANCE regardless of which ROBOT placed them, and no ROBOT may remove a SCORED SUPPLY from either CRAG. Defense is legal in the open field, but not against a ROBOT on its own CRAG APRON, in an opponent's OUTFITTER LANE, or against a ROBOT in its HEADWALL ZONE during the ENDGAME.

**ENDGAME.** Climbing the HEADWALL is legal at any time, but the final 30 seconds bring contact protection and the closing push. Each of the three lanes carries three rungs: LEDGE RUNG (30 in), CAMP RUNG (54 in), and SUMMIT RUNG (78 in), staggered 12 in laterally to alternating sides and set back 6.4 in per step by the 15° lean. One ROBOT per lane, and the climb must begin from the FIELD side of the truss. At the buzzer (with climbs assessed at rest, or at T+5 seconds), PARK in BASECAMP scores 3, hanging solely from the LEDGE RUNG scores 12, the CAMP RUNG 20, and the SUMMIT RUNG 30: a maximum ALLIANCE climb of 90.

## 2.3 MATCH AT A GLANCE

| Phase | Duration | Robots | What scores |
|---|---|---|---|
| **Setup** | pre-MATCH | Staged in BASECAMP; ≤1 preload each | ROUTE DECLARATION made (LOW default) |
| **AUTO** | 0:15 | Pre-programmed only; FORECAST broadcast at T=0 | LEAVE (3/robot); SUPPLIES at AUTO values (PRIORITY SUPPLY doubled); ROPED UP (+10); CAMP progress banks |
| **TELEOP** | 2:15 | Driver-controlled | SUPPLIES at TELEOP values; CAMP bonuses (declared ROUTE's CAMP uplifted); SUMMIT BEACON (+10); climbs legal any time |
| **ENDGAME** *(final 0:30 of TELEOP)* | 0:30 | HEADWALL ZONE protection active | PARK (3); LEDGE RUNG (12); CAMP RUNG (20); SUMMIT RUNG (30) |
| **Settle** | +0:03 (AUTO / final score); climbs at rest or +0:05 | ROBOTS disabled at the buzzer | Scores latch |

## 2.4 Scoring Quick Reference

**SUPPLY placement** (per SUPPLY; AUTO values apply to SUPPLIES whose last placing ROBOT contact occurred before the end of AUTO):

| Tier | Positions | Height | AUTO | TELEOP |
|---|---|---|---|---|
| **Low** | Shelf 1 (3 slots), Low Sockets (×2), Low Pegs (×2) | 24 / 30 / 30 in | **7** | **4** |
| **Mid** | Shelf 2 (3 slots), Mid Sockets (×2), Mid Pegs (×2) | 42 / 54 / 54 in | **10** | **7** |
| **High** | Summit Socket (×1), High Pegs (×2) | 72 / 78 in | **13** | **10** |
| **BASE DEPOT** | any SUPPLY, any orientation (~12) | floor (4 in lip) | **4** | **2** |

**Bonuses and ENDGAME:**

| Achievement | Requirement | Points |
|---|---|---|
| LEAVE (AUTO) | ROBOT fully exits BASECAMP during AUTO | **3** per ROBOT |
| FORECAST double (AUTO) | PRIORITY SUPPLY placements during AUTO | AUTO value **×2** |
| ROPED UP (AUTO) | All 3 ROBOTS LEAVE **and** ≥5 SUPPLIES SCORED incl. ≥2 PRIORITY SUPPLY and ≥1 of each other type | **+10** |
| CAMP I *(latched)* | ≥1 crate Shelf 1 + ≥1 Low-Socket O2 + ≥1 Low-Peg rope | **+6** *(+18 if LOW ROUTE)* |
| CAMP II *(latched)* | ≥1 crate Shelf 2 + ≥1 Mid-Socket O2 + ≥1 Mid-Peg rope | **+10** *(+24 if MID ROUTE)* |
| HIGH CAMP *(latched)* | Summit Socket filled + ≥1 High Peg | **+15** *(+35 if HIGH ROUTE)* |
| SUMMIT BEACON *(latched)* | All three CAMPS established | **+10** |
| PARK | ROBOT in BASECAMP at climb assessment | **3** |
| LEDGE RUNG | Supported solely by the LEDGE RUNG | **12** |
| CAMP RUNG | Supported solely by the CAMP RUNG | **20** |
| SUMMIT RUNG | Supported solely by the SUMMIT RUNG | **30** |

**Fouls:** MINOR FOUL = **+3** to the opposing ALLIANCE; MAJOR FOUL = **+8** to the opposing ALLIANCE.

**Ranking:** Win 3 RP, Tie 1 RP, plus three bonus RPs: SUPPLY LINE (total SUPPLIES SCORED, BASE DEPOT included), EXPEDITION (CAMPS established), and ASCENT (ALLIANCE ENDGAME points), detailed with tier thresholds in Section 4.7.

> *Example:* Late in a MATCH, Blue has declared MID ROUTE and completes CAMP II by hanging its first Mid-Peg ROPE COIL (7 points) while a crate already sits on Shelf 2 and an O2 CELL fills a Mid Socket. Blue scores 7 for the placement plus a latched +24 CAMP II bonus (uplifted from +10 by the ROUTE DECLARATION). Even if the ROPE COIL is later dislodged without robot contact, the CAMP II bonus remains — CAMP bonuses latch at the moment of completion — and FIELD STAFF restore the SUPPLY at the next safe opportunity.

> *Commentary:* The MATCH reads the way spectators watch it: SUPPLIES physically accumulate on the two spires, LED tier rings ignite as CAMPS are established, and a fully lit mountain is a winning mountain. The final 30 seconds, with six ROBOTS on two HEADWALLS and three per ALLIANCE climbing side by side, is the densest half minute of the MATCH, and a 30-point SUMMIT RUNG grab at the buzzer can flip a close MATCH without ever invalidating two minutes of cycling.
