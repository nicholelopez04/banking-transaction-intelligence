# Phase 4: robustness and model comparison

## Outcome

Validation selected **isolation_forest** before future generation.
Mean validation F1 across the fixed seeds/scenarios was 0.6358
for Isolation Forest and 0.6076 for LOF. This is a
selection objective, not evidence of statistically significant superiority.

The experiment fitted 30 models (five seeds x three scenarios x two algorithms)
and assessed all 30 frozen models on paired October synthetic periods. Each
future dataset contains 500 raw rows, 498 usable rows, and eight usable injections.
No future results changed the selected algorithm, feature set or thresholds.
The original September historical test was not used in this experiment.

## Future assessment: mean +/- sample standard deviation

Each row summarizes five seeds. Percentage metric SDs are in percentage points.
These are not confidence intervals. Alert counts refer to the entire ten-day
future period, not daily alerts.

| Scenario | Detector | Precision | Recall | F1 | Alerts |
|---|---|---:|---:|---:|---:|
| large_spikes | Isolation Forest | 90.0% +/- 16.3 pp | 72.5% +/- 10.5 pp | 79.7% +/- 10.4 pp | 6.6 +/- 1.3 |
| large_spikes | Local Outlier Factor | 92.2% +/- 10.8 pp | 60.0% +/- 24.0 pp | 69.2% +/- 18.1 pp | 5.4 +/- 2.6 |
| moderate_spikes | Isolation Forest | 44.0% +/- 27.0 pp | 30.0% +/- 11.2 pp | 30.7% +/- 16.9 pp | 13.2 +/- 19.5 |
| moderate_spikes | Local Outlier Factor | 14.2% +/- 14.1 pp | 37.5% +/- 31.9 pp | 16.9% +/- 15.2 pp | 75.0 +/- 146.6 |
| small_amounts | Isolation Forest | 51.4% +/- 24.7 pp | 60.0% +/- 27.1 pp | 54.6% +/- 24.6 pp | 9.2 +/- 2.5 |
| small_amounts | Local Outlier Factor | 61.0% +/- 37.1 pp | 57.5% +/- 25.9 pp | 58.0% +/- 30.2 pp | 9.0 +/- 3.3 |

## What the results mean

Large amount spikes were easier for these amount-based features than moderate
spikes. In the moderate-spike scenario, LOF alerted on 337 of 498 usable future
transactions for seed 44, with seven matching injection labels. That seed's
validation-selected threshold did not generalize; it was not altered afterward.
Its workload variation is preserved rather than removing the run. Isolation Forest
also varied: its moderate-spike alert counts ranged from 2 to 48 across seeds.
LOF had a slightly higher mean F1 for small amounts, while validation selected
Isolation Forest on the predeclared average objective. Future comparisons did not
trigger a new selection.

One future run had no alerts, making precision undefined. Summary arithmetic uses
the documented zero convention, and per-run defined flags preserve that distinction.
There were 0 no-positive validation fallbacks.
Each future period has only eight known injections, so one additional miss changes
recall by 12.5 percentage points. Scenarios share underlying random draws and are
not independent real-world populations. These perturbation labels are not fraud
outcomes; other unusual transactions may lack injection labels.

## Reproducible design and evidence

- Seeds: 11, 22, 33, 44, 55; scenarios: large multipliers 15–35, moderate 3–6,
  small amounts 0.01–0.08. This separate generator preserves the original baseline.
- Train September 1–14; validate September 15–20; future October 1–10, 2026.
  Future RNG seed is development seed plus 1,000,000.
- Features: the saved Phase 2 selection, log amount and prior customer ratio.
  Strictly earlier-day history; training-only scaling; no labels in features.
- Same data and preprocessing for both algorithms. Fixed 150-tree Isolation Forest
  and 20-neighbor LOF in novelty mode; no extra hyperparameter search.
- Per-run thresholds maximize validation F1; the overall algorithm is selected by
  mean validation F1. Hyperparameters and history policy remain frozen.
- selection_freeze.json records selection and model/scaler hashes before October
  generation. All 30 frozen artifact hashes and paired dataset identities verified.
- protocol.json records source hashes, versions, parameters and date boundaries.
  Per-run raw data, predictions, thresholds and frozen bundles support review.
- Each rerun writes a separate directory. Deterministic reruns reuse the same data
  and do not create new independent holdout evidence.

## Files changed

Added phase4.py and test_phase4.py. Updated main.py with --phase 4, added a saved
Robustness view in app.py/dashboard_data.py, documented the method in README.md,
and listed joblib as a direct dependency. Earlier files were backed up under
backups/phase3-before-robustness. Prior outputs are preserved.

## Interview explanation

Isolation Forest scores how easily random splits isolate a transaction. LOF asks
whether a transaction sits in a region that is sparse relative to its neighbors.
Repeated seeds expose how sensitive the result is to the simulated data and,
for Isolation Forest, random model construction. A mean alone can hide a large
review workload spike; reporting SD, ranges and per-run evidence makes that visible.
Synthetic evaluation cannot establish real-world fraud detection quality.

LOF usage follows the official documentation:
https://scikit-learn.org/stable/auto_examples/neighbors/plot_lof_novelty_detection.html


## Verification completed

All 24 tests passed, covering prior phases, scenario reproducibility, paired date/ID
separation, no-positive threshold fallback, undefined metrics, sample-SD arithmetic,
training-only scaling, frozen model round-trip predictions, and dashboard controls.
Pip check reported no broken requirements. All 30 frozen model hashes, protocol and
validation hashes, and all 15 paired future dataset identities were checked.
All six original baseline artifacts remain byte-identical to the Phase 0 backup.
The local dashboard Robustness chart was visually verified and captured below.

![Saved robustness chart](dashboard_robustness.png)
