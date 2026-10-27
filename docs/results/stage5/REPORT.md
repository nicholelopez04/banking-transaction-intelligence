# Stage 5 final paired independent synthetic evaluation

This is a single-draw evaluation of the frozen original Phase 2 pipeline and frozen Phase 6 v1 rules_B experimental development outcome. Labels are synthetic intervention assignments, **not verified real-world fraud**. Non-injected rows are not verified legitimate. Neither model, cutoff, rule, preprocessing or review policy was changed after freezing.

## Protocol and integrity

Study: `20261026T225228687831-0400`. Protocol SHA-256: `5c6f4d1a6704dd109689aae92f6cdfe97930c2d4518a9f492f12d47717efd9f2`. Forty cases, eight settings x five seeds, each generated exactly once after sealing. Latest human approval explicitly superseded the old proposal's double-generation step. Fixture-only reproduction and saved-file checksum readback were used; no final case was regenerated, replaced or selected based on scores.

Unique raw records: **1,000,000**, consisting of **200,000 warmup** and **800,000 scored**. Injected scored rows: **5,400**. Injected events: **4181**, counted once per contextual/merchant/inactivity row and once per multirow burst/ramp group. Rows, events, customers and replicate cases are different units. Both models score the same 800,000 rows; the two models and two policies do not create additional independent raw observations.

Each final seed has an exclusive persistent generation claim. The approved scenario/settings/seed table, warmup/arrival procedures, model/source/dependency hashes, generator clarifications and reporting rules are in protocol.json and source_snapshot. Final input hashes are checked after writing and after scoring. Frozen model/reference/scaler state hashes and historical archive hashes are checked before/after. See integrity and test records for exact details.

## Interpretation first

Both aggregate recall differences and their lower conditional interval bounds favor Phase 6: **True**. This Boolean describes the registered relative-evidence rule only. See all scenario losses, volume differences and screen failures below; it is not a claim of production readiness or actual fraud detection.

| model | policy | TP | FP | FN | TN | reviews | precision | recall | f1 | positive_scenario_macro_recall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase2 | equal_budget | 78 | 7922 | 5322 | 786678 | 8000 | 0.009750 | 0.014444 | 0.011642 | 0.019357 |
| phase2 | native | 0 | 83 | 5400 | 794517 | 83 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| phase6_v1 | equal_budget | 507 | 7493 | 4893 | 787107 | 8000 | 0.063375 | 0.093889 | 0.075672 | 0.063500 |
| phase6_v1 | native | 462 | 4722 | 4938 | 789878 | 5184 | 0.089120 | 0.085556 | 0.087302 | 0.054071 |

The native and equal-budget rows are distinct decision policies and must not be substituted for one another. Native Phase 2 keeps all >=0.1617068977463595 alerts without a cap. Native Phase 6 keeps >0.99945009150821 eligibility plus its frozen completed-day quota. Common-budget rankings ignore numeric cutoffs and require exactly 200 reviews per case for both score rankings, even when signals are weak. Scores are on unrelated scales and are not fraud probabilities.

## Native-policy scenario outcomes

Counts are pooled across five cases in each scenario; recall mean/SD/range describe the five replicate outcomes. Precision is scenario-pooled. Review rates use all scored rows, including non-injected rows.

| model | scenario | rows | positives | TP | FP | FN | TN | reviews | pooled_precision | mean_recall | recall_sd | recall_min | recall_max | pooled_f1 | review_rate | mean_auc | mean_ap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase2 | S1 | 100000 | 200 | 0 | 3 | 200 | 99797 | 3 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000030 | 0.618946 | 0.007738 |
| phase2 | S2 | 100000 | 500 | 0 | 2 | 500 | 99498 | 2 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000020 | 0.510225 | 0.005487 |
| phase2 | S3 | 100000 | 1000 | 0 | 14 | 1000 | 98986 | 14 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000140 | 0.488188 | 0.009956 |
| phase2 | S4 | 100000 | 2000 | 0 | 0 | 2000 | 98000 | 0 | N/A | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.497476 | 0.020790 |
| phase2 | S5 | 100000 | 500 | 0 | 5 | 500 | 99495 | 5 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000050 | 0.535099 | 0.006288 |
| phase2 | S6 | 100000 | 1000 | 0 | 18 | 1000 | 98982 | 18 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000180 | 0.534424 | 0.012813 |
| phase2 | S7 | 100000 | 200 | 0 | 34 | 200 | 99766 | 34 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000340 | 0.523690 | 0.003140 |
| phase2 | S8 | 100000 | 0 | 0 | 7 | 0 | 99993 | 7 | 0.000000 | N/A | N/A | N/A | N/A | 0.000000 | 0.000070 | N/A | N/A |
| phase6_v1 | S1 | 100000 | 200 | 2 | 319 | 198 | 99481 | 321 | 0.006231 | 0.010000 | 0.013693 | 0.000000 | 0.025000 | 0.007678 | 0.003210 | 0.581126 | 0.003963 |
| phase6_v1 | S2 | 100000 | 500 | 1 | 602 | 499 | 98898 | 603 | 0.001658 | 0.002000 | 0.004472 | 0.000000 | 0.010000 | 0.001813 | 0.006030 | 0.669943 | 0.007937 |
| phase6_v1 | S3 | 100000 | 1000 | 3 | 401 | 997 | 98599 | 404 | 0.007426 | 0.003000 | 0.002739 | 0.000000 | 0.005000 | 0.004274 | 0.004040 | 0.547399 | 0.012192 |
| phase6_v1 | S4 | 100000 | 2000 | 341 | 522 | 1659 | 97478 | 863 | 0.395133 | 0.170500 | 0.019478 | 0.155000 | 0.197500 | 0.238212 | 0.008630 | 0.979913 | 0.386850 |
| phase6_v1 | S5 | 100000 | 500 | 2 | 535 | 498 | 98965 | 537 | 0.003724 | 0.004000 | 0.005477 | 0.000000 | 0.010000 | 0.003857 | 0.005370 | 0.507778 | 0.005583 |
| phase6_v1 | S6 | 100000 | 1000 | 94 | 689 | 906 | 98311 | 783 | 0.120051 | 0.094000 | 0.017464 | 0.075000 | 0.110000 | 0.105440 | 0.007830 | 0.650398 | 0.041495 |
| phase6_v1 | S7 | 100000 | 200 | 19 | 915 | 181 | 98885 | 934 | 0.020343 | 0.095000 | 0.020917 | 0.075000 | 0.125000 | 0.033510 | 0.009340 | 0.647998 | 0.009197 |
| phase6_v1 | S8 | 100000 | 0 | 0 | 739 | 0 | 99261 | 739 | 0.000000 | N/A | N/A | N/A | N/A | 0.000000 | 0.007390 | N/A | N/A |

