"""Maximum-area inscribed ellipse -- the "John ellipse" / MVIE (thesis Section 2.3.2).

The ellipse is parametrised affinely as ``E = {x = G u + c : ‖u‖_2 <= 1}`` with
``G`` symmetric positive definite (eq. 2.6). Its area is proportional to
``det(G)``; maximising area is a convex program once ``det`` is replaced by its
concave surrogate ``log det``:

    maximise   log det(G)
    over       G (2x2 symmetric PSD),  c in R^2
    subject to ‖G a_i‖_2 + a_i^T c <= b_i,   i = 1..m         (eq. 2.9)

where ``(a_i, b_i)`` are the outward half-space rows of the (eroded) contact
polygon, from :func:`estimation.gripper.halfspaces`.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Ellipse:
    """Ellipse in the gripper plane, ``x = G u + c``."""

    G: np.ndarray          # (2, 2) symmetric positive definite shape matrix
    c: np.ndarray          # (2,) centre

    @property
    def axes(self):
        """Semi-axis lengths ``(major, minor)`` = eigenvalues of G, descending."""
        w = np.linalg.eigvalsh(self.G)
        return float(w.max()), float(w.min())

    @property
    def major_axis_direction(self):
        """Unit eigenvector of G for the largest eigenvalue (the major diagonal D)."""
        w, V = np.linalg.eigh(self.G)
        return V[:, int(np.argmax(w))]

    @property
    def orientation(self):
        """Angle of the major axis w.r.t. the gripper x-axis, in radians."""
        d = self.major_axis_direction
        return float(np.arctan2(d[1], d[0]))


def max_area_ellipse(polygon, solver="SCS"):
    """Solve the MVIE for a convex polygon and return an :class:`Ellipse`.

    Requires ``cvxpy``. ``polygon`` is an ``(N, 2)`` CCW array (already eroded).
    """
    import cvxpy as cp

    from .gripper import halfspaces

    A, b = halfspaces(polygon)

    G = cp.Variable((2, 2), symmetric=True)
    c = cp.Variable(2)
    constraints = [G >> 0]
    for a_i, b_i in zip(A, b):
        constraints.append(cp.norm(G @ a_i, 2) + a_i @ c <= b_i)

    cp.Problem(cp.Maximize(cp.log_det(G)), constraints).solve(solver=solver)
    if G.value is None:
        raise RuntimeError("MVIE solver failed to find a solution")
    return Ellipse(G=np.asarray(G.value), c=np.asarray(c.value))
