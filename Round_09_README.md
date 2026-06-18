# Round 9 — F4 Confirmed, F5 New Best

## What this round was about

F4 peak confirmed reproducible at exact same coordinates.

## Strategy

Returning F4 to [0.360, 0.410, 0.430, 0.395] matched its Round 7 best exactly. This matters — it means the peak is a real feature of the function, not a noise event. F5 got another x1 push and reached a new best for the third consecutive round.

## Pipeline at this stage

- Full pipeline
- F4: exact Round 7 coordinates
- F5: x1 pushed incrementally
- Others: tight exploitation or return to best

## Results

| Function | Output |
|----------|--------|
| F1 | 2.675e-9 |
| F2 | 0.441 |
| F3 | -0.028 |
| F4 | 0.5534 |
| F5 | 2699.31 |
| F6 | -0.707 |
| F7 | 1.807 |
| F8 | 9.923 |

## What the results showed

- F4 matched its all-time best at identical coordinates — the peak is real and reproducible
- F5: 2699 — another new best. The x1 gradient is the most consistent signal in this entire project.
- F2 gave a poor result at Round 6 coordinates again — this function is genuinely stochastic
- F6 recovery continuing — three rounds of consistent slow improvement

## Next step

Final exploitation rounds — document all decisions explicitly

---
*Full script with inline explanations: `round_09.py`*