## Equal-budget scenario outcomes — separate comparison

Exactly 200 completed-day reviews per 20,000-row case, using score descending and transaction ID ascending. Daily Q is `N_d//100-N_previous_day//100`; no numeric cutoff. This is not a new fitted model or revised native threshold.

| model | scenario | rows | positives | TP | FP | FN | TN | reviews | pooled_precision | mean_recall | recall_sd | recall_min | recall_max | pooled_f1 | review_rate | mean_auc | mean_ap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase2 | S1 | 100000 | 200 | 9 | 991 | 191 | 98809 | 1000 | 0.009000 | 0.045000 | 0.032596 | 0.000000 | 0.075000 | 0.015000 | 0.010000 | 0.618946 | 0.007738 |
| phase2 | S2 | 100000 | 500 | 2 | 998 | 498 | 98502 | 1000 | 0.002000 | 0.004000 | 0.005477 | 0.000000 | 0.010000 | 0.002667 | 0.010000 | 0.510225 | 0.005487 |
| phase2 | S3 | 100000 | 1000 | 9 | 991 | 991 | 98009 | 1000 | 0.009000 | 0.009000 | 0.009618 | 0.000000 | 0.025000 | 0.009000 | 0.010000 | 0.488188 | 0.009956 |
| phase2 | S4 | 100000 | 2000 | 27 | 973 | 1973 | 97027 | 1000 | 0.027000 | 0.013500 | 0.002850 | 0.010000 | 0.017500 | 0.018000 | 0.010000 | 0.497476 | 0.020790 |
| phase2 | S5 | 100000 | 500 | 5 | 995 | 495 | 98505 | 1000 | 0.005000 | 0.010000 | 0.014142 | 0.000000 | 0.030000 | 0.006667 | 0.010000 | 0.535099 | 0.006288 |
| phase2 | S6 | 100000 | 1000 | 19 | 981 | 981 | 98019 | 1000 | 0.019000 | 0.019000 | 0.015572 | 0.005000 | 0.045000 | 0.019000 | 0.010000 | 0.534424 | 0.012813 |
| phase2 | S7 | 100000 | 200 | 7 | 993 | 193 | 98807 | 1000 | 0.007000 | 0.035000 | 0.022361 | 0.000000 | 0.050000 | 0.011667 | 0.010000 | 0.523690 | 0.003140 |
| phase2 | S8 | 100000 | 0 | 0 | 1000 | 0 | 99000 | 1000 | 0.000000 | N/A | N/A | N/A | N/A | 0.000000 | 0.010000 | N/A | N/A |
| phase6_v1 | S1 | 100000 | 200 | 7 | 993 | 193 | 98807 | 1000 | 0.007000 | 0.035000 | 0.041833 | 0.000000 | 0.100000 | 0.011667 | 0.010000 | 0.581126 | 0.003963 |
| phase6_v1 | S2 | 100000 | 500 | 5 | 995 | 495 | 98505 | 1000 | 0.005000 | 0.010000 | 0.014142 | 0.000000 | 0.030000 | 0.006667 | 0.010000 | 0.669943 | 0.007937 |
| phase6_v1 | S3 | 100000 | 1000 | 16 | 984 | 984 | 98016 | 1000 | 0.016000 | 0.016000 | 0.010840 | 0.000000 | 0.030000 | 0.016000 | 0.010000 | 0.547399 | 0.012192 |
| phase6_v1 | S4 | 100000 | 2000 | 351 | 649 | 1649 | 97351 | 1000 | 0.351000 | 0.175500 | 0.019316 | 0.157500 | 0.200000 | 0.234000 | 0.010000 | 0.979913 | 0.386850 |
| phase6_v1 | S5 | 100000 | 500 | 4 | 996 | 496 | 98504 | 1000 | 0.004000 | 0.008000 | 0.010954 | 0.000000 | 0.020000 | 0.005333 | 0.010000 | 0.507778 | 0.005583 |
| phase6_v1 | S6 | 100000 | 1000 | 105 | 895 | 895 | 98105 | 1000 | 0.105000 | 0.105000 | 0.018371 | 0.075000 | 0.120000 | 0.105000 | 0.010000 | 0.650398 | 0.041495 |
| phase6_v1 | S7 | 100000 | 200 | 19 | 981 | 181 | 98819 | 1000 | 0.019000 | 0.095000 | 0.020917 | 0.075000 | 0.125000 | 0.031667 | 0.010000 | 0.647998 | 0.009197 |
| phase6_v1 | S8 | 100000 | 0 | 0 | 1000 | 0 | 99000 | 1000 | 0.000000 | N/A | N/A | N/A | N/A | 0.000000 | 0.010000 | N/A | N/A |

## Hypothetical synthetic screen applied to native policy only

Each positive scenario requires mean recall >=20% and scenario-pooled precision >=10%. Every control case must review <=100/20,000, and every native case must review <=200/20,000. Zero-alert positive cases have recall zero; undefined pooled precision fails the precision requirement. S8 recall/AUC/AP are N/A, not zero or 0.5. These targets are hypothetical research assumptions, **not JPMorgan requirements, banking standards or evidence of production readiness**. Relative gains cannot rescue a failed screen.

