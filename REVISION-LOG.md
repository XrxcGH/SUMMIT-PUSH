# SUMMIT PUSH — Revision Log

Every change from **v1.0** to **v2.0**, with the reasoning and the arithmetic behind it. Entries are grouped by kind and each one names the files it touched, so any single change can be reviewed or reverted in isolation.

Verification for the numeric changes lives in the cross-check script noted at the end; it currently reports zero failures.

---

## A. Editorial and identity

| # | Change | Why | Files |
|---|---|---|---|
| A1 | Removed the fictional sponsor ("presented by Ridgeline Outfitters") everywhere, including the manual cover line, the section-1 title block, the CADathon brief, and the README. | The package is now generic. | manual header, sections 01, brief, README |
| A2 | Removed every reference to a specific team, including the tie-breaker example, the CADathon note, the judging "buildable by X's shop" line, and the README credits. | So the release can be used by any program as a training exercise. | spec, sections 01/03/06, vision guide, brief, README |
| A3 | Removed the ℠ mark and the "Presented by … 2026" cover line. | Nothing in the package is a claimed mark. | README, brief, manual header |
| A4 | Converted first-person plural and second-person marketing voice to third person throughout. Replaced "A Message from the (Fictional) Game Design Team" with **§1.2 Design Intent**, a factual statement of the four design commitments. | The manual now reads like a rulebook rather than a pitch. Section numbering is unchanged so every "Section 1.3 / 1.4" citation still resolves. | section 01 |
| A5 | Tightened the story section (§2.1 "The Setting"), removed the closing slogan and the hype adjectives, kept the setting. | Real season manuals carry a short thematic passage; they do not carry taglines. | section 01 |
| A6 | Deduplicated the manual title block: the compiled manual no longer prints two H1 titles 21 lines apart. | `manual-header.md` now owns the front matter; section 01 begins at `# 1 Introduction`. | manual header, section 01 |
| A7 | Rule captions that were jokes are now descriptive: G105 → *Stay off FIELD elements*, G413 → *Use only your own HEADWALL*, G414 → *No detached components*. | Consistency with the rest of the caption set. | section 04 |

---

## B. Blocking geometry defects

### B1 — BASE DEPOT scoring was geometrically unsatisfiable

**v1.0:** a SUPPLY was SCORED in the BASE DEPOT only when "entirely below the plane of the top of the DEPOT lip (Z = 4 in)."
**Problem:** the CACHE CRATE is a 12.0-in cube (13.0 in across its pillowed faces) and the O2 CELL is 5.0 in in diameter. Neither can ever be entirely below 4 in, in any orientation. Only the ROPE COIL could ever be SCORED in a DEPOT — which contradicted the "accepts any piece in any orientation" text, the `any` row of every scoring table, the Regional CAMP I substitution, the G503 example, and the entire BASECAMP BOT reference design.
**v2.0:** a SUPPLY is SCORED in the BASE DEPOT when it is at rest, its **only support is the tray floor**, and it lies **entirely within the vertical projection of the DEPOT channel**. The 4.0-in lip is retained as robot-clearing geometry, so nothing else changes.
*Files:* spec §1.6, sections 02/03/06, CAD package §3.

### B2 — the Summit Socket could not be reached by a legal ROBOT

**v1.0:** the Summit Socket rim sat **on the CRAG's vertical axis** at 66 in, inside a spire recess.
**Problem:** the axis is 24.0 in from every face of a 48 × 48 in tower. R402 mandates 3.0 in of bumper, so a FRAME PERIMETER can never be closer than 27.0 in to the axis, against an 18-in extension limit (R105/G404) — short by 9 in from the best face and by 25.75 in from the SHELF FACE past the DEPOT, where the required reach is 43.75 in (19.75 in of standoff plus 24 in to the axis). HIGH CAMP, the SUMMIT BEACON, HIGH ROUTE, and the DCMP/Championship EXPEDITION RP were all unachievable. The tube also interfered with the spire: with the recess 10.0 in deep, its back wall *is* the crag axis, so a 6.68-in-OD tube on that axis was 3.2 in inside solid material at the rim.
**v2.0:** the Summit Socket moves onto the **SHELF FACE**, on the CRAG's centerline, **rim 72 in**, **8.0 in out from the face plane**, tilted 15° from vertical outward. The spire recess is deleted; the spire is a clean prism. Reach from a ROBOT at the DEPOT lip is **11.75 in** — inside the limit, with the 72-in lift as the actual difficulty. A SCORED CELL still leans toward the owning ALLIANCE's driver stations.
*Files:* spec §3, section 02 §3.3.2, CAD package §2.4, vision guide §6.6, ledger rows 7–8.

### B3 — the HEADWALL AprilTag panels stood in the climbing volume

**v1.0:** lane tag panels at **X = 50, Z = 30**, described as "2 in field-side of plane P's carpet line."
**Problem:** the offset was computed at the carpet but applied at 30 in. Plane P at Z = 30 is at X = 39.96, so a 10.5-in panel at X = 50 sat **10 in field-side of P** — directly in front of the LEDGE RUNG, at LEDGE height, spanning the lane centerline. It blocked the rung it was supposed to help a ROBOT find, and violated the sheet's own "all truss structure ≥ 4.0 in behind plane P" rule by 13.7 in.
**v2.0:** lane tags move to **Z = 12 in** on a plumb panel at **X = 39 (Blue) / 609 (Red)**, mounted on the truss lower crossbeam through a 15° wedge bracket. The panel's most-forward point clears plane P by **4.42 in**, satisfying the clearance rule over its whole height, and nothing enters the climbing volume.
*Files:* spec §6, section 02 §3.7, CAD package §4.1/§7, vision guide §§1–3, `apriltag-field-layout.json`.

### B4 — the OUTFITTER chute could not pass a CACHE CRATE

**v1.0:** chute opening **30 in wide × 12 in tall**.
**Problem:** a cube's minimum width in any orientation is its edge, so a 12.0-in crate needs more than 12.0 in of aperture; with the 0.5-in face crown its true envelope is 13.0 in. Clearance was −1.0 in. Fourteen of the 21 crates begin the MATCH in OUTFITTER stock and every out-of-bounds SUPPLY returns through a chute, so a third of the game's pieces had no legal path onto the FIELD.
**v2.0:** opening **30 in × 16 in**, sill unchanged at 24 in (opening spans Z 24–40). 3.0 in of clearance on the crowned crate; the tag panel at Z = 52 still clears the opening top by 7.50 in.
*Files:* spec §3, section 02 §3.5, G506, CAD package §5, ledger row 12.

### B5 — the BUMPER ZONE was shallower than a legal BUMPER

**v1.0:** R403 required BUMPERS "located entirely within the BUMPER ZONE, the volume bounded by the floor and horizontal planes 2.5 in and 5.75 in," while R402 required a 4.5-in cross-section. A 4.5-in bumper cannot fit inside a 3.25-in volume, and the sentence named three bounding surfaces for a two-bound volume.
**v2.0:** R403 is a **fill** rule, not a containment rule: BUMPERS must *completely fill* the 2.5–5.75 in zone, so a 4.5-in bumper sits with its bottom edge between 1.25 and 2.5 in above the floor, and no part of it may exceed 7.0 in. R402's Backing row was also 5 in tall inside a 4.5-in bumper; it is now 4.5 in, and the foam is two stacked 2.25-in cylinders so the cross-section closes geometrically.
*Files:* section 05 R402/R403, §7.3, §7.4 item 5.

### B6 — the SUMMIT RUNG was reachable without climbing

**Problem:** the HEADWALL leans back over BASECAMP, so the SUMMIT RUNG hangs at X ≈ 27.3 — almost 21 in inside the taped zone. A ROBOT could park beneath it and reach it with a purely vertical mast, skipping the traversal entirely. Nothing in v1.0 prevented this.
**v2.0:** new **G416** — a ROBOT supported by the carpet may not contact a HEADWALL rung unless its BUMPERS are entirely outside its own BASECAMP. The published arithmetic then follows: from the tape line the FRAME PERIMETER is at X = 51, so the LEDGE RUNG needs 10.84 in of extension, the CAMP RUNG 17.27 in, and the SUMMIT RUNG **23.70 in** — beyond the 18-in limit, so the SUMMIT RUNG can only be reached from a hang.
*Files:* spec §3, section 02 §3.4, section 03 §4.5.1, G416, CAD package §4.1.

### B7 — the lateral stagger did nothing

**v1.0:** rungs 30.0 in long, staggered ±6.0 in.
**Problem:** LEDGE spanned lane-centerline −21 to +9 and CAMP spanned −9 to +21, so an 18-in-wide common band engaged all three rungs with zero lateral motion. A straight telescoping hook *did* follow the rung line, contradicting the manual's own claim.
**v2.0:** rungs **20.0 in** long, staggered **±12.0 in**. LEDGE spans −22 to −2 and CAMP spans +2 to +22 — **no lateral position engages two successive rungs**. Rungs stay 2 in inside their lane and the minimum inter-lane gap is 4.0 in. The stagger convention is now published per lane, including the Red mirror.
*Files:* spec §3, section 02 §3.4, CAD package §4.1 (with a derived rung-end table).

---

## C. Other geometry corrections

