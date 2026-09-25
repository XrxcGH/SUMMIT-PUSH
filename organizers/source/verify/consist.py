# -*- coding: utf-8 -*-
"""Document consistency: rule and section cross-references, glossary coverage,
restated-rule qualifiers, and superseded values.

Scans every .md and .svg file and generate_drawings.py, except organizers/design/REVISION-LOG.md, the
organizers/archive/ research and concepts, and any node_modules/. Writes its report to
organizers/source/verify/consist.txt."""
import io, os, re, collections
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
BS = chr(92)
out = []
def p(s): out.append(s)

MD = []
# The drawing sheets and the generator carry prose too, and a stale number there reaches
# a CAD modeller before the Markdown does. Scan them alongside the documents.
for root, dirs, files in os.walk('.'):
    # organizers/archive/concepts/ and organizers/archive/research/ are archive material written before the specification;
    # node_modules/ holds the build tools' third-party packages.
    dirs[:] = [d for d in dirs if d not in ('.git', 'archive', 'node_modules')]
    for f in files:
        # organizers/design/REVISION-LOG.md quotes superseded text by design; scanning it for stale
        # values reports the log's own history and drowns real hits.
        if (f.endswith('.md') or f.endswith('.svg') or f == 'generate_drawings.py') and f != 'REVISION-LOG.md':
            MD.append(os.path.join(root, f).replace(BS, '/').lstrip('./'))

MAN = io.open('participants/01-game-manual/GAME-MANUAL.md', encoding='utf-8').read()

# ---- 1. rule definitions and references ---------------------------------
defined = set(re.findall(r'^\*\*([GR]\d{3})\*\*', MAN, re.M))
refs = collections.Counter(re.findall(r'\b([GR]\d{3})\b', MAN))
p("rules defined: %d" % len(defined))
dangling = sorted(r for r in refs if r not in defined)
p("DANGLING rule refs: %s" % (dangling or "none"))

bands = collections.defaultdict(list)
for r in defined:
    bands[r[0] + r[1]].append(int(r[1:]))
for b in sorted(bands):
    ns = sorted(bands[b])
    exp = list(range(ns[0], ns[0] + len(ns)))
    p("  band %sxx: %d rules %s%s" % (b, len(ns), ns, "" if ns == exp else "  <-- GAP/DUP"))

# ---- 2. section references ----------------------------------------------
heads = set()
for m in re.finditer(r'^#{2,4}\s+([\d.]+)\s', MAN, re.M):
    heads.add(m.group(1).rstrip('.'))
sec_refs = set(re.findall(r'Section (\d+\.\d+(?:\.\d+)?)', MAN))
bad = sorted(s for s in sec_refs if s not in heads)
p("section headings: %d ; DANGLING section refs: %s" % (len(heads), bad or "none"))

# ---- 3. glossary coverage -----------------------------------------------
# Anchor on the Glossary heading, not on an entry: the glossary is alphabetised
# ignoring punctuation, so A-STOP sits after ALLIANCE and anchoring there silently
# dropped the first five headwords from the coverage set.
anchor = '# 9 Glossary'
gl = MAN[MAN.index(anchor):] if anchor in MAN else ''
# Capture every bolded headword, including rows that qualify it -- "**APRON** (CRAG
# APRON)", "**BASE DEPOT** (short form: **DEPOT**)", "**RANKING POINT (RP)**". Also
# harvest the parenthetical aliases, which are defined terms in their own right.
gterms = set()
for _m in re.finditer(r'^\|\s*\*\*([^*]+)\*\*(.*)$', gl, re.M):
    _head = _m.group(1).strip()
    gterms.add(_head)
    gterms.add(re.sub(r'\s*\([^)]*\)', '', _head).strip())     # RANKING POINT (RP) -> RANKING POINT
    for _alias in re.findall(r'\*\*([^*]+)\*\*', _m.group(2)[:120]):
        gterms.add(_alias.strip())
    for _alias in re.findall(r'\(([A-Z][A-Z0-9 /-]+)\)', _head + _m.group(2)[:120]):
        gterms.add(_alias.strip())
gterms.discard('')
p("glossary entries: %d" % len(gterms))
body = MAN[:MAN.index(anchor)] if anchor in MAN else MAN
cands = collections.Counter(re.findall(r'\b([A-Z][A-Z]{2,}(?: [A-Z][A-Z]+)*)\b', body))
ALLOW = set("""AND OR NOT THE FOR WITH FROM THIS THAT ALL ANY ONE TWO PDF CAD SVG LED LEDS JSON
API CSS HTML NWU PSI CIM AWG PWM CAN USB RSL FMS PDH PDP VRM RPM NUT
LETTER NOTE EXAMPLE COMMENTARY XY XZ YZ REBUILT WPILIB ONSHAPE CTRE
FACE HIGH PACKAGE OPERATOR STOP SCORES DRIVER DRIVERS SURGEON"""
            .split()) | {
    # covered by a broader headword, or not a defined term at all
    "SUMMIT PUSH", "FIELD CAD PACKAGE",                       # the game, a filename
    "ASCENT",                                                 # ASCENT RP
    "CELL", "CELLS", "CRATES",                                # O2 CELL, CACHE CRATE
    "LOW ROUTE", "MID ROUTE", "HIGH ROUTE",                   # ROUTE
    "LAUNCHED SUPPLY",                                        # LAUNCH
    "CRATE FREIGHTER", "RING ALPINIST", "O2 SURGEON",         # ALLIANCE ROLE
}
def _forms(term):
    # a body term is covered if the glossary defines it, its singular, or its
    # possessive stem. Without this the check reports every plural as a miss and
    # nobody reads it.
    out = {term}
    for suf in ("S", "ES", "'S"):
        if term.endswith(suf):
            out.add(term[:-len(suf)])
    out.add(term + "S")
    head = term.rsplit(' ', 1)[0] if ' ' in term else None
    if head:
        out.add(head)
    return out

