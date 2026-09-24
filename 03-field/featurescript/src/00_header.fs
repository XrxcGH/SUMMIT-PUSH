FeatureScript 2960;
import(path : "onshape/std/geometry.fs", version : "2960.0");

// =====================================================================================
// SUMMIT PUSH — field generator (Onshape FeatureScript)
//
// Builds the complete SUMMIT PUSH field from the locked design package: carpet, guardrails
// and FIELD LEDs, alliance walls with driver stations, four OUTFITTER chutes, both CRAGS with
// every scoring position and their BASE DEPOTS, both HEADWALLS, all tape, 26 AprilTag panels
// with 36h11 decals, and the 63 SUPPLIES in their staged poses — with names, colours,
// materials and densities from 03-field/MATERIALS-AND-COLORS.md.
//
// Coordinate frame: always-blue-origin NWU, inches.  The Part Studio origin is the right
// corner of the Blue alliance wall; +X toward Red, +Y left (from Blue), +Z up.
//
// GENERATED FILE — built by 03-field/featurescript/build.py from src/*.fs.  Edit the
// sources, not this file.  Verified off-line by 03-field/featurescript/verify/run.py.
// =====================================================================================
