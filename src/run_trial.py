from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import rating_value_from_key, target_rating_for_condition


def _normalize_condition(condition: Any) -> str:
    return str(condition or "").strip().lower() or "medium_health_risk"


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one risk-perception judgment trial."""
    condition_label = _normalize_condition(condition)
    if str(condition).strip().lower() == "medium_health_risk":
        scenario_stim_id = "scenario_medium"
    elif str(condition).strip().lower() == "high_health_risk":
        scenario_stim_id = "scenario_high"
    else:
        scenario_stim_id = "scenario_low"
    target_rating = target_rating_for_condition(condition_label)
    trial_id = int(next_trial_id())

    block_id_str = str(block_id) if block_id is not None else "block_0"
    block_index = int(block_idx) if block_idx is not None else 0
    fixation_duration = float(getattr(settings, "fixation_duration", 0.5))
    preview_duration = float(getattr(settings, "scenario_preview_duration", 1.0))
    response_duration = float(getattr(settings, "response_window_duration", 3.0))
    iti_duration = float(getattr(settings, "iti_duration", 0.7))
    valid_keys = [str(k) for k in list(getattr(settings, "key_list", []))]
    response_triggers = {key: settings.triggers.get("rating_response_key") for key in valid_keys}

    trial_data = {
        "trial_id": trial_id,
        "block_id": block_id_str,
        "block_idx": block_index,
        "condition": condition_label,
        "condition_label": condition_label,
        "scenario_stim_id": scenario_stim_id,
        "target_rating": target_rating,
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    fixation = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="fixation",
        deadline_s=fixation_duration,
        valid_keys=[],
        block_id=block_id_str,
        condition_id=condition_label,
        task_factors={
            "stage": "fixation",
            "condition": condition_label,
            "target_rating": target_rating,
            "block_idx": block_index,
        },
        stim_id="fixation",
    )
    fixation.show(
        duration=fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    scenario_preview = make_unit(unit_label="scenario_preview").add_stim(stim_bank.get(scenario_stim_id))
    set_trial_context(
        scenario_preview,
        trial_id=trial_id,
        phase="scenario_preview",
        deadline_s=preview_duration,
        valid_keys=[],
        block_id=block_id_str,
        condition_id=condition_label,
        task_factors={
            "stage": "scenario_preview",
            "condition": condition_label,
            "target_rating": target_rating,
            "block_idx": block_index,
        },
        stim_id=scenario_stim_id,
    )
    scenario_preview.show(
        duration=preview_duration,
        onset_trigger=settings.triggers.get("scenario_preview_onset"),
    ).to_dict(trial_data)

    rating_response = make_unit(unit_label="rating_response")
    rating_response.add_stim(stim_bank.get(scenario_stim_id))
    rating_response.add_stim(stim_bank.get("rating_prompt"))
    rating_response.add_stim(stim_bank.get("rating_scale"))
    set_trial_context(
        rating_response,
        trial_id=trial_id,
        phase="rating_response",
        deadline_s=response_duration,
        valid_keys=valid_keys,
        block_id=block_id_str,
        condition_id=condition_label,
        task_factors={
            "stage": "rating_response",
            "condition": condition_label,
            "target_rating": target_rating,
            "block_idx": block_index,
        },
        stim_id=f"{scenario_stim_id}+rating_prompt+rating_scale",
        stim_features={
            "condition": condition_label,
            "target_rating": target_rating,
            "valid_keys": valid_keys,
        },
    )
    rating_response.capture_response(
        keys=valid_keys,
        duration=response_duration,
        correct_keys=valid_keys,
        onset_trigger=settings.triggers.get("rating_response_onset"),
        response_trigger=response_triggers if response_triggers else settings.triggers.get("rating_response_key"),
        timeout_trigger=settings.triggers.get("rating_response_timeout"),
    )
    rating_response.to_dict(trial_data)

    response_key = str(rating_response.get_state("response", "") or "").strip()
    response_rt = rating_response.get_state("rt", None)
    rating_value = rating_value_from_key(response_key)
    timeout = rating_value is None

    trial_data.update(
        {
            "response_key": response_key,
            "response_rt": float(response_rt) if isinstance(response_rt, (int, float)) else None,
            "rating_value": rating_value,
            "timeout": bool(timeout),
            "responded": not bool(timeout),
        }
    )

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="iti",
        deadline_s=iti_duration,
        valid_keys=[],
        block_id=block_id_str,
        condition_id=condition_label,
        task_factors={
            "stage": "iti",
            "condition": condition_label,
            "target_rating": target_rating,
            "block_idx": block_index,
        },
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    return trial_data
