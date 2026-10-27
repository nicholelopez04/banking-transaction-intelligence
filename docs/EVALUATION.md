# Evaluation methodology

## Three different questions

1. The original baseline asks how a fixed Isolation Forest behaves on a later
   synthetic period. It trains on September 1-20 and tests September 21-30, 2026.
2. Phase 1/2 use September 1-14 for training and September 15-20 for validation.
   Phase 1 assesses the already-inspected September 21-30 historical test once
   after threshold selection. Phase 2 uses validation only for feature selection.
3. Phase 4 repeats model selection on newly generated September development sets,
   freezes choices, then generates October 1-10 future assessment sets.

The Phase 1 historical test is not a pristine holdout because its original results
were known. Phase 2 never uses that period to select features. Phase 4 avoids it
entirely. October was ungenerated until the protocol/model choices froze, but is
now assessed: further development must reserve new data instead of tuning to it.

## Features and leakage

The original/Phase 1 ratio uses full-training customer means. Test means are
training-only, but training rows can include themselves and later training rows.
That reference is ineligible for Phase 2 feature selection. Eligible features use
strictly earlier dates, with same-day exclusion and documented cold-start fallback.
StandardScaler fits only training rows. Injection labels never enter features.
Validation/future history updates with earlier observed amounts, not labels.

## Threshold and feature selection

Scores equal negative decision_function; score >= threshold is an alert. Compare
every distinct validation score plus zero and a no-alert endpoint. Maximize
validation F1; ties prefer fewer alerts, then higher threshold. This objective
weights precision/recall equally and is not an operational banking cost function.
A lower threshold generally increases recall and workload, while a higher one
can miss injections. The saved operating-point tables show that tradeoff.

Phase 2 compares the old reference, a prior-only two-feature set, and a five-feature
set. Only prior-only candidates are eligible. Maximize validation F1; ties prefer
fewer features, then fewer alerts, then alphabetical name. Reusing validation for
feature and threshold selection makes its metrics optimistic selection evidence,
not independent estimates. Perfect metrics on two injections offer little assurance.

## Repeated model comparison

Fixed seeds: 11, 22, 33, 44, 55. The separate scenario_period_v1 generator creates
1,000 development rows over 20 September days and 500 future rows over ten October
days; future seeds are development seed + 1,000,000. Injection count is round(n *
0.015); missing count is round(n * 0.005), using Python round. Missing rows can
include injections. The original generator and baseline remain unchanged.

Scenarios multiply injected amounts by uniform factors of 15-35 (large), 3-6
(moderate), or 0.01-0.08 (small). Scenarios share underlying seed-controlled draws,
so they are related. Modified values can overlap ordinary data. The label means
a deliberate perturbation, not necessarily an easily separable anomaly.

Both algorithms use the same saved Phase 2 feature selection, training rows and
training-only StandardScaler. Isolation Forest has 150 trees and contamination
0.03; LOF has 20 neighbors, contamination 0.03 and novelty=True. LOF scores only
unseen validation/future observations, as required by the
[official API guidance](https://scikit-learn.org/stable/auto_examples/neighbors/plot_lof_novelty_detection.html).
Scaling is especially relevant for LOF's neighbor distances. It is retained for
both methods for a consistent pipeline; Isolation Forest generally does not need it.

Each detector/seed/scenario gets its own validation-selected threshold. A validation
split without positives uses a predeclared 97th-percentile validation-score cutoff
and is retained, not dropped. None of the recorded runs needed that fallback.
Choose the algorithm by mean validation F1 across all 15 cases; ties prefer fewer
mean alerts, then alphabetical model name. No other hyperparameter search occurs.

Before any future data is generated, protocol.json records settings/source hashes,
and selection_freeze.json records the selected algorithm, thresholds and fitted
model/scaler bundle hashes. Both frozen candidates are assessed once per future
period for transparent comparison; future results never trigger reselection.

## Reporting and limitations

Report precision, recall, F1 and alert counts as mean, sample SD, minimum and maximum
across the five seeds per scenario. SD is descriptive variation, not a confidence
interval. Zero-denominator precision/recall use zero numerically, with defined flags
saved; the dashboard displays precision as N/A if there are no alerts. LOF is
deterministic for fixed input; its seed variation comes from data generation.
Isolation Forest also changes model randomness with the seed.

Each recorded future period has eight usable injections, so one miss changes
recall by 12.5 percentage points. Five seeds and three narrow amount scenarios do
not establish real-world quality. A non-injected alert can still be unusual.
Aggregate scenario means are descriptive, not an independent-sample significance
test. Deterministic reruns do not create new holdout evidence. Results on different
splits/generators do not establish a causal improvement over the original baseline.

Future work should predeclare richer scenarios, review-budget or cost objectives,
and new untouched evaluation periods before collecting new assessment results.
