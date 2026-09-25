// =====================================================================================
// SUPPLIES — FIELD-CAD-PACKAGE §6 and §9.  CACHE CRATE, O2 CELL, ROPE COIL; 21 of each.
// One master of each type is modelled at the world origin, copied to every staged pose,
// then deleted.  Each master's density is set from its published weight and its modelled
// volume, so every copy weighs exactly 2.0 / 1.5 / 1.0 lb.  Part-code dialect.
// =====================================================================================

// Local frames: CACHE CRATE centred on the origin; O2 CELL centred, axis along +x;
// ROPE COIL centred, axis along +z.

// O2 CELL revolve profile and the points used to colour its faces.
function cellGeometry()
{
    const rb = CELL_D / 2;
    const hl = CELL_L / 2;
    const rd = (CELL_DOME * CELL_DOME + rb * rb) / (2 * CELL_DOME);   // dome radius, 2.8333
    const vc = hl - rd;                                                 // dome centre, 4.1667
    const rf = CELL_FILLET;
    const uf = rb - rf;                                                 // fillet centre u
    const vf = vc + sqrt((rd - rf) * (rd - rf) - uf * uf);              // fillet centre v, 5.2208
    const eu = uf / (rd - rf);
    const ev = (vf - vc) / (rd - rf);
    const td = [rd * eu, vc + rd * ev];                                 // fillet / dome tangent point
    const bl = sqrt((1 + eu) * (1 + eu) + ev * ev);
    const fm = [uf + rf * (1 + eu) / bl, vf + rf * ev / bl];            // fillet arc midpoint
    const dl = sqrt(eu * eu + (ev + 1) * (ev + 1));
    const dm = [rd * eu / dl, vc + rd * (ev + 1) / dl];                 // dome arc midpoint
    const loop = [["A", [0, -hl], [dm[0], -dm[1]], [td[0], -td[1]]],
            ["A", [td[0], -td[1]], [fm[0], -fm[1]], [rb, -vf]],
            ["L", [rb, -vf], [rb, vf]],
            ["A", [rb, vf], fm, td],
            ["A", td, dm, [0, hl]],
            ["L", [0, hl], [0, -hl]]];
    return { "loop" : loop, "body" : [0, rb, 0], "fillet" : [[fm[1], fm[0], 0], [-fm[1], fm[0], 0]],
            "cap" : [[dm[1], dm[0], 0], [-dm[1], dm[0], 0]], "fullDiameterLength" : 2 * vf };
}

// Build one SUPPLY of `kind` ("crate", "cell", "coil") in frame F, fully styled.
function buildPiece(context is Context, id is Id, kind, F)
{
    if (kind == "crate")
    {
        const hc = CRATE_S / 2;
        mkPillowBox(context, id, F, hc, CRATE_CROWN);
        var ep = [];
        for (var a in [-hc, hc])
        {
            for (var b in [-hc, hc])
            {
                ep = concatenateArrays([ep, [[a, 0, b], [0, a, b], [a, b, 0]]]);
            }
        }
        softFilletAt(context, id + "edges", [id], F, ep, CRATE_FILLET, "CACHE CRATE edge fillets");
        paint(context, [id], "CACHE CRATE", "crate-violet", 1, "plywood");
        massBody(context, [id], "Ripstop nylon over PU foam (CACHE CRATE, effective)", CRATE_LB);
    }
    else if (kind == "cell")
    {
        const g = cellGeometry();
        mkRevolve(context, id, F, plAxis([0, 0, 0], [1, 0, 0], [0, 1, 0]), g["loop"]);
        paint(context, [id], "O2 CELL", "cell-body", 1, "plywood");
        styleFacesAt(context, [id], F, g["cap"], PAL["cell-cap"], 1);
        styleFacesAt(context, [id], F, g["fillet"], PAL["cell-fillet"], 1);
        massBody(context, [id], "Rigid core, EVA sleeve, molded caps (O2 CELL, effective)", CELL_LB);
    }
    else
    {
        const rt = COIL_TUBE / 2;
        mkRevolve(context, id, F, plAxis([0, 0, 0], [0, 0, 1], [1, 0, 0]), [["C", [COIL_OD / 2 - rt, 0], rt]]);
        paint(context, [id], "ROPE COIL", "coil-amber", 1, "plywood");
        massBody(context, [id], "Molded rubber/foam (ROPE COIL, effective)", COIL_LB);
    }
}

function pieceLabel(kind)
{
    if (kind == "crate")
    {
        return "CACHE CRATE";
    }
    if (kind == "cell")
    {
        return "O2 CELL";
    }
    return "ROPE COIL";
}

