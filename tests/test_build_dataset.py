"""Tests for code/processing/build_dataset.py, using a synthetic fixture
(tests/fixtures/exp2_discrete_sample.csv) — not real participant data."""

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "code"))

from processing import build_dataset  # noqa: E402

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "exp2_discrete_sample.csv"


def test_load_exp2_discrete_renames_and_converts_to_radians():
    df = build_dataset.load_exp2_discrete(FIXTURE)

    expected_cols = {
        "id", "participant", "q5_gt",
        "theta1_prox_R", "theta2_prox_R",
        "theta1_prox_L", "theta2_prox_L",
        "theta1_dist_L", "theta2_dist_L",
        "theta1_dist_R", "theta2_dist_R",
    }
    assert expected_cols.issubset(df.columns)
    assert not any(c.startswith("dedo") for c in df.columns)

    row0 = df.iloc[0]
    assert np.isclose(row0["q5_gt"], np.radians(-90.0))
    assert np.isclose(row0["theta1_prox_R"], np.radians(60.0))   # dedo1_q1
    assert np.isclose(row0["theta2_dist_R"], np.radians(65.0))   # dedo4_q2
