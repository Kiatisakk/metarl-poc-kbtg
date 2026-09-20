# User-Adaptive Sequential Goal Management Policy via Meta-Reinforcement Learning

**Experiment proposal — K PLUS First Jobber Hackathon, Track 2: Data Science & Intelligence**

## 1. Decision in one paragraph

This project studies a small sequential decision problem for First Jobbers: over six pay cycles, how should limited surplus cash be allocated between an emergency buffer, one optional savings goal, and immediately spendable cash when future income and essential expenses are uncertain?

The project does not assume that Meta-Reinforcement Learning is necessary. It compares methods in order:

1. A transparent allocation heuristic.
2. Dynamic Programming with a known user-specific transition model.
3. A pooled Reinforcement Learning policy when the transition model is not supplied.
4. A recurrent Meta-RL policy that adapts to an unseen user's cash-flow dynamics from a short history.

If a fixed rule or personalized DP performs as well as Meta-RL, the project will report that result and stop at the simpler method. The technical contribution is the controlled comparison, not the use of the most complex algorithm.

## 2. Why this is a sequential problem

At each payday, allocating more money to the optional goal improves progress toward a future target but leaves less liquid cash for an uncertain expense. Allocating more to the emergency buffer reduces shortfall risk but may delay the optional goal. Keeping money liquid protects near-term flexibility but may make the goal harder to reach.

The action changes the state available at every later payday. This creates:

- changing cash, reserve, and goal balances;
- multiple feasible actions at each cycle;
- uncertain income and expenses;
- a trade-off between current liquidity and delayed goal attainment;
- hard feasibility constraints;
- user-specific dynamics that can be learned from early observations.

This is different from predicting next month's spending or displaying a dashboard. The policy must choose what to do now because the decision changes future options.

## 3. Booklet fit and user value

### Problem

First Jobbers may have several competing uses for a limited first salary: essential expenses, an emergency reserve, and a personal goal. A fixed saving rule can be too aggressive when expenses are volatile and too conservative when cash flow is stable. The specific prevalence of this problem among Thai K PLUS users is a hypothesis to validate; the supplied REF does not provide that prevalence estimate.

### Proposed K PLUS experience

At a salary or planning moment, K PLUS could show an optional allocation recommendation such as:

> “With your current cash flow, allocating ฿X to your goal keeps the reserve above your chosen floor in most simulated scenarios. Allocating more reaches the goal sooner but increases the chance of a shortfall.”

The user chooses whether to act. The prototype is a simulator and policy evaluator; it does not move money, block transactions, or claim production access to K PLUS data.

### Target segment hypothesis

K PLUS users aged 22–30 who receive regular salary income, have a small liquid buffer, and are trying to build one short-term goal while meeting monthly essentials. The prototype uses synthetic users and does not claim that all First Jobbers share this profile.

### User value hypothesis

The policy may help users make a more sustainable allocation by making the trade-off between goal progress and liquidity explicit. The experiment measures financial outcomes in the simulator; it does not claim actual debt reduction, savings behavior change, or welfare improvement in production.

### K PLUS value hypothesis

The feature could make existing saving and budgeting capabilities more useful at a decision point and could support trust in personalized financial guidance. Retention, deposit, revenue, and credit-risk effects are not measured by this proposal and must not be claimed as results.

## 4. Smallest experiment

### Fixed environment

- Horizon: (T=6) monthly pay cycles.
- Accounts: one liquid wallet, one protected emergency buffer, and one optional goal balance.
- Goal: one target amount and one deadline inside or at the end of the horizon.
- Income: salary at the start of each cycle, with user-type-specific variation.
- Essentials: one fixed monthly obligation plus a stochastic variable-expense shock.
- Actions: discrete allocation pairs on a small currency grid.
- Evaluation: held-out simulated cash-flow paths and held-out user types.

The environment is deliberately small. It is enough to test sequential allocation and adaptation without building a complete banking ecosystem.

### Event order in one cycle

At cycle (t):

