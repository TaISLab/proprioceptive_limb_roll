# Data

License: **CC-BY-4.0** — see [`LICENSE.md`](LICENSE.md). Collected under signed
informed consent with guaranteed anonymisation (thesis §4.2), approved by the
Comité Ético de Experimentación de la Universidad de Málaga (CEUMA),
registration number **7-2023-H**.

## Where the data actually lives

The raw per-participant recordings are **archived separately on Zenodo**, not
committed to this git repository. Rationale: keep the raw dataset's release
timing independent of the code repository (e.g. to coordinate with the journal
submission), avoid bloating the git history with CSV data, and give the
dataset its own citable DOI.

**Status: published.** Rodrigo's raw exports for Experiments 2 and 3,
anonymised, including the Experiment 3 export's precomputed per-sample error
against ground truth (`error_abs`/`q5_inv`) — a conscious call by the PI to
publish the raw data alongside the code rather than withhold it.

- Dataset DOI: [10.5281/zenodo.22551414](https://doi.org/10.5281/zenodo.22551414)
- Dataset URL: https://zenodo.org/records/22551414

**Anonymisation:** the mapping from real participant names to codes (`P01`…)
is held privately by the PI, outside this repository and outside Zenodo — it
must never be committed or uploaded anywhere.

To reproduce the analysis locally, download the Zenodo archive and unpack it
under `data/raw/` following the layout below (git-ignored — see `.gitignore`).

## Organisation (actual, as received from Rodrigo)

```
data/
├── raw/                                      # git-ignored, never committed
│   ├── exp2_discrete/
│   │   └── exp2_discrete_anonymized.csv      # all 9 sessions in one wide table
│   └── exp3_continuous/
│       └── exp3_continuous_sweep01_raw.csv   # single rosbag-style export (see below)
└── processed/                                # tidy tables from code/processing/ (regenerable, not tracked)
```

This differs from the earlier per-participant-folder layout originally
sketched here (that was a guess made before any real export existed). Both
files use anonymised participant codes `P01`…`P08`, some with an `L` suffix
for a left-arm session (`P07`/`P07L` = same participant, right/left arm;
`P08L` = a participant with only a left-arm session recorded) — **no names,
DOB or other identifying data**.

## Raw file schema (as actually received — Exp. 2)

`exp2_discrete_anonymized.csv`: one wide table, one row per discrete capture,
all participants together.

| Column | Unit | Description |
|--------|------|-------------|
| `id` | – | global row index |
| `participant` | – | anonymised code (`P01`…, see above) |
| `q5_gt` | **deg** | ground-truth pronosupination angle (IMU) |
| `dedo1_q1`…`dedo4_q2` | **deg** | phalange encoder angles, 4 fingers × 2 joints each (proximal `q1`, distal `q2`) |

Notes:
- Units are **degrees**, not radians as originally assumed —
  `code/processing/build_dataset.py` converts to radians and renames columns
  to the pinch/side-labelled names `gripper.py` expects (see
  `config/gripper.yaml`'s `raw_finger_column_mapping`, confirmed by Rodrigo:
  `dedo1`=proximal-right, `dedo2`=proximal-left, `dedo3`=distal-left,
  `dedo4`=distal-right).
- Still open: per-participant anthropometry (`a`, `b` semi-axes) was not
  collected (see "Anthropometry / demographics" below for the fallback).
  `P_base` is now filled in `config/gripper.yaml` (from Ruiz-Ruiz et al.
  2022's `D` = 80 mm — see `hardware/README.md`), which unblocks running
  `gripper.contact_polygon` on this data; that step (parsing/unit conversion
  -> contact polygon -> ellipse fit -> q5) still needs to actually be wired
  up in `build_dataset.py`.

## Raw file schema (as actually received — Exp. 3)

`exp3_continuous_sweep01_raw.csv`: a raw `rosbag`-to-CSV export (one row per
ROS message, topic columns sparse/misaligned in time — needs resampling, not
a tidy table). Relevant columns:

| Column | Unit | Description |
|--------|------|-------------|
| `__time` | s (epoch) | message timestamp |
| `/roll_angle_x/data` | **deg** | IMU ground truth |
| `/tactile/q5_pinza_1/angle`, `/tactile/q5_pinza_2/angle` | **deg** | per-pinch local q5 estimate |
| `/tactile/info/elbow/*`, `/tactile/info/wrist/*`, `/tactile/info/grasping_point/*` | m | forearm-axis reconstruction (§3.4.4) |
| `q5_inv` | deg | `q5_pinza_2` re-expressed in the ground-truth sign convention (`180 − q5_pinza_2`) |
| `error_abs` | deg | **precomputed** \|`q5_inv` − ground truth\| — already the accuracy metric, at sample resolution |

`error_abs`/`q5_inv` being already computed means this file lets anyone
reconstruct the paper's headline accuracy number directly — the PI has
decided to publish it as-is regardless (see "Status" above). Also open:
`/tactile/q5_pinza_1/angle` sits in a narrow 99–109° band throughout the
recording (unlike `pinza_2`, which spans the full sweep) — worth confirming
with Rodrigo whether pinch 1
was static/occluded for this session or this is a genuine signal.

## How to publish the dataset on Zenodo

1. Create a new Zenodo record (zenodo.org → "New upload"), upload the raw data
   as a single archive (e.g. `proprioceptive_limb_roll_dataset_v1.zip`).
2. Metadata: type = Dataset, license = CC-BY-4.0, authors = same list as
   [`CITATION.cff`](../CITATION.cff), keywords matching the code repo, and a
   description pointing back to `https://github.com/TaISLab/proprioceptive_limb_roll`.
3. Publish to mint the DOI (or reserve a DOI first if you want to cite it in
   the paper/README before the final upload — Zenodo supports this).
4. Fill in the DOI/URL above and in the root `README.md` "Data" section, and
   add the dataset as a `references` entry in `CITATION.cff`.
5. Optional but recommended: link this GitHub repository to Zenodo
   (zenodo.org → GitHub) so tagged **code** releases also get their own
   software DOI, separate from the dataset DOI.

## Anthropometry / demographics

`sex` and `arm_tested` are inferred, not measured: `arm_tested` from the
session naming convention (an `L`-suffixed code = left arm; no suffix =
right, the default when the raw export doesn't say otherwise), `sex` from
the participant's real first name (checked privately against the anonymised
code, then discarded — see "Anonymisation" above). This is recorded in
`data/raw/exp2_discrete/participants_meta.csv` (git-ignored, like all raw
data).

**Per-participant forearm section semi-axes (`a`, `b`) were not collected —
confirmed, this is not a "pending" item.** Fit Anatomical needs a known
aspect ratio to calibrate against; without per-participant measurements, use
the population model from thesis ref. `[4]` (3D-scan ellipse fit, R²
0.898–0.980) or a fixed literature value instead. Target per-participant
schema, kept here for reference in case per-participant values become
available later:

```json
{
  "participant": "P01",
  "sex": "M",
  "arm_tested": "right",
  "forearm_section_semi_axis_a_mm": 0.0,
  "forearm_section_semi_axis_b_mm": 0.0,
  "reference_joint_config_deg": {"q1": 0, "q2": 0, "q3": 0, "q4": 90},
  "notes": ""
}
```

## Processed / tidy dataset

`code/processing/build_dataset.py` produces one long-format table per experiment:

`experiment, participant, capture, t, method, polygon_model, q5_est, q5_gt, signed_error, abs_error`

## Large files

If a recording set exceeds a few tens of MB, track it with **Git LFS**:

```bash
git lfs install
git lfs track "data/raw/**/*.csv"
git add .gitattributes
```
