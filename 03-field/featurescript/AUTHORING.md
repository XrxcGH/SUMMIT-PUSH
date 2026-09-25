# Authoring guide — SUMMIT PUSH FeatureScript generator

How the generator is organized and the rules every source file follows. Read this before
editing anything under `src/`.

## Layout

| File | Role | Language |
|---|---|---|
| `src/00_header.fs` | version header, import, banner | FeatureScript |
| `src/10_kernel.fs` | the **only** code that calls the Onshape standard library | FeatureScript |
| `src/20_ledger.fs` | every dimension, the palette, the materials | part-code dialect |
| `src/30_util.fs` | shared helpers (planes, boxes, frames, painting) | part-code dialect |
| `src/40_field.fs` … `src/45_pieces.fs` | the field elements | part-code dialect |
| `src/48_main.fs` | `buildField`, `groupField` and the dimension self-check | part-code dialect |
| `src/90_features.fs` | the features that appear in Onshape's menu | FeatureScript |
| `build.py` | assembles and checks `SummitPushField.fs` | Python |
| `verify/kernel_occ.py` | OpenCascade twin of `10_kernel.fs`: same names, same semantics | Python |
| `verify/fs2py.py` | lints the dialect, transpiles it to Python and compiles it with FeatureScript's run-time rules | Python |
| `verify/scope_lint.py` | FeatureScript scope rules that the Python twin cannot see | Python |
| `verify/onshape_lint.py` | the Feature Studio editor's own warnings, reproduced off-line | Python |
| `verify/run.py`, `verify/inspect_field.py` | off-line build and whole-field checks; a measuring API over the build | Python |
| `verify/run_checks.py`, `verify/checks/check_*.py` | independent element checks, one module per element | Python |
| `verify/render.py`, `verify/export_glb.py`, `verify/animate.py`, `verify/webrender/` | PNG views, glTF export and a headless three.js renderer | Python, JavaScript |

`build.py` concatenates `src/*.fs` in name order into `SummitPushField.fs`, the file users paste
into a Feature Studio. It then:

- lints the part code (`fs2py.lint` and `scope_lint`, see below);
- fails on any warning the Onshape editor would show (an unused declaration, a variable set but
  never read) and on any call to a std function that fails during regeneration (`getProperty`);
- when a checkout of the FeatureScript standard library is available (`--std PATH`, `$FS_STD`
  or `.fs-std/`), checks every std function, enum member and name collision against it.

## The part-code dialect

Files `src/2x`–`src/4x` are written so that they mean the same thing in FeatureScript and, after
`verify/fs2py.py`, in Python. The dialect lint (`fs2py.lint`) enforces:

- plain numbers only, in **inches and degrees**; the kernel adds units. No `^`, `~`, `%`, `?:`, `++`.
- statements end in `;`; block braces stand alone on their own lines (Allman style).
- control flow: `for (var i = A; i < B; i += S)`, `for (var x in ARRAY)`, `if (...)` / `else if (...)` / `else`.
- declarations: `var x = ...;`, `const x = ...;`, `function name(context is Context, id is Id, a, b)`.
- maps are indexed `m["key"]`, never `m.key`.
- strings appear only as literals and through `nm(s, i)` / `msg([...])`; they are never joined
  with `+` (only `id + "name"` is legal).
- no variable may shadow a std-library name (`plane`, `line`, `box`, `vector`, `size`, …) or a
  reserved word of either language.
- vectors for arithmetic are `vector(x, y, z)`; plain arrays `[x, y]` are for points passed to the kernel.

`verify/scope_lint.py` rejects what the dialect lint cannot see, where FeatureScript and Python
behave differently: a name used outside the block that declared it (FeatureScript is
block-scoped), an undeclared name, assignment to a `const`, a name declared twice or shadowing an
enclosing one, a C-style loop whose body writes its loop variable, bound or step, an indexed
store `a[i] = ...` (FeatureScript arrays are values, Python lists alias) and a chained comparison.

The off-line build compiles the transpiled code with FeatureScript's run-time rules
(`fs2py.compile_part`): arithmetic on arrays is vector arithmetic, a condition or an operand of
`&&`, `||` or `!` must be a boolean, an array index must be a whole number in range, and a missing
map key reads as `undefined`. Anything else FeatureScript rejects raises an error.

## Kernel API (plain numbers; identical in `10_kernel.fs` and `kernel_occ.py`)

Frames and planes

- `frameMake(o, x, z)`: a world frame; `frameIn(F, o, x, z)`: a frame given in F's coordinates.
- A local plane `pl = [origin, normal, xDir]` is given in F's coordinates; sketch coordinates
  (u, v) run along xDir and normal × xDir. Helpers in `30_util.fs`: `plXY(z0)` (u, v = x, y;
  extrudes +z), `plYZ(x0)` (u, v = y, z; extrudes +x), `plXZ(y0)` (u, v = x, z; extrudes −y),
  `plAxis(o, axis, radial)` (for revolves: v along `axis`).

