# FRC Technical Standards, 2025–2026

## Key takeaways
- The control system core is the same in both seasons: 1 NI roboRIO/roboRIO 2.0 (am3000/am3000a) with a year-stamped image (2025_v2.0 / 2026_v1.2), 1 Vivid-Hosting VH-109 radio (7.0 Mbit/s cap), a 120A main breaker, 6 AWG main wire with an Anderson SB connector, and one 12V SLA battery (17-18.2 Ah, 7.1x3.0x6.6 in).
- Power distribution: CTRE PDP/PDP 2.0 or REV PDH in 2025; 2026 adds the AndyMark AMPD (am-5754). Legal motors include Kraken X60/X44, Falcon 500, Minion, NEO/NEO Vortex/NEO 550, CIM/Mini-CIM/BAG/775 variants and Venom; controllers include Talon FX/FXS/SRX, Spark MAX/Flex, Thrifty Nova and Koors40.
- A distinctive modern rule: R502 caps robots at 4 propulsion motors (new in 2025, kept in 2026).
- 2026 REBUILT robots are much smaller than 2025 robots: perimeter 120in -> 110in, starting height 3ft6in -> 30in with a hard 30.0in height cap at all times (R107, no climb exception listed), and extension 18in -> 12in, over only one side at a time (R106). Weight is unchanged: 115 lb (135 lb with bumpers).
- Bumper regime (reworked for 2025, carried into 2026): full-perimeter coverage with gaps <1.25in allowed, 2.25in-deep x 4.5in-tall foam, a floor-referenced BUMPER ZONE of 2.5-5.75in, max 4in beyond the perimeter, filled corners, no wedges, and red/blue covers with white team numbers 3.75in tall in 3+ locations. The only notable 2026 change allows one larger coverage gap with 5.0in protected on each side.
- AprilTags: family 36h11 since 2024, with a 6.5in tag body printed on an 8.125in-square target mounted on a 10.5in polycarbonate panel. Counts: 16 tags (IDs 1-16) in 2024, 22 (IDs 1-22) in 2025, 32 (IDs 1-32) in 2026. 2025 heights ranged from 6.875in (REEF) to 5ft9in (BARGE).
- WPILib conventions: NWU axes (X forward, Y left, Z up, CCW positive) and the 'Always Blue Origin' field frame (+X away from the blue alliance wall), with an official AprilTag field-layout JSON each season.
- Field: nominally 27ft x 54ft carpet (2025 actual 26ft5in x 57ft6.875in; 2026 back to ~26.5ft x 54.3ft), 20in polycarbonate guardrails with four 38in gates, and alliance walls of 3 driver stations (36.8in diamond-plate base + 42in polycarbonate, 69in x 12.25in shelf, E-stop and A-stop).
- Manual skeleton (the same in 2025 and 2026): 15 sections, namely Introduction, FIRST Season Overview, Game Sponsor Recognition, Game Overview, ARENA, Game Details, Game Rules (G), ROBOT Construction Rules (R), Inspection & Eligibility (I), Tournaments (T), District/Regional/Championship, Event Rules (E) and Glossary.
- Numbering conventions: a prefix letter + 3 digits, with the first digit = subsection (R4xx bumpers, R5xx motors, R6xx power, R7xx control, R8xx pneumatics); lettered sub-parts A/B/C; ALL-CAPS glossary terms; asterisked green 'evergreen' rules; and a 'Violation:' line for each rule, using VERBAL WARNING / MINOR FOUL (+2) / MAJOR FOUL (+6) / YELLOW / RED CARD (2025 point values).
- Match timing: 2025 = 0:15 AUTO + 2:15 TELEOP; 2026 = 0:20 AUTO + 2:20 teleop, split into a 10s TRANSITION SHIFT plus four 25s alliance SHIFTS (hub activation alternates via game data), with the last 30s = ENDGAME.
- Pneumatics (stable): one onboard compressor <=1.1 cfm @ 12VDC, stored pressure <=120 psi, working pressure <=60 psi behind a single relieving regulator, solenoids 1/8in NPT max, tubing 1/4in OD max.