1. Salary (Y_t) arrives and the fixed obligation (F_t) is paid.
2. The agent observes the available surplus and current wallet, reserve, and goal balances.
3. The agent allocates part of the surplus to the emergency buffer and optional goal; the rest remains liquid.
4. A variable expense (X_t) is drawn from the user's hidden cash-flow type.
5. Variable expense is paid from liquid cash first, then from the emergency buffer. Any remaining amount is a shortfall.
6. The next state and reward are recorded.

The reserve is protected from discretionary spending in the simulator and can be drawn only after the liquid wallet is exhausted. This is a modeling assumption representing a commitment or access friction. It must be made configurable because a real K PLUS product may allow transfers back without friction.

## 5. Mathematical formulation

### 5.1 State

At the decision point of cycle (t), define:

\[
s_t=(t,w_t,r_t,g_t,d_t,y_t,f_t),
\]

where:

- (t\in\{0,\ldots,T-1\}) is the cycle index;
- (w_t) is liquid wallet balance;
- (r_t) is emergency-buffer balance;
- (g_t) is optional-goal balance;
- (d_t) is the number of cycles until the goal deadline;
- (y_t) is current salary;
- (f_t) is the current fixed obligation.

For a tabular DP prototype, balances are discretized into currency bins. For RL, the same values are normalized to ([0,1]). The current salary and fixed obligation can be omitted from the state when they are already included in the available-surplus calculation.

### 5.2 Action

Let the fixed-obligation deficit and available surplus after salary and fixed obligations be:

\[
k_t=[f_t-w_t-y_t]_+,\qquad
m_t=[w_t+y_t-f_t]_+.
\]

The fixed-obligation shortfall $k_t$ is recorded before allocation. The feasible action is $(0,0)$ when $m_t=0$; otherwise:

\[
a_t=(e_t,q_t),
\]

where:

- (e_t) is the amount allocated to the emergency buffer;
- (q_t) is the amount allocated to the optional goal;
- (e_t+q_t\le m_t);
- both amounts lie on a small grid, for example $(0,5,10,\ldots)$ in the simulation units.

The remaining amount $m_t-e_t-q_t$ stays liquid for variable expenses.

### 5.3 Task and user dynamics

Each simulated user task has a hidden parameter:

\[
\theta=(\mu_Y,\sigma_Y,\mu_X,\sigma_X,p_{shock}),
\]

which controls salary variation and variable-expense shocks. The policy observes realized salaries and expenses, but not $\theta$ directly.

The task distribution contains a small number of illustrative types:

1. **Stable cash flow:** low salary and expense variance.
2. **Variable cash flow:** moderate variance.
3. **Shock-prone cash flow:** occasional large expense shocks.

These are experimental task types, not estimates of Thai population segments.

For a reproducible first prototype, use simulation units rather than claiming
Thai currency distributions. One possible starting table is:

| Task | Salary mean / SD | Variable-expense mean / SD | Shock probability / size |
|---|---:|---:|---:|
| Stable | 100 / 5 | 20 / 5 | 0.02 / 40 |
| Variable | 100 / 15 | 25 / 10 | 0.08 / 60 |
| Shock-prone | 100 / 10 | 25 / 12 | 0.20 / 100 |

Use a fixed obligation of 60, an initial wallet of 40, an initial reserve of
20, a goal target of 100, and $R^*=60$ only as transparent defaults. Sweep
these values in sensitivity tests; they are not empirical estimates.
Salary and expense draws must be truncated at zero; a simple truncated normal
or lognormal sampler is sufficient for the simulator.

### 5.4 Transition

After the action, liquid cash available for the variable expense is:

\[
\ell_t=m_t-e_t-q_t.
\]

Draw $X_t\sim P_\theta(X\mid t)$. If $t<T-1$, draw the next salary
$Y_{t+1}\sim P_\theta(Y\mid t+1)$; the next fixed obligation follows the
declared schedule (constant in the MVP). The variable expense first uses
liquid cash:

\[
u_t=\min(X_t,\ell_t).
\]

