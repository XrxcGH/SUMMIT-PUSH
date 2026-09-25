// =====================================================================================
// PIXEL FONT — a 5 x 7 dot-matrix font for signage, bumper numbers and screens, drawn with
// faceDecal (the lettering is painted onto a planar face; no geometry is added).  Each glyph is
// seven rows, top first; a row is a 5-bit number, most significant bit = leftmost pixel.
// Every lit run is inset by FONT_GAP on all sides, so no two rectangles touch (clean face
// splits in Onshape, and an LED-matrix look).  Part-code dialect.
// =====================================================================================

const FONT_POW2 = [16, 8, 4, 2, 1];
const FONT_GAP = 0.06;          // inset of each lit run, as a fraction of the pixel size
const FONT5X7 = {
        "A" : [14, 17, 17, 31, 17, 17, 17], "B" : [30, 17, 17, 30, 17, 17, 30],
        "C" : [14, 17, 16, 16, 16, 17, 14], "D" : [30, 17, 17, 17, 17, 17, 30],
        "E" : [31, 16, 16, 30, 16, 16, 31], "F" : [31, 16, 16, 30, 16, 16, 16],
        "G" : [14, 17, 16, 23, 17, 17, 15], "H" : [17, 17, 17, 31, 17, 17, 17],
        "I" : [14, 4, 4, 4, 4, 4, 14], "J" : [7, 2, 2, 2, 2, 18, 12],
        "K" : [17, 18, 20, 24, 20, 18, 17], "L" : [16, 16, 16, 16, 16, 16, 31],
        "M" : [17, 27, 21, 21, 17, 17, 17], "N" : [17, 17, 25, 21, 19, 17, 17],
        "O" : [14, 17, 17, 17, 17, 17, 14], "P" : [30, 17, 17, 30, 16, 16, 16],
        "Q" : [14, 17, 17, 17, 21, 18, 13], "R" : [30, 17, 17, 30, 20, 18, 17],
        "S" : [15, 16, 16, 14, 1, 1, 30], "T" : [31, 4, 4, 4, 4, 4, 4],
        "U" : [17, 17, 17, 17, 17, 17, 14], "V" : [17, 17, 17, 17, 17, 10, 4],
        "W" : [17, 17, 17, 21, 21, 21, 10], "X" : [17, 17, 10, 4, 10, 17, 17],
        "Y" : [17, 17, 17, 10, 4, 4, 4], "Z" : [31, 1, 2, 4, 8, 16, 31],
        "0" : [14, 17, 19, 21, 25, 17, 14], "1" : [4, 12, 4, 4, 4, 4, 14],
        "2" : [14, 17, 1, 2, 4, 8, 31], "3" : [31, 2, 4, 2, 1, 17, 14],
        "4" : [2, 6, 10, 18, 31, 2, 2], "5" : [31, 16, 30, 1, 1, 17, 14],
        "6" : [6, 8, 16, 30, 17, 17, 14], "7" : [31, 1, 2, 4, 8, 8, 8],
        "8" : [14, 17, 17, 14, 17, 17, 14], "9" : [14, 17, 17, 15, 1, 2, 12],
        " " : [0, 0, 0, 0, 0, 0, 0], "-" : [0, 0, 0, 31, 0, 0, 0],
        "." : [0, 0, 0, 0, 0, 12, 12], ":" : [0, 12, 12, 0, 12, 12, 0],
        "!" : [4, 4, 4, 4, 4, 0, 4], "/" : [1, 1, 2, 4, 8, 16, 16]
    };

// 1 if column c (0 = leftmost) of the 5-bit glyph row value r is lit, else 0.
function fontBit(r, c)
{
    return floor(r / FONT_POW2[c]) - 2 * floor(r / (2 * FONT_POW2[c]));
}

// Width of n characters at pixel size `cell` (5 pixels per glyph, 1 pixel between glyphs).
function textWidth(n, cell)
{
    return (6 * n - 1) * cell;
}

// Rectangles [u0, v0, u1, v1] that draw `text` — an array of one-character strings, e.g.
// chars("SUMMIT PUSH") — with the lower-left corner of the first glyph at (u0, v0).  The text is
// 7 * cell tall and textWidth(size(text), cell) wide.  Pass the result to faceDecal.
function textRects(text, u0, v0, cell)
{
    var out = [];
    const g0 = FONT_GAP * cell;
    for (var k = 0; k < size(text); k += 1)
    {
        const g = FONT5X7[text[k]];
        const ux = u0 + 6 * cell * k;
        for (var r = 0; r < 7; r += 1)
        {
            const v = v0 + (6 - r) * cell;
            var start = -1;
            for (var c = 0; c < 6; c += 1)
            {
                var lit = false;
                if (c < 5)
                {
                    lit = fontBit(g[r], c) == 1;
                }
                if (lit && start < 0)
                {
                    start = c;
                }
                if (!lit && start >= 0)
                {
                    out = append(out, [ux + start * cell + g0, v + g0, ux + c * cell - g0, v + cell - g0]);
                    start = -1;
                }
            }
        }
    }
    return out;
}

// Rectangles for `text` centred on (uc, vc).
function textRectsCentred(text, uc, vc, cell)
{
    return textRects(text, uc - textWidth(size(text), cell) / 2, vc - 3.5 * cell, cell);
}
