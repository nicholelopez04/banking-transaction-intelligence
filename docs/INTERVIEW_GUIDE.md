# Interview guide

## A concise project explanation

"I built a reproducible synthetic transaction analysis project using Python,
Pandas, SQLite and anomaly detection. I separated training, validation and future
assessment, computed customer history from earlier dates only, and compared
Isolation Forest with LOF across seeds and scenarios. I exposed saved evidence
in Streamlit. The experiment showed that perfect validation metrics on a few
synthetic injections can fail on later data. These are anomaly-review results,
not real-world fraud detection claims."

## Concepts to explain clearly

| Topic | Explanation tied to this project |
|---|---|
| Pandas groupby | Collect rows for the same customer/day and calculate sums and counts |
| Cumulative history | Running sums/counts minus the whole current day give earlier-day customer history |
| Merge | Attach that historical summary back to each transaction using customer and date |
| log1p | Compress very large amounts while remaining defined at zero |
| Cold start | No customer history exists yet; use a prior global fallback and neutral personal ratio |
| Training-only scaler | Learn feature means/scales from training, then apply them unchanged to later rows |
| SQL WHERE vs HAVING | WHERE filters rows before aggregation; HAVING filters the grouped results |
| Isolation Forest | Unusual observations can often be isolated by fewer random splits |
| LOF novelty mode | Compare new observations with neighbor density in the training reference |
| Contamination | Controls a training-derived default cutoff, not the future alert percentage |
| Decision threshold | Converts an anomaly score into a review flag; selection affects recall and workload |
| Precision | Of flagged records, what fraction has a known injection label? |
| Recall | Of known injections, what fraction was flagged? |
| F1 | Harmonic mean balancing precision/recall; it does not encode business costs |
| Precision@10 | Injection share within the ten highest-scored transactions in a complete period |
| Leakage | Using information unavailable when a transaction would have been scored |
| Reproducibility | Explicit seeds, pinned dependencies, saved protocol, source hashes and model artifacts |

## Evidence worth discussing

The original baseline found all four test injections with 16 alerts (25% precision).
Phase 1's threshold looked perfect on two validation injections but missed all four
historical test injections. I kept that failure visible instead of tuning to test.
Phase 2's expanded features tied the simpler prior-only set, so I kept the simpler
set. Phase 4 selected Isolation Forest on mean validation F1 before future data
existed. Its large-spike future F1 averaged about 0.80; moderate spikes were much
harder. LOF had a slightly higher small-amount F1, but one moderate-spike run
flagged 337 of 498 records. Average metrics alone would hide that workload risk.

## Questions to anticipate

**Why not call it fraud detection?** Labels mark deliberate synthetic amount
changes. We do not have confirmed fraud outcomes or representative real transactions.

**Is an unsupervised model using labels?** Model fitting uses features only.
Validation labels choose thresholds and models, so the operating-point selection
is label-informed. Calling the entire evaluation fully label-free would be wrong.

**Why separate validation and test?** Validation makes decisions; assessment checks
those fixed decisions on later observations. Repeatedly adjusting to assessment
results turns that data into development data.

**What did you fix about customer averages?** Full-window training averages include
future training rows. I used only earlier days for each row, excluded same-day peers,
and tested that later changes cannot alter earlier features.

**What would you improve next?** Predeclare richer scenarios, robust customer
history measures and cost/review-budget objectives, then reserve new untouched
periods. Any real-world claim needs representative data and reliable outcomes.

**Is this production ready?** It is a batch portfolio demo. It does not implement
real-time scoring, operational monitoring, deployment controls or payment decisions.

## Keep claims tied to evidence

Say "recall on known synthetic injections," not "fraud detection accuracy."
Say "no validation gain from extra features," not "features always hurt."
Say "variation across five seeds," not "a confidence interval."
Say "validation selected Isolation Forest," not "the test selected the winner."
