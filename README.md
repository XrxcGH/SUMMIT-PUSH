# SUMMIT PUSH — Complete Offseason Game Package

## The Game

The forecast window is closing. In SUMMIT PUSH, two three-robot expedition ALLIANCES race up opposite flanks of the same peak, ferrying CACHE CRATES, O2 CELLS, and ROPE COILS to their alliance's CRAG — a scoring spire at midfield that scores on all four faces and comes alive, tier by LED tier, as CAMPS are established. A randomized FORECAST doubles one supply type in AUTO and sets which type the ROPED UP bonus demands two of, forcing genuinely branching autonomous routines. Each alliance's chosen ROUTE DECLARATION raises one CAMP bonus for the whole match, with the uplift scaled by tier difficulty so that no declaration dominates: strategy that can be scouted, not luck that has to be endured. In the final 30 seconds, all six robots hit the HEADWALLS — three side-by-side lanes of staggered rungs on a 15°-leaning truss — where a 30-point SUMMIT RUNG grab on the buzzer can flip a match without invalidating two minutes of cycling.

---

## Quick Game Summary

> **Format:** 3v3 · 2:30 match (0:15 AUTO / 2:15 TELEOP, final 0:30 ENDGAME)

> **Supplies:** CACHE CRATE (12 in cube), O2 CELL (5 × 14 in cylinder), ROPE COIL (10 in ring) — 21 of each

> **Placement pays by tier, not by piece:** Low tier (24/30/30 in) 4 pts · Mid tier (42/54/54 in) 7 pts · High tier (72/78 in) 10 pts · BASE DEPOT 2 pts. AUTO values are 7 / 10 / 13 / 4.

> **Camp bonuses:** CAMP I +6 · CAMP II +10 · HIGH CAMP +15 — the declared ROUTE's camp pays +18 / +24 / +35 instead. Each CAMP wants one SCORED SUPPLY of every type its tier offers

> **Endgame:** climb the HEADWALL — PARK 3 / LEDGE RUNG 12 / CAMP RUNG 20 / SUMMIT RUNG 30, three independent lanes per alliance

> **Bonus RPs:** SUPPLY LINE (volume), EXPEDITION (camps), ASCENT (climbs) — escalating thresholds by tournament tier

---

## Package Map

| Path | What it is |
|---|---|
| `README.md` | This file — the package front door and organizer's guide. |
| `REVISION-LOG.md` | Every change from v1.0 through v2.2, with the reasoning and the arithmetic behind it. Sections A–I are the v1.0 → v2.0 pass, J a self-review of v2.0, K and L the adversarial re-audit that produced v2.1, and M a third pass that audited those fixes and produced v2.2. |
| `verify/` | The verification suite — five checks over the numbers, the cross-references, cross-document agreement, and the drawing sheets. `bash verify/run-all.sh` rebuilds everything and runs them all. |
| `00-research/` | The design-research foundation: decades of community sentiment around competitive robotics games, distilled into the game-quality rubric the package was judged against. |
| `00-concepts/` | The five-concept slate from the design phase (internal archive): the approved concept that became SUMMIT PUSH plus four runners-up and three judging reports. Working documents; not part of the published release. |
| `01-design/DESIGN-SPEC.md` | The **locked design specification** — the single source of truth. Every number, name, and rule in the package traces here. Where any document disagrees with the spec, the spec wins. |
| `02-manual/GAME-MANUAL.md` | The full game manual (compiled): Introduction, Game Overview, ARENA, Match Play & Scoring, G-rules, R-rules, Inspection, Tournament, and Glossary. |
| `02-manual/sections/` | The manual's source sections, one file per section. |
| `02-manual/manual-header.md` | The compiled manual's front matter — title, version, contents — prepended by the build. |
| `02-manual/build.sh` | Compiles the header and sections into `GAME-MANUAL.md`. Run it after any section edit. |
| `03-field/FIELD-CAD-PACKAGE.md` | The authoritative CAD geometry specification for every field element, with a master dimension ledger every drawing and document traces to. |
| `03-field/MATERIALS-AND-COLORS.md` | Appearance specification: material, color (with hex), finish, and section for every ARENA element and game piece. |
| `03-field/renderings/*.svg` | 6 dimensioned multi-view drawing sheets: field top view, CRAG, HEADWALL, OUTFITTER, game pieces with clearance studies, and the AprilTag map. |
| `03-field/renderings/generate_drawings.py` | Generates all six sheets from the master dimension ledger. Re-run after any geometry change; do not hand-edit the SVGs. |
| `03-field/renderings/_drawlib.py` | The drawing helper library the generator imports — sheet framing, dimensions, leaders, title blocks, palette. |
| `04-vision/VISION-GUIDE.md` | The 26-tag AprilTag layout (36h11), mounting geometry, tag-to-target transforms, and simulation guidance. |
| `04-vision/apriltag-field-layout.json` | WPILib-schema tag layout (meters, always-blue-origin NWU) — drops straight into vision simulation. |
| `05-cadathon/CADATHON-BRIEF.md` | The design challenge itself: structure, timeline, deliverables, and the judging rubric. |
| `06-style/MANUAL-STYLE-GUIDE.md` | The typesetting standard for producing a print-quality PDF edition of the manual from these Markdown sources (`research-notes.md` alongside it holds the underlying research). |

---

## How to Use This Package

**This is a virtual-only project.** Everything in this package — the field, the robots, the vision system — lives in CAD and in simulation. Nothing is fabricated: the field is reproduced in CAD from the drawing set, robot designs are validated with interference and motion checks, and vision work runs against WPILib/PhotonVision simulation driven by `04-vision/apriltag-field-layout.json`. The events described in the Game Manual — weigh-ins, referees, field staff — are part of the game's fiction; only documents are printed, and only for reading.

