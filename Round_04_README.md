# Round 4 — Neural Network Gradient

## What this round was about

Full four-component pipeline operational for the first time.

## Strategy

After the GP+UCB+SVM pipeline selects a candidate, a small neural network is trained on all observations. Backpropagation at the current best point estimates which direction in the input space would improve the output. The final query is nudged in that direction before submission.

## Pipeline at this stage

- GP + UCB + SVM (as Round 3)
- NN: 2-layer MLP (32 units), ReLU activations, PyTorch
- Gradient computed at current best via backpropagation
- Step size: 0.03 across all functions

## Results

| Function | Output |
|----------|--------|
| F1 | 1.2e-9 |
| F2 | 0.38 |
| F3 | -0.018 |
| F4 | 0.31 |
| F5 | 1450 |
| F6 | -0.65 |
| F7 | 1.4 |
| F8 | 9.88 |

## What the results showed

- Full pipeline now running — GP maps, UCB scores, SVM filters, NN refines
- F5 continuing strong — gradient in x1 direction appearing reliable
- F3 and F6 regressed from Round 3 bests — these peaks are fragile
- Mixed results elsewhere — the pipeline needs per-function tuning next

## Next step

Introduce per-function configuration — one beta for all is too blunt

---
*Full script with inline explanations: `round_04.py`*
