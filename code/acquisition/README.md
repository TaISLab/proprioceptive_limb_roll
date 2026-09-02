# Acquisition

ROS Noetic nodes that record a synchronised stream of:

- the passive phalange encoder angles of both pinches (gripper proprioception),
- the hand-held IMU / accelerometer (MPU) ground truth, over `rosserial`,
- optionally the Franka FR3 end-effector pose.

into per-participant CSVs under `data/raw/exp2_discrete/` and
`data/raw/exp3_continuous/` (schema in [`../../data/README.md`](../../data/README.md)).

This code is workstation-specific and is **not** required to reproduce the
analysis from already-recorded data.

## To add

- `record_node.py` (or a launch file): subscribe to the encoder and IMU topics,
  align on ROS time, write CSV.
- `imu_gt.py`: `q5_GT = atan2(a_y, a_z) − offset − π/2`, with the static
  calibration that estimates `offset` (sensor Z aligned with gravity).
- Experiment 2 helper: command the gripper fully open/closed between discrete
  captures.
- `rosserial` firmware for the MPU module.
