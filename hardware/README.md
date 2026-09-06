# Hardware

pHRI workstation and gripper used to grasp and roll the participant's forearm
(thesis §2.1, §3.4.1, §4.1).

**Primary reference for the gripper's kinematics and dimensions:**

> Ruiz-Ruiz, F.J.; Ventura, J.; Urdiales, C.; Gómez-de-Gabriel, J.M. *Compliant
> gripper with force estimation for physical human–robot interaction.*
> Mechanism and Machine Theory, 2022, 178, 105062.
> https://doi.org/10.1016/j.mechmachtheory.2022.105062

That paper describes the four-finger under-actuated compliant gripper this
project uses (rigid-link fingers with a compression spring in place of one
link, high-resolution angular sensors at the passive joints) in full detail.
Full text obtained 2026-09-06 — design parameters below (its Table 1),
transcribed into `config/gripper.yaml`.

**Finger numbering cross-check:** the paper's Section 3.3 groups its four
fingers by side: {finger 1, finger 4} on one side of the gripper's x-axis,
{finger 2, finger 3} on the other. This matches Rodrigo's confirmed
`dedoN` mapping exactly — {dedo1=proximal-right, dedo4=distal-right} vs.
{dedo2=proximal-left, dedo3=distal-left} — good independent confirmation.

### Design parameters (Table 1)

| Parameter | Symbol | Value |
|---|---|---|
| Phalanx length | `a` | 40 mm |
| Distal phalanx base | `b` | 20 mm |
| Distal phalanx angle | `ψ` | 90° |
| Contact point | `p` | 20 mm |
| Servo origin angle | `γ` | 56.6° |
| `O1`–`Oa` distance | `e` | 28 mm |
| Servo lever | `d` | 50 mm |
| Link width | `w` | 10 mm |
| Distance between parallel fingers | `D` | 80 mm |
| `S1` elastic constant / rest / pre-load / max length | `k_S1` | 60 N/m / 16 mm / 44.7 mm / 60 mm |
| `S2` elastic constant / rest / pre-load / min length | `k_S2` | 900 N/m / 59 mm / 55 mm / 45 mm |

**Open question for Rodrigo/Jesús:** the real finger (Fig. 2–3 of the paper)
is a 5-bar linkage — the proximal phalanx (`a` = 40 mm) matches the thesis's
`L1`, but there's no single fixed "`L2`" in the real mechanism; the distal
side is instead defined by `b`, `ψ` and a variable-length elastic link
(`S2`), with the contact point at `p` = 20 mm along each phalanx. The
thesis's simple 2-link chain (`L1` = 40 mm, `L2` = 50 mm, used in
`gripper.py`) looks like a deliberate straight-line approximation of this for
the ellipse-fitting purpose. Worth confirming whether that approximation is
intentional/validated, or whether the contact-polygon code should eventually
use the real 5-bar geometry instead.

`D` = 80 mm (distance between the two parallel fingers of one pinch) is now
used as `config/gripper.yaml`'s `finger_base_positions_mm` (±40 mm,
symmetric) — this was the missing piece blocking `gripper.contact_polygon`.

## Manipulator

- **Franka FR3** collaborative arm, ROS Noetic.
- Cartesian impedance control with low rotational stiffness during the grasp
  trajectory (to allow angular accommodation of the forearm).
- Safety: kinematic limits (velocity, acceleration, jerk) and dynamic thresholds
  (joint-torque limit, external-force detection).

## Under-actuated gripper

- Two **parallel pinches**, **75 mm** apart, so two forearm cross-sections are
  sampled far enough apart to define the forearm axis.
- Each finger: two links — proximal phalanx **L1 = 40 mm**, distal phalanx
  **L2 = 50 mm** (thesis values, a 2-link approximation — see the design
  parameters and open question below) — base point `P_base` now filled in
  `config/gripper.yaml` from `D` = 80 mm below.
- Passive phalange angles `(θ1, θ2)` read by **high-resolution magnetic
  encoders**.
- Smart servo with position feedback on the actuated joint.
- Under-actuation gives passive accommodation to different forearm anthropometries
  (but the pentagon/rhombus contact models lose feasibility for large or
  off-centre forearms — thesis fig. 4.12).

## Vision (context, not used by this repo's estimator)

- 4 RGB-D cameras, one per corner of the station, extrinsically calibrated
  eye-to-hand w.r.t. the manipulator base; factory intrinsic calibration.

## Ground-truth sensor for q5

- IMU / accelerometer, **MPU module**, held in the participant's hand.
- Read over `rosserial`, synchronised in ROS with the gripper proprioception.
- `q5_GT = atan2(a_y, a_z) − offset − π/2` (thesis eq. 4.1).

## OptiTrack (Experiment 1 only)

- 10 cameras (6× Prime 13, 4× Prime 13W), 120 Hz; NaturalPoint, Inc.
- 15 mm IR marker pairs on both sides of each joint; wrist markers replaced by a
  hand-held two-marker stick to avoid interfering with the grasp.

## Files to add

- `cad/` — STEP/STL of the custom fingers and fixtures.
- `bom.csv` — bill of materials.
- `wiring.md` — encoder / servo / IMU connections and pinout.
