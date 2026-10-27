# Final verification - October 26, 2026

## Results

- All 26 tests passed using unittest discovery under tests/.
- A temporary copy of the 56 files included by Git's current ignore rules
  ran Phase 1, default Phase 2 and the complete test suite successfully.
- All 16 reference CSV/JSON files reproduced byte-for-byte.
- All 4 SVG plots matched after normalizing their title text.
  A pre-existing encoding problem in the renderer's title was corrected to ASCII.
  Original saved charts remain unchanged; all plotted coordinates/values match.
- All 12 local Markdown links checked in that snapshot resolved.
- All 187 pre-Phase-5 data/result artifacts retained their SHA-256 hashes,
  including the six original baseline artifacts and recorded Phase 4 models/results.
- pip check reported no broken requirements.
- Git ignore checks excluded the existing environment, backups, databases and
  repeated-run output directories while retaining small Phase 1/2 fixtures.

## Test coverage

Threshold optima/ties/invalid scores, chronological boundaries, exact prior-day
history, same-day exclusion, future/label/order invariance, cold starts, finite
features, generator/scenario reproducibility, no-positive fallback, undefined metric
flags, sample-SD calculation, training-only scaler parameters, trusted local model
round-trip predictions, incomplete robustness runs, SQL/Pandas agreement and
Streamlit AppTest filtering/experiment/threshold controls.

The two SQL tests use an in-memory SQLite database populated from synthetic fixtures;
they account for daily rows and compare customer aggregation/filtering against Pandas.
The clean snapshot intentionally excludes the local Phase 4 runs, so dashboard tests
also verify operation with reference fixtures alone. The full robustness dashboard
and model evidence were checked during Phase 4.

## Scope and limits

The snapshot used the existing Python 3.12 virtual environment on Windows. It verifies
independence from ignored files, not a fresh environment installation or another OS.
Phase 4 was not repeated in Phase 5: no model/threshold/history code changed, and its
30 frozen bundles plus paired datasets were already verified in Phase 4. Rerunning
those fixed seeds would not produce independent evaluation evidence.

The SVG title cleanup changes the current main.py source hash relative to the
recorded Phase 4 protocol. Original source is retained in the local backup. This
text-only correction does not change model or metric calculations.

Changes remain local and uncommitted on codex/phase1-threshold-tuning. No remote
repository was created; nothing was pushed or published. No licensing terms or
real-world fraud performance claims were introduced.
