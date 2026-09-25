# Onshape field generator: source and verification

This folder builds `participants/03-field/onshape/SummitPushField.fs`, the Feature Studio that
participants paste into Onshape. Its user guide (installation, feature options, part naming,
materials and mass) is `participants/03-field/onshape/README.md`.

| Path | Contents |
|---|---|
| `src/*.fs` | The FeatureScript sources, assembled in name order. `src/20_ledger.fs` holds every dimension, taken from the master dimension ledger in `participants/03-field/FIELD-CAD-PACKAGE.md` §10. |
| `build.py` | Assembles the sources into `SummitPushField.fs` and fails on anything Onshape would reject: the dialect lint, the Onshape editor-warning check, calls not allowed during regeneration, and an API check against the Onshape standard library. |
| `verify/` | The off-line twin: `run.py` builds the same model with OpenCascade and runs the Feature Studio's own self-checks; `run_checks.py` runs the independent per-element checks in `verify/checks/`. |
| `AUTHORING.md` | How the sources are organized, the rules they follow, and the full command list. |

```bash
python3 organizers/source/featurescript/build.py              # assemble and lint SummitPushField.fs
python3 organizers/source/featurescript/verify/run.py         # build the field off-line and self-check it
python3 organizers/source/featurescript/verify/run_checks.py  # the independent per-element checks
```

The off-line build needs `pip install cadquery-ocp numpy`. The API check needs a copy of the
Onshape standard library: point `--std`, `$FS_STD` or a `.fs-std` link in this folder at it.
