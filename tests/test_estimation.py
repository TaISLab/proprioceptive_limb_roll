"""Smoke tests for code/estimation. Run: ``python -m pytest`` from the repo root."""

import sys
import pathlib

import numpy as np
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "code"))

from estimation import gripper, pronosupination, forearm_axis  # noqa: E402


def test_finger_points_shapes_and_lengths():
    p = gripper.finger_points([0.0, 0.0], theta1=0.3, theta2=-0.2)
    assert p.shape == (3, 2)
    assert np.isclose(np.linalg.norm(p[1] - p[0]), gripper.L1_DEFAULT)
    assert np.isclose(np.linalg.norm(p[2] - p[1]), gripper.L2_DEFAULT)


def test_hexagon_polygon_is_convex_ccw():
    left = {"p_base": [-20.0, 0.0], "theta1": 1.9, "theta2": 0.6}
    right = {"p_base": [20.0, 0.0], "theta1": 1.24, "theta2": 0.6}
    poly = gripper.contact_polygon(left, right, model="hexagon")
    assert len(poly) == 6
    # signed area > 0  => counter-clockwise
    x, y = poly[:, 0], poly[:, 1]
    area2 = np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)
    assert area2 > 0


def test_halfspaces_contain_centroid():
    poly = np.array([[0, 0], [10, 0], [10, 6], [0, 6]], dtype=float)
    A, b = gripper.halfspaces(poly)
    c = poly.mean(axis=0)
    assert np.all(A @ c <= b + 1e-9)          # centroid satisfies a_i^T x <= b_i


def test_forearm_axis_and_frame():
    fa = forearm_axis.reconstruct(G1=[0, 0, 75], G2=[0, 0, 0], l2=250.0, d_grasp=40.0)
    assert np.allclose(fa.u_arm, [0, 0, 1])
    assert np.allclose(fa.grasp_point, [0, 0, 37.5])
    axes = pronosupination.arm_frame([0, 300, 0], [0, 0, 0], [0, 0, 250])
    R = np.array(axes)
    assert np.allclose(R @ R.T, np.eye(3), atol=1e-9)   # orthonormal


def test_q5_wraps_to_pi():
    axes = (np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0]))
    val = pronosupination.q5([0.0, 1.0, 0.0], axes)     # D along Y_arm
    assert -np.pi < val <= np.pi


@pytest.mark.parametrize("solver_missing", [False])
def test_mvie_on_square_is_near_circle(solver_missing):
    cvxpy = pytest.importorskip("cvxpy")
    from estimation import mvie
    square = np.array([[-5, -5], [5, -5], [5, 5], [-5, 5]], dtype=float)
    ell = mvie.max_area_ellipse(square)
    major, minor = ell.axes
    assert np.isclose(major, minor, rtol=1e-2)
    assert np.isclose(major, 5.0, rtol=5e-2)
    assert np.allclose(ell.c, [0, 0], atol=1e-3)
