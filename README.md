# SUMMIT PUSH

SUMMIT PUSH is an original offseason game for competitive-robotics design training. It follows the conventions of modern three-versus-three robotics competitions and is played virtually: teams design ROBOTS in CAD against a field that exists as a CAD model, and test vision code in simulation. The game is the basis of a CAD design challenge, the SUMMIT PUSH CADathon, and this repository holds both sides of it: the kit that participating squads receive, and the materials used to create and run the challenge.

## Game summary

Two ALLIANCES of three ROBOTS carry three kinds of SUPPLIES (CACHE CRATES, O2 CELLS and ROPE COILS) to their own CRAG, a scoring tower on the FIELD centerline with scoring positions on all four faces. LED tier rings on the CRAG light as the ALLIANCE establishes CAMPS. At the start of AUTO a random FORECAST doubles the AUTO placement value of one SUPPLY type and sets which type the ROPED UP bonus needs two of, so an AUTO routine that goes for the bonus needs a branch for each FORECAST.

During MATCH setup each ALLIANCE makes a ROUTE DECLARATION, which raises one CAMP bonus for the whole MATCH. The increase is scaled to the difficulty of the tier, and the declaration is shown on the FIELD LEDs so that opponents can scout it. The final 30 seconds are ENDGAME, when the HEADWALL ZONES are protected and all six ROBOTS can climb at once, three to a HEADWALL. Each HEADWALL is a truss leaning back 15° with three side-by-side lanes of staggered rungs, and a climb to the SUMMIT RUNG is worth 30 points.

| | |
|---|---|
| **Format** | 3v3. 2:30 MATCH: 0:15 AUTO, then 2:15 TELEOP, of which the final 0:30 is ENDGAME. |
| **SUPPLIES** | CACHE CRATE (12 in cube), O2 CELL (5 × 14 in cylinder), ROPE COIL (10 in ring); 21 of each. |
| **Placement** | Every position in a tier is worth the same, whatever the SUPPLY type. TELEOP: Low tier (24 / 30 / 30 in) 4 pts, Mid tier (42 / 54 / 54 in) 7 pts, High tier (72 / 78 in) 10 pts, BASE DEPOT 2 pts. AUTO: 7 / 10 / 13 / 4. |
| **CAMP bonuses** | CAMP I +6, CAMP II +10, HIGH CAMP +15; the declared ROUTE's CAMP pays +18 / +24 / +35 instead. Each CAMP needs one SCORED SUPPLY of every type its tier accepts. SUMMIT BEACON +10 when all three CAMPS are established. |
| **AUTO extras** | LEAVE 3 per ROBOT. The FORECAST doubles the PRIORITY SUPPLY's AUTO placement value. ROPED UP +10. |
| **ENDGAME** | PARK in BASECAMP 3; HEADWALL climb to the LEDGE RUNG 12, CAMP RUNG 20, SUMMIT RUNG 30. Three independent lanes per ALLIANCE. |
| **Fouls** | MINOR FOUL +3, MAJOR FOUL +8, to the opposing ALLIANCE. |
| **Bonus RPs** | SUPPLY LINE (SUPPLIES SCORED), EXPEDITION (CAMPS established), ASCENT (ENDGAME points). Thresholds rise with tournament tier (manual Section 4.7). |

## Where to start

| You are | Start here | Contents |
|---|---|---|
| **A squad entering the CADathon** | [`participants/`](participants/README.md) | The Game Manual (PDF and Markdown), the CADathon brief (with its optional judging rubric), the Team Updates, the field CAD package, drawings and Onshape field generator, and the AprilTag vision guide and layout file. |
| **An organizer, judge or mentor running the event** | [`organizers/`](organizers/README.md) | The organizer guide (release plan, Q&A and Team Updates, optional judging and results), the Discord server setup, the design specification and revision log, the sources and build tools for every participant file, the verification suites, and the design-phase research and concept archive. |

The participant kit is self-contained: nothing in `participants/` depends on `organizers/`.

## Provenance and independence

SUMMIT PUSH began with a research phase that reviewed community opinion of competitive-robotics games over several decades, recording what players, mentors and spectators praise and criticize, and turned it into a game-quality rubric (`organizers/archive/research/`). Five game concepts were developed against that rubric (`organizers/archive/concepts/`) and scored by a panel of three judges. The winning concept became SUMMIT PUSH. It took on a set of fixes the judges asked for and two mechanics from the runner-up concept, SUMMIT SIGNAL: anti-pollution scoring and beacon ignition. The result was locked into `organizers/design/DESIGN-SPEC.md`, from which every document in the package was written. The package was revised to v2.0 after a full geometry, rules and balance audit, to v2.1 after an adversarial audit of v2.0, and to v2.2 after a third pass that audited the v2.1 fixes. `organizers/design/REVISION-LOG.md` records every change.

SUMMIT PUSH is an original work produced independently as a student training exercise. It is not affiliated with, endorsed by, or derived from the branding of any robotics competition organization.

## License

Copyright © 2026 Eric Dean. All rights reserved. The package may be used, printed and shared unmodified for training and educational purposes, including running or entering the CADathon, with credit to the author, under the SUMMIT PUSH Training Use License in [`LICENSE.md`](LICENSE.md). Commercial use, distributing modified versions, and machine-learning use need written permission. Third-party components (the vendored fonts, the AprilTag 36h11 patterns, and packages the build tools download) keep their own licenses, listed in section 6 of `LICENSE.md`.
