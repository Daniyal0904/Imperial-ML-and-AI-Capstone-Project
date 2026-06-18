# Strategy Log

## The pipeline in plain English

Think of it as a treasure hunt with a limited number of digs:

- **GP** builds the map — using everything observed so far to estimate where the treasure might be and how uncertain that estimate is
- **UCB** scores the next dig — high score = high predicted value OR high uncertainty (worth checking)
- **SVM** marks bad areas off the map — filters out regions the data says are unpromising
- **NN** points the shovel — computes gradient at the current best point and nudges the final query in the improving direction

---

## Round-by-round decisions

| Round | Key decision | Why | Outcome |
|-------|-------------|-----|---------|
| R1 | Random baseline | No information — spread wide | F5/F8 show early signals |
| R2 | GP + UCB added | Need a model to guide the search | More informed queries |
| R3 | SVM filter added | Filter unpromising regions | 3 all-time bests in one round |
| R4 | NN gradient added | Refine final query toward improving direction | Full pipeline operational |
| R5 | Per-function beta | One setting too blunt for 8 different functions | Adaptive approach begins |
| R6 | Return-to-best logic | Regressed functions need recovery, not more exploration | Best single round (6/8 improved) |
| R7 | Hyperparameter tuning | Each function needs different beta, step, SVM threshold | 3 more all-time bests |
| R8 | Recovery | Several functions regressed after R7 nudges | F5 continued, F4 recovered slightly |
| R9 | F4 exact coordinates | Nudge caused regression — return to confirmed best | F4 matched R7 best exactly |
| R10 | Explicit decisions | Final rounds — document rationale for everything | F5 new best, others near peak |
| R11 | Lock in results | F5 one last push, F4 to confirmed coordinates | TBD |

---

## Beta evolution per function

Beta controls exploration vs exploitation in UCB. Lower = exploit known good areas. Higher = explore uncertain areas.

| Function | R1-3 | R4-5 | R6-7 | R8-11 | Notes |
|----------|------|------|------|-------|-------|
| F1 | 2.58 | 3.0 | 3.0 | 3.0 | Never found reliable signal — kept exploring |
| F2 | 2.58 | 2.0 | 1.5 | 2.0 | Noisy — moderate, never committed |
| F3 | 2.58 | 2.5 | 2.0 | 2.0 | Fragile peak — careful search |
| F4 | 2.58 | 1.5 | 1.5 | 1.5 | Narrow but real — exploit carefully |
| F5 | 2.58 | 0.8 | 0.8 | 0.8 | Reliable gradient — low beta, tight exploit |
| F6 | 2.58 | 3.0 | 3.0 | 2.5 | Multimodal — explore broadly |
| F7 | 2.58 | 1.0 | 1.0 | 1.0 | Direction established R6 — exploit |
| F8 | 2.58 | 0.5 | 0.5 | 0.5 | Near plateau — very tight exploit |
