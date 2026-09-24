# tech-standards

## KEY TAKEAWAYS
- Control system core is identical both seasons: 1 NI roboRIO/roboRIO 2.0 (am3000/am3000a) with year-stamped image (2025_v2.0 / 2026_v1.2), 1 Vivid-Hosting VH-109 radio (7.0 Mbit/s cap), 120A main breaker, 6 AWG main wire with Anderson SB connector, and one 12V SLA battery (17-18.2 Ah, 7.1x3.0x6.6 in).
- Power distribution: CTRE PDP/PDP 2.0 or REV PDH in 2025; 2026 adds the AndyMark AMPD (am-5754). Legal motors span Kraken X60/X44, Falcon 500, Minion, NEO/NEO Vortex/NEO 550, CIM/Mini-CIM/BAG/775 variants, Venom; controllers include Talon FX/FXS/SRX, Spark MAX/Flex, Thrifty Nova, Koors40.
- A defining modern rule: R502 caps robots at 4 propulsion motors (new in 2025, kept in 2026).
- 2026 REBUILT dramatically shrank robots vs 2025: perimeter 120in -> 110in, starting height 3ft6in -> 30in with a hard 30.0in height cap at all times (R107, no listed climb exception), extension 18in -> 12in and only over one side at a time (R106). Weight unchanged: 115 lb (135 lb with bumpers).
- Bumper regime (reworked for 2025, carried to 2026): full-perimeter coverage with <1.25in gaps allowed, 2.25in-deep x 4.5in-tall foam, floor-referenced BUMPER ZONE 2.5-5.75in, max 4in beyond perimeter, filled corners, no wedges, red/blue covers with white 3.75in-tall team numbers in 3+ locations; 2026's only notable change is allowing one larger coverage gap with 5.0in protected on each side.
- AprilTags: family 36h11 since 2024, 6.5in tag body printed on an 8.125in-square target mounted on a 10.5in polycarbonate panel. Counts: 16 tags (IDs 1-16) in 2024, 22 (IDs 1-22) in 2025, 32 (IDs 1-32) in 2026; 2025 heights ranged from 6.875in (REEF) to 5ft9in (BARGE).
- WPILib conventions: NWU axes (X forward, Y left, Z up, CCW positive) and the 'Always Blue Origin' field frame (+X away from the blue alliance wall), with an official per-season AprilTag field-layout JSON.
- Field: nominally 27ft x 54ft carpet (2025 actual 26ft5in x 57ft6.875in; 2026 back to ~26.5ft x 54.3ft), 20in polycarb guardrails with four 38in gates, and alliance walls of 3 driver stations (36.8in diamond-plate base + 42in polycarb, 69in x 12.25in shelf, E-stop and A-stop).
- Manual skeleton (identical 2025/2026): 15 sections — Introduction, FIRST Season Overview, Game Sponsor Recognition, Game Overview, ARENA, Game Details, Game Rules (G), ROBOT Construction Rules (R), Inspection & Eligibility (I), Tournaments (T), District/Regional/Championship, Event Rules (E), Glossary.
- Numbering conventions: prefix letter + 3 digits with first digit = subsection (R4xx bumpers, R5xx motors, R6xx power, R7xx control, R8xx pneumatics), lettered sub-parts A/B/C, ALL-CAPS glossary terms, asterisked green 'evergreen' rules, and per-rule 'Violation:' lines using VERBAL WARNING / MINOR FOUL (+2) / MAJOR FOUL (+6) / YELLOW / RED CARD.
- Match timing: 2025 = 0:15 AUTO + 2:15 TELEOP; 2026 = 0:20 AUTO + 2:20 teleop split into a 10s TRANSITION SHIFT plus four 25s alliance SHIFTS (hub activation alternates via game data), last 30s = ENDGAME.
- Pneumatics (stable): one onboard compressor <=1.1 cfm @ 12VDC, stored <=120 psi, working <=60 psi behind a single relieving regulator, 1/8in NPT max solenoids, 1/4in OD max tubing.

## REPORT
# FRC Technical Standards Research: 2025 REEFSCAPE and 2026 REBUILT

