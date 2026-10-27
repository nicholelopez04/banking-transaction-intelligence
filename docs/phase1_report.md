# Phase 1 results

Training: 463 rows; validation: 199 rows, 2 injected positives;
historical test: 333 rows, four injected positives.

Selected validation threshold: 0.16963803312008074.
Validation precision, recall and F1: 1.0; alerts: 2.
Historical test precision, recall and F1: 0.0 (precision uses zero_division=0;
with no alerts its mathematical denominator is zero). Alerts: zero.
Confusion counts: TP=0, FP=0, FN=4, TN=329. Precision@10: 0.4.

This operating point failed to generalize. Perfect validation metrics on few
synthetic positives do not establish reliability. The selected threshold was not
changed after inspecting test outcomes. The original baseline found all four test
injections with 16 alerts, but the new training window also differs; this is not
an isolated causal comparison of thresholds. A fresh final period remains reserved
for assessment after subsequent model and feature choices are frozen.

Validation and test use training-only customer means; training features still
use full-window customer averages pending Phase 2. Synthetic injections are not fraud.
Original baseline artifacts were verified byte-for-byte against the backup.
