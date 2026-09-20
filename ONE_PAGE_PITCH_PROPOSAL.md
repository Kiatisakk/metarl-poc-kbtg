# K PLUS Adaptive Goal Allocation for First Jobbers

**Track 2 — Data Science & Intelligence**

## 1. Problem Statement

First Jobbers with a regular salary often have limited surplus after essential obligations. At each payday they must divide that surplus between immediate liquidity, an emergency buffer, and a short-term personal goal. Future expenses may be uncertain, so a fixed saving percentage can leave too little cash for an essential shock or delay the goal unnecessarily.

The specific failure point is the payday allocation decision: the user must choose an amount before knowing the next variable expense. The choice affects every later cycle because money placed in the goal or reserve is no longer immediately liquid. Existing budgeting tools can show balances or apply fixed rules, but they do not evaluate this sequential trade-off. The prevalence of this problem among K PLUS users is a validation hypothesis; the prototype makes no population claim.

## 2. Proposed Solution

K PLUS Adaptive Goal Allocation provides an optional recommendation at the payday moment. It observes the current wallet, reserve, goal progress, salary, obligations, and recent cash-flow history. It recommends a feasible pair:

- amount to add to the emergency buffer;
- amount to add to one optional savings goal;
- remaining surplus kept liquid.

The recommendation includes a short explanation and a counterfactual, such as how allocating more to the goal changes simulated shortfall risk. The core experiment models six pay cycles with synthetic cash-flow types. It compares fixed rules, Dynamic Programming, Bayesian adaptive DP, pooled RL, and a recurrent Meta-RL policy. The system does not move real funds or connect to production K PLUS data.

## 3. Target Users

The initial target segment is salaried K PLUS users aged 22–30 who:

- have a small liquid buffer;
- face regular essential obligations;
- are building one short-term savings goal; and
- may experience different levels of expense volatility.

These are a focused validation hypothesis rather than a claim that every First Jobber has the same financial situation.

## 4. Value Proposition

**For First Jobbers:** The user receives a decision that accounts for future uncertainty instead of applying the same percentage every month. The explanation makes the liquidity-versus-goal trade-off easier to understand, and the user retains control over the final action.

**For K PLUS/KBank:** K PLUS gains a small, auditable personalization use case that can be prototyped without moving money or accessing raw customer histories. It can test whether sequential decision support improves simulated goal and liquidity outcomes, and whether users understand the recommendation. Retention, deposits, debt reduction, and real customer impact require later validation.

## 5. Track Perspective

The problem is a finite-horizon Markov Decision Process. The state contains time, wallet, reserve, goal progress, deadline, current salary, and fixed obligations. The action is the pair of reserve and goal allocations subject to a cash-feasibility constraint. Salary and expense outcomes create stochastic transitions; rewards combine expense coverage, shortfall penalties, reserve progress, goal attainment, and terminal liquidity.

The project progresses from a transparent heuristic to known-model DP, Bayesian DP, pooled RL, and recurrent Meta-RL. DP supplies an interpretable benchmark. Bayesian DP is the strong low-complexity adaptation baseline. Meta-RL is accepted only if it adapts on held-out cash-flow dynamics and outperforms Bayesian DP under matched observations; otherwise the simpler method is retained.
