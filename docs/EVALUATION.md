# Evaluation methodology — final accepted study

## What was evaluated

The primary evidence is the accepted Stage 5 paired independent synthetic evaluation: eight fixed scenarios, five fresh seeds each (730280001–730280040), 40 cases. Every case has 5,000 warmup rows and 20,000 scored rows. Totals: 200,000 warmup rows, 800,000 scored rows, 5,400 injected rows and 4,181 injected events. A burst or ramp event can span multiple rows; confusion matrices use rows. Non-injected rows are not verified legitimate transactions.

The [sealed protocol](results/stage5/protocol.json) preserves the approved plan and its historical approval-status text; that embedded proposal status is not the study's completion status. Subsequent approval authorized execution. The explicit once-generation instruction superseded the older proposed double-generation check. All final cases were generated exactly once before scoring, with seed claims, saved predictions and provenance. Reproducibility tests use separate fixture seeds, not regenerated final cases. No parameters or generator settings changed in response to results.

## Frozen comparators and leakage controls

Phase 2 uses log1p(amount) and amount divided by the strictly earlier-day customer average. Same-day peers are excluded. Cold history uses a neutral personal ratio. A training-only StandardScaler precedes Isolation Forest (150 trees, contamination 0.03, max_samples auto, random_state 42). The original 463-row fit and validation-selected score threshold >=0.1617068977463595 remain frozen.

Phase 6 v1 rules_B is an experimental development outcome, not a validated detector. It computes the frozen 18-feature B vector and uses five empirical-CDF rules: relative amount over 30 days, hourly transaction count, recent spending ratio, inactivity and category surprise. Rules use right-continuous empirical CDFs and frozen sparse/cold-history gates, with the maximum component as score and no model scaler. The threshold is strictly >0.99945009150821, calibrated at the higher-method 99th percentile of 60,000 calibration scores without labels.

The Phase 6 development design contained exactly nine candidates across two feature sets: rules_B, four Isolation Forest configurations and four diagonal Gaussian mixtures. Fit/calibration/selection/audit periods were chronological. Only rules_B and gmm_B_2 met the no-injection selection control. Their macro recalls were within the predefined 0.005 tolerance, with tied worst-type recall; rules_B won on mean positive-world precision. Higher-recall Isolation Forest candidates were ineligible because control reviews exceeded 50 per 10,000. The later audit was assessment-only; rules_B audit recall was 16/670 = 2.39%, including zero detections for several types. The final study did not replace this selected model.

Phase 6 histories use [t-window, t), excluding equal-timestamp peers until batch update. Warmup covers June 1–August 1, 2027; scoring covers August 1–September 30 exclusive, in UTC. Both pipelines observe the same underlying transactions but retain their different history definitions, fitted states, thresholds and training histories. Warmup updates history only. Streaming/batch parity, future-prefix invariance, label exclusion and frozen-state checks were recorded for all 40 cases.

Frozen fitted artifact SHA-256 values:

- Phase 2: `b862c621b4a404004e4ba00a5f052fc4e273fbefd06204dee7ad4a2b38419976`.
- Phase 6 v1: `2db5dbef512b77eb0c199eb94f9f486f0d548008ea191c9cd88106b8a5866f43`.

## Review policies and budgets

Phase 2 native reviews are all scores meeting its >= threshold, without an added queue. Phase 6 native reviews must exceed its strict > threshold and fit the completed-UTC-day queue. Daily quota is floor(cumulative scored rows/100) minus floor(previous-day cumulative scored rows/100). Sort eligible scores descending and transaction IDs ascending; truncate excess candidates. Unused quota expires, with no carryover or below-cutoff backfill. An incomplete day is not yet reviewed. The study scores through a fixed completed-period boundary. These are batch review decisions, not transaction blocking.

The equal-budget assessment is separate: both rankings receive exactly 200 reviews per 20,000 rows, allocated by the predefined daily quotas, totaling 8,000 each over 40 cases. It includes below-threshold candidates and no-injection controls. Its results cannot be substituted for native policy results.

## Scenario design and assumptions