def _covered(term):
    # exact, singular/plural, or a leading word of a defined multiword term:
    # "LEDGE" is covered by "LEDGE RUNG", but "MID SOCKET" is not covered by "SOCKET".
    if _forms(term) & gterms:
        return True
    return any(g.startswith(term + ' ') for g in gterms)

missing = sorted(t for t, c in cands.items()
                 if not _covered(t) and t not in ALLOW and c >= 3
                 and not re.fullmatch(r'[A-Z]{1,3}', t))
p("ALL-CAPS body terms (>=3 uses) with no glossary entry: %d" % len(missing))
for t in missing[:40]:
    p("   %-36s x%d" % (t, cands[t]))

# ---- 3b. load-bearing rules must read the same wherever they are restated -
# Every sentence that cites one of these rules outside its own definition has to
# carry the phrase that makes the rule mean what it means. A restatement that
# drops the qualifier is how a fixed rule silently comes back.
RESTATED = {
    'G416': [('CLIMB LINE', 'the plane test, not the BASECAMP zone'),
             ('took hold of', 'the 5-second tail is scoped to the rung already in hand, not to the clock')],
    'G415': [('borne by', 'occupancy is support, not contact')],
    'G501': [('MAJOR FOUL', 'priced at a MAJOR from the first extra SUPPLY')],
}
p("")
p("rule restatements carry their qualifiers:")
for rid, needs in sorted(RESTATED.items()):
    defined_in = None
    for f in MD:
        if re.search(r'^\*\*%s\*\*' % rid, io.open(f, encoding='utf-8').read(), re.M):
            defined_in = f
            break
    bad = []
    for f in MD:
        if f == defined_in or f.endswith('GAME-MANUAL.md'):
            continue
        t = io.open(f, encoding='utf-8').read()
        for m in re.finditer(r'[^.\n]*\*\*%s\*\*[^.\n]*\.' % rid, t):
            sent = m.group(0)
            # Only sentences that STATE the test need its qualifiers.
            # Rationale ("G416 exists because..."), cross-references and the
            # term's own glossary row are not restatements.
            low = sent.lower()
            states_test = ('may not' in low or 'unless' in low or 'must not' in low)
            if not states_test or len(sent) < 120:
                continue
            # the term's own glossary row says "this plane", not its own headword
            line_start = t.rfind(chr(10), 0, m.start()) + 1
            row_head = re.match(r'\|\s*\*\*([^*]+)\*\*', t[line_start:line_start + 80])
            own_row = row_head.group(1).strip().upper() if row_head else ''
            for phrase, why in needs:
                if phrase.upper() == own_row:
                    continue
                if phrase.lower() not in sent.lower():
                    ln = t[:m.start()].count(chr(10)) + 1
                    bad.append("%s:%d missing %r (%s)" % (f, ln, phrase, why))
    p("  %-5s %s" % (rid, "ok" if not bad else "%d restatement(s) incomplete" % len(bad)))
    for b in bad[:6]:
        p("      " + b)

# ---- 4. stale numeric values across the package -------------------------
STALE = [
 (r'\bR36\b', 'old apron corner radius (now R20)'),
 (r'12\.0 in channel|12-in channel', 'old depot channel (now 16.0)'),
 (r'8\.0 in deep|8-in socket tube|tube 8\.0', 'old socket tube depth (now 7.0)'),
 (r'Ridgeline|8793', 'branding that must be gone'),
 (r'\+20 / \+30 / \+45|\+12 / \+18 / \+28', 'old route uplift (now 18/24/35)'),
 (r'\b28 / 48 / 56\b|\b30 / 50 / 58\b', 'old ASCENT thresholds (now 32/52/60)'),
 (r'SHELF-FACE APRON|within 36 in of the SHELF FACE', 'old G502 region wording'),
 (r'do not count toward the SUPPLY LINE RP for the remainder', 'old G501 consequence'),
 (r"entirely outside (?:its own |its ALLIANCE.s )?BASECAMP", "pre-v2.1 G416 zone test"),
 (r'12\.5 in (?:tall|to its)|crowned top at Z = 12\.5|top Z = 12\.0\)', 'old crowned-crate standing height (now 13.0)'),
 (r'Blue lanes 1 and 3|lanes 1 and 3\)', 'pre-L1 alternating-by-lane rung stagger'),
 (r'corner wrap', 'pre-Q26 DEPOT vocabulary (now leg / corner square / corner arm)'),
]
p("")
for pat, why in STALE:
    hits = []
    for f in MD:
        t = io.open(f, encoding='utf-8').read()
        for m in re.finditer(pat, t, re.I):   # a capitalised 'Corner wraps' row label slipped past
            ln = t[:m.start()].count('\n') + 1
            hits.append("%s:%d  %s" % (f, ln, m.group(0)[:60]))
    p("STALE %-52s %s" % (why, ("CLEAN" if not hits else "%d HIT(S)" % len(hits))))
    for h in hits[:8]:
        p("     " + h)

io.open("organizers/source/verify/consist.txt",
        'w', encoding='utf-8').write("\n".join(out))
print("\n".join(out))