The emergency-buffer draw is:

\[
v_t=\min\left(r_t+e_t,[X_t-\ell_t]_+\right).
\]

The variable-expense shortfall is:

\[
h^X_t=[X_t-\ell_t-(r_t+e_t)]_+.
\]

The amount of the variable expense that is covered is
$c_t=u_t+v_t=X_t-h^X_t$.

The next balances are:

\[
w_{t+1}=[\ell_t-X_t]_+,\qquad
r_{t+1}=r_t+e_t-v_t,\qquad
g_{t+1}=g_t+q_t.
\]

The total essential-expense shortfall used in the reward and risk metrics is
$h_t=k_t+h^X_t$. The next salary and fixed obligation complete $s_{t+1}$;
they are observed only when the next cycle begins.

The deadline decreases by one cycle. At the deadline, the goal is either achieved or not achieved according to (g_t\ge G^*). A goal purchase is not automatically made by the policy; the simulator measures goal attainment.

The full transition is:

\[
P_\theta(s',h\mid s,a)=
\sum_{x,y'}P_\theta(x,y'\mid s,a)
\mathbf 1\{F(s,a,x,y')=(s',h)\},
\]

where $y'$ denotes the next observed salary and the next fixed obligation is
looked up from the schedule. At the terminal cycle the sum contains only $x$.

### 5.5 Reward

The step reward is:

\[
\rho_t=\eta_c U(c_t)-\lambda_h h_t
      +\eta_r\Delta R_t,
\]

where:

- $U(c_t)$ is a diminishing-returns utility for covered variable expenses;
- $h_t$ is the unmet expense amount;
- $\Delta R_t=\min(r_{t+1},R^*)-\min(r_t,R^*)$ is the useful increase in emergency-buffer coverage;
- $\lambda_h$ is a sensitivity-tested shortfall cost.

At the end of the horizon:

\[
\rho_T=\eta_G\mathbf 1[g_T\ge G^*]
     +\eta_E\mathbf 1[r_T\ge R^*]
     +\eta_W w_T.
\]

The weights $(\eta_G,\eta_E,\eta_W)$ are explicit user or experiment parameters. They are not inferred by Meta-RL in the MVP. If a user can state that the reserve is more important than the optional goal, that preference should be supplied to DP and RL directly. Meta-RL is reserved for adaptation to hidden cash-flow dynamics.

### 5.6 Objective and constraints

The objective is:

\[
J(\pi;\theta)=
\mathbb E_{\pi,P_\theta}
\left[\sum_{t=0}^{T-1}\rho_t+\rho_T\right].
\]

Subject to:

\[
e_t\ge0,\quad q_t\ge0,\quad e_t+q_t\le m_t,
\]

and an experiment-level risk requirement:

\[
\Pr_\pi\left(\exists t:h_t>0\right)\le\alpha.
\]

The chance constraint is evaluated on held-out episodes. A penalty sweep can produce a Pareto frontier, but a penalty value must not be described as a formal guarantee of the risk limit.

## 6. Methods and why each is included

### 6.1 Baseline 1: fixed allocation rule

Use a transparent rule such as:

- fill the emergency reserve until (R^*);
- allocate a fixed fraction of remaining surplus to the optional goal;
- keep the rest liquid.

Tune the fraction and reserve threshold on training episodes only. Include a goal-first and reserve-first rule as simple reference policies.

### 6.2 Baseline 2: known-model Dynamic Programming

When $\theta$, the reward weights, and the transition model are known, solve:

\[
V_T(s)=\rho_T(s),
\]

\[
V_t(s)=\max_{a\in A(s)}
\mathbb E_{s',h\sim P_\theta}
\left[\rho(s,a,s',h)+V_{t+1}(s')\right].
\]

DP is the primary method because the horizon, state grid, and action set are small. It produces an interpretable policy table and an oracle benchmark for methods that do not know the transition model.

Required checks:

- refine the balance grid and confirm that policy values stabilize;
- verify the deterministic special case against direct enumeration;
- report sensitivity to (lambda_h), (R^*), and goal utility;
- test whether the best heuristic closes most of the DP gap.

DP fits because the horizon, state variables, and feasible actions are small
enough for backward induction. Its Markov assumption requires the state to
contain every balance, deadline, and observed income variable that affects the
future. DP is not a good fit if the state must remain high-dimensional,
continuous, or poorly modeled; that is why it is tested before model-free
methods rather than assumed to be the final answer.

### 6.3 Baseline 3: personalized or Bayesian DP

The policy does not observe $\theta$, but it maintains a posterior $b_t(\theta)$ after each observed salary and expense shock. The belief becomes part of the state:

\[
\tilde{s}_t=(s_t,b_t).
\]

The posterior is updated using Bayes' rule and the next action is selected by DP under the posterior predictive transition. This is the strongest low-complexity adaptation baseline. Meta-RL must beat this method to justify its use.

### 6.4 Baseline 4: pooled RL

Train a policy on a mixture of task types without recurrence or task inference. Its observation is the current state only. Use a small discrete-action actor-critic or PPO implementation. The purpose is to test whether model-free learning helps when the transition model is not provided.

Pooled RL is not expected to beat known-model DP in the small oracle setting. Its relevant comparison is estimated-model DP or Bayesian DP when the task distribution is unknown.

RL fits when the transition law is not trusted or is too costly to enumerate:
the policy can learn from complete episodes and optimize delayed reward. It may
be unnecessary here if a compact simulator makes DP exact, and it may be
unstable with too few episodes. The same state, action grid, reward, and
constraints are therefore used so that a performance difference is about
decision learning rather than a larger problem definition.

### 6.5 Main method: Meta-RL with recurrent context

Train one recurrent policy across a distribution of tasks. The hidden recurrent
context summarizes the user's observed cash-flow history:

\[
z_t=\operatorname{GRU}_\psi
\left(z_{t-1},[s_t,a_{t-1},\rho_{t-1},y_t,X_{t-1}]
\right),
\]

\[
a_t\sim\pi_\phi(a_t\mid s_t,z_t).
\]

The policy receives no explicit $\theta$. During evaluation on unseen task dynamics, the GRU state is updated from the first cycles without gradient updates or retraining. This is the only sense in which the policy is “user-adaptive.” It adapts to observed cash-flow dynamics, not to an unobserved moral judgment about how important the user's goal should be.

Use a small recurrent PPO or recurrent actor-critic implementation. Keep the action space discrete so that it matches DP exactly. If recurrent PPO is too large for the team, a tabular recurrent Q-learning prototype is acceptable as a method test; the comparison must still use the same environment and evaluation seeds.

Meta-RL fits only when the task dynamics are hidden at test time but leave
observable clues in the first cycles. It does not fit if the task type is
already supplied, if there is no persistent cross-user heterogeneity, or if a
simple Bayesian belief state is equally effective. The experiment therefore
treats Meta-RL as a falsifiable extension of DP, not as a required product
component.

## 7. Meta-RL justification test

Meta-RL is justified only if all of the following are true:

1. User task dynamics differ in a persistent way.
2. The policy observes evidence about those dynamics over time.
3. The dynamics are not fully provided as inputs.
4. A simple posterior or plug-in estimate is a meaningful competitor.
5. The recurrent policy improves held-out performance with the same observation budget.

If task type is given directly to the policy, this becomes conditional RL, not Meta-RL. If user preferences are directly elicited, conditioning DP/RL on those preferences is preferable to trying to infer them from behavior. If the posterior DP matches Meta-RL, the result is that Meta-RL is unnecessary for this problem.

## 8. Experimental protocol

### 8.1 Train/test separation

Generate task parameters from a declared distribution for training. Hold out:

- unseen random seeds for familiar task types;
- interpolation task types between the training types;
- at least one mild distribution shift, such as a higher shock probability or different salary variance.

Do not tune model weights, reserve thresholds, or policy hyperparameters on held-out episodes.

### 8.2 Matched evaluation

Every policy is evaluated on the same pre-generated cash-flow paths. Use at least five random training seeds and enough held-out episodes for stable confidence intervals; a student implementation can begin with 2,000 held-out episodes per task condition and increase this if estimates remain noisy.

Report:

1. expected total reward;
2. optional-goal attainment probability;
3. emergency-buffer target attainment probability;
4. probability of any expense shortfall;
5. average shortfall amount conditional on a shortfall;
6. terminal liquid cash;
7. adaptation gain from the first two cycles to later cycles;
8. compute time and training episodes.

Use paired bootstrap confidence intervals across identical paths. Report per-task-type results, not only a population average.

### 8.3 Primary hypotheses

These are directional hypotheses, not guaranteed percentage targets:

- **H1 — sequential value:** Known-model DP improves the goal/liquidity trade-off over the best fixed allocation rule on held-out paths.
- **H2 — model uncertainty:** Bayesian or estimated-model DP retains part of the known-model advantage when transition probabilities must be inferred from a short history.
- **H3 — adaptation:** Meta-RL improves later-cycle utility or reduces shortfalls on unseen task types compared with pooled RL and Bayesian DP, given the same observed history.
- **H4 — complexity check:** If Meta-RL does not beat Bayesian DP within uncertainty intervals, it should be rejected as unnecessary for the MVP.

### 8.4 Ablation tests

Run the following ablations:

- no task heterogeneity;
- no recurrent history;
- task type supplied explicitly;
- no emergency-buffer action;
- one goal instead of two account objectives;
- lower and higher shock volatility;
- different shortfall penalties;
- finer and coarser DP grids.

These tests reveal whether an apparent Meta-RL gain comes from adaptation, extra capacity, reward scaling, or an artifact of the simulator.

### 8.5 Required data and assumptions

The MVP requires no live K PLUS data. It needs:

- synthetic initial wallet, reserve, and goal balances;
- a declared salary distribution and expense distribution for each task;
- a fixed-obligation schedule;
- one goal target, deadline, and explicit reward-weight setting;
- the action grid, task random seeds, and evaluation paths.

If anonymized aggregate statistics later become available, they can calibrate the
synthetic distributions. They are not required to test the algorithmic question.
No customer identity, raw transaction history, production API, or real-money
movement is part of the experiment.

The main assumptions are that salary and essential expenses are observed at
cycle boundaries, the user can choose whether to follow a recommendation, goal
funds have configurable withdrawal friction, and the simulator is only a model
of the decision problem. The results therefore support method comparison under
declared assumptions, not a claim about real customer outcomes.

## 9. Minimal implementation plan

### Required components

1. `GoalAllocationEnv`: deterministic seeded simulator with the event order above.
2. `heuristics.py`: reserve-first, goal-first, and tuned fixed-split policies.
3. `dp.py`: discretized backward induction with a transition enumerator.
4. `evaluation.py`: common seeds, metrics, confidence intervals, and plots.

Optional method modules:

- `bayesian_dp.py`: posterior over three task types;
- `rl.py`: pooled discrete-action policy;
- `meta_rl.py`: recurrent policy with task-randomized training.

### Suggested implementation order

1. Implement and unit-test the simulator transition.
2. Add a hand-calculated two-cycle example and verify balances.
3. Implement heuristics and exact DP.
4. Run grid-sensitivity and deterministic sanity checks.
5. Add Bayesian or estimated-model DP.
6. Add pooled RL only if model uncertainty is part of the experiment.
7. Add recurrent Meta-RL only after the simpler baselines are working.
8. Run held-out evaluation and ablations.

### Pseudocode

```text
for each training seed:
    train_tasks = sample_task_parameters()

    fit heuristic thresholds on train_tasks
    compute oracle DP policy for each known task type
    fit pooled RL on sampled episodes                  # optional
    fit recurrent Meta-RL across sampled task types     # optional

for each held-out task and shared cash-flow path:
    run every policy from the same initial state
    record reward, goal attainment, reserve, and shortfall

aggregate by task type and policy
bootstrap paired differences
run ablations
apply the complexity gate:
    if Meta-RL does not beat Bayesian DP, omit Meta-RL from the product claim
```

### Implemented artifacts

The proposal is backed by a runnable NumPy implementation in this workspace:

- `goal_policy/environment.py`: task types, seeded simulator, matched
  trajectories, state transitions, rewards, and feasibility checks;
- `goal_policy/policies.py`: fixed split, reserve-first, goal-first, and
  posterior-weighted DP policies;
- `goal_policy/dp.py`: finite-horizon known-model DP and task-aware oracle;
- `goal_policy/rl.py`: pooled tabular Q-learning and a small recurrent
  policy-gradient Meta-RL prototype;
- `goal_policy/evaluation.py`: common paths, episode metrics, summaries, and
  paired bootstrap intervals;
- `run_experiment.py`: command-line experiment runner;
- `run_tests.py`: test runner that always creates unit-test artifacts
  and can refresh experiment artifacts with `--experiment`;
- `tests/test_goal_policy.py`: transition, feasibility, DP, adaptation, RL,
  and matched-evaluation tests.

Run the core checks with:

```text
python -m unittest discover -s tests -v
python run_tests.py
python run_tests.py --experiment --episodes 5
python run_experiment.py --episodes 100
```

The CLI defaults to a balance bin of 20 and DP allocation grid of 20 so the
full comparison is practical on a student laptop. Use
`--dp-balance-bin 1 --dp-action-grid 5` for the finest DP discretization;
runtime grows substantially because the state-action space grows
combinatorially.

A sample run artifact is stored at
`artifacts/experiment_summary.md`, with raw JSON and test output beside it.

## 10. Scope boundaries

### Must have

- one liquid wallet;
- one emergency reserve;
- one optional goal;
- six pay cycles;
- discrete actions;
- three synthetic cash-flow task types;
- fixed-rule baseline;
- exact DP;
- held-out simulation;
- shortfall and goal-attainment metrics.

### Optional

- Bayesian DP adaptation;
- pooled RL;
- recurrent Meta-RL;
- mild distribution shift;
- a simple visual policy map showing which allocation is selected at each state.

### Out of scope

- real K PLUS or bank integration;
- moving or locking real customer funds;
- cross-bank transaction aggregation;
- investment portfolios and market returns;
- credit underwriting or loan origination;
- fraud detection;
- LLM financial coaching;
- automatic financial advice presented as guaranteed or regulated advice;
- claims about Thai prevalence or customer impact from synthetic data;
- production-scale infrastructure;
- a multi-year, multi-goal financial ecosystem.

## 11. Technical risks and mitigations

| Risk | Why it matters | Mitigation |
|---|---|---|
| Simulator misspecification | A policy can optimize an artificial cash-flow distribution. | Vary task distributions, include shifts, publish parameters, and state that results are conditional on the simulator. |
| Fake Meta-RL adaptation | A recurrent policy may use extra capacity without inferring user dynamics. | Compare against Bayesian DP, no-history RL, and a task-type oracle; use identical histories and ablations. |
| Subjective reward weights | Goal importance can dominate the optimizer. | Treat weights as explicit user inputs; run sensitivity and do not claim the model discovers values. |
| Free transfer assumption | If goal funds can be withdrawn freely, allocation may not change behavior. | Parameterize withdrawal friction; show results with zero and positive friction; do not claim commitment effects without evidence. |
| Grid artifacts | DP may look optimal only because of coarse bins. | Run grid-refinement checks and report the action grid. |
| Reward hacking | The policy might preserve the reserve by starving discretionary consumption. | Include consumption utility, report all metrics, and inspect policies qualitatively. |
| Small horizon | Six cycles may not reveal long-run behavior. | Present the horizon as a controlled test of short-run sequential allocation, not lifetime planning. |

## 12. Research questions

1. Can a finite-horizon DP policy improve the goal-attainment versus liquidity-risk frontier over a strong fixed allocation rule when the cash-flow model is known?
2. When the user's cash-flow dynamics are unknown, does history-informed Bayesian DP retain the DP advantage over pooled policies?
3. Across unseen user dynamics, does Meta-RL adapt from a short observed history well enough to outperform Bayesian DP, or is Meta-RL unnecessary for this problem?

## 13. Expected result and decision rule

The project succeeds if it produces an auditable environment, a correct DP solution, strong baselines, and a fair held-out comparison. A Meta-RL win is not required for success.

Use this decision rule:

- If DP does not beat the tuned heuristic, the problem formulation or proposed feature is not compelling.
- If DP beats the heuristic but Bayesian DP matches Meta-RL, use personalized DP as the final Track 2 method.
- If Meta-RL beats both Bayesian DP and pooled RL across held-out task types and remains robust under distribution shift, present Meta-RL as an experimental contribution.
- If a result changes under small reward or simulator assumptions, report the instability and avoid a strong product claim.

## 14. Relationship to the supplied REF

- [Das et al., *Dynamic Optimization for Multi-Goals Wealth Management*](ref/MultWealthGoals.pdf) supports modeling competing goals with dynamic programming and explicit goal utilities. It is a modeled study, not evidence of K PLUS user impact.
- [Das et al., *A Meta Reinforcement Learning Approach to Goals-Based Wealth Management*](ref/2605.02300v1.pdf) reports zero-shot policy inference across simulated wealth-goal problems. It does not demonstrate online inference of one user's hidden preferences from a short history; this proposal tests that stronger claim separately.
- [Krohné & Pagrotsky, *Dynamic Optimization of Individual Financial Well-Being*](ref/FULLTEXT01.pdf) models young-adult buffer, housing, short-term, and long-term saving under uncertainty, but uses stylized assumptions and explicitly requires further empirical validation.
- [Deaton, *Saving and Liquidity Constraints*](ref/Deaton_1991_Saving_and_Liquidity_Constraints_w3196.pdf) motivates a buffer-versus-consumption trade-off under liquidity constraints. It does not prescribe a universal reserve target or prove that an app intervention changes behavior.
- [Chak et al., *Improving Household Debt Management with Robo-Advice*](ref/Chak_DAcunto_2023_Improving_Household_Debt_Robo_Advice_w30616.pdf) shows that automated repayment advice can improve choices in an incentivized UK experiment, while adoption, trust, and real-world transfer remain limitations.

Evidence discipline:

- **FACT:** the cited papers formulate financial allocation or goal-management
  decisions under uncertainty, and some evaluate simulated or incentivized
  interventions.
- **INTERPRETATION:** a short-horizon reserve-versus-goal allocation problem is
  a defensible Track 2 test bed for sequential decision methods.
- **OPPORTUNITY:** K PLUS could test a user-controlled allocation recommendation
  at the payday decision point, subject to product, trust, and user-research
  validation that this proposal does not claim to have completed.

## 15. One-page pitch direction

**Problem Statement:** First Jobbers must divide limited surplus income between an emergency buffer, an optional goal, and immediate needs. A fixed saving rule ignores changing cash-flow risk and can either delay the goal or leave the user exposed to a shortfall.

**Proposed Solution:** K PLUS estimates a user's near-term cash-flow dynamics from observed history and recommends a next-cycle allocation between reserve, goal, and liquid spending. The policy is evaluated as a sequential decision process, with an explanation of the trade-off and user control over the final action.

**Target Users:** Salaried K PLUS users aged 22–30 with a small liquid buffer and one short-term savings goal. This is a validation hypothesis, not a prevalence claim.

**Value Proposition:** Users receive an allocation that accounts for future uncertainty instead of relying on a fixed percentage. K PLUS gains a testable form of personalized financial decision support built on its existing money-management context.

**Track Perspective:** Track 2 is demonstrated through an explicit MDP, DP benchmark, uncertainty-aware adaptation, and a controlled Meta-RL comparison. The final method is selected by held-out evidence; Meta-RL is not included merely to add an AI label.
