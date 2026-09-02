# Data

License: **CC-BY-4.0** — see [`LICENSE.md`](LICENSE.md). Collected under signed
informed consent with guaranteed anonymisation (thesis §4.2).

## Organisation

```
data/
├── raw/
│   ├── exp2_discrete/        # Experiment 2 — 9 participants, discrete 20° sweep
│   │   ├── P01/
│   │   │   ├── P01_pronation.csv
│   │   │   ├── P01_supination.csv
│   │   │   ├── P01_anthropometry.json   # forearm section semi-axes a, b; arm tested
│   │   │   └── P01_notes.md
│   │   └── ...
│   └── exp3_continuous/      # Experiment 3 — continuous sweep, gripper closed
│       ├── P01/
│       │   ├── P01_sweep01.csv
│       │   └── P01_anthropometry.json
│       └── ...
└── processed/                # tidy tables from code/processing/ (regenerable, not tracked)
```

- One folder per participant, anonymised `P01`, `P02`, … No names, DOB or other
  identifying data anywhere in the repository.
- `raw/` is read-only; all cleaning happens in `code/processing/`.

## Raw file schema (proposed — confirm against the acquisition node)

| Column | Unit | Description |
|--------|------|-------------|
| `t` | s | ROS timestamp, zeroed at the start of the recording |
| `capture` | – | discrete capture index (Exp. 2); empty for continuous (Exp. 3) |
| `theta1_prox_L`, `theta2_dist_L` | rad | left-finger phalange encoder angles, proximal pinch |
| `theta1_prox_R`, `theta2_dist_R` | rad | right-finger phalange encoder angles, proximal pinch |
| `theta1_prox_L_d`, `theta2_dist_L_d`, `theta1_prox_R_d`, `theta2_dist_R_d` | rad | same, distal pinch |
| `q5_gt` | rad | accelerometer ground truth, `atan2(a_y,a_z) − offset − π/2` |
| `acc_x`, `acc_y`, `acc_z` | m/s² | raw accelerometer, for reprocessing the GT |
| `gripper_state` | open/closed | commanded gripper state (Exp. 2 toggles between captures) |
| `polygon_feasible_hex`, `polygon_feasible_pent`, `polygon_feasible_rhomb` | bool | per-frame feasibility |
| `ee_pose` | 7×float | end-effector pose (pos + quat) in the base frame, if logged |

## `*_anthropometry.json`

```json
{
  "participant": "P01",
  "sex": "M",
  "arm_tested": "right",
  "forearm_section_semi_axis_a_mm": 0.0,
  "forearm_section_semi_axis_b_mm": 0.0,
  "reference_joint_config_deg": {"q1": 0, "q2": 0, "q3": 0, "q4": 90},
  "notes": ""
}
```

## Processed / tidy dataset

`code/processing/build_dataset.py` produces one long-format table per experiment:

`experiment, participant, capture, t, method, polygon_model, q5_est, q5_gt, signed_error, abs_error`

## Large files

If a recording set exceeds a few tens of MB, track it with **Git LFS**:

```bash
git lfs install
git lfs track "data/raw/**/*.csv"
git add .gitattributes
```
