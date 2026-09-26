# SUMMIT PUSH — Organizer Guide

*For the mentors, judges and staff running a SUMMIT PUSH CADathon. Squads do not need this document: everything they receive is in `participants/`, and the event's public rules are the CADathon brief (`participants/02-cadathon/CADATHON-BRIEF.md`). This guide covers what the organizers do before, during and after the event.*

---

## 1. Roles

During the event the organizing mentor is the game authority, the Q&A desk and the head referee, and takes no part in design. There is no official judging or scoring: judging, the rubric, awards and the results show are optional (brief §5, §7), and run only if the organizers announce them at kickoff, in which case the judges are named then (brief §5.3). Mentors and alumni help only within the mentor-help rules in brief §3.2; an adult editing a squad's CAD document defeats the purpose of the event.

SUMMIT PUSH is a virtual project. The field, the ROBOTS and the vision system exist only in CAD and simulation: squads model the field from the drawing set (or build it with the Onshape field generator), check ROBOT designs with interference and motion studies, and run vision code against WPILib or PhotonVision simulation driven by `participants/04-vision/apriltag-field-layout.json`. The weigh-ins, referees and field staff in the manual are part of the game's fiction. Only documents are printed.

## 2. Before kickoff (Day −7 to −1)

1. **Announce the event and register squads.** Pair rookies with experienced students (brief §3.3). The announcement carries a theme teaser only.
2. **Release nothing design-relevant early.** The game, the field and the judging criteria are withheld until kickoff so that design starts from the released requirements.
3. **Decide whether to judge the event.** Judging is optional. If the event will be judged, name the judges (two or three, with a one-line background each) and set the results show date; both are announced at kickoff, and the show date is kept (§5). If it will not, say so at kickoff, and squads use the rubric as a self-check.
4. **Prepare the release.** The participant kit is the whole `participants/` folder. Check that its PDF, Markdown manual, drawings, Onshape Feature Studio and layout JSON are the current build (`organizers/README.md`, "Building and verifying").
5. **Decide how squads receive the kit.** This repository is public, so squads can read `organizers/` on their own, including this guide and the concept archive. Organizers who want to keep the reveal or the moderation notes private should hand out a copy of `participants/` directly (a zip file or a separate repository) and keep `organizers/` in a private copy.
6. **Print for kickoff:**
   - the game manual, `participants/01-game-manual/SUMMIT-PUSH-Game-Manual.pdf`: one copy per student, or at least one per subteam (Letter pages; print the Appendix A plates separately at ANSI C if a plotter is available). Reading it cover to cover is the first team activity, as on a real kickoff day;
   - a one-page reference sheet: the game summary from the repository `README.md` plus the Scoring Summary in manual Section 4.6 (Section 2.4 has a shorter version), printed large for the wall;
   - optionally, the field top view and CRAG sheets from `participants/03-field/drawings/` at 11 × 17 in for the strategy whiteboard, or at ANSI C (22 × 17 in) if the smallest note text must be readable.
7. **Set up the event server.** `organizers/discord/DISCORD-SETUP.md` gives the channel structure, roles, message templates, and the server icon and banner. The public Q&A channel and the read-only Team Updates channel are the ones the brief requires (§6).

## 3. Kickoff (Day 0)

Run the kickoff show as the brief's timeline describes: the game reveal, a Game Manual walkthrough, and the release of the field CAD, drawings and AprilTag layout. Publish the brief in full, and announce whether the event will be judged. If it will, the brief makes the rubric binding on the organizers (§5.3): it is final and public from Day 0, and no criteria are added, reweighted or reinterpreted afterwards. A public rubric helps rookie CAD teams set priorities and makes judging transparent; vague or hidden criteria are a common reason design challenges lose participants' trust. If it will not, the rubric still serves squads as a self-check. Open the Q&A desk.

## 4. During the build window (Days 1–14)

- **Strategy summaries (Day 3).** Reply to every posted summary with a short written check within 24 hours.
- **Office hours (Days 3, 5, 10, 12).** Answer design questions under the mentor-help rules. Use them to find squads that are stuck and point them to the BASECAMP BOT path (brief Appendix A) while there is still time to change course.
- **Mid-event design review (Days 7–8).** A 15-minute slot per squad, on the middle weekend, to walk through its in-progress CAD.
- **Q&A.** Answer in public only, within the turnaround in brief §6, and keep a public, cumulative answer sheet. Answers interpret the manual; they do not change it.
- **Team Updates.** Issue rule changes, and clarifications that change the manual text, only as numbered Team Updates, in the slots the brief sets (§6):
  1. Number updates in sequence (Team Update 01, 02, ...) and date each one. Post a "no changes" update on schedule if nothing changed.
  2. For each change, cite the rule number ("G404 is revised as follows: ..."), show deleted text struck through and added text in bold, and give a one-line rationale.
  3. Publish every update in the same channel, and add it to the kit as `participants/05-team-updates/TEAM-UPDATE-NN.md`. Each update amends the manual: the manual plus all updates is the current ruleset, and the most recent update governs where they conflict. The manual is not changed after Day 11 except to close a game-breaking exploit.
  4. To fold an update into the published documents, edit the manual sources, add a row to `organizers/source/typesetting/pdf/revisions.json`, rebuild the manual and the PDF, and record the change in `organizers/design/REVISION-LOG.md` (`organizers/README.md`, "Making a change"). The SUMMIT PUSH Training Use License lets organizers publish Team Updates for their own event.

## 5. Judging (optional, Days 15–21)

*Only if judging was announced at kickoff. There is no official judging or scoring otherwise; skip this section and the results show in §6.*

- Judges score independently against the rubric, then reconcile. A judge with a conflict (their own child or protégé on a squad) recuses from that squad's scoring.
- Score strategy built on Q&A-confirmed readings; strategy built on an unconfirmed exploit reading is scored as if the exploit did not exist (brief §6, spirit clause).
- Judge Design Feasibility within each squad's own resources (brief §5.2).
- Draft written feedback for every squad: per-criterion scores and at least one paragraph of narrative. It is a required organizer deliverable, equal in status to the squads' deadline.

Judging delays and missing feedback are the two failures that most damage participants' trust in events like this. Both have occurred in community design challenges: results published a month after the promised date, and notices that individual feedback would not be provided, which removes one of the main reasons to enter. When the event is judged, the judging window is one week, the show date is announced at kickoff, and written feedback for every squad is a required deliverable. If the organizers cannot staff that, reduce the size of the event, not the feedback.

## 6. Results show and after (optional, Day ~22)

- If the event is judged, run the live, ranked feedback show (every submission shown, bottom-up reveal, verbal feedback on every entry, awards presented; brief §7), and deliver the written feedback the same night. If it is not, an unranked showcase of the entries is an optional alternative.
- If People's Choice was announced, tally it from the peer ballots.
- Archive the strongest entries (the Winner and Best Rookie Squad, if awards were given) in the team's design library as reference examples.
- Release the design-phase archive now, if at all. `organizers/archive/research/` gives nothing away and can be shared at any time. Hold back `organizers/archive/concepts/` until the results show: `FIRST-ASCENT.md` is the concept that became SUMMIT PUSH and still carries v1.0 geometry and scoring, including a Summit Socket on the spire at rim 66 in that v2.0 moved to the SHELF FACE at 72. Handed out early, it spoils the reveal and gives students a superseded ruleset; after the results it makes a good design retrospective, labeled as a v1.0 archive.
