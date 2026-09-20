from __future__ import annotations

import math
import unittest

from goal_policy.dp import KnownModelDP
from goal_policy.environment import (
    EnvironmentConfig,
    GoalAllocationEnv,
    State,
    TaskType,
    Trajectory,
    is_valid_action,
)
from goal_policy.evaluation import evaluate_policies
from goal_policy.policies import BayesianDPPolicy, FixedSplitPolicy
from goal_policy.rl import PooledQPolicy, RecurrentMetaPolicy


class GoalPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = EnvironmentConfig(horizon=2, action_grid=10, max_action_cash=100)
        self.task = TaskType(
            "deterministic",
            salary_mean=100,
            salary_sd=0,
            expense_mean=20,
            expense_sd=0,
            shock_probability=0,
            shock_size=0,
        )

    def test_transition_updates_all_balances(self) -> None:
        env = GoalAllocationEnv(self.task, self.config)
        state = env.reset(
            trajectory=Trajectory(salaries=(100, 100), expenses=(20, 20))
        )
        next_state, _, done, info = env.step((10, 10))
        self.assertFalse(done)
        self.assertEqual(next_state.wallet, 40)
        self.assertEqual(next_state.reserve, 30)
        self.assertEqual(next_state.goal, 10)
        self.assertEqual(info["shortfall"], 0)
        self.assertEqual(info["coverage"], 20)

    def test_invalid_action_is_rejected(self) -> None:
        env = GoalAllocationEnv(self.task, self.config)
        state = env.reset(
            trajectory=Trajectory(salaries=(100, 100), expenses=(20, 20))
        )
        self.assertFalse(is_valid_action(state, (90, 0), self.config))
        with self.assertRaises(ValueError):
            env.step((90, 0))

    def test_dp_returns_a_feasible_finite_action(self) -> None:
        env = GoalAllocationEnv(self.task, self.config)
        state = env.reset(
            trajectory=Trajectory(salaries=(100, 100), expenses=(20, 20))
        )
        model = KnownModelDP(self.task, self.config, balance_bin=10, action_grid=10)
        value = model.value(state)
        action = model.action(state)
        self.assertTrue(math.isfinite(value))
        self.assertTrue(is_valid_action(state, action, self.config))

    def test_bayesian_policy_responds_to_a_shock_observation(self) -> None:
        stable = TaskType(
            "stable",
            salary_mean=100,
            salary_sd=0,
            expense_mean=20,
            expense_sd=0,
            shock_probability=0,
            shock_size=0,
        )
        shock = TaskType(
            "shock",
            salary_mean=100,
            salary_sd=0,
            expense_mean=20,
            expense_sd=0,
            shock_probability=1,
            shock_size=100,
        )
        models = {
            task.name: KnownModelDP(task, self.config, balance_bin=10, action_grid=10)
            for task in (stable, shock)
        }
        policy = BayesianDPPolicy(models, (stable, shock))
        state = State(0, 40, 20, 0, 2, 100, 60)
        policy.reset(state)
        policy.observe({"expense": 120}, state)
        self.assertGreater(policy.posterior["shock"], policy.posterior["stable"])

    def test_short_rl_and_meta_training_runs(self) -> None:
        tasks = (self.task, TaskType("volatile", 100, 10, 20, 5, 0.2, 50))
        q_policy = PooledQPolicy(tasks, self.config, seed=1)
        q_policy.train(episodes=3, seed=1)
        meta_policy = RecurrentMetaPolicy(
            tasks,
            self.config,
            seed=1,
            hidden_size=4,
        )
        meta_policy.train(episodes=2, seed=2)
        state = GoalAllocationEnv(self.task, self.config, seed=3).reset()
        for policy in (q_policy, meta_policy):
            policy.reset(state)
            action = policy.act(state)
            self.assertTrue(is_valid_action(state, action, self.config))

    def test_matched_evaluation_returns_each_policy_and_task(self) -> None:
        tasks = (self.task,)
        policies = {
            "fixed": FixedSplitPolicy(self.config),
            "goal": FixedSplitPolicy(self.config, reserve_fraction=0.0, goal_fraction=1.0),
        }
        results = evaluate_policies(
            policies,
            tasks,
            config=self.config,
            episodes_per_task=2,
            seed=4,
        )
        self.assertEqual(len(results), 4)
        self.assertEqual({result.policy for result in results}, {"fixed", "goal"})
        self.assertTrue(all(result.task == "deterministic" for result in results))


if __name__ == "__main__":
    unittest.main()
