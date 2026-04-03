# CHANGELOG

All notable development changes for `Risk Perception Estimation Task` are documented here.

## [0.1.0-dev] - 2026-04-03

### Added
- Built a three-condition health-risk judgment task with ordinal 1-7 ratings.
- Replaced the generic template controller with PsyFlow-native block condition generation.
- Added condition-aware risk scenario mapping and block/final summary helpers.
- Added a sampler responder for QA/sim mode that chooses rating keys by condition.
- Updated config, stimulus mapping, and task audit artifacts for the new paradigm.

### Changed
- Human-mode instructions now use the Chinese task wording and SimHei font.
- Block breaks and the final goodbye screen now summarize mean rating and mean RT.

### Fixed
- Removed generic accuracy/feedback logic that did not apply to a subjective rating task.

