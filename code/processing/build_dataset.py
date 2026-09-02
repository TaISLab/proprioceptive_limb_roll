"""Turn raw recordings in ``data/raw/`` into tidy tables in ``data/processed/``.

Run from the repository root:  ``python code/processing/build_dataset.py``

Output (one row per frame / capture):
    experiment, participant, capture, t, method, polygon_model,
    q5_est, q5_gt, signed_error, abs_error

TODO: implement once the acquisition CSV schema is fixed (see data/README.md).
"""

from __future__ import annotations

import pathlib

RAW = pathlib.Path("data/raw")
PROCESSED = pathlib.Path("data/processed")


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    experiments = sorted(p.name for p in RAW.iterdir() if p.is_dir())
    print(f"raw experiments found: {experiments or '(none yet)'}")
    raise SystemExit("build_dataset.py is a stub — implement the parser next")


if __name__ == "__main__":
    main()
