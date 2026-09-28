# 4 Match Play & Scoring

This section describes how a SUMMIT PUSH MATCH is set up, played, and scored: its periods, scoring conditions, bonuses, and RANKING POINTS. The game rules (G1xx–G5xx) are in Section 5. Where a scoring condition in this section disagrees with a diagram or animation, this text governs.

## 4.1 Match Timeline

A MATCH is 2 minutes 30 seconds long and consists of two periods played back-to-back with no pause:

**Table 4-1: MATCH timeline**

| Period | Duration | Notes |
|---|---|---|
| AUTO | 0:15 | ROBOTS operate autonomously. DRIVE TEAM members may not touch OPERATOR CONSOLE controls. |
| TELEOP | 2:15 | Driver control. The final 0:30 of TELEOP is the ENDGAME period, during which HEADWALL protection (§4.5.4) is active. |

Scores are assessed with settle windows:

- **AUTO settle:** a 3-second window immediately following the end of AUTO. Any SUPPLY that becomes SCORED (Section 4.4.1) before the end of the AUTO settle earns AUTO point values, provided the last ROBOT contact that placed or moved it into its scoring position occurred before the end of AUTO. A SUPPLY placed or moved into its scoring position by ROBOT contact during the settle window earns TELEOP values. Contact with an already-SCORED SUPPLY that does not remove it from its scoring position never changes that SUPPLY's point value, whichever ALLIANCE's ROBOT makes it.
- **LAST ROBOT CONTACT:** for a given SUPPLY, the most recent instant at which any ROBOT was in contact with it while placing or moving it into its scoring position. Contact that neither places nor displaces a SCORED SUPPLY does not establish LAST ROBOT CONTACT.
- **Match settle:** a 3-second window immediately following the final buzzer, after which all SUPPLY scores latch.
- **Climb assessment:** each ROBOT's ENDGAME state is assessed after the final buzzer, at the instant all ROBOTS have come to rest or at T+5 seconds, whichever comes first (Section 4.5.3).
- **End of MATCH:** at the final buzzer the FMS removes ROBOT enable. No ROBOT may move under its own power, or be operated by its DRIVE TEAM, during the match settle or the climb assessment. Residual motion (coasting, swinging, a mechanism settling) is not a violation.

> *Commentary:* The settle windows let a CACHE CRATE released half a second before the buzzer count once it settles onto the shelf, and they spare referees from judging a SUPPLY in flight: a SUPPLY that is at rest and SCORED when the window closes counts. The placing-contact condition limits the AUTO settle to SUPPLIES released during AUTO. A ROBOT cannot earn AUTO values, the FORECAST double, or ROPED UP by scoring during the settle window itself. Likewise, an opponent that brushes a SUPPLY SCORED during AUTO cannot take away its AUTO value.

## 4.2 Match Setup

### 4.2.1 Supply Staging

Sixty-three (63) SUPPLIES (21 CACHE CRATES, 21 O2 CELLS, and 21 ROPE COILS) are staged before each MATCH as follows. Of the 21 SUPPLIES of each type, 3 are neutral in the CENTER CACHE, 2 are staged on each ALLIANCE's side (4 in total), and 7 per ALLIANCE are in OUTFITTER stock (14 in total).

**Table 4-2: SUPPLY staging**

| Location | Contents |
|---|---|
| CENTER CACHE (neutral) | 9 SUPPLIES (3 of each type) at the 9 taped marks of the 3 × 3 grid (24 in spacing, centered on FIELD center), each type once per row and once per column |
| Alliance staging marks (per alliance) | 6 SUPPLIES (2 of each type) at taped marks 12 ft from the alliance wall, at Y = 108, 162, and 216 |
| OUTFITTER chutes (per alliance) | 21 SUPPLIES (7 of each type), stocked behind the ALLIANCE's two OUTFITTER stations for HUMAN PLAYER feed |
| Robot preloads (per alliance) | Up to 1 SUPPLY per ROBOT, of any type, chosen by the team and drawn from the ALLIANCE's OUTFITTER stock during setup (§4.2.2) |

### 4.2.2 Preloads and Starting Configuration

Each ROBOT may begin the MATCH with up to one preloaded SUPPLY of any type, drawn from the ALLIANCE's OUTFITTER stock during setup. The preload must be fully supported by the ROBOT and must not cause the ROBOT to exceed its STARTING CONFIGURATION limits (no more than 42 in tall and, apart from its BUMPERS, within the FRAME PERIMETER; see **R104**). A team may choose not to preload.

ROBOTS must start the MATCH (**G302**):

