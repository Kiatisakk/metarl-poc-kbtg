# K PLUS First Jobber Hackathon: evidence review and pitch direction

This review follows the booklet's five sections first, then tests several concept directions against the REF, existing products, track fit, and student-team feasibility. All proposed first-jobber behaviors are treated as hypotheses unless directly supported by a source.

## 1. What the booklet actually requires

The [official booklet](Booklet.md) asks for a **one-page PDF** with five named sections. The challenge is a new K PLUS feature, service, or digital experience for first jobbers aged 22–30 that improves daily finance and savings management and/or protection from financial risks. Selection considers the *quality and depth* of that proposal. The booklet asks for a clear connection to the applicant's technical track and role. It does not prescribe AI, a prototype, a quantitative business case, or a solution that covers both challenge themes.

| Required section | Explicit request | Information needed to answer it | Shallow answer | Deep, convincing answer | REF that can strengthen it |
|---|---|---|---|---|---|
| **1. Problem Statement** | State the problem and clear financial pain point or threat. | A situation, user, moment, consequence, and reason current behavior fails. | “Young people cannot save.” | A concrete choice where available balance is mistaken for free cash before obligations fall due, with source limits stated. | [Deaton](ref/Deaton_1991_Saving_and_Liquidity_Constraints_w3196.pdf), [Krohné & Pagrotsky](ref/FULLTEXT01.pdf), [Maxted et al.](ref/Maxted_Laibson_Moll_2025_Present_Bias_NBER_w29094.pdf), [Fagereng et al.](https://www.aeaweb.org/articles?id=10.1257/mac.20190211). |
| **2. Proposed Solution** | Explain how the new feature, service, or experience works. | Trigger, inputs, calculation or decision, screen/action, and outcome. | “An AI assistant improves spending.” | A before-confirmation calculation with a transparent message and a way to correct assumptions. | [Krohné & Pagrotsky](ref/FULLTEXT01.pdf) on liquidity versus goals; [Fan et al.](ref/behavsci-16-00454.pdf) on warning design as an analogy, not proof of a saving outcome. |
| **3. Target Users** | Say who benefits in the first-jobber 22–30 context. | A first-jobber subgroup and why its situation creates the chosen pain. | “Everyone aged 22–30.” | Salaried first jobbers using one K PLUS spending account for recurring bills and daily QR payments, explicitly marked as a segment hypothesis pending local validation. | [Krohné & Pagrotsky](ref/FULLTEXT01.pdf) models ages 18–30, but is not a Thai prevalence study. |
| **4. Value Proposition** | Explain value for both the user and K PLUS/KBank. | A credible user outcome plus a reason the bank benefits. | “Users save millions; bank revenue rises.” | Fewer avoidable bill shortfalls as a testable user outcome; possible trust and engagement for K PLUS as bank hypotheses. | [Deaton](ref/Deaton_1991_Saving_and_Liquidity_Constraints_w3196.pdf) for buffer rationale; [Chak et al.](ref/Chak_DAcunto_2023_Improving_Household_Debt_Robo_Advice_w30616.pdf) cautions that advice uptake and trust matter. |
| **5. Track Perspective** | Briefly connect the solution to the applicant's technical track/role. | The actual engineering, data, or security contribution that the team can demonstrate. | Append “AI-powered” or “secure” to the feature name. | For this concept, Track 1 can show a reliable pre-payment rule, account state handling, and quality tests. | The REF gives problem evidence, not an extra track requirement. |

The booklet's Track 1 perspective explicitly covers what to develop, how, and how to test/ensure quality, with architecture, scalability, reliability, and testability. Track 2 focuses on data/analytics/ML/intelligence for better financial decisions. Track 3 focuses directly on scam/fraud risk prevention, suspicious behavior/transactions, pre-loss alerts, and trust. Those descriptions guide the track analysis below; they are not a request to use every technique.

## 2. REF audit: fact, interpretation, opportunity

The archive's [README](ref/README.md) is an index with a prior “NEXT GOAL / Track 2” framing, **not primary evidence**. It says “8 files,” but there are **9 PDFs**. It also links to Fan et al. (already supplied as a PDF) and to an additional Fagereng et al. paper, audited from its publisher abstract below; the publisher's full text requires access. Several index descriptions conflict with the supplied files, as noted below. The papers mainly support mechanisms or design cautions. None measures how often Thai K PLUS users aged 22–30 suffer the precise proposed problem.

### R1 — Deaton, *Saving and Liquidity Constraints* ([PDF](ref/Deaton_1991_Saving_and_Liquidity_Constraints_w3196.pdf))

- **Problem / target:** A theoretical account of saving for consumers who cannot freely borrow; not a study of Thai first jobbers.
- **FACT — behavior/evidence/technology:** Under specified income processes and preferences, liquid assets can act as a buffer against low income. The paper develops economic models, not a bank app or field intervention. It also shows this result changes with assumptions about income persistence; in one limiting random-walk case, impatient constrained consumers consume current income.
- **Limitation / unsolved problem:** It does not establish the right buffer for an individual or demonstrate that an app prompt changes behavior.
- **INTERPRETATION:** Protecting near-term liquidity before discretionary spending is more defensible than maximizing a distant goal in isolation.
- **OPPORTUNITY:** Show the immediate trade-off between a payment and already committed cash. This is an inference, not Deaton's tested product recommendation.

### R2 — Maxted, Laibson & Moll, *Present Bias Amplifies the Household Balance-Sheet Channels of Macroeconomic Policy* ([PDF](ref/Maxted_Laibson_Moll_2025_Present_Bias_NBER_w29094.pdf))

- **Problem / target:** Macroeconomic effects of present-biased household choices in a calibrated US model; not first-jobber app use.
- **FACT — behavior/evidence/technology:** The model combines liquid savings, housing equity, debt, and present bias. Its present-bias calibration yields lower liquid buffers and more households at a borrowing constraint than its exponential-discount benchmark. The file is a **July 2021 NBER working paper**. It contains different calibrated beta cases (including 0.70 and 0.83); the README's single “beta ≈ 0.7” is too reductive.
- **Limitation / unsolved problem:** This is model output, not proof that a K PLUS nudge will change Thai spending.
- **INTERPRETATION:** The point of purchase is a plausible place to surface future costs that are otherwise easy to discount.
- **OPPORTUNITY:** Test an explicit pre-payment commitment reminder, while treating behavioral benefit as unproven.

### R3 — Krohné & Pagrotsky, *Dynamic Optimization of Individual Financial Well-Being* ([PDF](ref/FULLTEXT01.pdf))

- **Problem / target:** A Swedish banking-context thesis models ages 18–30 balancing emergency buffer, housing down payment, short-term, and long-term savings.
- **FACT — behavior/evidence/technology:** Dynamic programming and Monte Carlo simulation produce different allocations as income and utility weights change. Balanced specifications do better in constrained-income scenarios in the model; housing-heavy settings can reach the housing target faster. The authors explicitly call the work a **baseline for further empirical validation**, not a deployable advisory tool.
- **Limitation / unsolved problem:** It uses Swedish assumptions, simulated paths, and subjective weights. It does **not** demonstrate a measured “goal abandonment effect” in real users, despite that claim in the README.
- **INTERPRETATION:** A single fixed saving rule can be unsafe when obligations and income vary.
- **OPPORTUNITY:** A transparent near-term check can avoid overpromising an “optimal” lifetime allocation.

### R4 — Das et al., *Dynamic Optimization for Multi-Goals Wealth Management* ([PDF](ref/MultWealthGoals.pdf))

- **Problem / target:** Investor decisions among competing medium/long-term purchasing and investment goals; not daily payment behavior.
- **FACT — behavior/evidence/technology:** A dynamic-programming method chooses investment portfolios and goal fulfillment based on investor-supplied goal utilities and models goal-attainment probabilities. Comparisons are algorithmic/simulation based.
- **Limitation / unsolved problem:** Eliciting goal importance is difficult; the model does not establish real-world user adoption or solve day-to-day bill coverage.
- **INTERPRETATION:** “More goals” is not itself useful when users cannot understand the trade-off.
- **OPPORTUNITY:** If exploring goals, present one concrete trade-off rather than a full optimization engine.

### R5 — Das et al., *A Meta Reinforcement Learning Approach to Goals-Based Wealth Management* ([PDF](ref/2605.02300v1.pdf))

- **Problem / target:** Computational speed for multi-year investor goal and portfolio decisions; not a first-jobber behavior study.
- **FACT — behavior/evidence/technology:** In simulated test cases, meta-RL reached on average **97.8% of dynamic-programming expected utility**. The paper reports mean current-action inference of **20.94 ms with a goal decision** and **9.277 ms without** in Table 1, for its test cases. The README's “20 million people in <10 ms” is **not supported by this PDF**.
- **Limitation / unsolved problem:** Accuracy is against a modeled optimizer under modeled preferences/returns, not against user welfare or bank production data. The authors note value estimates can require much more computation than a single action.
- **INTERPRETATION:** A fast complex model is unnecessary for a one-cycle bill coverage decision.
- **OPPORTUNITY:** Keep complex goal optimization out of the MVP; use this paper only if a later, genuinely multi-goal investment product is pursued.

### R6 — Chak et al., *Improving Household Debt Management with Robo-Advice* ([PDF](ref/Chak_DAcunto_2023_Improving_Household_Debt_Robo_Advice_w30616.pdf))

- **Problem / target:** UK adults allocating repayments across multiple loans; not specifically ages 22–30 or Thai banking.
- **FACT — behavior/evidence/technology:** In a pre-registered online randomized experiment with **3,423** delivered participants, free automated allocations reduced forgone savings on the hypothetical loan tasks by **14.6 percentage points** on an intention-to-treat basis; the treatment-on-treated estimate was **19.6 points**. Around a quarter of offered free advice was declined. The authors found little subsequent unassisted learning, and lower algorithm trust among non-adopters/overriders. The PDF is a **November 2022 NBER working paper**; the README's “15% debt reduction” is not the measured result.
- **Limitation / unsolved problem:** Incentivized hypothetical task choices do not equal measured reductions in actual loan balances, nor prove a general spending-advice effect.
- **INTERPRETATION:** Even mathematically correct advice needs user trust, legibility, and a clear action.
- **OPPORTUNITY:** A narrow debt-repayment order helper is credible if loan data and authorization are available; otherwise a manually entered prototype can only test understanding.

### R7 — Fan et al., *The Impact of Multidimensional Warning Messages on Payment Security Behavior Across Different Scenarios* ([PDF](ref/behavsci-16-00454.pdf))

- **Problem / target:** Warning habituation in mobile transfers. The two experiments used Chinese university students (n=42, mean age 19.27; n=47, mean age 20.26), not Thai first jobbers.
- **FACT — behavior/evidence/technology:** Static transfer-screen lab experiments compared warning presence, color, wording, and transfer amount as a proxy for *potential loss*. Presence lengthened reaction time but **did not significantly increase rejection in Experiment 1**. Red and imperative warnings increased rejection in Experiment 2; eye tracking was used. No real fraud outcomes were measured.
- **Limitation / unsolved problem:** The authors note static screenshots, no real money, limited sample, and possible demand/fatigue effects. A higher rejection rate is not necessarily better if legitimate transfers are rejected.
- **INTERPRETATION:** Generic warnings alone may be weak, and warning timing/content matter.
- **OPPORTUNITY:** Test a selective, reason-specific fraud interruption, with false alarms and genuine loss prevention measured separately.

### R8 — UK Payment Systems Regulator, *Fighting authorised push payment scams: final decision* ([PDF](ref/UK_PSR_PS23_4_APP_Scams_Policy_Statement.pdf))

- **Problem / target:** UK authorised push payment scam reimbursement and payment-provider incentives; not a Thai legal or K PLUS policy.
- **FACT — behavior/evidence/technology:** The **December 2023 PS23/4** document argues for prevention at payment time and risk-based intervention. This version says a **£415,000 maximum** and **7 October 2024** start date. It is regulatory policy, not a trial of a warning interface. The README's **£85,000** is not the cap in this supplied PDF.
- **Limitation / unsolved problem:** UK policy cannot be applied as Thai legal obligation or evidence of KBank reimbursement economics.
- **INTERPRETATION:** Payment providers have strategic reasons to act before loss, but a Thai bank case needs Thai-specific validation.
- **OPPORTUNITY:** A Track 3 proposal can focus on one pre-loss decision, without claiming UK law governs K PLUS.

### R9 — The mislabeled “Capponi & Zhang” PDF ([PDF](ref/2112.04026_Capponi_Zhang_2024.pdf))

**FACT:** The supplied file is *A semi-group approach to Principal Component Analysis*, by Martin Schlather and Felix Reinbott (2021). It does not contain the README's purported continuous-time goal wealth-management paper. **No finance inference or concept is drawn from it.**

### R10 — Fagereng, Holm & Natvik, *MPC Heterogeneity and Household Balance Sheets* ([publisher abstract](https://www.aeaweb.org/articles?id=10.1257/mac.20190211))

- **Problem / target:** How Norwegian households with different liquid assets spend or save a one-off lottery gain; not a study of Thai first jobbers or recurring salaries.
- **FACT — behavior/evidence/technology:** The publisher abstract describes Norwegian administrative panel data. Spending peaks in the winning year and varies with prize size, age, and liquid assets. It reports that low-liquidity winners of the smallest prizes (around US$1,500) spent all within that year, while the estimate for high-liquidity winners of large prizes was slightly below half. The paper also uses a two-asset life-cycle model. The linked replication package does not give open access to the confidential administrative data.
- **Limitation / unsolved problem:** The publisher full text was access-restricted during this review, so this audit is limited to its abstract. Lottery windfalls cannot establish behavior at an ordinary K PLUS QR payment.
- **INTERPRETATION:** Liquidity and age can matter to spending response, which supports asking whether thin-buffer first jobbers need an in-context cash reminder.
- **OPPORTUNITY:** Use local interviews and scenario tests to see whether that possible mechanism translates to the proposed payment moment; do not transplant Norwegian effect sizes to Thailand.

## 3. Answering the five sections before choosing a final concept

### 1. Problem Statement — a focused working problem

**Working pain point:** A salaried first jobber sees a positive balance in the K PLUS spending account and makes a discretionary QR payment late in the pay cycle, without noticing that part of that balance is needed for bills due before the next salary. The payment succeeds, but the remaining cash may no longer cover those commitments and a basic reserve.

The *proposed mechanism* is that visible balance does not subtract future obligations, while immediate spending is salient. [Deaton](ref/Deaton_1991_Saving_and_Liquidity_Constraints_w3196.pdf) supports the value of liquid buffers under some constraints; [Maxted et al.](ref/Maxted_Laibson_Moll_2025_Present_Bias_NBER_w29094.pdf) model present bias and low liquid buffers; the [young-adult thesis](ref/FULLTEXT01.pdf) shows model trade-offs between goals and resilience. **None directly documents the frequency of this exact mistake among Thai first jobbers.** It must be validated. K PLUS matters because it owns the actual QR-payment confirmation moment and account balance. [K PLUS publicly describes My Spending, My Budget, and savings tools](https://www.kasikornbank.com/en/kplus); the public descriptions do not establish a bill-aware warning at this point of action. An in-app audit remains necessary before claiming a feature gap.

### 2. Proposed Solution — mechanisms considered for that problem

| Mechanism | Exact intervention | Inputs and logic | Behavior changed | K PLUS difference and weakness |
|---|---|---|---|---|
| **A. Bill-Safe Check** | When the user reviews a QR-payment amount, immediately before confirmation, and only if the payment crosses a user-set protection threshold. | Current balance minus QR amount minus user-confirmed unpaid bills due before next payday minus a user-chosen reserve. Show the resulting shortfall and the relevant due bill(s). | Makes the future obligation visible before the outflow; user can review or proceed. | Would add a decision-time check to K PLUS's described budget/summary tools. Depends on users entering/confirming obligations and on accurate account state. |
| **B. Payday Safe Save** | When salary arrives and the user considers moving money into a savings goal. | Salary/account balance, due bills, next payday, reserve; show a maximum suggested contribution. | Avoids saving an unsustainable amount that must soon be withdrawn. | Closer to existing K PLUS goal planning and MAKE pockets/auto saving, so differentiation is weaker. |
| **C. Goal Recovery Prompt** | After a planned contribution is missed. | Goal deadline, contribution history, cash available, chosen priority; offer a smaller catch-up or a new date. | Replaces silent abandonment with an explicit reset. | The REF does not establish real “abandonment” prevalence, and goal features already exist. |

These are design options, not established interventions. **A** is the narrowest payment-moment opportunity; the final recommendation follows the comparison below.

### 3. Target Users

**Hypothesized subgroup:** K PLUS users aged 22–30 with a regular first salary, one main K PLUS account used for daily QR payments, and rent/utility/transport or other essential payments falling before the next payday. They need the check when their cash margin is small enough that one optional purchase can collide with a known commitment. The REF supports the relevance of liquidity and young-adult trade-offs, but **does not prove this subgroup's size, common behavior, or willingness to enter bills in Thailand**. Users with irregular income or obligations spread across other banks may need a different design; the MVP does not promise full financial visibility.

### 4. Value Proposition

- **First jobber:** A more accurate decision at the payment moment: “If I pay this now, can I still meet the bills I told K PLUS about?” The intended outcome is fewer avoidable shortfalls and less need to raid savings; that outcome has to be tested, not assumed.
- **K PLUS / KBank:** K PLUS could make its budgeting tools useful at the point of action, plausibly improving trust and repeat use. Reduced payment distress and stronger retention are **business hypotheses**, not measured REF results or guaranteed revenue. Engagement alone should not be counted as value if the check creates annoying false alarms.

### 5. Track Perspective — all three tracks

| Track | Fit and meaningful contribution | What to demonstrate | What would be superficial |
|---|---|---|---|
| **Track 1 — Software Engineering & Quality** | **Strongest natural fit.** A small, reliable decision service and clear QR confirmation flow. | Correct obligation window, duplicate/paid bill handling, stale-balance refresh, accessible explanations, user override, and tests for edge cases. A student prototype can use a mock account and bills. | An attractive screen with no trustworthy state logic or quality plan. |
| **Track 2 — Data Science & Intelligence** | Possible later fit if KBank transaction history is available and recurring bills can be detected with confidence. | Precision/recall of bill detection, uncertainty display, cold-start fallback, and whether predictions improve decision quality over user-entered bills. | Labeling a subtraction rule “AI,” or training on synthetic data and claiming real-world predictive performance. |
| **Track 3 — Cyber Security & Digital Trust** | Weak fit for this cash-flow problem; it does not detect fraud. | Only if a separate, well-evidenced scam decision were chosen would a security threat model and risk-based pre-loss intervention be core. | Calling ordinary budgeting a cybersecurity feature because it uses a bank account. |

**Provisional selected track:** Track 1, subject to the team's actual application track. The booklet requires the proposal to match the track/role applied for, so a team already committed to Track 2 or 3 should choose and substantiate a fitting contribution rather than relabel this rule.

## 4. Cross-analysis and reasoning chain

**Repeated pattern:** The saving papers repeatedly distinguish liquid resilience from long-range goal progress. [Fagereng et al.'s publisher abstract](https://www.aeaweb.org/articles?id=10.1257/mac.20190211) adds observational evidence that liquidity and age are associated with how Norwegian households spend windfalls, though it does not test this proposal. The debt experiment shows correct automated advice is not automatically adopted. The fraud warning experiment shows interrupting a payment is not enough by itself: wording and context affect behavior, and a generic warning may add delay without changing rejection. The existing-product check shows K PLUS and MAKE already provide budgets, goals, pockets, and scheduled/automated money movement, while other banks already offer “left to spend” and bill segregation. The opportunity is therefore a *specific in-flow decision*, not another dashboard, pocket, or general assistant.

**Contradictions and boundaries:** The REF index's “goal abandonment,” “15% debt reduction,” “£85,000 in PS23/4,” and “20 million users in <10 ms” should not be used as pitch proof. Optimization papers model idealized investor decisions, while the shortlist concerns a one-month payment choice. Fraud warning results cannot be borrowed as proof that a bill warning reduces missed bills. No supplied paper establishes Thai segment prevalence. These limits argue for a prototype plus local user validation, not a stronger unsupported claim.

> **EVIDENCE** — liquid buffers matter under constraints; goal weights and income change modeled allocations; existing K PLUS budgets summarize and set limits.  
> **USER BEHAVIOR (hypothesis)** — a salaried first jobber pays by QR from an account containing future bill money.  
> **PAIN POINT** — the balance looks spendable although part is committed.  
> **ROOT CAUSE (hypothesis)** — future bills are absent from the immediate decision and immediate spending gets more attention.  
> **OPPORTUNITY** — the bank can surface the committed amount before a K PLUS payment.  
> **POSSIBLE SOLUTION** — a selective, explainable Bill-Safe Check.  
> **USER VALUE** — more informed proceed-or-pause choice; fewer shortfalls if behavior changes.  
> **K PLUS VALUE** — a plausible improvement in usefulness/trust of daily banking, to be measured.  
> **TECHNICAL TRACK** — Track 1 reliability and quality at the confirmation moment.

## 5. Small but deep scope

**One problem:** A discretionary QR payment can consume cash already needed for known bills. **One context:** salaried first jobbers late in a pay cycle. **One intervention:** a shortfall notice before confirmation, only when the transaction crosses the protected amount. **One clear value:** an informed payment choice before cash leaves the account.

**MUST HAVE:** (1) opt-in next payday, bill amounts/dates, and reserve; (2) account balance and QR amount in a prototype; (3) a deterministic, inspectable post-payment calculation; (4) warning that names the shortfall and due commitment; (5) correct/update inputs and proceed/cancel; (6) no warning when no shortfall. For a production proposal, the balance must be refreshed at confirmation and the calculation cannot be presented as a guarantee of future solvency.

**NICE TO HAVE:** user-approved recurring-bill suggestions based on transaction history; a single review of frequently overridden warnings; eventual link to existing K PLUS My Budget.

**OUT OF SCOPE:** transfers outside K PLUS, whole-bank data aggregation, investments, automated blocking, automatic bill payment, credit underwriting, fraud scoring, and lifetime financial optimization.

## 6. Challenge the selected concept

1. **Does the problem exist?** Plausible from liquidity theory and common payment structure, but **not directly evidenced for Thai K PLUS first jobbers**. Interview/test users before making a prevalence claim.
2. **Specific enough?** Yes: a discretionary K PLUS QR payment before known bills and payday.
3. **Already solved by K PLUS?** K PLUS publicly describes My Budget, My Spending, and savings features. The public material does not confirm this exact pre-confirmation check; inspect the current app before submission. [K PLUS feature page](https://www.kasikornbank.com/en/kplus), [KBank's budget announcement](https://www.kasikornbank.com/th/news/pages/k_investment.aspx).
4. **Already solved elsewhere?** Much of the underlying idea exists: [Starling Bills Manager](https://www.starlingbank.com/features/bills-manager/) and [Monzo Left to Spend](https://monzo.com/help/budgeting-overdrafts-savings/trends-left-to-spend-web) account for upcoming payments. **Do not claim global novelty.**
5. **Meaningfully different?** The proposed K PLUS addition is *the selective, bill-specific notice within QR payment confirmation*, not the arithmetic or a new pot. It is meaningful only if users understand and act on it more than they do with existing summaries.
6. **Unrealistic data?** No proprietary fraud labels or external-bank data for MVP. Manual bill entry creates adoption and omission risks.
7. **Unrealistic infrastructure?** A student team can prototype with mock balance/payment events. Deployment into the real confirmation flow would require KBank integration and authorization; do not claim it can be shipped independently.
8. **Unnecessary complexity?** A transaction-level forecast/ML model would add it. The MVP uses confirmed obligations and simple arithmetic.
9. **Can it be reduced further?** Yes. Begin with one spend account, one payday, one or two upcoming bills, and a chosen buffer. Skip automatic categorization.
10. **Believable user value?** Explainable, but must be measured as fewer *avoidable* shortfalls or better choices in scenarios, not merely more taps or screen views.
11. **Believable K PLUS value?** Plausible trust/engagement, unproven. Monitor opt-in, useful-warning rate, overrides, false alarms, and retention only in an authorized pilot.
12. **One page?** Yes: one use case, one formula, one example message, and one Track 1 quality contribution.

## 7. Six candidate directions

### 1. Bill-Safe Check

- **Problem / root cause:** A QR purchase leaves too little for known bills before payday because account balance does not show commitments.
- **Core insight / evidence:** Liquidity buffers and trade-offs matter ([R1](ref/Deaton_1991_Saving_and_Liquidity_Constraints_w3196.pdf), [R3](ref/FULLTEXT01.pdf)); K PLUS already offers budget summaries, so the gap worth testing is a payment-time decision.
- **Smallest solution / target / moment:** Before QR confirmation, show the bill/reserve shortfall only if this payment would cross it. Hypothesized salaried first jobbers with a main K PLUS spending account.
- **User / K PLUS value:** Better payment choice and potentially fewer bill shortfalls; potentially stronger perceived usefulness and trust, both requiring validation.
- **Track fit / included / out of scope:** Track 1; manual bill setup, deterministic check, reliable confirmation flow. Exclude ML, cross-bank data, auto-blocking.
- **Risk:** Manual setup and false alerts may outweigh benefit; similar concepts exist elsewhere and K PLUS may already have an equivalent.

### 2. Payday Safe Save

- **Problem / root cause:** A fixed contribution to a savings goal may leave insufficient cash for bills in a lean month; static saving ignores current obligations.
- **Core insight / evidence:** The young-adult allocation model changes with constrained income ([R3](ref/FULLTEXT01.pdf)); buffer logic ([R1](ref/Deaton_1991_Saving_and_Liquidity_Constraints_w3196.pdf)). Neither proves actual contribution reversals.
- **Smallest solution / target / moment:** On salary receipt, propose an optional safe contribution after user-confirmed bills and reserve. Salaried goal savers aged 22–30 are a hypothesis.
- **User / K PLUS value:** More sustainable saving; potential ongoing goal engagement.
- **Track fit / included / out of scope:** Track 1 for transparent arithmetic and safe execution; Track 2 only with real history and tested inference. Include one goal and one salary cycle. Exclude investment optimization.
- **Risk:** [K PLUS Goal-Based Portfolio](https://www.kasikornbank.com/th/kwealth/pages/a959-t4-hyb-goal-based-portfolio-kgth.aspx) and [MAKE Cloud Pocket](https://www.kasikornbank.com/th/news/pages/cloud_pocket.aspx) already cover much of the journey; difference may be too slight.

### 3. Missed-Goal Reset

- **Problem / root cause:** After missing a planned goal contribution, a user may stop engaging because the original target feels unattainable.
- **Core insight / evidence:** Goal priority changes the modeled optimal path ([R4](ref/MultWealthGoals.pdf), [R3](ref/FULLTEXT01.pdf)); **actual abandonment is not evidenced** in the supplied REF.
- **Smallest solution / target / moment:** At a missed contribution, offer “smaller amount now” or “move target date” with an explicit new plan. Target: first-jobber goal savers, a hypothesis.
- **User / K PLUS value:** Easier recovery from one missed payment; possible retention of goal-tool use.
- **Track fit / included / out of scope:** Track 1, one goal and simple rescheduling. Exclude broad multi-goal optimization.
- **Risk:** Weak direct evidence of the behavior; could duplicate existing goal reminders or be a cosmetic reschedule control.

### 4. Repay the Costliest Debt First

- **Problem / root cause:** A user with multiple loans pays by familiar heuristics rather than minimizing interest/fees.
- **Core insight / evidence:** Automated repayment allocation improved decisions in a UK online RCT ([R6](ref/Chak_DAcunto_2023_Improving_Household_Debt_Robo_Advice_w30616.pdf)).
- **Smallest solution / target / moment:** When allocating an extra repayment, show the highest-cost allocation and explain the saved interest. Target: first jobbers with multiple debts, whose prevalence here is unproven.
- **User / K PLUS value:** Lower avoidable borrowing cost if accurate; possible trust and deeper financial engagement.
- **Track fit / included / out of scope:** Track 2 for a clearly evaluated decision rule or Track 1 for correct calculation. Exclude lending marketplace and new credit products.
- **Risk:** Exact rates, terms, early-payment rules, and outside loans may be unavailable; the RCT did not show real-world debt reduction.

### 5. Reason-Specific Transfer Pause

- **Problem / root cause:** A user transferring to a suspected scammer may dismiss a repeated generic warning.
- **Core insight / evidence:** Generic warning presence delayed choices without increasing rejection in one lab experiment; wording/color affected rejection in another ([R7](ref/behavsci-16-00454.pdf)); [R8](ref/UK_PSR_PS23_4_APP_Scams_Policy_Statement.pdf) supports the strategic relevance of pre-loss intervention in a UK policy context.
- **Smallest solution / target / moment:** Before confirmation of a flagged first-time transfer, state the specific observable reason and safe verification step. Target: first jobbers who transfer to unfamiliar payees is a hypothesis, not proven susceptibility.
- **User / K PLUS value:** Potential scam avoidance; potential trust and lower exposure, unmeasured.
- **Track fit / included / out of scope:** Track 3 if the team can justify signals, threat model, false-positive handling, and a safe escalation path. Exclude generic “fraud AI” and claims to detect all scams.
- **Risk:** K PLUS already shows warnings before transfers ([KBank 2023 report](https://www.kasikornbank.com/en/IR/FinanInfoReports/financialReports/4Q23_MDxA_En.pdf)); useful risk signals and loss labels may be inaccessible. Rejection of genuine transfers is a real cost.

### 6. Two-Goal Trade-off Card

- **Problem / root cause:** When cash is tight, a saver cannot see how more for one goal delays another or depletes emergency liquidity.
- **Core insight / evidence:** Goal priority changes modeled attainment probabilities ([R4](ref/MultWealthGoals.pdf), [R5](ref/2605.02300v1.pdf)); the young-adult thesis warns of sensitivity to weights ([R3](ref/FULLTEXT01.pdf)).
- **Smallest solution / target / moment:** When increasing a monthly goal contribution, show the resulting date/shortfall change for one other goal and the buffer. Target: first jobbers with two active goals, a hypothesis.
- **User / K PLUS value:** Explicit trade-off; possibly more credible goal planning.
- **Track fit / included / out of scope:** Track 2 only if estimates can be calibrated and evaluated; otherwise Track 1 arithmetic. Exclude RL and portfolio advice in MVP.
- **Risk:** K PLUS already has goal planning; unreliable forecast precision may make the card less trustworthy than a simple rule.

## 8. Comparison and trade-offs

**Legend:** H = strong relative to this shortlist, M = moderate or conditional, L = weak/unproven. These are judgment calls, **not empirical scores**. “Evidence” means support for the mechanism and target together; it is lower when Thai first-jobber incidence is unknown. “Difference” is difference within the documented K PLUS experience, not world-first novelty.

| Concept | Problem depth | Evidence | Specificity | User relevance | K PLUS relevance | Solution clarity | Scope control | Feasibility | Track alignment | Difference | Discussion potential |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **1 Bill-Safe Check** | H | M | H | H | H | H | H | H | H (T1) | M | H |
| 2 Payday Safe Save | M | M | H | H | H | H | H | H | H (T1) | L | M |
| 3 Missed-Goal Reset | M | L | H | M | M | H | H | H | H (T1) | L | M |
| 4 Repay Costliest Debt | H | M | H | M | M | H | M | L | H (T2/T1) | M | H |
| 5 Transfer Pause | H | M | H | M | H | M | M | M | H (T3) | M | H |
| 6 Two-Goal Card | M | M | M | M | H | M | L | M | M (T2) | L | H |

**Trade-offs.** Concept 4 has the strongest experiment on decision assistance, but real loan terms and cross-lender coverage make it harder to deliver safely. Concept 5 has the clearest Track 3 story and a direct payment moment, but current K PLUS warnings and unavailable risk data raise the bar. Concepts 2, 3, and 6 align with much of the REF archive but overlap with existing KBank goal/pocket products and rely heavily on simulated rather than observed behavior. Concept 1 has moderate evidence and is not globally novel; it wins on an unusually clear user moment, testable calculation, limited data demands, and one-page explainability. A team must validate the local problem and check the live app before claiming it as a new K PLUS feature.

## 9. Final one-page pitch direction — conceptual draft

### 1. Problem Statement

A first-jobber can make a K PLUS QR purchase while their account still shows a positive balance, even though that cash is needed for bills due before the next salary. The account balance answers “Can I pay now?” but not “What remains for the commitments I have already made?” This specific situation among Thai users is a **hypothesis to validate**; the REF supports the importance of liquidity, not its local prevalence.

### 2. Proposed Solution

**Bill-Safe Check** is an opt-in check at the QR-payment confirmation screen. The user records the next payday, upcoming essential bill amounts/dates, and a minimum reserve. K PLUS calculates: **balance after proposed payment − unpaid bills due before payday − chosen reserve**. Only when that figure is negative, it shows the shortfall and named commitment, e.g. “Paying ฿1,200 now leaves ฿800 less than the amount you set aside for rent before payday.” The user can review the inputs, cancel, or continue. It never labels the purchase “bad” or blocks it.

### 3. Target Users

K PLUS users aged 22–30 with a regular first salary, daily QR spending from their main account, and bills due before payday. This is a **specific segment hypothesis**, not a measured demographic claim. The first prototype covers one account and user-confirmed bills.

### 4. Value Proposition

**First jobber:** sees the cost of a payment against near-term commitments before money leaves, enabling an informed choice and potentially fewer avoidable bill shortfalls. **K PLUS/KBank:** makes existing money-management capability useful inside a daily payment decision, with plausible trust and engagement value. Both outcomes require validation; no revenue or fraud-loss reduction is claimed.

### 5. Track Perspective

**Track 1 — Software Engineering & Quality** is the natural fit. Demonstrate a mock K PLUS QR confirmation flow backed by a small bill-coverage service, with tests for due-date boundaries, already-paid/duplicate bills, payment edits, a changing balance, and user override. Track 2 would require validated bill inference from real transaction history; Track 3 would require a separate fraud problem and is not claimed here.

## Final student-team test

A small team can explain the idea with one screenshot and the subtraction above; prototype it using mock balance/payment events and manually entered bills; and validate it with first-jobber interviews plus scenario tests comparing ordinary balance-only confirmation with Bill-Safe Check. Ask whether users understand the warning, change a risky choice when appropriate, and reject false alarms. **Pass condition for concept selection:** users encounter this situation often enough, the live K PLUS app lacks an equivalent intervention, and the check improves decisions without excessive setup or warning fatigue. If these fail, reject or revise the concept rather than add AI or more features.

### Current-product sources used for differentiation

- [K PLUS official feature page](https://www.kasikornbank.com/en/kplus): My Spending, My Budget, savings tools, QR payments.
- [KBank announcement of My Budget](https://www.kasikornbank.com/th/news/pages/k_investment.aspx); [K PLUS Goal-Based Portfolio](https://www.kasikornbank.com/th/kwealth/pages/a959-t4-hyb-goal-based-portfolio-kgth.aspx); [MAKE Cloud Pocket](https://www.kasikornbank.com/th/news/pages/cloud_pocket.aspx).
- [KBank 2023 financial report](https://www.kasikornbank.com/en/IR/FinanInfoReports/financialReports/4Q23_MDxA_En.pdf): a scam warning before every transfer, relevant to candidate 5.
- [Starling Bills Manager](https://www.starlingbank.com/features/bills-manager/), [Monzo Left to Spend](https://monzo.com/help/budgeting-overdrafts-savings/trends-left-to-spend-web), and [Revolut scheduled payments](https://www.revolut.com/en-US/subscriptions/): comparable outside-bank approaches; no global novelty claim.
