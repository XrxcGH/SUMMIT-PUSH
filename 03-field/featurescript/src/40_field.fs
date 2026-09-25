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

// FIELD LEDs (manual §3.1.2): each 324-in alliance segment is three 108-in blocks, counted from
// its own alliance wall.  GREEN lights all three; FORECAST lights 1 / 2 / 3 white blocks for
// WHITEOUT / ICEFALL / GALE in both alliances' segments; ROUTE lights 1 / 2 / 3 alliance-colour
// blocks for that alliance's LOW / MID / HIGH ROUTE.  Unlit blocks are dark.
function ledLitCount(opts, isRedHalf)
{
    const st = opts["fieldLed"];
    if (st == "GREEN")
    {
        return 3;
    }
    if (st == "FORECAST")
    {
        const f = opts["forecast"];
        if (f == "GALE")
        {
            return 3;
        }
        if (f == "ICEFALL")
        {
            return 2;
        }
        return 1;
    }
    if (st == "ROUTE")
    {
        var r = opts["routeBlue"];
        if (isRedHalf)
        {
            r = opts["routeRed"];
        }
        if (r == "HIGH")
        {
            return 3;
        }
        if (r == "MID")
        {
            return 2;
        }
        return 1;
    }
    return 0;
}

function ledOnRGB(opts, isRedHalf)
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
    return allianceRGB(isRedHalf);
}

