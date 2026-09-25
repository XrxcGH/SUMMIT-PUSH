# 1 Introduction

## 1.1 About SUMMIT PUSH

SUMMIT PUSH is an original offseason game, published as a design-training release for competitive robotics programs. This manual defines the game, the ARENA, the rules of play, the ROBOT construction rules, and the tournament structure. SUMMIT PUSH has no physical competition field. Every dimension, rule, and scoring value is nonetheless written for one, so that teams can design ROBOTS against it as they would for a competition season.

- **Authority.** Where any other document in the SUMMIT PUSH package (CAD packages, drawings, the vision guide) appears to conflict with this manual, this manual governs, with one exception. The design specification (`01-design/DESIGN-SPEC.md`) is the source document from which this manual was written; any discrepancy found between the two is reported to the event organizer and resolved in the specification's favor.
- **Defined terms.** Words in ALL CAPITAL LETTERS (e.g., CRAG, SCORED, MATCH) are defined terms. Each is collected, with its definition, in the Glossary (Section 9). When a rule uses a defined term, the definition governs over the everyday meaning of the word. Feature names that are not defined terms, such as Low Socket, Shelf 1, and slot fence, appear in title case.
- **Rule numbers.** Game rules carry G numbers and robot construction rules carry R numbers. Section 1.4 gives the numbering scheme.
- **Interpretation.** Referees, and in a design challenge the judges, enforce the rules as written. Teams raise ambiguities through the Q&A process rather than exploiting them (see Section 1.3).

## 1.2 Design Intent

The rules follow from four design decisions. They are stated here so that teams can read the rules in light of them.

**Three GAME PIECE shapes.** A cube, a cylinder, and a torus each pose a different manipulation problem. The CACHE CRATE needs a wide, compliant intake and flat placement. The O2 CELL needs ground pickup of a rolling body, reorientation, and insertion. The ROPE COIL needs precise hanging on an inclined peg. No single end effector handles all three well, so ALLIANCES specialize and cooperate.

**Uniform values by tier.** Every scoring position at a given height tier is worth the same, whatever the piece type. Placement value depends only on tier, so no piece type or ROBOT archetype is penalized.

**FORECAST and ROUTE DECLARATION.** The FORECAST is random and applies only during AUTO. It is worth preparing for because ROPED UP requires two of the PRIORITY SUPPLY: four of the five required SUPPLIES are fixed by type, and the doubled type is not known until T=0. The ROUTE DECLARATION is a strategic choice, made before the MATCH and public, so opponents can scout and counter it. The three ROUTE uplifts are scaled to tier difficulty so that no declaration is always best; the right choice depends on what the ALLIANCE can reliably complete.

**ENDGAME weighting.** HEADWALL climbs are worth enough to decide a close MATCH, but not enough to outweigh two minutes of cycling. Climbing is legal throughout the MATCH. Contact protection applies only during the final 30 seconds and the climb assessment that follows.

## 1.3 The MOUNTAIN ETHIC

Everyone taking part in SUMMIT PUSH is bound by the MOUNTAIN ETHIC, the game's code of conduct. It has three parts.

**Respect for opponents and partners.** Teams play to win within the rules and their spirit, and do not look for loopholes in the wording to use against other teams. Teams offer help to any ALLIANCE partner or opponent whose ROBOT is down, and treat everyone at the event with respect.

**Integrity toward referees.** Referees enforce the rules under time pressure and without video review. Teams accept their calls, including close ones. Disagreements go through the question box (Section 4.9) and the Q&A process; teams do not argue calls at the FIELD.

**Safety first.** No point value in this manual is worth an injury. Where competitive advantage conflicts with the safety of people, ROBOTS, or the FIELD, safety takes priority.

SUMMIT PUSH includes defense, contested space, and a protected ENDGAME, so competitive friction will occur. What matters is how a team behaves when it does. Winning a MATCH by exploiting an unintended reading of a rule, or by playing recklessly around a partner's climb, is contrary to the MOUNTAIN ETHIC.

> *Commentary:* The conduct rules apply in full when SUMMIT PUSH is run as a design exercise. In a design challenge, the MOUNTAIN ETHIC governs how entrants treat competing entries, judges, and organizers.

## 1.4 Document Conventions

**Rule numbering.** Rules are grouped by number band:

**Table 1-1: Rule number bands**

