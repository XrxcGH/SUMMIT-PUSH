# -*- coding: utf-8 -*-
"""
Write print HTML for the Team Updates: participants/05-team-updates/TEAM-UPDATE-NN.md ->
build/team-updates/TEAM-UPDATE-NN.html, set in the manual's fonts and colors.

    python3 team_update.py [TEAM-UPDATE-NN.md ...]      (default: every Team Update)

team_updates.sh runs this and prints each page to TEAM-UPDATE-NN.pdf beside its Markdown.
The Markdown is the source; the PDF is generated.  Struck text (~~old~~) prints in red with a
strike, as the brief's Team Update format asks (old text struck, new text, rationale).
"""
import glob
import html
import os
import re
import sys

from make_html import md

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(ROOT, "participants", "05-team-updates")
OUT = os.path.join(HERE, "build", "team-updates")

CSS = """
@page {
  size: letter;
  margin: 0.7in 0.75in 0.8in;
  @bottom-left { content: __FOOTER__; font: 8pt "Roboto Condensed", "Arial Narrow", sans-serif; color: #6E7378; }
  @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 8pt "Roboto Condensed", "Arial Narrow", sans-serif; color: #6E7378; }
}
:root {
  --ink: #1A1D21; --muted: #6E7378; --accent: #1F4E79; --accent-bright: #2E6FA8; --accent-deep: #16385A;
  --rule-line: #C8CCD1; --paper-dim: #F4F5F7; --danger: #A32A2A;
  --font-sans: "Roboto", "Noto Sans Math", Arial, sans-serif;
  --font-cond: "Roboto Condensed", "Noto Sans Math", "Arial Narrow", sans-serif;
  --font-mono: "JetBrains Mono", Consolas, monospace;
}
html { font-size: 10pt; }
body { font-family: var(--font-sans); color: var(--ink); line-height: 1.38; margin: 0; }
.band { background: var(--accent-deep); border-bottom: 2.2pt solid var(--accent-bright); color: #fff;
        padding: 14pt 16pt 12pt; margin-bottom: 10pt; }
.band .kicker { font: 700 9pt var(--font-cond); letter-spacing: 0.12em; text-transform: uppercase; color: #BFD3EA; }
.band h1 { font: 700 22pt/1.1 var(--font-cond); margin: 3pt 0 0; }
.band .meta { font: 400 10pt var(--font-cond); margin-top: 6pt; color: #E6EEF7; }
.band .meta strong { color: #fff; }
h2 { font: 700 13.5pt var(--font-cond); color: var(--accent); border-bottom: 1pt solid var(--rule-line);
     padding-bottom: 2pt; margin: 16pt 0 6pt; break-after: avoid; }
h3 { font: 700 11pt var(--font-cond); color: var(--ink); margin: 11pt 0 3pt; break-after: avoid; }
section.change { break-inside: avoid; }
p { margin: 3pt 0 5pt; }
del { color: var(--danger); text-decoration: line-through; text-decoration-thickness: 0.8pt; }
em { color: var(--muted); }
strong em, em strong { color: inherit; }
code { font: 8.6pt var(--font-mono); background: var(--paper-dim); padding: 0 2pt; border-radius: 2pt; }
hr { border: 0; border-top: 1pt solid var(--rule-line); margin: 12pt 0; }
ul { margin: 3pt 0 6pt; padding-left: 16pt; }
li { margin: 2pt 0; }
table { border-collapse: collapse; width: 100%; margin: 5pt 0 8pt; font-size: 8.8pt; break-inside: avoid; }
th, td { border: 0.6pt solid var(--rule-line); padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: var(--paper-dim); font-family: var(--font-cond); font-weight: 700; }
.intro { border-left: 3pt solid var(--accent-bright); padding: 1pt 0 1pt 9pt; margin: 8pt 0; }
"""


def wrap_changes(body):
    """Each change (an h3 and what follows it, up to the next h3, h2 or rule) stays on one page."""
    return re.sub(r"(<h3.*?)(?=<h3|<h2|<hr|\Z)", r'<section class="change">\1</section>', body, flags=re.S)


def build(path):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    title = lines[0].lstrip("# ").strip()                    # "SUMMIT PUSH — Team Update 01"
    meta = lines[2].strip() if len(lines) > 2 and lines[2].startswith("**") else ""
    rest = "\n".join(lines[3 if meta else 1:])
    parser = md()
    body = wrap_changes(parser.render(rest))
    # the italic lead paragraph and the summary read as the update's preamble
    body = re.sub(r"^\s*<p><em>(.*?)</em></p>", r'<p class="intro"><em>\1</em></p>', body, count=1, flags=re.S)
    short = title.split("—")[-1].strip()                        # "Team Update 01"
    kicker, name = ("SUMMIT PUSH", short) if "—" in title else ("SUMMIT PUSH", title)
    footer = '"%s"' % ("SUMMIT PUSH · " + short).replace('"', '\\"')
    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>%s</title>
<link rel="stylesheet" href="../../fonts.css">
<style>%s</style></head>
<body>
<div class="band"><div class="kicker">%s</div><h1>%s</h1>%s</div>
%s
</body></html>
""" % (html.escape(title), CSS.replace("__FOOTER__", footer), html.escape(kicker), html.escape(name),
       '<div class="meta">%s</div>' % parser.renderInline(meta) if meta else "", body)
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, os.path.splitext(os.path.basename(path))[0] + ".html")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    return out


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(SRC, "TEAM-UPDATE-*.md")))
    for f in files:
        print(os.path.relpath(build(f), ROOT).replace(os.sep, "/"))


if __name__ == "__main__":
    main()
