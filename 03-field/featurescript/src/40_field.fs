// =====================================================================================
// FIELD PERIMETER — carpet, guardrails with FIELD LED bands, alliance walls, driver
// stations and OUTFITTER chutes (FIELD-CAD-PACKAGE §1.3, §5; MATERIALS-AND-COLORS §2).
// Part-code dialect.
// =====================================================================================

function buildCarpet(context is Context, id is Id)
{
    const W = worldFrame();
    mkBox(context, id + "carpet", W, [0, 0, -CARPET_T], [FIELD_L, FIELD_W, 0]);
    paint(context, [id + "carpet"], "Field carpet", "carpet", 1, "carpet");
}

// FIELD LED colour for a segment on the Blue (X < 324) or Red half.
function fieldLedRGB(opts, isRedHalf)
{
    const st = opts["fieldLed"];
    if (st == "GREEN")
    {
        return PAL["led-green"];
    }
    if (st == "FORECAST")
    {
        return PAL["neutral-white"];
    }
    if (st == "ROUTE")
    {
        return allianceRGB(isRedHalf);
    }
    return PAL["led-dark"];
}

// One long-side guardrail.  side 0 runs along Y = 0, side 1 along Y = 324.  Built in world
// coordinates because its LED segments are coloured by field half, not by alliance.
function buildGuardrail(context is Context, id is Id, side, opts)
{
    const W = worldFrame();
    var yIn = 0;
    var yOut = -GUARD_RAIL_D;
    var gIn = LED_DEPTH;
    var label = "Y = 0";
    if (side == 1)
    {
        yIn = FIELD_W;
        yOut = FIELD_W + GUARD_RAIL_D;
        gIn = -LED_DEPTH;
        label = "Y = 324";
    }
    const lo = min(yIn, yOut);
    const hi = max(yIn, yOut);
    const name = msg(["Guardrail (", label, ")"]);
    mkBox(context, id + "bot", W, [0, lo, 0], [FIELD_L, hi, GUARD_RAIL_H]);
    mkBox(context, id + "top", W, [0, lo, GUARD_H - GUARD_RAIL_H], [FIELD_L, hi, GUARD_H]);
    // FIELD LED bands: two 324-in segments let into the inner face of the top rail
    const ledLo = min(yIn, yIn - gIn);
    const ledHi = max(yIn, yIn - gIn);
    mkBox(context, id + "ledA", W, [0, ledLo, LED_Z - LED_W / 2], [FIELD_CX, ledHi, LED_Z + LED_W / 2]);
    mkBox(context, id + "ledB", W, [FIELD_CX, ledLo, LED_Z - LED_W / 2], [FIELD_L, ledHi, LED_Z + LED_W / 2]);
    bSubtract(context, id + "groove", [id + "top"], [id + "ledA", id + "ledB"], true);
    paintRGB(context, [id + "ledA"], msg([name, " FIELD LED, Blue half"]), fieldLedRGB(opts, false), 1, "acrylic");
    paintRGB(context, [id + "ledB"], msg([name, " FIELD LED, Red half"]), fieldLedRGB(opts, true), 1, "acrylic");
    paint(context, [id + "bot"], msg([name, " bottom rail"]), "wall", 1, "al-tube-2x1");
    paint(context, [id + "top"], msg([name, " top rail"]), "wall", 1, "al-tube-2x1");
    // posts and glazing bays
    var posts = [[0, GUARD_RAIL_D]];
    for (var k = 1; k < 8; k += 1)
    {
        posts = append(posts, [k * GUARD_POST_PITCH - GUARD_RAIL_D / 2, k * GUARD_POST_PITCH + GUARD_RAIL_D / 2]);
    }
    posts = append(posts, [FIELD_L - GUARD_RAIL_D, FIELD_L]);
    const gMid = (yIn + yOut) / 2;
    for (var i = 0; i < size(posts); i += 1)
    {
        const pid = id + nm("post", i);
        mkBox(context, pid, W, [posts[i][0], lo, GUARD_RAIL_H], [posts[i][1], hi, GUARD_H - GUARD_RAIL_H]);
        paint(context, [pid], msg([name, " post"]), "wall", 1, "al-tube-2x1");
        if (i + 1 < size(posts))
        {
            const gid = id + nm("glaze", i);
            mkBox(context, gid, W, [posts[i][1], gMid - GUARD_GLAZE_T / 2, GUARD_RAIL_H],
                    [posts[i + 1][0], gMid + GUARD_GLAZE_T / 2, GUARD_H - GUARD_RAIL_H]);
            paint(context, [gid], msg([name, " glazing"]), "glazing", ALPHA_GLAZING, "polycarbonate");
        }
    }
}

