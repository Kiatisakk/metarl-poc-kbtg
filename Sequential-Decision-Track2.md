# Track 2 follow-up: the smallest real sequential decision

**Decision:** Start with a **six-payday extra-repayment versus cash-buffer problem**, narrowed from candidate 4 in the [earlier analysis](Research-and-Pitch-Direction.md). It has a real delayed effect: an extra debt payment reduces later interest but removes liquidity that may be needed after an uncertain expense. A small **finite-horizon dynamic program (DP)** is the main method to test. Reinforcement learning (RL) and Meta-RL are conditional research extensions, not required components. The second serious candidate is a **two-goal buy-or-defer problem**, narrowed from candidate 6. It maps more directly to the supplied goal-wealth papers but needs user utility assumptions that are hard to validate.

The [booklet](Booklet.md) asks for a K PLUS solution that helps first jobbers aged 22–30 manage daily finances/savings and/or financial risks, connected to the selected track. Track 2 is about data/analytics/intelligence improving financial decisions. It does not require DP, RL, or Meta-RL. All target-user incidence and product-value claims below are hypotheses until tested with Thai K PLUS users.

The accompanying [primary-source method audit](Research-Methods-Sources.md) records PDF page references for the DP, Meta-RL, young-adult modeling, and liquidity claims used here.

## 1. Revisit the six concepts by decision structure

| Earlier concept | Does today's action change tomorrow's feasible state? | Verdict for DP/RL |
|---|---|---|
| **1. Bill-Safe Check** | The user's payment changes cash, but the proposed *feature* simply calculates a threshold once before the payment; it does not choose a sequence of actions. | Keep as a Track 1 flow. Adding RL to the warning rule is unjustified. |
| **2. Payday Safe Save** | A transfer from spending cash to an accessible pocket changes labels but not total liquid wealth. If spending is independent of the label and withdrawals are free, depositing now versus later has the same attainable terminal outcomes. | **Conditional only.** It becomes sequential if commitment, withdrawal cost, different returns, or spending response is real and measured. The REF does not prove those effects for K PLUS users. |
| **3. Missed-Goal Reset** | A one-time edit to amount or deadline changes a plan. | Mainly a product interaction unless repeated decisions and their consequences are specified. The archive does not substantiate a real-user “abandonment effect.” |
| **4. Repay Costliest Debt** | An extra repayment irreversibly reduces principal and future interest while using cash that could absorb later shocks. | **Strong.** Reduce to *how much extra to repay versus retain as liquid buffer* over six paydays. Two debts are not needed for the core problem. |
| **5. Reason-Specific Transfer Pause** | Repeated warnings might cause habituation, so intervention timing could be sequential. | Theoretically interesting, but needs trustworthy scam labels and a model of user response; the supplied lab warning study does not provide these. It is more naturally Track 3. |
| **6. Two-Goal Trade-off Card** | An optional purchase at an earlier deadline cannot be undone and changes whether a later goal can be reached. | **Strong if reframed** as *buy the near-term goal now or preserve cash for the later goal*, not a progress dashboard. |

