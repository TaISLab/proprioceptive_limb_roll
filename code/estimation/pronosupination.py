"""Pronosupination angle q5 from the distal ellipse (thesis Section 3.4.5).

Build the local arm frame ``{arm}`` at the wrist ``P3`` by Gram-Schmidt, because
the forearm (``P3 - P2``) and upper arm (``P1 - P2``) are not orthogonal at the
elbow:

    X_arm      = (P3 - P2) / ‖P3 - P2‖
    Y_arm_prev = (P1 - P2) / ‖P1 - P2‖
    Z_arm      = X_arm x Y_arm_prev
    Y_arm      = Z_arm x X_arm            # re-orthogonalised

q5 is the angle between ``Y_arm`` and the major diagonal ``D`` of the distal-pinch
ellipse, projected on the Y-Z plane of ``{arm}`` (fig. 3.7):

    phi5 = atan2(D_y, D_z)
    q5   = pi/2 - phi5                    # eq. 3.30

``q5`` sign convention: positive = supination, negative = pronation, 0 at neutral.
"""

from __future__ import annotations

import numpy as np


def arm_frame(p1_shoulder, p2_elbow, p3_wrist):
    """Return the orthonormal ``{arm}`` frame ``(X_arm, Y_arm, Z_arm)`` at the wrist."""
    p1 = np.asarray(p1_shoulder, dtype=float)
    p2 = np.asarray(p2_elbow, dtype=float)
    p3 = np.asarray(p3_wrist, dtype=float)

    x_arm = _unit(p3 - p2)
    y_prev = _unit(p1 - p2)
    z_arm = _unit(np.cross(x_arm, y_prev))
    y_arm = np.cross(z_arm, x_arm)
    return x_arm, y_arm, z_arm


def q5(major_axis_dir_3d, arm_axes):
    """Pronosupination angle in radians.

    Parameters
    ----------
    major_axis_dir_3d : (3,) array
        Direction of the distal ellipse major diagonal ``D`` in the same frame as
        ``arm_axes`` (e.g. mapped from the gripper plane to Cartesian space).
    arm_axes : tuple
        ``(X_arm, Y_arm, Z_arm)`` from :func:`arm_frame`.
    """
    x_arm, y_arm, z_arm = arm_axes
    d = np.asarray(major_axis_dir_3d, dtype=float)
    d_y = d @ y_arm
    d_z = d @ z_arm
    phi5 = np.arctan2(d_y, d_z)
    return _wrap(np.pi / 2 - phi5)


def _unit(v):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    if n < 1e-9:
        raise ValueError("zero-length vector")
    return v / n


def _wrap(a):
    """Wrap an angle to (-pi, pi]."""
    return (a + np.pi) % (2 * np.pi) - np.pi
