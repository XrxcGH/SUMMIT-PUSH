# SUMMIT PUSH — Participant Kit

Everything a squad needs for the SUMMIT PUSH CADathon: the game, the event rules, the field and the vision layout. SUMMIT PUSH is played virtually. The field, the ROBOTS and the vision system exist only in CAD and simulation: you model the field (or build it with the Onshape field generator), design your ROBOT against it, and run vision code against simulation driven by the AprilTag layout file. The weigh-ins, referees and field staff in the manual are part of the game's fiction.

| Folder | Contents |
|---|---|
| `01-game-manual/` | The Game Manual: `SUMMIT-PUSH-Game-Manual.pdf` (the typeset edition, with the six drawing sheets as plates in Appendix A) and `GAME-MANUAL.md` (the same text in Markdown, with its figures in `figures/`). |
| `02-cadathon/` | `CADATHON-BRIEF.md`: how the event runs, the two-week timeline, the deliverables, and the optional judging rubric and awards. |
| `03-field/` | `FIELD-CAD-PACKAGE.md` (the geometry of every field element and the master dimension ledger), `MATERIALS-AND-COLORS.md` (appearance), `drawings/` (six dimensioned drawing sheets) and `onshape/` (a Feature Studio that builds the whole field in Onshape). |
| `04-vision/` | `VISION-GUIDE.md` (the 26-tag AprilTag layout, mounting geometry, occlusion analysis and simulation guidance) and `apriltag-field-layout.json` (the layout in the WPILib `AprilTagFieldLayout` schema). |
| `05-team-updates/` | The numbered Team Updates, each amending the manual and the kit since the kickoff release. Read every one: the manual plus all Team Updates is the current ruleset. |

## Read order

1. **The Game Manual**, cover to cover. It is the rulebook, and where any other document seems to disagree with it, the manual governs.
2. **The CADathon brief**, for the deadline and the deliverables (judging is optional and happens only if the organizers announce it). Start your strategy work with the BASECAMP BOT benchmark in its Appendix A.
3. **The Team Updates** in `05-team-updates/`, which amend the manual.
4. **The field and vision folders**, when modeling and vision work begin.

## Modeling the field

Work from `03-field/FIELD-CAD-PACKAGE.md`, with the sheets in `03-field/drawings/` as the drawing set and `03-field/MATERIALS-AND-COLORS.md` for appearance. To build the field in Onshape without modeling it by hand, paste `03-field/onshape/SummitPushField.fs` into a Feature Studio and add the SUMMIT PUSH Field feature to a Part Studio; `03-field/onshape/README.md` gives the steps.

When modeling by hand:

- Use the package's coordinate frame, always-blue-origin NWU: origin at the right corner of the Blue alliance wall, +X toward Red. The AprilTag JSON uses the same frame, so vision simulation runs against the model without changes.
- Hold the O2 socket ID of 6.50 ± 0.125 in, the tightest tolerance on the field. Most other robot-critical dimensions are whole or half inches, and the angles are 15°, 30° and 45°, so the field models quickly.
- Model the Blue half once, then pattern it 180° about field center for Red. Do not model the Red CRAG or HEADWALL separately.
- Check the finished model: run interference and clearance checks against the toleranced dimensions, and drive WPILib or PhotonVision simulation with `04-vision/apriltag-field-layout.json` to confirm that the tag poses match the model.

## Questions and Team Updates

Ask rules questions in the event's public Q&A channel, citing the rule number (brief §6). Answers are public and interpret the manual. Changes to the manual arrive only as numbered Team Updates, posted in the event's Team Updates channel and kept in `05-team-updates/`; the manual plus every Team Update is the current ruleset.

## Credit and license

SUMMIT PUSH © 2026 Eric Dean. All rights reserved. You may use, print and share these materials unmodified for training and educational purposes, including entering the CADathon, under the SUMMIT PUSH Training Use License (`LICENSE.md` at https://github.com/XrxcGH/SUMMIT-PUSH). Your own designs remain yours. When you post an entry that includes the field model or other SUMMIT PUSH material, include this credit line:

> SUMMIT PUSH © 2026 Eric Dean. Used under the SUMMIT PUSH Training Use License: https://github.com/XrxcGH/SUMMIT-PUSH
