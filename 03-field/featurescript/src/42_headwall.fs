// =====================================================================================
// HEADWALL (x2) — FIELD-CAD-PACKAGE §4.  Part-code dialect.
//
// Everything derives from PLANE P: the line {x = 48, z = 0} tilted 15 degrees from vertical,
// top toward the alliance wall.  Plane-P coordinates: w runs up the plane, n is the normal
// toward the field (robots climb the +n side), y is lateral.
//     x = 48 - w sin15 + n cos15,   z = w cos15 + n sin15
// All structure except the rung end brackets lies at n <= -4.0 (TRUSS_CLR).
// =====================================================================================

function hwXZ(w, n)
{
    const s = sind(HW_LEAN);
    const c = cosd(HW_LEAN);
    return [HW_X - w * s + n * c, w * c + n * s];
}

// w of a point in plane P (n = 0) at height z.
function hwW(z)
{
    return z / cosd(HW_LEAN);
}

// (n, w) rectangle -> (x, z) polygon.
function hwRect(n0, n1, w0, w1)
{
    return [hwXZ(w0, n0), hwXZ(w0, n1), hwXZ(w1, n1), hwXZ(w1, n0)];
}

// 2 x 2 member running along y, cross-section n0..n1 x w0..w1 (solid bar; its material is the
// effective density of a 2 x 2 x 0.120 tube, so mass is right and the lane frame welds cleanly).
function hwBarY(context is Context, id is Id, F, n0, n1, w0, w1, y0, y1)
{
    prismXZ(context, id, F, hwRect(n0, n1, w0, w1), y0, y1);
}