| Band | Scope |
|---|---|
| **G1xx** | Personal safety |
| **G2xx** | Conduct |
| **G3xx** | Pre-MATCH (setup, STARTING CONFIGURATION, ROUTE DECLARATION) |
| **G4xx** | In-MATCH robot rules (movement, contact, zones, ENDGAME) |
| **G5xx** | SUPPLY rules (possession, scoring, de-scoring) |
| **R1xx** | Robot size, weight, and extension |
| **R2xx** | Safety and materials |
| **R3xx** | Budget and fabrication |
| **R4xx** | BUMPERS |
| **R5xx** | Motors and actuators |
| **R6xx** | Power distribution |
| **R7xx** | Control system |
| **R8xx** | Pneumatics |

**Violations.** Each rule that can be violated states its consequence in a *Violation:* line. In-MATCH penalties use the taxonomy in Section 4.8. Rules enforced at INSPECTION, and the few rules that forfeit a specific credit, state their consequence directly.

- **VERBAL WARNING:** no points. A recorded warning for a first-instance, low-impact infraction; warnings persist for the team for the remainder of the event.
- **MINOR FOUL:** 3 points credited to the opposing ALLIANCE.
- **MAJOR FOUL:** 8 points credited to the opposing ALLIANCE.
- **YELLOW CARD:** a warning for egregious behavior or for specific listed violations. A second YELLOW CARD in the same tournament phase escalates to a RED CARD.
- **RED CARD:** disqualification for the MATCH.

**Examples and commentary.** Text labeled *Example:* shows how a rule applies and is a binding interpretation. Text labeled *Commentary:* explains design intent and is not binding; the rule text governs.

**Cross-references.** Sections are numbered for citation: "Section 4.3" in running text, "§4.3" in tables and boxes. Rules are cited by number (e.g., **G405**).

## 1.5 Team Updates

The event organizer may issue Team Updates at any time during an event. A Team Update may correct an error, resolve an ambiguity raised through the Q&A process, or, rarely, change a rule or value. Each Team Update is numbered and dated. The most recent Team Update supersedes conflicting text in this manual and in earlier updates. Teams are responsible for working to the manual as updated and should check for Team Updates before finalizing a design.

---

# 2 Game Overview

## 2.1 The Setting

SUMMIT PUSH has a mountaineering theme. Each ALLIANCE is an expedition with one short weather window, the length of a MATCH, to stock its route up a shared peak before a storm closes the mountain.

ROBOTS carry three kinds of SUPPLIES to their ALLIANCE's CRAG, a rock spire at midfield: CACHE CRATES of food and shelter go on shelves, O2 CELLS of oxygen go into angled sockets, and ROPE COILS of climbing line hang on pegs. Stocking a tier of the CRAG establishes a CAMP and lights that tier's ring in the ALLIANCE's color. Establishing all three CAMPS (CAMP I, CAMP II, and HIGH CAMP) lights the SUMMIT BEACON at the top of the spire.

When the MATCH starts, the FORECAST (WHITEOUT, ICEFALL, or GALE) names the SUPPLY whose placement points are doubled during AUTO. Before the MATCH, each ALLIANCE declares a ROUTE: low, mid, or high. The CAMP on the declared ROUTE pays a larger bonus, and higher ROUTES pay more. At the end of the MATCH, ROBOTS score for how high they have climbed the HEADWALL, a leaning three-lane truss at their own end of the FIELD, with rungs rising from the LEDGE RUNG to the CAMP RUNG to the SUMMIT RUNG.

*Figure 2-1. The SUMMIT PUSH FIELD, seen from above the Blue alliance wall. The dimensioned drawings are in Appendix A of the PDF edition and in 03-field/renderings.*

![The SUMMIT PUSH FIELD](../figures/field.png)

## 2.2 The Match

SUMMIT PUSH is played by two ALLIANCES of three teams each on a 54 ft × 27 ft carpeted FIELD. Each MATCH is 2 minutes 30 seconds long: a 15-second AUTONOMOUS period (AUTO), in which ROBOTS operate only on pre-programmed instructions, followed immediately by a 2-minute-15-second TELEOPERATED period (TELEOP), in which DRIVE TEAMS take control. The final 30 seconds of TELEOP is the ENDGAME period, during which HEADWALL protection is active.

**The FIELD.** Each ALLIANCE has one CRAG near midfield: a 48 in × 48 in structure rising to a spire top 90 in above the carpet. The CRAG is the ALLIANCE's only placement structure for SUPPLIES. Between the two CRAGS is the neutral CENTER CACHE, nine SUPPLIES staged across the centerline and contested by both ALLIANCES. Each ALLIANCE's end of the FIELD holds its BASECAMP zone (where ROBOTS start), its HEADWALL (a 144-in-wide climbing truss leaned 15° from vertical and split into three independent lanes), and two OUTFITTER chutes in the wall corners, through which HUMAN PLAYERS feed additional SUPPLIES onto the FIELD.

**The SUPPLIES.** There are three GAME PIECES, each a different shape and size:

**Table 2-1: The three SUPPLIES**

| SUPPLY | Shape | Size | Scores on |
|---|---|---|---|
| **CACHE CRATE** | Cube | 12.0 in | Shelves (24 / 42 in) and BASE DEPOT |
| **O2 CELL** | Cylinder | 5.0 in dia × 14.0 in | Sockets (30 / 54 / 72 in) and BASE DEPOT |
| **ROPE COIL** | Torus | 10.0 in OD | 45° pegs (30 / 54 / 78 in) and BASE DEPOT |

A ROBOT may possess at most 2 SUPPLIES at a time. Each CRAG also has a floor-level BASE DEPOT tray that accepts any SUPPLY in any orientation.

**Placement values.** Every Low-tier scoring position is worth the same, every Mid-tier position is worth the same, and every High-tier position is worth the same, regardless of which SUPPLY it takes. Value rises with height.

**ROUTE DECLARATION.** During setup, each ALLIANCE declares its ROUTE: LOW ROUTE, MID ROUTE, or HIGH ROUTE. An ALLIANCE that makes no declaration is assigned LOW ROUTE. The CAMP bonus matching the declared ROUTE pays its declared value for the entire MATCH (CAMP I +6→+18, CAMP II +10→+24, HIGH CAMP +15→+35). The declared ROUTE is shown on the FIELD LEDs at MATCH start, so opponents can scout it.

**The FORECAST.** When AUTO begins, the Field Management System (FMS) broadcasts one character of game data, `W` (WHITEOUT), `I` (ICEFALL), or `G` (GALE), and the FIELD LEDs display it in white. The FORECAST names the MATCH's PRIORITY SUPPLY (WHITEOUT = CACHE CRATES, ICEFALL = O2 CELLS, GALE = ROPE COILS). Placement points for the PRIORITY SUPPLY are doubled during AUTO, and ROPED UP requires two of it. To take advantage of it, AUTO routines must read the game data and branch between at least three prepared routines. Events without FMS game data use the card-draw fallback in Section 4.3.1.

**AUTO.** Each ROBOT earns 3 points for LEAVE (fully exiting BASECAMP). SUPPLIES score at AUTO values, doubled for the PRIORITY SUPPLY. An ALLIANCE earns the ROPED UP bonus (+10) if all three ROBOTS LEAVE and it scores at least 5 SUPPLIES, including at least two of the PRIORITY SUPPLY and at least one of each other type. AUTO scores are assessed after a 3-second settle window at the end of the period.

**TELEOP.** ALLIANCES cycle SUPPLIES to their CRAG from their OUTFITTER chutes, the staged marks, and the contested CENTER CACHE. Establishing a CAMP (at least one of each required SUPPLY simultaneously SCORED at that tier) latches a bonus and lights that tier's LED ring on the CRAG: CAMP I (+6), CAMP II (+10), HIGH CAMP (+15), each paying its declared value if it matches the declared ROUTE. Establishing all three CAMPS lights the SUMMIT BEACON for a latched +10. SUPPLIES SCORED on a CRAG score for that CRAG's ALLIANCE regardless of which ROBOT placed them, and no ROBOT may remove a SCORED SUPPLY from either CRAG. Defense is legal except against a ROBOT on its own CRAG APRON, a ROBOT in its own OUTFITTER LANE, or, during the ENDGAME, a ROBOT in its own HEADWALL ZONE. ROBOTS may not enter an opponent's OUTFITTER LANE at any time, or an opponent's HEADWALL ZONE during the ENDGAME.

**ENDGAME.** Climbing the HEADWALL is legal at any time; HEADWALL ZONE protection applies from the start of the ENDGAME through climb assessment. Each of the three lanes carries three rungs: the LEDGE RUNG (30 in), CAMP RUNG (54 in), and SUMMIT RUNG (78 in). The rungs are staggered 12 in laterally to alternating sides and set back 6.4 in per step by the 15° lean. Each lane takes one ROBOT, and every climb must begin from the FIELD side of the truss. Climbs are assessed after the final buzzer, when all ROBOTS are at rest or at T+5 seconds, whichever comes first. PARK in BASECAMP scores 3; hanging solely from the LEDGE RUNG scores 12, from the CAMP RUNG 20, and from the SUMMIT RUNG 30. The maximum ALLIANCE climb total is 90.

## 2.3 Match at a Glance

**Table 2-2: MATCH at a glance**

