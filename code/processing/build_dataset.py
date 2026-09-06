"""Turn the raw Experiment 2 (discrete) export into a tidy, radian-unit table.

Run from the repository root: ``python code/processing/build_dataset.py``

Input: ``data/raw/exp2_discrete/exp2_discrete_anonymized.csv`` (not tracked by
git — see data/README.md for how to obtain it). Renames the as-received
``dedoN_q{1,2}`` columns to the pinch/side-labelled names used by
``code/estimation/gripper.py`` and converts degrees to radians.

dedoN -> (pinch, side) mapping, confirmed by Rodrigo (2026-09-06), all
"respecto al usuario" (from the participant's point of view):
    dedo1 = proximal pinch, right finger
    dedo2 = proximal pinch, left finger
    dedo3 = distal pinch,   left finger
    dedo4 = distal pinch,   right finger

Note: this does *not* yet run the geometric estimation pipeline
(gripper.contact_polygon -> erosion -> ellipse fit -> q5). That needs
``P_base`` per finger from CAD in ``config/gripper.yaml``, still pending —
see data/README.md. This script only produces the cleaned, radian-unit input
that pipeline will consume once P_base lands.

Experiment 3 (continuous) is a separate, sparser rosbag export and needs its
own resampling/alignment step — not handled here yet.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW_EXP2 = pathlib.Path("data/raw/exp2_discrete/exp2_discrete_anonymized.csv")
PROCESSED = pathlib.Path("data/processed")

# dedoN -> (pinch, side)
DEDO_MAP = {
    1: ("prox", "R"),
    2: ("prox", "L"),
    3: ("dist", "L"),
    4: ("dist", "R"),
}


def _rename_map() -> dict[str, str]:
    rename = {}
    for dedo, (pinch, side) in DEDO_MAP.items():
        rename[f"dedo{dedo}_q1"] = f"theta1_{pinch}_{side}"
        rename[f"dedo{dedo}_q2"] = f"theta2_{pinch}_{side}"
    return rename


def load_exp2_discrete(path: pathlib.Path = RAW_EXP2) -> pd.DataFrame:
    """Load the raw wide CSV, rename finger columns, convert deg -> rad."""
    df = pd.read_csv(path)
    df = df.rename(columns=_rename_map())
    angle_cols = ["q5_gt"] + list(_rename_map().values())
    df[angle_cols] = np.radians(df[angle_cols])
    return df


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    if not RAW_EXP2.exists():
        raise SystemExit(
            f"{RAW_EXP2} not found — see data/README.md for how to obtain the "
            "Experiment 2 export."
        )
    df = load_exp2_discrete()
    out = PROCESSED / "exp2_discrete_tidy.csv"
    df.to_csv(out, index=False)
    print(f"wrote {len(df)} rows -> {out}")


if __name__ == "__main__":
    main()
