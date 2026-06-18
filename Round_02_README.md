# Round 2 — First Gaussian Process

## What this round was about

GP surrogate fitted. UCB acquisition function introduced.

## Strategy

Even with a handful of observations, the GP can start estimating the shape of each function. UCB scoring balances using what we know (mean) with exploring what we don't (uncertainty). Same beta across all functions for now — differentiation comes later.

## Pipeline at this stage

- GP: Matern 2.5 kernel, normalised outputs
- UCB: score = mean + 2.576 × std (uniform beta)
- No SVM or NN yet

## Results

| Function | Output |
|----------|--------|
| F1 | ~0 |
| F2 | 0.23 |
| F3 | -0.028 |
| F4 | -0.18 |
| F5 | ~900 |
| F6 | -0.9 |
| F7 | 0.95 |
| F8 | 9.87 |

## What the results showed

- F5 and F7 responding to GP-guided queries
- F1 still near-zero — the GP has nothing to go on here
- UCB producing more informed queries than pure random

## Next step

Add SVM region classifier to filter unpromising candidates

---
*Full script with inline explanations: `round_02.py`*
