# Data

## Organisation

```
data/
├── raw/         # exactly as logged by the acquisition software — treat as READ-ONLY
│   ├── P01/
│   │   ├── P01_session01_<condition>.csv
│   │   └── P01_notes.md
│   ├── P02/
│   └── ...
└── processed/   # tidy tables produced by code/processing/ (regenerable, not tracked)
```

- One folder per participant, anonymised as `P01`, `P02`, … No names, dates of
  birth, or other identifying data anywhere in this repository.
- Do not edit files in `raw/` by hand. All cleaning happens in
  `code/processing/` and is written to `processed/`.

## Raw file format

> ⚠️ **TODO** — replace with the real columns once the acquisition script is
> finalised. Example schema:

| Column | Unit | Description |
|--------|------|-------------|
| `t` | s | timestamp from start of trial |
| `trial` | – | trial index within the session |
| `condition` | – | experimental condition label |
| `target_angle` | deg | commanded forearm roll angle |
| `actual_angle` | deg | measured forearm roll angle (ground-truth sensor) |
| `reported_angle` | deg | participant's proprioceptive estimate |
| `grip_force` | N | gripper force set-point / measured |
| `finger_pos` | mm or deg | adaptive finger configuration |
| `direction` | pron/sup | rotation direction |
| `response_time` | s | time from end of rotation to report |

## Processed / tidy dataset

`code/processing/build_dataset.py` (or `.m`) produces one long-format table:

`participant, trial, condition, target_angle, actual_angle, reported_angle, signed_error, abs_error, ...`

## Large files

If raw data exceeds a few tens of MB, track it with **Git LFS**:

```bash
git lfs install
git lfs track "data/raw/**/*.csv"
git add .gitattributes
```

## Ethics

> ⚠️ **TODO** — ethics committee approval reference, informed consent statement,
> and any data-sharing restrictions.