1. entirely within their ALLIANCE's BASECAMP zone,
2. in contact with their alliance wall, and
3. in legal STARTING CONFIGURATION, with BUMPERS at legal height.

The in-MATCH possession limit is two (2) SUPPLIES in any combination (**G501**). A preload counts toward this limit from the start of AUTO.

> *Example:* A ROBOT preloads an O2 CELL, then collects a ROPE COIL from the CENTER CACHE during AUTO. It is at its possession limit of 2 and may not intake a CACHE CRATE until it SCORES or releases one of the SUPPLIES it controls.

### 4.2.3 ROUTE DECLARATION

During setup, each ALLIANCE declares its ROUTE for the MATCH: LOW ROUTE, MID ROUTE, or HIGH ROUTE. The declared ROUTE raises that ALLIANCE's corresponding CAMP bonus to its declared value for the entire MATCH:

**Table 4-3: ROUTE DECLARATION uplifts**

| Declared ROUTE | CAMP affected | Base | Declared |
|---|---|---|---|
| LOW ROUTE | CAMP I | +6 | **+18** |
| MID ROUTE | CAMP II | +10 | **+24** |
| HIGH ROUTE | HIGH CAMP | +15 | **+35** |

Procedure:

1. A student member of any of the ALLIANCE's three DRIVE TEAMS reports the ALLIANCE's ROUTE to the HEAD REFEREE or a designated route official (**G304**) before the FIELD STAFF "field ready" signal. ALLIANCES are expected to agree in the queue. If DRIVE TEAMS report conflicting ROUTES, the HEAD REFEREE asks the ALLIANCE to resolve the conflict; if it remains unresolved, the default applies.
2. If no ROUTE is declared before the "field ready" signal, the ALLIANCE's ROUTE defaults to LOW ROUTE.
3. Declared ROUTES latch at the "field ready" signal and cannot be changed after it. Each ALLIANCE's declared ROUTE is displayed on the FIELD LEDs at MATCH start and shown on the audience screen.
4. ROUTE DECLARATION is per ALLIANCE and per MATCH. The two ALLIANCES declare independently and may declare the same ROUTE or different ROUTES.

> *Commentary:* Declaring a ROUTE does not limit where an ALLIANCE may score. An ALLIANCE that declares HIGH ROUTE may still score on both lower tiers; it has chosen which CAMP bonus pays its declared value, and its EXPEDITION RP depends on reaching that altitude. The uplifts over base (+12, +14, +20) differ because the three CAMPS are not equally likely to be completed. At completion rates typical of a strong ALLIANCE, LOW and MID are worth within a point of each other and HIGH falls well behind (§4.7), so the best declaration is the one the ALLIANCE can reliably complete. Each team's ROUTE history is worth scouting, because it shows which tier its ALLIANCES tend to work first.

## 4.3 AUTO (0:15)

### 4.3.1 The FORECAST

At T=0 of AUTO, the FMS broadcasts a one-character game data string to all ROBOTS and lights the white FIELD LEDs in the corresponding pattern:

**Table 4-4: FORECAST states**

| Game data | FORECAST | PRIORITY SUPPLY | FIELD LED blocks |
|---|---|---|---|
| `W` | WHITEOUT | CACHE CRATES | 1 |
| `I` | ICEFALL | O2 CELLS | 2 |
| `G` | GALE | ROPE COILS | 3 |

Each PRIORITY SUPPLY that becomes SCORED before the end of the AUTO settle, and whose last placing ROBOT contact occurred before the end of AUTO, earns double its AUTO placement value in every scoring location, including the BASE DEPOT. The FORECAST is field-wide: both ALLIANCES receive the same FORECAST. It affects only AUTO placement points and the ROPED UP requirement (Section 4.3.4), and has no effect on LEAVE, CAMP bonuses, TELEOP values, or ENDGAME. Each of the three values is equally likely, and the FORECAST is not published before the MATCH.

> *Example:* The FORECAST is ICEFALL. During AUTO, Blue scores an O2 CELL in a Mid Socket (10 × 2 = 20), an O2 CELL in the BASE DEPOT (4 × 2 = 8), and a CACHE CRATE on Shelf 1 (7, not doubled). Blue's AUTO placement total is 35.

**Offseason FORECAST fallback (no FMS game data).** Events without FMS game-data support use the following procedure. It has the same standing as the rest of this manual.

