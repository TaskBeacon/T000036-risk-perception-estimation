from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import random as _py_random

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


def _normalize_condition(label: Any) -> str:
    return str(label or "").strip().lower()


def _as_numeric_key(key: Any) -> int | None:
    try:
        value = int(str(key).strip())
    except Exception:
        return None
    return value if 1 <= value <= 7 else None


@dataclass
class TaskSamplerResponder:
    """Condition-aware sampler for the risk-perception rating task."""

    rating_key_map: dict[str, str] = field(
        default_factory=lambda: {
            "low_health_risk": "2",
            "medium_health_risk": "4",
            "high_health_risk": "6",
        }
    )
    noise_sd: float = 0.45
    rt_mean_s: float = 0.30
    rt_sd_s: float = 0.06
    rt_min_s: float = 0.12
    fallback_key: str | None = None

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.noise_sd = max(0.0, float(self.noise_sd))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))
        self.rating_key_map = {
            _normalize_condition(key): str(value).strip()
            for key, value in dict(self.rating_key_map or {}).items()
            if str(value).strip()
        }
        self.fallback_key = str(self.fallback_key).strip() if self.fallback_key else None

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def end_session(self) -> None:
        self._rng = None

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        if hasattr(rng, "gauss"):
            return float(rng.gauss(mean, sd))
        return float(mean)

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _choose_non_rating_key(self, valid_keys: list[str]) -> str | None:
        if self.fallback_key and self.fallback_key in valid_keys:
            return self.fallback_key
        if "space" in valid_keys:
            return "space"
        return valid_keys[0] if valid_keys else None

    def _choose_rating_key(self, obs: Observation, valid_keys: list[str]) -> str | None:
        factors = dict(obs.task_factors or {})
        condition = _normalize_condition(factors.get("condition") or obs.condition_id or "")

        target_key = str(factors.get("target_key") or self.rating_key_map.get(condition) or "").strip()
        target_rating = _as_numeric_key(target_key)
        if target_rating is None:
            target_rating = _as_numeric_key(factors.get("target_rating"))
        if target_rating is None:
            target_rating = _as_numeric_key(self.rating_key_map.get(condition))
        if target_rating is None:
            target_rating = 4

        numeric_valid = sorted(
            {
                value
                for value in (_as_numeric_key(key) for key in valid_keys)
                if value is not None
            }
        )
        if not numeric_valid:
            if target_key and target_key in valid_keys:
                return target_key
            return self._choose_non_rating_key(valid_keys)

        sampled_rating = int(round(self._sample_normal(float(target_rating), float(self.noise_sd))))
        sampled_rating = max(numeric_valid[0], min(numeric_valid[-1], sampled_rating))
        candidate = str(sampled_rating)
        if candidate in valid_keys:
            return candidate

        nearest = min(numeric_valid, key=lambda value: (abs(value - sampled_rating), value))
        candidate = str(nearest)
        if candidate in valid_keys:
            return candidate

        for key in valid_keys:
            if _as_numeric_key(key) is not None:
                return key
        return self._choose_non_rating_key(valid_keys)

    def act(self, obs: Observation) -> Action:
        valid_keys = [str(key).strip() for key in list(obs.valid_keys or []) if str(key).strip()]
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        rng = self._rng
        if rng is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "rng_missing"})

        factors = dict(obs.task_factors or {})
        stage = _normalize_condition(factors.get("stage") or obs.phase or "")
        rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))

        if stage == "rating_response":
            key = self._choose_rating_key(obs, valid_keys)
            if key is None:
                return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_rating_key"})
            meta = {
                "source": "task_sampler",
                "stage": stage,
                "condition": _normalize_condition(factors.get("condition") or obs.condition_id or ""),
                "target_rating": factors.get("target_rating"),
                "chosen_key": key,
            }
            return Action(key=key, rt_s=rt, meta=meta)

        key = self._choose_non_rating_key(valid_keys)
        if key is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_fallback_key"})

        meta = {
            "source": "task_sampler",
            "stage": stage,
            "condition": _normalize_condition(factors.get("condition") or obs.condition_id or ""),
            "chosen_key": key,
        }
        return Action(key=key, rt_s=rt, meta=meta)