Research compiled from the official FIRST game manuals (firstfrc.blob.core.windows.net mirrors), FRCManual.com (a faithful HTML mirror of the official manuals), WPILib documentation, and Chief Delphi community discussion. All rule numbers below were verified against 2025 and/or 2026 manual text.

## 1. Legal Control System Components (R-rules)

FRC robot construction rules use a subsection-based numbering scheme that has been stable since the 2023 manual restructure: **R1xx** = size/weight/general, **R2xx** = safety/materials, **R3xx** = budget/fabrication, **R4xx** = BUMPERS, **R5xx** = motors/actuators, **R6xx** = power distribution, **R7xx** = control/signal system, **R8xx** = pneumatics.

### Controller, radio, and communication
- **roboRIO (R701 in both 2025 and 2026):** "ROBOTS must be controlled via 1 programmable NI roboRIO or roboRIO 2.0 (P/N am3000 or am3000a, both versions referred to throughout this manual as 'roboRIO')." Image version requirements are year-stamped: **2025_v2.0 or later** (REEFSCAPE), **2026_v1.2 or later** (REBUILT). Source: [2025 manual R701](https://www.frcmanual.com/2025/robot-construction-rules-(r)), [2026 manual R701](https://www.frcmanual.com/2026/robot-construction-rules-(r)).
- **Radio (R702):** Exactly **1 Vivid-Hosting wireless bridge, P/N VH-109** (also sold as WCP-1538), "the only permitted device for communicating to and from the ROBOT during the MATCH," configured with an encryption key tied to the team number. Events in China still use the legacy OpenMesh OM5P-AN/OM5P-AC. R703 governs the roboRIO-to-radio Ethernet port connection; **R704** caps bandwidth at **7.0 Mbit/s for the VH-109** (4.0 Mbit/s for OpenMesh).

### Power distribution
- **Battery (R601):** Exactly **one non-spillable 12 V sealed lead-acid (SLA) battery**; nominal capacity at the 20-hour rate **minimum 17 Ah, maximum 18.2 Ah**; dimensions **7.1 in × 3.0 in × 6.6 in (±0.1 in)**. Named examples: Enersys NP18-12 / NP18-12B / NP18-12BFR, MK Battery ES17-12, Yuasa NP18-12B.
- **Main circuit (R609):** ≥**6 AWG copper wire**, a **single pair of Anderson Power Products 2-pole SB-type connectors**, and a **single 120 A main breaker** (Cooper Bussmann CB185-120 / CB285-120 or Optifuse 153120 / 253120), feeding **one power distribution device**: in 2025, CTR Electronics **PDP (am-2856)**, **PDP 2.0 (24-806880)**, or REV Robotics **PDH (REV-11-1850)**; **2026 adds the AndyMark AMPD (am-5754)** to that list.

### Legal motors (R501, "Allowable motors")
Cross-year list (2025 and 2026 substantially identical): AndyMark **9015, NeveRest, PG, RedLine, Snow Blower**; Banebots **RS775/RS550** variants; **CIM**; CTR Electronics **Minion** and **Falcon 500**; KOP automotive motors (**Denso, Bosch, Johnson Electric**); Playing With Fusion **Venom** (integrated controller); REV Robotics **HD Hex, NEO Brushless (NEO), NEO 550, NEO Vortex**; VEX **BAG** and **Mini-CIM**; West Coast Products **Kraken X60, Kraken X44** (Kraken X44 and Minion were added to the 2025 list mid-season via Team Updates), and **RS775 Pro**. 2025 also lists the **Nidec Dynamo BLDC**; 2026 adds the **Thrifty Pulsar 775**. Blanket allowances in both years: cooling fans ≤120 mm and ≤10 W @ 12 VDC; PWM COTS servos with **stall current ≤4 A and output power ≤8 W @ 6 V**; one compressor; COTS linear actuators/solenoids/electromagnets. Note: the venerable 775pro appears in the tables under its vendor names (Banebots RS775 / WCP RS775 Pro).
- **R502 (notable, introduced for 2025 and retained in 2026):** "A ROBOT may not have more than **4 propulsion motors**." This effectively outlaws 6-CIM-style drivetrains and 8-motor swerve overkill and is a distinctive modern-era rule a mock manual should mirror.

### Legal motor controllers (R504)
2025 list: DMC 60/DMC 60c, Jaguar (PWM only), **Koors40 (am-5600)**, Nidec Dynamo (integral), SD540 variants, **Spark (REV-11-1200), Spark MAX (REV-11-2158), Spark Flex (REV-11-2159)**, **Talon (legacy), Talon SRX (217-8080), Talon FX (217-6515, 19-708850), Talon FXS (24-708883)**, **Thrifty Nova (TTB-0100)**, **Venom (BDC-10001, integral)**, Victor 884/888/SP/SPX. The 2026 list is trimmed to the modern set (Koors40, Spark family, Talon family including Talon FXS, Thrifty Nova, Venom, Victor SP/SPX) — the legacy DMC60/Jaguar/SD540/Victor 884 entries do not appear in the 2026 table as rendered on FRCManual.com. Relay-class devices legal in both years: **Spike H-Bridge (217-0220)**, Automation Direct relays, and **REV PDH switched channels** (non-actuator loads only). CAN motor controllers are legal provided **all commands originate from the roboRIO**.

### Pneumatics (R8xx)
Stable across both seasons: compressed air must come from **one onboard compressor** rated **≤ nominal 1.1 cfm @ 12 VDC** (R806); **stored pressure ≤120 psi** (R807); **working pressure ≤60 psi**, downstream of a **single primary adjustable relieving regulator** (R808). R804 permits solenoid valves (max ⅛ in NPT), tubing (max ¼ in OD), pressure vent plugs, relief valves, transducers/gauges, cylinders, and storage tanks (2026 explicitly bans the white Clippard AVT-PP-41 tank).

## 2. Robot Constraint Conventions — and the big 2025→2026 shift

| Constraint | 2025 REEFSCAPE | 2026 REBUILT |
|---|---|---|
| Weight (less bumpers & battery) | ≤115 lb (R103) | ≤115 lb (R103) |
| Weight with bumpers (R408) | ≤135 lb | ≤135 lb |
| Starting-config perimeter (R104) | ≤120 in | **≤110 in** |
| Starting-config height (R104) | ≤3 ft 6 in | **≤30 in** |
| Horizontal extension (R105) | ≤1 ft 6 in beyond perimeter | **≤12 in**, and (R106) **only over one side at a time** |
| In-match height | no global cap (robots reached 6+ ft for L4/deep cage) | **R107: total height may never exceed 30.0 in** — no climbing exception listed |

Sources: [2025 R-rules](https://www.frcmanual.com/2025/robot-construction-rules-(r)), [2026 R-rules](https://www.frcmanual.com/2026/robot-construction-rules-(r)); the 110-inch perimeter is corroborated by Chief Delphi ("[110' vs 110\" perimeter](https://www.chiefdelphi.com/t/110-vs-110-perimeter/521817)").

**Frame perimeter convention (R101/R102):** the ROBOT PERIMETER is "comprised of fixed, non-articulated structural elements," established in STARTING CONFIGURATION, and measured by "wrap[ping] a piece of string around the outer most parts of the ROBOT (excluding BUMPERS) at the BUMPER ZONE… and pull it taut" (2025 R102). Minor protrusions (bolt heads, rivets) are excluded.

**Bumper rules (R4xx) — 2025 rework carried into 2026:** The major bumper overhaul happened 2024→2025 (see CD thread "[2025 Bumper Rules Changes](https://www.chiefdelphi.com/t/2025-bumper-rules-changes/478756)"): the BUMPER ZONE became floor-referenced and full-perimeter coverage became mandatory. 2026 carries the same regime with only a coverage-gap tweak. Verified specifics (rule numbers valid both years):
- **R401:** bumpers must protect the **entire ROBOT PERIMETER**; gaps **<1.25 in** between adjacent segments are permitted (corners must still be filled per R406). 2026 additionally allows **one larger gap** if at least **5.0 in** of perimeter on each side of it remains protected.
- **R402:** construction = **≥2.25 in depth of foam padding, ≥4.5 in tall** (pool noodles; polyethylene 1.5–3.0 lb/ft³; EVA 2.0–6.0 lb/ft³; foam floor tiles), a wood/plywood-style backing ≥4.5 in tall, a cloth cover, and a rigid fastening system.
- **R403:** bumpers extend **≤4.0 in** from the ROBOT PERIMETER. **R404:** hard parts ≤1.25 in from the perimeter; padding must extend ≥2.0 in beyond any hard part.
- **R405:** padding must **entirely fill the BUMPER ZONE, 2.5 in to 5.75 in from the floor** — this floor-referenced zone is the signature modern bumper convention.
- **R406:** corners filled with uncompressed padding ≥2.25 in from the corner, no voids. **R407:** no wedge geometry. **R409:** non-articulated. **R410:** removable for inspection/weighing.
- **R411/R412:** must display **red or blue** to match alliance, with team numbers in **white Arabic numerals ≥3.75 in tall, ≥0.5 in stroke**, visible in **≥3 locations approximately 90° apart**.

## 3. AprilTag Standard

- **Family:** **36h11** since 2024 (2023 used 16h5). Per [WPILib's AprilTag introduction](https://docs.wpilib.org/en/stable/docs/software/vision-processing/apriltag/apriltag-intro.html): "Starting from 2024, FIRST has chosen the 36h11 family," and tags are "printed such that the tag's main 'body' is **6.5 inches** in length."
- **Physical target:** the printed target sheet is **8.125 in (8⅛ in) square** (the 6.5-in tag body plus white margin), mounted centered on a **10.5 in square polycarbonate panel**. This 6.5-in body / 8.125-in sheet / 10.5-in panel stack is consistent in the 2024, 2025, and 2026 field drawings.
- **2024 CRESCENDO:** **16 tags, IDs 1–16**. SOURCE tags 1, 2, 9, 10 on the source walls; AMP and SPEAKER tags mid-field-wall; STAGE tags 11–16 centered on the three wide faces of each STAGE core at **3 ft 11½ in** above carpet. Source: [2024 AprilTag Images and User Guide](https://firstfrc.blob.core.windows.net/frc2024/FieldAssets/Apriltag_Images_and_User_Guide.pdf), [FRCManual 2024 ARENA](https://www.frcmanual.com/2024/arena).
- **2025 REEFSCAPE:** **22 tags, IDs 1–22** ([FRCManual 2025 ARENA](https://www.frcmanual.com/2025/arena)). Mounting heights (to tag center-ish, per manual): **CORAL STATION tags 1, 2, 12, 13 at 4 ft 5¼ in**; **PROCESSOR tags 3, 16 at 3 ft 9⅞ in**; **BARGE tags 4, 5, 14, 15 at 5 ft 9 in**; **REEF tags 6–11 and 17–22 at just 6⅞ in** above the carpet (one per reef face — the famously low tags used for auto-align scoring).
- **2026 REBUILT:** **32 tags, IDs 1–32** ([FRCManual 2026 ARENA](https://www.frcmanual.com/2026/arena)): 16 HUB tags at **44.25 in**, 4 TOWER-wall tags and 4 OUTPOST tags at **21.75 in**, 8 TRENCH tags at **35 in**.
- **Coordinate conventions** ([WPILib coordinate system docs](https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html)): WPILib uses **NWU axes** (X forward, Y left, Z up; counter-clockwise positive). The dominant field convention is **"Always Blue Origin"**: origin fixed at the blue-alliance corner, +X pointing away from the blue alliance wall — preferred because "AprilTags throughout the field are unique," so no alliance-flip transform is needed for pose estimation. WPILib ships an official AprilTag field-layout JSON (tag ID → 3D pose) each season.

## 4. Standard Field Conventions

The colloquial "27 ft × 54 ft" field is nominal; the manuals give exact figures:
- **2025:** carpet playing surface ≈ **26 ft 5 in × 57 ft 6⅞ in** (REEFSCAPE ran long). **2026:** ≈ **317.7 in × 651.2 in** (~26.5 ft × ~54.3 ft), back to the classic ~54-ft length.
- **Guardrails:** transparent polycarbonate on aluminum extrusion along the long edges — **1 ft 8 in (20.0 in) tall**, with **four access gates, 38 in (3 ft 2 in) wide** when open.
- **Alliance walls / driver stations:** each alliance wall holds **three DRIVER STATIONS**; each station is a **~36.8-in (3 ft ¾ in) tall diamond-plate base topped by a 42-in (3 ft 6 in) transparent polycarbonate sheet**, with an aluminum operator-console shelf **69 in (5 ft 9 in) wide × 12.25 in deep**, plus an **E-stop button, A-stop button (autonomous stop, standard since 2024), Ethernet drop, power outlet, team sign, and LED status indicators**. Sources: [2025 ARENA](https://www.frcmanual.com/2025/arena), [2026 ARENA](https://www.frcmanual.com/2026/arena).
- Carpet is low-pile, edges/seams secured with gaffers tape.

## 5. Game Manual Structure and Rule-Numbering Conventions

Both the [2025](https://www.frcmanual.com/2025) and [2026](https://www.frcmanual.com/2026) manuals use the identical 15-section skeleton:
1. Introduction — 2. FIRST Season Overview — 3. Game Sponsor Recognition — 4. Game Overview — 5. ARENA — 6. Game Details — 7. Game Rules (**G**) — 8. ROBOT Construction Rules (**R**) — 9. Inspection & Eligibility (**I**) — 10. Tournaments (**T**) — 11. District Tournaments — 12. Regional Tournaments — 13. FIRST Championship Tournament (**C**) — 14. Event Rules (**E**) — 15. Glossary.

Conventions a mock manual should replicate:
- **Rule IDs** = letter prefix + 3-digit number; **first digit = subsection** (G4xx = section 7.4, R6xx = section 8.6, etc.). Sub-requirements use capital letters (A, B, C…) and roman numerals below that. Rules carry a bold headline (e.g., "R104 *STARTING CONFIGURATION – max size*") followed by rule text, blue-box examples, and non-binding gray commentary boxes.
- **Evergreen rules** (stable year to year) are marked with an asterisk and green text; season-specific rules are blue.
- **Defined terms** are SMALL-CAPS/ALL-CAPS glossary words (ROBOT, MATCH, BUMPER ZONE, STARTING CONFIGURATION, MOMENTARY).
- **Violation taxonomy** (2025 Table 6-3, retained 2026): **VERBAL WARNING**, **MINOR FOUL** (+2 points to opponent), **MAJOR FOUL** (+6 points), **YELLOW CARD**, **RED CARD** (disqualification); second yellow becomes red. (Pre-2025 these were FOUL/TECH FOUL — the MINOR/MAJOR renaming is a current-era marker.) Each G-rule ends with a "Violation:" line naming its penalty.
- **Match structure:** 2025 = **AUTO 0:15 + TELEOP 2:15** (2:30 total). 2026 REBUILT = **AUTO 0:20**, then a **2:20 teleop** subdivided into a **10-s TRANSITION SHIFT + four 25-s alliance SHIFTS** (hub activation alternating by game data) with the final **30 s as ENDGAME**, 2:40 total — plus a post-AUTO 3-s scoring-assessment window. Sources: [2025 manual HTML](https://firstfrc.blob.core.windows.net/frc2025/Manual/HTML/2025GameManual.htm), [2026 game details](https://www.frcmanual.com/2026/game-details), [WPILib 2026 game data](https://docs.wpilib.org/en/stable/docs/yearly-overview/2026-game-data.html).
- 2026 game specifics for flavor: game piece = **FUEL** (504 staged per match; up to 8 preloaded per robot; 24 per DEPOT, 24 per OUTPOST chute), HUB scoring **1 pt/FUEL when active**, TOWER climb **L1 = 15 pts (AUTO, max 2 robots), L2 = 20, L3 = 30**, one climb level per robot in TELEOP.

### Caveats
- FRCManual.com is an unofficial but faithful mirror; the authoritative texts are the season PDFs at firstfrc.blob.core.windows.net (2026 manual current at TU22). Chief Delphi threads corroborated the surprising 2026 numbers (110-in perimeter, 30-in hard height cap).
- The 2026 motor-controller table omitting legacy controllers (Jaguar, DMC60, SD540, Victor 884/888) is based on the mirror's rendering; treat as high-confidence but worth a spot check against the official PDF if exact 2026 legality of legacy controllers matters.
