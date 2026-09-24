# 4 MATCH PLAY & SCORING

This section describes how a SUMMIT PUSH MATCH is set up, played, and scored. ROBOT conduct rules (G1xx–G5xx) appear in Section 5; this section defines the *state machine of the MATCH itself*: periods, scoring conditions, bonuses, and RANKING POINTS. Where a scoring condition in this section and a diagram or animation disagree, this text is the authority.

## 4.1 Match Timeline

A MATCH is 2 minutes 30 seconds long and consists of two periods played back-to-back with no pause:

| Period | Duration | Notes |
|---|---|---|
| AUTO | 0:15 | ROBOTS operate autonomously. DRIVERS may not touch OPERATOR CONSOLE controls. |
| TELEOP | 2:15 | Driver control. The **final 0:30 of TELEOP is the ENDGAME period**, during which HEADWALL protection (Section 4.5.4) is active. |

Scores are assessed with settle windows:

- **AUTO settle:** a 3-second window immediately following the end of AUTO. Any SUPPLY that becomes SCORED (Section 4.4.1) before the end of the AUTO settle earns AUTO point values, provided the last ROBOT contact that placed or moved it into its scoring position occurred before the end of AUTO. A SUPPLY placed or moved into its scoring position by ROBOT contact during the settle window earns TELEOP values. Contact with an already-SCORED SUPPLY that does not remove it from its scoring position never changes that SUPPLY's point value, whichever ALLIANCE's ROBOT makes it.
- **LAST ROBOT CONTACT:** for a given SUPPLY, the most recent instant at which any ROBOT was in contact with it *while placing or moving it into its scoring position*. Contact that neither places nor displaces a SCORED SUPPLY does not establish LAST ROBOT CONTACT.
- **Match settle:** a 3-second window immediately following the final buzzer, after which all SUPPLY scores latch.
- **Climb assessment:** each ROBOT's ENDGAME state is assessed after the final buzzer — at the instant all ROBOTS have come to rest, or at T+5 seconds, whichever comes first (Section 4.5.3).
- **End of MATCH:** at the final buzzer the FMS removes ROBOT enable. No ROBOT may move under its own power, or be operated by its DRIVE TEAM, during the match settle or the climb assessment; residual motion — coasting, swinging, a mechanism settling — is not a violation.

> *Commentary:* The settle windows exist so that a CACHE CRATE released a half-second before the buzzer, still settling onto a shelf, counts, and so referees never have to judge a SUPPLY "in flight." If it is at rest and SCORED when the window closes, it counts. The placing-contact condition on the AUTO settle exists so that the window rewards SUPPLIES released *during* AUTO, not SUPPLIES placed after it: a ROBOT cannot bank AUTO values, the FORECAST double, or ROPED UP by scoring during the settle window itself. Equally, an opponent brushing a SUPPLY already SCORED during AUTO cannot strip its AUTO value.

## 4.2 Match Setup

### 4.2.1 Supply Staging

Sixty-three (63) SUPPLIES — 21 CACHE CRATES, 21 O2 CELLS, 21 ROPE COILS — are staged before each MATCH as follows. Per type, the 21 SUPPLIES break down as: 3 neutral in the CENTER CACHE + 2 staged per ALLIANCE side (4) + 7 per ALLIANCE in OUTFITTER stock (14).

| Location | Contents |
|---|---|
| CENTER CACHE (neutral) | 9 SUPPLIES (3 of each type) at the 9 taped marks of the 3×3 grid (24 in spacing, centered on FIELD center), one type per row and per column |
| Alliance staging marks (per alliance) | 6 SUPPLIES (2 of each type) at taped marks 12 ft from the alliance wall, at Y = 108, 162, and 216 |
| OUTFITTER chutes (per alliance) | 21 SUPPLIES (7 of each type), stocked behind the ALLIANCE's two OUTFITTER stations for HUMAN PLAYER feed |
| Robot preloads (per alliance) | Up to **1 SUPPLY per ROBOT, of any type**, chosen by the team and **drawn from the ALLIANCE's OUTFITTER stock during setup** (Section 4.2.2) |

### 4.2.2 Preloads and Starting Configuration

Each ROBOT may begin the MATCH with up to one preloaded SUPPLY of any type, drawn from the ALLIANCE's OUTFITTER stock during setup. The preload must be fully supported by the ROBOT and must not cause the ROBOT to exceed its starting configuration limits (≤ 42 in tall, within the FRAME PERIMETER — see R1xx). A team may elect to preload nothing.

ROBOTS must start the MATCH:

1. entirely within their ALLIANCE's BASECAMP zone, and
2. in contact with their alliance wall, and
3. in legal STARTING CONFIGURATION, with BUMPERS at legal height.

The in-match possession limit is two (2) SUPPLIES in any combination (see G5xx). A preload counts toward this limit from the start of AUTO.

