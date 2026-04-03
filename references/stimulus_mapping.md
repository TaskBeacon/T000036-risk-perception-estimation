# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `all` | `instruction` | `instruction_text` | `请根据每个情境的主观危险程度进行评分。按 1-7 键作答：1 = 非常低，7 = 非常高。` | `W2142604507`, `W3016902371` | Risk-literacy and health-risk judgment framing; inferred from the selected papers’ methods and task descriptions | `psychopy_builtin` | `n/a` | Inferred participant instruction text for the Chinese task build. |
| `all` | `fixation` | `fixation` | `+` | `W2142604507` | Generic fixation used for paced judgment tasks; inferred from standard experimental timing | `psychopy_builtin` | `n/a` | Neutral inter-phase fixation. |
| `low_health_risk` | `scenario_preview`, `rating_response` | `scenario_low` | `你在空旷的户外散步，周围几乎没有其他人。` | `W2121507569`, `W3016902371` | Health-risk optimism and protective-behavior context; scenario wording is inferred to express low perceived risk | `psychopy_builtin` | `n/a` | Low-risk health scenario. |
| `medium_health_risk` | `scenario_preview`, `rating_response` | `scenario_medium` | `你在通风良好的室内与少数人短暂停留。` | `W2129528797`, `W3016902371` | Temporal-framing and health-risk judgment context; scenario wording is inferred to express moderate risk | `psychopy_builtin` | `n/a` | Moderate-risk health scenario. |
| `high_health_risk` | `scenario_preview`, `rating_response` | `scenario_high` | `你在拥挤的室内参加长时间聚会。` | `W2177211260`, `W3016902371` | Risk-perception and health-risk response context; scenario wording is inferred to express high risk | `psychopy_builtin` | `n/a` | High-risk health scenario. |
| `all` | `rating_response` | `rating_prompt`, `rating_scale` | `你觉得这个情境有多危险？` and `1  非常低   2  较低   3  稍低   4  中等   5  稍高   6  高   7  非常高` | `W2142604507`, `W2129528797` | Explicit numeric scale and risk-rating language; inferred from numeracy and health-risk judgment literature | `psychopy_builtin` | `n/a` | Shared response prompt and ordinal scale. |

Allowed implementation modes:

- `psychopy_builtin`
- `generated_reference_asset`
- `licensed_external_asset`

Decision rule:

- Participant-facing text should be configured in `config/*.yaml` stimuli and referenced via stimulus IDs.
