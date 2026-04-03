# Task Plot Audit

- generated_at: 2026-04-03T19:54:09
- mode: existing
- task_path: E:\Taskbeacon\T000036-risk-perception-estimation

## 1. Inputs and provenance

- E:\Taskbeacon\T000036-risk-perception-estimation\README.md
- E:\Taskbeacon\T000036-risk-perception-estimation\config\config.yaml
- E:\Taskbeacon\T000036-risk-perception-estimation\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | Fixation | Show a central fixation cross. |
- | Scenario Preview | Show the condition-specific risk vignette without response options. |
- | Rating Response | Show the scenario again with the risk question and 1-7 scale; collect one keypress or timeout. |
- | ITI | Show the fixation cross again before the next trial. |

## 3. Evidence extracted from config/source

- low_health_risk: phase=fixation, deadline_expr=fixation_duration, response_expr=n/a, stim_expr='fixation'
- low_health_risk: phase=scenario preview, deadline_expr=preview_duration, response_expr=n/a, stim_expr=scenario_stim_id
- low_health_risk: phase=rating response, deadline_expr=response_duration, response_expr=response_duration, stim_expr=f'{scenario_stim_id}+rating_prompt+rating_scale'
- low_health_risk: phase=iti, deadline_expr=iti_duration, response_expr=n/a, stim_expr='fixation'
- medium_health_risk: phase=fixation, deadline_expr=fixation_duration, response_expr=n/a, stim_expr='fixation'
- medium_health_risk: phase=scenario preview, deadline_expr=preview_duration, response_expr=n/a, stim_expr=scenario_stim_id
- medium_health_risk: phase=rating response, deadline_expr=response_duration, response_expr=response_duration, stim_expr=f'{scenario_stim_id}+rating_prompt+rating_scale'
- medium_health_risk: phase=iti, deadline_expr=iti_duration, response_expr=n/a, stim_expr='fixation'
- high_health_risk: phase=fixation, deadline_expr=fixation_duration, response_expr=n/a, stim_expr='fixation'
- high_health_risk: phase=scenario preview, deadline_expr=preview_duration, response_expr=n/a, stim_expr=scenario_stim_id
- high_health_risk: phase=rating response, deadline_expr=response_duration, response_expr=response_duration, stim_expr=f'{scenario_stim_id}+rating_prompt+rating_scale'
- high_health_risk: phase=iti, deadline_expr=iti_duration, response_expr=n/a, stim_expr='fixation'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 4
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: no adjustment needed; left=0.027, right=0.041, blank=0.276
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0265, 'right_ratio': 0.0409, 'blank_ratio': 0.2758}

## 7. Output files and checksums

- E:\Taskbeacon\T000036-risk-perception-estimation\references\task_plot_spec.yaml: sha256=5067ecb436fd76ddfd4411bfd2d0f2fac19540f7e174ddbb062cd41c26feeb1e
- E:\Taskbeacon\T000036-risk-perception-estimation\references\task_plot_spec.json: sha256=d4f30c3490bb08d2ddff8fa9784c7170954dcd41fc91d52c4969cacfe903fad6
- E:\Taskbeacon\T000036-risk-perception-estimation\references\task_plot_source_excerpt.md: sha256=af5d4cafcefa8b40b17a057263e02e969c9404587443b01a58adf1723e9b2a84
- E:\Taskbeacon\T000036-risk-perception-estimation\task_flow.png: sha256=90200df67cca4769640db19ce12babbaf205b0283542f80683701262d7b4b2f5

## 8. Inferred/uncertain items

- low_health_risk:fixation:heuristic numeric parse from 'float(getattr(settings, 'fixation_duration', 0.5))'
- low_health_risk:scenario preview:heuristic numeric parse from 'float(getattr(settings, 'scenario_preview_duration', 1.0))'
- low_health_risk:rating response:heuristic numeric parse from 'float(getattr(settings, 'response_window_duration', 3.0))'
- low_health_risk:iti:heuristic numeric parse from 'float(getattr(settings, 'iti_duration', 0.7))'
- medium_health_risk:fixation:heuristic numeric parse from 'float(getattr(settings, 'fixation_duration', 0.5))'
- medium_health_risk:scenario preview:heuristic numeric parse from 'float(getattr(settings, 'scenario_preview_duration', 1.0))'
- medium_health_risk:rating response:heuristic numeric parse from 'float(getattr(settings, 'response_window_duration', 3.0))'
- medium_health_risk:iti:heuristic numeric parse from 'float(getattr(settings, 'iti_duration', 0.7))'
- high_health_risk:fixation:heuristic numeric parse from 'float(getattr(settings, 'fixation_duration', 0.5))'
- high_health_risk:scenario preview:heuristic numeric parse from 'float(getattr(settings, 'scenario_preview_duration', 1.0))'
- high_health_risk:rating response:heuristic numeric parse from 'float(getattr(settings, 'response_window_duration', 3.0))'
- high_health_risk:iti:heuristic numeric parse from 'float(getattr(settings, 'iti_duration', 0.7))'
- collapsed equivalent condition logic into representative timeline: low_health_risk, medium_health_risk, high_health_risk
- unparsed if-tests defaulted to condition-agnostic applicability: str(condition).strip().lower() == 'high_health_risk'; str(condition).strip().lower() == 'medium_health_risk'
