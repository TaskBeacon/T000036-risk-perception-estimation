from contextlib import nullcontext
from functools import partial
from pathlib import Path

import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    count_down,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import run_trial, summarize_risk_trials

MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def _collect_subject_data(options: TaskRunOptions, cfg: dict, runtime_ctx) -> dict[str, str]:
    if options.mode == "qa":
        return {"subject_id": "qa"}
    if options.mode == "sim":
        participant_id = "sim"
        if runtime_ctx is not None and runtime_ctx.session is not None:
            participant_id = str(runtime_ctx.session.participant_id or "sim")
        return {"subject_id": participant_id}

    subform = SubInfo(cfg["subform_config"])
    return subform.collect()


def run(options: TaskRunOptions):
    """Run the risk-perception estimation task in human/qa/sim mode."""
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path))

    output_dir: Path | None = None
    runtime_scope = nullcontext()
    runtime_ctx = None
    if options.mode in ("qa", "sim"):
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=options.mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)

    with runtime_scope:
        subject_data = _collect_subject_data(options, cfg, runtime_ctx)

        settings = TaskSettings.from_dict(cfg["task_config"])
        if options.mode in ("qa", "sim") and output_dir is not None:
            settings.save_path = str(output_dir)
        settings.add_subinfo(subject_data)

        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        settings.triggers = cfg["trigger_config"]
        trigger_runtime = initialize_triggers(mock=True) if options.mode in ("qa", "sim") else initialize_triggers(cfg)

        win, kb = initialize_exp(settings)

        stim_bank = StimBank(win, cfg["stim_config"])
        if options.mode == "human" and bool(getattr(settings, "voice_enabled", False)):
            stim_bank = stim_bank.convert_to_voice(
                "instruction_text",
                voice=str(getattr(settings, "voice_name", "zh-CN-YunyangNeural")),
            )
        stim_bank = stim_bank.preload_all()

        settings.controller = cfg.get("controller_config", {})
        settings.save_to_json()

        trigger_runtime.send(settings.triggers.get("exp_onset"))

        instruction = StimUnit("instruction_text", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get("instruction_text")
        )
        if options.mode == "human" and stim_bank.has("instruction_text_voice"):
            instruction.add_stim(stim_bank.get("instruction_text_voice"))
        instruction.wait_and_continue()

        all_data: list[dict] = []
        condition_weights = settings.resolve_condition_weights()
        for block_i in range(settings.total_blocks):
            if options.mode == "human":
                count_down(win, 3, color="black")

            block = (
                BlockUnit(
                    block_id=f"block_{block_i}",
                    block_idx=block_i,
                    settings=settings,
                    window=win,
                    keyboard=kb,
                )
                .generate_conditions(
                    n_trials=int(settings.trials_per_block),
                    condition_labels=list(getattr(settings, "conditions", [])),
                    weights=condition_weights,
                    order="random",
                )
                .on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset")))
                .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end")))
                .run_trial(
                    partial(
                        run_trial,
                        stim_bank=stim_bank,
                        trigger_runtime=trigger_runtime,
                        block_id=f"block_{block_i}",
                        block_idx=block_i,
                    )
                )
                .to_dict(all_data)
            )

            block_summary = summarize_risk_trials(block.get_all_data())
            StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get_and_format(
                    "block_break",
                    block_num=block_i + 1,
                    total_blocks=settings.total_blocks,
                    mean_rating=block_summary["mean_rating"],
                    mean_rt=block_summary["mean_rt"],
                )
            ).wait_and_continue()

        final_summary = summarize_risk_trials(all_data)
        StimUnit("goodbye", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get_and_format(
                "good_bye",
                mean_rating=final_summary["mean_rating"],
                mean_rt=final_summary["mean_rt"],
            )
        ).wait_and_continue(terminate=True)

        trigger_runtime.send(settings.triggers.get("exp_end"))

        pd.DataFrame(all_data).to_csv(settings.res_file, index=False)

        trigger_runtime.close()
        core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = parse_task_run_options(
        task_root=task_root,
        description="Run task in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )
    run(options)


if __name__ == "__main__":
    main()
