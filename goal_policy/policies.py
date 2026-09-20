"""Transparent baselines and a history-informed plug-in DP policy."""

from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np

from .dp import KnownModelDP
from .environment import (
    Action,
    EnvironmentConfig,
    State,
    TaskType,
    available_surplus,
)


def _floor_grid(value: int, grid: int) -> int:
    return max(0, int(value) // grid * grid)


class FixedSplitPolicy:
    """Reserve-first policy with a fixed fraction of surplus for the goal."""

    def __init__(
        self,
        config: EnvironmentConfig | None = None,
        reserve_fraction: float = 0.50,
        goal_fraction: float = 0.50,
    ) -> None:
        self.config = config or EnvironmentConfig()
        self.reserve_fraction = float(np.clip(reserve_fraction, 0.0, 1.0))
        self.goal_fraction = float(np.clip(goal_fraction, 0.0, 1.0))

    def reset(self, state: State | None = None) -> None:
        del state

    def act(self, state: State, stochastic: bool = False) -> Action:
        del stochastic
        surplus = available_surplus(state)
        reserve_gap = max(0, self.config.reserve_target - state.reserve)
        goal_gap = max(0, self.config.goal_target - state.goal)
        reserve_cap = _floor_grid(reserve_gap, self.config.action_grid)
        e = min(
            reserve_cap,
            _floor_grid(round(surplus * self.reserve_fraction), self.config.action_grid),
        )
        remaining = surplus - e
        goal_cap = _floor_grid(goal_gap, self.config.action_grid)
        q = min(
            goal_cap,
            _floor_grid(round(remaining * self.goal_fraction), self.config.action_grid),
        )
        return e, q

    def observe(self, info: dict, next_state: State) -> None:
        del info, next_state


class ReserveFirstPolicy(FixedSplitPolicy):
    """Fill the reserve target before allocating any goal money."""

    def __init__(self, config: EnvironmentConfig | None = None) -> None:
        super().__init__(config=config, reserve_fraction=1.0, goal_fraction=1.0)

    def act(self, state: State, stochastic: bool = False) -> Action:
        del stochastic
        surplus = available_surplus(state)
        reserve_gap = _floor_grid(
            max(0, self.config.reserve_target - state.reserve),
            self.config.action_grid,
        )
        e = min(_floor_grid(surplus, self.config.action_grid), reserve_gap)
        remaining = surplus - e
        goal_gap = _floor_grid(
            max(0, self.config.goal_target - state.goal),
            self.config.action_grid,
        )
        return e, min(_floor_grid(remaining, self.config.action_grid), goal_gap)


class GoalFirstPolicy(FixedSplitPolicy):
    """Reach the optional goal before filling the emergency reserve."""

    def __init__(self, config: EnvironmentConfig | None = None) -> None:
        super().__init__(config=config, reserve_fraction=1.0, goal_fraction=1.0)

    def act(self, state: State, stochastic: bool = False) -> Action:
        del stochastic
        surplus = available_surplus(state)
        goal_gap = _floor_grid(
            max(0, self.config.goal_target - state.goal),
            self.config.action_grid,
        )
        q = min(_floor_grid(surplus, self.config.action_grid), goal_gap)
        remaining = surplus - q
        reserve_gap = _floor_grid(
            max(0, self.config.reserve_target - state.reserve),
            self.config.action_grid,
        )
        return min(_floor_grid(remaining, self.config.action_grid), reserve_gap), q


class BayesianDPPolicy:
    """Posterior-weighted action values from task-specific DP models.

    This is a deliberately simple adaptive baseline. It updates beliefs from
    observed salaries and expenses, then chooses the action with the largest
    posterior-weighted one-step DP value. It does not claim to solve the full
    belief-state POMDP; its purpose is to be a strong, transparent competitor
    for the recurrent Meta-RL policy.
    """

    def __init__(
        self,
        models: Mapping[str, KnownModelDP],
        tasks: Sequence[TaskType],
        prior: Mapping[str, float] | None = None,
        min_probability: float = 1e-12,
    ) -> None:
        self.models = dict(models)
        self.tasks = tuple(tasks)
        if {task.name for task in self.tasks} != set(self.models):
            raise ValueError("tasks and models must contain the same names")
        self.min_probability = float(min_probability)
        if prior is None:
            prior_values = {task.name: 1.0 / len(self.tasks) for task in self.tasks}
        else:
            prior_values = {task.name: max(0.0, float(prior.get(task.name, 0.0))) for task in self.tasks}
            total = sum(prior_values.values())
            if total <= 0:
                raise ValueError("prior must contain positive mass")
            prior_values = {name: value / total for name, value in prior_values.items()}
        self.prior = prior_values
        self.posterior = dict(prior_values)

    def reset(self, state: State | None = None) -> None:
        self.posterior = dict(self.prior)
        if state is not None:
            self._update(
                {
                    task.name: task.salary_probability(state.salary)
                    for task in self.tasks
                }
            )

    def _update(self, likelihoods: Mapping[str, float]) -> None:
        weighted = {
            task.name: self.posterior[task.name]
            * max(self.min_probability, float(likelihoods.get(task.name, 0.0)))
            for task in self.tasks
        }
        total = sum(weighted.values())
        if total <= 0:
            return
        self.posterior = {name: value / total for name, value in weighted.items()}

    def act(self, state: State, stochastic: bool = False) -> Action:
        del stochastic
        reference_model = next(iter(self.models.values()))
        candidates = reference_model.actions(state)
        values = {
            action: sum(
                self.posterior[task.name]
                * self.models[task.name].action_value(state, action)
                for task in self.tasks
            )
            for action in candidates
        }
        return max(values, key=lambda candidate: (values[candidate], -sum(candidate), -candidate[0]))

    def observe(self, info: dict, next_state: State) -> None:
        likelihoods = {
            task.name: task.expense_probability(int(info["expense"]))
            for task in self.tasks
        }
        self._update(likelihoods)
        if next_state.t < next(iter(self.models.values())).config.horizon:
            salary_likelihoods = {
                task.name: task.salary_probability(next_state.salary)
                for task in self.tasks
            }
            self._update(salary_likelihoods)