| # | Change | Reason |
|---|---|---|
| C1 | Socket rim-center standoff **6.0 → 8.0 in**; tube length **12.0 → 7.0 in**. | At 6.0/12.0 the tube's closed bottom landed exactly on the face plane and its inboard edge penetrated the tower shell by 2.89 in — eight interferences per field. At 8.0/7.0 the bottom is 4.50 in outboard and the inboard edge 1.61 in outboard. A seated CELL now protrudes 7.0 in along the axis (4.39 in clear of the rim's high lip) instead of 0.06 in, so a SCORED call is a glance, not a look down the tube. |
| C2 | SUMMIT BEACON is now the **translucent top 12 in of the spire** (Z 78–90, luminous center 84 in). | v1.0 put a ⌀4-in dome "centered on the spire top face at 84 in" while the spire top is at 90 in — a lamp 6 in inside solid material. Making the lantern part of the prism keeps both the 84-in luminous center and the 90-in overall height exact. |
| C3 | CRAG APRON offset **36 in everywhere, trimmed at the CENTER CACHE band** → **36 in on the SHELF and PEG faces, 20 in on the SOCKET faces, corners filleted R20, no trim**. | The trim rectangle was exactly the inter-crag corridor, and each CRAG's field-center-facing SOCKET FACE apron lay entirely inside it — so one of the two socket faces on every CRAG had *no* APRON protection, undisclosed. Two 36-in aprons also could not coexist with the staged CENTER CACHE inside a 108-in corridor. At 20 in the aprons occupy Y 108–128 and 196–216, leaving a 68-in open corridor that contains the whole cache (Y 132–192). The corner radius drops from 36 to 20 so the fillet is tangent to both offset lines — a 36-in arc cannot meet a 20-in offset. G407 loses its band-exclusion clause and becomes a clean line call. |
| C4 | BASE DEPOT channel and corner wraps confirmed at **16.0 in** (not reduced), with the open-aperture consequence stated. | 16.0 is required for a 13.0-in crowned crate to fit the channel's vertical projection at all. The shelves overhang 14.0 in, so the outer 2.0 in of the shelf-face leg and both 16 × 16 in corner wraps are open from above; the rest is loaded by pushing. Both facts are now published rather than left to be discovered. |
| C5 | Shelf slot lateral centers published as **±15.5 / 0**. | Four 1.5-in fences and three 14.0-in slots across a 48-in face put the outer centers at ±15.5, not ±14. The vision guide had ±14 and was wrong by 1.5 in. |
| C6 | Rung setback corrected **6.5 → 6.4 in** (24 × tan 15° = 6.4308). | The package published both values. |
| C7 | CENTER CACHE staging changed from **one type per column** to a **Latin square** (each type once per row and once per column). | The column layout aligned the crate column with Blue's SHELF FACE and the rope column with Red's, so six of the nine neutral pieces cost Red about 50% more travel. A strictly rotation-invariant 3/3/3 assignment is impossible on a 3 × 3 grid (one fixed point, four swapped pairs), so the Latin square is the best achievable: aggregate haul distance is **identical** for both alliances (725.0 in each) and no single type differs by more than 1%. Staged O2 CELLS now lie axis-along-+X so the cache spans Y 132–192 and clears both aprons by 4 in. |
| C8 | Starting position: "touching the alliance wall **or the HEADWALL**" → **touching the alliance wall**. | The truss leans back over BASECAMP; the clear height under its field-side face is H(X) = 3.732 × (43.86 − X), so a 42-in ROBOT fits only up to X = 32.6 and cannot reach the truss at that height without raking its superstructure back nearly 10 in. The clear-volume curve is now published in CAD package §4.1 rather than left as a trap. |
| C9 | CRAG AprilTag centers **12 → 17.5 in**; all panels **10.5 → 9.0 in** square. | At 12 in, a 12.0-in CACHE CRATE standing in the BASE DEPOT occludes the shelf-face and inner-socket-face tag pairs — a routine game state. At 17.5 in on a 9.0-in panel the target spans Z 13.44–21.56, clearing a crate top by 1.44 in below and the Shelf 1 underside by 1.25 in above, with the Low Socket tube's lowest point 0.71 in above the target. |
| C10 | Shelf gusset envelope bounded. | v1.0 left it "free," which allowed a Shelf 2 gusset to hang into the space a CRATE on Shelf 1 occupies. |

---

## D. Scoring and balance

### D1 — placement values are now uniform by tier

**v1.0 (TELEOP):** Shelf 1 = 3, Shelf 2 = 5, Low Socket = 4, Mid Socket = 7, Summit Socket = 10, Low Peg = 4, Mid Peg = 6, High Peg = 9.
**Problem:** CACHE CRATES were worth 24 points across six positions (4.00 per piece) against O2's 32 across five (6.40) and rope's 38 across six (6.33). Crates are the largest and heaviest piece and demand the widest intake and a 42-in lift, and a Shelf 1 placement was worth barely more per second than dumping in the DEPOT. The CRATE FREIGHTER was a tax, not a strategy.
**v2.0:** **Low tier 7 AUTO / 4 TELEOP · Mid tier 10 / 7 · High tier 13 / 10 · BASE DEPOT 4 / 2.** Altitude prices the task; piece type does not.

| Type | v1.0 ceiling | v2.0 ceiling |
|---|---|---|
| CACHE CRATE (6 positions) | 24 | **33** |
| O2 CELL (5 positions) | 32 | **32** |
| ROPE COIL (6 positions) | 38 | **42** |
| **Full CRAG** | 94 | **107** |

*Files:* spec §4, sections 01 §2.4, 03 §4.6, brief Appendix A.

### D2 — the ROUTE DECLARATION was a dominated choice

**v1.0:** the declared ROUTE doubled its CAMP bonus (+6→+12, +10→+20, +15→+30), and the Championship EXPEDITION RP required "the declared ROUTE camp at full capacity" — 7 positions for LOW and MID but only **3** for HIGH, which the manual itself conceded was identical to establishing HIGH CAMP. Since all three CAMPS are required at that tier anyway, declaring HIGH added **zero** extra work and paid the largest bonus. HIGH ROUTE was strictly dominant on both axes, so the declaration was not a decision.
**v2.0, two changes:**
1. **Uplifts are scaled by tier difficulty:** CAMP I 6 → **18** (+12), CAMP II 10 → **24** (+14), HIGH CAMP 15 → **35** (+20). At plausible completion rates the three declarations sit within a couple of points of each other, and the optimum moves with capability — a mid-tier ALLIANCE maximizes on LOW, a strong one on MID, an elite one on HIGH.
2. **Full capacity is seven positions for every ROUTE.** HIGH is defined as Summit Socket + both High Pegs + both Mid Sockets + both Mid Pegs, so the HIGH declaration now costs the four hardest mid-tier positions on top of its own tier.

*Files:* spec §1.2/§4/§5, sections 01 §2.2/§2.4, 03 §4.2.3/§4.4.3/§4.7, 06 glossary, brief.

### D3 — the FORECAST had no branch value

**Problem:** doubling one type's AUTO placement did not change what any ROBOT should do — the optimal AUTO target set was identical in all three branches, with a 1–2 point spread. The mechanic was a flat gift, not a branch.
**v2.0:** ROPED UP now requires **≥5 SUPPLIES including ≥2 of the PRIORITY SUPPLY and ≥1 of each other type** (was ≥4 including ≥1 of each). Four of the five are pinned by type — two of the priority type plus one of each other — and which type is doubled is unknown until T = 0, so an ALLIANCE chasing the bonus must genuinely prepare and agree three routines. Branch stake is now the +10 bonus plus the doubled value of the extra priority piece.
*Files:* spec §4, sections 01 §2.2/§2.4, 03 §4.3.4.

### D4 — ASCENT threshold

Championship **62 → 60**. At 62, an ALLIANCE whose three ROBOTS all completed a 54-in CAMP RUNG climb (3 × 20 = 60) missed the RP by two points, while one summit plus one camp plus one ledge got it on the nose. The threshold effectively required two SUMMIT RUNG climbs. Regional (32 = CAMP + LEDGE) and DCMP (52 = CAMP + CAMP + LEDGE) are unchanged and check out.

### D5 — ROPED UP could be earned in TELEOP

The AUTO settle window (T = 15.0 to 18.0) is entirely inside TELEOP under driver control. Every other provision spanning that window carried a LAST ROBOT CONTACT guard; ROPED UP did not, so an ALLIANCE could score its qualifying pieces under driver control and bank the AUTO bonus. The guard is now applied.

---

## E. Rules corrections

| # | Rule | Change | Reason |
|---|---|---|---|
| E1 | §4.1 | LAST ROBOT CONTACT defined, and keyed to **placing** contact. | Unqualified, an opponent brushing an already-SCORED AUTO piece during the settle window stripped its AUTO value and the FORECAST double, with no foul and no de-score. |
| E2 | G503 / G504 | Contact with the CRAG **structure** that shakes a piece loose is now a no-fault knock-off under G504, not a MAJOR FOUL under G503; deliberate shaking is G202 ARENA abuse. The undefined term "CRAG STRUCTURE" is gone. | v1.0 gave the identical fact pattern — a bumped CRAG — opposite outcomes in two sections, and the locked spec's own test ("contact **on the piece**") sided with G504. |
| E3 | G503 | Violation line no longer both restores a SUPPLY and forbids it from ever being SCORED again. | Those two clauses contradicted each other, and the SUPPLY LINE RP counts SCORED pieces after restoration. |
| E4 | G412 | Protection now runs **from the start of ENDGAME until climb assessment is complete**, not to the buzzer; adds a forced-position exception, caps the 5-second accrual at 3 additional MAJOR FOULS, and moves the blocked-climb award into §4.5.4 with a determinate value. | Climb assessment runs to T+5 s while G412 expired at T+0, leaving up to five unprotected seconds in which a shove was worth −27 points. The accrual was unbounded (96 points/minute) and the shove-across-the-tape play cost the aggressor nothing. |
| E5 | G415 | Lane occupancy now applies to a ROBOT **of its own ALLIANCE**; opponent rung contact is a G413 violation and does not occupy the lane. | As written, an opponent could touch a rung, "occupy" the lane, and void an ALLIANCE's own 30-point climb for the price of one foul. |
| E6 | G413 | Violation line gains a per-instance and per-5-second cadence and the blocked-climb award. | Without cadence, one continuous arm-on-rung was one foul. |
| E7 | G205 | Foul-baiting now covers pushing, carrying, or holding an opponent into a zone where mere presence is penalized, and drops the "essentially stationary" gate. | That gate was what made the shove-across-the-tape play legal. |
| E8 | G402 | Example restated in BUMPER extents rather than a single ROBOT coordinate. | The old example's ruling was false for any ROBOT wider than 24 in: a 36-in bumper footprint at X = 360 still has 6 in inside the band. |
| E9 | G403 | Adds protection for a ROBOT whose BUMPERS intersect its own CRAG APRON during AUTO. | The inner SOCKET FACE sits on the opponent's side of the centerline, so the one approach a ROBOT must make across the line was the only one with no AUTO protection at all. |
| E10 | G408 | PINNED now requires contact with "a ROBOT **other than the pinning ROBOT**"; separation reduced 10 ft → **6 ft**. | The old qualifier was always satisfied — the pinning ROBOT is itself another ROBOT — so every sustained push was a pin. 10 ft is a third of the field width to eyeball. |
| E11 | G501 | Violation line adds: SUPPLIES CONTROLLED in violation earn no points and do not count toward SUPPLY LINE. | Foul points cannot reach a bonus-RP threshold, so bulldozing eight loose SUPPLIES into the DEPOT cost 18 foul points and bought 16 points plus a third of a ranking point — rational in any decided MATCH. |
| E12 | G502 | LAUNCH no longer includes travel "across the carpet"; the DEPOT exception is restricted to the **SHELF-FACE side** of the APRON. | The old definition made ordinary depot pushing illegal, including the manual's own binding CAMP I example, while permitting a ROBOT on its PEG-FACE apron to hurl SUPPLIES over a 90-in spire. |
| E13 | G507 | Out-of-bounds SUPPLIES always return through the nearest chute. | The punitive "deliberate ejections go to the opponent's chute" rule contradicted §3.5, §4.4.4, and the locked spec. |
| E14 | G302 | Staging contact is the alliance wall (see C8). | |
| E15 | G304 / §4.2.3 | One deadline (the "field ready" signal) and one eligible declarer (a student DRIVE TEAM member). | The two texts gave different deadlines, and §4.2.3's later deadline handed whichever ALLIANCE declared second a free look at the opponent's declaration. |
| E16 | New **G307** | HUMAN PLAYER assignment: exactly two per ALLIANCE, one per OUTFITTER station, drawn from any of the three DRIVE TEAMS, fixed at "field ready." | A DRIVE TEAM was defined as containing one HUMAN PLAYER, giving three per ALLIANCE for two stations. The DRIVE TEAM definition is now 1 DRIVE COACH + up to 4 DRIVERS/OPERATORS/HUMAN PLAYERS. |
| E17 | New **G416** | Climb entry (see B6). | |
| E18 | G401 | "Behind their alliance wall starting lines" → explicit MATCH positions; E-STOP/A-STOP named. | "Starting lines" were a field marking that appears in no taping plan and on no drawing. |
| E19 | §1.4 / §4.8 | VERBAL WARNING added to the §1.4 taxonomy; the Section 5 preamble now cites §4.8 (the taxonomy) rather than §1.4; four rules capitalize the defined term. | The manual published two different taxonomies and four rules issued a level the shorter one omitted. |
| E20 | G102 / §3.5 | Both now say the same thing: HUMAN PLAYERS may break the plane of the **chute opening** and no further. | §3.5 said "the plane of the alliance wall," which the chute pierces — G102 permitted what §3.5 forbade, with a MAJOR FOUL riding on which text a referee applied. |

