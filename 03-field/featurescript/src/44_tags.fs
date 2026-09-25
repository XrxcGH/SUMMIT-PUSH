// =====================================================================================
// APRILTAGS — FIELD-CAD-PACKAGE §7, VISION-GUIDE §1.  26 tags, family 36h11.
// Each panel is 9.0 in square x 0.25 in, its front face in the published tag plane (flush
// with the structure it is let into), carrying an 8.125-in target: a 10 x 10 grid of
// 0.8125-in cells whose outer ring is white and whose inner 8 x 8 is the 6.5-in tag body.
// Red tags are the Blue tags rotated 180 degrees about field centre, ID + 13.
// Part-code dialect.
// =====================================================================================

// [ID, x, y, z (tag centre, on the face), yaw of the facing normal in degrees]
const TAGS_BLUE = [
        [1, 0, 30, 52, 0],
        [2, 0, 294, 52, 0],
        [3, 39, 114, 12, 0],
        [4, 39, 162, 12, 0],
        [5, 39, 210, 12, 0],
        [6, 300, 226, 17.5, 180],
        [7, 300, 254, 17.5, 180],
        [8, 310, 264, 17.5, 90],
        [9, 338, 264, 17.5, 90],
        [10, 310, 216, 17.5, 270],
        [11, 338, 216, 17.5, 270],
        [12, 348, 226, 17.5, 0],
        [13, 348, 254, 17.5, 0]
    ];

// Mounting location of each tag, as the Game Manual's §3.7 table names it.
const TAG_WHERE = ["BLUE OUTFITTER chute", "BLUE OUTFITTER chute", "BLUE HEADWALL lane 1", "BLUE HEADWALL lane 2",
        "BLUE HEADWALL lane 3", "BLUE CRAG SHELF FACE", "BLUE CRAG SHELF FACE", "BLUE CRAG +Y SOCKET FACE",
        "BLUE CRAG +Y SOCKET FACE", "BLUE CRAG -Y SOCKET FACE", "BLUE CRAG -Y SOCKET FACE", "BLUE CRAG PEG FACE",
        "BLUE CRAG PEG FACE", "RED OUTFITTER chute", "RED OUTFITTER chute", "RED HEADWALL lane 1", "RED HEADWALL lane 2",
        "RED HEADWALL lane 3", "RED CRAG SHELF FACE", "RED CRAG SHELF FACE", "RED CRAG -Y SOCKET FACE",
        "RED CRAG -Y SOCKET FACE", "RED CRAG +Y SOCKET FACE", "RED CRAG +Y SOCKET FACE", "RED CRAG PEG FACE",
        "RED CRAG PEG FACE"];

// 36h11 codes for IDs 1..26 (AprilRobotics tag36h11.c, as decimal) and the bit layout.
const TAG36H11 = [59498712231, 59133511713, 60527243497, 64308969905, 65542086003, 1570935333, 4570528323,
        9189644189, 9115345212, 13936729254, 17036128504, 18952582164, 18753773744, 19969498994, 21877611414,
        25427209038, 28093235948, 29808535122, 32336336285, 36431974697, 36184565189, 37418301711, 41967662609,
        43890307829, 47057427331, 48748314607];
const TAG_BIT_X = [1, 2, 3, 4, 5, 2, 3, 4, 3, 6, 6, 6, 6, 6, 5, 5, 5, 4, 6, 5, 4, 3, 2, 5, 4, 3, 4, 1, 1, 1, 1, 1, 2, 2, 2, 3];
const TAG_BIT_Y = [1, 1, 1, 1, 1, 2, 2, 2, 3, 1, 2, 3, 4, 5, 2, 3, 4, 3, 6, 6, 6, 6, 6, 5, 5, 5, 4, 6, 5, 4, 3, 2, 5, 4, 3, 4];

// The 26-tag table in world coordinates: Blue as published, Red by rotation.
function tagTable()
{
    var out = [];
    for (var t in TAGS_BLUE)
    {
        out = append(out, t);
    }
    for (var t in TAGS_BLUE)
    {
        const p = rot180([t[1], t[2], t[3]]);
        var yaw = t[4] + 180;
        if (yaw >= 360)
        {
            yaw = yaw - 360;
        }
        out = append(out, [t[0] + 13, p[0], p[1], p[2], yaw]);
    }
    return out;
}

// [row, col] cells of the 10 x 10 target that are black for tag `tid`.
function tagBlackCells(tid)
{
    const code = TAG36H11[tid - 1];
    var white = [];
    var p = 1;
    for (var i = 0; i < 35; i += 1)
    {
        p = p * 2;
    }
    for (var i = 0; i < 36; i += 1)
    {
        const bit = floor(code / p) - 2 * floor(code / (2 * p));
        if (bit == 1)
        {
            white = append(white, [TAG_BIT_Y[i] + 1, TAG_BIT_X[i] + 1]);
        }
        p = p / 2;
    }
    var black = [];
    for (var r = 1; r < 9; r += 1)
    {
        for (var c = 1; c < 9; c += 1)
        {
            var isWhite = false;
            for (var wc in white)
            {
                if (wc[0] == r && wc[1] == c)
                {
                    isWhite = true;
                }
            }
            if (!isWhite)
            {
                black = append(black, [r, c]);
            }
        }
    }
    return black;
}

function tagFrame(t)
{
    return frameMake([t[1], t[2], t[3]], [cosd(t[4]), sind(t[4]), 0], [0, 0, 1]);
}

function buildTags(context is Context, id is Id, opts)
{
    const hp = TAG_PANEL / 2;
    for (var t in tagTable())
    {
        const F = tagFrame(t);
        const tid = id + nm("tag", t[0]);
        mkBox(context, tid, F, [-TAG_PANEL_T, -hp, -hp], [0, hp, hp]);
        paint(context, [tid], msg(["AprilTag ", t[0], " - ", TAG_WHERE[t[0] - 1]]), "neutral-white", 1, "tag");
        if (opts["decals"])
        {
            tagDecal(context, id + nm("decal", t[0]), [tid], F, [[0, 0, 0], [1, 0, 0], [0, 1, 0]], tagBlackCells(t[0]), 10, TAG_CELL, PAL["tag-black"]);
        }
    }
}
