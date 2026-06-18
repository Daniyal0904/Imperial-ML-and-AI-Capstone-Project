# Round 1 — Setting the Baseline

## What this round was about

Random exploration to understand each function's starting behaviour.

## Strategy

No surrogate model at this stage. The goal is to spread initial observations across the search space and see how each function responds. Even bad results are useful — they tell you where not to look.

## Pipeline at this stage

- Random sampling across [0,1]^n
- No GP, UCB, SVM or NN yet

## Results

| Function | Output |
|----------|--------|
| F1 | ~0 |
| F2 | 0.1051 |
| F3 | -0.0319 |
| F4 | -0.2441 |
| F5 | ~800 |
| F6 | -1.007 |
| F7 | 0.747 |
| F8 | 9.820 |

## What the results showed

- F5 immediately returned a strong signal in the hundreds
- F8 responded well from the first query
- F1 returned near-zero — this becomes the hardest function in the project
- F4 returned negative — complex landscape confirmed

## Next step

Fit the first Gaussian Process surrogate and add UCB acquisition

---
*Full script with inline explanations: `round_01.py`*
