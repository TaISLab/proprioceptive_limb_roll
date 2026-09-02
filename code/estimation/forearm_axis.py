"""Forearm axis, elbow and wrist from the two pinch ellipses (thesis Section 3.4.4).

Given the geometric centres ``G1`` (proximal pinch) and ``G2`` (distal pinch) of
the two inscribed ellipses, expressed in Cartesian space:

    u_arm = (G1 - G2) / ‖G1 - G2‖         # forearm longitudinal axis (eq. 3.26-3.27)
    Pg    = (G1 + G2) / 2                 # grasp point

Elbow ``P2`` and wrist ``P3`` are then placed along ``u_arm`` using distances
recorded before the grasp:

    P2 = Pg - (l2 - d_grasp) * u_arm      # eq. 3.28
    P3 = Pg + d_grasp * u_arm             # eq. 3.29

where ``l2`` is the elbow-wrist anatomical length estimated during the
occlusion-free approach window and ``d_grasp`` is the distance between ``Pg`` and
the stored wrist position.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class ForearmAxis:
    u_arm: np.ndarray      # (3,) unit vector, distal -> proximal
    grasp_point: np.ndarray  # (3,) Pg
    elbow: np.ndarray      # (3,) P2
    wrist: np.ndarray      # (3,) P3


def reconstruct(G1, G2, l2, d_grasp):
    """Return a :class:`ForearmAxis`. ``G1``/``G2`` are 3-D ellipse centres."""
    G1 = np.asarray(G1, dtype=float)
    G2 = np.asarray(G2, dtype=float)
    d = G1 - G2
    n = np.linalg.norm(d)
    if n < 1e-9:
        raise ValueError("the two ellipse centres coincide; cannot define an axis")
    u_arm = d / n
    pg = 0.5 * (G1 + G2)
    return ForearmAxis(
        u_arm=u_arm,
        grasp_point=pg,
        elbow=pg - (l2 - d_grasp) * u_arm,
        wrist=pg + d_grasp * u_arm,
    )
