# Hardware

pHRI workstation and gripper used to grasp and roll the participant's forearm
(thesis §2.1, §3.4.1, §4.1).

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
  **L2 = 50 mm** — with a fixed base point `P_base` per finger (from CAD; fill in
  `config/gripper.yaml`).
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
