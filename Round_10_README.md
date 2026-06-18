# Round 10 — Explicit Decision-Making

## What this round was about

Every query decision documented with explicit reasoning. Near-full exploitation.

## Strategy

With one round remaining, every decision was weighed against the all-time best. F5 got another x1 push. F4 got a careful nudge from its confirmed best — trying to find if there is slightly more performance close to the peak. F2, F3 and F1 were kept near their best known regions with no large moves. F6 continued its patient recovery direction.

## Pipeline at this stage

- Full pipeline
- Decision rationale written before each query
- Conservative: protect known good results over gambling on new regions

## Results

| Function | Output |
|----------|--------|
| F1 | 2.624e-9 |
| F2 | 0.564 |
| F3 | -0.036 |
| F4 | 0.486 |
| F5 | 2798.79 |
| F6 | -0.698 |
| F7 | 1.804 |
| F8 | 9.923 |

## What the results showed

- F5: 2798 — new all-time best. Eleven consecutive rounds of improvement on x1.
- F4 regressed again — any deviation from exact peak coordinates causes regression
- F2 giving variable outputs at similar inputs — stochastic behaviour confirmed
- F6 continuing its slow recovery over four rounds

## Next step

Final round — return F4 to confirmed best, push F5 one more time

---
*Full script with inline explanations: `round_10.py`*
