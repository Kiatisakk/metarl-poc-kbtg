"""Matched-path evaluation and summary metrics."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

import numpy as np

from .environment import (
    EnvironmentConfig,
    GoalAllocationEnv,
    State,
    TaskType,
    Trajectory,
    sample_trajectory,
)


@dataclass(frozen=True)
class EpisodeResult:
    policy: str
    task: str
    total_reward: float
    goal_attained: float
    reserve_attained: float
    any_shortfall: float
    shortfall_amount: float
    terminal_wallet: float
    first_two_reward: float
    later_reward: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_episode(
    policy: Any,
    policy_name: str,
    task: TaskType,
    config: EnvironmentConfig,
    seed: int,
    trajectory: Trajectory | None = None,
) -> EpisodeResult:
    if hasattr(policy, "set_task"):
        policy.set_task(task)
    env = GoalAllocationEnv(task, config, seed=seed)
    state = env.reset(trajectory=trajectory)
    if hasattr(policy, "reset"):
        policy.reset(state)
    rewards: list[float] = []
    done = False
    while not done:
        action = policy.act(state, stochastic=False)
        next_state, reward, done, info = env.step(action)
        rewards.append(float(reward))
        if hasattr(policy, "observe"):
            policy.observe(info, next_state)
        state = next_state
    return EpisodeResult(
        policy=policy_name,
        task=task.name,
        total_reward=float(env.total_reward),
        goal_attained=float(state.goal >= config.goal_target),
        reserve_attained=float(state.reserve >= config.reserve_target),
        any_shortfall=float(env.shortfall_total > 0),
        shortfall_amount=float(env.shortfall_total),
        terminal_wallet=float(state.wallet),
        first_two_reward=float(sum(rewards[:2])),
        later_reward=float(sum(rewards[2:])),
    )


def evaluate_policies(
    policies: Mapping[str, Any],
    tasks: Sequence[TaskType],
    config: EnvironmentConfig | None = None,
    episodes_per_task: int = 200,
    seed: int = 123,
) -> list[EpisodeResult]:
    config = config or EnvironmentConfig()
    generator = np.random.default_rng(seed)
    trajectories: dict[tuple[str, int], Trajectory] = {}
    for task in tasks:
        for episode in range(int(episodes_per_task)):
            trajectories[(task.name, episode)] = sample_trajectory(
                task,
                config,
                generator,
            )

    results: list[EpisodeResult] = []
    for task in tasks:
        for episode in range(int(episodes_per_task)):
            trajectory = trajectories[(task.name, episode)]
            for policy_name, policy in policies.items():
                results.append(
                    run_episode(
                        policy,
                        policy_name,
                        task,
                        config,
                        seed=seed + episode,
                        trajectory=trajectory,
                    )
                )
    return results


def summarize(results: Sequence[EpisodeResult]) -> list[dict[str, Any]]:
    if not results:
        return []
    grouped: dict[tuple[str, str], list[EpisodeResult]] = {}
    for result in results:
        grouped.setdefault((result.policy, result.task), []).append(result)
    rows: list[dict[str, Any]] = []
    for (policy, task), group in sorted(grouped.items()):
        row: dict[str, Any] = {"policy": policy, "task": task, "episodes": len(group)}
        for field in (
            "total_reward",
            "goal_attained",
            "reserve_attained",
            "any_shortfall",
            "shortfall_amount",
            "terminal_wallet",
            "first_two_reward",
            "later_reward",
        ):
            values = np.asarray([getattr(result, field) for result in group], dtype=float)
            row[field] = float(np.mean(values))
            row[f"{field}_std"] = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
        rows.append(row)
    return rows


def paired_bootstrap_difference(
    results: Sequence[EpisodeResult],
    policy_a: str,
    policy_b: str,
    metric: str = "total_reward",
    samples: int = 1_000,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Return mean difference and a percentile bootstrap interval.

    Pairing uses (task, episode order) within the supplied result collection.
    The helper is intentionally small; a caller should provide matched result
    sets produced by evaluate_policies.
    """

    a = [result for result in results if result.policy == policy_a]
    b = [result for result in results if result.policy == policy_b]
    if len(a) != len(b) or not a:
        raise ValueError("Policies must have equal, non-empty result counts")
    a_values = np.asarray([getattr(result, metric) for result in a], dtype=float)
    b_values = np.asarray([getattr(result, metric) for result in b], dtype=float)
    difference = a_values - b_values
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(difference), size=(int(samples), len(difference)))
    bootstraps = np.mean(difference[indices], axis=1)
    lower, upper = np.percentile(bootstraps, [2.5, 97.5])
    return float(np.mean(difference)), float(lower), float(upper)
