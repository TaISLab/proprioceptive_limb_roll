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
The exact finger base positions (`P_base`) and any link-length values there
should supersede the placeholders in `config/gripper.yaml` — accessing the
full text (e.g. via institutional access to ScienceDirect) to pull those
numbers is still pending.

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
  **L2 = 50 mm** (thesis values; cross-check against Ruiz-Ruiz et al. 2022
  above) — with a fixed base point `P_base` per finger (see that paper; still
  to be transcribed into `config/gripper.yaml`).
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