| model | scenario | mean_recall | pooled_precision | recall_pass | precision_pass | control_pass | capacity_pass | max_reviews | passed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase2 | S1 | 0.000000 | 0.000000 | False | False | N/A | True | 2 | False |
| phase2 | S2 | 0.000000 | 0.000000 | False | False | N/A | True | 1 | False |
| phase2 | S3 | 0.000000 | 0.000000 | False | False | N/A | True | 4 | False |
| phase2 | S4 | 0.000000 | N/A | False | False | N/A | True | 0 | False |
| phase2 | S5 | 0.000000 | 0.000000 | False | False | N/A | True | 2 | False |
| phase2 | S6 | 0.000000 | 0.000000 | False | False | N/A | True | 7 | False |
| phase2 | S7 | 0.000000 | 0.000000 | False | False | N/A | True | 12 | False |
| phase2 | S8 | N/A | N/A | N/A | N/A | True | True | 3 | True |
| phase6_v1 | S1 | 0.010000 | 0.006231 | False | False | N/A | True | 68 | False |
| phase6_v1 | S2 | 0.002000 | 0.001658 | False | False | N/A | True | 131 | False |
| phase6_v1 | S3 | 0.003000 | 0.007426 | False | False | N/A | True | 85 | False |
| phase6_v1 | S4 | 0.170500 | 0.395133 | False | True | N/A | True | 176 | False |
| phase6_v1 | S5 | 0.004000 | 0.003724 | False | False | N/A | True | 118 | False |
| phase6_v1 | S6 | 0.094000 | 0.120051 | False | True | N/A | True | 169 | False |
| phase6_v1 | S7 | 0.095000 | 0.020343 | False | False | N/A | True | 191 | False |
| phase6_v1 | S8 | N/A | N/A | N/A | N/A | False | True | 159 | False |

| model | passes_all | hypothetical_only |
| --- | --- | --- |
| phase2 | False | True |
| phase6_v1 | False | True |

## Paired differences and uncertainty

Differences are Phase 6 minus Phase 2 on identical cases. Primary overall means give each of seven positive scenario settings equal weight. S8 is always reported separately because recall is undefined. Ten thousand bootstrap samples resample whole paired cases within each fixed scenario; the same resample indices preserve both models and both policies. Seed 730289901. Five replicates per setting yield coarse, conditional descriptive intervals, not independent-transaction or real-world guarantees. Intervals are not multiple-testing-adjusted.

| policy | mean_delta | lower_95 | upper_95 | draws | unit | seed |
| --- | --- | --- | --- | --- | --- | --- |
| native | 0.054071 | 0.050000 | 0.058214 | 10000 | whole paired case, stratified by fixed scenario | 730289901 |
| equal_budget | 0.044143 | 0.038427 | 0.050071 | 10000 | whole paired case, stratified by fixed scenario | 730289901 |

| policy | scenario | mean_delta | std_delta | min_delta | max_delta | lower_95 | upper_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| native | S1 | 0.010000 | 0.013693 | 0.000000 | 0.025000 | 0.000000 | 0.020000 |
| native | S2 | 0.002000 | 0.004472 | 0.000000 | 0.010000 | 0.000000 | 0.006000 |
| native | S3 | 0.003000 | 0.002739 | 0.000000 | 0.005000 | 0.001000 | 0.005000 |
| native | S4 | 0.170500 | 0.019478 | 0.155000 | 0.197500 | 0.156500 | 0.187000 |
| native | S5 | 0.004000 | 0.005477 | 0.000000 | 0.010000 | 0.000000 | 0.008000 |
| native | S6 | 0.094000 | 0.017464 | 0.075000 | 0.110000 | 0.081000 | 0.107000 |
| native | S7 | 0.095000 | 0.020917 | 0.075000 | 0.125000 | 0.080000 | 0.110000 |
| equal_budget | S1 | -0.010000 | 0.022361 | -0.025000 | 0.025000 | -0.025000 | 0.010000 |
| equal_budget | S2 | 0.006000 | 0.013416 | -0.010000 | 0.020000 | -0.004000 | 0.016000 |
| equal_budget | S3 | 0.007000 | 0.016432 | -0.010000 | 0.025000 | -0.006000 | 0.020000 |
| equal_budget | S4 | 0.162000 | 0.018658 | 0.142500 | 0.187500 | 0.148000 | 0.177500 |
| equal_budget | S5 | -0.002000 | 0.004472 | -0.010000 | 0.000000 | -0.006000 | 0.000000 |
| equal_budget | S6 | 0.086000 | 0.022749 | 0.055000 | 0.110000 | 0.067000 | 0.103000 |
| equal_budget | S7 | 0.060000 | 0.028504 | 0.025000 | 0.100000 | 0.040000 | 0.080125 |

## All 160 model/case/policy outcomes

No case is omitted. N/A is an undefined value; defined flags and all extra fields are preserved in all_case_metrics.csv. There are 40 underlying datasets, not 160 independent datasets.