| Scenario | Injected rows per case | Customers per case |
|---|---:|---:|
| S1 Contextual amounts | 40 | 240 |
| S2 Bursts | 100 | 420 |
| S3 Merchant changes | 200 | 360 |
| S4 Inactivity returns | 400 | 1,000 |
| S5 Spending ramps | 100 | 360 |
| S6 Mixed | 200 | 600 |
| S7 Rare injections | 40 | 800 |
| S8 No-injection control | 0 | 500 |

Distributions vary customer activity, within-customer amount variation, seasonality, drift, cold starts, merchant mix and prevalence. Ordinary transactions include heavy tails, clusters and inactivity returns. Interventions overlap ordinary behavior rather than creating trivially separated labels. An injected row is a generator intervention, not necessarily an objectively suspicious or fraudulent transaction. Exact multipliers, mixture distributions, event allocation and warmup rules are in the sealed protocol. The authors knew the model families; this is independent of selection data, not an externally blinded test.

## Metrics, aggregation and screening

Report TP, FP, FN, TN, precision, recall, F1, review counts/rates, ranking measures and event measures for every model/case/policy. All 160 records and every negative result are retained. Scenario summaries include pooled precision/F1, five-seed mean recall, sample SD, minimum and maximum. Zero-alert precision is undefined (N/A); recall for no-injection controls is N/A. Defined flags preserve interpretation. Zero-alert positive cases fail the precision screen.

The hypothetical native-policy screening targets require mean recall >=20% in every positive scenario and pooled precision >=10% within every positive scenario, plus <=100 reviews per control case and <=200 per case overall. Controls use workload gates, not recall. These are research benchmarks, not JPMorgan or banking requirements.

**Both models failed.** Phase 2 had TP=0, FP=83, FN=5,400, TN=794,517. Phase 6 had TP=462, FP=4,722, FN=4,938, TN=789,878: precision 8.912%, pooled recall 8.556%, F1 8.730%, 5,184 reviews. Both failed recall in every positive scenario. Phase 6 met precision only in S4 and S6, and all five controls exceeded 100 reviews. Both met overall capacity.

Of Phase 6 native detections, 452/462 (97.8%) were inactivity returns; contextual amounts contributed four, bursts one, merchant changes three and ramps two. Equal-budget TP was 78 for Phase 2 versus 507 for Phase 6, at 8,000 reviews each. Phase 6 equal-budget recall was worse in S1 and S5. See the [full report](results/stage5/REPORT.md), [pooled metrics](results/stage5/pooled_metrics.csv), [all cases](results/stage5/all_case_metrics.csv) and [screen table](results/stage5/native_screening_by_scenario.csv).

Paired differences use equal weights for the seven positive-scenario means, excluding controls. Ten thousand whole-case bootstrap resamples within fixed scenarios, seed 730289901, produce saved descriptive 95% percentile intervals. Native Phase 6-minus-Phase 2 mean recall difference is +5.407 percentage points [5.000, 5.821]; equal-budget difference is +4.414 points [3.843, 5.007]. These differ from pooled recall differences. Five seeds and fixed scenarios limit uncertainty inference; intervals are conditional, not multiplicity-adjusted or real-world guarantees. An aggregate relative gain does not satisfy absolute detection targets.

## Evidence preservation and presentation

The complete raw study, predictions, review queues, source snapshots and test records remain archived locally with verified SHA-256. The compact public evidence is copied byte-for-byte, linked to original study hashes through its [manifest](results/stage5/evidence_manifest.json), and hash-checked by the dashboard. The manifest is a provenance check, not an externally signed authenticity guarantee. No experiment is executed on dashboard load. Historical source snapshots remain fixed even when approved presentation code changes.

## Historical selection and development evidence

**Model Selection Only — Two Injected Anomalies:** Phase 2's 100% precision/recall used the same two validation positives for threshold and feature choice. This was selection evidence, not generalization. The earlier Phase 2 independent study had TP=0, FP=6, FN=3,000, TN=296,994 across 300,000 scored rows. Phase 6's development audit remained weak at 2.39% recall. Neither is replaced or revised by Stage 5.

The following original methodology is retained as historical documentation of earlier phases. Its references to future work or unassessed periods describe that earlier point in time; Stage 5 above is the final accepted study. Earlier robustness exercises are development context rather than the final independent assessment.

---

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
