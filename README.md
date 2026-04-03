# Risk Perception Estimation Task

| Field | Value |
|---|---|
| Name | Risk Perception Estimation Task |
| Version | main (0.1.0-dev) |
| URL / Repository | https://github.com/TaskBeacon/T000036-risk-perception-estimation |
| Short Description | Chinese health-risk judgment task with 3 scenario levels and 1-7 ordinal ratings |
| Created By | TaskBeacon build pipeline |
| Date Updated | 2026-04-03 |
| PsyFlow Version | local checkout |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |

## 1. Task Overview

Participants judge the perceived health risk of brief everyday scenarios. The task uses three scenario levels (`low_health_risk`, `medium_health_risk`, `high_health_risk`) and a discrete 1-7 response scale. There is no objective correctness score and no reward feedback.

The runtime is split into human, QA, and simulation modes. Participant-facing wording is stored in `config/*.yaml` so the same task logic can be audited and localized without editing trial code.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| Load Config | Load the mode-specific config and task settings. |
| Collect Subject Info | Collect `subject_id` in human mode; inject deterministic IDs in QA/sim. |
| Setup Runtime | Initialize triggers, window, keyboard, and stimulus bank. |
| Show Instructions | Present the Chinese instruction screen, with optional instruction voice in human mode. |
| Generate Conditions | Use built-in `BlockUnit.generate_conditions(...)` with the three risk labels. |
| Run Trials | Execute the per-trial risk judgment flow for each condition. |
| Show Block Break | Display block mean rating and mean RT. |
| Save Data | Write trial-level CSV output and settings JSON. |
| Finalize | Emit the end trigger, close the trigger runtime, and quit PsychoPy. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Fixation | Show a central fixation cross. |
| Scenario Preview | Show the condition-specific risk vignette without response options. |
| Rating Response | Show the scenario again with the risk question and 1-7 scale; collect one keypress or timeout. |
| ITI | Show the fixation cross again before the next trial. |

### Controller Logic

| Feature | Description |
|---|---|
| Condition Scheduling | Uses PsyFlow `BlockUnit.generate_conditions(...)` with the configured condition labels. |
| Determinism | Block seeds come from `TaskSettings` so QA/sim runs are reproducible. |
| Adaptive Control | None. This task does not adapt difficulty or reward. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | Numeric participant ID in human mode; QA/sim inject deterministic placeholders. |

### b. Window Settings

| Parameter | Meaning |
|---|---|
| `window.size` | Window resolution in pixels. |
| `window.units` | PsychoPy coordinate units. |
| `window.bg_color` | Background color. |
| `window.fullscreen` | Fullscreen toggle. |

### c. Stimuli

| Stimulus ID | Purpose |
|---|---|
| `instruction_text` | Chinese task instructions. |
| `fixation` | Central fixation cross. |
| `scenario_low` / `scenario_medium` / `scenario_high` | Condition-specific health-risk scenarios. |
| `rating_prompt` | Risk question shown during the response window. |
| `rating_scale` | 1-7 ordinal rating legend. |
| `block_break` | Block summary with mean rating and mean RT. |
| `good_bye` | Final summary screen. |

### d. Timing

| Parameter | Meaning |
|---|---|
| `timing.fixation_duration` | Duration of the fixation screen. |
| `timing.scenario_preview_duration` | Duration of the scenario-only preview screen. |
| `timing.response_window_duration` | Duration of the rating response window. |
| `timing.iti_duration` | Inter-trial interval duration. |

### e. Triggers

| Parameter | Meaning |
|---|---|
| `exp_onset` / `exp_end` | Experiment start/end. |
| `block_onset` / `block_end` | Block start/end. |
| `fixation_onset` | Fixation screen onset. |
| `scenario_preview_onset` | Scenario preview onset. |
| `rating_response_onset` | Rating screen onset. |
| `rating_response_key` | Rating keypress trigger. |
| `rating_response_timeout` | Rating window timeout trigger. |
| `iti_onset` | ITI onset. |

### f. Adaptive Controller

| Parameter | Meaning |
|---|---|
| `task.conditions` | Condition labels scheduled across blocks. |
| `task.condition_weights` | Optional weights; `null` means even scheduling. |
| `task.key_list` | Valid rating keys (`1`-`7`). |
| `task.seed_mode` | Seed mode for reproducible block ordering. |

## 4. Methods (for academic publication)

Participants completed a computerized risk-perception judgment task implemented in PsychoPy/PsyFlow. Each trial presented a brief health-risk scenario, followed by a discrete 1-7 subjective risk rating. Trials were organized into three condition levels corresponding to low, medium, and high perceived risk. The task measured ordinal risk judgments and response latency, with no binary correctness or reward contingency. Trial stimuli, timings, and response mapping were config-defined to support reproducibility, auditability, and localization.