| scenario | seed | model | policy | positives | TP | FP | FN | TN | precision | recall | f1 | alerts | review_rate | roc_auc | average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | 730280001 | phase2 | native | 40 | 0 | 0 | 40 | 19960 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.705192 | 0.012642 |
| S1 | 730280001 | phase2 | equal_budget | 40 | 3 | 197 | 37 | 19763 | 0.015000 | 0.075000 | 0.025000 | 200 | 0.010000 | 0.705192 | 0.012642 |
| S1 | 730280001 | phase6_v1 | native | 40 | 1 | 60 | 39 | 19900 | 0.016393 | 0.025000 | 0.019802 | 61 | 0.003050 | 0.611311 | 0.006029 |
| S1 | 730280001 | phase6_v1 | equal_budget | 40 | 4 | 196 | 36 | 19764 | 0.020000 | 0.100000 | 0.033333 | 200 | 0.010000 | 0.611311 | 0.006029 |
| S1 | 730280002 | phase2 | native | 40 | 0 | 0 | 40 | 19960 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.623072 | 0.002877 |
| S1 | 730280002 | phase2 | equal_budget | 40 | 0 | 200 | 40 | 19760 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.623072 | 0.002877 |
| S1 | 730280002 | phase6_v1 | native | 40 | 0 | 68 | 40 | 19892 | 0.000000 | 0.000000 | 0.000000 | 68 | 0.003400 | 0.592991 | 0.002653 |
| S1 | 730280002 | phase6_v1 | equal_budget | 40 | 0 | 200 | 40 | 19760 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.592991 | 0.002653 |
| S1 | 730280003 | phase2 | native | 40 | 0 | 0 | 40 | 19960 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.555904 | 0.003780 |
| S1 | 730280003 | phase2 | equal_budget | 40 | 1 | 199 | 39 | 19761 | 0.005000 | 0.025000 | 0.008333 | 200 | 0.010000 | 0.555904 | 0.003780 |
| S1 | 730280003 | phase6_v1 | native | 40 | 0 | 67 | 40 | 19893 | 0.000000 | 0.000000 | 0.000000 | 67 | 0.003350 | 0.513091 | 0.002525 |
| S1 | 730280003 | phase6_v1 | equal_budget | 40 | 0 | 200 | 40 | 19760 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.513091 | 0.002525 |
| S1 | 730280004 | phase2 | native | 40 | 0 | 1 | 40 | 19959 | 0.000000 | 0.000000 | 0.000000 | 1 | 0.000050 | 0.598965 | 0.011682 |
| S1 | 730280004 | phase2 | equal_budget | 40 | 3 | 197 | 37 | 19763 | 0.015000 | 0.075000 | 0.025000 | 200 | 0.010000 | 0.598965 | 0.011682 |
| S1 | 730280004 | phase6_v1 | native | 40 | 1 | 61 | 39 | 19899 | 0.016129 | 0.025000 | 0.019608 | 62 | 0.003100 | 0.605245 | 0.004335 |
| S1 | 730280004 | phase6_v1 | equal_budget | 40 | 2 | 198 | 38 | 19762 | 0.010000 | 0.050000 | 0.016667 | 200 | 0.010000 | 0.605245 | 0.004335 |
| S1 | 730280005 | phase2 | native | 40 | 0 | 2 | 40 | 19958 | 0.000000 | 0.000000 | 0.000000 | 2 | 0.000100 | 0.611596 | 0.007707 |
| S1 | 730280005 | phase2 | equal_budget | 40 | 2 | 198 | 38 | 19762 | 0.010000 | 0.050000 | 0.016667 | 200 | 0.010000 | 0.611596 | 0.007707 |
| S1 | 730280005 | phase6_v1 | native | 40 | 0 | 63 | 40 | 19897 | 0.000000 | 0.000000 | 0.000000 | 63 | 0.003150 | 0.582991 | 0.004272 |
| S1 | 730280005 | phase6_v1 | equal_budget | 40 | 1 | 199 | 39 | 19761 | 0.005000 | 0.025000 | 0.008333 | 200 | 0.010000 | 0.582991 | 0.004272 |
| S2 | 730280006 | phase2 | native | 100 | 0 | 0 | 100 | 19900 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.434426 | 0.004120 |
| S2 | 730280006 | phase2 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.434426 | 0.004120 |
| S2 | 730280006 | phase6_v1 | native | 100 | 0 | 118 | 100 | 19782 | 0.000000 | 0.000000 | 0.000000 | 118 | 0.005900 | 0.688816 | 0.008305 |
| S2 | 730280006 | phase6_v1 | equal_budget | 100 | 2 | 198 | 98 | 19702 | 0.010000 | 0.020000 | 0.013333 | 200 | 0.010000 | 0.688816 | 0.008305 |
| S2 | 730280007 | phase2 | native | 100 | 0 | 1 | 100 | 19899 | 0.000000 | 0.000000 | 0.000000 | 1 | 0.000050 | 0.495628 | 0.004525 |
| S2 | 730280007 | phase2 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.495628 | 0.004525 |
| S2 | 730280007 | phase6_v1 | native | 100 | 0 | 129 | 100 | 19771 | 0.000000 | 0.000000 | 0.000000 | 129 | 0.006450 | 0.668115 | 0.007397 |
| S2 | 730280007 | phase6_v1 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.668115 | 0.007397 |
| S2 | 730280008 | phase2 | native | 100 | 0 | 0 | 100 | 19900 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.530341 | 0.005367 |
| S2 | 730280008 | phase2 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.530341 | 0.005367 |
| S2 | 730280008 | phase6_v1 | native | 100 | 0 | 102 | 100 | 19798 | 0.000000 | 0.000000 | 0.000000 | 102 | 0.005100 | 0.663978 | 0.008761 |
| S2 | 730280008 | phase6_v1 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.663978 | 0.008761 |
| S2 | 730280009 | phase2 | native | 100 | 0 | 0 | 100 | 19900 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.548062 | 0.006822 |
| S2 | 730280009 | phase2 | equal_budget | 100 | 1 | 199 | 99 | 19701 | 0.005000 | 0.010000 | 0.006667 | 200 | 0.010000 | 0.548062 | 0.006822 |
| S2 | 730280009 | phase6_v1 | native | 100 | 0 | 131 | 100 | 19769 | 0.000000 | 0.000000 | 0.000000 | 131 | 0.006550 | 0.631221 | 0.006901 |
| S2 | 730280009 | phase6_v1 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.631221 | 0.006901 |
| S2 | 730280010 | phase2 | native | 100 | 0 | 1 | 100 | 19899 | 0.000000 | 0.000000 | 0.000000 | 1 | 0.000050 | 0.542667 | 0.006601 |
| S2 | 730280010 | phase2 | equal_budget | 100 | 1 | 199 | 99 | 19701 | 0.005000 | 0.010000 | 0.006667 | 200 | 0.010000 | 0.542667 | 0.006601 |
| S2 | 730280010 | phase6_v1 | native | 100 | 1 | 122 | 99 | 19778 | 0.008130 | 0.010000 | 0.008969 | 123 | 0.006150 | 0.697584 | 0.008322 |
| S2 | 730280010 | phase6_v1 | equal_budget | 100 | 3 | 197 | 97 | 19703 | 0.015000 | 0.030000 | 0.020000 | 200 | 0.010000 | 0.697584 | 0.008322 |
| S3 | 730280011 | phase2 | native | 200 | 0 | 3 | 200 | 19797 | 0.000000 | 0.000000 | 0.000000 | 3 | 0.000150 | 0.500444 | 0.010084 |
| S3 | 730280011 | phase2 | equal_budget | 200 | 1 | 199 | 199 | 19601 | 0.005000 | 0.005000 | 0.005000 | 200 | 0.010000 | 0.500444 | 0.010084 |
| S3 | 730280011 | phase6_v1 | native | 200 | 1 | 74 | 199 | 19726 | 0.013333 | 0.005000 | 0.007273 | 75 | 0.003750 | 0.556288 | 0.014076 |
| S3 | 730280011 | phase6_v1 | equal_budget | 200 | 6 | 194 | 194 | 19606 | 0.030000 | 0.030000 | 0.030000 | 200 | 0.010000 | 0.556288 | 0.014076 |
| S3 | 730280012 | phase2 | native | 200 | 0 | 3 | 200 | 19797 | 0.000000 | 0.000000 | 0.000000 | 3 | 0.000150 | 0.491320 | 0.009913 |
| S3 | 730280012 | phase2 | equal_budget | 200 | 2 | 198 | 198 | 19602 | 0.010000 | 0.010000 | 0.010000 | 200 | 0.010000 | 0.491320 | 0.009913 |
| S3 | 730280012 | phase6_v1 | native | 200 | 0 | 80 | 200 | 19720 | 0.000000 | 0.000000 | 0.000000 | 80 | 0.004000 | 0.544756 | 0.011502 |
| S3 | 730280012 | phase6_v1 | equal_budget | 200 | 0 | 200 | 200 | 19600 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.544756 | 0.011502 |
| S3 | 730280013 | phase2 | native | 200 | 0 | 4 | 200 | 19796 | 0.000000 | 0.000000 | 0.000000 | 4 | 0.000200 | 0.455681 | 0.008884 |
| S3 | 730280013 | phase2 | equal_budget | 200 | 1 | 199 | 199 | 19601 | 0.005000 | 0.005000 | 0.005000 | 200 | 0.010000 | 0.455681 | 0.008884 |
| S3 | 730280013 | phase6_v1 | native | 200 | 1 | 84 | 199 | 19716 | 0.011765 | 0.005000 | 0.007018 | 85 | 0.004250 | 0.525718 | 0.011332 |
| S3 | 730280013 | phase6_v1 | equal_budget | 200 | 3 | 197 | 197 | 19603 | 0.015000 | 0.015000 | 0.015000 | 200 | 0.010000 | 0.525718 | 0.011332 |
| S3 | 730280014 | phase2 | native | 200 | 0 | 2 | 200 | 19798 | 0.000000 | 0.000000 | 0.000000 | 2 | 0.000100 | 0.524611 | 0.011871 |
| S3 | 730280014 | phase2 | equal_budget | 200 | 5 | 195 | 195 | 19605 | 0.025000 | 0.025000 | 0.025000 | 200 | 0.010000 | 0.524611 | 0.011871 |
| S3 | 730280014 | phase6_v1 | native | 200 | 1 | 78 | 199 | 19722 | 0.012658 | 0.005000 | 0.007168 | 79 | 0.003950 | 0.574449 | 0.012971 |
| S3 | 730280014 | phase6_v1 | equal_budget | 200 | 3 | 197 | 197 | 19603 | 0.015000 | 0.015000 | 0.015000 | 200 | 0.010000 | 0.574449 | 0.012971 |
| S3 | 730280015 | phase2 | native | 200 | 0 | 2 | 200 | 19798 | 0.000000 | 0.000000 | 0.000000 | 2 | 0.000100 | 0.468882 | 0.009029 |
| S3 | 730280015 | phase2 | equal_budget | 200 | 0 | 200 | 200 | 19600 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.468882 | 0.009029 |
| S3 | 730280015 | phase6_v1 | native | 200 | 0 | 85 | 200 | 19715 | 0.000000 | 0.000000 | 0.000000 | 85 | 0.004250 | 0.535784 | 0.011080 |
| S3 | 730280015 | phase6_v1 | equal_budget | 200 | 4 | 196 | 196 | 19604 | 0.020000 | 0.020000 | 0.020000 | 200 | 0.010000 | 0.535784 | 0.011080 |
| S4 | 730280016 | phase2 | native | 400 | 0 | 0 | 400 | 19600 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.494280 | 0.019848 |
| S4 | 730280016 | phase2 | equal_budget | 400 | 5 | 195 | 395 | 19405 | 0.025000 | 0.012500 | 0.016667 | 200 | 0.010000 | 0.494280 | 0.019848 |
| S4 | 730280016 | phase6_v1 | native | 400 | 79 | 97 | 321 | 19503 | 0.448864 | 0.197500 | 0.274306 | 176 | 0.008800 | 0.982133 | 0.411763 |
| S4 | 730280016 | phase6_v1 | equal_budget | 400 | 80 | 120 | 320 | 19480 | 0.400000 | 0.200000 | 0.266667 | 200 | 0.010000 | 0.982133 | 0.411763 |
| S4 | 730280017 | phase2 | native | 400 | 0 | 0 | 400 | 19600 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.491517 | 0.022856 |
| S4 | 730280017 | phase2 | equal_budget | 400 | 7 | 193 | 393 | 19407 | 0.035000 | 0.017500 | 0.023333 | 200 | 0.010000 | 0.491517 | 0.022856 |
| S4 | 730280017 | phase6_v1 | native | 400 | 74 | 99 | 326 | 19501 | 0.427746 | 0.185000 | 0.258290 | 173 | 0.008650 | 0.978456 | 0.373745 |
| S4 | 730280017 | phase6_v1 | equal_budget | 400 | 77 | 123 | 323 | 19477 | 0.385000 | 0.192500 | 0.256667 | 200 | 0.010000 | 0.978456 | 0.373745 |
| S4 | 730280018 | phase2 | native | 400 | 0 | 0 | 400 | 19600 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.494311 | 0.020144 |
| S4 | 730280018 | phase2 | equal_budget | 400 | 5 | 195 | 395 | 19405 | 0.025000 | 0.012500 | 0.016667 | 200 | 0.010000 | 0.494311 | 0.020144 |
| S4 | 730280018 | phase6_v1 | native | 400 | 63 | 107 | 337 | 19493 | 0.370588 | 0.157500 | 0.221053 | 170 | 0.008500 | 0.978768 | 0.376937 |
| S4 | 730280018 | phase6_v1 | equal_budget | 400 | 65 | 135 | 335 | 19465 | 0.325000 | 0.162500 | 0.216667 | 200 | 0.010000 | 0.978768 | 0.376937 |
| S4 | 730280019 | phase2 | native | 400 | 0 | 0 | 400 | 19600 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.488112 | 0.019257 |
| S4 | 730280019 | phase2 | equal_budget | 400 | 4 | 196 | 396 | 19404 | 0.020000 | 0.010000 | 0.013333 | 200 | 0.010000 | 0.488112 | 0.019257 |
| S4 | 730280019 | phase6_v1 | native | 400 | 62 | 108 | 338 | 19492 | 0.364706 | 0.155000 | 0.217544 | 170 | 0.008500 | 0.980000 | 0.384428 |
| S4 | 730280019 | phase6_v1 | equal_budget | 400 | 66 | 134 | 334 | 19466 | 0.330000 | 0.165000 | 0.220000 | 200 | 0.010000 | 0.980000 | 0.384428 |
| S4 | 730280020 | phase2 | native | 400 | 0 | 0 | 400 | 19600 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.519161 | 0.021846 |
| S4 | 730280020 | phase2 | equal_budget | 400 | 6 | 194 | 394 | 19406 | 0.030000 | 0.015000 | 0.020000 | 200 | 0.010000 | 0.519161 | 0.021846 |
| S4 | 730280020 | phase6_v1 | native | 400 | 63 | 111 | 337 | 19489 | 0.362069 | 0.157500 | 0.219512 | 174 | 0.008700 | 0.980210 | 0.387375 |
| S4 | 730280020 | phase6_v1 | equal_budget | 400 | 63 | 137 | 337 | 19463 | 0.315000 | 0.157500 | 0.210000 | 200 | 0.010000 | 0.980210 | 0.387375 |
| S5 | 730280021 | phase2 | native | 100 | 0 | 1 | 100 | 19899 | 0.000000 | 0.000000 | 0.000000 | 1 | 0.000050 | 0.524428 | 0.006212 |
| S5 | 730280021 | phase2 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.524428 | 0.006212 |
| S5 | 730280021 | phase6_v1 | native | 100 | 0 | 104 | 100 | 19796 | 0.000000 | 0.000000 | 0.000000 | 104 | 0.005200 | 0.510350 | 0.005505 |
| S5 | 730280021 | phase6_v1 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.510350 | 0.005505 |
| S5 | 730280022 | phase2 | native | 100 | 0 | 1 | 100 | 19899 | 0.000000 | 0.000000 | 0.000000 | 1 | 0.000050 | 0.589187 | 0.006879 |
| S5 | 730280022 | phase2 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.589187 | 0.006879 |
| S5 | 730280022 | phase6_v1 | native | 100 | 0 | 109 | 100 | 19791 | 0.000000 | 0.000000 | 0.000000 | 109 | 0.005450 | 0.472073 | 0.004580 |
| S5 | 730280022 | phase6_v1 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.472073 | 0.004580 |
| S5 | 730280023 | phase2 | native | 100 | 0 | 2 | 100 | 19898 | 0.000000 | 0.000000 | 0.000000 | 2 | 0.000100 | 0.516099 | 0.006402 |
| S5 | 730280023 | phase2 | equal_budget | 100 | 3 | 197 | 97 | 19703 | 0.015000 | 0.030000 | 0.020000 | 200 | 0.010000 | 0.516099 | 0.006402 |
| S5 | 730280023 | phase6_v1 | native | 100 | 1 | 117 | 99 | 19783 | 0.008475 | 0.010000 | 0.009174 | 118 | 0.005900 | 0.538766 | 0.006230 |
| S5 | 730280023 | phase6_v1 | equal_budget | 100 | 2 | 198 | 98 | 19702 | 0.010000 | 0.020000 | 0.013333 | 200 | 0.010000 | 0.538766 | 0.006230 |
| S5 | 730280024 | phase2 | native | 100 | 0 | 1 | 100 | 19899 | 0.000000 | 0.000000 | 0.000000 | 1 | 0.000050 | 0.538971 | 0.007014 |
| S5 | 730280024 | phase2 | equal_budget | 100 | 2 | 198 | 98 | 19702 | 0.010000 | 0.020000 | 0.013333 | 200 | 0.010000 | 0.538971 | 0.007014 |
| S5 | 730280024 | phase6_v1 | native | 100 | 1 | 102 | 99 | 19798 | 0.009709 | 0.010000 | 0.009852 | 103 | 0.005150 | 0.536953 | 0.006929 |
| S5 | 730280024 | phase6_v1 | equal_budget | 100 | 2 | 198 | 98 | 19702 | 0.010000 | 0.020000 | 0.013333 | 200 | 0.010000 | 0.536953 | 0.006929 |
| S5 | 730280025 | phase2 | native | 100 | 0 | 0 | 100 | 19900 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.506810 | 0.004935 |
| S5 | 730280025 | phase2 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.506810 | 0.004935 |
| S5 | 730280025 | phase6_v1 | native | 100 | 0 | 103 | 100 | 19797 | 0.000000 | 0.000000 | 0.000000 | 103 | 0.005150 | 0.480748 | 0.004673 |
| S5 | 730280025 | phase6_v1 | equal_budget | 100 | 0 | 200 | 100 | 19700 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.480748 | 0.004673 |
| S6 | 730280026 | phase2 | native | 200 | 0 | 3 | 200 | 19797 | 0.000000 | 0.000000 | 0.000000 | 3 | 0.000150 | 0.549752 | 0.014246 |
| S6 | 730280026 | phase2 | equal_budget | 200 | 3 | 197 | 197 | 19603 | 0.015000 | 0.015000 | 0.015000 | 200 | 0.010000 | 0.549752 | 0.014246 |
| S6 | 730280026 | phase6_v1 | native | 200 | 22 | 137 | 178 | 19663 | 0.138365 | 0.110000 | 0.122563 | 159 | 0.007950 | 0.631451 | 0.039523 |
| S6 | 730280026 | phase6_v1 | equal_budget | 200 | 23 | 177 | 177 | 19623 | 0.115000 | 0.115000 | 0.115000 | 200 | 0.010000 | 0.631451 | 0.039523 |
| S6 | 730280027 | phase2 | native | 200 | 0 | 3 | 200 | 19797 | 0.000000 | 0.000000 | 0.000000 | 3 | 0.000150 | 0.558976 | 0.016021 |
| S6 | 730280027 | phase2 | equal_budget | 200 | 9 | 191 | 191 | 19609 | 0.045000 | 0.045000 | 0.045000 | 200 | 0.010000 | 0.558976 | 0.016021 |
| S6 | 730280027 | phase6_v1 | native | 200 | 15 | 133 | 185 | 19667 | 0.101351 | 0.075000 | 0.086207 | 148 | 0.007400 | 0.637046 | 0.040213 |
| S6 | 730280027 | phase6_v1 | equal_budget | 200 | 20 | 180 | 180 | 19620 | 0.100000 | 0.100000 | 0.100000 | 200 | 0.010000 | 0.637046 | 0.040213 |
| S6 | 730280028 | phase2 | native | 200 | 0 | 5 | 200 | 19795 | 0.000000 | 0.000000 | 0.000000 | 5 | 0.000250 | 0.506266 | 0.011107 |
| S6 | 730280028 | phase2 | equal_budget | 200 | 2 | 198 | 198 | 19602 | 0.010000 | 0.010000 | 0.010000 | 200 | 0.010000 | 0.506266 | 0.011107 |
| S6 | 730280028 | phase6_v1 | native | 200 | 21 | 148 | 179 | 19652 | 0.124260 | 0.105000 | 0.113821 | 169 | 0.008450 | 0.641120 | 0.041790 |
| S6 | 730280028 | phase6_v1 | equal_budget | 200 | 24 | 176 | 176 | 19624 | 0.120000 | 0.120000 | 0.120000 | 200 | 0.010000 | 0.641120 | 0.041790 |
| S6 | 730280029 | phase2 | native | 200 | 0 | 0 | 200 | 19800 | N/A | 0.000000 | 0.000000 | 0 | 0.000000 | 0.534744 | 0.011737 |
| S6 | 730280029 | phase2 | equal_budget | 200 | 1 | 199 | 199 | 19601 | 0.005000 | 0.005000 | 0.005000 | 200 | 0.010000 | 0.534744 | 0.011737 |
| S6 | 730280029 | phase6_v1 | native | 200 | 15 | 135 | 185 | 19665 | 0.100000 | 0.075000 | 0.085714 | 150 | 0.007500 | 0.689893 | 0.041288 |
| S6 | 730280029 | phase6_v1 | equal_budget | 200 | 15 | 185 | 185 | 19615 | 0.075000 | 0.075000 | 0.075000 | 200 | 0.010000 | 0.689893 | 0.041288 |
| S6 | 730280030 | phase2 | native | 200 | 0 | 7 | 200 | 19793 | 0.000000 | 0.000000 | 0.000000 | 7 | 0.000350 | 0.522382 | 0.010952 |
| S6 | 730280030 | phase2 | equal_budget | 200 | 4 | 196 | 196 | 19604 | 0.020000 | 0.020000 | 0.020000 | 200 | 0.010000 | 0.522382 | 0.010952 |
| S6 | 730280030 | phase6_v1 | native | 200 | 21 | 136 | 179 | 19664 | 0.133758 | 0.105000 | 0.117647 | 157 | 0.007850 | 0.652480 | 0.044662 |
| S6 | 730280030 | phase6_v1 | equal_budget | 200 | 23 | 177 | 177 | 19623 | 0.115000 | 0.115000 | 0.115000 | 200 | 0.010000 | 0.652480 | 0.044662 |
| S7 | 730280031 | phase2 | native | 40 | 0 | 2 | 40 | 19958 | 0.000000 | 0.000000 | 0.000000 | 2 | 0.000100 | 0.540896 | 0.003960 |
| S7 | 730280031 | phase2 | equal_budget | 40 | 2 | 198 | 38 | 19762 | 0.010000 | 0.050000 | 0.016667 | 200 | 0.010000 | 0.540896 | 0.003960 |
| S7 | 730280031 | phase6_v1 | native | 40 | 3 | 185 | 37 | 19775 | 0.015957 | 0.075000 | 0.026316 | 188 | 0.009400 | 0.628879 | 0.010222 |
| S7 | 730280031 | phase6_v1 | equal_budget | 40 | 3 | 197 | 37 | 19763 | 0.015000 | 0.075000 | 0.025000 | 200 | 0.010000 | 0.628879 | 0.010222 |
| S7 | 730280032 | phase2 | native | 40 | 0 | 12 | 40 | 19948 | 0.000000 | 0.000000 | 0.000000 | 12 | 0.000600 | 0.488024 | 0.001913 |
| S7 | 730280032 | phase2 | equal_budget | 40 | 0 | 200 | 40 | 19760 | 0.000000 | 0.000000 | 0.000000 | 200 | 0.010000 | 0.488024 | 0.001913 |
| S7 | 730280032 | phase6_v1 | native | 40 | 4 | 182 | 36 | 19778 | 0.021505 | 0.100000 | 0.035398 | 186 | 0.009300 | 0.627036 | 0.006165 |
| S7 | 730280032 | phase6_v1 | equal_budget | 40 | 4 | 196 | 36 | 19764 | 0.020000 | 0.100000 | 0.033333 | 200 | 0.010000 | 0.627036 | 0.006165 |
| S7 | 730280033 | phase2 | native | 40 | 0 | 5 | 40 | 19955 | 0.000000 | 0.000000 | 0.000000 | 5 | 0.000250 | 0.524423 | 0.003498 |
| S7 | 730280033 | phase2 | equal_budget | 40 | 2 | 198 | 38 | 19762 | 0.010000 | 0.050000 | 0.016667 | 200 | 0.010000 | 0.524423 | 0.003498 |
| S7 | 730280033 | phase6_v1 | native | 40 | 4 | 178 | 36 | 19782 | 0.021978 | 0.100000 | 0.036036 | 182 | 0.009100 | 0.584183 | 0.009127 |
| S7 | 730280033 | phase6_v1 | equal_budget | 40 | 4 | 196 | 36 | 19764 | 0.020000 | 0.100000 | 0.033333 | 200 | 0.010000 | 0.584183 | 0.009127 |
| S7 | 730280034 | phase2 | native | 40 | 0 | 9 | 40 | 19951 | 0.000000 | 0.000000 | 0.000000 | 9 | 0.000450 | 0.542685 | 0.003278 |
| S7 | 730280034 | phase2 | equal_budget | 40 | 1 | 199 | 39 | 19761 | 0.005000 | 0.025000 | 0.008333 | 200 | 0.010000 | 0.542685 | 0.003278 |
| S7 | 730280034 | phase6_v1 | native | 40 | 3 | 184 | 37 | 19776 | 0.016043 | 0.075000 | 0.026432 | 187 | 0.009350 | 0.731462 | 0.009903 |
| S7 | 730280034 | phase6_v1 | equal_budget | 40 | 3 | 197 | 37 | 19763 | 0.015000 | 0.075000 | 0.025000 | 200 | 0.010000 | 0.731462 | 0.009903 |
| S7 | 730280035 | phase2 | native | 40 | 0 | 6 | 40 | 19954 | 0.000000 | 0.000000 | 0.000000 | 6 | 0.000300 | 0.522421 | 0.003053 |
| S7 | 730280035 | phase2 | equal_budget | 40 | 2 | 198 | 38 | 19762 | 0.010000 | 0.050000 | 0.016667 | 200 | 0.010000 | 0.522421 | 0.003053 |
| S7 | 730280035 | phase6_v1 | native | 40 | 5 | 186 | 35 | 19774 | 0.026178 | 0.125000 | 0.043290 | 191 | 0.009550 | 0.668432 | 0.010567 |
| S7 | 730280035 | phase6_v1 | equal_budget | 40 | 5 | 195 | 35 | 19765 | 0.025000 | 0.125000 | 0.041667 | 200 | 0.010000 | 0.668432 | 0.010567 |
| S8 | 730280036 | phase2 | native | 0 | 0 | 1 | 0 | 19999 | 0.000000 | N/A | 0.000000 | 1 | 0.000050 | N/A | N/A |
| S8 | 730280036 | phase2 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |
| S8 | 730280036 | phase6_v1 | native | 0 | 0 | 159 | 0 | 19841 | 0.000000 | N/A | 0.000000 | 159 | 0.007950 | N/A | N/A |
| S8 | 730280036 | phase6_v1 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |
| S8 | 730280037 | phase2 | native | 0 | 0 | 1 | 0 | 19999 | 0.000000 | N/A | 0.000000 | 1 | 0.000050 | N/A | N/A |
| S8 | 730280037 | phase2 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |
| S8 | 730280037 | phase6_v1 | native | 0 | 0 | 150 | 0 | 19850 | 0.000000 | N/A | 0.000000 | 150 | 0.007500 | N/A | N/A |
| S8 | 730280037 | phase6_v1 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |
| S8 | 730280038 | phase2 | native | 0 | 0 | 3 | 0 | 19997 | 0.000000 | N/A | 0.000000 | 3 | 0.000150 | N/A | N/A |
| S8 | 730280038 | phase2 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |
| S8 | 730280038 | phase6_v1 | native | 0 | 0 | 141 | 0 | 19859 | 0.000000 | N/A | 0.000000 | 141 | 0.007050 | N/A | N/A |
| S8 | 730280038 | phase6_v1 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |
| S8 | 730280039 | phase2 | native | 0 | 0 | 0 | 0 | 20000 | N/A | N/A | N/A | 0 | 0.000000 | N/A | N/A |
| S8 | 730280039 | phase2 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |
| S8 | 730280039 | phase6_v1 | native | 0 | 0 | 149 | 0 | 19851 | 0.000000 | N/A | 0.000000 | 149 | 0.007450 | N/A | N/A |
| S8 | 730280039 | phase6_v1 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |
| S8 | 730280040 | phase2 | native | 0 | 0 | 2 | 0 | 19998 | 0.000000 | N/A | 0.000000 | 2 | 0.000100 | N/A | N/A |
| S8 | 730280040 | phase2 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |
| S8 | 730280040 | phase6_v1 | native | 0 | 0 | 140 | 0 | 19860 | 0.000000 | N/A | 0.000000 | 140 | 0.007000 | N/A | N/A |
| S8 | 730280040 | phase6_v1 | equal_budget | 0 | 0 | 200 | 0 | 19800 | 0.000000 | N/A | 0.000000 | 200 | 0.010000 | N/A | N/A |