1. Before each MATCH, the HEAD REFEREE (or a designated FIELD STAFF member) holds a deck of exactly three cards labeled `W`, `I`, and `G`, shuffles it face-down, and draws one card during the setup period. The drawn card is not revealed to any DRIVE TEAM before AUTO begins.
2. At T=0 of AUTO, the card is revealed to both ALLIANCES at once: the FIELD STAFF member sets the white FIELD LEDs to the corresponding pattern (or, on fields without controllable LEDs, raises a placard visible from all six driver stations and announces the FORECAST over the sound system).
3. A ROBOT without game data may read the FORECAST from a driver-station dashboard entry made by a DRIVER/OPERATOR at the reveal, or by vision on the LEDs or placard, or it may run a fixed-assumption AUTO. **G401** otherwise bars every DRIVE TEAM member from touching the OPERATOR CONSOLE during AUTO, and the DRIVE COACH may not touch it at any time during a MATCH. The single dashboard selection described here is a stated exception to **G401** for one DRIVER/OPERATOR at fallback events and is not "operating the ROBOT." The permitted entry is limited to selecting exactly one of the three FORECAST values (`W`, `I`, or `G`); any other dashboard input during AUTO is operating the ROBOT.
4. The drawn card is returned and the deck reshuffled for every MATCH.

### 4.3.2 LEAVE

A ROBOT earns LEAVE (3 points) if, at any time during AUTO, its BUMPERS have fully exited its ALLIANCE's BASECAMP zone, meaning that no part of its BUMPERS intersects the vertical projection of the BASECAMP zone, tape included. LEAVE latches once earned; a ROBOT that exits and returns to BASECAMP keeps its LEAVE points.

### 4.3.3 AUTO Scoring

SUPPLIES SCORED (per Section 4.4.1) before the end of the AUTO settle earn the AUTO values in the Scoring Summary (Section 4.6), provided the SUPPLY's last placing ROBOT contact occurred before the end of AUTO. A SUPPLY placed or moved into its scoring position during the AUTO settle earns TELEOP values (Section 4.1). CAMPS may be established during AUTO: AUTO placements count toward CAMP requirements, and a CAMP established in AUTO latches immediately.

### 4.3.4 ROPED UP

An ALLIANCE earns ROPED UP (+10) if, during AUTO (assessed at the end of the AUTO settle):

1. all three of its ROBOTS earn LEAVE, and
2. the ALLIANCE has at least 5 SUPPLIES SCORED, including at least 2 of the PRIORITY SUPPLY and at least 1 of each of the other two types, in any combination of scoring locations including the BASE DEPOT, counting only SUPPLIES whose last placing ROBOT contact occurred before the end of AUTO.

ROPED UP is a count of SUPPLIES; their point values do not matter.

> *Commentary:* Four of the five required SUPPLIES are fixed by type (two of the PRIORITY SUPPLY plus one of each other type), and the fifth may be any type. The PRIORITY SUPPLY is not known until T=0, so an ALLIANCE that wants the bonus must prepare three routines and agree in the queue on which ROBOT covers the PRIORITY SUPPLY in each case. With the 2-SUPPLY possession limit and a 15-second AUTO, no single ROBOT can earn it alone.

### 4.3.5 AUTO Distances

The following distances are published for planning AUTO routines. All are straight-line distances from ROBOT center to the target approach position, for the Blue ALLIANCE; Red distances are the same by symmetry.

**Table 4-5: AUTO distances**

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

The CENTER CACHE is equidistant from the two CRAGS, and each SUPPLY type is staged once in each row of the grid, so no type is materially nearer to one ALLIANCE than the other (Section 3.6.1). The race for the CENTER CACHE is therefore symmetric, and contesting it is an intended AUTO strategy: **G402** permits a ROBOT to cross the centerline entirely while any part of its BUMPERS is in the CENTER CACHE band.

## 4.4 TELEOP (2:15)

During TELEOP, DRIVE TEAMS cycle SUPPLIES to their ALLIANCE's CRAG from their OUTFITTER chutes, the staged marks, and the floor. TELEOP point values apply to SUPPLIES that become SCORED after the AUTO settle and before the end of the match settle, and to SUPPLIES SCORED during the AUTO settle whose last placing ROBOT contact occurred after the end of AUTO (Section 4.1).

### 4.4.1 SCORED

A SUPPLY is SCORED in a scoring location when all of the following are true:

1. it is at rest,
2. it is directly and fully supported by the scoring element (support transmitted through another SUPPLY does not qualify), and
3. it is not in contact with any ROBOT of the ALLIANCE for which it would score.

Additional location-specific conditions:

- **BASE DEPOT:** a SUPPLY is SCORED when it is at rest, its only support is the tray floor, and it lies entirely within the vertical projection of the DEPOT channel. A SUPPLY supported by the lip, by the carpet outside the tray, or by another SUPPLY is not SCORED; a SUPPLY that stands taller than the lip is SCORED as long as the tray floor alone supports it. FIELD STAFF may level heaped SUPPLIES during MATCH stoppages; teams may not request leveling.
- **Shelves:** CACHE CRATES only, one per shelf slot. A crate is SCORED in a shelf slot when the shelf alone supports it at rest. A crate resting wholly or partly on another crate is not SCORED, earns no points, and satisfies no CAMP or RANKING POINT requirement.
- **Sockets:** O2 CELLS only, one per socket. An O2 CELL is fully supported by a socket when the socket alone holds it captive at rest.
- **Pegs:** ROPE COILS only, one per peg. A ROPE COIL is SCORED on a peg when the peg passes through the coil's central hole and the peg alone supports it at rest. If more than one ROPE COIL hangs on a peg, only the innermost one supported directly by the peg is SCORED; any additional ROPE COIL is not SCORED, earns no points, and satisfies no CAMP or RANKING POINT requirement.
- Every scoring position (each shelf slot, socket, and peg) SCORES at most one SUPPLY at a time.
- Contact by an opponent ROBOT does not prevent a SUPPLY from being SCORED; condition 3 refers only to the scoring ALLIANCE's ROBOTS.

### 4.4.2 Ownership of Scored Supplies

Any SUPPLY SCORED on a CRAG or in its BASE DEPOT scores for that CRAG's ALLIANCE, regardless of which ROBOT placed it. An opponent therefore cannot pollute a CRAG: a SUPPLY that an opponent pushes into an ALLIANCE's BASE DEPOT during TELEOP is 2 points for that ALLIANCE.

ROBOTS may never remove a SCORED SUPPLY from either CRAG, including either BASE DEPOT (**G503**).

*Violation:* MAJOR FOUL per SUPPLY, and the SUPPLY is restored (Section 4.4.4).

### 4.4.3 CAMPS and the SUMMIT BEACON

A CAMP is established at the moment its required SUPPLIES are simultaneously SCORED. Establishment latches: once established, a CAMP remains established for the rest of the MATCH even if its SUPPLIES are later dislodged. The corresponding LED tier ring (30 / 54 / 78 in) lights in ALLIANCE color when its CAMP is established and never goes dark. LED state is decorative confirmation only; the referee-recorded latch is the scoring authority.

**Table 4-6: CAMP requirements and bonuses**

| CAMP | Requirement (simultaneously SCORED) | Base | If declared ROUTE |
|---|---|---|---|
| **CAMP I** | ≥1 CACHE CRATE on Shelf 1 **+** ≥1 O2 CELL in a Low Socket **+** ≥1 ROPE COIL on a Low Peg | +6 | +18 (LOW ROUTE) |
| **CAMP II** | ≥1 CACHE CRATE on Shelf 2 **+** ≥1 O2 CELL in a Mid Socket **+** ≥1 ROPE COIL on a Mid Peg | +10 | +24 (MID ROUTE) |
| **HIGH CAMP** | ≥1 O2 CELL in the Summit Socket **+** ≥1 ROPE COIL on a High Peg | +15 | +35 (HIGH ROUTE) |
| **SUMMIT BEACON** | All three CAMPS established | +10 | never uplifted |

The SUMMIT BEACON (+10, latched) is banked at the moment the ALLIANCE's third CAMP latches, and the spire lantern lights. CAMPS may be established in any order.

Every CAMP requires one SCORED SUPPLY of each type that its tier accepts. The CRAG has no shelf above 42 in, so HIGH CAMP requires an O2 CELL and a ROPE COIL but no CACHE CRATE. The second High Peg is not part of HIGH CAMP; it is a placement target in its own right and part of the HIGH ROUTE's full capacity (Section 4.7).

**Regional-tier CAMP I substitution:** at Regional-tier events only, a missing piece-type slot of CAMP I may be satisfied by 4 SCORED BASE DEPOT SUPPLIES of that type. The substitution applies to CAMP I only, and to at most one of CAMP I's three slots per MATCH; the other two slots must be satisfied by SUPPLIES SCORED on the low tier itself.

> *Example:* At a Regional-tier event, Red has a crate on Shelf 1 and an O2 CELL in a Low Socket, but no ROBOT that can hang a ROPE COIL. Red pushes 4 ROPE COILS into its BASE DEPOT (8 points as BASE DEPOT SUPPLIES). When the 4th ROPE COIL in the DEPOT is SCORED, CAMP I's rope slot is satisfied and CAMP I latches. This substitution would not satisfy CAMP II's Mid Peg slot at any tier, and does not apply at all at DCMP or Championship tier.