function buildHeadwall(context is Context, id is Id, isRed)
{
    const F = allianceFrame(isRed);
    const A = allianceName(isRed);
    const hn = msg([A, " HEADWALL"]);
    const s = sind(HW_LEAN);
    const c = cosd(HW_LEAN);
    const wdir = [-s, 0, c];
    const ndir = [c, 0, s];

    var frames = [];
    var rungsAll = [];
    var brackets = [];
    var uprightsAll = [];
    const rungNames = ["LEDGE RUNG", "CAMP RUNG", "SUMMIT RUNG"];
    for (var li = 0; li < size(LANE_Y); li += 1)
    {
        const yc = LANE_Y[li];
        const ylo = yc - LANE_W / 2;
        const yhi = yc + LANE_W / 2;
        const lid = id + nm("lane", li + 1);
        // one welded lane frame, all members in a single 2-in layer 4.0-6.0 in behind plane P:
        // two uprights running up the plane (trimmed to Z 0..84 below), a bottom rail, a top rail
        // and one carrier behind each rung
        const uy = [[ylo + UPRIGHT_INSET, ylo + UPRIGHT_INSET + TUBE_S], [yhi - UPRIGHT_INSET - TUBE_S, yhi - UPRIGHT_INSET]];
        var members = [];
        for (var k = 0; k < 2; k += 1)
        {
            const uid = lid + nm("upright", k);
            mkPrism(context, uid, F, [[HW_X, 0, 0], wdir, ndir], rectPts(FRONT_N[0], uy[k][0], FRONT_N[1], uy[k][1]), -3, hwW(TRUSS_TOP) + 6);
            members = append(members, uid);
            uprightsAll = append(uprightsAll, uid);
        }
        const my0 = ylo + 0.5;
        const my1 = yhi - 0.5;
        hwBarY(context, lid + "railBot", F, FRONT_N[0], FRONT_N[1], 2, 2 + TUBE_S, my0, my1);
        hwBarY(context, lid + "railTop", F, FRONT_N[0], FRONT_N[1], 85, 85 + TUBE_S, my0, my1);
        members = concatenateArrays([members, [lid + "railBot", lid + "railTop"]]);
        for (var ri = 0; ri < size(RUNG_TOP); ri += 1)
        {
            const zc = RUNG_TOP[ri] - RUNG_OD / 2;
            const wc = hwW(zc);
            const cid = lid + nm("carrier", ri);
            hwBarY(context, cid, F, FRONT_N[0], FRONT_N[1], wc - TUBE_S / 2, wc + TUBE_S / 2, my0, my1);
            members = append(members, cid);
            // the rung: centreline in plane P, 20.0 long, staggered from the lane centre
            const ya = yc + RUNG_STAGGER[ri] - RUNG_L / 2;
            const rid = lid + nm("rung", ri);
            const rc = hwXZ(wc, 0);
            mkCyl(context, rid, F, plXZ(0), rc, RUNG_OD / 2, -(ya + RUNG_L), -ya);
            paint(context, [rid], msg([hn, " lane ", li + 1, " ", rungNames[ri]]), "rung", 1, "steel");
            rungsAll = append(rungsAll, rid);
            // end brackets: saddle plates within 2.0 in of each rung end, from the carrier face
            // to 0.25 in short of the rung's front surface (nothing projects past the rung)
            const bys = [[ya + BRACKET_FROM_END, ya + BRACKET_FROM_END + BRACKET_T],
                    [ya + RUNG_L - BRACKET_FROM_END - BRACKET_T, ya + RUNG_L - BRACKET_FROM_END]];
            for (var bi = 0; bi < 2; bi += 1)
            {
                const bid = lid + nm(nm("bracket", ri), bi);
                prismXZ(context, bid, F, hwRect(FRONT_N[1], BRACKET_FRONT, wc - TUBE_S / 2, wc + TUBE_S / 2), bys[bi][0], bys[bi][1]);
                bSubtract(context, bid + "hole", [bid], [rid], true);
                brackets = append(brackets, bid);
            }
        }
        frames = append(frames, members);
    }
    // trim the uprights to Z 0 .. 84 (truss chords end at 84 in vertical), then weld each lane
    mkBox(context, id + "trimLo", F, [-20, HW_Y0 - 10, -30], [80, HW_Y1 + 10, 0]);
    mkBox(context, id + "trimHi", F, [-20, HW_Y0 - 10, TRUSS_TOP], [80, HW_Y1 + 10, TRUSS_TOP + 40]);
    bSubtract(context, id + "trim", uprightsAll, [id + "trimLo", id + "trimHi"], false);
    for (var li = 0; li < size(frames); li += 1)
    {
        paint(context, frames[li], msg([hn, " lane ", li + 1, " frame"]), "truss", 1, "steel-tube-2x2");
        bUnion(context, id + nm("weld", li + 1), frames[li]);
    }
    paint(context, brackets, msg([hn, " rung end bracket"]), "truss-dark", 1, "steel");

    // lower crossbeam, 8.0-10.0 in behind P so the plumb tag panels sit in front of it, held off
    // the lane frames by a 2 x 2 standoff at every upright; and the three 15-degree tag wedges
    const wcb = (BEAM_Z - (BEAM_N[0] + BEAM_N[1]) / 2 * s) / c;
    var beam = [id + "crossbeam"];
    hwBarY(context, id + "crossbeam", F, BEAM_N[0], BEAM_N[1], wcb - TUBE_S / 2, wcb + TUBE_S / 2, HW_Y0, HW_Y1);
    for (var li = 0; li < size(LANE_Y); li += 1)
    {
        for (var k = 0; k < 2; k += 1)
        {
            var y0 = LANE_Y[li] - LANE_W / 2 + UPRIGHT_INSET;
            if (k == 1)
            {
                y0 = LANE_Y[li] + LANE_W / 2 - UPRIGHT_INSET - TUBE_S;
            }
            const sid = id + nm(nm("standoff", li), k);
            hwBarY(context, sid, F, BEAM_N[1], FRONT_N[0], wcb - TUBE_S / 2, wcb + TUBE_S / 2, y0, y0 + TUBE_S);
            beam = append(beam, sid);
        }
    }
    paint(context, beam, msg([hn, " lower crossbeam"]), "truss", 1, "steel-tube-2x2");
    bUnion(context, id + "beamWeld", beam);
    const pb = hwXZ(wcb - TUBE_S / 2, BEAM_N[1]);
    const pt = hwXZ(wcb + TUBE_S / 2, BEAM_N[1]);
    const xBack = TAG_HW_X - TAG_PANEL_T;
    var wedges = [];
    for (var li = 0; li < size(LANE_Y); li += 1)
    {
        const wid = id + nm("wedge", li + 1);
        prismXZ(context, wid, F, [pb, [xBack, pb[1]], [xBack, pt[1]], pt], LANE_Y[li] - TAG_PANEL / 2, LANE_Y[li] + TAG_PANEL / 2);
        wedges = append(wedges, wid);
    }
    paint(context, wedges, msg([hn, " tag wedge bracket"]), "truss-dark", 1, "aluminum");
}
