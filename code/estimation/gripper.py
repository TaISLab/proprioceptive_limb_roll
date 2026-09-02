"""Forward kinematics of the under-actuated gripper and contact-polygon construction.

Thesis Section 3.4.1. Each finger has two links (proximal L1, distal L2) and three
characteristic points:

    P_base  : centre of rotation of the proximal phalanx (fixed, from CAD)
    P_joint : centre of rotation of the distal phalanx
    P_tip   : physical tip of the distal phalanx

    P_joint = P_base  + [L1 cos(t1),        L1 sin(t1)]
    P_tip   = P_joint + [L2 cos(t1 + t2),   L2 sin(t1 + t2)]

where (t1, t2) are the proximal/distal joint angles read from the encoders.
"""

from __future__ import annotations

import numpy as np

L1_DEFAULT = 40.0  # mm, proximal phalanx
L2_DEFAULT = 50.0  # mm, distal phalanx


def finger_points(p_base, theta1, theta2, l1=L1_DEFAULT, l2=L2_DEFAULT):
    """Return ``(P_base, P_joint, P_tip)`` as a (3, 2) array for one finger."""
    p_base = np.asarray(p_base, dtype=float)
    p_joint = p_base + l1 * np.array([np.cos(theta1), np.sin(theta1)])
    p_tip = p_joint + l2 * np.array([np.cos(theta1 + theta2),
                                     np.sin(theta1 + theta2)])
    return np.vstack([p_base, p_joint, p_tip])


def contact_polygon(left, right, model="hexagon", l1=L1_DEFAULT, l2=L2_DEFAULT):
    """Build the convex contact polygon for one pinch.

    Parameters
    ----------
    left, right : dict
        ``{"p_base": (x, y), "theta1": rad, "theta2": rad}`` for each finger.
    model : {"hexagon", "pentagon", "rhombus"}
        Hexagon uses the six finger points directly (virtual edge between the two
        distal tips) and is always feasible. Pentagon and rhombus require the
        distal (or proximal) phalanx lines to intersect *outside* the gripper
        (t, s > 1 in eq. 3.23) and are ~80 % feasible.

    Returns
    -------
    (N, 2) ndarray
        Polygon vertices ordered counter-clockwise (interior on the left).
    """
    pl = finger_points(left["p_base"], left["theta1"], left["theta2"], l1, l2)
    pr = finger_points(right["p_base"], right["theta1"], right["theta2"], l1, l2)

    if model == "hexagon":
        # H = {Pbase_L, Pjoint_L, Ptip_L, Ptip_R, Pjoint_R, Pbase_R}
        poly = np.vstack([pl[0], pl[1], pl[2], pr[2], pr[1], pr[0]])
    elif model == "pentagon":
        # P = {Pbase_L, Pjoint_L, Vbot, Pjoint_R, Pbase_R}; Vbot = intersection of
        # the two distal phalanx lines forced outside the gripper (t, s > 1).
        raise NotImplementedError("pentagon: implement eq. 3.23-3.24 (line intersection)")
    elif model == "rhombus":
        # R = {Pjoint_L, Vdistal, Pjoint_R, Vproximal}
        raise NotImplementedError("rhombus: implement eq. 3.25 (phalanx-line intersections)")
    else:
        raise ValueError(f"unknown polygon model: {model!r}")

    return _order_ccw(poly)


def _order_ccw(points):
    """Order polygon vertices counter-clockwise about their centroid."""
    pts = np.asarray(points, dtype=float)
    c = pts.mean(axis=0)
    ang = np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0])
    return pts[np.argsort(ang)]


def halfspaces(polygon):
    """Convert a polygon into half-space rows ``a_i^T x <= b_i``.

    Returns ``(A, b)`` with ``A`` of shape (m, 2) holding **outward** unit
    normals and ``b`` of shape (m,). This is the form used by the John-ellipse
    constraint ``‖G a_i‖_2 + a_i^T c <= b_i`` (thesis eq. 2.8) and by
    :mod:`estimation.fit_anatomical`.
    """
    p = np.asarray(polygon, dtype=float)
    m = len(p)
    A = np.zeros((m, 2))
    b = np.zeros(m)
    c = p.mean(axis=0)
    for i in range(m):
        edge = p[(i + 1) % m] - p[i]
        n = np.array([edge[1], -edge[0]], dtype=float)   # a normal to the edge
        n /= np.linalg.norm(n)
        if n @ (p[i] - c) < 0:                           # force it to point outward
            n = -n
        A[i] = n
        b[i] = n @ p[i]
    return A, b