### 4.4.4 Restoration and Out-of-Bounds Supplies

**No-fault knock-offs:** any SUPPLY that leaves a scoring position without direct ROBOT contact on that SUPPLY (for example, from vibration, a bumped CRAG, wind from a passing ROBOT, or another SUPPLY settling) is restored by FIELD STAFF to its scoring position at the next safe opportunity (**G504**). Referees do not attribute causation for no-fault knock-offs, and no points are lost for the interval the SUPPLY was displaced. A latched CAMP is unaffected in any case.

**De-scoring contact:** direct ROBOT contact on a SUPPLY that removes it from a scoring position is a MAJOR FOUL per SUPPLY (Section 4.4.2, **G503**), and the SUPPLY is restored by FIELD STAFF.

**Out-of-bounds supplies:** FIELD STAFF return any SUPPLY that leaves the FIELD, at the next safe opportunity, to the nearest OUTFITTER chute: the chute of the ALLIANCE on that side of the FIELD, which may be an opponent's chute. A ROBOT may not deliberately eject a SUPPLY out of the FIELD (**G507**).

### 4.4.5 Cycle Distances

The following approach distances are published for estimating points per cycle. All are for the Blue ALLIANCE, from ROBOT center to the approach position; Red distances are the same by symmetry.

**Table 4-7: Cycle distances**

| Route | Distance (one way) |
|---|---|
| OUTFITTER (24, 294) → SHELF FACE approach (284, 240) | 266 in |
| OUTFITTER (24, 294) → +Y SOCKET FACE approach (324, 280) | 300 in |
| OUTFITTER (24, 294) → PEG FACE approach (368, 240) | 348 in |
| CENTER CACHE (324, 162) → SHELF FACE approach | 88 in |
| CENTER CACHE (324, 162) → +Y SOCKET FACE approach | 118 in |
| Alliance staging mark (144, 216) → SHELF FACE approach | 142 in |

The CRAG has 17 scoring positions in total (6 shelf slots, 5 sockets, 6 pegs) plus a BASE DEPOT that holds roughly 12 SUPPLIES. Once an ALLIANCE has filled its CRAG, further SUPPLIES can score only in the DEPOT, and the SUPPLY LINE RP thresholds assume that strong ALLIANCES will use it.

## 4.5 ENDGAME (final 0:30)

### 4.5.1 The Climb

Each ALLIANCE's HEADWALL offers three independent 48-in lanes, with one ROBOT per lane (**G415**). Each lane carries three rungs: the LEDGE RUNG (30 in), CAMP RUNG (54 in), and SUMMIT RUNG (78 in). Climbing is legal at any time during the MATCH; only the protection is limited to the ENDGAME and the climb assessment that follows it. A ROBOT may not contact a rung while any part of its BUMPERS is on the alliance-wall side of the CLIMB LINE (X = 48 in for Blue, X = 600 in for Red) unless it is at that moment supported solely by rungs, or is still touching a rung it took hold of while so supported within the preceding 5 seconds (**G416**). Every climb therefore begins from the FIELD side of the truss.

### 4.5.2 Climb and Park Definitions

At climb assessment (Section 4.5.3), each ROBOT earns exactly one of the following (the highest that applies):

**Table 4-8: Climb and PARK states**

| State | Definition | Points |
|---|---|---|
| **SUMMIT RUNG climb** | ROBOT supported solely by the SUMMIT RUNG (directly or via its own mechanisms), BUMPERS not in contact with the carpet | **30** |
| **CAMP RUNG climb** | As above, for the CAMP RUNG | **20** |
| **LEDGE RUNG climb** | As above, for the LEDGE RUNG | **12** |
| **PARK** | ROBOT's BUMPERS fully contained within the vertical projection of its ALLIANCE's BASECAMP zone; ROBOT not supported solely by a rung. Contact with HEADWALL structure other than a rung is permitted; rung contact from the carpet is governed by **G416** | **3** |

"Supported solely by" a rung means that the rung, through the ROBOT's own mechanisms, bears the ROBOT's entire weight, with no contact with the carpet, a partner ROBOT, or any other FIELD element that transfers support. Incidental, non-supporting contact with the HEADWALL truss (for example, a swing-damping roller or a guide wheel riding the diagonal) is permitted. A ROBOT supported in any part by a partner ROBOT is not supported solely by a rung and earns no rung credit. Partner support is legal (**G413**), but there are no buddy climbs in SUMMIT PUSH.

A ROBOT whose weight is carried by two rungs at once (caught mid-traversal at assessment) is credited for the lower of the two. This is the only case in which support by more than one rung scores, so a traversal that stalls partway still earns the lower rung's value.