## Per-type outcomes and event failures

| model | policy | injection_type | positives | TP | recall |
| --- | --- | --- | --- | --- | --- |
| phase2 | equal_budget | burst | 740 | 5 | 0.006757 |
| phase2 | equal_budget | contextual_amount | 440 | 24 | 0.054545 |
| phase2 | equal_budget | inactivity_return | 2240 | 31 | 0.013839 |
| phase2 | equal_budget | merchant_change | 1240 | 11 | 0.008871 |
| phase2 | equal_budget | spending_ramp | 740 | 7 | 0.009459 |
| phase2 | native | burst | 740 | 0 | 0.000000 |
| phase2 | native | contextual_amount | 440 | 0 | 0.000000 |
| phase2 | native | inactivity_return | 2240 | 0 | 0.000000 |
| phase2 | native | merchant_change | 1240 | 0 | 0.000000 |
| phase2 | native | spending_ramp | 740 | 0 | 0.000000 |
| phase6_v1 | equal_budget | burst | 740 | 6 | 0.008108 |
| phase6_v1 | equal_budget | contextual_amount | 440 | 10 | 0.022727 |
| phase6_v1 | equal_budget | inactivity_return | 2240 | 469 | 0.209375 |
| phase6_v1 | equal_budget | merchant_change | 1240 | 17 | 0.013710 |
| phase6_v1 | equal_budget | spending_ramp | 740 | 5 | 0.006757 |
| phase6_v1 | native | burst | 740 | 1 | 0.001351 |
| phase6_v1 | native | contextual_amount | 440 | 4 | 0.009091 |
| phase6_v1 | native | inactivity_return | 2240 | 452 | 0.201786 |
| phase6_v1 | native | merchant_change | 1240 | 3 | 0.002419 |
| phase6_v1 | native | spending_ramp | 740 | 2 | 0.002703 |

