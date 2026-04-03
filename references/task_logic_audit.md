# Task Logic Audit

## 1. Paradigm Intent

- Task: Risk Perception Estimation Task
- Primary construct: subjective risk perception / health-risk judgment
- Manipulated factors:
  - scenario risk level (`low_health_risk`, `medium_health_risk`, `high_health_risk`)
  - repeated sampling across blocks to estimate within-person stability and RT
- Dependent measures:
  - ordinal risk rating on a 1-7 scale
  - response time for the rating decision
  - condition-wise mean rating and mean RT
- Key citations:
  - Using social and behavioural science to support COVID-19 pandemic response
  - Measuring Risk Literacy: The Berlin Numeracy Test
  - Smokers’ unrealistic optimism about their risk
  - When a Day Means More than a Year: Effects of Temporal Framing on Judgments of Health Risk
  - Risk Perception and Risk-Taking Behaviour during Adolescence: The Influence of Personality and Gender

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 3
- Trials per block: 12
- Randomization/counterbalancing:
  - conditions are balanced across blocks with built-in block generation
  - trial order is shuffled within each block
- Condition weight policy:
  - `task.condition_weights` is omitted / `null`
  - runtime resolves no explicit weights, so generation is even by design
- Condition generation method:
  - built-in `BlockUnit.generate_conditions(...)`
  - a custom generator is not needed because simple condition labels are sufficient
  - generated condition data shape: a per-block list of condition labels passed directly into `run_trial.py`
- Runtime-generated trial values (if any):
  - `trial_id` and `block_idx` are generated at runtime
  - `rating_value` is derived from the pressed response key
  - block-level summary metrics are computed after each block from accumulated trial rows

### Trial State Machine

List each state in order with entry/exit conditions:

1. State name: `fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown: central fixation cross only
   - Valid keys: none
   - Timeout behavior: auto-advance after the fixed duration
   - Next state: `scenario_preview`

2. State name: `scenario_preview`
   - Onset trigger: `scenario_preview_onset`
   - Stimuli shown: condition-specific health-risk scenario text only
   - Valid keys: none
   - Timeout behavior: auto-advance after the fixed preview duration
   - Next state: `rating_response`

3. State name: `rating_response`
   - Onset trigger: `rating_response_onset`
   - Stimuli shown: the same scenario text plus the risk question and 1-7 rating scale
   - Valid keys: `1`, `2`, `3`, `4`, `5`, `6`, `7`
   - Timeout behavior: store a missing response and advance after the response window ends
   - Next state: `iti`

4. State name: `iti`
   - Onset trigger: `iti_onset`
   - Stimuli shown: central fixation cross only
   - Valid keys: none
   - Timeout behavior: auto-advance after the fixed ITI duration
   - Next state: next trial / end of block

## 3. Condition Semantics

For each condition token in `task.conditions`:

- Condition ID: `low_health_risk`
  - Participant-facing meaning: a clearly low-risk everyday health scenario
  - Concrete stimulus realization (visual/audio): text describing a low-risk outdoor or low-exposure situation
  - Outcome rules: participant gives a subjective risk rating from 1 (very low) to 7 (very high)

- Condition ID: `medium_health_risk`
  - Participant-facing meaning: a moderate-risk everyday health scenario
  - Concrete stimulus realization (visual/audio): text describing a moderately risky but not extreme exposure situation
  - Outcome rules: participant gives a subjective risk rating from 1 (very low) to 7 (very high)

- Condition ID: `high_health_risk`
  - Participant-facing meaning: a clearly high-risk everyday health scenario
  - Concrete stimulus realization (visual/audio): text describing a crowded / prolonged / high-exposure situation
  - Outcome rules: participant gives a subjective risk rating from 1 (very low) to 7 (very high)

Also document where participant-facing condition text/stimuli are defined:

- Participant-facing text source (config stimuli / code formatting / generated assets): config stimuli only
- Why this source is appropriate for auditability: each scenario and scale label is explicitly stored in `config/*.yaml`, so changes in wording do not require code edits
- Localization strategy (how language variants are swapped via config without code edits): Chinese participant-facing text is stored in `config/config.yaml` and uses `font: SimHei`; language variants can be swapped by replacing the config stimulus text and font settings

## 4. Response and Scoring Rules

- Response mapping: keys `1` through `7` map directly to ordinal risk ratings
- Response key source (config field vs code constant): config field `task.key_list`
- If code-defined, why config-driven mapping is not sufficient: not applicable
- Missing-response policy: record the trial as timed out and store `rating_value = null`
- Correctness logic: no binary correctness is used because this is a subjective rating task
- Reward/penalty updates: none; the task does not use adaptive reward or punishment
- Running metrics:
  - per-trial `rating_value`
  - per-block mean rating by condition
  - per-block mean RT
  - whole-task mean rating and mean RT

## 5. Stimulus Layout Plan

For every screen with multiple simultaneous options/stimuli:

- Screen name: `scenario_preview`
  - Stimulus IDs shown together: `scenario_text_low` / `scenario_text_medium` / `scenario_text_high`
  - Layout anchors (`pos`): centered, slightly above midline for readability
  - Size/spacing (`height`, width, wrap): large enough for one short paragraph with `wrapWidth` around 900 px
  - Readability/overlap checks: only one text block is shown, so no overlap risk
  - Rationale: the preview screen should isolate the scenario text before the response scale appears

- Screen name: `rating_response`
  - Stimulus IDs shown together: scenario text stimulus, `risk_prompt`, `rating_scale`
  - Layout anchors (`pos`): scenario text at upper center, prompt near center, rating scale near lower center
  - Size/spacing (`height`, width, wrap): scenario text uses a larger height and wider wrap; prompt and scale use smaller heights to preserve vertical spacing
  - Readability/overlap checks: vertical gaps between the three text regions are required so the prompt and scale remain readable on 1024x768 and 1280x720 windows
  - Rationale: the participant must see both the scenario and the ordinal response scale during the response window

## 6. Trigger Plan

Map each phase/state to trigger code and semantics.

- `exp_onset`: experiment start
- `exp_end`: experiment end
- `block_onset`: block start
- `block_end`: block end
- `fixation_onset`: fixation cross appears
- `scenario_preview_onset`: scenario text preview appears
- `rating_response_onset`: response screen appears and the key window opens
- `rating_response_key`: participant presses one of the rating keys
- `rating_response_timeout`: response window expires with no keypress
- `iti_onset`: inter-trial fixation appears

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style (simple single flow / helper-heavy / why): simple single flow with mode-aware setup (`human|qa|sim`) and no extra controller layer
- `utils.py` used? (yes/no): yes
- If yes, exact purpose (adaptive controller / sequence generation / asset pool / other): task-specific helpers for condition-to-scenario mapping, rating-key conversion, and block summaries
- Custom controller used? (yes/no): no
- If yes, why PsyFlow-native path is insufficient: not applicable
- Legacy/backward-compatibility fallback logic required? (yes/no): no
- If yes, scope and removal plan: not applicable

## 8. Inference Log

List any inferred decisions not directly specified by references:

- Decision: use a 1-7 ordinal rating scale rather than a continuous slider
  - Why inference was required: the framework’s standard response capture is key-based, not slider-based
  - Citation-supported rationale: the selected papers justify subjective risk judgments and numeric risk literacy, while the framework constraint determines the discrete implementation

- Decision: use three health-risk scenario levels rather than a single canonical scenario list
  - Why inference was required: the literature contains several compatible health-risk judgment paradigms but no single universally standardized stimulus set
  - Citation-supported rationale: smoker optimism, temporal framing, adolescent risk, and broader health-risk-response work all support a scenario-based health-risk judgment task

- Decision: no correctness or reward feedback
  - Why inference was required: the task measures subjective perception rather than objective accuracy
  - Citation-supported rationale: the selected papers emphasize judgment/risk perception, not binary performance scoring

## Contract Note

- Participant-facing labels/instructions/options should be config-defined whenever possible.
- `src/run_trial.py` should not hardcode participant-facing text that would require code edits for localization.