// Driver-station shelf span for station centre s: the shelf is cut back clear of the
// OUTFITTER chute so a CACHE CRATE can slide down the ramp (README: spec finding F-1).
function stationShelfSpan(s)
{
    var lo = s - STATION_W / 2;
    var hi = s + STATION_W / 2;
    const clear = RAMP_FLARE_W / 2 + RAMP_T;
    for (var c in CHUTE_Y)
    {
        if (c - clear < hi && c + clear > lo)
        {
            if (c < s)
            {
                lo = c + clear;
            }
            else
            {
                hi = c - clear;
            }
        }
    }
    return [lo, hi];
}

function buildButton(context is Context, id is Id, F, x, y, tok, name)
{
    const zTop = STATION_SHELF_TOP;
    mkCyl(context, id + "base", F, plXY(0), [x, y], 0.625, zTop, zTop + 1);
    paint(context, [id + "base"], msg([name, " base"]), "button-base", 1, "abs");
    // mushroom head: 1.0-in radius skirt 0.5 tall, then a spherical cap to 1.0 above the skirt base
    const z0 = zTop + 1;
    const rc = 1.25;
    const zc = z0 + 1 - rc;
    const aMid = (atan2d(z0 + 0.5 - zc, 1) + 90) / 2;
    const loop = [["L", [0, z0], [1, z0]],
            ["L", [1, z0], [1, z0 + 0.5]],
            ["A", [1, z0 + 0.5], [rc * cosd(aMid), zc + rc * sind(aMid)], [0, z0 + 1]],
            ["L", [0, z0 + 1], [0, z0]]];
    mkRevolve(context, id + "head", F, plAxis([x, y, 0], [0, 0, 1], [1, 0, 0]), loop);
    paint(context, [id + "head"], name, tok, 1, "abs");
}

// One alliance wall with its driver stations and both OUTFITTER chutes.
function buildAllianceWall(context is Context, id is Id, isRed)
{
    const F = allianceFrame(isRed);
    const A = allianceName(isRed);
    const wn = msg([A, " alliance wall"]);
    // lower solid panel and upper glazing, both flush with the field-side plane x = 0
    mkBox(context, id + "panel", F, [-WALL_PANEL_T, 0, 0], [0, FIELD_W, WALL_SOLID_H]);
    mkBox(context, id + "glaze", F, [-WALL_GLAZE_T, 0, WALL_SOLID_H], [0, FIELD_W, WALL_H]);
    for (var i = 0; i < size(CHUTE_Y); i += 1)
    {
        const c = CHUTE_Y[i];
        mkBox(context, id + nm("open", i), F, [-WALL_T - 1, c - CHUTE_W / 2, CHUTE_SILL], [1, c + CHUTE_W / 2, CHUTE_SILL + CHUTE_H]);
        bSubtract(context, id + nm("cut", i), [id + "panel", id + "glaze"], [id + nm("open", i)], false);
        // pocket for the OUTFITTER AprilTag panel, which sits flush in the glazing plane
        mkBox(context, id + nm("tagpk", i), F, [-WALL_GLAZE_T - 0.05, c - TAG_PANEL / 2, TAG_Z_OUT - TAG_PANEL / 2],
                [0.1, c + TAG_PANEL / 2, TAG_Z_OUT + TAG_PANEL / 2]);
        bSubtract(context, id + nm("tagcut", i), [id + "glaze"], [id + nm("tagpk", i)], false);
    }
    for (var i = 0; i < size(CHUTE_Y); i += 1)
    {
        softFilletAt(context, id + nm("sill", i), [id + "panel"], F, [[0, CHUTE_Y[i], CHUTE_SILL]], CHUTE_SILL_R, "OUTFITTER sill edge");
    }
    paint(context, [id + "panel"], msg([wn, " lower panel"]), "wall", 1, "plywood");
    paint(context, [id + "glaze"], msg([wn, " glazing"]), "glazing", ALPHA_GLAZING, "polycarbonate");

    // steel frame behind the panels (ref): rails and posts, 2.0 in overall wall thickness
    const fx0 = -WALL_T;
    const fx1 = -WALL_PANEL_T;
    var fr = [];
    mkBox(context, id + "frBot", F, [fx0, 0, 0], [fx1, FIELD_W, WALL_RAIL]);
    mkBox(context, id + "frTop", F, [fx0, 0, WALL_H - WALL_RAIL], [fx1, FIELD_W, WALL_H]);
    fr = [id + "frBot", id + "frTop"];
    const midSpans = [[0, CHUTE_Y[0] - CHUTE_W / 2], [CHUTE_Y[0] + CHUTE_W / 2, CHUTE_Y[1] - CHUTE_W / 2], [CHUTE_Y[1] + CHUTE_W / 2, FIELD_W]];
    for (var i = 0; i < size(midSpans); i += 1)
    {
        mkBox(context, id + nm("frMid", i), F, [fx0, midSpans[i][0], WALL_SOLID_H - 1], [fx1, midSpans[i][1], WALL_SOLID_H + 1]);
        fr = append(fr, id + nm("frMid", i));
    }
    const postY = [0, STATION_Y[0] + STATION_W / 2 + 5, STATION_Y[1] + STATION_W / 2 + 5, FIELD_W - WALL_RAIL];
    for (var i = 0; i < size(postY); i += 1)
    {
        mkBox(context, id + nm("frPostLo", i), F, [fx0, postY[i], WALL_RAIL], [fx1, postY[i] + WALL_RAIL, WALL_SOLID_H - 1]);
        mkBox(context, id + nm("frPostHi", i), F, [fx0, postY[i], WALL_SOLID_H + 1], [fx1, postY[i] + WALL_RAIL, WALL_H - WALL_RAIL]);
        fr = append(fr, id + nm("frPostLo", i));
        fr = append(fr, id + nm("frPostHi", i));
    }
    paint(context, fr, msg([wn, " frame"]), "wall", 1, "steel-frame");

    // driver stations: shelf (clear of the chutes) and E-STOP / A-STOP buttons
    for (var i = 0; i < size(STATION_Y); i += 1)
    {
        const s = STATION_Y[i];
        const span = stationShelfSpan(s);
        const sid = id + nm("station", i + 1);
        mkBox(context, sid + "shelf", F, [-WALL_T - STATION_SHELF_D, span[0], STATION_SHELF_TOP - STATION_SHELF_T],
                [-WALL_T, span[1], STATION_SHELF_TOP]);
        paint(context, [sid + "shelf"], msg([A, " driver station ", i + 1, " shelf"]), "wall", 1, "plywood");
        var by = s + 30;
        if (span[1] < s + 40)
        {
            by = s - 36;
        }
        buildButton(context, sid + "estop", F, -8, by, "estop-red", msg([A, " driver station ", i + 1, " E-STOP"]));
        buildButton(context, sid + "astop", F, -8, by + 6, "alliance-blue", msg([A, " driver station ", i + 1, " A-STOP"]));
    }

    // OUTFITTER chutes: ramp, cheek funnels and the ramp's leg (behind the wall, ref)
    for (var i = 0; i < size(CHUTE_Y); i += 1)
    {
        buildOutfitterRamp(context, id + nm("outfitter", i + 1), F, CHUTE_Y[i], msg([A, " OUTFITTER ", i + 1]));
    }
}

