from __future__ import annotations

from typing import Any, Iterable


CONDITION_TO_SCENARIO_STIM = {
    "low_health_risk": "scenario_low",
    "medium_health_risk": "scenario_medium",
    "high_health_risk": "scenario_high",
}

CONDITION_TO_TARGET_RATING = {
    "low_health_risk": 2,
    "medium_health_risk": 4,
    "high_health_risk": 6,
}


def normalize_condition_label(condition: Any) -> str:
    """Return a stable lower-case condition label."""
    label = str(condition or "").strip().lower()
    return label or "medium_health_risk"


def scenario_stimulus_id(condition: Any) -> str:
    """Map a condition label to the matching scenario stimulus id."""
    label = normalize_condition_label(condition)
    return CONDITION_TO_SCENARIO_STIM.get(label, "scenario_medium")


def target_rating_for_condition(condition: Any) -> int:
    """Return the nominal 1-7 risk rating associated with a condition."""
    label = normalize_condition_label(condition)
    return int(CONDITION_TO_TARGET_RATING.get(label, 4))


def rating_value_from_key(response_key: Any) -> int | None:
    """Convert a captured key into a 1-7 rating value when possible."""
    if response_key is None:
        return None

    key = str(response_key).strip()
    if not key:
        return None

    try:
        rating = int(key)
    except Exception:
        return None

    return rating if 1 <= rating <= 7 else None


def summarize_risk_trials(trials: Iterable[dict[str, Any]]) -> dict[str, float | int]:
    """Summarize trial-level ratings and response times for block feedback."""
    trial_list = list(trials)
    ratings: list[float] = []
    rts: list[float] = []

    for trial in trial_list:
        rating_value = trial.get("rating_value")
        if isinstance(rating_value, (int, float)):
            ratings.append(float(rating_value))

        response_rt = trial.get("response_rt")
        if isinstance(response_rt, (int, float)):
            rts.append(float(response_rt))

    mean_rating = sum(ratings) / len(ratings) if ratings else 0.0
    mean_rt = sum(rts) / len(rts) if rts else 0.0
    timeout_count = sum(1 for trial in trial_list if bool(trial.get("timeout", False)))

    return {
        "mean_rating": float(mean_rating),
        "mean_rt": float(mean_rt),
        "n_trials": int(len(trial_list)),
        "n_ratings": int(len(ratings)),
        "n_timeouts": int(timeout_count),
    }