Maximum ALLIANCE climb total: 90 (three SUMMIT RUNG climbs).

> *Example:* At assessment, a Blue ROBOT hangs with its hooks on the SUMMIT RUNG, but one climber arm still lightly loads the CAMP RUNG below. It scores 20 (CAMP RUNG). Its partner hangs cleanly from the CAMP RUNG: 20. The third ROBOT's climb failed, and it sits in BASECAMP with BUMPERS on the carpet: PARK, 3. Blue ENDGAME total: 43.

### 4.5.3 Assessment Timing

ENDGAME states are assessed after the final buzzer, at the instant all ROBOTS have come to rest or at T+5 seconds, whichever comes first. A ROBOT that reaches a rung early and hangs there for the last minute is assessed with every other ROBOT after the final buzzer; no ENDGAME state is locked in before then. A ROBOT still swinging at T+5 s is assessed in whatever state it occupies at that instant. A ROBOT that falls after its state has been assessed keeps its points.

### 4.5.4 HEADWALL Protection

From the start of the ENDGAME period until climb assessment is complete, the HEADWALL ZONE (each ALLIANCE's taped BASECAMP area) is protected. An opponent ROBOT may not contact a ROBOT whose BUMPERS are wholly or partly within its own ALLIANCE's HEADWALL ZONE, and may not contact a ROBOT that is supported by its own ALLIANCE's HEADWALL, wherever that ROBOT's BUMPERS project. During that window, a ROBOT may not position its BUMPERS within the opponent's HEADWALL ZONE at all. This is a line call on the contacted ROBOT's position and does not depend on intent (**G412**). Contact that the protected ROBOT initiates is not a violation (**G205**).

**Blocked and displaced climbs.** A ROBOT prevented from attaining a rung by a violation of **G412** or **G413** is credited at the LEDGE RUNG value (12), unless it was already supported by a higher rung when the violation occurred, in which case that rung's value applies. Points awarded under this paragraph are ENDGAME points and count toward the ASCENT RP.

## 4.6 Scoring Summary

All point values in SUMMIT PUSH:

**Table 4-9: Scoring summary**

| Category | Item | Height | Piece | AUTO | TELEOP |
|---|---|---|---|---|---|
| Placement, Low tier | Shelf 1 (3 slots) | 24 in | CACHE CRATE | 7 | 4 |
| Placement, Low tier | Low Socket (×2) | 30 in | O2 CELL | 7 | 4 |
| Placement, Low tier | Low Peg (×2) | 30 in | ROPE COIL | 7 | 4 |
| Placement, Mid tier | Shelf 2 (3 slots) | 42 in | CACHE CRATE | 10 | 7 |
| Placement, Mid tier | Mid Socket (×2) | 54 in | O2 CELL | 10 | 7 |
| Placement, Mid tier | Mid Peg (×2) | 54 in | ROPE COIL | 10 | 7 |
| Placement, High tier | Summit Socket (×1) | 72 in | O2 CELL | 13 | 10 |
| Placement, High tier | High Peg (×2) | 78 in | ROPE COIL | 13 | 10 |
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

In Qualification MATCHES, ALLIANCES earn RANKING POINTS (RP): Win = 3 RP, Tie = 1 RP, Loss = 0 RP, plus up to three bonus RPs (maximum 6 RP per MATCH). Bonus RPs are earned independently of the MATCH outcome. Their thresholds increase with event tier:

**Table 4-10: Bonus RANKING POINT thresholds**

| Bonus RP | Earned for | Regional | District Championship (DCMP) | Championship |
|---|---|---|---|---|
| **SUPPLY LINE RP** | Total SUPPLIES SCORED by the ALLIANCE, BASE DEPOT included | ≥15 | ≥19 | ≥23 |
| **EXPEDITION RP** | CAMPS established | 2 CAMPS, including the CAMP matching the ALLIANCE's declared ROUTE | All 3 CAMPS | All 3 CAMPS and the declared ROUTE's tier at full capacity |
| **ASCENT RP** | ALLIANCE ENDGAME points (climbs + PARKS) | ≥32 | ≥52 | ≥60 |

**SUPPLY LINE count.** The SUPPLY LINE RP counts the SUPPLIES in a SCORED state (Section 4.4.1) at the close of the match settle. Any SUPPLY then awaiting a **G504** restoration (Section 4.4.4) is counted in the scoring position it occupied when it was displaced. Each physical SUPPLY counts at most once: a SUPPLY scored, dislodged, and re-scored is one SUPPLY.

**Full capacity** (Championship EXPEDITION RP) is seven SCORED positions for every ROUTE:

**Table 4-11: Full capacity by declared ROUTE**

| Declared ROUTE | Full capacity = all of |
|---|---|
| LOW | Shelf 1 ×3, Low Sockets ×2, Low Pegs ×2 |
| MID | Shelf 2 ×3, Mid Sockets ×2, Mid Pegs ×2 |
| HIGH | Summit Socket ×1, High Pegs ×2, Mid Sockets ×2, Mid Pegs ×2 |

Full capacity is assessed at the end of the match settle; it does not latch when first reached. The HIGH set reaches down into the mid tier because the CRAG has only three positions above 54 in. Adding the four hardest mid-tier positions keeps the count at seven for every ROUTE.

All three CAMPS are also required, so the three ROUTES differ only in what they add beyond the CAMPS. LOW adds four low-tier positions (24–30 in), MID adds four mid-tier positions (42–54 in), and HIGH adds three: the second High Peg at 78 in, the second Mid Socket, and the second Mid Peg. HIGH requires one fewer position because one of its three, the second High Peg, is the hardest position on the CRAG.

**Design-challenge note:** design entries are judged against the Championship column. A Championship-caliber design contributes toward ≥23 SCORED SUPPLIES, all three CAMPS with the declared ROUTE tier at full capacity, and a ≥60-point ENDGAME.

> *Commentary:* The Regional ASCENT threshold of 32 can be met with one CAMP RUNG climb plus one LEDGE RUNG climb (32), or with one SUMMIT RUNG climb plus a PARK (33), so an ALLIANCE with one strong climber and modest partners can still earn it at small events. The Championship threshold of 60 is set so that "all three ROBOTS reach the CAMP RUNG" (3 × 20) earns the RP; it does not require two SUMMIT RUNG climbs.

> *Commentary:* The uplifts are set so that each declaration is the best choice for some ALLIANCES and no declaration is best for all of them. With all three CAMPS established, declaring pays 53 / 55 / 61 bonus points (LOW / MID / HIGH, SUMMIT BEACON included). If the declared CAMP is not established, the declaration pays nothing and the ALLIANCE also loses the BEACON, leaving 25 / 21 / 16. Writing *p* for the ALLIANCE's chance of establishing the CAMP it declares, expected value is 25 + 28p for LOW, 21 + 34p for MID, and 16 + 45p for HIGH. Those three lines cross at p = 9/17 ≈ 0.53 (HIGH over LOW) and p = 5/11 ≈ 0.45 (HIGH over MID), but only if the ALLIANCE is equally likely to establish whichever CAMP it declares, which no ALLIANCE is. CAMP I is the easiest and HIGH CAMP the hardest, so the real decision compares different probabilities: against a 0.95 chance at CAMP I, declaring HIGH needs about p = 0.79 at HIGH CAMP to overtake declaring LOW. Applied to sample capability profiles:
>
> | ALLIANCE | chance of CAMP I / II / HIGH | EV of LOW | EV of MID | EV of HIGH | declares |
> |---|---|---|---|---|---|
> | elite | .98 / .95 / .90 | 52.4 | 53.3 | **56.5** | HIGH |
> | strong | .92 / .90 / .55 | 50.8 | **51.6** | 40.8 | MID |
> | good | .95 / .85 / .50 | **51.6** | 49.9 | 38.5 | LOW |
> | developing | .90 / .70 / .30 | **50.2** | 44.8 | 29.5 | LOW |
> | rookie | .70 / .35 / .05 | **44.6** | 32.9 | 18.3 | LOW |
>
> The declaration is therefore a bet on the ALLIANCE's demonstrated capability. Because it is public on the FIELD LEDs at MATCH start (**G304**), opponents can read it and defend the tier it names.

**Ranking order.** Teams are ranked by:

1. RANKING SCORE: average RP per Qualification MATCH played (Section 8.2);
2. cumulative MATCH points (fouls included);
3. cumulative AUTO points;
4. cumulative ENDGAME points;
5. random sort by FMS.

**Playoffs.** The top 8 seeded ALLIANCES (standard alliance selection) play an 8-ALLIANCE double-elimination bracket. Playoff MATCHES are scored by MATCH points only, with no RPs; ties are handled as described in Section 8.4.

## 4.8 Violation Taxonomy

Every rule violation that carries an in-MATCH penalty uses the following taxonomy. Rules enforced at INSPECTION instead state their own consequence ("ROBOT will not pass INSPECTION"), and a few rules add a specific forfeiture (no LEAVE credit, no rung credit, BYPASSED, DISABLED) named in their own *Violation:* line. Each rule's *Violation:* line specifies which apply; escalation for repeated violations is at the HEAD REFEREE's discretion within the listed range.

**Table 4-12: Violation levels**

| Level | Effect |
|---|---|
| **VERBAL WARNING** | No points. Issued for first-instance, low-impact infractions where the rule so provides. Warnings persist for the team for the remainder of the event. |
| **MINOR FOUL** | +3 points credited to the opposing ALLIANCE's MATCH score. |
| **MAJOR FOUL** | +8 points credited to the opposing ALLIANCE's MATCH score. |
| **YELLOW CARD** | Formal warning for egregious ROBOT or team-member behavior, or for specific listed violations. A second YELLOW CARD in the same tournament phase automatically becomes a RED CARD. YELLOW CARDS reset between the qualification and playoff phases. |
| **RED CARD** | Disqualification for the MATCH: the team earns 0 MATCH points and 0 RP in a Qualification MATCH; in Playoffs, a RED CARD disqualifies the ALLIANCE for that MATCH. |

Foul points are added to the opponent's score. They count toward the MATCH outcome and toward every points-based threshold except the bonus-RP thresholds, which are computed only from the earning ALLIANCE's own SCORED SUPPLIES, CAMPS, and ENDGAME points.

> *Commentary:* The contact rules in §5 are judged by outcome (damage, functional impairment, tipping). The exceptions are the protected zones, line calls that referees make from the tape: the CRAG APRON, the OUTFITTER LANES, the ENDGAME HEADWALL ZONE, and during AUTO the opponent's side of the centerline. Everywhere else, whether a defensive contact draws a foul depends on what the contact did.

## 4.9 Score Finality and the Question Box

Referees record SCORED SUPPLIES, latched CAMP and SUMMIT BEACON states, ENDGAME states, and fouls; the FMS totals them. The HEAD REFEREE approves the MATCH score.

A MATCH score becomes FINAL when the HEAD REFEREE approves it. If approval has not been given sooner, the score becomes FINAL at the start of the next MATCH played on that FIELD. For the last MATCH of a tournament phase, of a day, or of the event, where there is no next MATCH, it becomes FINAL 10 minutes after the final buzzer if it has not been approved sooner. The HEAD REFEREE may extend that 10-minute window once, by announcement, while a question box conversation or a **G504** restoration is still open. All **G504** restorations (Section 4.4.4) are completed and accounted for before approval.

**Question box.** One student DRIVE TEAM member per ALLIANCE may present a question to the HEAD REFEREE at the question box before the score is FINAL (**G204**). Only SCORING ERRORS can be corrected: a miscounted or misattributed SUPPLY, an unrecorded CAMP or SUMMIT BEACON latch, a mis-entered ENDGAME state, or a foul credited to the wrong ALLIANCE. A disagreement with a referee's judgment about whether a violation occurred is not a SCORING ERROR and is never reviewable; referee judgment is final per **G204**.

Once FINAL, a MATCH score may not be changed.

## 4.10 ALLIANCE Roles

SUMMIT PUSH rewards ALLIANCES built from complementary ROBOTS. Four ALLIANCE ROLES recur. They describe common designs and are not rules.

**Table 4-13: ALLIANCE Roles**

| Role | Primary targets | What it contributes |
|---|---|---|
| **CRATE FREIGHTER** | Shelf 1 and Shelf 2, BASE DEPOT | Volume toward SUPPLY LINE, and the crate slot of both CAMP I and CAMP II. Wide compliant intake and a 42-in lift. |
| **O2 SURGEON** | Low, Mid, and Summit Sockets | The oxygen slot of every CAMP, including the High-tier Summit Socket. Reorientation wrist plus a 72-in reach. |
| **RING ALPINIST** | Low, Mid, and High Pegs | The High Pegs, which no other role can supply, and therefore HIGH CAMP and the HIGH ROUTE's full capacity. Hook or spear end effector plus a 78-in reach. |
| **HYBRID** | Two tiers across two piece types, plus a strong climb | Flexibility in the draft, cover for a partner's failure, and usually the ALLIANCE's ASCENT contribution. |

Placement values depend only on tier. In TELEOP, a CRATE FREIGHTER filling six shelf slots scores 33 placement points, an O2 SURGEON filling five sockets scores 32, and a RING ALPINIST filling six pegs scores 42. Within a tier, every position pays the same for every piece; the totals differ because each piece has a different number of positions on each tier. The CRAG has no crate position above 42 in, so a CACHE CRATE's best TELEOP placement is worth 7 points, while a ROPE COIL's is worth 10. The roles are therefore drafted as complements.
