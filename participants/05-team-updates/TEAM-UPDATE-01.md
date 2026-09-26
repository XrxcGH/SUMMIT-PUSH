# SUMMIT PUSH — Team Update 01

**Date:** 2026-09-25 · **Amends:** Version 2.2 as released at kickoff (TU-00)

*The Game Manual plus every Team Update is the current ruleset; where they conflict, the most recent update governs. Each change below gives the rule or section, the old text struck through, the new text in bold, and a one-line rationale. The published documents (the Markdown and PDF manual, the brief, the Field CAD Package, the drawings and the Onshape generator) already incorporate this update.*

**Summary.** The CACHE CRATE and ROPE COIL gain a published compression tolerance, and the O2 CELL becomes fully rigid. The design challenge now runs two weeks instead of nine days. There is no official judging or scoring: the judging sections of the brief are optional and apply only if the organizers announce judging at kickoff. Several figures and drawing sheets are corrected editorially; no dimension, scoring value or rule number changes.

---

## A. Game Manual

### A1. Section 3.6, Table 3-4 (O2 CELL official construction)

~~4.0-in OD rigid tube core, 0.5-in EVA foam sleeve, molded foam caps~~

**rigid molded shell: thick-wall ABS tube with rigid molded ABS domed caps, no foam**

*Rationale:* the O2 CELL is now perfectly rigid, so it has no foam layer.

### A2. Section 3.6, Table 3-4 (new row: Compression tolerance)

| | CACHE CRATE | O2 CELL | ROPE COIL |
|---|---|---|---|
| **Compression tolerance** | **compliant: compresses up to 2.0 in across any pair of opposing faces (13.0-in crowned envelope → 11.0 in) under a squeeze of up to 15 lbf, crowns first; recovers fully when released** | **rigid: does not compress (zero compression tolerance)** | **compliant: tube section compresses up to 0.5 in (2.5 → 2.0 in) under a pinch of up to 10 lbf; the ring ovalizes up to 1.0 in across the OD (10.0 → 9.0 in) under a diametral squeeze of up to 5 lbf; recovers fully when released** |

*Rationale:* gripper design needs a stated squeeze limit for the two foam SUPPLIES, and a statement that the O2 CELL gives nothing.

### A3. Section 3.6 (new paragraph after "All three SUPPLY types are durable enough to be driven over...")

**The CACHE CRATE and the ROPE COIL are compliant: a ROBOT or a HUMAN PLAYER may squeeze either one within its compression tolerance in normal handling, and it recovers its shape when released. The O2 CELL is rigid, so a mechanism that grips it must supply its own compliance. Every fit, clearance and envelope in this manual and in the Field CAD Package is computed at nominal, uncompressed size: compression is margin, not budget.**

*Rationale:* no published clearance changes; compression is never credited toward a fit (for example the 0.78-in shelf-slot clearance).

### A4. G203 *Do not alter SUPPLIES*

HUMAN PLAYERS may not deform SUPPLIES to change how they feed or score, for example by pre-folding a ROPE COIL flat or ~~denting an O2 CELL cap.~~ **crushing a CACHE CRATE beyond its compression tolerance. Squeezing a CACHE CRATE or a ROPE COIL within its compression tolerance (Section 3.6) in normal handling does not alter it.**

*Rationale:* a rigid O2 CELL cannot be dented, and normal squeezing of a compliant SUPPLY must not read as alteration. The violation is unchanged.

### A5. Section 1.1, Interpretation

Referees, and in a ~~design challenge~~ **judged design challenge** the judges, enforce the rules as written.

*Rationale:* there is no official judging (see C2).

### A6. R303 *Budget realism*, Violation

~~An entry is penalized at judging per the published rubric;~~ **In a judged design challenge, an entry is penalized per the published rubric;** at a physical event, the ROBOT will not pass INSPECTION.

*Rationale:* as A5.

### A7. Section 7.4, Design-Entry Self-Inspection Checklist (opening paragraph)

Design-challenge entries are ~~judged~~ **reviewed** from their submissions. In place of physical INSPECTION, every entry must include a self-inspection page in its submission that demonstrates the items below. ~~Judges treat~~ **In a judged design challenge, judges treat** a missing or unsupported item as an inspector treats a failed check.

*Rationale:* as A5. The self-inspection page is still a required part of every entry.

### A8. Section 8.5, first bullet

~~**Entries are judged against the Championship column.** Where bonus RP thresholds escalate by tier, a judging rubric evaluates a design's credible performance against the Championship column of the Section 4.7 table. A design that can reach only the Regional thresholds is judged as a Regional-level design.~~

**Entries are designed against the Championship column.** **Where bonus RP thresholds escalate by tier, a design is measured by its credible performance against the Championship column of the Section 4.7 table, as is any judging rubric an event chooses to use. A design that can reach only the Regional thresholds is a Regional-level design.**

*Rationale:* as A5. The Championship column remains the design standard.

### A9. Figures 2-1 and 3-1 to 3-5 (editorial)

Re-rendered from the unchanged field model. In Figure 3-5 (CENTER CACHE) the figure finisher had whitened the lit carpet, so the white tape marks disappeared into it. The other figures had white blotches on the translucent wall panels.

*Rationale:* the figures now show the field as modeled. No geometry changed.

### A10. Appendix A plates (Drawings 1, 2 and 5, editorial)

- **Drawing 1 (FIELD top view):** the 2-in white FIELD centerline tape, and its tape-key swatch, are drawn with a grey casing, so the tape no longer vanishes into the carpet tint.
- **Drawing 2 (CRAG), View D:** the LOW and MID socket labels are moved clear of their socket circles.
- **Drawing 5 (SUPPLIES):** the sheet note now reads "model rigid at nominal (uncompressed) size". The CACHE CRATE and ROPE COIL gain their compression tolerances (A2), and the O2 CELL note ~~4.0 OD rigid core, 0.5 EVA sleeve (ref)~~ now reads **RIGID molded ABS shell and caps, no foam: zero compression**.

