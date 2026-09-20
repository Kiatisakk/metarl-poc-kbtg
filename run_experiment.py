"""Run the sequential goal-allocation experiment.

Examples:
    python run_experiment.py --episodes 100
    python run_experiment.py --episodes 20 --rl-episodes 500 --meta-episodes 500
    python run_experiment.py --skip-rl --skip-meta --json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from goal_policy.dp import KnownModelDP, OracleDPPolicy
from goal_policy.environment import EnvironmentConfig, TaskType
from goal_policy.evaluation import evaluate_policies, summarize
from goal_policy.policies import (
    BayesianDPPolicy,
    FixedSplitPolicy,
    GoalFirstPolicy,
    ReserveFirstPolicy,
)
from goal_policy.rl import PooledQPolicy, RecurrentMetaPolicy


def default_tasks() -> tuple[TaskType, ...]:
    return (
        TaskType(
            name="stable",
            salary_mean=100,
            salary_sd=5,
            expense_mean=20,
            expense_sd=5,
            shock_probability=0.02,
            shock_size=40,
        ),
        TaskType(
            name="variable",
            salary_mean=100,
            salary_sd=15,
            expense_mean=25,
            expense_sd=10,
            shock_probability=0.08,
            shock_size=60,
        ),
        TaskType(
            name="shock_prone",
            salary_mean=100,
            salary_sd=10,
            expense_mean=25,
            expense_sd=12,
            shock_probability=0.20,
            shock_size=100,
        ),
    )


def build_policies(
    tasks: tuple[TaskType, ...],
    config: EnvironmentConfig,
    seed: int,
    include_rl: bool,
    include_meta: bool,
    rl_episodes: int,
    meta_episodes: int,
    dp_balance_bin: int,
    dp_action_grid: int,
) -> dict[str, object]:
    models = {
        task.name: KnownModelDP(
            task,
            config,
            balance_bin=dp_balance_bin,
            action_grid=dp_action_grid,
        )
        for task in tasks
    }
    policies: dict[str, object] = {
        "reserve_first": ReserveFirstPolicy(config),
        "goal_first": GoalFirstPolicy(config),
        "fixed_split": FixedSplitPolicy(config, reserve_fraction=0.50, goal_fraction=0.50),
        "dp_oracle": OracleDPPolicy(models),
        "bayesian_dp": BayesianDPPolicy(models, tasks),
    }
    if include_rl:
        pooled = PooledQPolicy(tasks, config, seed=seed)
        pooled.train(episodes=rl_episodes, seed=seed)
        policies["pooled_q"] = pooled
    if include_meta:
        meta = RecurrentMetaPolicy(tasks, config, seed=seed)
        meta.train(episodes=meta_episodes, seed=seed + 1)
        policies["recurrent_meta"] = meta
    return policies


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=100, help="matched evaluation episodes per task")
    parser.add_argument("--rl-episodes", type=int, default=1_000, help="pooled Q-learning episodes")
    parser.add_argument("--meta-episodes", type=int, default=1_000, help="recurrent Meta-RL episodes")
    parser.add_argument(
        "--dp-balance-bin",
        type=int,
        default=20,
        help="DP balance discretization; use 1 for the finest grid",
    )
    parser.add_argument(
        "--dp-action-grid",
        type=int,
        default=20,
        help="DP allocation grid; use 5 to match the environment grid exactly",
    )
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--skip-rl", action="store_true")
    parser.add_argument("--skip-meta", action="store_true")
    parser.add_argument("--json", action="store_true", help="print summary as JSON")
    parser.add_argument("--output", type=Path, help="optional JSON output path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = EnvironmentConfig()
    tasks = default_tasks()
    policies = build_policies(
        tasks,
        config,
        seed=args.seed,
        include_rl=not args.skip_rl,
        include_meta=not args.skip_meta,
        rl_episodes=args.rl_episodes,
        meta_episodes=args.meta_episodes,
        dp_balance_bin=args.dp_balance_bin,
        dp_action_grid=args.dp_action_grid,
    )
    results = evaluate_policies(
        policies,
        tasks,
        config=config,
        episodes_per_task=args.episodes,
        seed=args.seed + 10,
    )
    rows = summarize(results)
    if args.output:
        args.output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(rows, indent=2))
        return

    headers = (
        "policy",
        "task",
        "episodes",
        "total_reward",
        "goal_attained",
        "reserve_attained",
        "any_shortfall",
        "shortfall_amount",
        "terminal_wallet",
    )
    print("\t".join(headers))
    for row in rows:
        print(
            "\t".join(
                str(row[key]) if key in {"policy", "task", "episodes"} else f"{row[key]:.4f}"
                for key in headers
            )
        )


if __name__ == "__main__":
    main()