Shapes (each creates exactly one body under `id`; never create a body under another body's id)

- `mkPrism(ctx, id, F, pl, pts, d0, d1)`: a polygon extruded d0..d1 along the plane normal.
- `mkPrismHoles(ctx, id, F, pl, outer, holes, d0, d1)`; `mkPrismProfile(ctx, id, F, pl, loops, d0, d1)`
  with loops of segments `["L", a, b]`, `["A", a, mid, b]`, `["C", centre, r]`.
- `mkCyl(ctx, id, F, pl, c, r, d0, d1)`; `mkRevolve(ctx, id, F, pl, loop)`: a full revolve about the plane's v axis.
- `mkPillowBox(ctx, id, F, h, crown)`; `mkBox(ctx, id, F, p0, p1)` and `prismXY` / `prismXZ` / `prismYZ` (in `30_util.fs`).

Booleans and finishing

- `bSubtract(ctx, id, targets, tools, keepTools)`, `bUnion(ctx, id, bodies)` (style every input
  first: the merged body keeps the style of the earliest input), `bDelete`.
- Ids after a boolean follow std `qCreatedBy`: a merged body answers to the Id of every body that
  merged into it and to the union's Id; the pieces of a body split by a subtraction answer to the
  original Id and to the subtraction's Id. The twin tracks both per solid.
- `removeSlivers(ctx, id, bodies, minVolume)`: delete the tiny bodies a boolean can leave behind.
- `shellHollow(ctx, id, bodies, t)`.
- `filletAt(ctx, id, bodies, F, pts, r)`: fillet the edges through the local points;
  `softFilletAt(..., label)` warns instead of failing (use it for decoration).
- `copyBody(ctx, id, src, F)`: copy a body modeled about the world origin into frame F.

Appearance and properties

- `paint(ctx, bodies, name, paletteToken, alpha, materialKey)`, `paintRGB(...)` (in `30_util.fs`);
  `styleBody(...)`; `nameBody(...)`.
- `styleFacesAt(ctx, bodies, F, pts, rgb, alpha)`: color individual faces.
- `tagDecal(ctx, id, bodies, F, pl, black, cells, s, rgb)`: split the panel face on plane `pl` with
  `cells + 1` planes each way and paint the black cells of an AprilTag; the geometry stays coplanar.
- `massBody(ctx, bodies, materialName, massLb)`: set the density so that the body weighs exactly `massLb`.
- `numberSharedNames(ctx, bodies)`: suffix " 1", " 2", … onto parts that share a name (it reads
  the names `styleBody` and `nameBody` store in an attribute, since `getProperty` is not
  available during regeneration).
- `groupParts(ctx, id, bodies, name)`: group finished bodies into one open composite part (call it last).
- `kWarn(ctx, id, message)`: append a warning to the feature's own status (warnings on
  sub-operation Ids are not shown in Onshape).

Measurement (used by the self-check): `measureBox(ctx, bodies, F)`, `measureVolume`,
`measureDistToPoint`, `measureDist`, `countBodies`, `decalApplied`.

## Conventions every element follows

- **Every body is named, colored and given a material.** Names read as
  `<ALLIANCE> <ELEMENT> <part>`, e.g. `BLUE CRAG Mid Socket (centre side)`. Parts that come in
  pairs on either side of a CRAG say which side they are on ("guardrail side" is the side farther
  from the field's long centerline Y = 162).
- **CRITICAL dimensions are never touched by decoration.** Robot-interaction surfaces (shelf
  tops, socket bores and rims, pegs, rungs, lip, tags) keep their exact geometry. The CRAG's rock
  finish is an appearance, never geometry (MATERIALS-AND-COLORS §3 rule 1): no relief on CRAG faces.
- Decoration uses `softFilletAt`, so a failure only warns.
- Every Id prefix is one contiguous run of operations (std `context.fs`): never return to an
  element's Id after another element has started. A self-check probe gets its own top-level Id.
- No two bodies may share volume (contact is allowed), and every body must stay valid and
  manifold. `verify/run.py` checks all three.
- Red is always Blue rotated 180° about (324, 162): build it with the alliance frame, never by hand.

## The element checks

Each module in `verify/checks/` checks one element against the package documents
(FIELD-CAD-PACKAGE.md, MATERIALS-AND-COLORS.md, DESIGN-SPEC.md, the Game Manual, VISION-GUIDE.md
and the AprilTag layout JSON), never against the ledger or the part code. Where the package leaves
a choice free, the module's docstring states the generator's reading as a *construction reading*.
Where two documents disagree, DESIGN-SPEC.md governs, and the module's docstring and the check's
detail text give the reasoning. `check_twin` compares the twin with the FeatureScript std library,
and `check_fs_api` checks the kernel's std calls.

## Verifying a change

```
git clone https://github.com/javawizard/onshape-std-library-mirror 03-field/featurescript/.fs-std   # once
python 03-field/featurescript/build.py                 # assemble, lint, editor warnings, std API check
python 03-field/featurescript/verify/run.py            # off-line build, self-check, palette, tags, SUPPLIES, interference
python 03-field/featurescript/verify/run_checks.py     # the element checks (or name modules: run_checks.py headwall tags)
python 03-field/featurescript/verify/render.py         # PNG views in renders/
```

The Studio targets FeatureScript 2960; check out the mirror's `Version 2960.0` commit if its head
has moved on. The off-line tools need the Python packages `cadquery-ocp`, `numpy` and, for
`render.py`, `matplotlib`.

All checks must pass before a change is committed.
