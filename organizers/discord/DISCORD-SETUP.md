# SUMMIT PUSH — Discord Server Setup

*For the organizer setting up the public Discord server for a SUMMIT PUSH CADathon. This is where squads receive the event, ask rules questions, and post their work. It implements the roles, Q&A and Team Update rules from `participants/02-cadathon/CADATHON-BRIEF.md` and the moderation practices in `organizers/moderation/ORGANIZER-GUIDE.md` as a concrete server: settings, roles, channels, and copy-paste templates. Day numbers below are relative to Day 0 (kickoff, a Saturday), the same convention the brief uses; the organizer sets the actual calendar dates.*

---

## 1. Server settings

| Setting | Value | Why |
|---|---|---|
| **Community** | Enabled | Required for announcement channels, the onboarding/welcome screen, server insights, and AutoMod. Enable it before creating channels below. |
| **Verification level** | High (must have a verified email and be a member of the server for 10 minutes, and a member of Discord for longer than 5 minutes) | The server is public and most members are students. High cuts down drive-by raids and throwaway accounts without blocking legitimate squads, who join days before they need to post anyway. |
| **Explicit media content filter** | Scan media from all members | Public server, minors present. There is no reason to exempt anyone. |
| **Default notifications** | Only @mentions | The volume of channel traffic (Q&A, strategy summaries, submissions) would otherwise bury the announcements that matter; @mentions and the announcement channels' own "Follow" behavior still reach everyone. |
| **Explicit content filter on DMs** | Keep Discord's default (scan direct messages for explicit content) | Defense in depth; see §5 on youth safety for the policy that matters more, which is behavioral, not automated. |
| **Icon** | `brand/summit-push-icon-512.png` (min 512×512; `summit-push-icon-1024.png` also provided) | Discord accepts 512×512 minimum for the server icon; upload the 1024 px file if given the choice, it downsamples cleanly. |
| **Banner** | `brand/summit-push-banner-960x540.png` (960×540) | Server banners need **Boost Level 2**. If the server isn't boosted yet, hold the banner until it is (ask squads to boost, or boost it yourself) — the icon alone is enough to launch without it. |

## 2. Roles

Color is reserved for the three roles squads need to recognize on sight; everyone else uses Discord's default (no color), so the accent colors keep their meaning. Order top to bottom is the server's role hierarchy.

