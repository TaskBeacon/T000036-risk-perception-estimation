# Task Plot Review

## Evidence Match

- Pass: title and construct match the Risk Perception Estimation Task.
- Pass: rows match configured low_health_risk, medium_health_risk, and high_health_risk conditions.
- Pass: phase order matches README and `src/run_trial.py`: Fixation -> Scenario preview -> Rating response -> ITI.
- Pass: timing labels match config: 500 ms fixation, 1000 ms scenario preview, 3000 ms response window, 700 ms ITI.
- Pass: response mapping shows 1-7 ordinal risk rating keys.
- Pass: no feedback, objective correctness, reward, or adaptive controller is shown.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
