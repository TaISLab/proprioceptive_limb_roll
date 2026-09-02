# Proprioceptive estimation of forearm roll during robotic grasping

Programs and data for the study of **human proprioceptive estimation of forearm
rotation (limb roll, i.e. pronation/supination)** when the forearm is grasped by
a **robotic gripper with adaptive (underactuated) fingers**.

This repository corresponds to the experiment described in **Section 2.3** of the
associated manuscript.

> ⚠️ **TODO** — Fill in once Section 2.3 text is available:
> full title of the paper, authors, venue/DOI, and a 3–4 sentence abstract of the
> experiment (what was manipulated, what participants reported, main outcome).

---

## 1. Experiment overview

> ⚠️ **TODO** — Replace the placeholder description below with the real protocol
> from Section 2.3.

- **Goal.** Quantify how accurately humans estimate the roll angle of their own
  forearm while it is held by an adaptive robotic gripper, and how gripper
  parameters (grip force, finger configuration, contact location) affect that
  estimate.
- **Task.** The participant's forearm is passively rotated to a target roll
  angle by the gripper/actuator; the participant reports the perceived angle
  (verbal report / dial / matching with the contralateral limb — *TODO: which*).
  Vision of the arm is occluded.
- **Independent variables (TODO confirm):** target roll angle, grip force,
  rotation direction (pronation vs. supination), contact position along the
  forearm.
- **Dependent variables (TODO confirm):** reported angle, signed error
  (perceived − actual), absolute error, response time.

## 2. Hardware

> ⚠️ **TODO** — Specify from Section 2.3.

| Item | Model / description | Notes |
|------|--------------------|-------|
| Robotic gripper | *TODO (e.g. adaptive/underactuated parallel gripper)* | number of fingers, actuation |
| Adaptive fingers | *TODO* | material, compliance, phalanges |
| Rotation actuator | *TODO* | motor + encoder providing ground-truth roll angle |
| Force/torque sensing | *TODO* | at wrist / in fingers |
| Reference angle sensor | *TODO (encoder / IMU / goniometer on the arm)* | ground truth for roll |
| Acquisition | *TODO (microcontroller / DAQ / ROS)* | sampling rate |

See [`hardware/README.md`](hardware/README.md) for wiring, CAD and bill of
materials.

## 3. Participants

> ⚠️ **TODO** — N, age range, handedness, inclusion/exclusion criteria, which arm
> was tested, ethics approval reference and informed-consent statement.

## 4. Repository layout

```
.
├── code/
│   ├── acquisition/   # firmware / scripts that run the experiment and log data
│   ├── processing/    # raw -> tidy: parsing, synchronisation, trial segmentation
│   └── analysis/      # statistics and figures for the paper
├── data/
│   ├── raw/           # exactly as logged, one folder per participant/session (read-only)
│   └── processed/     # derived tables (regenerable; not tracked by default)
├── docs/
│   ├── protocol.md    # step-by-step experimental protocol
│   └── section_2.3.md # transcription / notes of the manuscript section
├── hardware/          # gripper description, CAD, BOM, wiring
└── results/
    ├── figures/       # generated figures (not tracked by default)
    └── tables/        # generated tables (not tracked by default)
```

## 5. Data

Raw data format, variable names and units are documented in
[`data/README.md`](data/README.md). Each participant/session is anonymised with a
code (e.g. `P01`, `P02`, …); no identifying information is stored in this
repository.

## 6. Reproducing the analysis

> ⚠️ **TODO** — adjust to the actual language/toolchain (Python and/or MATLAB).

```bash
# Python example
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

python code/processing/build_dataset.py      # data/raw -> data/processed
python code/analysis/run_analysis.py         # -> results/figures, results/tables
```

## 7. Citation

If you use this code or data, please cite the paper (see
[`CITATION.cff`](CITATION.cff)).

## 8. License

- **Code:** MIT (see [`LICENSE`](LICENSE)).
- **Data:** *TODO — recommend CC-BY-4.0; confirm with co-authors and ethics
  approval before publishing.*

## 9. Contact

J. Manuel Gómez-de-Gabriel — Universidad de Málaga — <jesus.gomez@uma.es>