> *Example:* A ROBOT preloads an O2 CELL, then collects a ROPE COIL from the CENTER CACHE during AUTO. It is at its possession limit of 2 and may not intake a CACHE CRATE until it SCORES or releases one of the SUPPLIES it controls.

### 4.2.3 ROUTE DECLARATION

During setup, each ALLIANCE declares its ROUTE for the MATCH: LOW ROUTE, MID ROUTE, or HIGH ROUTE. The declared ROUTE raises that ALLIANCE's corresponding CAMP bonus to its declared value for the entire MATCH:

| Declared ROUTE | CAMP affected | Base | Declared |
|---|---|---|---|
| LOW ROUTE | CAMP I | +6 | **+18** |
| MID ROUTE | CAMP II | +10 | **+24** |
| HIGH ROUTE | HIGH CAMP | +15 | **+35** |

Procedure:

1. A student member of any of the ALLIANCE's three DRIVE TEAMS reports the ALLIANCE's ROUTE to the HEAD REFEREE (or enters it at the FMS route selector, where equipped) before the FIELD STAFF "field ready" signal. ALLIANCES are expected to agree in the queue; if DRIVE TEAMS report conflicting ROUTES, the HEAD REFEREE will ask the ALLIANCE to resolve the conflict, and if it remains unresolved the default applies.
2. If no ROUTE is declared before the "field ready" signal, the ALLIANCE's ROUTE defaults to LOW ROUTE.
3. Declared ROUTES latch at the "field ready" signal and cannot be changed thereafter. Each ALLIANCE's declared ROUTE is displayed on the FIELD LEDs at MATCH start and shown on the audience screen.
4. ROUTE DECLARATION is per-ALLIANCE and per-MATCH. The two ALLIANCES declare independently and may declare the same or different ROUTES.

> *Commentary:* The ROUTE is a promise, not a restriction. An ALLIANCE that declares HIGH ROUTE may still score at every level of both lower tiers; it has simply chosen which CAMP bonus pays its declared value, and staked its EXPEDITION RP on reaching that altitude. The uplifts are deliberately unequal — +12, +14, +20 over base — because the three CAMPS are not equally likely to be completed. At completion rates typical of a strong ALLIANCE the three declarations are worth within a couple of points of each other, so the right declaration is the one that matches what the ALLIANCE can actually finish. Scouts should track opponents' ROUTE histories: a team that always declares LOW has announced where its ALLIANCE will spend the first ninety seconds.

## 4.3 AUTO (0:15)

### 4.3.1 The FORECAST

At T=0 of AUTO, the FMS broadcasts a one-character game data string to all ROBOTS and lights the white FIELD LEDs in the corresponding pattern:

| Game data | FORECAST | PRIORITY SUPPLY | FIELD LED blocks |
|---|---|---|---|
| `W` | WHITEOUT | CACHE CRATES | 1 |
| `I` | ICEFALL | O2 CELLS | 2 |
| `G` | GALE | ROPE COILS | 3 |

Each PRIORITY SUPPLY that becomes SCORED before the end of the AUTO settle, and whose last placing ROBOT contact occurred before the end of AUTO, earns double its AUTO placement value in every scoring location including the BASE DEPOT. The FORECAST is field-wide (both ALLIANCES receive the same FORECAST), affects AUTO placement points and the ROPED UP requirement (Section 4.3.4) only, and has no effect on LEAVE, CAMP bonuses, TELEOP values, or ENDGAME. The FORECAST is equally likely to be any of the three values and is not published before the MATCH.

> *Example:* The FORECAST is ICEFALL. During AUTO, Blue scores an O2 CELL in a Mid Socket (10 × 2 = 20), an O2 CELL in the BASE DEPOT (4 × 2 = 8), and a CACHE CRATE on Shelf 1 (7, not doubled). Blue's AUTO placement total is 35.

**Offseason FORECAST fallback (no FMS game data).** Events without FMS game-data support use the following procedure, which is part of this manual rather than an optional appendix:

1. Before each MATCH, the HEAD REFEREE (or a designated FIELD STAFF member) holds a deck of exactly three cards labeled `W`, `I`, and `G`, shuffles it face-down, and draws one card during the setup period. The drawn card is not revealed to any DRIVE TEAM before AUTO begins.
2. At T=0 of AUTO, the card is revealed simultaneously to both ALLIANCES: the FIELD STAFF member sets the white FIELD LEDs to the corresponding pattern (or, on fields without controllable LEDs, raises a placard visible from all six driver stations and announces the FORECAST over the sound system).
3. ROBOTS without game data may read the FORECAST via a driver-station dashboard entry made by a DRIVER/OPERATOR at reveal, via vision on the LED or placard, or may run a fixed-assumption AUTO. **G401** otherwise bars every DRIVE TEAM member from touching the OPERATOR CONSOLE during AUTO, and the DRIVE COACH may never touch it at all; the single dashboard selection described here is a stated exception to G401 for one DRIVER/OPERATOR at fallback events, and is not "operating the ROBOT." The permitted entry is limited to selecting exactly one of the three FORECAST values (`W`, `I`, or `G`) and nothing else; any other dashboard input during AUTO is operating the ROBOT.
4. The drawn card is returned and the deck reshuffled for every MATCH.

