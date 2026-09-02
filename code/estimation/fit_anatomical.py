"""Flexible anatomical ellipse fit with an asymmetric penalty (thesis Section 3.4.6).

The MVIE tends to return low-aspect-ratio (over-rounded) ellipses when the gripper
cannot fully accommodate the arm. Instead, start from the patient's *known*
forearm section (semi-axes ``a``, ``b``) and search for the rigid-plus-isotropic-
scale placement that best fits inside the contact polygon.

State: ``x = [cx, cy, theta, s]`` where ``theta`` is the ellipse orientation (=
pronosupination ``q5``) and ``s`` is an isotropic scale (soft-tissue
compression/expansion). Shape matrix (eq. 3.31-3.32):

    S = diag(a * s, b * s)
    G = R(theta) @ S @ R(theta).T

Cost (eq. 3.33-3.34):

    J(x) = sum_i L(d_i)  +  lambda * (s - 1)^2
    L(d) = 10.0 * d^2   if d > 0    (ellipse crosses the edge: hard collision penalty)
           0.5  * d^2   if d <= 0   (ellipse strictly inside: soft attraction to the wall)

with ``d_i = ‖G a_i‖_2 + a_i^T c - b_i`` the John-form slack of edge ``i``
(``d_i <= 0`` means "inside"). Solved with L-BFGS-B; bounds in ``config/gripper.yaml``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from .mvie import Ellipse

PENALTY_OUTSIDE = 10.0
PENALTY_INSIDE = 0.5
SCALE_REG_LAMBDA = 50.0


@dataclass
class FitResult:
    ellipse: Ellipse
    theta: float            # orientation == q5 (rad)
    scale: float            # isotropic scale s
    cost: float
    success: bool


def _rot(theta):
    ct, st = np.cos(theta), np.sin(theta)
    return np.array([[ct, -st], [st, ct]])


def _shape_matrix(a, b, theta, s):
    R = _rot(theta)
    return R @ np.diag([a * s, b * s]) @ R.T


def _edge_slacks(G, c, A, b):
    # d_i = ‖G a_i‖_2 + a_i^T c - b_i ; d_i <= 0 => inside
    return np.linalg.norm(A @ G, axis=1) + A @ c - b


def fit(polygon, a, b_semi, *, x0=None, theta_seeds=None,
        center_radius_mm=30.0, scale_bounds=(0.7, 1.3),
        penalty_outside=PENALTY_OUTSIDE, penalty_inside=PENALTY_INSIDE,
        scale_reg_lambda=SCALE_REG_LAMBDA):
    """Fit an ellipse of semi-axes ``(a, b_semi)`` inside ``polygon``.

    ``polygon`` is an ``(N, 2)`` CCW array (already eroded). Returns a
    :class:`FitResult`; ``result.theta`` is the pronosupination estimate ``q5``.
    """
    from .gripper import halfspaces

    A, bvec = halfspaces(polygon)
    centroid = np.asarray(polygon, dtype=float).mean(axis=0)

    def cost(x):
        cx, cy, theta, s = x
        G = _shape_matrix(a, b_semi, theta, s)
        d = _edge_slacks(G, np.array([cx, cy]), A, bvec)
        w = np.where(d > 0.0, penalty_outside, penalty_inside)
        return float(np.sum(w * d * d) + scale_reg_lambda * (s - 1.0) ** 2)

    bounds = [
        (centroid[0] - center_radius_mm, centroid[0] + center_radius_mm),
        (centroid[1] - center_radius_mm, centroid[1] + center_radius_mm),
        (-np.pi / 2, np.pi / 2),
        (scale_bounds[0], scale_bounds[1]),
    ]

    if theta_seeds is None:
        # narrow search around the previous estimate first, else spread seeds
        theta_seeds = ([x0[2]] if x0 is not None
                       else list(np.linspace(-np.pi / 2, np.pi / 2, 7)))

    best = None
    for th in theta_seeds:
        start = (x0 if x0 is not None
                 else np.array([centroid[0], centroid[1], th, 1.0]))
        start = np.array([start[0], start[1], th, start[3]])
        res = minimize(cost, start, method="L-BFGS-B", bounds=bounds)
        if best is None or res.fun < best.fun:
            best = res

    cx, cy, theta, s = best.x
    G = _shape_matrix(a, b_semi, theta, s)
    return FitResult(
        ellipse=Ellipse(G=G, c=np.array([cx, cy])),
        theta=float(theta),
        scale=float(s),
        cost=float(best.fun),
        success=bool(best.success),
    )