function buildOutfitterRamp(context is Context, id is Id, F, c, name)
{
    const s30 = sind(RAMP_ANGLE);
    const c30 = cosd(RAMP_ANGLE);
    const x0 = -WALL_PANEL_T;                      // back face of the lower panel = sill line
    const half0 = CHUTE_W / 2;
    const half1 = RAMP_FLARE_W / 2;
    // ramp: trapezoid in the 30-degree plane, top surface through the sill line
    const upN = [s30, 0, c30];
    const slope = [-c30, 0, s30];
    mkPrism(context, id + "ramp", F, [[x0, c, CHUTE_SILL], upN, slope],
            [[0, -half0], [RAMP_RUN, -half1], [RAMP_RUN, half1], [0, half0]], -RAMP_T, 0);
    paint(context, [id + "ramp"], msg([name, " chute ramp"]), "wall", 1, "uhmw-ply");
    // leg under the loading end
    const xTop = x0 - RAMP_RUN * c30;              // top surface, loading end
    const xb = xTop - RAMP_T * s30;                // underside corner, loading end
    const zb = CHUTE_SILL + RAMP_RUN * s30 - RAMP_T * c30;
    const xl1 = xb + RAMP_T;
    const zl1 = zb - RAMP_T * tand(RAMP_ANGLE);
    prismXZ(context, id + "leg", F, [[xb, 0], [xl1, 0], [xl1, zl1], [xb, zb]], c - half1 + 0.5, c + half1 - 0.5);
    paint(context, [id + "leg"], msg([name, " ramp leg"]), "wall", 1, "plywood");
    // cheek funnels: vertical plates on the ramp's slanted edges, flaring 30 -> 36 in
    const runX = RAMP_RUN * c30;
    const flare = half1 - half0;
    const L = sqrt(runX * runX + flare * flare);
    const u0 = 0.25;
    for (var sg in [-1, 1])
    {
        const t = [-runX / L, sg * flare / L, 0];
        const n = [flare / L, sg * runX / L, 0];
        const zAt0 = CHUTE_SILL + (u0 * runX / L) * tand(RAMP_ANGLE);
        const zAt1 = CHUTE_SILL + RAMP_RUN * s30;
        const cid = id + nm("cheek", (sg + 1) / 2);
        mkPrism(context, cid, F, [[x0, c + sg * half0, 0], n, t],
                [[u0, sg * (zAt0 - 1)], [L, sg * (zAt1 - 1)], [L, sg * (zAt1 + CHEEK_H)], [u0, sg * (zAt0 + CHEEK_H)]], 0, RAMP_T);
        paint(context, [cid], msg([name, " cheek funnel"]), "wall", 1, "plywood");
    }
}