### 4.3.2 LEAVE

A ROBOT earns LEAVE (3 points) if, at any time during AUTO, its BUMPERS have fully exited its ALLIANCE's BASECAMP zone — no part of the ROBOT's BUMPERS intersects the vertical projection of the BASECAMP tape. LEAVE latches once earned; a ROBOT that exits and returns to BASECAMP keeps its LEAVE points.

### 4.3.3 AUTO Scoring

SUPPLIES SCORED (per Section 4.4.1) before the end of the AUTO settle earn the AUTO values in the Scoring Summary (Section 4.6), provided the SUPPLY's last placing ROBOT contact occurred before the end of AUTO; a SUPPLY placed or moved into its scoring position during the AUTO settle earns TELEOP values (Section 4.1). CAMP bonuses may be established during AUTO: AUTO placements count toward CAMP requirements, and a CAMP established in AUTO latches immediately.

### 4.3.4 ROPED UP

An ALLIANCE earns ROPED UP (+10) if, during AUTO (assessed at the end of the AUTO settle):

1. all three of its ROBOTS earn LEAVE, and
2. the ALLIANCE has at least **5 SUPPLIES SCORED**, including **at least 2 of the PRIORITY SUPPLY** and **at least 1 of each of the other two types**, in any combination of scoring locations including the BASE DEPOT, counting only SUPPLIES whose last placing ROBOT contact occurred before the end of AUTO.

ROPED UP counts SUPPLIES, not points.

> *Commentary:* ROPED UP is where the FORECAST earns its keep. Four of the five required SUPPLIES are pinned by type — two of the PRIORITY SUPPLY plus one of each other type — and the fifth is free; which type is doubled arrives at T = 0. An ALLIANCE that wants the bonus must prepare three routines and agree in the queue on who covers the doubled type in each branch. Under the 2-SUPPLY possession limit and a 15-second clock, no single ROBOT can earn it alone.

### 4.3.5 Designing an AUTO

The following distances are published so that AUTO routines can be planned on paper before they are driven. All are straight-line, ROBOT-center to target-approach, for the Blue ALLIANCE; Red mirrors.

| From | To | Distance |
|---|---|---|
| BASECAMP center (24, 162) | BASECAMP tape edge at X = 48 (LEAVE) | 24 in, plus half the ROBOT's BUMPER length |
| BASECAMP center | Blue alliance staging mark (144, 162) | 120 in |
| BASECAMP center | Blue SHELF FACE approach (284, 240) | 271 in |
| Blue staging mark (144, 216) | Blue SHELF FACE approach (284, 240) | 142 in |
| Blue SHELF FACE approach | nearest CENTER CACHE mark (300, 186) | 56 in |
| Blue +Y SOCKET FACE approach (324, 280) | nearest CENTER CACHE mark (324, 186) | 94 in |
| CENTER CACHE center (324, 162) | Blue CRAG center | 78 in |
| CENTER CACHE center | Red CRAG center | 78 in |

The CENTER CACHE is equidistant from the two CRAGS, and each SUPPLY type is staged once in each row of the grid, so no type is nearer to one ALLIANCE than the other. The contested race for the cache is therefore symmetric, and it is the intended high-ceiling AUTO play: **G402** permits a ROBOT to cross the centerline entirely while any part of its BUMPERS is in the CENTER CACHE band.

## 4.4 TELEOP (2:15)

During TELEOP, DRIVE TEAMS cycle SUPPLIES from their OUTFITTER chutes, staged marks, and the floor to their ALLIANCE's CRAG. TELEOP point values apply to SUPPLIES that become SCORED after the AUTO settle and before the end of the match settle, and to SUPPLIES SCORED during the AUTO settle whose last placing ROBOT contact occurred after the end of AUTO (Section 4.1).

### 4.4.1 SCORED

A SUPPLY is SCORED in a scoring location when all of the following are true:

1. it is at rest,
2. it is directly and fully supported by the scoring element (support transmitted through another SUPPLY does not qualify), and
3. it is not in contact with any ROBOT of the ALLIANCE for whom it would score.

Additional location-specific conditions:

