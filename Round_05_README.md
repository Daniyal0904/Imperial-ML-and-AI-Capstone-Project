# Round 5 — Per-Function Configuration

## What this round was about

Different functions need different settings. Uniform configuration abandoned.

## Strategy

Five rounds in, the functions have shown clearly different characters. F5 has a reliable exploitable gradient and needs low beta (tight exploitation). F1 has almost no signal and needs high beta (aggressive exploration). F4 keeps oscillating and needs different step sizes. This round introduces function-specific settings based on what the data has actually shown.

## Pipeline at this stage

- Full GP + UCB + SVM + NN
- Beta per function: F1=3.0, F2=2.0, F5=0.8, F8=0.5 etc.
- Step size per function: 0.01 to 0.05
- SVM percentile per function: 25-35%

## Results

| Function | Output |
|----------|--------|
| F1 | 2.68e-9 |
| F2 | 0.49 |
| F3 | -0.022 |
| F4 | 0.28 |
| F5 | 1800 |
| F6 | -0.71 |
| F7 | 1.55 |
| F8 | 9.90 |

## What the results showed

- F1 hits a meaningful positive value at the centre point [0.5, 0.5]
- F5 continuing its run — x1 gradient is the most reliable signal in the project
- Per-function beta is immediately producing more sensible queries
- The approach is now adaptive rather than uniform

## Next step

Return regressed functions to confirmed best coordinates rather than pushing further

---
*Full script with inline explanations: `round_05.py`*