| Phase | Duration | ROBOTS | What scores |
|---|---|---|---|
| **Setup** | pre-MATCH | Staged in BASECAMP; ≤1 preload each | ROUTE DECLARATION made (LOW default) |
| **AUTO** | 0:15 | Pre-programmed only; FORECAST broadcast at T=0 | LEAVE (3/robot); SUPPLIES at AUTO values (PRIORITY SUPPLY doubled); ROPED UP (+10); CAMPS may be established |
| **TELEOP** | 2:15 | Driver-controlled | SUPPLIES at TELEOP values; CAMP bonuses (declared ROUTE's CAMP uplifted); SUMMIT BEACON (+10); climbing legal at any time |
| **ENDGAME** *(final 0:30 of TELEOP)* | 0:30 | HEADWALL ZONE protection active | PARK (3); LEDGE RUNG (12); CAMP RUNG (20); SUMMIT RUNG (30) |
| **Settle** | 0:03 after AUTO and after the final buzzer; climbs assessed at rest or at +0:05 | Disabled at the final buzzer | Scores latch |

## 2.4 Scoring Quick Reference

**SUPPLY placement** (per SUPPLY; AUTO values apply to SUPPLIES whose last placing ROBOT contact occurred before the end of AUTO):

**Table 2-3: SUPPLY placement points**

| Tier | Positions | Height | AUTO | TELEOP |
|---|---|---|---|---|
| **Low** | Shelf 1 (3 slots), Low Sockets (×2), Low Pegs (×2) | 24 / 30 / 30 in | **7** | **4** |
| **Mid** | Shelf 2 (3 slots), Mid Sockets (×2), Mid Pegs (×2) | 42 / 54 / 54 in | **10** | **7** |
| **High** | Summit Socket (×1), High Pegs (×2) | 72 / 78 in | **13** | **10** |
| **BASE DEPOT** | any SUPPLY, any orientation (~12) | floor (4 in lip) | **4** | **2** |

**Table 2-4: Bonus and ENDGAME points**

| Achievement | Requirement | Points |
|---|---|---|
| LEAVE (AUTO) | ROBOT fully exits BASECAMP during AUTO | **3** per ROBOT |
| FORECAST double (AUTO) | PRIORITY SUPPLY placements during AUTO | AUTO value **×2** |
| ROPED UP (AUTO) | All 3 ROBOTS LEAVE and ≥5 SUPPLIES SCORED, including ≥2 of the PRIORITY SUPPLY and ≥1 of each other type | **+10** |
| CAMP I *(latched)* | ≥1 CACHE CRATE on Shelf 1, ≥1 O2 CELL in a Low Socket, ≥1 ROPE COIL on a Low Peg | **+6** *(+18 if LOW ROUTE)* |
| CAMP II *(latched)* | ≥1 CACHE CRATE on Shelf 2, ≥1 O2 CELL in a Mid Socket, ≥1 ROPE COIL on a Mid Peg | **+10** *(+24 if MID ROUTE)* |
| HIGH CAMP *(latched)* | O2 CELL in the Summit Socket, ≥1 ROPE COIL on a High Peg | **+15** *(+35 if HIGH ROUTE)* |
| SUMMIT BEACON *(latched)* | All three CAMPS established | **+10** |
| PARK | ROBOT in BASECAMP at climb assessment | **3** |
| LEDGE RUNG | Supported solely by the LEDGE RUNG | **12** |
| CAMP RUNG | Supported solely by the CAMP RUNG | **20** |
| SUMMIT RUNG | Supported solely by the SUMMIT RUNG | **30** |

**Fouls:** MINOR FOUL = **+3** to the opposing ALLIANCE; MAJOR FOUL = **+8** to the opposing ALLIANCE.

**Ranking:** Win 3 RP, Tie 1 RP, plus three bonus RPs: SUPPLY LINE (total SUPPLIES SCORED, BASE DEPOT included), EXPEDITION (CAMPS established), and ASCENT (ALLIANCE ENDGAME points). Section 4.7 gives the thresholds for each event tier.

> *Example:* Late in a MATCH, Blue, which declared MID ROUTE, completes CAMP II by hanging its first ROPE COIL on a Mid Peg (7 points) while a CACHE CRATE is already on Shelf 2 and an O2 CELL is in a Mid Socket. Blue scores 7 points for the placement plus a latched +24 CAMP II bonus (raised from +10 by the ROUTE DECLARATION). CAMP bonuses latch when the CAMP is established, so if the ROPE COIL is later dislodged without ROBOT contact, the bonus remains; FIELD STAFF restore the SUPPLY at the next safe opportunity.

> *Commentary:* Spectators can follow the score on the FIELD: SUPPLIES accumulate on the two spires, and tier rings light as CAMPS are established. In the final 30 seconds, up to six ROBOTS climb the two HEADWALLS, three per ALLIANCE side by side. A 30-point SUMMIT RUNG climb at the buzzer can decide a close MATCH, but it cannot outweigh two minutes of cycling.
