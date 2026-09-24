// =====================================================================================
// FEATURES — what appears in the Onshape feature menu.
// =====================================================================================

export enum SpCragLighting
{
    annotation { "Name" : "Unlit" }
    UNLIT,
    annotation { "Name" : "Lit (all CAMPS established)" }
    LIT
}

export enum SpFieldLed
{
    annotation { "Name" : "Dark" }
    DARK,
    annotation { "Name" : "Green (FIELD safe)" }
    GREEN,
    annotation { "Name" : "White (FORECAST)" }
    FORECAST,
    annotation { "Name" : "Alliance colour (ROUTE)" }
    ROUTE
}

export enum SpStagingPairs
{
    annotation { "Name" : "Side by side" }
    SIDE_BY_SIDE,
    annotation { "Name" : "Stacked" }
    STACKED
}

export enum SpSupplyKind
{
    annotation { "Name" : "CACHE CRATE" }
    CACHE_CRATE,
    annotation { "Name" : "O2 CELL" }
    O2_CELL,
    annotation { "Name" : "ROPE COIL" }
    ROPE_COIL
}

function spOptions(definition is map) returns map
{
    var led = "DARK";
    if (definition.fieldLed == SpFieldLed.GREEN)
        led = "GREEN";
    else if (definition.fieldLed == SpFieldLed.FORECAST)
        led = "FORECAST";
    else if (definition.fieldLed == SpFieldLed.ROUTE)
        led = "ROUTE";
    return {
            "perimeter" : definition.perimeter,
            "walls" : definition.walls,
            "crags" : definition.crags,
            "headwalls" : definition.headwalls,
            "tape" : definition.tape,
            "tags" : definition.tags,
            "decals" : definition.tags && definition.decals,
            "staged" : definition.staged,
            "stock" : definition.stock,
            "lit" : definition.lighting == SpCragLighting.LIT,
            "fieldLed" : led,
            "pairs" : definition.pairs == SpStagingPairs.STACKED ? "STACKED" : "SIDE"
        };
}

annotation { "Feature Type Name" : "SUMMIT PUSH Field",
        "Feature Type Description" : "Builds the complete SUMMIT PUSH field (always-blue-origin NWU, inches) with names, colours, materials and densities." }
export const summitPushField = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Group Name" : "Build", "Collapsed By Default" : false }
        {
            annotation { "Name" : "Carpet, guardrails and FIELD LEDs", "Default" : true }
            definition.perimeter is boolean;
            annotation { "Name" : "Alliance walls, driver stations, OUTFITTERS", "Default" : true }
            definition.walls is boolean;
            annotation { "Name" : "CRAGS and BASE DEPOTS", "Default" : true }
            definition.crags is boolean;
            annotation { "Name" : "HEADWALLS", "Default" : true }
            definition.headwalls is boolean;
            annotation { "Name" : "Tape", "Default" : true }
            definition.tape is boolean;
            annotation { "Name" : "AprilTag panels", "Default" : true }
            definition.tags is boolean;
            annotation { "Name" : "36h11 decals on the AprilTag panels", "Default" : true }
            definition.decals is boolean;
            annotation { "Name" : "Staged SUPPLIES (CENTER CACHE and staging marks)", "Default" : true }
            definition.staged is boolean;
            annotation { "Name" : "OUTFITTER stock (behind the alliance walls)", "Default" : true }
            definition.stock is boolean;
        }
        annotation { "Group Name" : "Appearance", "Collapsed By Default" : false }
        {
            annotation { "Name" : "CRAG tier rings and SUMMIT BEACON", "Default" : SpCragLighting.UNLIT }
            definition.lighting is SpCragLighting;
            annotation { "Name" : "FIELD LED state", "Default" : SpFieldLed.DARK }
            definition.fieldLed is SpFieldLed;
            annotation { "Name" : "Pieces on each alliance staging mark", "Default" : SpStagingPairs.SIDE_BY_SIDE }
            definition.pairs is SpStagingPairs;
        }
        annotation { "Name" : "Run dimension self-check", "Default" : true }
        definition.selfCheck is boolean;
    }
    {
        const opts = spOptions(definition);
        buildField(context, id, opts);
        if (definition.selfCheck)
        {
            const checks = selfCheck(context, id, opts);
            const fails = failures(checks);
            if (size(fails) == 0)
            {
                reportFeatureInfo(context, id, "SUMMIT PUSH self-check: all " ~ size(checks) ~ " dimension checks pass");
            }
            else
            {
                for (var f in fails)
                {
                    println("SUMMIT PUSH self-check FAILED: " ~ f);
                }
                reportFeatureWarning(context, id, "SUMMIT PUSH self-check: " ~ size(fails) ~ " of " ~ size(checks) ~
                            " dimension checks failed (details in the FeatureScript console)");
            }
        }
    }, {
            "perimeter" : true,
            "walls" : true,
            "crags" : true,
            "headwalls" : true,
            "tape" : true,
            "tags" : true,
            "decals" : true,
            "staged" : true,
            "stock" : true,
            "lighting" : SpCragLighting.UNLIT,
            "fieldLed" : SpFieldLed.DARK,
            "pairs" : SpStagingPairs.SIDE_BY_SIDE,
            "selfCheck" : true
        });

annotation { "Feature Type Name" : "SUMMIT PUSH Game Piece",
        "Feature Type Description" : "One SUMMIT PUSH SUPPLY at the origin, with its official colour and weight." }
export const summitPushGamePiece = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "SUPPLY", "Default" : SpSupplyKind.CACHE_CRATE }
        definition.kind is SpSupplyKind;
        annotation { "Name" : "Rest on the Top plane", "Default" : true }
        definition.rest is boolean;
    }
    {
        var kind = "crate";
        if (definition.kind == SpSupplyKind.O2_CELL)
            kind = "cell";
        else if (definition.kind == SpSupplyKind.ROPE_COIL)
            kind = "coil";
        var F = worldFrame();
        if (definition.rest)
            F = restFrame(kind, 0, 0, 0);
        buildPiece(context, id + "piece", kind, F);
    }, {
            "kind" : SpSupplyKind.CACHE_CRATE,
            "rest" : true
        });
