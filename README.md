# Meta-RL POC — K PLUS First Jobber Hackathon

This repository contains a small, reproducible Track 2 experiment for
user-adaptive sequential goal management. The simulator allocates each cycle's
surplus among liquid cash, an emergency reserve, and one optional goal.

All experiment amounts are synthetic simulation units. The project does not
connect to K PLUS, move real funds, or make production financial-advice claims.

## Quick start

```text
python -m pip install -r requirements.txt
python run_tests.py
python run_tests.py --experiment --episodes 5
```

`run_tests.py` always creates `artifacts/unit_test_report.json` and
`artifacts/unit_test_report.md`. With `--experiment`, it also refreshes the
matched-path DP comparison in the `artifacts/` directory.

For the full comparison, including pooled Q-learning and recurrent Meta-RL:

```text
python run_experiment.py --episodes 100
```

The default CLI uses a balance bin of 20 and allocation grid of 20 so the
experiment remains practical on a student laptop. Use
`--dp-balance-bin 1 --dp-action-grid 5` for the finest DP discretization;
runtime grows substantially.

## Project layout

- `goal_policy/environment.py`: seeded simulator and transition model
- `goal_policy/policies.py`: transparent and Bayesian DP policies
- `goal_policy/dp.py`: finite-horizon known-model DP
- `goal_policy/rl.py`: pooled Q-learning and recurrent Meta-RL prototype
- `goal_policy/evaluation.py`: matched evaluation and metrics
- `run_experiment.py`: experiment CLI
- `run_tests.py`: test and artifact runner
- `tests/`: unit and integration checks
- `EXPERIMENT_PROPOSAL.md`: mathematical formulation and research protocol
- `ONE_PAGE_PITCH_PROPOSAL.md`: the five required booklet sections in pitch form
- `proposal/`: IEEE-style research proposal and one-page PDF pitch adapted from the public hackathon template
- `ref/`: research papers and source materials used by the proposal

The main research decision is whether Meta-RL improves held-out adaptation
over a transparent Bayesian DP baseline. If it does not, the simpler method
should be retained.
