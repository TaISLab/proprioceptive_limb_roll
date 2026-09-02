"""Experiment 3 — continuous q5 estimation (thesis §4.5).

Reproduces the temporal q5 tracking (pentagon + Fit Anatomical, 1-D
constant-velocity Kalman, Q = 0.05) against the accelerometer ground truth, and
the absolute-error trace (mean global error ≈ 8.31°). Discusses the
direction-dependent (hysteresis) error.

Run from the repo root:  ``python code/analysis/exp3_continuous.py``
Reads ``data/processed/exp3_continuous.parquet``; writes ``results/``.

TODO: implement after build_dataset.py produces the tidy table.
"""

from __future__ import annotations


def main() -> None:
    raise SystemExit("exp3_continuous.py is a stub")


if __name__ == "__main__":
    main()