The source distinction matters. [Das et al.'s multi-goal DP paper](ref/MultWealthGoals.pdf) optimizes whether to **fulfill** goals when they arise, plus a portfolio choice, rather than proving that labeling cash into goals changes behavior. The [young-adult Swedish thesis](ref/FULLTEXT01.pdf) simulates allocation trade-offs and explicitly calls for empirical validation. [Chak et al.](ref/Chak_DAcunto_2023_Improving_Household_Debt_Robo_Advice_w30616.pdf) experimentally studied loan repayment advice in UK adults; its results concern hypothetical repayment tasks, not actual K PLUS debt reduction.

## 2. Candidate A — one debt, extra repayment, and a cash buffer

### The smallest meaningful K PLUS decision

At each of **six monthly paydays**, a first jobber with one revolving debt decides how much *extra* to repay after the required minimum and known bills. Repaying more today saves future interest; keeping cash helps cover variable essentials before the next payday. K PLUS could show two or three feasible repayment choices and their modeled debt-versus-shortfall trade-off, with the user choosing and authorizing any payment. The simulator evaluates a policy that chooses the amount; it does **not** assume the user will follow advice in a real app.

The proposed segment is first jobbers with a revolving balance and limited liquid buffer. Its prevalence among K PLUS users is **not established** by the REF. The practical inspiration is the loan-allocation experiment in [Chak et al.](ref/Chak_DAcunto_2023_Improving_Household_Debt_Robo_Advice_w30616.pdf) and the liquidity-buffer logic in [Deaton](ref/Deaton_1991_Saving_and_Liquidity_Constraints_w3196.pdf). This is a different, narrower problem from Chak et al.'s multiple-loan allocation task, so their measured effect cannot be transplanted to it.

The **user value to test** is lower debt cost without more episodes of cash shortage. The **K PLUS value hypothesis** is a more useful repayment decision in its daily banking flow, potentially improving trust and engagement; no retention or revenue effect is established. The narrow proposed experience is an optional amount suggestion at the extra-repayment moment, with an explanation of the modeled interest-versus-buffer trade-off.

### Finite-horizon model

Use normalized currency units in the prototype. Let $t=0,\ldots,T-1$, with $T=6$ pay cycles. A decision occurs just after salary arrives and the current known bills and minimum debt payment have been covered. Assume for this **controlled model** that extra repayment is allowed without a fee, the revolving monthly rate is known, and the decision maker observes current cash and debt exactly. Conditional on time and user type, shocks are independent of earlier history; if that fails, an observed income/expense regime must be added to the state. A real contract would need to replace these assumptions before any actual recommendation.

| Element | Definition |
|---|---|
| **State $S_t$** | $(t,c_t,d_t)$: cycle index, liquid cash, outstanding revolving balance. Known next-cycle bill $B_{t+1}$, required minimum $m_{t+1}$, and interest $r_t$ are calendar/contract parameters. A belief about an unknown user type is added only in an adaptation experiment. |
| **Action $A_t$** | Extra repayment $a_t\in\{0,\Delta,2\Delta,\ldots\}$, bounded by $0\le a_t\le\min(c_t,d_t)$. Keep this to three or four amounts in the first prototype. |
| **Exogenous transition** | Variable essential spending $X_t$ and next net salary $Y_{t+1}$ are drawn from a declared scenario distribution $P_\theta(X,Y\mid t)$. One missed-payday or expense-shock state is enough; no full economy model. |
| **Controlled transition** | Debt before next minimum: $\hat d=(d_t-a_t)(1+r_t)$; next minimum: $\mu=\min(m_{t+1},\hat d)$. Provisional cash: $\ell=c_t-a_t-X_t+Y_{t+1}-B_{t+1}-\mu$. Shortfall $q_t=[-\ell]_+$. Then $c_{t+1}=[\ell]_+$, $d_{t+1}=\hat d-\mu$. |
| **Reward/cost** | Terminal $R_T=c_T-d_T$ (higher net cash after debt is better); step cost $\kappa q_t$, where $\kappa$ is an explicit, sensitivity-tested cost of externally resolving a cash shortfall. Track $1(q_t>0)$ separately. |
| **Constraints** | The extra payment cannot exceed cash or debt. Required minimums and bills occur before the next decision. An optional risk requirement is $P_\pi(\exists t:q_t>0)\le\alpha$, with $\alpha$ chosen as a scenario parameter, not asserted as a bank policy. |
| **Objective** | Choose a policy $\pi$ to maximize $J(\pi)=E_\pi[c_T-d_T-\kappa\sum_{t=0}^{T-1}q_t]$, or report the Pareto frontier between expected terminal net cash and shortfall probability rather than hiding that trade-off in one weight. |

Here $[x]_+=\max(x,0)$. The simulator assumes an external fallback resolves a cash shortfall at cost $\kappa q_t$, with $\kappa\ge1$ covering the missing cash plus any disruption; it does **not** claim a specific real credit facility exists. If that abstraction drives the result, run sensitivity tests or replace it with an absorbing failure state. Money is not invested, and there is no automatic borrowing product in scope.

Writing $F(s,a,x,y)=(s',q)$ for the deterministic update makes the stochastic transition explicit:

$$
P_\theta(s',q\mid s,a)=\sum_{x,y}P_\theta(x,y\mid t)\,\mathbf 1\{F(s,a,x,y)=(s',q)\},
\qquad R(s,a,s',q)=-\kappa q.
$$

The next *decision* state is $s'=(t+1,c',d')$; realized $q$ is recorded for reward and risk evaluation. For an unobserved but persistent user type $\theta$, a Bayesian alternative adds belief $b_t(\theta)$ to the state and updates it from observed cash flow. That is a partially observed problem, not an ordinary MDP over only $(t,c,d)$.

For a known transition distribution, discretize $c,d,a,X,Y$ and solve the Bellman recursion:

$$
V_T(c,d)=c-d,\qquad
V_t(c,d)=\max_{a\in A(c,d)}\mathbb E_{X,Y\sim P_\theta}\left[-\kappa q_t+V_{t+1}(c',d')\right].
$$

The separate chance constraint can be handled in a student prototype by scanning a shortfall penalty (a Lagrangian), evaluating each resulting policy on held-out paths, and presenting feasible/non-dominated policies. Do not describe a penalty sweep as an exact guarantee of the risk bound.

### DP, RL, and Meta-RL fit

| Method | Why it fits | Why it might not | State, action, transition, reward, constraints, objective |
|---|---|---|---|
| **DP — primary** | Small finite state/action space; known interest and bills; uncertainty can be represented by a few shock outcomes. It makes delayed interest and liquidity costs explicit and produces an inspectable policy table. | Requires a reasonably specified $P_\theta(X,Y)$, a discretization, and defensible shortfall preference/constraint. State explosion is possible if many debts, daily decisions, and multiple goals are added. | Exactly the $S,A,P,R$, constraints, and $J$ above. For a user with known $\theta$, backward induction solves the six-cycle problem. |
| **RL — conditional** | If the transition distribution is unknown but repeated simulated transitions are available, an RL policy can learn how action values evolve. An empirical transition model followed by DP is the simplest model-based version; finite-horizon tabular Q-learning is a clear model-free comparator. | In a small known simulator, RL usually buys no capability over DP and introduces sample/computation cost. Offline bank data are unavailable; model-free RL on a few real cycles would be unjustified. | Same $S,A,R$ and constraints. A learned model or value/policy approximates decisions under the unknown transition. It must be compared with **estimated-model DP using the same data**, not only with an oracle. |
| **Meta-RL — stretch only** | Suppose users differ in an *unobserved, persistent* income/expense-shock pattern $\theta_u$. A recurrent policy could use the first one or two observed cycles to adapt later extra repayments on a new user. | If $\theta_u$ is known from user entries, or can be estimated from passive history and plugged into DP, ordinary personalized/Bayesian DP is simpler. Six cycles offer little adaptation data. Synthetic user-type gains do not establish real-world personalization. | Augment effective state with history $h_t=(X_{<t},Y_{\le t})$ or belief $b_t(\theta)$; actions and physical transitions remain as above. Reward/constraints are unchanged. Train across simulated user types and evaluate adaptation on held-out types with identical observed histories for all methods. |

**Meta-RL is a testable hypothesis, not the product mechanism.** The supplied [Das et al. Meta-RL paper](ref/2605.02300v1.pdf) is mainly evidence that pre-training across many modeled wealth-goal problems can amortize the cost of a new optimization problem; its reported 97.8% utility ratio is relative to DP in simulations. Its test uses a pretrained, zero-shot policy on new modeled problems, not within-user learning of hidden preferences or spending dynamics ([page-level audit](Research-Methods-Sources.md)). That stronger adaptation claim would need the held-out-user experiment described below. In this proposed debt environment, income and spending observations arrive whether or not the policy explores, so a simple estimator plus DP is a particularly strong alternative to Meta-RL.

### Baseline to advanced progression

1. **Simple baselines:** after bills/minimums, repay all cash above a fixed reserve $L$, capped by debt. Also test a stronger horizon-aware reserve rule using expected upcoming essentials plus a safety margin, and include “pay minimum only” as a sanity reference. Tune rules on training paths only.
2. **Known-model DP (oracle ceiling):** solve the finite-horizon model using the simulator's true shock distribution. This asks whether sequential optimization can matter *in principle*.
3. **Estimated-model DP (realistic comparison):** estimate shock probabilities from a short synthetic history, then solve the same DP. This asks whether the oracle gain survives model error.
4. **RL only if needed:** train with the same simulated interaction budget and compare with estimated-model DP. Prefer the simpler method if outcome differences are negligible.
5. **Meta-RL only if heterogeneity is central:** train across user-type distributions and compare to pooled DP, posterior/plug-in personalized DP, and a type-aware oracle DP on unseen users. A recurrent policy must beat the simpler personalized methods with equal history and under multiple held-out distributions to justify its complexity.

### Realistic experiment, required data, and risks

Use a **Python notebook or small script**, not a bank integration. Choose a transparent synthetic environment: six pay cycles; discrete cash/debt grids; one known debt interest rate and minimum payment; one fixed bill; three extra-payment amounts; and low/medium/high essential-spending shocks. Define two or three **illustrative** user types with different shock volatility or salary stability, and vary parameters in sensitivity tests. Do not present synthetic parameter choices as Thai population estimates.

Run all policies on paired held-out random paths. Report mean terminal net cash after debt, probability/amount of a shortfall, frequency of debt payoff, and compute/training cost with uncertainty intervals. In the deterministic case, check that DP and the obvious early-repayment rule agree. In high-uncertainty cases, check whether DP retains cash and whether that reduces shortfalls without excessive interest cost. If a tuned reserve rule matches estimated-model DP across plausible scenarios, that **falsifies the need for DP in the pitch**. Do not tune reserve or model parameters on the held-out paths.

**Required real data for a future K PLUS deployment:** balance, debt balance/APR/minimum and prepayment terms, known obligations, and consent to use relevant transaction history. The student prototype needs none of these; all inputs are simulated. The largest risk is **simulator validity**: a sophisticated policy can optimize assumed shock frequencies, shortfall cost, and repayment behavior rather than real welfare. Other risks are coarse currency grids, rare events, missing outside debts/bills, policy recommendations being ignored, and a user's changing circumstances. The controlled experiment tests an algorithmic proposition, not a field outcome or personalized financial advice.

## 3. Candidate B — two goal opportunities, buy or defer

### The smallest meaningful decision

Reframe the earlier “Two-Goal Trade-off Card” as **two optional purchases at different dates**: a nearer goal becomes purchasable at month $\tau_1$; a more important/larger goal is due at month $\tau_2>\tau_1$. At $\tau_1$, should the user make the first purchase, knowing uncertain income and essential spending may prevent the later one? The advice is a transparent trade-off; K PLUS does not autonomously buy anything. This is close to the actual *fulfill/forgo goal* decision modeled by [Das et al.](ref/MultWealthGoals.pdf). It is not the full investment/portfolio problem in that paper.

The **target hypothesis** is a first jobber with a modest liquid balance, one near-term optional purchase, and a later valued goal. The **user value to test** is making that purchase decision with a quantified risk to the later goal and essential cash. The **K PLUS value hypothesis** is deeper use of its existing goal-planning experience; again, engagement and trust are not measured by the REF.

### Finite-horizon model

| Element | Definition |
|---|---|
| **Horizon / state** | $T=6$ monthly cycles; $S_t=(t,c_t,z_{1,t},z_{2,t})$, where $c_t$ is cash and $z_j\in\{0,1\}$ records whether optional goal $j$ was purchased. Dates $\tau_j$, prices $C_j$, and user-stated utilities $u_j$ are parameters. |
| **Action** | At a goal's opportunity date, $a_t\in\{\text{buy},\text{skip}\}$; otherwise wait. Buy only if the price is available and cash after the purchase stays nonnegative. A “defer” action is added only if that goal truly remains purchasable later. |
| **Transition** | Provisional cash is $\ell_t=c_t-C_j1(a_t=\text{buy})+Y_{t+1}-X_t-B_{t+1}$. Record shortfall $q_t=[-\ell_t]_+$; next cash is $c_{t+1}=[\ell_t]_+$. Purchased-goal indicator $z_j$ flips to one and cannot be reversed. $P_\theta(Y,X)$ describes the uncertain cash flow. |
| **Reward / constraints** | Receive $u_j$ when goal $j$ is bought, retain terminal cash value $v(c_T)$, and penalize or constrain essential-cash shortfalls. The action cannot spend money absent at the decision time; an optional risk bound limits the probability of a future shortfall. |
| **Objective** | Maximize $E[\sum_j u_j z_{j,T}+v(c_T)-\lambda\sum_t q_t]$, with sensitivity over $u_j,v,\lambda$. Goal utility is *elicited preference*, not observed financial return. |

Formally, if $F_B(s,a,x,y)=(s',q)$ is the cash-and-goal update, then $P_\theta(s',q\mid s,a)=\sum_{x,y}P_\theta(x,y\mid t)\mathbf 1\{F_B(s,a,x,y)=(s',q)\}$. The step reward is $R_B(s,a,s',q)=u_j1(a=\text{buy})-\lambda q$ at a goal opportunity, plus terminal $v(c_T)$. The simulator again assumes a shortfall is externally resolved at the stated cost; an absorbing failure state is an alternative.

**DP:** natural and easy to solve by backward induction over a small cash grid, assuming known goal dates/prices/utilities and a specified cash-flow kernel. **RL:** potentially useful only if the income/expense kernel is unknown and enough simulated episodes are available; a learned transition model plus DP is a stronger first comparison than a complex policy network. With two purchase events and a known simulator, RL is mostly overhead. **Meta-RL:** pre-training across different goal prices/deadlines/preferences could give a fast generalized policy, but the inputs are normally known or can be asked directly. Two purchases provide little within-user feedback to infer hidden preferences, and ordinary conditioning on stated preferences would suffice. The supplied [Meta-RL goal paper](ref/2605.02300v1.pdf) demonstrates simulated cross-problem generalization, not that online preference inference is necessary here.

**Baseline:** “always buy the nearer affordable goal” versus “reserve the cash for the later goal.” **Advanced:** DP with uncertainty. **Experiment:** compare goal-attainment rates, essential-cash shortfalls, and declared-utility totals on paired paths while varying the two goals' relative values and income volatility. An advanced method adds value only if it changes decisions in interpretable boundary cases, improves declared utility without breaking the risk constraint, and remains robust to reasonable preference uncertainty.

**Biggest risks:** User values $u_1,u_2$ are subjective, may change, and can drive the answer more than the optimizer. Treating the purchase as irreversible is a design assumption. If the advice is just “show the date moved,” it returns to a dashboard. A student can prototype this in simulation, but it has less direct daily-banking value than the debt/buffer choice and more overlap with K PLUS goal planning.

## 4. Why a tempting third candidate collapses

The earlier **Payday Safe Save** sounds like a sequential allocation problem. In a minimal model with cash $c_t$, accessible goal balance $g_t$, transfer $a_t$, and exogenous income/spending $Y_t,X_t$:

$$
c_{t+1}=c_t-a_t+Y_t-X_t,\quad g_{t+1}=g_t+a_t,\quad
c_{t+1}+g_{t+1}=c_t+g_t+Y_t-X_t.
$$

If users can reverse the transfer freely and spending/returns do not depend on which pocket holds the money, choosing $a_t$ changes **no feasible future consumption or terminal total wealth**. DP/RL over transfer timing then learns an arbitrary label policy. It becomes substantive only with a real commitment effect, withdrawal friction, different interest, or a measured behavior change when the spending balance shrinks. Neither the supplied REF nor the prior product audit proves such an effect in K PLUS. Therefore this is **not selected** for the core technical project. This invariance check is a useful way to avoid a fake optimization problem.

## 5. Research questions, scope, and final choice

### Precise questions for Candidate A

1. Under the same shortfall-risk limit, does six-cycle DP lower expected terminal net debt relative to the best tuned fixed-reserve repayment rule on held-out synthetic cash-flow paths?
2. How much of the oracle DP advantage remains when next-cycle income/expense probabilities are estimated from a short history or shifted at test time?
3. **Optional Meta-RL question:** Across held-out simulated user types, does a history-adaptive policy outperform pooled and posterior/plug-in DP policies given the same first two cycles of observations? If not, omit Meta-RL.

### Strict build scope

**MUST HAVE:** One revolving debt, one liquid account, six monthly decisions, one fixed obligation, one stochastic essential-expense/income process, three or four extra-payment actions, terminal net-cash and shortfall measures, a fixed-reserve baseline, discretized DP, and paired held-out simulation. A table/plot of the policy frontier is enough; no app UI is necessary.

**OPTIONAL:** Estimate the transition from short histories; compare model-based RL on equal data; test two or three user types and a Bayesian/Meta-RL adaptation comparison. Add one additional debt only if the one-debt result is already validated and the second changes the optimal decision.

**OUT OF SCOPE:** Real banking integration, production architecture, cross-bank aggregation, loan origination, a full financial ecosystem, investment portfolios, fraud classification, LLM coaching, complex frontends/backends, and claims of real-world performance from synthetic data.

### Choice

Candidate A is the **richest technical problem that still fits a small student project**. Its action has a real future consequence through interest; the buffer creates a concrete competing objective; uncertainty matters; and a policy can be evaluated against strong simple baselines. Candidate B is the closest conceptual match to the supplied goal DP/Meta-RL papers, but its answer depends on subjective goal utilities and offers fewer repeated decisions. The proposed Track 2 story is therefore **“choose an extra repayment amount over the next six pay cycles while preserving liquidity,” solved and stress-tested with DP**. Add RL or Meta-RL only if controlled comparisons reveal an actual need for model learning or fast adaptation across users.

### Primary sources and prior product check

- [Official hackathon booklet](Booklet.md) and [previous candidate analysis](Research-and-Pitch-Direction.md).
- [Deaton, *Saving and Liquidity Constraints*](ref/Deaton_1991_Saving_and_Liquidity_Constraints_w3196.pdf): buffer-stock logic is assumption-dependent.
- [Chak et al., *Improving Household Debt Management with Robo-Advice*](ref/Chak_DAcunto_2023_Improving_Household_Debt_Robo_Advice_w30616.pdf): experimental evidence that repayment advice can help with hypothetical allocations, with uptake and trust caveats.
- [Das et al., *Dynamic Optimization for Multi-Goals Wealth Management*](ref/MultWealthGoals.pdf) and [Das et al., *A Meta Reinforcement Learning Approach to Goals-Based Wealth Management*](ref/2605.02300v1.pdf): formal multi-goal decision methods and simulation comparisons, not proof of Thai user benefit.
- [Krohné & Pagrotsky, *Dynamic Optimization of Individual Financial Well-Being*](ref/FULLTEXT01.pdf): simulated young-adult buffer-versus-goal allocation and explicit need for empirical validation.
- [K PLUS official features](https://www.kasikornbank.com/en/kplus): publicly describes loan/asset overview and money-management tools; inspect the current repayment flow before claiming a product gap.