All per-case/type cells, including absent types and zero detections, are in all_type_metrics.csv. All events, undetected events, any/all-member detections and delay to day-close review are in all_event_metrics.csv. These complement rather than redefine row recall. Retrospective P@100/P@200, recall@200, within-model score distributions and ties are also saved. No threshold sweep or alternate cutoff was run.

## Limitations and negative findings

This is a fresh synthetic test independent of model selection, but not an externally blind real-bank study. Scenario authors knew both frozen models and prior failures. Prespecified ordinary tails, payment clusters, preference shifts and hiatuses overlap interventions; labels may be observationally ambiguous. The hiatus-rich S4 setting and guaranteed warmup coverage are explicit stress assumptions, not empirical customer behavior. Synthetic labels do not establish malice or legitimacy.

Phase 6 uses timestamp-level behavioral information and 120,000 fitting rows, while Phase 2 uses earlier-day amount features and 463 fitting rows. Both use their original preprocessing, memory, thresholds and native policies. A relative gain cannot isolate an algorithm effect, and native recall must be read alongside differing review costs. Warmup updates history only, never model parameters. Equal-budget results evaluate a different policy from each native policy.

The original Phase 2 failed study and Phase 6's 2.39% pooled development-audit recall, including missing entire anomaly types, remain unchanged. New favorable results do not erase old failures; unfavorable or mixed results do not trigger model/generator repairs. Either or both models may fail the practical screen or fail to outperform one another. A positive aggregate cannot erase scenario losses or establish operational adequacy.

No retraining of either frozen model, empirical-CDF update, recalibration, feature edit, new candidate search, final-case redraw, dashboard edit, commit, push or deployment occurred. Existing and new tests were run before and after execution; fixture models in existing unit tests are separate temporary objects, not retraining of these frozen artifacts. Stop for user approval before publication or further development.
