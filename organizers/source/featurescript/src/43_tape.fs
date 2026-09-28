// =====================================================================================
// TAPE — FIELD-CAD-PACKAGE §1.2 and §6.  2-in gaffer tape modelled as 0.01-in-thick
// solids on the carpet (Z 0 .. 0.01), line edges on the stated coordinate, inside the zone
// they bound.  Where two tapes cross, the one that governs the line call is kept whole and
// the other is cut around it: APRON > marks > centerline > CENTER CACHE band.
// Part-code dialect.
// =====================================================================================

function tapeBox(context is Context, id is Id, F, x0, y0, x1, y1)
{
    prismXY(context, id, F, rectPts(x0, y0, x1, y1), 0, TAPE_T);
}

// 12-in "X": two 2-in bars crossing at 90 degrees, arms along the diagonals.
function xMarkPts(cx, cy, halfLen, halfW)
{
    const plus = [[halfW, halfLen], [-halfW, halfLen], [-halfW, halfW], [-halfLen, halfW], [-halfLen, -halfW], [-halfW, -halfW],
            [-halfW, -halfLen], [halfW, -halfLen], [halfW, -halfW], [halfLen, -halfW], [halfLen, halfW], [halfW, halfW]];
    const c = cosd(45);
    var out = [];
    for (var p in plus)
    {
        out = append(out, [cx + (p[0] - p[1]) * c, cy + (p[0] + p[1]) * c]);
    }
    return out;
}

// Rounded rectangle loop centred on the origin, half-sizes a x b, corner radius r.
function roundRectLoop(a, b, r)
{
    const k = r * (1 - cosd(45));
    return [["L", [-a + r, -b], [a - r, -b]], ["A", [a - r, -b], [a - k, -b + k], [a, -b + r]],
            ["L", [a, -b + r], [a, b - r]], ["A", [a, b - r], [a - k, b - k], [a - r, b]],
            ["L", [a - r, b], [-a + r, b]], ["A", [-a + r, b], [-a + k, b - k], [-a, b - r]],
            ["L", [-a, b - r], [-a, -b + r]], ["A", [-a, -b + r], [-a + k, -b + k], [-a + r, -b]]];
}

// Alliance tape for one side of the field.  Returns [apronId] for the overlap pass.
function buildAllianceTape(context is Context, id is Id, isRed)
{
    const F = allianceFrame(isRed);
    const A = allianceName(isRed);
    const rgb = allianceRGB(isRed);
    const w = TAPE_W;
    // BASECAMP / HEADWALL ZONE: X 0-48, Y 90-234 (the wall closes the fourth side)
    tapeBox(context, id + "bcX", F, HW_X - w, HW_Y0, HW_X, HW_Y1);
    tapeBox(context, id + "bcLo", F, 0, HW_Y0, HW_X - w, HW_Y0 + w);
    tapeBox(context, id + "bcHi", F, 0, HW_Y1 - w, HW_X - w, HW_Y1);
    paintRGB(context, [id + "bcX", id + "bcLo", id + "bcHi"], msg([A, " BASECAMP tape"]), rgb, 1, "tape");
    bUnion(context, id + "bcJoin", [id + "bcX", id + "bcLo", id + "bcHi"]);
    // CLIMB LINE: the X = 48 line carried across the full width, dashed outside BASECAMP
    const dashes = climbDashes();
    var cl = [];
    for (var i = 0; i < size(dashes); i += 1)
    {
        tapeBox(context, id + nm("climb", i), F, HW_X - w, dashes[i][0], HW_X, dashes[i][1]);
        cl = append(cl, id + nm("climb", i));
    }
    paintRGB(context, cl, msg([A, " CLIMB LINE dash"]), rgb, 1, "tape");
    // OUTFITTER LANES: 36 wide x 48 deep, centred on each chute
    for (var i = 0; i < size(CHUTE_Y); i += 1)
    {
        const c = CHUTE_Y[i];
        const lid = id + nm("lane", i + 1);
        tapeBox(context, lid + "end", F, LANE_TAPE_D - w, c - LANE_TAPE_W / 2, LANE_TAPE_D, c + LANE_TAPE_W / 2);
        tapeBox(context, lid + "lo", F, 0, c - LANE_TAPE_W / 2, LANE_TAPE_D - w, c - LANE_TAPE_W / 2 + w);
        tapeBox(context, lid + "hi", F, 0, c + LANE_TAPE_W / 2 - w, LANE_TAPE_D - w, c + LANE_TAPE_W / 2);
        paintRGB(context, [lid], msg([A, " OUTFITTER LANE ", i + 1, " tape"]), rgb, 1, "tape");
        bUnion(context, lid + "join", [lid + "end", lid + "lo", lid + "hi"]);
    }
    // CRAG APRON: 36 in off the SHELF and PEG FACES, 20 in off the SOCKET FACES, R20 corners
    const CF = cragFrame(isRed);
    const ax = CRAG_S / 2 + 36;
    const ay = CRAG_S / 2 + 20;
    mkPrismProfile(context, id + "apron", CF, plXY(0), [roundRectLoop(ax, ay, 20), roundRectLoop(ax - w, ay - w, 20 - w)], 0, TAPE_T);
    paintRGB(context, [id + "apron"], msg([A, " CRAG APRON tape"]), rgb, 1, "tape");
    return [id + "apron"];
}

