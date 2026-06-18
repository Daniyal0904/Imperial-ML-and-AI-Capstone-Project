# Round 6 — Best Round of the Project

## What this round was about

Six out of eight functions improved. Three new all-time bests.

## Strategy

The key insight this round was to return regressed functions to their last confirmed best coordinates instead of always nudging forward. When F2 was taken back to its Round 3 coordinates, it produced a new all-time best. This taught an important lesson about the difference between following a gradient and chasing noise.

## Pipeline at this stage

- Full pipeline
- Return-to-best logic introduced for regressed functions
- Beta varied by function trajectory

## Results

| Function | Output |
|----------|--------|
| F1 | 3.61e-10 |
| F2 | 0.6202 |
| F3 | -0.016 |
| F4 | 0.499 |
| F5 | 2366.81 |
| F6 | -0.7925 |
| F7 | 1.7982 |
| F8 | 9.9238 |

## What the results showed

- F2: 0.6202 — the highest this function ever produced across eleven rounds
- F5: 2366 — another new best, x1 gradient continuing its run
- F7: 1.7982 — first clear indication that x2 direction is key
- Six functions improved in one round — the strongest single round of the project

## Next step

Systematic hyperparameter tuning across all four pipeline components

---
*Full script with inline explanations: `round_06.py`*
