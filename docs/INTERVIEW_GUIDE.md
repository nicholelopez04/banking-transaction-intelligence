# Interview guide — final research findings

## A concise explanation

“I built a synthetic transaction intelligence portfolio using Python, Pandas, SQLite and Streamlit. I tested customer-history leakage, froze the models and review policies, and evaluated them on 40 new paired cases. Perfect validation metrics on two injected examples did not generalize. A richer behavioral pipeline found more injections, but nearly all its detections were inactivity returns, it exceeded control-review limits, and neither pipeline passed the predefined research screens. I preserved those failures and made the complete evidence visible rather than tuning to the test.”

## The numbers to know

- Final study: eight scenarios × five seeds, 800,000 scored rows, 5,400 injected rows, 4,181 injected events and 200,000 warmup rows.
- Phase 2 native: 83 reviews, zero injected rows detected; precision/recall/F1 all zero.
- Phase 6 v1 native: 5,184 reviews, 462 detections, 8.912% precision, 8.556% pooled recall, 8.730% F1.
- 452 of those 462 detections (97.8%) were inactivity returns. Only ten covered all other types.
- Equal-budget ranking only: exactly 8,000 reviews each; Phase 2 detected 78 and Phase 6 detected 507. Phase 6 still lost on contextual amounts and spending ramps.
- Both failed 20% mean recall in every positive scenario. Phase 6 passed scenario precision only in S4/S6 and failed all five control workloads. These are hypothetical synthetic benchmarks, not banking requirements.

Use the [saved report](results/stage5/REPORT.md), [pooled metrics](results/stage5/pooled_metrics.csv), and [all per-case results](results/stage5/all_case_metrics.csv) to substantiate claims.

## Questions to anticipate

**Why was validation precision and recall 100%?** The Phase 2 model selected features and a threshold using only two injected positives. Label this “Model Selection Only — Two Injected Anomalies.” It was not independent performance. Its earlier independent study missed all 3,000 injected rows; the final paired study also found zero at its native threshold.

**What did Phase 6 change?** New chronological development data, richer timestamp histories, two feature sets, nine predefined candidates, label-free percentile calibration and an explicit end-of-day review budget. Candidates included empirical-CDF rules, Isolation Forest and diagonal Gaussian mixtures. No expanded search was performed after seeing results.

**Why select rules_B if Isolation Forest had higher recall?** Higher-recall Isolation Forest configurations violated the predefined no-injection control gate. Only rules_B and gmm_B_2 were eligible; their macro recall difference fell within the predefined tie tolerance and worst-type recalls tied, so positive-world precision selected rules_B. A selected development outcome is not necessarily a successful model. Its later development audit recall was only 16/670 = 2.39% and did not trigger reselection.

**How did you prevent leakage?** Phase 2 averages use strictly earlier dates. Phase 6 windows include [t-window, t), excluding equal-timestamp peers. Training-only fitted states and score-only calibration were frozen. Tests cover future perturbations, labels, ordering, cold starts, streaming parity and chronological boundaries. Warmup updates history without fitting. No final test was used to tune the pipeline.

**What is an empirical-CDF rule?** A value is compared with a frozen reference distribution; its percentile is the fraction of reference values less than or equal to it. Five behavioral percentiles feed a maximum score with fixed sparse-history gates. This is an unusualness score, not a fraud probability.

**Why report two review policies?** Native policies describe actual frozen decisions with unequal workloads. Equal-budget ranking describes prioritization with identical total review capacity, including below-threshold rows. Mixing them would misrepresent operational behavior. The Phase 6 queue is batch review after UTC day closure, not real-time blocking.

**Did Phase 6 outperform Phase 2?** It had higher aggregate synthetic recall under both comparisons, with conditional paired intervals, but this was concentrated in one anomaly type. It lost in two equal-budget scenarios, failed workload controls and failed every scenario's recall requirement. Different training data, features and policies prevent attributing the gain solely to an algorithm. I would not call it a generally superior or practical fraud detector.

**What do the uncertainty intervals mean?** They describe paired variation conditional on these fixed scenarios and five seeds, using whole-case bootstrap resampling within scenarios. The native mean-scenario recall difference was +5.407 percentage points, interval [5.000, 5.821]. This is not the pooled recall difference, and the interval does not establish representative banking performance. Sample SD in scenario charts is a different descriptive quantity.

**Are false positives legitimate transactions?** No. FP here means a review without a synthetic injection label. Such a transaction may still be unusual. An injected row may also look ordinary. There are no verified real-world fraud outcomes in this study.

**What technical skills does the project demonstrate?** Pandas cleaning and groupby operations, chronological feature state, training-only preprocessing, explicit model-selection rules, reproducible fixtures, serialized artifact checks, confusion/ranking metrics, SQLite aggregation, Streamlit interactions and evidence provenance. SQL WHERE filters rows before aggregation; HAVING filters grouped totals. Descriptive full-period SQL summaries never feed historical scoring features.

**Is it production-ready?** No. Synthetic labels and populations, narrow coverage, failed targets and no operational validation prevent that claim. The hosted dashboard is a saved-evidence portfolio viewer. Further model development would need a separately approved design and new untouched assessment data; no Phase 6 v2 has begun.

## Keep claims precise

Say “synthetic injection detection,” not “fraud detection accuracy.” Distinguish rows from events, pooled metrics from mean-scenario metrics, native decisions from equal-budget ranking, and validation selection from independent evaluation. Keep negative results visible. No new dashboard deployment is claimed until separately approved and verified.
