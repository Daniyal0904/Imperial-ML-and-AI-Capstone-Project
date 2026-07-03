# Round 12 — Final Refinement

## What this round was about

Final optimisation round. Preserve confirmed best-performing regions while making only small refinements where previous rounds showed consistent improvement.

## Strategy

With the final query budget available, the strategy focused almost entirely on exploitation rather than exploration. Functions with stable high-performing regions remained close to their best-known coordinates, while only functions that had shown reliable directional improvement received small adjustments.

F4 returned to its exact confirmed best coordinates after previous deviations consistently reduced performance. F5 received one final increase in x1 because this direction had produced improvements throughout the project. All remaining functions stayed close to their strongest-performing regions, allowing the surrogate models to make conservative refinements rather than exploring new areas.

## Pipeline at this stage

- Full pipeline
- F4: exact confirmed best coordinates
- F5: final incremental x1 increase
- F1, F2, F3, F6, F7 and F8: return-to-best or tight local exploitation
- Minimal exploration to preserve confirmed results

## Results

| Function | Output |
|----------|--------|
| F1 | TBD |
| F2 | TBD |
| F3 | TBD |
| F4 | TBD |
| F5 | TBD |
| F6 | TBD |
| F7 | TBD |
| F8 | TBD |

## What the results showed

- Awaiting portal results
- Final strategy prioritised protecting confirmed high-performing regions
- F5 tested whether one final x1 refinement could extend its consistent improvement trend
- F4 validated whether the previously identified optimum remained reproducible
- Remaining functions focused on maximising reliability rather than exploring uncertain regions

## Next step

Project complete — see `MODEL_CARD.md`, `DATASHEET.md` and `docs/` for the full summary of the optimisation strategy and results.
