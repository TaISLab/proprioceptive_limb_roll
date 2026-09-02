# Code

| Folder | Purpose |
|--------|---------|
| `acquisition/` | Firmware and host scripts that run the experiment: drive the gripper/rotation actuator, present conditions, and log raw data to `data/raw/`. |
| `processing/`  | Turn `data/raw/` into tidy tables in `data/processed/`: parsing, clock synchronisation, trial segmentation, artefact rejection. |
| `analysis/`    | Statistics and paper figures from `data/processed/` into `results/`. |

## Conventions

> ⚠️ **TODO** — pick the stack and delete the other column.

- **Language:** Python 3.11+ *and/or* MATLAB R202x.
- **Python deps:** listed in `requirements.txt` at repo root.
- Scripts are run from the repository root so relative paths (`data/…`,
  `results/…`) resolve.
- Every script that writes output prints the exact input files it read and output
  files it wrote.

## Typical pipeline

```bash
python code/processing/build_dataset.py
python code/analysis/run_analysis.py
```
