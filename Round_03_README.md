# Round 3 — SVM Region Filter

## What this round was about

SVM classifier added. Three all-time bests achieved.

## Strategy

The SVM trains on all observations and labels the top 30% of outputs as 'promising'. Any candidate point that fails the filter gets removed before UCB scoring. This concentrates the search in regions the data says are productive, rather than wasting queries on areas already shown to be poor.

## Pipeline at this stage

- GP: Matern 2.5 kernel
- UCB: beta = 2.0
- SVM: RBF kernel, top 30% outputs as positive class

## Results

| Function | Output |
|----------|--------|
| F1 | 2.8e-9 |
| F2 | 0.41 |
| F3 | -0.0045 |
| F4 | 0.12 |
| F5 | 1200 |
| F6 | -0.2957 |
| F7 | 1.2 |
| F8 | 9.9250 |

## What the results showed

- F3: -0.0045 — closest to zero achieved in the whole project. Never improved since.
- F6: -0.2957 — same story, this was the peak and it was never recovered
- F8: 9.9250 — confirmed plateau. This value recurs across multiple rounds.
- The SVM filter is clearly helping — three bests in one round is not random

## Next step

Add neural network gradient analysis

---
*Full script with inline explanations: `round_03.py`*