| Role | Color | Can do |
|---|---|---|
| **Organizer** | `#7B3FA0` expedition violet | Full server administration. Runs the event per the Organizer Guide: releases, judging, results. Only Organizers get the `org-*` category. |
| **Game Authority (Q&A desk)** | `#D9A441` amber | Answers rules questions in `#rules-qa`, maintains `#qa-answer-sheet`, drafts and posts Team Updates. Usually the same person as the Organizer, held as a separate role so squads can `@`-mention "the ref" without needing to know who's wearing that hat this event. |
| **Mentor** | `#2E8B57` O2 green | Runs office hours and the mid-event design review, answers in `#onshape-help`, under the mentor-help rules in brief §3.2 (may critique and teach technique; may not touch a squad's document). |
| **Alumni** | default | Same mentor-help rules as Mentor; invited past participants who help at office hours. |
| **Participant** | default | The default role for registered squad members. Can post in every public channel and open threads in the forums. |
| **Rookie** *(optional tag)* | default | A stackable tag alongside Participant for first/second-year students, so office hours and the BASECAMP BOT nudge (brief Appendix A) can find them. No extra permissions. |
| **Spectator** | default | Read access to `start-here`, `game`, and `submissions`; cannot post in the build-window or submissions categories. For parents, other teams, and the generally curious. |
| **Judge** *(optional)* | `#7B3FA0` expedition violet (reused; judges are only present in years judging is announced) | Access to the judging category (§3). Only create and assign this role if judging is announced at kickoff (brief §5.3, Organizer Guide §5). |
| **Bots** | default gray | Any moderation or utility bot (AutoMod is built in and doesn't need this role; add it if you add a third-party bot). |

## 3. Categories and channels

Slowmode is given in seconds. "Who can post" lists roles beyond Organizer/Game Authority, who can post everywhere by virtue of admin permissions.

### START HERE

| Channel | Type | Purpose | Who can post | Slowmode | Topic |
|---|---|---|---|---|---|
| `#welcome` | Text, read-only | First stop; links the welcome message (§8) and the onboarding questions. | Organizer | — | `Start here. Read #rules, then #resources for the public kit. Questions about the event go in #rules-qa.` |
| `#rules` | Text, read-only | Server code of conduct and the youth-safety policy (§5). | Organizer | — | `Server rules and the youth-safety policy. This is a public server with students in it — read this before posting.` |
| `#announcements` | Announcement | Kickoff, deadlines, Team Update notices, results. Members can follow/crosspost to their own server. | Organizer, Game Authority | — | `Event announcements only. Team Updates post here and in full in #team-updates.` |
| `#team-updates` | Text, read-only | The numbered Team Updates, and nothing else. | Game Authority | — | `Team Update 01, 02, ... in order. Each amends the manual: manual + every Team Update = the current ruleset. Also published as participants/05-team-updates/TEAM-UPDATE-NN.md in the kit repo.` |
| `#resources` | Text, read-only | Links to the public kit. | Organizer | — | `The public kit: https://github.com/XrxcGH/SUMMIT-PUSH — Game Manual, CADathon brief, field CAD package, drawings, and the vision guide.` |

### GAME

| Channel | Type | Purpose | Who can post | Slowmode | Topic |
|---|---|---|---|---|---|
| `#rules-qa` | Forum | Rules questions, cited by rule number. Tags: `G1xx`, `G2xx`, `G3xx`, `G4xx`, `G5xx`, `R-rules`, `Field`, `Vision`, `Brief`, plus status tags `Pending` / `Answered`. | Participant, Rookie, Spectator (read) | 60 | `Ask with a rule number, e.g. "Does G501's possession limit count a piece bridging the DEPOT lip?" Answers are public only — never by DM (brief §6).` |
| `#qa-answer-sheet` | Text, read-only | The cumulative, authoritative answer log kept in sync with `#rules-qa`. | Game Authority | — | `The authoritative, cumulative Q&A record. Answers interpret the manual; they do not change it — changes are Team Updates (#team-updates).` |

### BUILD WINDOW

| Channel | Type | Purpose | Who can post | Slowmode | Topic |
|---|---|---|---|---|---|
| `#strategy-summaries` | Forum | One thread per squad for the Day 3 strategy summary (recommended, not enforced). | Participant | 30 | `Post your one-pager here: archetype, target score, RP plan. A mentor replies with a written check within 24 hours.` |
| `#office-hours` | Text | Drop-in text Q&A during scheduled office-hour windows. | Participant | 10 | `Live during scheduled office hours (see #announcements and Events). Design questions and sketch critiques, under the mentor-help rules — mentors don't edit your document.` |
| `Office Hours` | Voice | Live drop-in voice for office hours; open a Stage instead if a session draws a crowd (e.g. the rookie "how to read a game manual" session). | Participant | — | — |
| `#design-review-signups` | Text | Claim a 15-minute mid-event design-review slot (Days 7–8). | Participant | — | `Reply to claim a 15-minute slot for the mid-event design review. One slot per squad.` |
| `#onshape-help` | Text | Onshape *technique* only — a mentor may demo a technique on a throwaway part, never touch your document (brief §3.2). | Participant, Mentor, Alumni | 10 | `Technique questions only ("how do I pattern a feature") — not "can you fix my document." Mentors demo on a scratch part, never in your Onshape document.` |
| `#looking-for-squad` | Text | Solo students and rookies find a squad (brief §3.1 caps squads at 2–4). | Participant | 30 | `Solo or short a member? Post here. Squads are 2–4 students; rookies should have at least one experienced squadmate (brief §3.3).` |

### SUBMISSIONS

| Channel | Type | Purpose | Who can post | Slowmode | Topic |
|---|---|---|---|---|---|
| `#submissions` | Forum | One post per squad, **opened by an Organizer** ahead of the deadline so every squad posts into a pre-made thread. | Participant (reply only; Organizer opens threads) | — | `Post your four deliverables here by the deadline (brief §4): Robot CAD link, Technical Binder PDF, video link, renders (optional). Include the license credit line if your entry includes SUMMIT PUSH material.` |
| `#showcase` | Text | Renders, poster shots, reveal-style edits — optional and not scored, but the People's Choice reference. | Participant | — | `Renders and posters (brief §4.4). Not scored, but eligible for People's Choice.` |

### JUDGING *(optional — create and unhide only if the organizers announce judging at kickoff)*

There is no official judging or scoring by default. If the organizers choose to run judging for a given event, create this category then and unhide it; otherwise leave it out entirely rather than posting it empty.

| Channel | Type | Purpose | Who can post | Slowmode | Topic |
|---|---|---|---|---|---|
| `#judges-private` | Text, private (Judge + Organizer) | Judges' working channel: score sheets, reconciliation, conflict-of-interest recusals. | Judge, Organizer | — | `Private to judges and organizers. Independent scores first, then reconcile (brief §5.3). Recuse from any squad with a conflict.` |
| `#results` | Announcement, read-only | The results-show recap and awards, posted the same night as written feedback goes out. | Organizer | — | `Results and awards, posted live at the results show. Written per-squad feedback goes out the same night.` |
| `#peoples-choice` | Text | Peer-vote instructions and the ballot window. | Organizer | — | `People's Choice: every participant ranks 3 entries other than their own. Instructions and deadline pinned above.` |

### ORGANIZERS *(private, staff only)*

| Channel | Type | Purpose | Who can post | Slowmode | Topic |
|---|---|---|---|---|---|
| `#org-chat` | Text | General staff coordination. | Organizer, Game Authority, Mentor | — | `Staff coordination. Not visible to participants.` |
| `#qa-triage` | Text | Draft rules answers before they go public in `#rules-qa`. | Organizer, Game Authority | — | `Draft answers here first; post the final wording publicly in #rules-qa and log it in #qa-answer-sheet.` |
| `#tu-drafts` | Text | Draft Team Updates before posting. | Organizer, Game Authority | — | `Draft Team Updates here: rule number, struck old text, new text, one-line rationale. Post the final version in #team-updates and fold it into the manual sources per organizers/README.md.` |
| `#mod-log` | Text | Moderation actions, including AutoMod hits worth a human look. | Organizer, Mentor | — | `Moderation log: warnings, timeouts, removals, and flagged AutoMod hits.` |

## 4. The brief's binding rules, mapped onto the server

These are not suggestions; they come straight out of the CADathon brief and the Organizer Guide, and the server layout above exists to enforce them structurally rather than by memory:

- **Rules answers are public only, never by DM** (brief §6). `#rules-qa` is a forum everyone can read; the Game Authority role answers there and never in a direct message. State this in the welcome message and the rules post (§8).
- **Team Updates are posted only in `#team-updates`**, numbered in sequence, in the brief's fixed format: rule number, old text struck through, new text, one-line rationale (brief §6, Organizer Guide §4). Draft them in `#tu-drafts` first. They are also published in the repository as `participants/05-team-updates/TEAM-UPDATE-NN.md` — say so in the channel topic and in the template (§8), so squads know the server post and the repo file are the same authoritative text.
- **Squads do not share CAD or binder content with each other before the deadline** (brief §3.1). `#looking-for-squad` is for *forming* a squad, not for cross-squad collaboration once formed; `#strategy-summaries` and `#onshape-help` are for a squad's own work and general technique, not shared CAD files. Say this explicitly in the rules post.
- **Mentor-help rules** (brief §3.2): Mentors and Alumni may answer questions, critique strategy and sketches, and teach Onshape technique on a throwaway part; they may not create or edit features in a squad's document, sketch solutions, dictate architecture, or do points modeling for a squad. This is written into the `#onshape-help` and `#office-hours` topics and into the Mentor/Alumni role descriptions (§2) so it's visible every time someone opens those channels.
- **The license credit line** (from `participants/README.md`) is required on any posted entry that includes the field model or other SUMMIT PUSH material. It's built into the submission post template (§8) so nobody has to remember the exact wording:

  > SUMMIT PUSH © 2026 Eric Dean. Used under the SUMMIT PUSH Training Use License: https://github.com/XrxcGH/SUMMIT-PUSH

## 5. Youth safety

Participants are students, most of them minors. This is policy, not decoration:

- **Adults keep event conversations in public channels.** Organizers, the Game Authority, Mentors, and Alumni answer questions, critique work, and run office hours in `#rules-qa`, `#office-hours`, `#onshape-help`, and the Office Hours voice channel — never in a direct message to a student.
- **No one-to-one adult–student DMs.** If a student DMs an adult with a question, the answer goes back in the appropriate public channel ("good question — answering in #onshape-help so everyone sees it"), not in the DM thread. This is the same rule as the brief's public-Q&A requirement (§6), extended to every adult role, not just the Game Authority.
- **Moderator expectations.** Organizers and Mentors are expected to: keep their own conversations with students visible to other staff (favor the voice channel or a public text channel over a DM even for casual chat); report any adult–student DM they become aware of to `#mod-log`; and treat the AutoMod log and `#mod-log` as a standing agenda item at organizer check-ins, not a channel that only gets read after something goes wrong.
- **Two-deep awareness**, adapted for a virtual event: avoid a single adult being the only staff presence in a voice/stage channel with students for extended periods; a second Mentor or Organizer should be reachable.

## 6. Onboarding and AutoMod

### Onboarding questions

Configure these in Server Settings → Onboarding (needs Community, §1). Two short questions are enough:

1. **"What's your role?"** (single select) — Participant, Rookie (first or second year), Mentor / Alumni, Judge *(only show if judging is announced)*, Spectator. Maps directly to the roles in §2.
2. **"Build season experience?"** (single select, shown only if "Participant" or "Rookie" was picked) — First season, 2–3 seasons, 4+ seasons. Feeds the Rookie tag and helps office hours find who needs the BASECAMP BOT nudge (brief Appendix A).

Pair onboarding with a short welcome screen pointing to `#welcome`, `#rules`, and `#rules-qa`.

### AutoMod suggestions

- **Block invite links** posted by anyone below Mentor, to stop the server being used to funnel students off-platform.
- **Mention spam**: block messages with an excessive number of role or user mentions (Discord's default preset, 5+ mentions).
- **Profanity / slurs**: enable Discord's default keyword presets (slurs, sexual content) server-wide; this is a student-facing server, don't rely on manual moderation to catch it first.
- **Custom keyword block list** for known exploit-sharing language (e.g., "infinite foul," "exploit," paired with "don't tell" or "before Q&A") — flag to `#mod-log` for a human look rather than auto-block, since legitimate rules questions use similar words; this backs up the spirit clause in brief §6.
- **DM scanning**: turn on Discord's "scan direct messages for explicit content" account-level setting and encourage staff to do the same; it's a backstop, not a substitute for the no-DM policy in §5.

## 7. Fonts and brand assets

`brand/summit-push-icon.svg` (1024×1024, plus `summit-push-icon-1024.png` and `summit-push-icon-512.png`) and `brand/summit-push-banner.svg` (960×540, plus `summit-push-banner-960x540.png`) are hand-written SVGs using the palette from `participants/03-field/MATERIALS-AND-COLORS.md` (expedition violet `#7B3FA0`, amber `#D9A441`, O2 green `#2E8B57`, off-white `#F2F2F0`, ink `#1A1D21`). Both depict the CRAG scoring tower — its stepped tiers and lit SUMMIT BEACON — rather than any other organization's branding.

The banner embeds **Roboto Condensed Bold** (`organizers/source/typesetting/pdf/fonts/roboto-condensed-latin-700-normal.woff2`) as a base64 `@font-face` data URI, so the wordmark renders identically wherever the SVG or its PNG export is opened. Roboto Condensed is licensed under the **SIL Open Font License 1.1** (`organizers/source/typesetting/pdf/fonts/LICENSE-roboto-condensed.txt`), which explicitly permits embedding the font in another work, including bundling it as a data URI inside an SVG; it does not need to be sold or redistributed separately, and this use doesn't trigger any additional obligation beyond keeping the license text alongside the font, which the source folder already does.

## 8. Message templates

Copy these as-is; fill in the bracketed parts.

### Welcome message (`#welcome`)

> **Welcome to SUMMIT PUSH!**
> This is the public server for the SUMMIT PUSH CADathon — an original offseason robotics design challenge. Two weeks, one game, one robot in CAD.
>
> Start here:
> 1. Read **#rules** (it's short, and it covers how questions work on this server).
> 2. Grab the public kit from **#resources** — the Game Manual, the CADathon brief, and the field files.
> 3. Pick your role and experience level in the onboarding prompt if you haven't already.
> 4. Questions about the game go in **#rules-qa**, cited by rule number. Answers are always public — we don't take rules questions by DM.
>
> Kickoff is [DATE]. See you on the mountain.

### Rules post (`#rules`)

> **Server rules**
> 1. This is a public, student-facing server. Be the kind of teammate you'd want in your own pit.
> 2. **Rules questions are public only.** Ask in **#rules-qa** with a rule number. Adults won't answer rules questions by DM, and won't take strategy questions by DM either — see #4.
> 3. **Squads don't share CAD or binder content with each other before the deadline.** Discussing strategy in the open is fine and encouraged; sharing a document or a binder draft with another squad is not.
> 4. **No one-to-one DMs between adults (organizers, mentors, alumni, judges) and students.** If you need help, ask in the relevant channel or an office-hours voice call — that way everyone benefits from the answer, and no conversation happens where staff can't see it.
> 5. Mentors and alumni will critique your strategy, sketches, and CAD, and can show you Onshape *technique* on a scratch part. They will not edit your document, sketch your solution, or model anything for you. If a mentor is driving in your document, something has gone wrong — say so.
> 6. Standard good-conduct rules apply: no harassment, no spam, no NSFW content, no invite-link posting outside staff roles.
> 7. Breaking these gets a warning, then a timeout, then removal, logged in the open where staff can see the pattern.

### How to ask a rules question (pinned in `#rules-qa`)

> **Asking a rules question**
> - Open a new post in this forum. Title it with the rule number if you have one (e.g. "G501 — possession limit at the DEPOT lip").
> - Tag it: pick the rule area (`G1xx`–`G5xx`, `R-rules`, `Field`, `Vision`, `Brief`) plus `Pending`.
> - State the specific scenario, not just "what does G501 mean" — cite the situation you're designing around.
> - The Game Authority answers here, publicly, and re-tags your post `Answered` once it's resolved. The answer also gets logged in **#qa-answer-sheet**, which is the authoritative cumulative record.
> - Turnaround is within 24 hours on weekdays, same-day on the Day 0–1 weekend. After the last-call day (Day 11), answers are best-effort — ask early.
> - Rules changes don't happen here — only in **#team-updates**, as a numbered Team Update.

### Team Update post format (`#team-updates`)

> **Team Update [NN] — [DATE]**
>
> **[Rule number] is revised as follows:**
> ~~[old text]~~
> **[new text]**
>
> *Rationale: [one line].*
>
> *(Repeat the block above for each change. If there's nothing to change this cycle, post: "Team Update [NN] — no changes.")*
>
> This update is also published as `participants/05-team-updates/TEAM-UPDATE-[NN].md` in the kit repository. The manual plus every Team Update is the current ruleset; the most recent update governs where they conflict.

### Submission post (`#submissions`, one thread per squad)

> **[Squad name] — SUMMIT PUSH CADathon submission**
>
> - **Robot CAD (Onshape):** [link, view or edit access as required, edit history intact]
> - **Technical Binder (PDF):** [link or attachment]
> - **Video walkthrough (3–5 min):** [link]
> - **Renders (optional):** [link or attached images]
>
> ALLIANCE ROLE: [CRATE FREIGHTER / O2 SURGEON / RING ALPINIST / HYBRID / other]. Target match score: [X].
>
> SUMMIT PUSH © 2026 Eric Dean. Used under the SUMMIT PUSH Training Use License: https://github.com/XrxcGH/SUMMIT-PUSH

### Kickoff announcement (`#announcements`)

> **SUMMIT PUSH CADathon — kickoff is live**
> The Game Manual, the field CAD package, drawings, the AprilTag layout, the CADathon brief, and the judging rubric (if judging is announced this event) are all in **#resources** now. Read the manual cover to cover — it's the rulebook, and where anything else seems to disagree with it, the manual governs.
> The Q&A desk is open in **#rules-qa**. Strategy day is tomorrow (Day 1). See the Events tab for the full schedule: office hours, the strategy-summary deadline, Team Update slots, the mid-event design review, and the submission deadline.
> Good luck out there.

### Submission deadline announcement (`#announcements`)

> **Submission deadline: Day 14, 11:59 PM local — no extensions**
> All four deliverables (brief §4) go in **#submissions** as one thread per squad. If the event is judged, late entries are exhibition only — reviewed, not ranked. If you're not going to make it with everything, post what you have on time; a complete BASECAMP-BOT-plus-a-rung entry on the clock beats a more ambitious entry posted late.
> [If judging is announced:] Judging opens Day 15; results and written feedback for every squad land at the results show, about Day 22.

## 9. Scheduled events

Create these as Discord Scheduled Events (Server → Events) so they show in every member's Events tab and send reminder notifications. Day numbers are relative to Day 0 (kickoff); the organizer fills in real dates and picks the office-hours voice/stage channel per §3.

| Day | What | Channel |
|---|---|---|
| Day 0 (Sat) | **Kickoff show** — game reveal, brief published, judging announced or ruled out | `#announcements` (voice/stage if run live) |
| Day 1 (Sun) | **Strategy day** — points-per-cycle modeling, RP arithmetic, ALLIANCE ROLE selection | `#office-hours` |
| Day 3 (Tue) | **Strategy-summary deadline (recommended)** + **Office hours** | `#strategy-summaries`, Office Hours voice |
| Day 4 (Wed) | **Team Update 01 slot** | `#team-updates` |
| Day 5 (Thu) | **Office hours** | Office Hours voice |
| Days 7–8 (weekend) | **Mid-event design review** — 15-minute per-squad slots | Office Hours voice/stage, signups in `#design-review-signups` |
| Day 9 (Mon) | **Team Update 02 slot** | `#team-updates` |
| Day 10 (Tue) | **Office hours** | Office Hours voice |
| Day 11 (Wed) | **Last call for guaranteed rules answers** | `#rules-qa` |
| Day 12 (Thu) | **Office hours** | Office Hours voice |
| Day 14 (Sat) | **Submission deadline, 11:59 PM local** | `#submissions` |
| Days 15–21 *(optional)* | **Judging week** — only if judging was announced at kickoff | `#judges-private` |
| ~Day 22 *(optional)* | **Results and feedback show** — only if judging was announced | `#results` (voice/stage if run live) |

There is no official judging or scoring by default. Create the two optional events (and the Judging category in §3) only if the organizers announce judging at kickoff; otherwise the event ends at the Day 14 submission deadline and `#submissions` stands as the record.
