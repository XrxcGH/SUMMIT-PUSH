# -*- coding: utf-8 -*-
"""
Copy the manual's typefaces from the Fontsource packages into fonts/ and write fonts.css.

    npm ci --prefix organizers/source/typesetting/pdf && python organizers/source/typesetting/pdf/vendor_fonts.py

Only the weights and Unicode subsets the manual uses are copied (MANUAL-STYLE-GUIDE.md §4):
Roboto 400/400i/500/700/700i, Roboto Condensed 400/700 and JetBrains Mono 400/700, in the
latin, latin-ext, greek, math and symbols subsets; and, because Roboto has no arrows, the arrows
block (U+2190-21FF) of Noto Sans Math.  All four families are SIL OFL 1.1.
"""
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "node_modules", "@fontsource")
DST = os.path.join(HERE, "fonts")
WANT = {"roboto": ["400", "400-italic", "500", "700", "700-italic"],
        "roboto-condensed": ["400", "700"],
        "jetbrains-mono": ["400", "700"]}
SUBSETS = {"latin", "latin-ext", "greek", "math", "symbols"}
ARROWS = ("noto-sans-math", "noto-sans-math-latin-400-normal.woff2", "Noto Sans Math", "U+2190-21FF")


def main():
    os.makedirs(DST, exist_ok=True)
    out = ["/* Vendored from Fontsource (@fontsource/roboto, roboto-condensed, jetbrains-mono, noto-sans-math), SIL OFL 1.1.",
           "   See LICENSE-*.txt in this folder.  Regenerate with organizers/source/typesetting/pdf/vendor_fonts.py. */", ""]
    n = 0
    for fam, weights in WANT.items():
        shutil.copy(os.path.join(SRC, fam, "LICENSE"), os.path.join(DST, "LICENSE-%s.txt" % fam))
        for w in weights:
            with open(os.path.join(SRC, fam, w + ".css"), encoding="utf-8") as fh:
                css = fh.read()
            for m in re.finditer(r"/\* (\S+) \*/\n(@font-face \{.*?\n\})", css, re.S):
                name, block = m.group(1), m.group(2)
                sub = re.match(r"%s-(.+)-\d+-(normal|italic)$" % fam, name).group(1)
                if sub not in SUBSETS:
                    continue
                f = name + ".woff2"
                shutil.copy(os.path.join(SRC, fam, "files", f), os.path.join(DST, f))
                n += 1
                block = re.sub(r"src: url\([^)]*\) format\('woff2'\), url\([^)]*\) format\('woff'\);",
                               "src: url(fonts/%s) format('woff2');" % f, block)
                block = block.replace("  font-display: swap;\n", "  font-display: block;\n")
                out.append("/* %s */\n%s\n" % (name, block))
    fam, f, family, urange = ARROWS
    shutil.copy(os.path.join(SRC, fam, "LICENSE"), os.path.join(DST, "LICENSE-%s.txt" % fam))
    shutil.copy(os.path.join(SRC, fam, "files", f), os.path.join(DST, f))
    n += 1
    out.append("/* %s (arrows only: Roboto has none) */\n@font-face {\n  font-family: '%s';\n  font-style: normal;\n"
               "  font-display: block;\n  font-weight: 400;\n  src: url(fonts/%s) format('woff2');\n  unicode-range: %s;\n}\n"
               % (f[:-6], family, f, urange))
    with open(os.path.join(HERE, "fonts.css"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))
    print("copied %d font files" % n)


if __name__ == "__main__":
    main()
