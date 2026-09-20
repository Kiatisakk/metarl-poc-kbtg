"""Deterministic, finite-horizon environment for sequential goal allocation.

The implementation mirrors the event order in EXPERIMENT_PROPOSAL.md:
salary and fixed obligations arrive first, the policy allocates surplus, a
variable expense is realized, and the next state is created.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np

Action = tuple[int, int]


def _merge_outcomes(outcomes: Iterable[tuple[int, float]]) -> tuple[tuple[int, float], ...]:
    merged: dict[int, float] = {}
    for value, probability in outcomes:
        merged[int(value)] = merged.get(int(value), 0.0) + float(probability)
    total = sum(merged.values())
    if total <= 0:
        raise ValueError("Outcome probabilities must sum to a positive value")
    return tuple(sorted((value, probability / total) for value, probability in merged.items()))


@dataclass(frozen=True)
class TaskType:
    """One hidden cash-flow dynamics type used by the simulator.

    The defaults are deliberately simulation units. They are not claims about
    Thai salaries, expenses, or customer populations.
    """

    name: str
    salary_mean: float = 100.0
    salary_sd: float = 5.0
    expense_mean: float = 20.0
    expense_sd: float = 5.0
    shock_probability: float = 0.02
    shock_size: float = 40.0

    def salary_outcomes(self) -> tuple[tuple[int, float], ...]:
        sd = max(0.0, float(self.salary_sd))
        mean = max(0.0, float(self.salary_mean))
        return _merge_outcomes(
            (
                (round(max(0.0, mean - sd)), 0.25),
                (round(mean), 0.50),
                (round(mean + sd), 0.25),
            )
        )

    def expense_outcomes(self) -> tuple[tuple[int, float], ...]:
        sd = max(0.0, float(self.expense_sd))
        mean = max(0.0, float(self.expense_mean))
        p = min(1.0, max(0.0, float(self.shock_probability)))
        base = (
            (round(max(0.0, mean - sd)), 0.25),
            (round(mean), 0.50),
            (round(mean + sd), 0.25),
        )
        return _merge_outcomes(
            [(value, probability * (1.0 - p)) for value, probability in base]
            + [(value + round(max(0.0, self.shock_size)), probability * p) for value, probability in base]
        )

    def sample_salary(self, rng: np.random.Generator) -> int:
        values, probabilities = zip(*self.salary_outcomes())
        return int(rng.choice(np.asarray(values), p=np.asarray(probabilities)))

    def sample_expense(self, rng: np.random.Generator) -> int:
        values, probabilities = zip(*self.expense_outcomes())
        return int(rng.choice(np.asarray(values), p=np.asarray(probabilities)))

    def salary_probability(self, value: int) -> float:
        return dict(self.salary_outcomes()).get(int(value), 0.0)

    def expense_probability(self, value: int) -> float:
        return dict(self.expense_outcomes()).get(int(value), 0.0)


@dataclass(frozen=True)
class EnvironmentConfig:
    """Experiment controls and reward weights."""

    horizon: int = 6
    fixed_obligation: int = 60
    initial_wallet: int = 40
    initial_reserve: int = 20
    initial_goal: int = 0
    goal_target: int = 100
    reserve_target: int = 60
    action_grid: int = 5
    max_action_cash: int = 400
    eta_consumption: float = 0.10
    shortfall_penalty: float = 2.0
    eta_reserve: float = 0.05
    eta_goal: float = 10.0
    eta_emergency: float = 4.0
    eta_wallet: float = 0.02
    goal_deadline: int | None = None

    def __post_init__(self) -> None:
        if self.horizon <= 0:
            raise ValueError("horizon must be positive")
        if self.action_grid <= 0:
            raise ValueError("action_grid must be positive")
        if self.max_action_cash < 0:
            raise ValueError("max_action_cash must be non-negative")
        if self.goal_deadline is not None and not 1 <= self.goal_deadline <= self.horizon:
            raise ValueError("goal_deadline must be between 1 and horizon")

    @property
    def deadline(self) -> int:
        return self.goal_deadline if self.goal_deadline is not None else self.horizon


@dataclass(frozen=True)
class State:
    """Decision-point state after the current salary and fixed obligation arrive."""

    t: int
    wallet: int
    reserve: int
    goal: int
    deadline: int
    salary: int
    fixed: int


@dataclass(frozen=True)
class Trajectory:
    """Exogenous salary and expense path used for matched evaluation."""

    salaries: tuple[int, ...]
    expenses: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.salaries) != len(self.expenses):
            raise ValueError("salaries and expenses must have equal length")
        if not self.salaries:
            raise ValueError("trajectory must contain at least one cycle")


@dataclass(frozen=True)
class Transition:
    next_state: State
    step_reward: float
    terminal_reward: float
    info: dict[str, Any]


def available_surplus(state: State) -> int:
    """Cash left after the current salary and fixed obligation."""

    return max(0, int(state.wallet + state.salary - state.fixed))


def fixed_shortfall(state: State) -> int:
    return max(0, int(state.fixed - state.wallet - state.salary))


def valid_actions(state: State, config: EnvironmentConfig) -> tuple[Action, ...]:
    """Enumerate the discrete feasible allocation pairs for a state."""

    surplus = available_surplus(state)
    grid = config.action_grid
    if surplus < grid:
        return ((0, 0),)

    max_units = surplus // grid
    actions: list[Action] = []
    for e_units in range(max_units + 1):
        for q_units in range(max_units - e_units + 1):
            actions.append((e_units * grid, q_units * grid))
    return tuple(actions)


def is_valid_action(state: State, action: Action, config: EnvironmentConfig) -> bool:
    e, q = int(action[0]), int(action[1])
    return (
        e >= 0
        and q >= 0
        and e % config.action_grid == 0
        and q % config.action_grid == 0
        and e + q <= available_surplus(state)
    )


def terminal_reward(state: State, config: EnvironmentConfig) -> float:
    return (
        config.eta_goal * float(state.goal >= config.goal_target)
        + config.eta_emergency * float(state.reserve >= config.reserve_target)
        + config.eta_wallet * float(state.wallet)
    )


def transition_from_outcome(
    state: State,
    action: Action,
    expense: int,
    next_salary: int | None,
    config: EnvironmentConfig,
) -> Transition:
    """Apply one action to one fixed exogenous outcome."""

    if state.t >= config.horizon:
        raise ValueError("Cannot transition from a terminal state")
    if not is_valid_action(state, action, config):
        raise ValueError(f"Invalid action {action} for state {state}")

    e, q = int(action[0]), int(action[1])
    surplus = available_surplus(state)
    liquid_after_alloc = surplus - e - q
    variable_expense = max(0, int(expense))
    liquid_covered = min(variable_expense, liquid_after_alloc)
    reserve_draw = min(
        state.reserve + e,
        max(0, variable_expense - liquid_after_alloc),
    )
    variable_shortfall = max(
        0,
        variable_expense - liquid_after_alloc - (state.reserve + e),
    )
    essential_shortfall = fixed_shortfall(state) + variable_shortfall
    next_wallet = max(0, liquid_after_alloc - variable_expense)
    next_reserve = state.reserve + e - reserve_draw
    next_goal = state.goal + q
    next_t = state.t + 1
    next_deadline = max(0, state.deadline - 1)
    if next_t < config.horizon:
        if next_salary is None:
            raise ValueError("A next salary is required before the terminal cycle")
        next_state = State(
            t=next_t,
            wallet=next_wallet,
            reserve=next_reserve,
            goal=next_goal,
            deadline=next_deadline,
            salary=int(next_salary),
            fixed=config.fixed_obligation,
        )
    else:
        next_state = State(
            t=next_t,
            wallet=next_wallet,
            reserve=next_reserve,
            goal=next_goal,
            deadline=next_deadline,
            salary=0,
            fixed=0,
        )

    coverage = liquid_covered + reserve_draw
    delta_reserve = (
        min(next_reserve, config.reserve_target)
        - min(state.reserve, config.reserve_target)
    )
    step_reward = (
        config.eta_consumption * float(np.log1p(coverage))
        - config.shortfall_penalty * float(essential_shortfall)
        + config.eta_reserve * float(delta_reserve)
    )
    terminal = terminal_reward(next_state, config) if next_t >= config.horizon else 0.0
    info: dict[str, Any] = {
        "expense": variable_expense,
        "salary": state.salary,
        "fixed": state.fixed,
        "fixed_shortfall": fixed_shortfall(state),
        "surplus": surplus,
        "emergency_allocation": e,
        "goal_allocation": q,
        "liquid_after_alloc": liquid_after_alloc,
        "liquid_covered": liquid_covered,
        "reserve_draw": reserve_draw,
        "coverage": coverage,
        "variable_shortfall": variable_shortfall,
        "shortfall": essential_shortfall,
        "delta_reserve": delta_reserve,
        "step_reward": step_reward,
        "terminal_reward": terminal,
        "reward": step_reward + terminal,
    }
    return Transition(next_state, step_reward, terminal, info)


def transition_outcomes(
    state: State,
    action: Action,
    task: TaskType,
    config: EnvironmentConfig,
) -> tuple[tuple[float, Transition], ...]:
    """Enumerate P(s', h | s, a) for the finite-support simulator."""

    expense_outcomes = task.expense_outcomes()
    salary_outcomes = task.salary_outcomes() if state.t + 1 < config.horizon else ((0, 1.0),)
    outcomes: list[tuple[float, Transition]] = []
    for expense, expense_probability in expense_outcomes:
        for next_salary, salary_probability in salary_outcomes:
            transition = transition_from_outcome(
                state,
                action,
                expense,
                next_salary if state.t + 1 < config.horizon else None,
                config,
            )
            outcomes.append((expense_probability * salary_probability, transition))
    return tuple(outcomes)


def sample_trajectory(
    task: TaskType,
    config: EnvironmentConfig,
    rng: np.random.Generator,
) -> Trajectory:
    salaries = tuple(task.sample_salary(rng) for _ in range(config.horizon))
    expenses = tuple(task.sample_expense(rng) for _ in range(config.horizon))
    return Trajectory(salaries=salaries, expenses=expenses)


class GoalAllocationEnv:
    """Small environment with optional matched-evaluation trajectories."""

    def __init__(
        self,
        task: TaskType,
        config: EnvironmentConfig | None = None,
        seed: int | None = None,
    ) -> None:
        self.config = config or EnvironmentConfig()
        self.task = task
        self.rng = np.random.default_rng(seed)
        self.trajectory: Trajectory | None = None
        self.state: State | None = None
        self.done = True
        self.total_reward = 0.0
        self.shortfall_total = 0

    def reset(
        self,
        task: TaskType | None = None,
        seed: int | None = None,
        trajectory: Trajectory | None = None,
    ) -> State:
        if task is not None:
            self.task = task
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        if trajectory is not None and len(trajectory.salaries) != self.config.horizon:
            raise ValueError("trajectory length must equal config.horizon")
        self.trajectory = trajectory
        salary = (
            trajectory.salaries[0]
            if trajectory is not None
            else self.task.sample_salary(self.rng)
        )
        self.state = State(
            t=0,
            wallet=self.config.initial_wallet,
            reserve=self.config.initial_reserve,
            goal=self.config.initial_goal,
            deadline=self.config.deadline,
            salary=int(salary),
            fixed=self.config.fixed_obligation,
        )
        self.done = False
        self.total_reward = 0.0
        self.shortfall_total = 0
        return self.state

    def step(self, action: Action) -> tuple[State, float, bool, dict[str, Any]]:
        if self.done or self.state is None:
            raise RuntimeError("Call reset() before step()")
        current = self.state
        if self.trajectory is not None:
            expense = self.trajectory.expenses[current.t]
            next_salary = (
                self.trajectory.salaries[current.t + 1]
                if current.t + 1 < self.config.horizon
                else None
            )
        else:
            expense = self.task.sample_expense(self.rng)
            next_salary = (
                self.task.sample_salary(self.rng)
                if current.t + 1 < self.config.horizon
                else None
            )
        transition = transition_from_outcome(
            current,
            action,
            expense,
            next_salary,
            self.config,
        )
        self.state = transition.next_state
        self.done = self.state.t >= self.config.horizon
        self.total_reward += transition.step_reward + transition.terminal_reward
        self.shortfall_total += int(transition.info["shortfall"])
        info = dict(transition.info)
        info["done"] = self.done
        info["total_reward"] = self.total_reward
        return self.state, transition.step_reward + transition.terminal_reward, self.done, info
