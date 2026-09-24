# gap-critic

## KEY TAKEAWAYS
- 2026 RP thresholds escalate by event tier and were patched mid-season: Energized 100 fuel (regional) -> 240 (DCMP, TU19) -> 360 (Champs, TU22); Supercharged 360 -> 360 -> 500; Traversal 50 flat. Build a Regional/DCMP/Champs threshold table into the mock manual from day one and judge against the top column.
- Calibration rule of thumb derived from 2025-2026 failures: entry volume RP should be ~40-60% achievable at regionals (100 fuel proved routine and had to be raised 2.4-3.6x), stretch RP ~3-3.5x entry (360 fuel = 71% of the 504 staged, ~3.3 fuel/sec across ~110s of active-hub time), endgame RP = 'two robots do the mid-tier action' (50 tower pts).
- Foul values rescale to each season's point economy: 2026 uses MINOR 5 / MAJOR 15 (not 2025's 2/6) because fuel is worth 1 pt - set mock-game fouls at roughly 3-8x the base scoring action.
- 2026 REBUILT has NO coopertition mechanic, breaking the 2023-2025 RP-relief pattern - a co-op mechanic is a design option, not a current convention; win/tie = 3/1 RP with three bonus RPs (max 6/match) is the convention to keep.
- Critical anti-farming wording: fuel scored in an inactive hub scores 0 and does not count toward fuel RPs (TU01 had to patch this wording); auto winner gets hub INACTIVE in shifts 1&3; auto tie -> random pattern; scoring settles 3s after each period - every one of these edge cases needs explicit manual text or the Q&A thread finds the exploit.
- Buildability now has an official spec: FIRST's 2026 four-tier ladder (Team Test Elements = hardware-store lumber + basic tools; Event Test = notch-and-tab plywood; Team Practice = 4x8 CNC-router CAD; Wood Practice Perimeter), with official CAD in Onshape + STEP - the mock field package should ship an Onshape doc plus a plywood 'team version' of every scoring element.
- Real 2026 element dimensions are the buildability benchmark: hub 47x47in with 41.7in hex opening at 72in, tower rungs of 1.25in pipe at 27/45/63in, 6.5in bumps with 15-degree ramps, 22.25in trench clearance - round numbers, sheet goods, shallow standard angles (the fix for 2025's resented 35-degree reef branches).
- AprilTag placement grammar to copy: 36h11, 8.125in tag on 10.5in panel, TWO tags per scoring face (one centered, one offset) at element-tuned heights (hub 44.25in, tower/outpost 21.75in, trench 35in), IDs 1-32 mirrored red/blue; the mandatory vision deliverable is a WPILib-schema field-layout JSON (ID + Pose3d, always-blue-origin NWU) that PhotonVision/Limelight can ingest - note 2026 ships separate Welded and AndyMark layouts.
- Biggest 2026 design pitfall (TU19 G415/G416 crisis): small game piece + 30in robots forced constant in-perimeter contact, and FIRST rewrote the contact rules mid-season with an apology - write contact rules by OUTCOME (damage/functional impairment, 'unable to drive ~20s' escalation) not geometry, and grant home-alliance-zone immunity from day one.
- Wording exploits are the recurring failure across real and mock games (Hero Heist district-ownership, 2026 'active hub' RP text, 2025 FMS auto-coral bug that flipped 8 match outcomes) - red-team every scoring definition and publish out-of-bounds handling, settle timing, and tie randomization before release.

## REPORT
# Completeness Critique: Remaining Gaps and Answers

The five source reports cover history, sentiment, pedagogy, CADathon format, and control-system standards well. But a designer sitting down to write a full mock manual + field CAD + vision spec would still hit five concrete walls. Each gap below is stated, then answered with fresh research (all verified against 2026-season primary sources, current as of August 2026).

---

## GAP 1: The takeaways describe 2026 REBUILT only at headline level — the full scoring economy, foul economy, and edge-case rules a manual author must mirror were missing

A mock manual has to reproduce the *texture* of a real Section 6, and several takeaway numbers were incomplete or stale. Verified specifics from the TU22-era manual ([frcmanual.com/2026/game-details](https://www.frcmanual.com/2026/game-details), [2026 Game Manual PDF](https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf)):

- **Fuel = 1 pt in auto AND teleop, but only in an *active* hub; inactive-hub fuel scores 0 and does NOT count toward fuel RPs** (TU01 explicitly reworded the RP rows to "scored in *an active* HUB"). This is the game's central anti-farming clause — a mock manual needs an equivalent "wasted scoring" rule.
- **Hub shift logic**: the alliance that scores more auto fuel gets its hub *inactive* in Shifts 1 & 3 and active in 2 & 4 (winning auto = your opponent shoots first — a deliberate rubber-band mechanic the takeaways had backwards in spirit). Auto tie → FMS randomly assigns the pattern. Both hubs are active in auto, the 10s transition shift, and the 30s endgame. Max active windows per alliance ≈ 20 + 10 + 25 + 25 + 30 = **110 seconds**.
- **Tower**: L1 = 15 pts in auto (max 2 robots); teleop L1/L2/L3 = 10/20/30; one level per robot in teleop, but auto-L1 + teleop level stacks. Qualification criteria are written geometrically (bumpers fully above LOW/MID RUNG) — a clean template for writing climb rules.
- **Fouls were re-scaled to the game economy: MINOR FOUL = 5 pts, MAJOR FOUL = 15 pts** — not the 2025 values (+2/+6) implied by the tech-standards report. Lesson: foul values track the season's point inflation (2025 coral was worth 2–7 pts, so fouls were 2/6; 2026 fuel is worth 1, so fouls are 5/15 ≈ "a minor foul = one intake-load of fuel"). A mock game should set fouls at roughly 3–8x the base scoring action.
- **No coopertition mechanic exists in 2026** — REBUILT broke the 2023–2025 pattern of RP-threshold relief ([CD: "No Coopertition this year"](https://www.chiefdelphi.com/t/no-coopertition-this-year/512825)). Coopertition survives only as ethos. So "one co-op mechanic" is a design *option*, not a current-manual requirement.
- Scoring assessment timing convention: fuel counted 3 seconds after the period ends; tower points evaluated when all robots are at rest or T+3s — copy this "settle window" language for any ball-scoring mock game.

---

## GAP 2: No report answered the core balance question — *how do you set point values and RP thresholds mathematically, and what achievement rate should they target?*

The 2026 season itself is now the best public case study, because FIRST published a **per-event-tier RP escalation table and then had to patch it mid-season**:

**Table 6-5 evolution** (extracted directly from [Team Update 19, Mar 31 2026](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate19.pdf) and Team Update 22, Apr 21 2026, in the [combined updates PDF](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate-Combined.pdf)):

| Bonus RP | Regional/District | District Champs (TU19) | FIRST Champs (TU22) |
|---|---|---|---|
| ENERGIZED | 100 fuel | **240** | **360** |
| SUPERCHARGED | 360 fuel | 360 | **500** |
| TRAVERSAL | 50 tower pts | 50 | 50 |

Balance math a designer can reuse:

- **Energized at 100 was routine by mid-season** (CD threads show teams modeling rankings around the 240 jump and debating dropping climbers once thresholds moved) — i.e., the "entry" volume RP was hit by nearly every functional alliance, exactly repeating 2025's too-easy-RP problem (NE DCMP matches where both alliances took 2–3 bonus RPs, making schedule luck dominant). FIRST's fix: **2.4x at DCMP, 3.6x at Champs**.
- **Throughput ceiling check**: 504 fuel staged; Supercharged 360 = 71% of all staged fuel; 360 fuel ÷ ~110s of active-hub time ≈ **3.3 fuel/sec alliance-wide sustained** — deliberately near the physical limit. Rule of thumb: entry RP ≈ what a median alliance does in a match (aim ~40–60% achievement at regionals); stretch RP ≈ 3–3.5x entry, achievable only by coordinated elite alliances (<10%); endgame RP = "two robots do the mid-tier action" (50 = L2+L3, or 15+15+20 with auto climbs).
- **Design the escalation table into the manual from day one** (columns for Regional/DCMP/Champs with TBA allowed) — this is now an established convention (2024 Melody RP did it too) and it inoculates the game against the "solved by week 4" failure mode. For a one-week CADathon, publish the table and judge robots against the *Champs* column; it forces entrants to model both metas.
- Win/tie = 3/1 RP (confirmed), so max 6 RP/match; the three bonus RPs are worth exactly one win — keep that ratio.

---

## GAP 3: "Teams resent unbuildable field elements" was noted, but nobody answered *what buildable actually means* — FIRST formalized it for 2026

FIRST's [2026 Practice Field & Team Element Changes](https://community.firstinspires.org/2026-practice-field-team-element-changes) post defines a **four-tier fidelity ladder** a mock game's field-CAD package should imitate:

1. **Team Test Elements** — low fidelity, hardware-store lumber, hand/power tools only, validates a single robot function (e.g., [TE-26500 build instructions](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/TE-26500-build-instructions.pdf));
2. **Event Test Elements** — notch-and-tab plywood, real field components only where robot interaction is tolerance-sensitive;
3. **Team Practice Elements** — medium fidelity, cut on a 4×8 ft CNC router, shipped as CAD-only ("FIRST has not built or tested the final design");
4. **Wood Practice Perimeter** — compatible medium-fidelity perimeter.

Plus: **official field CAD is now Onshape-first with STEP exports** — matching the WCP CADathon's Onshape requirement; a mock game should ship an Onshape field document.

Buildability benchmarks from the real 2026 elements ([frcmanual.com/2026/arena](https://www.frcmanual.com/2026/arena)): Hub = 47×47 in footprint, hex opening 41.7 in across at 72 in height; Tower rungs = 1.25 in pipe at 27/45/63 in (18 in spacing — even numbers, ladder-buildable from pipe and lumber); Bumps = 6.513 in tall with 15° HDPE ramps; Trench under-clearance = 50.34 in wide × 22.25 in tall; Chute opening 31.8×7 in at 28.1 in. Note the pattern: **critical robot-interaction dimensions land on round or half-inch values, structures decompose into sheet goods + pipe, and ramp/branch angles are shallow standard angles** — the direct answer to 2025's resented 35° reef branches. Design rule for the mock game: every scoring element must have a stated "team version" buildable from ≤2 sheets of plywood + hardware-store pipe, and publish it with the manual.

---

## GAP 4: "AprilTag vision" was specced only as tag family/size — the *placement grammar* and layout-file deliverable were undefined

From the [2026 AprilTag Images and User Guide](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-apriltag-images-user-guide.pdf) and [WPILib AprilTagFieldLayout docs](https://github.wpilib.org/allwpilib/docs/release/java/edu/wpi/first/apriltag/AprilTagFieldLayout.html):

- 36h11 family, IDs 1–32, 8.125 in square tag centered on a 10.5 in square polycarbonate panel (all consistent with 2024–25).
- **Placement grammar**: every scoring face gets **two tags — one centered on the feature, one horizontally offset** — enabling MultiTag pose solves from oblique angles. Heights are per-element, tuned to camera sightlines: Hub tags at 44.25 in (16 tags, four faces × 2 × 2 hubs), Tower and Outpost tags at 21.75 in, Trench tags at 35 in facing both zones. A mock game should copy this: 2 tags per approach face, mounted 20–45 in high, IDs mirrored red/blue.
- **The vision deliverable is a JSON file**: WPILib's format is `{"tags": [{"ID": n, "pose": Pose3d(translation + quaternion)}...], "field": {"length": m, "width": m}}`, in the Always-Blue-Origin NWU frame. **2026 ships TWO official layouts (Welded vs AndyMark field), and TU22 specifies Championship fields are Welded** — vendors like [PhotonVision](https://docs.photonvision.org/en/latest/docs/apriltag-pipelines/multitag.html) and [Limelight](https://docs.limelightvision.io/docs/resources/downloads) ingest these directly. A complete mock-game release must therefore include a field-layout JSON in this exact schema so entrants can simulate localization; the dual-layout wrinkle is worth copying into the manual as a note (or explicitly declaring one canonical layout).

---

## GAP 5: The pitfall lists were sentiment-level; the 2026 season delivered a concrete, manual-text-level pitfall — the G415/G416 contact-rule crisis — that any mock manual must design around

[Team Update 19](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate19.pdf) (Mar 31, 2026) **replaced the in-perimeter-contact fouls wholesale mid-season**, with FIRST apologizing: the 5.91 in game piece, 30 in robot height cap, and bumper-zone geometry meant robots "frequently interacting inside the ROBOT PERIMETER of opposing ROBOTS," putting "intense scrutiny on REFEREES to observe every interaction," and FIRST pledged "to do a better job of not putting teams and REFEREES in this same difficult position." The rewrite's design principles are directly reusable in a mock manual:

- Penalize **outcome, not geometry**: only *damage or functional impairment* from *initiated* contact draws the MAJOR FOUL + card, with cosmetic damage, tipped robots, auto-phase contact, and bumper-gap openings all carved out as exceptions.
- Grant **home-zone immunity**: contact inside your own Alliance Zone is never a G415 violation — protecting scoring robots near their hub without protecting them everywhere.
- Escalate by consequence: "unable to drive ~20+ s" upgrades yellow to red.

Combined with the earlier reports, the designer's pitfall checklist gains three hard rules: (1) if game-piece size + robot size force intake-vs-intake proximity, write outcome-based contact rules from day one and give each alliance a protected zone; (2) any exploit lives in *wording* (Hero Heist's district-ownership ambiguity; 2026's "active hub" RP wording needing a TU01 patch) — run a red-team pass on every scoring definition before release; (3) publish scoring-settle timing, out-of-bounds piece handling (2026: staff return fuel at point of exit), and auto-tie randomization explicitly, because these are the questions a CADathon Q&A thread will ask first.

---

### Sources
- [frcmanual.com — 2026 Game Details](https://www.frcmanual.com/2026/game-details) · [2026 Arena](https://www.frcmanual.com/2026/arena) · [2026 Game Manual (TU22) PDF](https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf)
- [REBUILT Team Update 19](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate19.pdf) · [Combined Team Updates (TU01–TU22)](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate-Combined.pdf)
- [FIRST: 2026 Practice Field & Team Element Changes](https://community.firstinspires.org/2026-practice-field-team-element-changes) · [TE-26500 build instructions](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/TE-26500-build-instructions.pdf) · [FIRST Playing Field page](https://www.firstinspires.org/resources/library/frc/playing-field)
- [2026 AprilTag Images & User Guide](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-apriltag-images-user-guide.pdf) · [WPILib AprilTagFieldLayout](https://github.wpilib.org/allwpilib/docs/release/java/edu/wpi/first/apriltag/AprilTagFieldLayout.html) · [PhotonVision MultiTag](https://docs.photonvision.org/en/latest/docs/apriltag-pipelines/multitag.html) · [Limelight downloads](https://docs.limelightvision.io/docs/resources/downloads)
- [Wikipedia: Rebuilt (FIRST)](https://en.wikipedia.org/wiki/Rebuilt_(FIRST)) · [2026 REBUILT cheat sheet](https://www.firstinspires.org/hubfs/web/volunteer/frc/2026-rebuilt-cheat-sheet.pdf)
- Chief Delphi: [No Coopertition this year](https://www.chiefdelphi.com/t/no-coopertition-this-year/512825) · [Inactive-hub fuel and RPs](https://www.chiefdelphi.com/t/does-fuel-scored-while-a-hub-is-inactive-count-toward-fuel-based-ranking-points/510717) · [2026 Team Update 19 thread](https://www.chiefdelphi.com/t/2026-team-update-19/517726) · [Are you adding a climber for DCMP?](https://www.chiefdelphi.com/t/are-you-adding-a-climber-for-dcmp/518040) · [Worlds 2025 RP increases](https://www.chiefdelphi.com/t/worlds-2025-ranking-points-rps-increaces/498243)
- [FIRST blog: Coral Scoring Adjustments (2025)](https://community.firstinspires.org/coral-scoring-adjustments) · [TBA Blog: Making Better RP Predictions](https://blog.thebluealliance.com/2019/08/04/making-better-rp-predictions/)