// X range of LED block k (0 = nearest its own alliance wall) in the Blue or Red half.
function ledBlockX(isRedHalf, k)
{
    const b = FIELD_CX / LED_BLOCKS;
    if (isRedHalf)
    {
        return [FIELD_L - b * (k + 1), FIELD_L - b * k];
    }
    return [b * k, b * (k + 1)];
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
    // FIELD LED blocks let into the inner face of the top rail
    const ledLo = min(yIn, yIn - gIn);
    const ledHi = max(yIn, yIn - gIn);
    var leds = [];
    for (var isRedHalf in [false, true])
    {
        const lit = ledLitCount(opts, isRedHalf);
        for (var k = 0; k < LED_BLOCKS; k += 1)
        {
            const bx = ledBlockX(isRedHalf, k);
            const lid = id + nm(nm("led", allianceName(isRedHalf)), k);
            mkBox(context, lid, W, [bx[0], ledLo, LED_Z - LED_W / 2], [bx[1], ledHi, LED_Z + LED_W / 2]);
            var rgb = PAL["led-dark"];
            if (k < lit)
            {
                rgb = ledOnRGB(opts, isRedHalf);
            }
            paintRGB(context, [lid], msg([name, " FIELD LED, ", allianceName(isRedHalf), " segment block ", k + 1]), rgb, 1, "acrylic");
            leds = append(leds, lid);
        }
    }
    bSubtract(context, id + "groove", [id + "top"], leds, true);
    paint(context, [id + "bot"], msg([name, " bottom rail"]), "wall", 1, "al-tube-2x1");
    paint(context, [id + "top"], msg([name, " top rail"]), "wall", 1, "al-tube-2x1");
    // posts (2 x 1 tube: 2 in along the rail) and glazing bays
    const pw = GUARD_RAIL_H;
    var posts = [[0, pw]];
    for (var k = 1; k < 8; k += 1)
    {
        posts = append(posts, [k * GUARD_POST_PITCH - pw / 2, k * GUARD_POST_PITCH + pw / 2]);
    }
    posts = append(posts, [FIELD_L - pw, FIELD_L]);
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

    // steel frame behind the panels (ref): rails and posts, 2.0 in overall wall thickness.  The
    // members of the glazed band come forward to the glazing's back face so the glazing is held.
    const fx0 = -WALL_T;
    const fx1 = -WALL_PANEL_T;
    const fg = -WALL_GLAZE_T;
    var fr = [];
    mkBox(context, id + "frBot", F, [fx0, 0, 0], [fx1, FIELD_W, WALL_RAIL]);
    mkBox(context, id + "frTop", F, [fx0, 0, WALL_H - WALL_RAIL], [fg, FIELD_W, WALL_H]);
    fr = [id + "frBot", id + "frTop"];
    const jw = CHUTE_W / 2 + THROAT_T;         // the mid rail stops at the chute throat liner
    const midSpans = [[0, CHUTE_Y[0] - jw], [CHUTE_Y[0] + jw, CHUTE_Y[1] - jw], [CHUTE_Y[1] + jw, FIELD_W]];
    for (var i = 0; i < size(midSpans); i += 1)
    {
        mkBox(context, id + nm("frMid", i), F, [fx0, midSpans[i][0], WALL_SOLID_H - 1], [fx1, midSpans[i][1], WALL_SOLID_H + 1]);
        fr = append(fr, id + nm("frMid", i));
    }
    const postY = [0, STATION_Y[0] + STATION_W / 2 + 5, STATION_Y[1] + STATION_W / 2 + 5, FIELD_W - WALL_RAIL];
    for (var i = 0; i < size(postY); i += 1)
    {
        mkBox(context, id + nm("frPostLo", i), F, [fx0, postY[i], WALL_RAIL], [fx1, postY[i] + WALL_RAIL, WALL_SOLID_H - 1]);
        mkBox(context, id + nm("frPostHi", i), F, [fx0, postY[i], WALL_SOLID_H + 1], [fg, postY[i] + WALL_RAIL, WALL_H - WALL_RAIL]);
        fr = append(fr, id + nm("frPostLo", i));
        fr = append(fr, id + nm("frPostHi", i));
    }
    paint(context, fr, msg([wn, " frame"]), "wall", 1, "steel-frame");
    bUnion(context, id + "frWeld", fr);

    // driver stations: shelf (clear of the chutes, run back to the lower panel between the frame
    // posts) and E-STOP / A-STOP buttons
    for (var i = 0; i < size(STATION_Y); i += 1)
    {
        const s = STATION_Y[i];
        const span = stationShelfSpan(s);
        const sid = id + nm("station", i + 1);
        mkBox(context, sid + "shelf", F, [-WALL_PANEL_T - STATION_SHELF_D, span[0], STATION_SHELF_TOP - STATION_SHELF_T],
                [-WALL_PANEL_T, span[1], STATION_SHELF_TOP]);
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

// OUTFITTER chute behind the wall: a 2.0-in-deep throat liner that carries the opening through
// the full wall, a 30-degree ramp from the back of the throat, plumb cheeks on the ramp edges,
// 45-degree funnel wings opening to 36 in at the loading end, and a leg (all (ref), §5).
function buildOutfitterRamp(context is Context, id is Id, F, c, name)
{
    const s30 = sind(RAMP_ANGLE);
    const c30 = cosd(RAMP_ANGLE);
    const t30 = tand(RAMP_ANGLE);
    const hw = CHUTE_W / 2;
    const x0 = -WALL_T;                            // back of the throat = start of the ramp
    const xp = -WALL_PANEL_T;                      // back face of the lower panel
    const zs = CHUTE_SILL;
    const zh = CHUTE_SILL + CHUTE_H;
    const tt = THROAT_T;
    // throat liner: sill plate, two jambs and a head plate, flush with the opening
    mkBox(context, id + "throatSill", F, [x0, c - hw - tt, zs - tt], [xp, c + hw + tt, zs]);
    mkBox(context, id + "throatJambA", F, [x0, c - hw - tt, zs], [xp, c - hw, zh]);
    mkBox(context, id + "throatJambB", F, [x0, c + hw, zs], [xp, c + hw + tt, zh]);
    mkBox(context, id + "throatHead", F, [x0, c - hw - tt, zh], [-WALL_GLAZE_T, c + hw + tt, zh + tt]);
    const th = [id + "throatSill", id + "throatJambA", id + "throatJambB", id + "throatHead"];
    paint(context, th, msg([name, " chute throat"]), "wall", 1, "aluminum");
    bUnion(context, id + "throatJoin", th);
    // ramp: 30 wide, 30 degrees, top surface through the sill line at the back of the throat
    const upN = [s30, 0, c30];
    const slope = [-c30, 0, s30];
    mkPrism(context, id + "ramp", F, [[x0, c, zs], upN, slope], rectPts(0, -hw, RAMP_RUN, hw), -RAMP_T, 0);
    paint(context, [id + "ramp"], msg([name, " chute ramp"]), "wall", 1, "uhmw-ply");
    // leg under the loading end
    const xTop = x0 - RAMP_RUN * c30;              // top surface, loading end
    const zTop = zs + RAMP_RUN * s30;
    const xb = xTop - RAMP_T * s30;                // underside corner, loading end
    const zb = zTop - RAMP_T * c30;
    const xl1 = xb + RAMP_T;
    const zl1 = zb - RAMP_T * t30;
    prismXZ(context, id + "leg", F, [[xb, 0], [xl1, 0], [xl1, zl1], [xb, zb]], c - hw + 0.5, c + hw - 0.5);
    paint(context, [id + "leg"], msg([name, " ramp leg"]), "wall", 1, "plywood");
    // cheeks: plumb plates on the ramp edges, from 1.0 below the ramp surface to CHEEK_H above
    const xa = x0 - 0.25;
    const za = zs + (x0 - xa) * t30;
    var cheeks = [];
    for (var sg in [-1, 1])
    {
        const cid = id + nm("cheek", (sg + 1) / 2);
        var y0 = c + hw;
        if (sg < 0)
        {
            y0 = c - hw - RAMP_T;
        }
        prismXZ(context, cid, F, [[xa, za - 1], [xTop, zTop - 1], [xTop, zTop + CHEEK_H], [xa, za + CHEEK_H]], y0, y0 + RAMP_T);
        cheeks = append(cheeks, cid);
    }
    paint(context, cheeks, msg([name, " cheek"]), "wall", 1, "plywood");
    // funnel wings: plumb plates at 45 degrees in plan, from the cheek ends out to +/-18 in
    const flare = RAMP_FLARE_W / 2 - hw;
    const wl = flare * sqrt(2) + RAMP_T;
    var wings = [];
    for (var sg in [-1, 1])
    {
        const wid = id + nm("wing", (sg + 1) / 2);
        const t = [-cosd(45), sg * sind(45), 0];
        const n = [cosd(45), sg * sind(45), 0];
        mkPrism(context, wid, F, [[xTop, c + sg * hw, 0], n, t],
                [[0, sg * (zTop - 1)], [wl, sg * (zTop - 1)], [wl, sg * (zTop + CHEEK_H)], [0, sg * (zTop + CHEEK_H)]], 0, RAMP_T);
        bSubtract(context, wid + "trim", [wid], cheeks, true);
        wings = append(wings, wid);
    }
    paint(context, wings, msg([name, " funnel wing"]), "wall", 1, "plywood");
}