*Rationale:* legibility, plus A1–A2 on the SUPPLY sheet.

---

## B. Field CAD Package, materials and Onshape generator

### B1. Field CAD Package §9.1 CACHE CRATE

Skinned-foam construction~~; model rigid at nominal size.~~ **, compliant: compression tolerance 2.0 in across any pair of opposing faces (13.0-in crowned envelope → 11.0 in) under a squeeze of up to 15 lbf between flat plates; the crowns flatten first, and the CRATE recovers fully when released. Model rigid at nominal size. Every fit and clearance in this package is computed uncompressed, so compression is margin, not budget: the 0.78-in slot clearance below does not count on it.**

### B2. Field CAD Package §9.2 O2 CELL

~~Rigid tube core with a foam sleeve; model rigid at nominal size.~~ **Rigid molded shell (thick-wall ABS tube with rigid molded ABS domed caps, no foam): rigid, zero compression tolerance. Model rigid at nominal size; a gripper must supply its own compliance.**

### B3. Field CAD Package §9.3 ROPE COIL

Molded rubber/foam ring, ~~semi-compliant; model rigid at nominal size.~~ **compliant: the tube section compresses up to 0.5 in (2.5 → 2.0 in) under a pinch of up to 10 lbf, and the ring ovalizes up to 1.0 in across the OD (10.0 → 9.0 in) under a diametral squeeze of up to 5 lbf, which narrows the hole by the same 1.0 in (5.0 → 4.0 in, still 2.5 in larger than the 1.5-in peg). It recovers fully when released. Model rigid at nominal size.**

### B4. MATERIALS-AND-COLORS.md, O2 CELL row

Material ~~Rigid tube core, EVA foam sleeve, molded caps~~ **Rigid molded ABS shell and domed caps, no foam**; finish ~~satin foam~~ **satin rigid plastic**. Colors are unchanged.

### B5. Onshape field generator (`03-field/onshape/SummitPushField.fs`)

The O2 CELL mass-body label ~~Rigid core, EVA sleeve, molded caps~~ now reads **Rigid molded ABS shell and caps**. Geometry and mass are unchanged, so a field already built with the kickoff generator does not need rebuilding.

*Rationale (B1–B5):* these carry A1–A3 into the field documents.

---

## C. CADathon brief (`02-cadathon/CADATHON-BRIEF.md`)

### C1. Event length: two weeks

§1: "a ~~nine-day~~ **two-week** design sprint"; "~~Nine days~~ **Two weeks** forces scoping decisions".

§2: ~~The event runs nine days across two weekends~~ **The event runs two weeks, from the kickoff on Day 0 (a Saturday) to the submission deadline at the end of Day 14, the Saturday two weeks later.** The timeline table is replaced:

| Item | Old | New |
|---|---|---|
| Strategy summary (recommended) | ~~Day 2 (Mon)~~ | **Day 3 (Tue)** |
| Office hours | ~~Days 3, 4, 6 (three sessions)~~ | **Days 3, 5, 10, 12 (four sessions)** |
| Team Update 01 slot | Day 4 (Wed) | **Day 4 (Wed)**, unchanged |
| Team Update 02 slot | ~~Day 5 (Thu)~~ | **Day 9 (Mon)** |
| Mid-event design review | ~~Day 5 (Thu)~~ | **Days 7–8 (middle weekend)** |
| Last call for guaranteed rules answers; emergency updates through | ~~Day 6 (Fri)~~ | **Day 11 (Wed)** |
| Submission deadline, 11:59 PM local | ~~Day 8 (Sun)~~ | **Day 14 (Sat)** |
| Judging week | ~~Days 9–14~~ | ***optional:* Days 15–21** |
| Results and feedback show | ~~Day ~15~~ | ***optional:* Day ~22** |

§4, §5.3 and §6 follow the new days: deliverables are due by the Day 14 deadline; the manual is not changed after ~~Day 6~~ **Day 11** except to close a game-breaking exploit.

*Rationale:* organizer decision: a two-week build window.

### C2. No official judging or scoring

New notice under the title: **There is no official judging or scoring. The sections on judging, scoring, rankings and awards (§5, §7, and the judging and results rows of §2) are optional. They apply only if the organizers announce at kickoff that the event will be judged. Without that announcement, entries are not scored, ranked or awarded, and squads can use the rubric in §5 as a self-check.**

§5 becomes **Judging Rubric (optional)** and §7 **Awards (optional)**, each with the same notice. The §5.3 transparency commitments bind the organizers **if the organizers announce judging**. Sentences elsewhere that assumed judging (§1, §3.3, §4.1 to §4.4, §6 spirit clause, §7 prizes) now say "if the event is judged", or describe the same standard without a score. The deliverables, the Q&A rules and the mentor-help rules are unchanged.

*Rationale:* organizer decision: no official judging.

### C3. §4.1, new bullet

**Grippers sized to the SUPPLIES as specified.** **The CACHE CRATE and ROPE COIL are compliant and the O2 CELL is rigid (Game Manual Section 3.6, as amended by Team Update 01). A mechanism may squeeze a compliant SUPPLY only within its compression tolerance, and must carry its own compliance for the O2 CELL.**

*Rationale:* carries A2–A3 into the deliverable requirements.

### C4. §6, Team Updates

Updates are **posted in the event's Team Updates channel and kept in the kit as `05-team-updates/TEAM-UPDATE-NN.md`**.

*Rationale:* tells squads where to find every update.
