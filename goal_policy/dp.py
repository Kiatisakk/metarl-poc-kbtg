"""Exact finite-horizon dynamic programming for the discrete simulator."""

from __future__ import annotations

from functools import lru_cache
from typing import Mapping

from .environment import (
    Action,
    EnvironmentConfig,
    State,
    TaskType,
    GoalAllocationEnv,
    terminal_reward,
    transition_outcomes,
)


class KnownModelDP:
    """Oracle policy whose task transition model is known."""

    def __init__(
        self,
        task: TaskType,
        config: EnvironmentConfig | None = None,
        balance_bin: int = 1,
        action_grid: int | None = None,
    ) -> None:
        self.task = task
        self.config = config or EnvironmentConfig()
        if balance_bin <= 0:
            raise ValueError("balance_bin must be positive")
        self.balance_bin = int(balance_bin)
        self.dp_action_grid = int(action_grid or self.config.action_grid)
        if self.dp_action_grid <= 0 or self.dp_action_grid % self.config.action_grid != 0:
            raise ValueError("DP action_grid must be a positive multiple of environment action_grid")
        self._value_cached = lru_cache(maxsize=None)(self._value_uncached)
        self._action_value_cached = lru_cache(maxsize=None)(self._action_value_uncached)

    def _canonical_state(self, state: State) -> State:
        if state.t >= self.config.horizon:
            return state
        bin_size = self.balance_bin
        floor = lambda value: max(0, int(value) // bin_size * bin_size)
        return State(
            t=state.t,
            wallet=floor(state.wallet),
            reserve=floor(state.reserve),
            goal=floor(state.goal),
            deadline=state.deadline,
            salary=state.salary,
            fixed=state.fixed,
        )

    def _value_uncached(self, state: State) -> float:
        if state.t >= self.config.horizon:
            return terminal_reward(state, self.config)
        return max(
            self._action_value_cached(state, action)
            for action in self.actions(state)
        )

    def actions(self, state: State) -> tuple[Action, ...]:
        state = self._canonical_state(state)
        surplus = max(0, state.wallet + state.salary - state.fixed)
        grid = self.dp_action_grid
        max_units = surplus // grid
        return tuple(
            (e_units * grid, q_units * grid)
            for e_units in range(max_units + 1)
            for q_units in range(max_units - e_units + 1)
        )

    def _action_value_uncached(self, state: State, action: Action) -> float:
        expected = 0.0
        for probability, transition in transition_outcomes(
            state, action, self.task, self.config
        ):
            expected += probability * (
                transition.step_reward + self.value(transition.next_state)
            )
        return expected

    def value(self, state: State) -> float:
        if state.t >= self.config.horizon:
            return float(terminal_reward(state, self.config))
        return float(self._value_cached(self._canonical_state(state)))

    def action_values(self, state: State) -> dict[Action, float]:
        state = self._canonical_state(state)
        return {
            action: float(self._action_value_cached(state, action))
            for action in self.actions(state)
        }

    def action_value(self, state: State, action: Action) -> float:
        state = self._canonical_state(state)
        return float(self._action_value_cached(state, action))

    def action(self, state: State) -> Action:
        values = self.action_values(state)
        return max(values, key=lambda candidate: (values[candidate], -sum(candidate), -candidate[0]))

    def cache_info(self) -> dict[str, int]:
        value_info = self._value_cached.cache_info()
        action_info = self._action_value_cached.cache_info()
        return {
            "value_hits": value_info.hits,
            "value_misses": value_info.misses,
            "value_size": value_info.currsize,
            "action_hits": action_info.hits,
            "action_misses": action_info.misses,
            "action_size": action_info.currsize,
        }

    def solve_from_initial(self, seed: int = 0) -> tuple[State, float]:
        env = GoalAllocationEnv(self.task, self.config, seed=seed)
        state = env.reset()
        return state, self.value(state)


class OracleDPPolicy:
    """Task-aware wrapper used to evaluate the known-model oracle fairly."""

    def __init__(
        self,
        models: Mapping[str, KnownModelDP],
    ) -> None:
        self.models = dict(models)
        self.current_task: str | None = None

    def set_task(self, task: TaskType) -> None:
        if task.name not in self.models:
            raise KeyError(f"No DP model supplied for task {task.name!r}")
        self.current_task = task.name

    def reset(self, state: State | None = None) -> None:
        return None

    def act(self, state: State, stochastic: bool = False) -> Action:
        del stochastic
        if self.current_task is None:
            raise RuntimeError("set_task() must be called before act()")
        return self.models[self.current_task].action(state)

    def observe(self, info: dict, next_state: State) -> None:
        del info, next_state
