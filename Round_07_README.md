# Round 7 — Hyperparameter Tuning

## What this round was about

All four pipeline components tuned per function based on observed behaviour.

## Strategy

Beta (exploration-exploitation balance), step size (how far the NN nudges), SVM percentile (how selective the filter is) and NN weight decay (regularisation strength) were all adjusted based on what each function had shown. Functions with consistent improvement got tighter settings. Functions with no signal got looser settings to keep searching.

## Pipeline at this stage

- Full pipeline
- Beta: 0.5 to 3.0 by function
- Step size: 0.01 to 0.05 by function
- NN weight_decay: 1e-4 for smooth functions, 1e-3 for noisy ones

## Results

| Function | Output |
|----------|--------|
| F1 | 2.675e-9 |
| F2 | 0.537 |
| F3 | -0.022 |
| F4 | 0.5534 |
| F5 | 2512.64 |
| F6 | -0.792 |
| F7 | 1.8116 |
| F8 | 9.9236 |

## What the results showed

- F4: +0.5534 — first time breaking through to positive territory reliably
- F5: 2512 — continuing the longest winning streak in the project
- F7: 1.8116 — all-time best, x2 decreasing direction firmly established
- Three all-time bests in one round — hyperparameter tuning paying off

## Next step

Maintain gains; return regressions to confirmed best regions

---
*Full script with inline explanations: `round_07.py`*
