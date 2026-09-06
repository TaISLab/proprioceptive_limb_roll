# Code

Python 3.11+. Install with `pip install -r ../requirements.txt`. Run every script
from the repository root so relative paths (`config/…`, `data/…`, `results/…`)
resolve.

| Folder | Purpose |
|--------|---------|
| `estimation/` | The proprioceptive pipeline as an importable package. Pure geometry/optimisation, no ROS. See [`../docs/method.md`](../docs/method.md). |
| `acquisition/` | ROS Noetic / `rosserial` nodes that log the phalange encoders and the IMU ground truth to `data/raw/`. Depends on the workstation; not needed to reproduce the analysis. |
| `processing/` | `data/raw/` → tidy per-trial tables in `data/processed/`: parsing, clock alignment, capture segmentation, GT recomputation. |
| `analysis/` | Error analysis and paper figures for Experiments 2 and 3, into `results/`. |

## `estimation/` modules

| Module | Thesis § | What it does |
|--------|----------|--------------|
| `gripper.py` | 3.4.1 | Finger forward kinematics; convex contact polygon (hexagon / pentagon / rhombus); polygon → outward half-spaces. |
| `erosion.py` | 3.4.2 | Morphological erosion (Minkowski difference, Shapely `buffer`, `d = -7.5 mm`). |
| `mvie.py` | 2.3.2 | Maximum-area inscribed ellipse (John ellipse) as a convex program (`cvxpy`). |
| `fit_anatomical.py` | 3.4.6 | Known-aspect-ratio ellipse fit with asymmetric penalty (`scipy` L-BFGS-B). |
| `forearm_axis.py` | 3.4.4 | Two ellipse centres → forearm axis; elbow and wrist localisation. |
| `pronosupination.py` | 3.4.5 | `{arm}` frame by Gram–Schmidt; `q5` from the distal ellipse major diagonal. |

## Typical pipeline

```bash
python code/processing/build_dataset.py
python code/analysis/exp2_discrete.py
python code/analysis/exp3_continuous.py
```

## Status

`estimation/` contains working implementations of the unambiguous steps
(kinematics, hexagon polygon, half-spaces, MVIE, Fit Anatomical, axis, `q5`).
Items still marked `NotImplementedError` / `TODO`: pentagon & rhombus polygon
construction (line-intersection, eq. 3.23–3.25), `P_base` values from CAD, the
gripper-plane → Cartesian mapping of the ellipse major diagonal, and the
acquisition / analysis scripts.

`processing/build_dataset.py` parses the real Experiment 2 (discrete) export
(column rename + deg→rad) — see `data/README.md`. It does not yet run the
geometric pipeline on that data (blocked on `P_base`), and Experiment 3
(continuous) still needs its own resampling step for the raw rosbag export.
