# Round 8 — Recovery Round

## What this round was about

Returning regressed functions to confirmed best coordinates.

## Strategy

Several functions regressed when nudged slightly away from their confirmed best in Round 7. The same principle from Round 6 applies: narrow peaks are fragile. When a function has a known good region, return to it exactly rather than continuing to push. F4 in particular was brought back to its Round 7 coordinates.

## Pipeline at this stage

- Full pipeline
- F4 returned to exact Round 7 coordinates
- Conservative step sizes — protecting gains over chasing new ones

## Results

| Function | Output |
|----------|--------|
| F1 | 1.65e-9 |
| F2 | 0.523 |
| F3 | -0.020 |
| F4 | 0.361 |
| F5 | 2583.58 |
| F6 | -0.717 |
| F7 | 1.791 |
| F8 | 9.922 |

## What the results showed

- F5: 2583 — another new best. Ten rounds in a row of improvement on x1.
- F4 regressed significantly — the nudge moved off the narrow peak
- F2 confirmed noisy — same coordinates, meaningfully different output vs Round 6
- F6 continuing slow recovery across three rounds

## Next step

Return F4 to exact Round 7 coordinates. Continue F5 gradient.

---
*Full script with inline explanations: `round_08.py`*
