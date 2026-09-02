"""Morphological erosion of the contact polygon (thesis Section 3.4.2).

The polygon vertices sit on link rotation axes / intersections; the real contact
section is slightly smaller because the phalanges have thickness. The polygon is
shrunk along each edge normal by a Minkowski difference, implemented with
Shapely's ``buffer`` and a negative distance (``d = -7.5 mm`` in the thesis).
"""

from __future__ import annotations

import numpy as np

EROSION_DISTANCE_MM = -7.5


def erode(polygon, distance=EROSION_DISTANCE_MM):
    """Return the eroded polygon vertices (CCW) as an ``(N, 2)`` array.

    ``distance`` must be negative to shrink the polygon.
    """
    from shapely.geometry import Polygon  # local import keeps shapely optional

    if distance > 0:
        raise ValueError("erosion distance must be <= 0 to shrink the polygon")
    shrunk = Polygon(np.asarray(polygon, dtype=float)).buffer(
        distance, join_style=2  # mitre: keep it a polygon, no rounded corners
    )
    if shrunk.is_empty:
        raise ValueError("erosion removed the whole polygon; grasp too small")
    return np.asarray(shrunk.exterior.coords[:-1], dtype=float)
