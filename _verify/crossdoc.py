# -*- coding: utf-8 -*-
"""Cross-document agreement.

consist.py asks whether a superseded value survives anywhere. This asks the other
question: does a value that MUST appear in several documents actually appear in all
of them? A fix can be applied correctly in one place and simply never written in
another, and no stale-text scan can see that -- the absence looks like clean text.

Each row names a value, the documents that must carry it, and the wording that must
be gone. Add a row whenever a change has to land in more than one document."""
import io, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

DOCS = {
 'spec':   '01-design/DESIGN-SPEC.md',
 'arena':  '02-manual/sections/02-arena.md',
 'play':   '02-manual/sections/03-match-play.md',
 'rules':  '02-manual/sections/04-game-rules.md',
 'robot':  '02-manual/sections/05-robot-rules.md',
 'gloss':  '02-manual/sections/06-tournament-glossary.md',
 'cad':    '03-field/FIELD-CAD-PACKAGE.md',
 'vision': '04-vision/VISION-GUIDE.md',
 'brief':  '05-cadathon/CADATHON-BRIEF.md',
 'gen':    '03-field/renderings/generate_drawings.py',
 'mats':   '03-field/MATERIALS-AND-COLORS.md',
}
T = {k: io.open(v, encoding='utf-8').read() for k, v in DOCS.items()}
SVG = {os.path.basename(p): io.open('03-field/renderings/' + p, encoding='utf-8').read()
       for p in os.listdir('03-field/renderings') if p.endswith('.svg')}
ALL = dict(T); ALL.update(SVG)

# (label, must-appear-in, pattern, must-NOT-appear-in, stale pattern)
ROWS = [
 ("crowned crate stands 13.0",      ['vision', 'cad', 'arena'], r'13\.0',
                                    ['vision', 'cad', 'arena'], r'crowned (?:top|apex) at Z = 12\.5'),
 ("tag clearance 0.19 in as-built", ['vision', 'cad', 'arena'], r'0\.19',
                                    ['vision', 'cad', 'arena'], r'0\.(?:94|44) in below the target'),
 ("Shelf 1 gusset floor 19.0",      ['cad'], r'entirely above \*\*Z = 19\.0\*\*',
                                    ['cad'], r'gusset may descend to \*\*Z = 13\.0\*\*'),
 ("Shelf 2 gusset floor 38.0",      ['cad'], r'above \*\*Z = 38\.0\*\*', [], None),
 ("camera 20 in -> 15 in as-built", ['vision'], r'\| 20 in \| 15 in \|',
                                    ['vision'], r'\| 20 in \| (?:22|24|29) in \|'),
 ("DEPOT tray floor at 0.25",        ['spec', 'cad', 'arena', 'vision'], r'0\.25',
                                    [], None),
 ("crate apex 13.25 in the DEPOT",   ['cad', 'arena', 'vision', 'spec'], r'13\.25',
                                    ['cad', 'arena', 'vision'], r'crowned apex at Z = \*\*13\.0\*\*'),
 ("DEPOT colour #7F7F7F",            ['mats'], r'#7F7F7F', ['mats'], r'#B8A888'),
 ("CELL R1.0 cap/body fillet",       ['spec', 'cad', 'vision'], r'R1\.0|1\.0-in fillet|1\.0 in fillet',
                                    [], None),
 ("CELL fillet band colour",         ['mats'], r'#4D4D4D', [], None),
 ("CELL full-diameter body 10.44",   ['cad'], r'10\.44', [], None),
 ("CRATE R1.0 edge fillets",         ['cad'], r'1\.0-in edge fillets', [], None),
 ("CRATE slot tolerance 0.78",       ['cad', 'arena', 'brief'], r'0\.78',
                                    ['cad'], r'\(1\.0-in clearance per side\)'),
 ("apex form is a lower bound only", ['vision'], r'lower bound that is 1\u20135 in optimistic', [], None),
 ("G416 tail is scoped to the rung", ['spec', 'arena', 'play', 'rules', 'gloss'], r'took hold of',
                                    ['spec', 'arena', 'play', 'rules', 'gloss'], r'has not driven'),
 ("G412 and G413 both capped",       ['rules'], r'to a maximum of 3 additional MAJOR FOULS',
                                    ['rules'], r'with no maximum'),
 ("rung bracket exception in all 3", ['spec', 'arena', 'cad'], r'end brackets',
                                    ['arena'], r'every rung offers full hook wrap'),
 ("EV crossover 9/17 published",     ['play'], r'9/17', [], None),
 ("MID wins in a published row",     ['play'], r'\.92 / \.90 / \.55', [], None),
 ("uniform stagger everywhere",      ['spec', 'arena', 'cad', 'vision', 'gen'],
                                     r'identical in all three lanes|same in \*\*every lane\*\*|same in every lane|same stagger|all three lanes',
                                     ['spec', 'arena', 'cad', 'vision', 'gen'], r'lanes 1 and 3'),
 ("climb reach: only LEDGE",         ['cad', 'rules'], r'11\.59|11\.6',
                                    ['cad'], r'yes, by 0\.73 in'),
 ("depot vocabulary settled",        ['cad'], r'corner square', ['cad', 'arena', 'spec'], r'(?i)corner wrap'),
]

bad = 0
for label, must, pat, mustnot, stale in ROWS:
    miss = [d for d in must if not re.search(pat, ALL[d])]
    surv = []
    if stale:
        surv = [d for d in mustnot if re.search(stale, ALL[d])]
    if miss or surv:
        bad += 1
        print("  FAIL %-34s %s%s" % (label,
              ("missing from %s" % miss) if miss else "",
              ("  stale text survives in %s" % surv) if surv else ""))
    else:
        print("  ok   %-34s" % label)

# the drawing set must not contradict the documents on these
print()
for label, pat, files in (
    ("sheets: no 12.0-in crate occlusion note", r'top Z = 12\.0', ['apriltag-map.svg']),
    ("sheets: no 10.4-in Shelf 2 clearance",    r'clears the tube by 10\.4', ['crag.svg']),
    ("sheets: no per-lane stagger caption",     r'Lane 2 alternates', ['headwall.svg']),
    ("sheets: no 4.0-in inter-lane gap",        r'inter-lane gap at any height is 4\.0', ['headwall.svg']),
    ("sheets: no 47-deg coil tilt",             r'about 47 deg', ['crag.svg', 'game-pieces.svg']),
):
    hit = [f for f in files if re.search(pat, SVG.get(f, ''))]
    if hit:
        bad += 1
        print("  FAIL %-40s still in %s" % (label, hit))
    else:
        print("  ok   %-40s" % label)
print("\nRESULT: %d failure(s)" % bad)
