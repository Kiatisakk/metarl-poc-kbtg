# K PLUS Adaptive Goal Allocation Proposal

This directory follows the IEEE LaTeX structure from the public
[Snackathon-Swin-Hackathon/proposal](https://github.com/Snackathon-Swin-Hackathon/proposal)
repository. The document is written for the K PLUS First Jobber Hackathon,
Track 2: Data Science & Intelligence.

## Build

From this directory, with an IEEEtran LaTeX installation:

```text
latexmk -pdf proposal.tex
```

The compiled five-page submission is `proposal.pdf`. The proposal keeps the
research style of the template while mapping explicitly to the booklet's five
pitch sections. It treats Meta-RL as an empirical candidate and retains
Bayesian DP as the required simpler baseline.

For the booklet submission, use `one_page_pitch.pdf`. Its source is
`one_page_pitch.tex` and it contains the five required sections directly on a
single page.

The figures in `img/` are generated experiment artifacts. They contain only
synthetic simulation results and do not represent K PLUS customer data.