## Sources

This research draws on the official FIRST game manuals (hosted at firstfrc.blob.core.windows.net), FRCManual.com (an accurate HTML mirror of the official manuals), WPILib documentation and Chief Delphi discussion. All rule numbers below were checked against the 2025 and/or 2026 manual text.

## 1. Legal control system components (R-rules)

FRC robot construction rules use a numbering scheme by subsection that has been stable since the 2023 manual restructure: R1xx = size/weight/general, R2xx = safety/materials, R3xx = budget/fabrication, R4xx = BUMPERS, R5xx = motors/actuators, R6xx = power distribution, R7xx = control/signal system, R8xx = pneumatics.

### Controller, radio and communication
- **roboRIO (R701 in both 2025 and 2026):** "ROBOTS must be controlled via 1 programmable NI roboRIO or roboRIO 2.0 (P/N am3000 or am3000a, both versions referred to throughout this manual as 'roboRIO')." The image version requirements are year-stamped: 2025_v2.0 or later (REEFSCAPE), 2026_v1.2 or later (REBUILT). Source: [2025 manual R701](https://www.frcmanual.com/2025/robot-construction-rules-(r)), [2026 manual R701](https://www.frcmanual.com/2026/robot-construction-rules-(r)).
- **Radio (R702):** exactly 1 Vivid-Hosting wireless bridge, P/N VH-109 (also sold as WCP-1538), "the only permitted device for communicating to and from the ROBOT during the MATCH," configured with an encryption key tied to the team number. Events in China still use the legacy OpenMesh OM5P-AN/OM5P-AC. R703 governs the Ethernet connection from the roboRIO to the radio; R704 caps bandwidth at 7.0 Mbit/s for the VH-109 (4.0 Mbit/s for OpenMesh).

### Power distribution
- **Battery (R601):** exactly one non-spillable 12 V sealed lead-acid (SLA) battery; nominal capacity at the 20-hour rate minimum 17 Ah, maximum 18.2 Ah; dimensions 7.1 in × 3.0 in × 6.6 in (±0.1 in). Named examples: Enersys NP18-12 / NP18-12B / NP18-12BFR, MK Battery ES17-12, Yuasa NP18-12B.
- **Main circuit (R609):** ≥6 AWG copper wire, a single pair of Anderson Power Products 2-pole SB-type connectors, and a single 120 A main breaker (Cooper Bussmann CB185-120 / CB285-120 or Optifuse 153120 / 253120), feeding one power distribution device. In 2025 the device is a CTR Electronics PDP (am-2856), PDP 2.0 (24-806880) or REV Robotics PDH (REV-11-1850); 2026 adds the AndyMark AMPD (am-5754) to that list.

### Legal motors (R501, "Allowable motors")
The lists for 2025 and 2026 are substantially the same: AndyMark 9015, NeveRest, PG, RedLine, Snow Blower; Banebots RS775/RS550 variants; CIM; CTR Electronics Minion and Falcon 500; KOP automotive motors (Denso, Bosch, Johnson Electric); Playing With Fusion Venom (integrated controller); REV Robotics HD Hex, NEO Brushless (NEO), NEO 550, NEO Vortex; VEX BAG and Mini-CIM; West Coast Products Kraken X60, Kraken X44 (Kraken X44 and Minion were added to the 2025 list mid-season through Team Updates) and RS775 Pro. 2025 also lists the Nidec Dynamo BLDC; 2026 adds the Thrifty Pulsar 775. Blanket allowances in both years: cooling fans ≤120 mm and ≤10 W @ 12 VDC; PWM COTS servos with stall current ≤4 A and output power ≤8 W @ 6 V; one compressor; COTS linear actuators, solenoids and electromagnets. The 775pro appears in the tables under its vendor names (Banebots RS775 / WCP RS775 Pro).
- **R502 (introduced for 2025 and retained in 2026):** "A ROBOT may not have more than **4 propulsion motors**." This rules out 6-CIM drivetrains and 8-motor swerve designs. It is a distinctive modern rule that a mock manual should mirror.

### Legal motor controllers (R504)
2025 list: DMC 60/DMC 60c, Jaguar (PWM only), Koors40 (am-5600), Nidec Dynamo (integral), SD540 variants, Spark (REV-11-1200), Spark MAX (REV-11-2158), Spark Flex (REV-11-2159), Talon (legacy), Talon SRX (217-8080), Talon FX (217-6515, 19-708850), Talon FXS (24-708883), Thrifty Nova (TTB-0100), Venom (BDC-10001, integral), Victor 884/888/SP/SPX. The 2026 list is trimmed to the modern set (Koors40, the Spark family, the Talon family including Talon FXS, Thrifty Nova, Venom, Victor SP/SPX); the legacy DMC60/Jaguar/SD540/Victor 884 entries do not appear in the 2026 table as rendered on FRCManual.com. Relay-class devices legal in both years: Spike H-Bridge (217-0220), Automation Direct relays and REV PDH switched channels (non-actuator loads only). CAN motor controllers are legal provided all commands originate from the roboRIO.

### Pneumatics (R8xx)
The rules are stable across both seasons. Compressed air must come from one onboard compressor rated ≤ nominal 1.1 cfm @ 12 VDC (R806); stored pressure ≤120 psi (R807); working pressure ≤60 psi, downstream of a single primary adjustable relieving regulator (R808). R804 permits solenoid valves (max ⅛ in NPT), tubing (max ¼ in OD), pressure vent plugs, relief valves, transducers and gauges, cylinders, and storage tanks (2026 explicitly bans the white Clippard AVT-PP-41 tank).

## 2. Robot constraints and the 2025→2026 change

| Constraint | 2025 REEFSCAPE | 2026 REBUILT |
|---|---|---|
| Weight (less bumpers & battery) | ≤115 lb (R103) | ≤115 lb (R103) |
| Weight with bumpers (R408) | ≤135 lb | ≤135 lb |
| Starting-config perimeter (R104) | ≤120 in | **≤110 in** |
| Starting-config height (R104) | ≤3 ft 6 in | **≤30 in** |
| Horizontal extension (R105) | ≤1 ft 6 in beyond perimeter | **≤12 in**, and (R106) only over one side at a time |
| In-match height | no global cap (robots reached 6+ ft for L4/deep cage) | **R107: total height may never exceed 30.0 in**; no climbing exception listed |

Bold marks a value that changed for 2026. Sources: [2025 R-rules](https://www.frcmanual.com/2025/robot-construction-rules-(r)), [2026 R-rules](https://www.frcmanual.com/2026/robot-construction-rules-(r)); Chief Delphi corroborates the 110-inch perimeter ("[110' vs 110\" perimeter](https://www.chiefdelphi.com/t/110-vs-110-perimeter/521817)").

**Frame perimeter (R101/R102):** the ROBOT PERIMETER is "comprised of fixed, non-articulated structural elements," is established in STARTING CONFIGURATION, and is measured by "wrap[ping] a piece of string around the outer most parts of the ROBOT (excluding BUMPERS) at the BUMPER ZONE… and pull it taut" (2025 R102). Minor protrusions (bolt heads, rivets) are excluded.

**Bumpers (R4xx):** the major bumper overhaul came between 2024 and 2025 (see the CD thread "[2025 Bumper Rules Changes](https://www.chiefdelphi.com/t/2025-bumper-rules-changes/478756)"). The BUMPER ZONE became floor-referenced, and full-perimeter coverage became mandatory. 2026 carries the same regime with one change to coverage gaps. Verified specifics (rule numbers valid in both years):
- **R401:** bumpers must protect the entire ROBOT PERIMETER; gaps <1.25 in between adjacent segments are permitted (corners must still be filled per R406). 2026 also allows one larger gap if at least 5.0 in of perimeter on each side of it remains protected.
- **R402:** construction = ≥2.25 in depth of foam padding, ≥4.5 in tall (pool noodles; polyethylene 1.5–3.0 lb/ft³; EVA 2.0–6.0 lb/ft³; foam floor tiles), a wood/plywood-style backing ≥4.5 in tall, a cloth cover and a rigid fastening system.
- **R403:** bumpers extend ≤4.0 in from the ROBOT PERIMETER. **R404:** hard parts ≤1.25 in from the perimeter; padding must extend ≥2.0 in beyond any hard part.
- **R405:** padding must entirely fill the BUMPER ZONE, 2.5 in to 5.75 in from the floor. This floor-referenced zone is the characteristic modern bumper convention.
- **R406:** corners filled with uncompressed padding ≥2.25 in from the corner, with no voids. **R407:** no wedge geometry. **R409:** non-articulated. **R410:** removable for inspection and weighing.
- **R411/R412:** bumpers must display red or blue to match the alliance, with team numbers in white Arabic numerals ≥3.75 in tall with a ≥0.5 in stroke, visible in ≥3 locations approximately 90° apart.

## 3. AprilTag standard

- **Family:** 36h11 since 2024 (2023 used 16h5). Per [WPILib's AprilTag introduction](https://docs.wpilib.org/en/stable/docs/software/vision-processing/apriltag/apriltag-intro.html): "Starting from 2024, FIRST has chosen the 36h11 family," and tags are "printed such that the tag's main 'body' is **6.5 inches** in length."
- **Physical target:** the printed target sheet is 8.125 in (8⅛ in) square (the 6.5-in tag body plus a white margin), mounted centered on a 10.5 in square polycarbonate panel. This stack of 6.5-in body, 8.125-in sheet and 10.5-in panel is the same in the 2024, 2025 and 2026 field drawings.
- **2024 CRESCENDO:** 16 tags, IDs 1–16. SOURCE tags 1, 2, 9, 10 on the source walls; AMP and SPEAKER tags at mid-height on the field wall; STAGE tags 11–16 centered on the three wide faces of each STAGE core at 3 ft 11½ in above the carpet. Source: [2024 AprilTag Images and User Guide](https://firstfrc.blob.core.windows.net/frc2024/FieldAssets/Apriltag_Images_and_User_Guide.pdf), [FRCManual 2024 ARENA](https://www.frcmanual.com/2024/arena).
- **2025 REEFSCAPE:** 22 tags, IDs 1–22 ([FRCManual 2025 ARENA](https://www.frcmanual.com/2025/arena)). Mounting heights (approximately to tag center, per the manual): CORAL STATION tags 1, 2, 12, 13 at 4 ft 5¼ in; PROCESSOR tags 3, 16 at 3 ft 9⅞ in; BARGE tags 4, 5, 14, 15 at 5 ft 9 in; REEF tags 6–11 and 17–22 at only 6⅞ in above the carpet (one per reef face; teams used these low tags for auto-align scoring).
- **2026 REBUILT:** 32 tags, IDs 1–32 ([FRCManual 2026 ARENA](https://www.frcmanual.com/2026/arena)): 16 HUB tags at 44.25 in, 4 TOWER-wall tags and 4 OUTPOST tags at 21.75 in, and 8 TRENCH tags at 35 in.
- **Coordinate conventions** ([WPILib coordinate system docs](https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html)): WPILib uses NWU axes (X forward, Y left, Z up; counter-clockwise positive). The dominant field convention is "Always Blue Origin": the origin is fixed at the blue-alliance corner, with +X pointing away from the blue alliance wall. It is preferred because "AprilTags throughout the field are unique," so pose estimation needs no alliance-flip transform. WPILib ships an official AprilTag field-layout JSON (tag ID → 3D pose) each season.

## 4. Field conventions

The colloquial "27 ft × 54 ft" field is nominal; the manuals give exact figures:
- **2025:** carpet playing surface ≈ 26 ft 5 in × 57 ft 6⅞ in (the REEFSCAPE field ran long). **2026:** ≈ 317.7 in × 651.2 in (~26.5 ft × ~54.3 ft), back to the usual ~54-ft length.
- **Guardrails:** transparent polycarbonate on aluminum extrusion along the long edges, 1 ft 8 in (20.0 in) tall, with four access gates 38 in (3 ft 2 in) wide when open.
- **Alliance walls and driver stations:** each alliance wall holds three DRIVER STATIONS. Each station is a ~36.8-in (3 ft ¾ in) tall diamond-plate base topped by a 42-in (3 ft 6 in) transparent polycarbonate sheet, with an aluminum operator-console shelf 69 in (5 ft 9 in) wide × 12.25 in deep, an E-stop button, an A-stop button (autonomous stop, standard since 2024), an Ethernet drop, a power outlet, a team sign and LED status indicators. Sources: [2025 ARENA](https://www.frcmanual.com/2025/arena), [2026 ARENA](https://www.frcmanual.com/2026/arena).
- The carpet is low-pile, with edges and seams secured with gaffer's tape.

## 5. Game manual structure and rule numbering

The [2025](https://www.frcmanual.com/2025) and [2026](https://www.frcmanual.com/2026) manuals use the same 15-section skeleton:

1. Introduction
2. FIRST Season Overview
3. Game Sponsor Recognition
4. Game Overview
5. ARENA
6. Game Details
7. Game Rules (**G**)
8. ROBOT Construction Rules (**R**)
9. Inspection & Eligibility (**I**)
10. Tournaments (**T**)
11. District Tournaments
12. Regional Tournaments
13. FIRST Championship Tournament (**C**)
14. Event Rules (**E**)
15. Glossary

Conventions a mock manual should replicate:
- **Rule IDs** = a letter prefix + a 3-digit number, where the first digit = subsection (G4xx = section 7.4, R6xx = section 8.6, etc.). Sub-requirements use capital letters (A, B, C…), with roman numerals below that. Each rule carries a bold headline (e.g., "R104 *STARTING CONFIGURATION – max size*") followed by the rule text, blue-box examples and non-binding gray commentary boxes.
- **Evergreen rules** (stable from year to year) are marked with an asterisk and green text; season-specific rules are blue.
- **Defined terms** are glossary words in SMALL-CAPS/ALL-CAPS (ROBOT, MATCH, BUMPER ZONE, STARTING CONFIGURATION, MOMENTARY).
- **Violation taxonomy** (2025 Table 6-3; the categories are retained in 2026, with the 2026 point values given in `gap-critic.md`): VERBAL WARNING, MINOR FOUL (+2 points to the opponent), MAJOR FOUL (+6 points), YELLOW CARD, RED CARD (disqualification); a second yellow becomes a red. Before 2025 these were FOUL/TECH FOUL; the MINOR/MAJOR names mark the current era. Each G-rule ends with a "Violation:" line naming its penalty.
- **Match structure:** 2025 = AUTO 0:15 + TELEOP 2:15 (2:30 total). 2026 REBUILT = AUTO 0:20, then a 2:20 teleop subdivided into a 10-s TRANSITION SHIFT + four 25-s alliance SHIFTS (hub activation alternating by game data), with the final 30 s as ENDGAME, 2:40 total, plus a 3-s scoring-assessment window after AUTO. Sources: [2025 manual HTML](https://firstfrc.blob.core.windows.net/frc2025/Manual/HTML/2025GameManual.htm), [2026 game details](https://www.frcmanual.com/2026/game-details), [WPILib 2026 game data](https://docs.wpilib.org/en/stable/docs/yearly-overview/2026-game-data.html).
- **2026 game specifics:** the game piece is FUEL (504 staged per match; up to 8 preloaded per robot; 24 per DEPOT, 24 per OUTPOST chute); HUB scoring is 1 pt/FUEL when active; the TOWER climb is L1 = 15 pts (AUTO, max 2 robots), L2 = 20, L3 = 30, with one climb level per robot in TELEOP.

### Caveats
- FRCManual.com is an unofficial but accurate mirror. The authoritative texts are the season PDFs at firstfrc.blob.core.windows.net (the 2026 manual is current at TU22). Chief Delphi threads corroborated the unusual 2026 numbers (110-in perimeter, 30-in hard height cap).
- The finding that the 2026 motor-controller table omits legacy controllers (Jaguar, DMC60, SD540, Victor 884/888) is based on the mirror's rendering. Treat it as high-confidence, but check it against the official PDF if the exact 2026 legality of legacy controllers matters.