- **BASE DEPOT:** a SUPPLY is SCORED when it is at rest, its only support is the tray floor, and it lies entirely within the vertical projection of the DEPOT channel. A SUPPLY supported by the lip, by the carpet outside the tray, or by another SUPPLY is not SCORED; a SUPPLY that stands taller than the lip is SCORED so long as the tray floor alone supports it. FIELD STAFF may level heaped SUPPLIES during MATCH stoppages; teams may not request leveling.
- **Shelves:** CACHE CRATES only, one per shelf slot. A crate is SCORED in a shelf slot when the shelf alone supports it at rest. A crate resting wholly or partly on another crate is NOT SCORED, earns no points, and satisfies no CAMP or RANKING POINT requirement.
- **Sockets:** O2 CELLS only, one per socket. An O2 CELL is fully supported by a socket when the socket alone holds it captive at rest.
- **Pegs:** ROPE COILS only, one per peg. A ROPE COIL is SCORED on a peg when the peg passes through the coil's central hole and the peg alone supports it at rest. If more than one coil hangs on a peg, only the innermost coil supported directly by the peg is SCORED; any additional coil is NOT SCORED, earns no points, and satisfies no CAMP or RANKING POINT requirement.
- Every scoring position — each shelf slot, socket, and peg — SCORES at most one SUPPLY at a time.
- Contact by an *opponent* ROBOT does not prevent a SUPPLY from being SCORED (condition 3 refers only to the scoring ALLIANCE's ROBOTS).

### 4.4.2 Ownership of Scored Supplies (Anti-Pollution)

Any SUPPLY SCORED on a CRAG or in its BASE DEPOT scores for that CRAG's ALLIANCE, regardless of which ROBOT placed it. There is no such thing as polluting an opponent's CRAG: a SUPPLY an opponent pushes into an ALLIANCE's BASE DEPOT is 2 points for that ALLIANCE.

ROBOTS may never remove a SCORED SUPPLY from either CRAG, including either BASE DEPOT.

*Violation:* MAJOR FOUL per SUPPLY, and the SUPPLY is restored (Section 4.4.4).

### 4.4.3 Camps and the SUMMIT BEACON

A CAMP is established at the moment its required SUPPLIES are simultaneously SCORED. Establishment latches: once established, a CAMP remains established for the rest of the MATCH even if its SUPPLIES are later dislodged. The corresponding LED tier ring (30 / 54 / 78 in) ignites in ALLIANCE color when its CAMP is established and never un-lights. LED state is decorative confirmation only; the referee-recorded latch is the scoring authority.

| CAMP | Requirement (simultaneously SCORED) | Base | If declared ROUTE |
|---|---|---|---|
| **CAMP I** | ≥1 CACHE CRATE on Shelf 1 **+** ≥1 O2 CELL in a Low Socket **+** ≥1 ROPE COIL on a Low Peg | +6 | +18 (LOW ROUTE) |
| **CAMP II** | ≥1 CACHE CRATE on Shelf 2 **+** ≥1 O2 CELL in a Mid Socket **+** ≥1 ROPE COIL on a Mid Peg | +10 | +24 (MID ROUTE) |
| **HIGH CAMP** | ≥1 O2 CELL in the Summit Socket **+** ≥1 ROPE COIL on a High Peg | +15 | +35 (HIGH ROUTE) |
| **SUMMIT BEACON** | All three CAMPS established | +10 | never uplifted |

The SUMMIT BEACON (+10, latched) is banked at the moment the ALLIANCE's third CAMP latches; the spire lantern ignites. CAMPS may be established in any order.

Every CAMP follows the same pattern — one SCORED SUPPLY of each type the tier offers. HIGH CAMP therefore requires oxygen and rope but no crate: crates are not hauled above CAMP II, and the CRAG carries no shelf above 42 in. The second High Peg is not part of HIGH CAMP; it is a placement target in its own right and part of the HIGH ROUTE's full capacity (Section 4.7).

**Regional-tier CAMP I substitution:** at Regional-tier events only, a missing piece-type slot of CAMP I may be satisfied by 4 SCORED BASE DEPOT SUPPLIES of that type. The substitution applies to CAMP I only, and to at most one of CAMP I's three slots per MATCH; the other two slots must be satisfied by SUPPLIES SCORED on the low tier itself.

> *Example:* At a Regional-tier event, Red has a crate on Shelf 1 and an O2 CELL in a Low Socket, but no rope-capable ROBOT. Red pushes 4 ROPE COILS into its BASE DEPOT (8 points as BASE DEPOT SUPPLIES). The moment the 4th DEPOT rope is SCORED, CAMP I's rope slot is satisfied and CAMP I latches. This substitution would not satisfy CAMP II's mid-peg slot at any tier, and would not apply at all at DCMP or Championship tier.

### 4.4.4 Restoration and Out-of-Bounds Supplies

**No-fault knock-offs:** any SUPPLY that leaves a scoring position without direct ROBOT contact on that SUPPLY — vibration, a bumped CRAG, wind from a passing ROBOT, another SUPPLY settling — is restored by FIELD STAFF to an equivalent scoring position at the next safe opportunity. Referees do not attribute causation for no-fault knock-offs, and no points are lost for the interval the SUPPLY was displaced. A latched CAMP is unaffected in any case.

**De-scoring contact:** direct ROBOT contact on a SUPPLY that removes it from a scoring position is a MAJOR FOUL per SUPPLY (Section 4.4.2), and the SUPPLY is restored by FIELD STAFF.

**Out-of-bounds supplies:** any SUPPLY that leaves the FIELD is returned by FIELD STAFF, at the next safe opportunity, to the nearest OUTFITTER chute — the chute of the ALLIANCE on that side of the FIELD, which may be an opponent's chute. ROBOTS and HUMAN PLAYERS may not deliberately eject SUPPLIES from the FIELD (see G5xx).

### 4.4.5 Cycle reference

The following approach distances are published so that points-per-cycle models can be built from the geometry rather than guessed. All are for the Blue ALLIANCE, ROBOT center to approach position; Red mirrors.

| Route | Distance (one way) |
|---|---|
| OUTFITTER (24, 294) → SHELF FACE approach (284, 240) | 266 in |
| OUTFITTER (24, 294) → +Y SOCKET FACE approach (324, 280) | 300 in |
| OUTFITTER (24, 294) → PEG FACE approach (368, 240) | 348 in |
| CENTER CACHE (324, 162) → SHELF FACE approach | 88 in |
| CENTER CACHE (324, 162) → +Y SOCKET FACE approach | 118 in |
| Alliance staging mark (144, 216) → SHELF FACE approach | 142 in |

The CRAG carries 17 scoring positions in total (6 shelf slots, 5 sockets, 6 pegs) plus a BASE DEPOT of roughly 12. An ALLIANCE that fills the CRAG has taken its precision work off the board; the DEPOT is where the back half of a dominant MATCH goes, and the SUPPLY LINE RP is written on the assumption that it will.

## 4.5 ENDGAME (final 0:30)

### 4.5.1 The Climb

Each ALLIANCE's HEADWALL offers three independent 48-in lanes; one ROBOT per lane (see G4xx). Each lane carries three rungs: LEDGE RUNG (30 in), CAMP RUNG (54 in), SUMMIT RUNG (78 in). Climbing is legal at any time during the MATCH; only the *protection* is limited to the ENDGAME and the climb assessment that follows it. A ROBOT may not contact a rung while any part of its BUMPERS is on the alliance-wall side of the CLIMB LINE — X = 48 in for Blue, X = 600 in for Red — unless it is at that moment supported solely by rungs, or is still touching a rung it took hold of while so supported within the preceding 5 seconds (**G416**). Every climb therefore begins from the FIELD side of the truss.

### 4.5.2 Climb and Park Definitions

At climb assessment (Section 4.5.3), each ROBOT earns exactly one of the following (the highest that applies):

| State | Definition | Points |
|---|---|---|
| **SUMMIT RUNG climb** | ROBOT supported **solely by** the SUMMIT RUNG (directly or via its own mechanisms), BUMPERS not in contact with the carpet | **30** |
| **CAMP RUNG climb** | As above, for the CAMP RUNG | **20** |
| **LEDGE RUNG climb** | As above, for the LEDGE RUNG | **12** |
| **PARK** | ROBOT's BUMPERS fully contained within the vertical projection of its ALLIANCE's BASECAMP zone; ROBOT not fully supported by a rung. Contact with HEADWALL structure other than a rung is permitted (see **G416**) | **3** |

"Supported solely by" a rung means the rung, through the ROBOT's own mechanisms, bears the ROBOT's entire weight: no contact with the carpet, a partner ROBOT, or any other FIELD element that transfers support. Incidental, non-supporting contact with the HEADWALL truss — a swing-damping roller, a guide wheel riding the diagonal — is permitted. A ROBOT supported in any part by a partner ROBOT is not supported *solely* by a rung and so earns no rung credit: partner support is legal (**G413**) but worth nothing. There are no buddy climbs in SUMMIT PUSH.

A ROBOT whose weight is carried by two rungs at once — caught mid-traversal at assessment — is credited for the **lower** of the two. This is the one case in which support by more than one rung still scores, and it is why a traversal that stalls is worth attempting rather than abandoning.

Maximum ALLIANCE climb total: 90 (three SUMMIT RUNG climbs).

> *Example:* At assessment, a Blue ROBOT hangs with its hooks on the SUMMIT RUNG but one climber arm still lightly loads the CAMP RUNG below. It scores 20 (CAMP RUNG). Its partner hangs cleanly from the CAMP RUNG: 20. The third ROBOT's climb failed; it sits in BASECAMP with BUMPERS on the carpet: PARK, 3. Blue ENDGAME total: 43.

### 4.5.3 Assessment Timing

ENDGAME states are assessed after the final buzzer: at the instant all ROBOTS have come to rest, or at T+5 seconds, whichever comes first. A ROBOT that reaches a rung early and hangs there for the last minute is assessed with everyone else, on the buzzer — nothing is locked in before then. A ROBOT still swinging at T+5 s is assessed in whatever state it occupies at that instant. A ROBOT that falls after its state has been assessed keeps its points.

### 4.5.4 HEADWALL Protection

From the start of the ENDGAME period until climb assessment is complete, the HEADWALL ZONE (each ALLIANCE's taped BASECAMP area) is protected. An opponent ROBOT may not contact a ROBOT whose BUMPERS are wholly or partly within its own ALLIANCE's HEADWALL ZONE, and may not contact a ROBOT that is supported by its own ALLIANCE's HEADWALL, wherever that ROBOT's BUMPERS project. An opponent ROBOT may not position its BUMPERS within the opponent's HEADWALL ZONE at all during that window. This is a line call on the contacted ROBOT's position, not a judgment of intent. See **G412**.

**Blocked and displaced climbs.** A ROBOT prevented from attaining a rung by a violation of **G412** or **G413** is credited at the LEDGE RUNG value (12), unless it was already supported by a higher rung when the violation occurred, in which case that rung's value applies. Points awarded under this paragraph are ENDGAME points and count toward the ASCENT RP.

## 4.6 Scoring Summary

All point values in SUMMIT PUSH:

| Category | Item | Height | Piece | AUTO | TELEOP |
|---|---|---|---|---|---|
| Placement — Low tier | Shelf 1 (3 slots) | 24 in | CACHE CRATE | 7 | 4 |
| Placement — Low tier | Low Socket (×2) | 30 in | O2 CELL | 7 | 4 |
| Placement — Low tier | Low Peg (×2) | 30 in | ROPE COIL | 7 | 4 |
| Placement — Mid tier | Shelf 2 (3 slots) | 42 in | CACHE CRATE | 10 | 7 |
| Placement — Mid tier | Mid Socket (×2) | 54 in | O2 CELL | 10 | 7 |
| Placement — Mid tier | Mid Peg (×2) | 54 in | ROPE COIL | 10 | 7 |
| Placement — High tier | Summit Socket (×1) | 72 in | O2 CELL | 13 | 10 |
| Placement — High tier | High Peg (×2) | 78 in | ROPE COIL | 13 | 10 |
| Placement | BASE DEPOT | floor (4 in lip) | any | 4 | 2 |
| AUTO | FORECAST | — | PRIORITY SUPPLY | ×2 on placement values | — |
| AUTO | LEAVE | — | — | 3 / robot | — |
| AUTO | ROPED UP | — | — | +10 / alliance | — |
| Bonus (latched) | CAMP I | low tier | — | +6 (**+18** if LOW ROUTE) | same |
| Bonus (latched) | CAMP II | mid tier | — | +10 (**+24** if MID ROUTE) | same |
| Bonus (latched) | HIGH CAMP | high tier | — | +15 (**+35** if HIGH ROUTE) | same |
| Bonus (latched) | SUMMIT BEACON | 84 in lantern | — | +10 | same |
| ENDGAME | PARK | — | — | — | 3 |
| ENDGAME | LEDGE RUNG | 30 in | — | — | 12 |
| ENDGAME | CAMP RUNG | 54 in | — | — | 20 |
| ENDGAME | SUMMIT RUNG | 78 in | — | — | 30 |
| Penalty | MINOR FOUL | — | — | +3 to opponent | +3 to opponent |
| Penalty | MAJOR FOUL | — | — | +8 to opponent | +8 to opponent |

A CRAG filled to capacity in TELEOP is worth 107 placement points (28 low + 49 mid + 30 high); a full BASE DEPOT adds about 24.

## 4.7 RANKING POINTS

In qualification MATCHES, ALLIANCES earn RANKING POINTS (RP): Win = 3 RP, Tie = 1 RP, Loss = 0 RP, plus up to three bonus RPs (maximum 6 RP per MATCH). Bonus RPs are earned independently of the MATCH outcome. Thresholds escalate by event tier:

| Bonus RP | Earned for | Regional | District Championship (DCMP) | Championship |
|---|---|---|---|---|
| **SUPPLY LINE RP** | Total SUPPLIES SCORED by the ALLIANCE, BASE DEPOT included | ≥15 | ≥19 | ≥23 |
| **EXPEDITION RP** | CAMPS established | 2 CAMPS, including the CAMP matching the ALLIANCE's declared ROUTE | All 3 CAMPS | All 3 CAMPS **and** the declared ROUTE's tier at **full capacity** |
| **ASCENT RP** | ALLIANCE ENDGAME points (climbs + PARKS) | ≥32 | ≥52 | ≥60 |

**SUPPLY LINE count.** The SUPPLY LINE RP counts the number of SUPPLIES in a SCORED state (Section 4.4.1) at the close of the final match settle, with any SUPPLY then awaiting a **G504** restoration (Section 4.4.4) counted in the scoring position it occupied when it was displaced. Each physical SUPPLY counts at most once; a SUPPLY scored, dislodged, and re-scored is one SUPPLY, not two.

**Full capacity** (Championship EXPEDITION RP) is **seven SCORED positions** for every ROUTE:

| Declared ROUTE | Full capacity = all of |
|---|---|
| LOW | Shelf 1 ×3, Low Sockets ×2, Low Pegs ×2 |
| MID | Shelf 2 ×3, Mid Sockets ×2, Mid Pegs ×2 |
| HIGH | Summit Socket ×1, High Pegs ×2, Mid Sockets ×2, Mid Pegs ×2 |

Full capacity is assessed at the end of the match settle, not merely latched earlier. The HIGH set reaches down into the mid tier because the CRAG has only three positions above 54 in; requiring the four hardest mid-tier positions alongside them keeps the count at seven for every ROUTE.

Because all three CAMPS are required as well, the three ROUTES differ only in what they add on top of the CAMPS: LOW adds four low-tier positions (24–30 in), MID adds four mid-tier positions (42–54 in), and HIGH adds three — the second High Peg at 78 in, the second Mid Socket, and the second Mid Peg. HIGH asks for one fewer position and gets the largest bonus because the position it asks for is the hardest on the CRAG.

**Design-challenge note:** design entries are judged against the Championship column. A Championship-caliber design contributes toward ≥23 SCORED SUPPLIES, all three CAMPS with the declared ROUTE tier at full capacity, and a ≥60-point ENDGAME.

> *Commentary:* The Regional ASCENT threshold of 32 is reachable two ways — one CAMP RUNG plus one LEDGE RUNG (32), or one SUMMIT RUNG plus a PARK (33) — so a single strong climber with modest partners is never locked out at small events. The Championship threshold of 60 is set so that "all three ROBOTS reach the CAMP RUNG" (3 × 20) earns the RP; it does not require two SUMMIT RUNG climbs.

> *Commentary:* The uplifts are set so that each declaration is the right answer for some real ALLIANCE, and none is the right answer for all of them. With all three CAMPS established, declaring pays **53 / 55 / 61** bonus points (LOW / MID / HIGH, SUMMIT BEACON included); if the declared CAMP is not established, the declaration pays nothing and the ALLIANCE also loses the BEACON, leaving **25 / 21 / 16**. Writing *p* for the ALLIANCE's chance of establishing the CAMP it declares, expected value is 25 + 28p for LOW, 21 + 34p for MID, and 16 + 45p for HIGH. Those three lines cross at **p = 9/17 ≈ 0.53** (HIGH over LOW) and **p = 5/11 ≈ 0.45** (HIGH over MID) — but only if the ALLIANCE is equally likely to land whichever CAMP it declares, which no ALLIANCE is. CAMP I is the easiest and HIGH CAMP the hardest, so the decision that matters compares *different* probabilities: against a 0.95 chance at CAMP I, declaring HIGH needs about **p = 0.79** at HIGH CAMP to overtake declaring LOW. Worked through plausible capability profiles:
>
> | ALLIANCE | chance of CAMP I / II / HIGH | EV of LOW | EV of MID | EV of HIGH | declares |
> |---|---|---|---|---|---|
> | elite | .98 / .95 / .90 | 52.4 | 53.3 | **56.5** | HIGH |
> | strong | .92 / .90 / .55 | 50.8 | **51.6** | 40.8 | MID |
> | good | .95 / .85 / .50 | **51.6** | 49.9 | 38.5 | LOW |
> | developing | .90 / .70 / .30 | **50.2** | 44.8 | 29.5 | LOW |
> | rookie | .70 / .35 / .05 | **44.6** | 32.9 | 18.2 | LOW |
>
> The declaration is therefore a real, scoutable bet on the ALLIANCE's own demonstrated capability rather than a formality — and because it is public on the FIELD LEDs at MATCH start (**G304**), an opponent can read it and defend the tier it names.

**Ranking order.** Teams are ranked by:

1. **Ranking Score** — average RP per qualification MATCH played;
2. cumulative MATCH points (fouls included);
3. cumulative AUTO points;
4. cumulative ENDGAME points;
5. random sort by FMS.

**Playoffs.** The top 8 seeded ALLIANCES (standard alliance selection) play an 8-ALLIANCE double-elimination bracket; playoff MATCHES are scored by MATCH points only (no RPs), with tie handling per the Tournament section.

## 4.8 Violation Taxonomy

Every rule violation that carries an in-MATCH penalty uses the following taxonomy. Rules enforced at INSPECTION instead state their own consequence ("ROBOT will not pass INSPECTION"), and a few rules add a specific forfeiture — no LEAVE credit, no rung credit, BYPASSED, DISABLED — named in their own Violation line. Each rule's `Violation:` line specifies which apply; escalation for repeated violations is at the HEAD REFEREE's discretion within the listed range.

| Level | Effect |
|---|---|
| **VERBAL WARNING** | No points. Issued for first-instance, low-impact infractions where the rule so provides. Warnings persist for the team for the remainder of the event. |
| **MINOR FOUL** | **+3 points** credited to the opposing ALLIANCE's MATCH score. |
| **MAJOR FOUL** | **+8 points** credited to the opposing ALLIANCE's MATCH score. |
| **YELLOW CARD** | Formal warning for egregious ROBOT or team-member behavior. A **second YELLOW CARD in the same tournament phase automatically becomes a RED CARD.** YELLOW CARDS reset between the qualification and playoff phases. |
| **RED CARD** | Disqualification for the MATCH: the team earns 0 MATCH points and 0 RP in a qualification MATCH; in playoffs, a RED CARD disqualifies the ALLIANCE for that MATCH. |

Foul points are added to the opponent's score and count toward the MATCH outcome and every points-based threshold *except* bonus-RP thresholds, which are computed from the earning ALLIANCE's own SCORED SUPPLIES, CAMPS, and ENDGAME points only.

> *Commentary:* SUMMIT PUSH's contact rules (Section 5) are written by outcome — damage, functional impairment, tipping — not geometry, with two bright-line exceptions that referees call off the tape: the CRAG APRON and the ENDGAME HEADWALL ZONE. The test for whether a defensive play draws a flag is what the contact *did*, not where it *was* — unless it was across one of those two lines.

## 4.9 Score Finality and the Question Box

Referees record SCORED SUPPLIES, latched CAMP and SUMMIT BEACON states, ENDGAME states, and FOULS; the FMS totals them. The HEAD REFEREE approves the MATCH score.

A MATCH score becomes FINAL when the HEAD REFEREE approves it. If approval has not been given sooner, the score becomes FINAL at the start of the next MATCH played on that FIELD, or — for the last MATCH of a tournament phase, of a day, or of the event, where there is no next MATCH — **10 minutes after the final buzzer**, whichever comes first. The HEAD REFEREE may extend that 10-minute window once, by announcement, while a question box conversation or a **G504** restoration is still open. All **G504** restorations (Section 4.4.4) are completed and accounted before approval.

**Question box.** One student DRIVE TEAM member per ALLIANCE may present a question to the HEAD REFEREE at the question box before the score is FINAL (**G204**). Only SCORING ERRORS are correctable: a miscounted or misattributed SUPPLY, an unrecorded CAMP or SUMMIT BEACON latch, a mis-entered ENDGAME state, or a FOUL credited to the wrong ALLIANCE. A disagreement with a referee's judgment about whether a violation occurred is not a SCORING ERROR and is never reviewable; referee judgment is final per **G204**.

Once FINAL, a MATCH score may not be changed.

## 4.10 ALLIANCE Roles

SUMMIT PUSH is designed so that a complete ALLIANCE is assembled from complementary ROBOTS rather than three copies of one design. Four ALLIANCE ROLES recur; they are descriptive, not rules.

| Role | Primary targets | What it contributes |
|---|---|---|
| **CRATE FREIGHTER** | Shelf 1 and Shelf 2, BASE DEPOT | Volume toward SUPPLY LINE, both crate slots for CAMP I and CAMP II. Wide compliant intake and a 42-in lift. |
| **O2 SURGEON** | Low, Mid, and Summit Sockets | The oxygen slot of every CAMP and the single highest-value placement on the FIELD. Reorientation wrist plus a 72-in reach. |
| **RING ALPINIST** | Low, Mid, and High Pegs | The High Pegs, which no other role can supply, and therefore HIGH CAMP and the HIGH ROUTE's full capacity. Hook or spear end effector plus a 78-in reach. |
| **HYBRID** | Two tiers across two piece types, plus a strong climb | Flexibility in the draft, cover for a partner's failure, and usually the ALLIANCE's ASCENT contribution. |

Because placement values are uniform by tier, no role is a points tax: a CRATE FREIGHTER filling six shelf slots banks 33 points of placement, an O2 SURGEON filling five sockets banks 32, and a RING ALPINIST filling six pegs banks 42. Within any one tier every position pays the same whatever the piece; the totals differ because the tiers each piece can reach differ. The CRAG carries no crate position above 42 in, so a crate role's best cycle is worth 7 while a peg role's tops out at 10 — which is why the roles are drafted as complements rather than ranked.
