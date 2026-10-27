# Recorded evidence

These compact files copy the completed Phase 4 run
20261026T230547002064Z. They support review without committing raw repeated-run
datasets or fitted model files. The original full run remains local under the
application's ignored outputs/phase4 directory.

- phase4_report.md: interpretation and verification recorded at the end of Phase 4.
- future_summary.csv / future_overall_summary.csv: future mean, sample SD and ranges.
- validation_summary.csv / validation_runs.csv: evidence used for selection.
- future_runs.csv: all 30 future detector assessments.
- protocol.json: settings, parameters, versions and original source hashes.
- selection_freeze.json: pre-assessment model selection, thresholds and artifact hashes.
- evaluation_metrics.json: completion metadata and summary.
- dashboard_robustness.png: verified local chart screenshot.

Historical reports record the file layout and test count at that phase. Current
commands use unittest discovery in tests/; see the root README and docs/VALIDATION.md.
Hash entries reference the original recorded run. Phase 5 also corrected the
SVG title encoding in main.py; its current source hash therefore differs from
the recorded one. The model/threshold logic and prior output files are unchanged,
and the pre-cleanup source is backed up locally. This does not rewrite run provenance. Reproduction creates a new timestamped
run with the same fixed datasets, not a new independent evaluation sample.