---

## F. Rules and sections added

| # | Addition | Why |
|---|---|---|
| F1 | **§3.1.2 FIELD LEDs** — physical specification, four states, explicit "indicators only." | G101 gated FIELD entry on an element the package never defined physically or as a term. |
| F2 | **E-STOP and A-STOP** established as driver-station equipment in §3.1, with a glossary entry each. | G401 granted permission to press a button the manual never established. |
| F3 | **§4.9 Score Finality and the Question Box.** | Three provisions hung off a post-MATCH scoring event the manual never defined, including the temporal scope of the entire G-rule set ("until scores are final") and G504's "before final scoring." |
| F4 | **§4.10 ALLIANCE Roles.** | Section 8.5 cited four archetypes that existed only in an archival concept document. |
| F5 | **§4.3.5 Designing an AUTO** and **§4.4.5 Cycle reference** — published FIELD distances. | So points-per-cycle models are built from the geometry rather than guessed, which is what the judging rubric asks for. |
| F6 | **§8.6 ARENA Faults, Stoppages, Timeouts, and Replays.** | G504 restored SUPPLIES "during a stoppage" with no rule defining one; §4.7 promised "standard tiebreaker replays per the Tournament section" that did not exist; there was no TIMEOUT rule at all. |
| F7 | **SURROGATE** and **BACKUP ROBOT** defined in §8.2 / §8.3 and the glossary. | Both were invoked normatively exactly once and defined nowhere; SURROGATE gates the primary qualification sort. |
| F8 | **BYPASSED** RP and RANKING SCORE consequence stated in §8.1. | Otherwise a team could raise its RANKING SCORE by bypassing an unfavorable draw. |
| F9 | **R206** Stored energy at MATCH start; **R207** Decorations must not imitate the FIELD. | R205 constrained only the *capability* to neutralize stored energy, never the state at T = 0. Nothing prohibited a ROBOT from carrying a 36h11 pattern, an alliance-colored ring resembling a tier ring, or a lamp resembling the SUMMIT BEACON. |
| F10 | **R706** ROBOT SIGNAL LIGHT; **R707** Operator console. | No enabled-state indicator existed in a game where ROBOTS hang at 78 in over FIELD STAFF, and OPERATOR CONSOLE was an undefined ALL-CAPS term that G206 made the sole legal channel of ROBOT interaction. |
| F11 | **R807** Pneumatics control; **R808** Closed-loop compressor control; pneumatics controllers and the Servo Power Module added to Table 6-3; the compressor added to Table 6-1. | R501 permitted only Table 6-1 actuators while R802 required a compressor that was not in it. No pneumatics controller existed anywhere in the package, and the only automatic pressure limit (R805's relief valve at "125 psi or below") was set *above* R803's 120 psi cap. |
| F12 | **§7.4 items 9 and 10** — reach proof measured from the standoff the FIELD imposes, and climb proof of the traversal. | Judged entries were previously asked for a reach dimension with no stated datum. |
| F13 | Glossary grown from 57 to **89 entries**, alphabetized, and now covering ROBOT, FIELD, BUMPER, MECHANISM, COMPONENT, COTS, FABRICATED ITEM, VENDOR, INSPECTION, HEAD REFEREE, DRIVE COACH, DRIVER/OPERATOR, FINAL, SCORING ERROR, LAST ROBOT CONTACT, SHELF/SOCKET/PEG FACE, ALLIANCE ROLE, ARENA FAULT, TIMEOUT, SURROGATE, BACKUP ROBOT, E-STOP, A-STOP, OPERATOR CONSOLE, ROBOT SIGNAL LIGHT, VERBAL WARNING, FIELD LEDs, FIELD STAFF, and GAME PIECE (as a synonym of SUPPLY). | The manual promised every ALL-CAPS term would be collected in the Glossary. A mechanical diff now returns nothing. |

---

## G. Other rules corrections

| # | Rule | Change |
|---|---|---|
| G1 | R105 | Violation line becomes an INSPECTION consequence; in-MATCH over-extension is penalized under G404 alone. Previously the same prohibition carried two different escalation tests, a 5-point swing apart. |
| G2 | R401 | "The total of all gaps … at any single gap" → "Each individual gap … must be less than 1.25 in," matching the locked spec's strict inequality. |
| G3 | R504 / R505 | Servo and ELECTRIC SOLENOID ACTUATOR power paths defined; the Servo Power Module named in Table 6-3; R505 now enumerates relay outputs and solenoids. |
| G4 | R604 / Table 6-2 | Branch protection capped at 40 A, manual-reset only, self-resetting breakers prohibited; Table 6-2 rows converted from exact values to non-overlapping ranges so every legal rating has a defined minimum wire size. |
| G5 | R605 | Wire color rule made normative, black removed from the +12 V list, and striped wire resolved by base insulation. |
| G6 | R702 | The blanket ban on wireless-capable devices replaced with a behavioral rule, since every vision coprocessor the package recommends ships with Wi-Fi silicon. |
| G7 | §7.2 | "Extend to its mechanical limit" → "drive to its commanded (software-limited) maximum reach," matching §7.4 and the brief. |
| G8 | §5.4 headings | "Movement and extension" → "Extension and contact"; a new "FIELD boundaries and HEADWALL rules" heading before G411 so no heading mislabels its contents. |
| G9 | §8.1 / §8.2 | The duplicated RP threshold table and tiebreaker list now defer to §4.7 rather than restating it. |
| G10 | Naming | Rung names normalized to LEDGE RUNG / CAMP RUNG / SUMMIT RUNG; socket, peg, shelf, and fence names normalized to title case; DEPOT sanctioned as the short form of BASE DEPOT; "slot fence" adopted over "divider". |
| G11 | §3.3.2 | "0.75 in of nominal **diametral** clearance per side" → "0.75 in of nominal **radial** clearance per side (1.50 in on diameter)." |
| G12 | HIGH CAMP | The manual now states explicitly that HIGH CAMP needs no crate, and why. The story section no longer claims every CAMP needs all three SUPPLIES. |

---

## H. Package additions

| # | File | Contents |
|---|---|---|
| H1 | `03-field/MATERIALS-AND-COLORS.md` | Material, color (with hex), finish, and section for every ARENA element and game piece; six appearance rules; a render checklist. Game pieces now have official colors — expedition violet, off-white with green caps, and amber — chosen to sit far from both alliance colors in hue so no SUPPLY can be mistaken for an alliance element. Previously the drawing set filled the CACHE CRATE in a lightened alliance blue. |
| H2 | `06-style/MANUAL-STYLE-GUIDE.md` | Page setup, palette, typography, rule anatomy, table and figure conventions, front and back matter, and a production recipe for typesetting a print-quality PDF from the Markdown sources. `06-style/_research-notes.md` holds the underlying research. |
| H3 | `02-manual/build.sh` and `02-manual/manual-header.md` | The compiled manual is now reproducible from its sections with one command. |
| H4 | `REVISION-LOG.md` | This file. |
| H5 | `_PROGRESS.md` | Working status tracker for the revision pass. |

---

## I. Verification

A cross-check script re-derives, from the documents themselves:

- every AprilTag pose in the JSON against the manual table (26 of 26),
- the 180° rotational symmetry of the tag layout,
- quaternion purity and unit norm,
- every tag-to-target transform in the vision guide,
- HEADWALL rung positions, tag-panel clearance behind plane P, and the climb-reach table,
- the CRAG tag occlusion budget,
- DEPOT channel fit and robot standoff/reach,
- socket tube clearance and CELL protrusion for all three socket types,
- the rung stagger's no-common-band property and inter-lane gaps,
- scoring ceilings by piece type and the CRAG total,
- RP threshold reachability,
- piece accounting (21 per type, 63 total),
- CENTER CACHE haul balance between alliances.

It currently reports **zero failures**. The manual's internal cross-references (89 rule IDs, 86 numbered sections) also resolve with no dangling targets, and the glossary covers every ALL-CAPS term used in the body.

---

## J. v2.1 — second-pass corrections

These changes came out of a re-audit of v2.0 itself, on the principle that the
first audit had only ever seen v1.0 and every v2.0 change was therefore
unverified.

| # | Change | Why | Files |
|---|---|---|---|
| J1 | **HIGH CAMP** requirement relaxed from *Summit Socket + **both** High Pegs* to *Summit Socket + **≥1** High Peg*. | With HIGH CAMP consuming all three high-tier positions, the Championship EXPEDITION requirement for a MID declaration (all 3 CAMPS + the full mid tier) and for a HIGH declaration (all 3 CAMPS + Summit + both High Pegs + both Mid Sockets + both Mid Pegs) reduced to the **identical 13-position set**, while HIGH paid **+35** and MID paid **+24**. HIGH strictly dominated MID at Championship tier. Freeing the second High Peg from the CAMP makes the three requirement sets distinct (LOW 12, MID 12, HIGH 11 positions) and their increments beyond the CAMPS 4 / 4 / 3, with HIGH's three being the hardest positions on the CRAG. It also makes every CAMP follow one pattern — one SCORED SUPPLY of each type the tier offers. | spec, sections 01/03/06, brief |
| J2 | **G501** violation rewritten. The clause voiding points and SUPPLY LINE credit for over-CONTROLLED SUPPLIES *for the remainder of the MATCH* was replaced by an escalation: CONTROL of four or more SUPPLIES at once, or herding SUPPLIES as a group toward a scoring location, is a **MAJOR FOUL per extra SUPPLY**. | The original consequence required referees to track individual rubber rings and cardboard crates for two minutes after a call — not callable in practice. The escalation prices bulldozing out of the game with a single count at the moment of the call: eight herded SUPPLIES is six MAJOR FOULS (48 points) against 16 points of cargo. | section 04 |
| J3 | **G502**'s launch exception re-drawn. *"CRAG APRON on the SHELF FACE side, within 36 in of the SHELF FACE or of the DEPOT's corner wraps"* → *"the portion of its own ALLIANCE's CRAG APRON that lies on the same side of the FIELD centerline as its own SHELF FACE."* | The old region was not a taped area and could not be judged from the referee platform: it measured 36 in from a curved corner wrap. Both CRAGS straddle X = 324, so the new region is the half of the APRON on the ROBOT's SHELF FACE side of the centerline — two lines the FIELD already carries, and it contains the SHELF FACE, the tray, and both corner wraps. | section 04, glossary |
| J4 | **G416** given an explicit carve-out for a ROBOT that has already been supported solely by a rung. | As written, a ROBOT that completed a legal climb and then came back down — or fell — landed on the carpet inside BASECAMP touching a rung, and lost its rung credit for the MATCH. A hanging ROBOT's BUMPERS are over BASECAMP by construction, so the same reading penalized a successful climb. The carve-out cannot be claimed by the vertical mast the rule is written against, which never leaves the carpet. | section 04 |
| J5 | **§4.5.2** two-rung case reconciled with the definition above it. The definition said "supported solely by" excludes contact with *another rung*; the next paragraph said a ROBOT on two rungs scores the lower. | Direct contradiction: under the definition a mid-traversal ROBOT scored nothing. "Another rung" removed from the exclusion list and the two-rung case restated as the one exception. | section 03 |
| J6 | **§4.5.3** assessment re-anchored to the buzzer: *"assessed when all ROBOTS are at rest, or at T+5 s after the final buzzer, whichever comes first"* → *"assessed after the final buzzer: at the instant all ROBOTS have come to rest, or at T+5 s, whichever comes first."* | "Whichever comes first" allowed assessment to fire mid-MATCH the moment all six ROBOTS happened to be stationary, locking in ENDGAME states before the ENDGAME ended. | section 03 |
| J7 | **§4.5.2** buddy-climb sentence aligned with **G413**. §4.5.2 said a ROBOT "may not be supported by a partner ROBOT"; G413 says partner support is legal but earns no rung credit. | The scoring section stated as a prohibition what the rule states as a scoring consequence. §4.5.2 now matches G413. | section 03 |
| J8 | **§4.3.5** LEAVE row corrected from "~36 in of travel" to "24 in, plus half the ROBOT's BUMPER length". | The published figure silently assumed a particular ROBOT length; LEAVE is a BUMPER test, so the distance depends on the ROBOT. | section 03 |
| J9 | Glossary **BASE DEPOT** entry corrected from a *12-in channel wrapping 12 in around both corners* to the specified **16-in channel wrapping 16 in**. | Last surviving instance of the reverted v2.0 channel value; the spec, the ARENA section, and the CAD package all read 16.0. A 13.0-in crowned CACHE CRATE cannot lie inside a 12-in channel's vertical projection, so the stale entry described a DEPOT in which no crate could be SCORED. | glossary |
| J10 | Verification suite extended with a set-theoretic model of the Championship EXPEDITION requirement: it now asserts that the three ROUTE requirement sets are pairwise distinct, that their increments beyond the CAMPS agree within one position, that every full-capacity set lies inside the CRAG's 17 positions, and that HIGH CAMP does not saturate the high tier. | J1 was a defect that no numeric check could catch, because every individual number was correct. | verification suite |
| J11 | Six text collisions in the generated drawing sheets resolved: the HEADWALL elevation's LANE / rung-length / truss-top labels, the HEADWALL plan's LEDGE / CAMP / SUMMIT labels (only 6.43 in apart at scale), the side profile's 15° callout over the tag-panel leader, the OUTFITTER plan's chute label over its own view subtitle, and the SUPPLIES sheet's crate dimension over a view scale. A bounding-box collision detector was written and added to the checks so the sheets cannot regress. | The sheets are the drawing set entrants model from; a dimension that lands on top of a label is a dimension that gets guessed. | generator, all six SVGs, verification suite |
| J12 | **R105** commentary and the CAD package corrected and expanded on socket reach. The old text read "a Low Socket rim 11.75 in *inboard* of" the FRAME PERIMETER, which does not describe a reach. | The two sockets on a SOCKET FACE are not approached from the same standoff: the Low Socket sits at −14.0 lateral, directly above the BASE DEPOT's 16-in corner wrap, so BUMPERS stop 16.75 in off the face and the rim is 11.75 in of extension away; the Mid Socket at +14.0 is clear of the wrap and is 5.0 in away. A mechanism sized for the 5.0-in case cannot reach the Low Socket, and nothing in the package said so. | section 05, section 02, CAD package, verification suite |
| J13 | CAD package gained a PEG FACE approach note: a 45° peg with 10.0 in exposed projects 7.07 in off its face, so with BUMPERS on the tower's PEG FACE the Low and Mid Peg tips reach 4.07 in inside the FRAME PERIMETER's projection, while a High Peg root — 14.0 in inboard on the spire — is 17.0 in away, the tightest horizontal reach on the CRAG. | Both facts drive end-effector and chassis geometry and neither was published. | CAD package |
| J14 | Occlusion budget corrected. The CACHE CRATE was budgeted at 12.0 in rather than its crowned 12.5, and the one SUPPLY that reaches into a CRAG tag's target band — an **O2 CELL stood on its end in the BASE DEPOT**, 14.0 in against a target bottom of 13.44 — was missing entirely. §1.3 now carries the case, the camera-height rule `h ≥ 13.44 + 0.56·D/d`, and a range table; §5.1's "SCORED pieces never occlude a tag" was false as written and is corrected; §5.2 raises the single-camera floor to 18 in; §6.8 adds the occluder to the simulation recipe. | An occlusion budget that omits a case is worse than none, because it is relied on. | vision guide, verification suite |

---

## K. v2.1 — findings from the adversarial re-audit of v2.0

A ten-auditor adversarial pass was run against v2.0 itself, each finding then
put to independent verifiers instructed to refute it. What follows is every
confirmed finding and what was done about it. Four were blockers; three of
those were introduced by the v2.0 revision.

### Blockers

| # | Change | Why |
|---|---|---|
| K1 | **G416 rewritten twice over.** The zone test became a **plane test** — the **CLIMB LINE** at X = 48 (Blue) / X = 600 (Red), across the full width of the FIELD — and the exemption for rung support became **current** rather than lifetime. | Two independent holes. (a) BASECAMP spans only Y 90–234, but lane 1's SUMMIT RUNG reaches Y 92, so a ROBOT parked beside BASECAMP at Y ≈ 75 had every BUMPER outside the zone while sitting directly under that rung, 5 in of extension from its end. (b) The J4 carve-out said "has already been supported solely by a rung **at any point in the MATCH**" — a permanent exemption bought with one brief unweighting on the LEDGE RUNG, after which the same vertical mast could take the SUMMIT RUNG straight up. Either hole reopened exactly the play B6 created the rule to close. The CAD package's climb-reach analysis had assumed the plane test all along, so the rule was the outlier. |
| K2 | **G416's trigger changed from "supported by the carpet" to BUMPER position plus rung support.** | A ROBOT that unweighted itself on the truss lower chord, or on a partner, was not "supported by the carpet" and so fell outside the rule entirely — for the price of at most one **G202** foul against a 30-point climb. |
| K3 | **Mirrored rectangles in the plan sheets anchored at the wrong edge.** `s.rect(..., fy(Y(234)), ..., SC*144)` reads correctly for Blue and, under the 180° mirror, anchors at the band's *low* Y edge and runs 144 in further down. | The Red BASECAMP, the Red HEADWALL truss band on two sheets, and both Red OUTFITTER lanes and chute openings were drawn 144 in / 36 in / 24 in south of where they belong — 54 in of several shapes hanging off the carpet — while the lane divider lines and text labels on the same sheets were drawn at the correct Y. Fixed by anchoring every mirrored rect at `min(fy(a), fy(b))`. |
| K4 | **Socket tubes drawn leaning the wrong way in both CRAG elevations.** | VIEW A and VIEW B rotated the tubes so all five sockets leaned *inward* at the open end — the opposite of the locked "tilting outward, open end up," and the opposite of details D1/D2 on the same sheet. The side-socket bottoms were drawn 11.50 in outboard instead of 4.50, the Summit Socket's 9.81 instead of 6.19. Sign flipped; the decoded values now read 4.50 and 6.19 exactly. |

### Rules and scoring

| # | Change | Why |
|---|---|---|
| K5 | **G501** priced at a **MAJOR FOUL from the first extra SUPPLY**, replacing the MINOR tier and the "four or more" threshold. | Carrying exactly three SUPPLIES was neither of the escalating conditions, so it stayed a 3-point MINOR while a third piece into a Mid Socket is worth 7, and a third PRIORITY SUPPLY into the Summit Socket in AUTO is worth 26. A three-piece hopper paid for itself every cycle. |
| K6 | **G412** — blocking or displacing a climb is now an **additional MAJOR FOUL and a YELLOW CARD**, and the 5-second accrual cap is removed. | One incursion cost the fouling ALLIANCE 8 points and cost the victim an 18-point climb downgrade plus its ASCENT RP, since §4.8 bars foul points from bonus-RP thresholds. Denying a SUMMIT climb was worth about +10 net. Removing the cap also resolves G413 being priced at twice G412 for a lesser offence. |
| K7 | **G412's forced-position exception** no longer covers a ROBOT that invited the contact, and a ROBOT of the ALLIANCE that owns the zone neither violates the rule nor triggers the exception by contacting an opponent already inside it. **G205** gains clause (c) for reverse baiting. | An opponent could stop 2 in short of the HEADWALL ZONE tape astride the lane, be pushed across it, and collect a MAJOR FOUL from the ROBOT trying to reach its own truss — with the protection running the wrong way. |
| K8 | **G403** — in the 48 × 20 in strip where the CENTER CACHE band overlaps a CRAG APRON, the cache exception governs and clause (b) does not apply. | The two halves of one sentence gave opposite rulings on the same bumper touch: no violation, or MAJOR FOUL plus a second and a YELLOW if AUTO was disrupted. |
| K9 | **G307's** per-SUPPLY taint replaced with a per-SUPPLY MINOR FOUL and removal of the person from the station; the §5 preamble now bans moving **between OUTFITTER stations**. | The taint clause was the same untrackable construction J2 removed from G501. Separately, both HUMAN PLAYERS walking to the same chute was a G307 violation that cost 3 points and doubled the feed rate at the productive chute for the rest of the MATCH. |
| K10 | **§4.3.1 fallback** now has a DRIVER/OPERATOR make the FORECAST dashboard entry, and **G401** carries the exception explicitly. | The step named the DRIVE COACH, whom the §5 preamble, the glossary, and R707 together bar from touching the OPERATOR CONSOLE at any time. |
| K11 | **§4.5.4's** blocked-climb award now names **G412 or G413**. | G413's Violation line promised the award; §4.5.4 named only G412, so a climb blocked by an opponent grasping the rung was credited nothing. |
| K12 | **PARK** row and glossary entry narrowed to HEADWALL structure *other than a rung*, and **G416** gains "a ROBOT that earns only PARK is not penalized under this rule." | The PARK row permitted contact that G416 forbade, on an identical fact pattern — the LEDGE RUNG hangs 7.8 in inside the tape, so a parking ROBOT brushes it routinely. |
| K13 | **ROPED UP** commentary corrected: **four** of the five SUPPLIES are pinned by type, not three. | With "≥2 PRIORITY and ≥1 of each other," the qualifying compositions are (2,1,2), (2,2,1) and (3,1,1) — four pieces constrained, one free. The spec carried the same miscount. |
| K14 | **§4.9** score finality gains a real backstop: 10 minutes after the final buzzer where there is no next MATCH, extendable once by announcement. | "No later than the start of the next MATCH played on that FIELD" never fires for the last MATCH of a phase, a day, or the event — leaving the whole G-rule set, the question box, and G504 restorations open-ended, since all three are scoped to "before the score is FINAL." |

### Robot rules

| # | Change | Why |
|---|---|---|
| K15 | **R805** relief valve now set **between 125 and 130 psi**; **R808** stops the compressor at **≤115 psi**. | F11 had lowered the relief setting to "120 psi or below" to sit under R803's 120 psi cap, but 120 is not under 120: a system charged to its legal maximum sat exactly at the valve's cracking pressure and would weep continuously. "Or below" with no floor also allowed a 60 psi relief valve, which makes R803's own 120 psi store unattainable. |
| K16 | **R207** rewritten: the banned block display is white **for the FORECAST** and ALLIANCE-colored **for the ROUTE**, the closing permission is qualified against one-, two-, and three-block arrangements, and the amber **R706** ROBOT SIGNAL LIGHT is expressly exempt. | The ROUTE indication is ALLIANCE-colored, not white, so the ban was written against the wrong colour while expressly permitting the lookalike. And R207's "could be mistaken for a SUPPLY" bullet, read literally against the amber ROPE COIL (`#D9A441`), failed every ROBOT that complied with R706's mandatory amber light. |
| K17 | **R707** now permits the one connection it requires — the FIELD-provided FMS connection point. | The rule required an Ethernet connection to the FMS and then forbade connection to any device outside the driver station, where §3.1 and §8.6 both place the FMS. Every legal console violated it. |
| K18 | **Inspection checklist item 9** now publishes three standoffs, not one: 19.75 in from the SHELF FACE, 19.75 in at a Low Socket and 3.0 in at a Mid Socket, 3.0 in from the PEG FACE. | See J12; the checklist repeated the single 3.0-in figure for both sockets. |

### Field CAD and drawings

| # | Change | Why |
|---|---|---|
| K19 | **Shelf gusset envelope re-datumed** to per-shelf floors: above **Z = 38.0** under Shelf 2, above **Z = 22.0** under Shelf 1 (and down to Z = 13.0 only outside the tag-panel prisms). | C10's bound was stated as an offset below the gusset's *own* shelf, but the shelf pitch is 18.0 in and a crowned CRATE standing on a shelf reaches 13.0 in above it. Shelf 2's limit computed to Z 29.5, six and a half inches inside the crate it was written to protect; Shelf 1's computed to Z 11.5, inside the tag panel. |
| K20 | **BASE DEPOT tray closed into a real U:** the two 16 × 16 in outer corner squares are now dimensioned and drawn. | The main leg and the two arms met only at two points, so the "open-topped U in plan" was three disconnected rectangles. Open-from-above area rises to four 16 × 16 in openings. |
| K21 | **VIEW D shelf footprint** was drawn 14 in *into* the tower (`K * (SHELF_DEPTH - SHELF_DEPTH)` — a botched edit evaluating to zero); now cantilevered outward over the channel. | The view contradicted its own note, detail D4 on the same sheet, and the open-to-sky check. |
| K22 | **Detail D1** now draws the bore and dimensions **ID 6.50 ± 0.125** across it. | The dimension was built from `SOCK_OD/2` endpoints and measured 6.68 in — the outside diameter. The FIELD's single toleranced dimension had no bore geometry to attach to. |
| K23 | **Rung end brackets** made an explicit exception to the ≥ 4.0 in behind-plane-P rule, confined to the outer 2.0 in of each rung. | Every rung centerline lies in plane P, so an end support must cross the band the rule reserves; §4.1 and §4.2 could not both be satisfied as written. |
| K24 | **Summit Socket support** re-specified: a mast from the tower top plate within 4.0 in of its shelf-face edge, leaning out to the tube's closed bottom, with the silhouette bound applying above Z = 62. | The (ref) envelope excluded the mast's own stated base, and the prose had the socket cantilevering off a face that ends 12 in below the rim. |
| K25 | Stale derived values corrected: **socket tube 8.0 → 7.0** in the "model these first and exactly" list; **Low Socket low point 21.40 → 22.27**; **OUTFITTER tag panel span 46.75–57.25 → 47.50–56.50** (a 9.0-in panel, not the old 10.5). | Each was a v1.0 number surviving a v2.0 change. The 21.40 figure is what an 8.0-in tube gives, and it sits 0.16 in *below* the tag target's top edge — so the occlusion paragraph refuted its own conclusion. |

### Vision

| # | Change | Why |
|---|---|---|
| K26 | **§6.6 shelf-slot "Out" sign corrected from −7.0 to +7.0** (both shelves), and the CAD package's "7.0 in inboard of the face" with it. | The shelves cantilever outward, so a slot centre is 7.0 in outboard. As published the transform put a Blue shelf goal at X = 307 — 14 in inside solid structure, and 26.75 in of extension from a compliant FRAME PERIMETER, past **R105**. The same table used the convention correctly for the Summit Socket. |
| K27 | **§4 quaternion table, 270° row** re-signed to match the stated `W = cos(yaw/2)` rule and the shipped JSON, with a note that *q* and *−q* denote the same rotation. | The row contradicted the formula printed one line above it, and §4's claim that the table and the file "match exactly" was false for four of the 26 tags. |
| K28 | **§3.2 worked example** corrected: the −Y SOCKET FACE points *into* the inter-crag corridor, toward field centre, not away from it. | The sentence teaches which face a ROBOT is looking at, and the next sentence depends on the corridor geometry. |
| K29 | **§3.7 closing commentary** no longer says every close-range tag is at 12 in. | Sixteen of the 26 tags moved to 17.5 in in C9; the subsection's own opening paragraph had been updated and its closing sentence had not. |
| K30 | Package version raised to **v2.1** across the manual cover, the specification, the CAD package, and every drawing title block. | The compiled manual's cover line read "Version 1.1," a version that existed nowhere else in the package. |

---

## L. v2.1 — the rest of the re-audit

Section K covers the blockers and the first wave. The re-audit finished with
**123 findings confirmed of 178 raised**, across 192 agents; the remainder were
refuted by their verifiers or, for four agents lost to API errors, adjudicated
by hand. What follows is everything else that was acted on.

### Field geometry and the drawing set

| # | Change | Why |
|---|---|---|
| L1 | **Rung stagger no longer alternates by lane.** Every lane now carries LEDGE −12.0 · CAMP +12.0 · SUMMIT −12.0. | Alternating the sign per lane put rungs at the same height in adjacent lanes **24 in apart centre-to-centre** — closer than two hanging ROBOTS are wide at the 120-in frame-perimeter limit — which made "all three ROBOTS can climb simultaneously with zero traffic conflict" false and an inadvertent **G415** violation the normal case. Uniform stagger puts them 48 in apart, 28 in end to end, and preserves the property the stagger exists for: no lateral position engages two successive rungs *within* a lane. |
| L2 | **Only the LEDGE RUNG is reachable from the carpet.** The climb-reach table and the **G416** commentary now state extensions to the rung centerline and add the 0.75 in a hook needs to wrap a 1.5-in rung. | The CAMP RUNG was published as "17.27 in — yes, by 0.73 in," but wrapping it needs **18.02 in**, outside **R105**. The corrected figures are LEDGE 11.59, CAMP 18.02, SUMMIT 24.45. This makes the two-handoff traversal the only route above the LEDGE RUNG, which is what the HEADWALL was designed to require. |
| L3 | **High Peg roots cross the SUMMIT BEACON lantern joint.** A 45° peg meets the spire face in an ellipse 2.12 in tall, so a root at Z = 78 spans Z 76.94–79.06 against a joint at Z = 78. Roots are now specified on a structural boss in the opaque spire with the lantern's lower edge backed opaque, and the 78-in tier ring is interrupted where they cross it. | A ROPE COIL hangs on that peg; none of its load may reach a translucent panel. |
| L4 | **The Summit Socket stands over Shelf 2's centre slot.** Published: 5.0 in of overhead clearance above a crowned CRATE there, so that slot must be loaded from the front, not dropped into. The two outer slots stay open to the sky. | The §2.4 clearance checks tested the vertical case only and never noted the plan overlap. It is the only slot on the CRAG with that restriction and entrants size grippers against it. |
| L5 | **The corner arms of the BASE DEPOT are not clear from above** — each Low Socket tube overhangs its arm, leaving clear columns of at most 6.66 in. The two outer corner squares added in K20 are the only places a CACHE CRATE or ROPE COIL can be dropped straight in. | The K20 wording claimed all four openings were clear. They are not, and the difference decides whether a DEPOT scorer needs a lateral pusher. |
| L6 | **DEPOT capacity re-derived** from "~12 pieces" to about **8 CACHE CRATES**, or about **12 SUPPLIES** mixed. | B1 made DEPOT scoring a single-layer floor-support test and nobody re-derived the capacity. Twelve crowned crates need 2028 in² against 1792 in² of tray, so the published figure was unattainable for the piece most likely to be counted. |
| L7 | **The 20-in SOCKET FACE apron is shallower than the legal reach**, and this is now published. Protection there requires engaging the rim with 15 in of extension or less; at 18 in a ROBOT's BUMPERS sit 3 in outside its own tape. | C3 justified the 20-in offset on corridor packing and never checked it against **R105**. The consequence is real and one-sided, so it is disclosed rather than papered over — changing the offset would re-break the corridor. |
| L8 | **The FIELD centerline is now taped.** | **G402** and **G502** are both presented as line calls against X = 324, which carried no marking; the nearest tape was 24 in away. |
| L9 | **The CENTER CACHE band is now in the taping plan**, with a note that its outer 20 in at each end lie inside a CRAG APRON. | §1.2 was the package's only tape specification and omitted an element three other documents draw and require. |
| L10 | Drawing corrections: VIEW B was labelled "+Y face shown" while drawing the −Y face; detail D1's toleranced **ID 6.50 ± 0.125** was built from OD endpoints and measured 6.68; the Red tag-label token swap was a one-line fragment of a three-step rotation. | Each is a drawing that says something the ledger does not. |
| L11 | Derived-value corrections: the BASECAMP clear-height table's H(24) and H(36) cells (74.2 → 74.1, 29.4 → 29.3) in both the CAD package and the generator; the tag-panel clearance formula, which evaluated to the negative of its own stated result; the ROPE COIL tilt bound (47° → 48°, exactly 47.9°) in all four places it appears; the CENTER CACHE extent against the crowned rather than nominal crate (Y 131.5–192.5, 3.5 in of apron clearance, not 4.0); and two cycle-reference distances (262 → 266, 90 → 88). | The package's own formulas are printed beside these numbers, so each was checkable and each failed. |
| L12 | Undimensioned bodies given (ref) geometry: the alliance wall and driver stations, the HEADWALL lower crossbeam and its 15° tag wedge, the tier rings' depth and which body each wraps, the DEPOT entry chamfer, and the guardrail frame section. The ledger's tag row gained the CRAG pairs' ±14.0 lateral. | §0 promises that nothing requires guessing a length or an angle. |

### Rules

| # | Change | Why |
|---|---|---|
| L13 | **G502's Violation line no longer condemns its own exception.** Escalation now excludes the LAUNCHING ALLIANCE's own APRON and its own BASE DEPOT. | The permitted DEPOT launch enters a protected zone and disturbs SCORED SUPPLIES by construction, so a referee reading the line literally had to escalate every intended use of the rule. |
| L14 | **G303** now states where a preload comes from — the ALLIANCE's OUTFITTER stock, not a staged mark. | Without it a team could preload a piece lifted off a CENTER CACHE or staging mark, leaving a staged position empty at T = 0 and breaking the 21-per-type accounting. |
| L15 | **§8.6** gained three fixes: a ROBOT hanging at a stoppage is recorded and credited; the stop/replay contradiction is resolved in favour of the Replays paragraph; and TIMEOUTS are one per Playoff bracket plus one for the Finals, replacing an undefined "series". | Each was a gap in a section added by this revision. |
| L16 | **§4.8's** taxonomy claim narrowed to in-MATCH penalties. | It claimed to cover all violations while 43 Violation lines read "ROBOT will not pass INSPECTION" and others issue BYPASSED, DISABLED, or a specific forfeiture. |
| L17 | **G407's** commentary and the spec no longer claim the whole CENTER CACHE is open defensive ground. | 40 of the band's 108 in lie inside an APRON. |
| L18 | **ROPED UP** corrected everywhere: four of the five SUPPLIES are pinned by type, not three. | The qualifying compositions are (2,1,2), (2,2,1) and (3,1,1). |
| L19 | **R805 / R808**: relief valve set between 125 and 130 psi, compressor stopping at ≤115 psi. **R703** no longer offers the compressor a power path **R807** forbids. **R707** permits the FMS connection it requires. **R207** bans the right colours and exempts the mandatory amber RSL. | Four rules that, read literally, could not be satisfied — three of them added by this revision. |

### Documents

| # | Change | Why |
|---|---|---|
| L20 | The README no longer tells organizers to publish `00-concepts/` freely: `FIRST-ASCENT.md` is the approved concept that became SUMMIT PUSH and still carries v1.0 geometry. The package map gained the four files it omitted. | The same paragraph promised that no design-relevant material releases early. |
| L21 | The style guide no longer asks for drawing sheets at the 7.00-in body measure. They go on landscape plates at ≥ 15 in of image width. | At 504 pt, `crag.svg`'s note text prints at about 2 pt. The guide's own acceptance check ("legible at 100% and at 60% zoom") was unachievable by arithmetic. |
| L22 | `_PROGRESS.md` no longer names a real robotics organization in a file whose first workstream is "de-brand", and its verification section now points at a suite that exists. | The claims it made were previously unreproducible. |
| L23 | Remaining second-person voice removed from the brief's §4.2; the BASECAMP BOT no longer scores Shelf 1, which its own description (no elevator, no extension) makes impossible; the brief's socket-angle sentence distinguishes the 15° Summit Socket from the 30° Low and Mid. | A4 claimed the second person was gone "throughout". |
| L24 | Glossary gained **CLIMB LINE**, **PLANE P**, and **DCMP**; **ALLIANCE ROLE** is now actually used in the body; **PARK** and **BASE DEPOT** re-worded to match the rules they summarize. | A defined term that appears nowhere, and a body term with no entry, are the same defect from opposite ends. |

### What was not changed

Twenty MAJOR and twenty-five MINOR findings were **refuted** by their verifiers
and no action was taken. Two of the four blockers were refuted on their own
terms but had already been fixed by the G416 rewrite that a third, confirmed
finding required, so the fix stands either way.

---

## M. v2.2 — the third pass: auditing the auditor's fixes

Sections J–L were themselves unaudited when they were written. A third
adversarial pass was run against v2.1 with eight lenses and two refuters per
finding, alongside an independent re-derivation of the balance model and a
read-only red-team of the rewritten rules. Two patterns dominate what it found,
and both are worth stating plainly because they are what a revision pass is
*for*:

1. **A fix that lands in the rule but not in every restatement of the rule is
   not a fix.** Five separate defects were the same L1 change failing to reach a
   table, a caption or a note that also published the geometry.
2. **A verification suite can report zero failures while asserting nothing.**
   Four checks in `_verify/` were tautologies, one was computed on a superseded
   dimension, and the scanner skipped the drawing set entirely.

### Blockers

| # | Change | Why |
|---|---|---|
| M1 | **G416's 5-second grace scoped to a ROBOT that has not driven since.** | The grace added in K1 was a touch-and-go loophole. A ROBOT could hang from the LEDGE RUNG with its BUMPERS on the CLIMB LINE (11.59 in of reach, legal), lower to the carpet, reverse the 23.7 in to sit under the SUMMIT RUNG, and take it on a vertical mast with **zero horizontal extension** — about 1.6 s against a 5-second window. That is verbatim the play G416 exists to prevent, reopened by the rule's own exemption. The grace now protects only what it was written for: a ROBOT that falls or lowers mid-traversal has not driven; a ROBOT that repositions has. Found by red-teaming my own v2.1 wording. |
| M2 | **The manual's §3.4 rung table still published the alternating-by-lane stagger.** Five auditors found this independently. | L1 changed the stagger to uniform in every lane and updated the spec, the CAD ledger, the generator and the prose — but not the table those paragraphs sit beside, which still read "−12.0 in (Blue lanes 1 and 3), +12.0 in (Blue lane 2)". §3's own preamble says it governs over every other document, so the stale table formally outranked the specification. A field built from it puts adjacent lanes' rungs 24 in apart centre-to-centre and 4 in end to end — the exact condition L1 removed, under which three ROBOTS cannot hang side by side and an inadvertent **G415** is the normal case. The CAD package's derived rung-end table had the same defect in its Lane-2 column. |

### The verification suite was not verifying

| # | Change | Why |
|---|---|---|
| M3 | Socket clearance checks recomputed on the **7.0-in tube**, and tightened to assert the published figures exactly (inboard edge 1.61 / 1.61 / 2.96 in; seated CELL clearing the rim's uphill lip by 4.39 / 4.39 / 5.90 in). | They were computed on the superseded **8.0-in** tube K25 corrected, and the assertions were `> 0` and `> 2.0` — loose enough that a regression back to an 8.0-in tube would have passed. The whole socket family was effectively unverified. |
| M4 | Three tautologies replaced with checks that can fail. | `abs((3.0 + 8.0) - 8.0 - 3.0) < 1e-9` is `abs(0)`, true by construction, and never touched the 5.0-in figure it was labelled with. `abs((24 + 3.0) - 14.0 - 10.0) < 1e-9 or True` was forced to PASS by the trailing `or True`, and the expression it disabled was wrong anyway. The camera-height check asserted `abs(26.88 - 26.88) < 0.05` and named a "published 27-in camera height" that appears nowhere in the vision guide; it now re-derives all five rows of §1.3's range table. |
| M5 | The rung checks now **parse the published tables** instead of re-asserting the model against itself. | Hard-coding `STAG = (-1, 1, -1)` is why the suite reported zero failures while two documents published a different stagger. It now reads the offsets out of the manual's §3.4 table and the lane spans out of the CAD package's derived table. Verified by re-injecting both defects and confirming the suite fails — a check that has never failed is not a check. |
| M6 | `consist.py` now scans the **drawing set and the generator**, not only Markdown. | It pruned `renderings/` from its walk, so no SVG was ever checked for a stale value. Extending it immediately surfaced four: the pre-L1 stagger surviving in the vision guide's HEADWALL table, the old DEPOT vocabulary in two generator strings, and a now-false "both corner wraps are open from above" note printed on the CRAG sheet. |
| M7 | The glossary-coverage check anchored on the **GLOSSARY heading** rather than on `\| **A-STOP**`, headword capture widened to qualified rows and parenthetical aliases, and morphological variants normalised. | The glossary is alphabetised ignoring punctuation, so A-STOP sits *after* ALLIANCE — anchoring there silently dropped the first five headwords. Between that, rows like "**APRON** (CRAG APRON)" that the regex could not match, and every plural counted as a miss, the check reported 61 false positives and was therefore ignored. It now reports **0**, and fails when a real entry is removed. |

### Rules

| # | Change | Why |
|---|---|---|
| M8 | **G415** occupancy redefined from *contact* to *support*. | K12 let a ROBOT that only PARKS brush a rung without penalty under G416, but G415 still made contact enough to *occupy* a lane. Since the LEDGE RUNG hangs 7.8 in inside the BASECAMP tape, a partner parking early occupied the lane and cost the teammate who then climbed it up to 30 points and the ALLIANCE's ASCENT RP — on a fact pattern the manual itself calls routine. |
| M9 | **G303** priced at a MAJOR FOUL per extra SUPPLY, with no undeclared preload SCORING or counting toward any CAMP, ROPED UP or RP. | Two preloads sit inside G501's two-SUPPLY limit, so G501 never fired and G303's 3-point MINOR governed alone — against a second PRIORITY SUPPLY worth 20 points in a Mid Socket or 26 in the Summit Socket during AUTO, plus a fifth SUPPLY toward ROPED UP that §4.8 puts beyond the reach of foul points. The same arithmetic K5 used on G501 had never been applied here. |
| M10 | **G501** gained a forced-possession carve-out. | With K5 pricing the first extra SUPPLY at a MAJOR FOUL, an opponent could shove a third SUPPLY into a ROBOT's intake and collect 8 points. |
| M11 | **R207's** closing permission narrowed to a countable block pattern. | K16's qualifier — "provided it is not arranged as one, two, or three discrete lit blocks" — read literally banned a single alliance-coloured LED bar, so the sentence that exists to permit ordinary lighting prohibited the commonest form of it, with INSPECTION failure as the consequence. |

### Geometry, drawings and documents

| # | Change | Why |
|---|---|---|
| M12 | A crowned CACHE CRATE stands **13.0 in**, not the 12.5 J14 used. Clearance to the CRAG tag target is **0.44 in**, not 0.94. | The crate rests on its bottom crown *and* carries a top crown: 0.5 + 12.0 + 0.5. The package's own arithmetic says 13.0 in four other places. Corrected in the vision guide, the CAD package, the manual, the tag-map sheet and the suite. |
| M13 | The **spec and the manual** stopped claiming no SCORED SUPPLY can occlude a tag. | K14 established the upright-O2-CELL exception and corrected the vision guide, but not the two documents that outrank it — so as published the refuted claim formally overrode the camera-height rule that answers it. |
| M14 | Five stale drawing notes corrected: the front elevation's lane-2 caption (which contradicted the line directly above it and the geometry the sheet draws), the 4.0-in inter-lane gap, D2's nominal-crate clearance and the missing mast constraint over Shelf 2's centre slot, D3's 47° coil tilt, and the RUNG DETAIL's "full hook wrap" against K23's 16-in wrappable length. | The sheets are what entrants model from. |
| M15 | The **FIELD centerline** added to the manual's markings table, the **CLIMB LINE** taped across the full field width, and the tier rings' 78-in band reconciled with its own centre height. | G402 and G502 are line calls against the centerline, which the referee-facing table did not list; G416 is a line call against a plane the tape only covered over Y 90–234; and a 1.0-in band spanning Z 77.0–78.0 is centred on 77.5, not the 78 the spec locks. The 78 ring is now explicitly hung with its top edge on the lantern joint. |
| M16 | The **ROUTE declaration EV model published**, and the false "no declaration is cheaper than another" claim removed. | The spec asserted that no ROUTE dominates without showing it, while J1 had made the incremental costs 4 / 4 / 3. Re-derived: declaring pays 53 / 55 / 61 when the declared CAMP lands and 25 / 21 / 16 when it does not, so HIGH beats LOW at p ≈ 0.79 and each declaration is optimal for a real capability profile — which is the property the uplifts were tuned for and is now demonstrated rather than asserted. |
| M17 | The BASE DEPOT's three parts given one vocabulary — **shelf-face leg**, **corner square**, **corner arm** — across 14 references, and the SCORED test stopped enumerating them. | K20 and L5 left three overlapping names for overlapping things, and the SCORED test's "including the corner wraps" under-described the channel by omitting the corner squares. "Within the vertical projection of the DEPOT channel" is complete and cannot drift again. |
| M18 | Remaining document corrections: the ALLIANCE-role parity claim its own numbers refuted, the CENTER CACHE extent against the crowned crate, the Low Socket tube's plan extent, the spec's revision line, and README/`_PROGRESS` maps that stopped at section K. | |

### Late findings, from the same pass

| # | Change | Why |
|---|---|---|
| M19 | **G412's accrual cap restored** at 3 additional MAJOR FOULS, with an exemption for a ROBOT that is DISABLED, immobile, or otherwise unable to leave under its own power. | K6 removed the cap to make climb denial unprofitable, reintroducing the unbounded case E4 had closed in v2.0. Climb denial is priced by the extra MAJOR FOUL and the YELLOW CARD, not by the accrual — so the cap costs nothing there, while uncapped it reached **64 points** across the 35-second protection window. §8.6 requires a DISABLED ROBOT to remain on the FIELD, so a ROBOT that lost a battery inside the zone handed that over with no way to avoid it. |
| M20 | **G303's Violation line** extended to cover the sourcing clause L14 added to its text. | L14 forbade taking a preload from a CENTER CACHE or staging mark, but the Violation line only ever counted *extra* SUPPLIES. A ROBOT preloading one piece lifted off a cache mark has nothing extra and nothing unsupported, so the penalty evaluated to nothing and the new clause was unenforceable — while the harm it names (a contested piece already in hand, an empty staged mark at T = 0, the 21-per-type accounting broken) was free. |
| M21 | **G416 stated identically in all five places** it appears. | §4.5.1 printed the 5-second grace without the "has not driven" qualifier — the exact version M1 had just closed, and the one G416's own commentary describes as the loophole — while §3.4 omitted the grace entirely, which reads as forfeiting rung credit for a ROBOT that falls mid-traversal. Two referees reading the two sections reached opposite calls. This is the third time the same defect shape appeared, which is why `consist.py` now checks for it structurally. |
| M22 | **PLANE P** refiled between PINNED and POSSESSION. | It had been inserted ahead of PARK in an otherwise strictly alphabetical glossary. |
| M23 | Drawing plates re-specified as landscape **ANSI C (22 × 17 in) at ≥ 20.5 in of image width**, replacing L21's 11 × 17 at ≥ 15 in. | L21 replaced one arithmetically unachievable instruction with another: its own sentence computes that a 6-pt floor needs up to 20.4 in of image width, which five of the six sheets miss at 15 in and which does not fit on a tabloid plate at any margin. ANSI C is the standard drawing-set size and the smallest that satisfies the floor, with 1.6 in to spare on the widest sheet. |
| M26 | **G416's tail re-scoped from the clock to the rung**, third and final attempt: the exemption now covers a ROBOT "still touching a rung it took hold of while so supported within the preceding 5 seconds". | M1's "has not driven" condition did not close the touch-and-go, and the reason is not obvious. Hanging from the LEDGE RUNG settles the chassis under the hook at X = 40.16, so a ROBOT at the 120-in FRAME PERIMETER limit already spans X 25.16–55.16 — which **contains the SUMMIT RUNG at X = 27.30**. It never has to drive: unweight for an instant, let the hang centre it, lower straight down, mast up with zero horizontal extension. Tying the tail to the rung fixes it cleanly. A ROBOT that falls or lowers mid-traversal is still touching a rung it had hold of, so it stays protected; a ROBOT that releases, returns to the carpet and reaches for a different rung is not; and a ROBOT with the reach to take the SUMMIT RUNG *while still hanging* is doing the legal direct climb of M25. |
| M25 | The **direct LEDGE → SUMMIT climb** documented as a legal second route, replacing three claims that the CAMP step is mandatory. | L1's uniform stagger alternates with period two, so the LEDGE and SUMMIT RUNGS share the −12.0 offset and a climber with two hook sets at one lateral position can go straight from one to the other — 48 in up, 12.86 in back, 49.69 in measured in plane P, against 24.85 in for a single traversal step. This is **unavoidable**, not a choice: a 20.0-in rung in a 48-in lane admits only two non-overlapping lateral positions, so two of the three rungs must share one. It is also a genuinely harder mechanism — twice the reach in one move — so it stands as a legitimate alternative rather than a shortcut. §3.4, inspection checklist item 10 and the HEADWALL sheet now say so instead of demanding evidence of a traversal the rules do not require. |
| M24 | The BASECAMP BOT's first graduation rung corrected from "add a wrist" to **"add a wrist, a 30-in lift, and about 12 in of extension"**, with the Low Socket standoff published alongside it. | The reference design is a fixed-height claw with no lift and no extension, so a wrist supplies neither of the two things a Low Socket needs. The rookie-facing ladder also omitted the J12/K18 fact the package went to trouble to establish: the DEPOT's corner arm holds BUMPERS 16.75 in off the SOCKET FACE, making that rim 11.75 in of extension away rather than the Mid Socket's 5.0. |

### From the completeness critic

The audit's last stage asked one agent what the eight lenses had missed. It found
thirteen more, and the pattern it named is the one section M opens with: **the pass
that identified "a fix that lands in the rule but not in every restatement" committed
that error four more times while fixing it.**

| # | Change | Why |
|---|---|---|
| M27 | The **K23 rung-bracket exception** carried into DESIGN-SPEC §3 and manual §3.4. | It had reached the CAD package, the glossary and the drawing sheet, but not the two documents that outrank them — both of which still said flatly "all truss structure ≥ 4.0 in behind plane P", and the manual added the affirmatively false consequence "so every rung offers full hook wrap". Wrap is clear over 16.0 in of a 20.0-in rung. A hook placed within 2 in of a rung end collides with a bracket the governing text says is not there. |
| M28 | The **CLIMB LINE added to the manual's markings table**. | M15 taped it in the CAD package and the render checklist. The manual — whose §3 is "the authoritative physical description of the ARENA" and whose §3.2 opens "all zone boundaries are marked with tape" — described the CLIMB LINE only ever as a *plane*, never as a marking. A field built from the governing document has no tape at X = 48 outside Y 90–234, which is exactly the strip M15 was written for. |
| M29 | **G413** given M19's cap and immobility exemption. | M19 fixed G412 and left its sibling untouched, re-creating the pricing inversion K6 had cited as its reason for removing the cap: the lesser offence now carried the larger accrual, uncapped, and G413 is not even scoped to the ENDGAME. |
| M30 | **Sheet 1's tape key** completed from four markings to six, the CLIMB LINE drawn dashed outside BASECAMP, and X = 324 redrawn as white tape broken at the CRAG footprints. | Drawing 1 of 6 is the sheet a field is taped from, and it omitted the two markings most recently added — the two that carry rule calls. What it drew at X = 324 was a muted dash-dot *construction* line, unbroken, in the wrong colour. A builder taping from sheet 1 laid neither line. |
| M31 | The **ROUTE EV crossover corrected** from a bare "p = 0.79" to both figures with their conditions. | M16's own formulas (25 + 28p, 21 + 34p, 16 + 45p) cross at p = 9/17 ≈ 0.53 and p = 5/11 ≈ 0.45 at *equal* probability. The published 0.79 silently froze p at 0.95 for CAMP I while varying it for HIGH CAMP — a different and more realistic question, but not the one the printed derivation asks. Both are now stated with what they assume. The "strong" profile was also an exact tie at 51.60, so MID never strictly won in any published row; it is now .92 / .90 / .55, where it wins outright. |
| M32 | The **camera-height rule re-solved against the domed cap**. | K14's rule modelled the upright O2 CELL as a point at its 14.0-in apex. The caps are 1.5-in domes, and the sight line grazes the **flank nearer the face**, not the apex — so the rule understated the required height by up to 5 in and every range in the table was 20–25% optimistic. Corrected: a camera at 20 in clears to 22 in, not 29; at 30 in to 56, not 74. The apex form survives only as an explicitly-labelled optimistic lower bound. |
| M33 | Two more checks in the suite that could not fail: the **CAMP row's sign test** accepted either sign (stripping '+' from '+12.0' leaves '12.0', a substring of a minus-signed cell — so flipping the one row the whole stagger property depends on left the suite green), and the **stale-term scan was case-sensitive**, missing a CRITICAL ledger row still labelled "Corner wraps". Both fixed and both re-proved by injecting the regression. |
| M34 | The **HEADWALL crossbeam, wedge and tag panel** no longer occupy the same volume. | L12's three (ref) bodies interfered: the beam's field-side face at X = 40.64 against a panel back at X = 38.75 and a wedge filling the space between them. The wedge thicknesses were self-consistent, which is what proved it — they were computed against the clearance *surface*, then attributed to the front face of a 2-in-deep beam. The beam is now notched at the three lane-tag stations. |
| M35 | Remaining: the manual's centerline tape no longer breaks for trays that stop 8 in short of it, and the ledger row label follows the M17 vocabulary. | |

### Closing sweep

| # | Change | Why |
|---|---|---|
| M36 | **Shelf 1's gusset floor raised to Z = 19.0** and the DEPOT loading clearance restated as "23.25 in to the Shelf 1 underside, and not less than 19.0 in anywhere a gusset descends". | The rule contradicted itself: it permitted a descent to Z = 13.0 "outside the tag prisms" and then required Z ≥ 13.5 "wherever the DEPOT channel runs beneath" — but Shelf 1's whole footprint (Blue X 286–300) sits inside the 16-in channel (X 284–300), so the second clause applied everywhere and the first was dead text. Separately, §3 published a flat 23.25 in of loading clearance that any legal gusset reduced. At Z = 19.0 a crowned 13.0-in CACHE CRATE passes with 6.0 in to spare and the gusset still has 4.25 in of depth. An audit verifier had refuted this finding by answering a narrower question than it asked. |
| M37 | **G416 and its four restatements unified on one phrasing** ("a rung it took hold of while so supported"). | The rule said "contacted while so supported" while every restatement said "took hold of". Identical in meaning, but this rule has been mis-restated three times already, and the restatement check keys on the phrase. |
| M38 | Bare **CRATE** spelled as the defined term **CACHE CRATE**. | §9 requires defined terms in full; two of the three instances were introduced by this pass's own edits. |
| M39 | **`crossdoc.py` added as a fifth check**, and the stale-value scan made case-insensitive. | `consist.py` asks whether a superseded value survives. Nothing asked the opposite question — whether a value that must appear in several documents actually appears in all of them. A fix applied correctly in one place and never written in another leaves no stale text to find; the absence reads as clean. The new check caught two on its first run. The case-sensitivity fix was one the audit had raised and whose patch had silently aborted on an earlier assertion — a CRITICAL ledger row labelled "Corner wraps" had been sailing past a scan written to catch exactly it. |

### From the first CAD build

The CACHE CRATE was modelled in Onshape: 12-in cube, 0.5-in pillow from the centre
of each face, 1.0-in fillets on all twelve edges. That matches §9.1 exactly, and
building it surfaced one defect the drawings had carried since v1.0.

| # | Change | Why |
|---|---|---|
| M40 | **Shelf-slot clearance re-derived against the crown**, replacing the nominal-cube figure. | §9.1 and the SUPPLIES sheet both published "1.0 in of clearance per side" from the 12.0-in nominal cube. A CRATE rests on its bottom crown, so the cube's bottom plane sits 0.5 in above the shelf and each side face reaches its full 0.5-in bulge **6.5 in** up. The binding width is at the top of the 2.0-in fences, where the crate is **12.44 in** across — **0.78 in per side**, a 22% smaller placement tolerance than published, and the number a scoring mechanism is actually designed against. The 13.0-in crown sits 4.5 in above the fences and touches nothing; crates in adjacent slots clear each other by 2.5 in. Now in the CAD package, the manual's §3.3.1, the brief's architecture section and the drawing sheet, with the crown profile locked into the verification suite. |
| M41 | The **1.0-in edge fillets** given their consequence rather than just their dimension. | They remove material at the edges, so the 13.0-in envelope is unchanged — but they are what lets a CRATE roll up over the 4-in BASE DEPOT lip when pushed, which is the mechanism the BASECAMP BOT reference design depends on, and what stops a corner catching on the OUTFITTER chute. |

| M42 | **O2 CELL as built**: the R1.0 cap/body fillet recorded, the `#4D4D4D` fillet band added to the palette, the full-diameter body corrected from 11.0 to **10.44 in**, and the camera-height table re-solved. | The cap arc is struck through the pole and the equator, so it meets the cylinder at a **28.1° tangent break** — the fillet is structural to the shape, not cosmetic, and it moves the shoulder inboard: the 11.0 in the sketch is the arc-endpoint dimension, not the full-diameter length. It also changes the silhouette the CRAG-tag occlusion rule is solved against: a CELL standing on end now reaches Z = 12.22 where it touches the face rather than the 12.5 a bare dome gives, so every published camera range grows about 10–15% (at 20 in, 24 in of range rather than 22). The old figures were conservative, which is the safe direction, but they described a part that was never built. |
| M43 | **ROPE COIL confirmed to spec, and its construction recorded.** | All three published numbers reproduce from the single revolve: a 2.5-dia profile circle whose outer edge is 5.0 from the axis puts its centre at r = 3.75, giving OD 10.0, ID 5.0 and a 2.5 tube. The derived 47.87° tilt bound reproduces too. The suite now derives OD and ID from the profile rather than asserting them separately, and §2.5 states the **2.9° margin** between that bound and the 45° a vertical hang needs — the number that makes a 45° peg capture a coil rather than let it balance. Nothing needed changing. |

| M44 | **BASE DEPOT as built.** Plan confirmed exactly (48-in notch + two 16-in arms = the 80-in outer run). Recorded: **tray floor top at Z = 0.25** above the carpet, lip top 4.0 above the carpet and therefore **3.75 above the floor**, R0.25 on every outside face, and `depot` re-coloured **#7F7F7F** from #B8A888. | The package had the tray floor "flush-shimmed to carpet" and every occlusion figure assumed SUPPLIES rest at Z = 0. A tray laid on the carpet stands everything in it 0.25 in higher, which propagates: a crowned CACHE CRATE now apexes at **13.25** against a 13.4375 target bottom (**0.19 in**, down from 0.44), an upright O2 CELL at **14.25** (0.81 into the band, up from 0.56), and every camera range in VISION-GUIDE §1.3 loses about a third — at 20 in, 15 in of range rather than 24. The D4 depot section was drawing the CRATE resting at Z = 0 and 12.0 tall; it now sits on the floor at its crowned 13.0. |
| M45 | **Open decision recorded, not silently absorbed:** the 0.19-in CRATE-to-tag margin is smaller than the panel's own build tolerance. | A field built 0.2 in low would let a CRATE clip the bottom of tags 6/7 and 19/20. The panel cannot simply be raised — a 9.0-in panel centred at 17.75 puts its top edge at 22.25 against the Low Socket tube's 22.27. §1.3 now carries both ways out: shrink the panel to **8.5 in and raise the centre to 17.75**, which holds the top edge at 22.00 so every upper clearance is unchanged and restores **0.44 in** of margin at the cost of white surround (0.4375 → 0.1875 per side); or keep 9.0 at 17.5 and state the panel height tolerance as **±0.15 in**. The package publishes the second, because it is what the current geometry gives. This is a design decision, so it is flagged rather than made. |

### Also fixed, from the deferred queue

All twelve style-guide findings the second audit confirmed and this pass had
deferred: the `attr()` that cannot resolve in a page-margin box, the footer
string the specified mechanism cannot produce, the full-bleed band on a page
declared to need no bleed, the 60-vs-148-page contradiction, the alignment-row
claim that no table satisfies, five contrast ratios that do not recompute, the
italic-versus-bold rule headline, the production recipe's unshipped files, and
the drawing sheets specified at a measure where their type sets at 2 pt.