// CLIMB LINE dashes (6 on / 6 off) on the X = 48 line outside BASECAMP, derived from the ledger:
// the free spans run between the field edges, the two OUTFITTER LANE end lines (which lie on the
// same strip and serve as the CLIMB LINE there) and BASECAMP.  A dash starts at a field edge or
// one gap after a neighbouring line, and stops one gap before the next.
function climbDashes()
{
    const half = LANE_TAPE_W / 2;
    const spans = [[0, CHUTE_Y[0] - half, true, false], [CHUTE_Y[0] + half, HW_Y0, false, false],
            [HW_Y1, CHUTE_Y[1] - half, false, false], [CHUTE_Y[1] + half, FIELD_W, false, true]];
    var out = [];
    for (var sp in spans)
    {
        var y = sp[0] + CLIMB_DASH;
        if (sp[2])
        {
            y = sp[0];
        }
        var stop = sp[1] - CLIMB_DASH;
        if (sp[3])
        {
            stop = sp[1];
        }
        for (var k = 0; k < 20; k += 1)
        {
            if (y + CLIMB_DASH <= stop + 0.000001)
            {
                out = append(out, [y, y + CLIMB_DASH]);
            }
            y = y + 2 * CLIMB_DASH;
        }
    }
    return out;
}

// Staging marks (FIELD-CAD-PACKAGE §6): the 9 CENTER CACHE X marks and each alliance's three
// staging marks.  Built with the staged SUPPLIES, as a separate "staging" set that can be
// switched off with them.
function buildStagingMarks(context is Context, id is Id)
{
    const W = worldFrame();
    var marks = [];
    for (var i = 0; i < 3; i += 1)
    {
        for (var j = 0; j < 3; j += 1)
        {
            const mid = id + nm(nm("cache", i), j);
            prismXY(context, mid, W, xMarkPts(CACHE_X[i], CACHE_Y[j], 6, 1), 0, TAPE_T);
            paint(context, [mid], msg(["CENTER CACHE mark (", CACHE_X[i], ", ", CACHE_Y[j], ")"]), "neutral-white", 1, "tape");
            marks = append(marks, mid);
        }
    }
    for (var isRed in [false, true])
    {
        buildAllianceStagingMarks(context, id + nm("stage", allianceName(isRed)), isRed);
    }
    return marks;
}

