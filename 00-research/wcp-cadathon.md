# wcp-cadathon

## KEY TAKEAWAYS
- The WCP CADathon is a week-long annual offseason FRC design competition: WCP releases a fictional game (full FRC-style manual + Onshape field CAD + score calculator, and in 2025 a MoSim Unity simulator), teams CAD a robot and write a tech binder in ~7 days, and judges rank public submissions weeks later.
- Two editions so far: DunkTank (Oct 2024, won by 8033 Highlander Robotics) and Hero Heist (Nov 2025, 100+ entries, won by 5458 Digital Minds). Hero Heist's three robot classes (Commander/Mystic/Gadgeteer) forced a strategic pre-design choice that participants found compelling.
- Deliverables are exactly two things: robot CAD (Onshape required in 2025) and a PDF tech binder covering strategy, robot function, and engineering rationale — all posted publicly to the Chief Delphi thread, which creates a shared library of 100+ designs.
- Judging rewards strategy-first design: criteria are strategic analysis quality, feasibility/practicality (judged within a team's resource capacity), documentation effectiveness, and bonus creativity with WCP parts. Winner citations consistently emphasize points modeling and decision rationale over raw CAD polish.
- Team rules: max 2 entries per FRC team, 1 mentor per 2 students, students expected to do at least half the work (honor system); cross-team collabs, solo entries, and alumni are common and accepted. Q&A runs directly through the CD thread with the game designer (Andrew Lawrence) answering.
- Prizes are identity-level: 1st place gets a TeamWCP sponsorship (passed down if a past winner repeats), plus WCP/Fabworks gift cards, a Bambu P1S for People's Choice, and (2024) a Best Onshape Submission award with a PTC grant.
- The community-run F4 CADathon (12+ events, sponsored by WCP) pioneered the format and its best practices: formal Q&A forms with public answer sheets, mid-event Team Updates, team-size caps for fairness, and a live ranked-feedback results show on FUN's Twitch — still the gold standard for judging transparency.
- Biggest participant frustrations with WCP's version: judging delays (2025 results slipped a month, landing 3 days before kickoff; People's Choice still unannounced 7 months later) and dropping individual feedback in 2025 'due to bandwidth' after providing it in 2024.
- What makes a CADathon good per participants: complete kickoff-quality release materials, fast authoritative rules Q&A, transparent judges/criteria, individual feedback, public submissions, a ~1-week window timed in November, and games with real strategic depth. What kills trust: unnamed judges, vague criteria, no resource limits, mentor-stacked teams vs. students, and ambiguous scoring rules (Hero Heist's district-ownership wording briefly implied a 20-30 point exploit).
- Contrast with other offseason activities: Ri3D is a 72-hour physical build after real kickoff (demonstration, not judged); Behind the Bumpers is FUN's robot interview series (content, not a challenge); many teams (226, 271) now use the WCP CADathon as their rookie design-training capstone, supported by the frcdesign.org/David's Design Server community.
- Timeline design matters: F4's original 3-day format was permanently extended to 1 week; a November window (post-offseason comps, pre-build season) measurably boosted participation vs. early October.

## REPORT
# The WCP CADathon: In-Depth Research Report

## 1. What the WCP CADathon Is

The WCP CADathon is an annual, week-long offseason FRC design competition run by WestCoast Products (WCP), one of the major FRC COTS vendors. Teams are given a fictional FRC-style game (with a full game manual and field CAD), and have roughly **one week** to design a complete robot in CAD and produce documentation explaining their strategy and engineering decisions. Judges evaluate submissions and announce winners a few weeks later. WCP's stated goal for its first event was "to connect with the community in a fun and exciting way" ([WCP CADathon 2024: DunkTank — Chief Delphi](https://www.chiefdelphi.com/t/wcp-cadathon-2024-dunktank/472262); [wcproducts.com/pages/cadathon](https://wcproducts.com/pages/cadathon)).

The broader "CADathon" concept predates WCP: the community-run **F4 CADathon** series (12+ events, 2017–2022) popularized the format and defined it as "like a hackathon but with CAD. People/teams are given a short period of time to CAD a specific thing (in this case a robot) ending with a panel of judges selecting a winner" ([9th F4 CADathon — Rolling Rampage](https://www.chiefdelphi.com/t/9th-f4-cadathon-rolling-rampage-rankings-archives-available/386821)). Notably, Andrew Lawrence (Andrew_L on CD), who designed both WCP CADathon games, was an active voice in the earlier CADathon ecosystem, and the WCP events are effectively the professionalized successor to F4's community events.

There have been two WCP CADathons so far:
- **2024: "DunkTank"** — first annual, October 2024
- **2025: "Hero Heist"** — second annual, November 2025

## 2. How It Runs: Timeline, Teams, Organization

### Timeline (both years)
| Phase | DunkTank 2024 | Hero Heist 2025 |
|---|---|---|
| Announcement/theme reveal | 9/30/24 | 11/1/25 |
| Game reveal (start) | 10/4/24, 12pm PST | 11/10/25, ~1–2pm PT |
| Submission deadline | 10/13/24, 11:59pm PST | 11/17/25, 11:59pm PST |
| Results (scheduled) | 11/1/24 | 12/3/25 |
| Results (actual) | ~11/22/24 | 1/6/26 (delayed) |

The design window is **about one week** (2024's was slightly longer, ~9 days). Results follow after a multi-week judging period. In 2025 judging slipped badly — results scheduled for Dec 3 arrived Jan 6, days before FRC kickoff, and the People's Choice winner still hadn't been announced by mid-2026, becoming a running joke in the thread ("Quarter of the way to the next WCP CADATHON watching this thread hoping for the peoples choice award") ([Hero Heist thread](https://www.chiefdelphi.com/t/wcp-2025-cadathon-hero-heist/507753)).

### Team formation
Per the 2025 rules on WCP's site: **max 2 CADathon teams per FRC team**, no more than **1 mentor per 2 high-school students**, and students are expected (honor system) to do at least half the work. Teams register via Google Form and can register any time during the event. Multiple submissions per organization were allowed in 2025 ("Submit as much as you'd like" — R.C). Cross-team collaborations are common and accepted — e.g., "Team JPC," a collab of designers from 2035/4159/9038/9470, and solo entries by individuals or alumni are welcomed. 8033's winning 2024 entry openly credited helpers from teams 1153, 9442, and 111.

Contrast with F4's team rules, which were stricter about fairness: unlimited team size **only** if all members were from the same FIRST team; otherwise max 3 members, "to prevent the 10 best CADathon participants from 10 different teams from teaming up"; solo entrants could request random partner matching by CAD software and timezone ([9th F4 CADathon](https://www.chiefdelphi.com/t/9th-f4-cadathon-rolling-rampage-rankings-archives-available/386821)).

### Communication channels
WCP runs official **Q&A through the Chief Delphi thread itself** — the game designer (Andrew_L) answers rules questions directly in-thread ("this forum post is the best place to ask game questions"). F4 instead used a **Discord server** (migrated from Slack) plus a formal **Q&A Google Form** with a public answered-questions sheet and published **Team Updates** (rule revisions mid-event, exactly like real FRC). The MoSim project maintains its own Discord for the simulator integration.

## 3. What the Challenge Release Contains

The WCP game reveal package is deliberately modeled on an FRC kickoff:
- **Full game manual** with FRC-style numbered rules (G-rules, R-rules), match phases (auto/teleop/endgame, 2:15 matches in DunkTank), scoring tables, and robot constraints (frame perimeter, extension limits like "G08: horizontal dimensions may never exceed 18" beyond FRAME PERIMETER," possession limits, weight limits, current-season bumper rules).
- **Field CAD** (Onshape document; F4 provided STEP + Onshape).
- **Score calculator spreadsheet** (praised in 2024: "Huge fan of the linked core calculator. This is something FIRST could easily do").
- **2025 addition: MoSimBuilder Alpha integration** — a Unity-based simulation where teams could play the game with simple robot archetypes before designing, described as "the KrayonCAD of FRC video games" ([Hero Heist reveal post](https://www.chiefdelphi.com/t/wcp-2025-cadathon-hero-heist/507753)).

### The games themselves
- **DunkTank (2024)**: basketball-themed — robots dunk **BASKETBALLS** (1-at-a-time possession limit) and collect **ELECTROLYTES** (unlimited possession) to boost performance, with "hoop stacks" and clearing mechanics. Community loved the *Idiocracy*-flavored theme ("sponsored by BRAWNDO, the thirst mutilator").
- **Hero Heist (2025)**: superhero-themed in "Corgiopolis." Teams designed a robot for one of **three classes — COMMANDER, MYSTIC, GADGETEER —** each with different rules (e.g., extension limits), competing for **FAME** by controlling **DISTRICTS** via **SPEECH BUBBLES** (balls) and **STORY PANELS** (HDPE panels), plus climbs. The class system forced a strategic pre-design choice and created interesting meta-analysis (CD polls on which class would be most/least common; the Commander class proved unpopular, prompting one solo entrant to deliberately design one).

## 4. Deliverables

Submissions require exactly two artifacts (2025):
1. **Robot CAD** — Onshape link required in 2025 ("CRITICAL NOTE: All submissions must be made using OnShape"); 2024 allowed Onshape or STEP.
2. **Documentation / "tech binder" (PDF)** — robot function, strategic analysis, engineering decision rationale.

All submissions must be **publicly posted to the Chief Delphi thread** (CAD + docs), which turns the deadline into a massive public design-share — one of the event's most valued features. Renders and reveal-style videos are common but optional (5414 Pearadox even made a full reveal video for their "suPEARman" design). F4 additionally required native CAD files, renders uploaded to a GrabCAD Workbench, and a Google Forms "pit scouting document."

Participation scale: 2024 drew enough entries that WCP ran multi-round judging with 3 winners + 8 named finalists (254, 604, 1902, 5987, 7475, etc.); 2025 had "well over 100" submissions, with 31 teams advancing to Round 2 (including 254, 971, 111, 2767, 6800, 1540) ([results post, Jan 6, 2026](https://www.chiefdelphi.com/t/wcp-2025-cadathon-hero-heist/507753?page=12)).

## 5. Judging: Criteria and Process

Per WCP's CADathon page, judging evaluates:
- **Strategic analysis quality** (does the design follow from a coherent read of the game/meta?)
- **Design feasibility and practicality** ("teams judged within their resource capacity")
- **Documentation effectiveness**
- **Creative use of WCP components** (bonus only — WCP parts are *not* mandatory)

The judge citations in the winners' posts reveal what actually wins: 2024 winner 8033's "Whirlpool" was praised for mechanism detail (torsion-spring/cable hopper flap), documentation "offering thorough breakdowns and clear explanations of their decision-making process," and Onshape best practices (driving sketches, organized features, high-fidelity block CAD before detail work). 2025 winner 5458 was cited for "fast, repeatable cycles and endgame consistency… a strong understanding of ownership mechanics… while staying mechanically cohesive." Strategy-first design with clear points modeling recurs in every citation — pure CAD polish without strategic justification does not top the rankings.

Process: 2024 used named judges (6 listed, including Andrew Lawrence) and **sent individual feedback to every team**. 2025 used two judging rounds, and WCP announced it would **not** send individual feedback "due to our current bandwidth" — a notable regression (see §7). F4's process: submissions split in thirds among 3 judges, each judge picks a top 5–7, then all judges review those, so "the top 15 will have feedback from all 3 judges," with results delivered as a **live ranked show on FIRST Updates Now's Twitch channel** with recorded rank-by-rank feedback (archives on YouTube for ranks 1–5, 6–15, 16–62).

### Prizes
2025: 1st = **TeamWCP sponsorship** for the upcoming season (with a rule that a repeat winner passes the sponsorship down so new teams enter #TeamWCP), 2nd = $250 WCP gift card, 3rd = $150; Fabworks gift cards ($500/$350/$150); People's Choice = Bambu Lab P1S printer; Best Class Design swag. 2024 also had a **Best Onshape Submission** award (won by 8033) carrying a guaranteed PTC grant. Partners: Fabworks, Onshape/PTC, MoSim.

## 6. Comparison: Other FRC Offseason Design Challenges

- **F4 CADathon (2017–2022, ~12 events)**: the community original. Normally **3 days** (extended to 1 week from 2020), biannual, free, all ages. Formal Q&A forms, Team Updates, GrabCAD submission, live Twitch results show with per-team feedback, WCP-sponsored prizes. Its live-feedback show remains the gold standard for judging transparency ([2020 Spring Special results](https://www.chiefdelphi.com/t/2020-spring-special-f4-cadathon-results-posted/383527)).
- **WRRF WaterWorks CADathon (2020)**: a regional first attempt — 1 week design + 1 week judging, teams of ≤3, CAD + PDF documentation, judged on "function, aesthetic, feasibility, and documentation" with point-scored category awards. Memorable mostly for the public grilling it received over vague judging details (see §7) ([WRRF WaterWorks CADathon](https://www.chiefdelphi.com/t/wrrf-waterworks-cadathon/388027)).
- **Robot in 3 Days (Ri3D)**: the physical-build contrast — collegiate teams **build a working robot in 72 hours** after real FRC kickoff, documenting everything to help teams start their season. It's a demonstration/educational sprint, not a judged competition; CADathons are its offseason, design-only mirror with fictional games and judged rankings ([Ri3D category on CD](https://www.chiefdelphi.com/c/other/robot-in-3-days-ri3d/79); [AndyMark Ri3D](https://andymark.com/pages/meet-the-ri3d-teams)).
- **Behind the Bumpers (FUN Robotics Network)**: not a challenge at all but an in-season robot-interview video series (with quick "Pit Stop" companions) — relevant as the design-communication genre CADathon tech binders emulate, and FUN historically hosted F4's results shows ([Behind the Bumpers thread](https://www.chiefdelphi.com/t/behind-the-bumpers-pit-stop-interviews-frc-rebuilt/515918)).
- **Team-internal offseason design challenges**: many teams now use the WCP CADathon as their rookie training capstone — e.g., 226 Hammerheads had design rookies build "STARSCREAM" for Hero Heist using 3005's high-fidelity block-CAD technique ([226 Fall Recap](https://www.chiefdelphi.com/t/226-hammerheads-fall-project-recap/510230)); 271 used it to onboard the team to Onshape.
- The surrounding ecosystem matters: winners repeatedly credit **frcdesign.org and David's Design Server** for building the CAD-training community that feeds CADathon participation.

## 7. What Makes a CADathon Good vs. Frustrating (Participant Consensus)

**What participants praise:**
- **A real, complete kickoff experience**: full FRC-style manual, field CAD, score calculator, and (2025) a playable simulator. Teams explicitly call it "the tune-up we needed" and "a fantastic way to get people engaged in the offseason" ([DunkTank thread](https://www.chiefdelphi.com/t/wcp-cadathon-2024-dunktank/472262)).
- **Responsive, authoritative rules Q&A**: the game designer answering interpretation questions in-thread within hours (e.g., the Hero Heist "district ownership" edge cases, story-panel material, extension-limit questions).
- **Judging transparency and feedback**: F4's live ranked feedback show and WCP 2024's individual written feedback were beloved. The first question after 2024 results was "Where can we find our individual feedback?"
- **Public submissions**: forcing all CAD + docs into a public thread creates a shared library of 100+ designs teams learn from.
- **Well-designed fictional games** with genuine strategic depth (class systems, ownership mechanics) and fun themes.
- **Timing**: a November window (after offseason comps, before build season) was credited for boosting participation vs. early October.
- **Meaningful, identity-level prizes** (TeamWCP sponsorship) plus rules that spread them to new teams.

**What frustrates participants:**
- **Judging delays and silence**: 2025's results slipping a month past deadline (landing 3 days before kickoff), followed by a People's Choice award still unannounced 7+ months later, generated persistent thread-camping and memes — the single biggest complaint about the WCP event.
- **Dropping individual feedback**: WCP's 2025 "no individual feedback due to bandwidth" note directly removed what participants said was a key reason to enter.
- **Rules ambiguity without a formal Q&A system**: Hero Heist's ownership-scoring wording spawned multi-interpretation debates (one reading allowed a 20–30-point exploit loop); with only in-thread answers, participants had to hope their question got seen. Andrew_L himself has said rules should be "taken as intended to minimize lawyering" but that consistent, transparent communication is what keeps ambiguity from souring an event.
- **Opaque judging setups**: the WRRF thread is the canonical checklist of what erodes trust — unnamed judges of unknown qualification, unstated criteria, no manufacturing-resource limits ("judges either too impressed by or too skeptical of 6-axis parts"), and no separation of all-student teams from mentor-heavy teams. As Andrew_L put it: "Anything left vague and ambiguous can sometimes (incorrectly) imply that things aren't figured out… The more information given up front, the more confidence people will have about your program."
- **Fairness of team composition**: stacked all-mentor or all-star cross-team squads vs. student teams is a recurring worry; F4 solved it with size caps on mixed teams, WCP with mentor ratios and honor-system student-work requirements — imperfect but accepted.
- **Scope vs. timeline**: one week is regarded as roughly right for a full robot (F4's original 3 days was brutal and was permanently extended), but life collisions (travel, exams) mean solo/small teams often submit knowingly unfinished work; teams whose training calendar didn't align simply couldn't participate well.

