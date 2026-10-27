# Phase 2 results

## Changes

Added phase2.py and test_phase2.py; updated main.py dispatch and README.md.
Default main.py runs validation-only Phase 2; --phase 1 reproduces Phase 1.
Original source and documentation were copied to backups/phase1-before-phase2.
Existing baseline and Phase 1 outputs were not overwritten.

## Evidence

Training: 463 rows. Validation: 199 rows, two known synthetic injections.
All three feature sets yielded two alerts, 100% validation precision, recall and F1.
The selected eligible set is prior_ratio (two features), threshold 0.161707 approx.
The five-feature enhanced set showed no measured validation gain.
The Phase 1 reference is ineligible because its training means include later
training records. These reused validation observations cannot establish generalization.
Historical test and future final holdout were not scored during Phase 2.

## History and interview explanation

A groupby aggregates amounts and counts for each customer and day. Cumulative
sums minus the current day's contribution yield history from strictly earlier days.
Joining that history back to each transaction prevents both self-inclusion and
same-day look-ahead. Validation history updates with earlier observed amounts,
not labels. StandardScaler learns parameters from training rows only.
New customers use earlier global means (fixed $1 when none exist) and a neutral
personal ratio of 1. Prior-count and cold-start features are available in the
expanded candidate. Sparse histories and injected spikes can distort means.
No timestamp or merchant field was invented; the synthetic generator is unchanged.
All metrics concern synthetic injections, never confirmed fraud.

## Verification

10 unit tests passed, including Phase 1 tests and five historical-feature tests.
The feature experiment completed successfully using the existing Python 3.12 venv.