function buildAllianceStagingMarks(context is Context, id is Id, isRed)
{
    const F = allianceFrame(isRed);
    const A = allianceName(isRed);
    const rgb = allianceRGB(isRed);
    // white 12-in X with a 0.5-in alliance-colour border
    const kinds = ["CACHE CRATES", "O2 CELLS", "ROPE COILS"];
    for (var i = 0; i < size(STAGE_Y); i += 1)
    {
        const mid = id + nm("stage", i);
        prismXY(context, mid + "white", F, xMarkPts(STAGE_X, STAGE_Y[i], 6, 1), 0, TAPE_T);
        prismXY(context, mid + "border", F, xMarkPts(STAGE_X, STAGE_Y[i], 6.5, 1.5), 0, TAPE_T);
        bSubtract(context, mid + "cut", [mid + "border"], [mid + "white"], true);
        paint(context, [mid + "white"], msg([A, " staging mark - ", kinds[i]]), "neutral-white", 1, "tape");
        paintRGB(context, [mid + "border"], msg([A, " staging mark border - ", kinds[i]]), rgb, 1, "tape");
    }
}

function buildTape(context is Context, id is Id, marks)
{
    const W = worldFrame();
    const w = TAPE_W;
    const aprons = concatenateArrays([buildAllianceTape(context, id + "blue", false), buildAllianceTape(context, id + "red", true)]);
    // FIELD centerline, broken at the two CRAG footprints
    const segs = [[0, CRAG_RED[1] - CRAG_S / 2], [CRAG_RED[1] + CRAG_S / 2, CRAG_BLUE[1] - CRAG_S / 2], [CRAG_BLUE[1] + CRAG_S / 2, FIELD_W]];
    var cl = [];
    for (var i = 0; i < size(segs); i += 1)
    {
        tapeBox(context, id + nm("center", i), W, FIELD_CX - w / 2, segs[i][0], FIELD_CX + w / 2, segs[i][1]);
        cl = append(cl, id + nm("center", i));
    }
    // CENTER CACHE band outline: X 300-348, Y 108-216
    const bx0 = CACHE_X[0];
    const bx1 = CACHE_X[2];
    const by0 = CRAG_RED[1] + CRAG_S / 2;
    const by1 = CRAG_BLUE[1] - CRAG_S / 2;
    tapeBox(context, id + "bandL", W, bx0, by0, bx0 + w, by1);
    tapeBox(context, id + "bandR", W, bx1 - w, by0, bx1, by1);
    tapeBox(context, id + "bandB", W, bx0 + w, by0, bx1 - w, by0 + w);
    tapeBox(context, id + "bandT", W, bx0 + w, by1 - w, bx1 - w, by1);
    const band = [id + "bandL", id + "bandR", id + "bandB", id + "bandT"];
    // overlap pass: the band stops at the BASE DEPOT trays; everything yields to the APRONS
    const dh = CRAG_S / 2 + 20;         // out to the SOCKET FACE APRON line, so no sliver survives
    const dx0 = CRAG_S / 2 - DEPOT_WRAP - DEPOT_LIP_T - DEPOT_CHAMFER;
    const dx1 = CRAG_S / 2 + DEPOT_CH + DEPOT_LIP_T + DEPOT_CHAMFER;
    mkBox(context, id + "depotB", cragFrame(false), [dx0, -dh, -1], [dx1, dh, 1]);
    mkBox(context, id + "depotR", cragFrame(true), [dx0, -dh, -1], [dx1, dh, 1]);
    bSubtract(context, id + "bandDepot", band, [id + "depotB", id + "depotR"], false);
    bSubtract(context, id + "bandOver", band, concatenateArrays([cl, marks, aprons]), true);
    bSubtract(context, id + "centerOver", cl, concatenateArrays([marks, aprons]), true);
    // drop only degenerate boolean slivers; the 0.34-sq-in triangles of band tape between an X
    // mark's arms are real tape and stay
    removeSlivers(context, id + "slivers", concatenateArrays([cl, band]), 0.01 * TAPE_T);
    paint(context, cl, "FIELD centerline tape", "neutral-white", 1, "tape");
    paint(context, band, "CENTER CACHE band tape", "neutral-white", 1, "tape");
}
