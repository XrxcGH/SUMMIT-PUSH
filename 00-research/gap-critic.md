# Completeness Critique of the Research

## Key takeaways
- 2026 RP thresholds escalate by event tier and were patched mid-season: Energized 100 fuel (regional) -> 240 (DCMP, TU19) -> 360 (Champs, TU22); Supercharged 360 -> 360 -> 500; Traversal 50 flat. Build a Regional/DCMP/Champs threshold table into the mock manual from day one and judge against the top column.
- Calibration rule of thumb derived from the 2025-2026 failures: the entry volume RP should be ~40-60% achievable at regionals (100 fuel proved routine and had to be raised 2.4-3.6x); the stretch RP should be ~3-3.5x the entry RP (360 fuel = 71% of the 504 staged, ~3.3 fuel/sec across ~110s of active-hub time); the endgame RP = 'two robots do the mid-tier action' (50 tower pts).
- Foul values scale with each season's point economy. 2026 uses MINOR 5 / MAJOR 15 (instead of 2025's 2/6) because fuel is worth 1 pt. Set mock-game fouls at roughly 3-8x the base scoring action.
- 2026 REBUILT has no coopertition mechanic, which breaks the 2023-2025 pattern of RP relief. A co-op mechanic is therefore optional. The convention to keep is win/tie = 3/1 RP with three bonus RPs (max 6/match).
- Anti-farming wording needs care. Fuel scored in an inactive hub scores 0 and does not count toward fuel RPs (TU01 had to patch this wording); the auto winner's hub is INACTIVE in shifts 1&3; an auto tie -> random pattern; scoring settles 3s after each period. Each of these edge cases needs explicit manual text, or the Q&A thread will find the exploit.
- Buildability now has an official specification: FIRST's 2026 four-tier ladder (Team Test Elements = hardware-store lumber + basic tools; Event Test = notch-and-tab plywood; Team Practice = 4x8 CNC-router CAD; Wood Practice Perimeter), with official CAD in Onshape + STEP. The mock field package should ship an Onshape document plus a plywood 'team version' of every scoring element.
- The real 2026 element dimensions are the buildability benchmark: hub 47x47in with a 41.7in hex opening at 72in, tower rungs of 1.25in pipe at 27/45/63in, 6.5in bumps with 15-degree ramps, 22.25in trench clearance. They use round numbers, sheet goods and shallow standard angles (the fix for 2025's resented 35-degree reef branches).
- AprilTag placement pattern to copy: 36h11, 8.125in tag on a 10.5in panel, TWO tags per scoring face (one centered, one offset) at heights set per element (hub 44.25in, tower/outpost 21.75in, trench 35in), IDs 1-32 mirrored red/blue. The required vision deliverable is a WPILib-schema field-layout JSON (ID + Pose3d, always-blue-origin NWU) that PhotonVision/Limelight can ingest. 2026 ships separate Welded and AndyMark layouts.
- The largest 2026 design pitfall was the TU19 G415/G416 crisis. A small game piece and 30in robots forced constant contact inside robot perimeters, and FIRST rewrote the contact rules mid-season with an apology. Write contact rules around outcomes (damage or functional impairment, with escalation at 'unable to drive ~20s') and grant immunity in the home alliance zone from day one.
- Wording exploits are the recurring failure in real and mock games (Hero Heist district ownership, the 2026 'active hub' RP text, the 2025 FMS auto-coral bug that flipped 8 match outcomes). Red-team every scoring definition, and publish out-of-bounds handling, settle timing and tie randomization before release.

## Scope

The five source reports cover history, sentiment, pedagogy, CADathon format and control-system standards. A designer writing a full mock manual, field CAD and vision specification from them would still meet five gaps. Each gap below is stated and then answered with further research, verified against 2026-season primary sources current as of August 2026.

---

## Gap 1: The full 2026 REBUILT scoring and foul economy

The earlier takeaways describe 2026 REBUILT only at headline level. The full scoring economy, the foul economy and the edge-case rules that a manual author must mirror were missing. A mock manual has to reproduce the detail of a real Section 6, and several takeaway numbers were incomplete or stale. Verified specifics from the TU22-era manual ([frcmanual.com/2026/game-details](https://www.frcmanual.com/2026/game-details), [2026 Game Manual PDF](https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf)):

- Fuel = 1 pt in auto and teleop, but only in an active hub. Fuel scored in an inactive hub scores 0 and does not count toward fuel RPs (TU01 reworded the RP rows to "scored in *an active* HUB"). This is the game's central anti-farming clause; a mock manual needs an equivalent rule for wasted scoring.
- Hub shift logic: the alliance that scores more auto fuel has its hub inactive in Shifts 1 & 3 and active in 2 & 4. Winning auto therefore means your opponent shoots first, an intentional rubber-band mechanic that the earlier takeaways framed as an advantage. On an auto tie, the FMS assigns the pattern at random. Both hubs are active in auto, the 10s transition shift and the 30s endgame. Max active windows per alliance ≈ 20 + 10 + 25 + 25 + 30 = 110 seconds.
- Tower: L1 = 15 pts in auto (max 2 robots); teleop L1/L2/L3 = 10/20/30. Each robot scores one level in teleop, but an auto L1 and a teleop level stack. The qualification criteria are written geometrically (bumpers fully above LOW/MID RUNG), which is a clean template for writing climb rules.
- Fouls were rescaled to the game economy: MINOR FOUL = 5 pts, MAJOR FOUL = 15 pts, instead of the 2025 values (+2/+6) implied by the tech-standards report. Foul values track the season's point inflation. 2025 coral was worth 2–7 pts, so fouls were 2/6; 2026 fuel is worth 1, so fouls are 5/15 ≈ "a minor foul = one intake-load of fuel". A mock game should set fouls at roughly 3–8x the base scoring action.
- No coopertition mechanic exists in 2026. REBUILT broke the 2023–2025 pattern of RP-threshold relief ([CD: "No Coopertition this year"](https://www.chiefdelphi.com/t/no-coopertition-this-year/512825)), and coopertition survives only as an ethos. "One co-op mechanic" is therefore a design option and not a requirement of the current manual.
- Timing of scoring assessment: fuel is counted 3 seconds after the period ends, and tower points are evaluated when all robots are at rest or at T+3s. Copy this "settle window" language for any ball-scoring mock game.

---

## Gap 2: Setting point values and RP thresholds

No report answered the core balance question: how to set point values and RP thresholds mathematically, and what achievement rate they should target. The 2026 season is now the best public case study, because FIRST published an RP escalation table by event tier and then had to patch it mid-season.

Evolution of Table 6-5, from [Team Update 19, Mar 31 2026](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate19.pdf) and Team Update 22, Apr 21 2026, in the [combined updates PDF](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate-Combined.pdf) (bold marks a raised value):

| Bonus RP | Regional/District | District Champs (TU19) | FIRST Champs (TU22) |
|---|---|---|---|
| ENERGIZED | 100 fuel | **240** | **360** |
| SUPERCHARGED | 360 fuel | 360 | **500** |
| TRAVERSAL | 50 tower pts | 50 | 50 |

Balance math a designer can reuse:

- Energized at 100 was routine by mid-season. CD threads show teams modeling rankings around the 240 jump and debating whether to drop climbers once the thresholds moved. Nearly every functional alliance reached the entry volume RP, which repeated 2025's problem of RPs that were too easy (NE DCMP matches in which both alliances took 2–3 bonus RPs, making schedule luck dominant). FIRST's fix: 2.4x at DCMP, 3.6x at Champs.
- Throughput ceiling check: 504 fuel staged; Supercharged 360 = 71% of all staged fuel; 360 fuel ÷ ~110s of active-hub time ≈ 3.3 fuel/sec sustained across the alliance, which is intentionally near the physical limit. Rule of thumb: entry RP ≈ what a median alliance does in a match (aim for ~40–60% achievement at regionals); stretch RP ≈ 3–3.5x entry, achievable only by coordinated elite alliances (<10%); endgame RP = "two robots do the mid-tier action" (50 = L2+L3, or 15+15+20 with auto climbs).
- Design the escalation table into the manual from day one (columns for Regional/DCMP/Champs, with "TBA" allowed as a value). This is now an established convention (the 2024 Melody RP did it too), and it protects the game against the "solved by week 4" failure mode. For a one-week CADathon, publish the table and judge robots against the Champs column, which forces entrants to model both metas.
- Win/tie = 3/1 RP (confirmed), so the maximum is 6 RP/match and the three bonus RPs together equal one win. Keep that ratio.

---

## Gap 3: What buildable means

The research noted that teams resent unbuildable field elements but did not define buildable. FIRST formalized the term for 2026. Its [2026 Practice Field & Team Element Changes](https://community.firstinspires.org/2026-practice-field-team-element-changes) post defines a four-tier fidelity ladder that a mock game's field-CAD package should imitate:

1. Team Test Elements: low fidelity, hardware-store lumber, hand and power tools only; each validates a single robot function (e.g., [TE-26500 build instructions](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/TE-26500-build-instructions.pdf)).
2. Event Test Elements: notch-and-tab plywood, with real field components only where robot interaction is sensitive to tolerance.
3. Team Practice Elements: medium fidelity, cut on a 4×8 ft CNC router, shipped as CAD only ("FIRST has not built or tested the final design").
4. Wood Practice Perimeter: a compatible medium-fidelity perimeter.

Official field CAD is now published in Onshape first, with STEP exports, which matches the WCP CADathon's Onshape requirement. A mock game should ship an Onshape field document.

Buildability benchmarks from the real 2026 elements ([frcmanual.com/2026/arena](https://www.frcmanual.com/2026/arena)): Hub = 47×47 in footprint, hex opening 41.7 in across at 72 in height; Tower rungs = 1.25 in pipe at 27/45/63 in (18 in spacing, even numbers, buildable as a ladder from pipe and lumber); Bumps = 6.513 in tall with 15° HDPE ramps; Trench under-clearance = 50.34 in wide × 22.25 in tall; Chute opening 31.8×7 in at 28.1 in. The pattern is that critical robot-interaction dimensions land on round or half-inch values, structures break down into sheet goods and pipe, and ramp and branch angles are shallow standard angles. This answers the resentment over 2025's 35° reef branches. Design rule for the mock game: every scoring element must have a stated "team version" buildable from ≤2 sheets of plywood + hardware-store pipe, published with the manual.

---

## Gap 4: AprilTag placement and the layout file

The research specified AprilTag vision only by tag family and size. The placement pattern and the layout-file deliverable were undefined. From the [2026 AprilTag Images and User Guide](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-apriltag-images-user-guide.pdf) and the [WPILib AprilTagFieldLayout docs](https://github.wpilib.org/allwpilib/docs/release/java/edu/wpi/first/apriltag/AprilTagFieldLayout.html):

- 36h11 family, IDs 1–32, 8.125 in square tag centered on a 10.5 in square polycarbonate panel (all consistent with 2024–25).
- Placement pattern: every scoring face gets two tags, one centered on the feature and one offset horizontally, which enables MultiTag pose solves from oblique angles. Heights are set per element to suit camera sightlines: Hub tags at 44.25 in (16 tags, four faces × 2 × 2 hubs), Tower and Outpost tags at 21.75 in, Trench tags at 35 in facing both zones. A mock game should copy this: 2 tags per approach face, mounted 20–45 in high, IDs mirrored red/blue.
- The vision deliverable is a JSON file. WPILib's format is `{"tags": [{"ID": n, "pose": Pose3d(translation + quaternion)}...], "field": {"length": m, "width": m}}`, in the Always-Blue-Origin NWU frame. 2026 ships TWO official layouts (Welded and AndyMark fields), and TU22 specifies that Championship fields are Welded. Tools such as [PhotonVision](https://docs.photonvision.org/en/latest/docs/apriltag-pipelines/multitag.html) and [Limelight](https://docs.limelightvision.io/docs/resources/downloads) ingest these files directly. A complete mock-game release must therefore include a field-layout JSON in this schema so entrants can simulate localization. The dual layout is worth copying into the manual as a note, or the manual can declare one canonical layout.

---

## Gap 5: The 2026 contact-rule rewrite

The pitfall lists in the research were at the level of sentiment. The 2026 season produced a concrete pitfall at the level of manual text, the G415/G416 contact-rule crisis, and any mock manual must design around it.

[Team Update 19](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate19.pdf) (Mar 31, 2026) replaced the in-perimeter contact fouls wholesale mid-season, and FIRST apologized. The 5.91 in game piece, the 30 in robot height cap and the bumper-zone geometry meant robots were "frequently interacting inside the ROBOT PERIMETER of opposing ROBOTS," putting "intense scrutiny on REFEREES to observe every interaction," and FIRST pledged "to do a better job of not putting teams and REFEREES in this same difficult position." The design principles of the rewrite can be reused directly in a mock manual:

- Penalize outcomes instead of geometry. Only damage or functional impairment from initiated contact draws the MAJOR FOUL + card; cosmetic damage, tipped robots, contact during auto and openings in bumper gaps are all carved out as exceptions.
- Grant home-zone immunity. Contact inside your own Alliance Zone is never a G415 violation, which protects scoring robots near their hub without protecting them everywhere.
- Escalate by consequence: "unable to drive ~20+ s" upgrades a yellow card to a red.

Combined with the earlier reports, the designer's pitfall checklist gains three rules:

1. If the sizes of the game piece and the robot force intake-to-intake proximity, write outcome-based contact rules from day one and give each alliance a protected zone.
2. Exploits live in wording (Hero Heist's district-ownership ambiguity; 2026's "active hub" RP wording, which needed a TU01 patch). Red-team every scoring definition before release.
3. Publish scoring-settle timing, the handling of out-of-bounds pieces (2026: staff return fuel at the point of exit) and auto-tie randomization explicitly, because these are the first questions a CADathon Q&A thread will ask.

---

## Sources
- [frcmanual.com: 2026 Game Details](https://www.frcmanual.com/2026/game-details) · [2026 Arena](https://www.frcmanual.com/2026/arena) · [2026 Game Manual (TU22) PDF](https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf)
- [REBUILT Team Update 19](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate19.pdf) · [Combined Team Updates (TU01–TU22)](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate-Combined.pdf)
- [FIRST: 2026 Practice Field & Team Element Changes](https://community.firstinspires.org/2026-practice-field-team-element-changes) · [TE-26500 build instructions](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/TE-26500-build-instructions.pdf) · [FIRST Playing Field page](https://www.firstinspires.org/resources/library/frc/playing-field)
- [2026 AprilTag Images & User Guide](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-apriltag-images-user-guide.pdf) · [WPILib AprilTagFieldLayout](https://github.wpilib.org/allwpilib/docs/release/java/edu/wpi/first/apriltag/AprilTagFieldLayout.html) · [PhotonVision MultiTag](https://docs.photonvision.org/en/latest/docs/apriltag-pipelines/multitag.html) · [Limelight downloads](https://docs.limelightvision.io/docs/resources/downloads)
- [Wikipedia: Rebuilt (FIRST)](https://en.wikipedia.org/wiki/Rebuilt_(FIRST)) · [2026 REBUILT cheat sheet](https://www.firstinspires.org/hubfs/web/volunteer/frc/2026-rebuilt-cheat-sheet.pdf)
- Chief Delphi: [No Coopertition this year](https://www.chiefdelphi.com/t/no-coopertition-this-year/512825) · [Inactive-hub fuel and RPs](https://www.chiefdelphi.com/t/does-fuel-scored-while-a-hub-is-inactive-count-toward-fuel-based-ranking-points/510717) · [2026 Team Update 19 thread](https://www.chiefdelphi.com/t/2026-team-update-19/517726) · [Are you adding a climber for DCMP?](https://www.chiefdelphi.com/t/are-you-adding-a-climber-for-dcmp/518040) · [Worlds 2025 RP increases](https://www.chiefdelphi.com/t/worlds-2025-ranking-points-rps-increaces/498243)
- [FIRST blog: Coral Scoring Adjustments (2025)](https://community.firstinspires.org/coral-scoring-adjustments) · [TBA Blog: Making Better RP Predictions](https://blog.thebluealliance.com/2019/08/04/making-better-rp-predictions/)