### Read order

1. **`01-design/DESIGN-SPEC.md`** first. It is short, dense, and governing. Everything else elaborates it.
2. **`02-manual/GAME-MANUAL.md`** — the document students will actually live in.
3. **`05-cadathon/CADATHON-BRIEF.md`** — how the event runs and how entries are judged.
4. **`03-field/` and `04-vision/`** as field-modeling and software needs arise.
5. `00-concepts/` and `00-research/` are background — read them to understand *why* the game is shaped the way it is, or to run a design retrospective with students. Note that `00-concepts/` is a v1.0 archive: its geometry and scoring are superseded by the specification, and it should not be handed to students before the results show.

### Kickoff day — what to print

- **The full game manual**, one copy per student or at minimum one per subteam. Reading the manual cover to cover is the first team activity, exactly as on a real kickoff day.
- **A one-page at-a-glance sheet** — the Quick Game Summary box above plus the Scoring Summary from Manual Section 4.6 (quick reference in 2.4). Print it large and tape it to the wall.
- Optionally, the field top view and the CRAG elevations from `03-field/renderings/` at 11 × 17 for the strategy whiteboard.

### What to publish to students vs. hold back

Publish **everything at kickoff, including the judging rubric** in `05-cadathon/CADATHON-BRIEF.md`. The brief makes this a binding organizer commitment (§5.3): the rubric is final and public from Day 0, with no criteria added, reweighted, or reinterpreted after kickoff. A public rubric reduces anxiety, helps rookie CAD teams prioritize, and makes judging transparent rather than arbitrary. The research on failed design challenges is unambiguous: vague or hidden criteria kill trust.

Some community events withhold judging criteria so that students design for the game rather than the rubric — a defensible choice elsewhere, but not this event's. The only thing held back before Day 0 is the game itself: no design-relevant material releases early. `00-research/` can be published freely; it spoils nothing and makes excellent "how games get designed" reading. `00-concepts/` cannot: `FIRST-ASCENT.md` is the approved concept that became SUMMIT PUSH and still carries v1.0 geometry and scoring, including a Summit Socket on the spire at rim 66 in that v2.0 moved to the SHELF FACE at 72. Publishing it both spoils the reveal and puts a superseded ruleset in students' hands. Release it after the results show, labelled as a v1.0 archive.

### Modeling the field

Work from **`03-field/FIELD-CAD-PACKAGE.md`** (the geometry spec and master dimension ledger) with the **`03-field/renderings/`** SVGs as the drawing set, and **`03-field/MATERIALS-AND-COLORS.md`** for appearance. Key practices:

- Model in the spec's coordinate frame: always-blue-origin NWU, origin at the right corner of the Blue alliance wall, +X toward Red. Every element position in the spec and the AprilTag JSON uses this frame, so a consistent origin means vision simulation works against the model unmodified.
- Hold the strictly toleranced dimensions exactly, above all the O2 socket ID of 6.50 ± 0.125 in. Every other robot-critical dimension lands on a round or half-inch value, and all angles are 15/30/45°, so the field models quickly.
- Model the Blue half once, then rotate-pattern 180° about field center. Never model the second CRAG or HEADWALL twice.
- Validate the finished field model: run interference and clearance checks against the toleranced dimensions, and drive WPILib/PhotonVision simulation with `04-vision/apriltag-field-layout.json` to confirm the tag poses match the model.

### Producing the PDF edition

The Markdown sources are the working format. `06-style/MANUAL-STYLE-GUIDE.md` specifies page setup, palette, typography, rule anatomy, table and figure conventions, and a production recipe for typesetting a print-quality PDF that reads like a real competition manual — without copying any organization's trademarks or brand assets.

### Issuing Team Updates

Run updates with the discipline of a real season. When a rules question, wording exploit, or field-model discrepancy surfaces during the event:

1. Number updates sequentially (**Team Update 01, 02, …**) with a date.
2. Show changed manual text with strikethrough for deletions and bold for additions, citing the rule number ("G404 is revised as follows…").
3. Publish to the same channel every time, on a predictable cadence, and treat each update as amending the manual — the manual plus all updates is the current ruleset.
4. Keep a running Q&A log for questions that need answers but not rule changes.

The design specification stays frozen unless the organizer deliberately changes a design decision — updates are for clarifications and fixes, not redesigns. Every such change belongs in `REVISION-LOG.md`.

---

## Design Provenance

SUMMIT PUSH began with a research phase that distilled decades of community sentiment around competitive robotics games — what players, mentors, and spectators consistently praise and punish in game design — into an explicit game-quality rubric (`00-research/`). Five complete game concepts were then developed against that rubric (`00-concepts/`), scored by a three-judge panel, and SUMMIT PUSH emerged as the winner, absorbing a judge-directed fix package plus two mechanics grafted from the runner-up concept SUMMIT SIGNAL (anti-pollution scoring and beacon ignition). The result was locked into `01-design/DESIGN-SPEC.md`, from which every document in this package was authored, and revised to v2.0 after a full geometric, rules, and balance audit, then to v2.1 after a second, adversarial audit run against v2.0 itself, and then to v2.2 after a third pass that audited the second pass's own fixes — all recorded in `REVISION-LOG.md`.

SUMMIT PUSH is an original work produced independently as a student training exercise. It is not affiliated with, endorsed by, or derived from the branding of any robotics competition organization.
