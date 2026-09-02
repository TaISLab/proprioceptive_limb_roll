"""Proprioceptive estimation of forearm roll (pronosupination, q5).

Pipeline (thesis Sections 2.3 and 3.4):

    phalange encoder angles
        -> gripper.contact_polygon()          # convex polygon of the grasp
        -> erosion.erode()                    # account for phalange thickness
        -> mvie.max_area_ellipse()  OR  fit_anatomical.fit()
        -> forearm_axis.reconstruct()         # two ellipse centres -> forearm axis, elbow, wrist
        -> pronosupination.q5()               # roll angle from the distal ellipse

All lengths are in millimetres and all angles in radians unless stated otherwise.
"""

from . import gripper, erosion, mvie, fit_anatomical, forearm_axis, pronosupination

__all__ = [
    "gripper",
    "erosion",
    "mvie",
    "fit_anatomical",
    "forearm_axis",
    "pronosupination",
]