// Height of the piece frame origin above the surface it rests on.
function restHeight(kind)
{
    if (kind == "crate")
    {
        return CRATE_S / 2 + CRATE_CROWN;
    }
    if (kind == "cell")
    {
        return CELL_D / 2;
    }
    return COIL_TUBE / 2;
}

// Pose [x, y, z-of-surface] -> frame for a resting piece (crates square to the axes,
// cells lying with the axis along +X, coils flat).
function restFrame(kind, x, y, zs)
{
    return frameMake([x, y, zs + restHeight(kind)], [1, 0, 0], [0, 0, 1]);
}

// Two pieces of one type on one alliance staging mark.
function pairOffsets(kind, opts)
{
    if (opts["pairs"] == "STACKED")
    {
        return [[0, 0, 0], [0, 0, 2 * restHeight(kind)]];
    }
    if (kind == "crate")
    {
        return [[-7, 0, 0], [7, 0, 0]];
    }
    if (kind == "cell")
    {
        return [[0, -3, 0], [0, 3, 0]];
    }
    return [[-5.5, 0, 0], [5.5, 0, 0]];
}

// All 63 staged poses: [kind, x, y, zSurface, label].
function supplyPoses(opts)
{
    var out = [];
    // CENTER CACHE — FIELD SETUP CHART (a), rows Y = 138 / 162 / 186, columns X = 300 / 324 / 348
    const latin = [["cell", "coil", "crate"], ["coil", "crate", "cell"], ["crate", "cell", "coil"]];
    for (var j = 0; j < 3; j += 1)
    {
        for (var i = 0; i < 3; i += 1)
        {
            const k = latin[j][i];
            out = append(out, [k, CACHE_X[i], CACHE_Y[j], TAPE_T, msg([pieceLabel(k), " - CENTER CACHE (", CACHE_X[i], ", ", CACHE_Y[j], ")"])]);
        }
    }
    // alliance staging marks — chart (b): Blue 108 crates, 162 cells, 216 coils; Red rotated
    const stageKinds = ["crate", "cell", "coil"];
    for (var isRed in [false, true])
    {
        for (var j = 0; j < 3; j += 1)
        {
            const k = stageKinds[j];
            const offs = pairOffsets(k, opts);
            for (var n = 0; n < 2; n += 1)
            {
                // a piece rests on the mark's tape only if its lowest point is over the X; the
                // side-by-side CACHE CRATES' crown apexes land 3.45 in clear of it, on the carpet
                var zs = TAPE_T;
                if (k == "crate" && opts["pairs"] != "STACKED")
                {
                    zs = 0;
                }
                var p = [STAGE_X + offs[n][0], STAGE_Y[j] + offs[n][1], zs + offs[n][2]];
                if (isRed)
                {
                    p = rot180(p);
                }
                out = append(out, [k, p[0], p[1], p[2], msg([pieceLabel(k), " - ", allianceName(isRed), " staging mark #", n + 1])]);
            }
        }
    }
    // OUTFITTER stock — 7 of each type per alliance, split between the two chutes (ref)
    const stock = [[["crate", -54, [-21, -7, 7, 21]], ["cell", -72, [-7, 0, 7]], ["coil", -88, [-16.5, -5.5, 5.5, 16.5]]],
            [["crate", -54, [-14, 0, 14]], ["cell", -72, [-10.5, -3.5, 3.5, 10.5]], ["coil", -88, [-11, 0, 11]]]];
    for (var isRed in [false, true])
    {
        for (var ci = 0; ci < 2; ci += 1)
        {
            for (var row in stock[ci])
            {
                var n = 0;
                for (var dy in row[2])
                {
                    n += 1;
                    var p = [row[1], CHUTE_Y[ci] + dy, 0];
                    if (isRed)
                    {
                        p = rot180(p);
                    }
                    out = append(out, [row[0], p[0], p[1], p[2], msg([pieceLabel(row[0]), " - ", allianceName(isRed), " OUTFITTER ", ci + 1, " stock #", n])]);
                }
            }
        }
    }
    return out;
}

function buildSupplies(context is Context, id is Id, opts)
{
    const W = worldFrame();
    const kinds = ["crate", "cell", "coil"];
    for (var k in kinds)
    {
        buildPiece(context, id + nm("master", k), k, W);
    }
    var i = 0;
    for (var p in supplyPoses(opts))
    {
        const isStock = abs(p[1] - FIELD_CX) > FIELD_CX;      // behind an alliance wall
        if ((isStock && opts["stock"]) || (!isStock && opts["staged"]))
        {
            i += 1;
            const pid = id + nm("piece", i);
            copyBody(context, pid, [id + nm("master", p[0])], restFrame(p[0], p[1], p[2], p[3]));
            nameBody(context, [pid], p[4]);
        }
    }
    for (var k in kinds)
    {
        bDelete(context, id + nm("drop", k), [id + nm("master", k)]);
    }
}
