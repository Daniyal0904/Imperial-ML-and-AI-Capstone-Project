# Datasheet for the BBO Capstone Dataset

---

## Motivation

**Why was this dataset created?**

This dataset was built to document and support an iterative black-box optimisation challenge across eight unknown synthetic functions. Each function simulates a real-world problem — locating a 2D radiation source, optimising a drug compound formula, tuning a logistics model — where the underlying equation is hidden and every evaluation is expensive. The dataset captures the growing history of input-output observations accumulated week by week as the optimisation pipeline learned from each query.

The primary purpose is to train and update surrogate models that guide the next query for each function. A secondary purpose is to provide a transparent, reproducible record of how sequential human-guided decisions interact with complex multi-dimensional landscapes under strict budget constraints.

**Who created it and for what purpose?**

Created independently by Monalisa Saha as part of the Imperial College London Professional Certificate in ML & AI capstone project. No external funding or institutional backing was involved.

**What tasks does it support?**

Evaluating sample-efficiency of Bayesian optimisation and surrogate-guided search under strict evaluation budgets. Training and comparing GP, SVM and NN surrogate models. Providing a reproducible optimisation trace for academic review.

---

## Composition

**What does the dataset contain?**

Eight sub-datasets, one per function. Each instance contains a multi-dimensional input vector (X) and a scalar maximisation output (Y).

| Function | Dimensions | Initial observations | Total after Round 11 |
|----------|-----------|---------------------|----------------------|
| F1 | 2D | 10 | 21 |
| F2 | 2D | 10 | 21 |
| F3 | 3D | 10 | 21 |
| F4 | 4D | 10 | 21 |
| F5 | 4D | 10 | 21 |
| F6 | 5D | 10 | 21 |
| F7 | 6D | 10 | 21 |
| F8 | 8D | 10 | 21 |

Each function starts with 10 baseline observations provided by the programme. One new observation is added per function per round.

**Format**

All data is stored as NumPy `.npy` arrays:
- `initial_inputs_fN.npy` — shape `(10, dims)`
- `initial_outputs_fN.npy` — shape `(10,)`

All input values are bounded in `[0, 1]^n`. Outputs vary significantly across functions — from near-zero (F1) to thousands (F5).

**Are there gaps or known limitations?**

Yes — and intentionally so. Because the pipeline follows a strict one-query-per-function-per-round budget, the dataset has severe geographical gaps. The adaptive nature of Bayesian optimisation means later queries cluster around high-performing regions, leaving large portions of the search space — particularly in high-dimensional functions — completely unsampled.

F1 is the most extreme case: near-zero outputs across all eleven rounds suggest the true peak sits in a region that was never visited. F8 in eight dimensions has 21 observations covering a vanishingly small fraction of the possible space.

The dataset contains entirely synthetic numerical data. There is no human data, no private information, and no personally identifiable content.

---

## Collection Process

**How were queries generated?**

Collection took place in two stages. The first stage provided ten static baseline observations per function before any queries were submitted. The second stage ran for eleven consecutive weeks, with exactly one new query submitted per function per round.

Query generation evolved across rounds:

| Rounds | Method |
|--------|--------|
| R1 | Random sampling — no surrogate, spread observations across the space |
| R2 | Gaussian Process fitted; UCB acquisition function introduced |
| R3 | SVM region classifier added to filter unpromising candidates |
| R4 | Neural network gradient analysis added; full pipeline operational |
| R5 | Per-function configuration introduced — beta, step size, SVM threshold, NN weight decay all tuned per function |
| R6–R11 | Full GP + UCB + SVM + NN pipeline with adaptive per-function settings |

**Over what time frame?**

Eleven weeks, one submission per function per week via the capstone portal. Results were returned after each submission and incorporated into the next round's training data.

**Were any ethical reviews required?**

No. The dataset is entirely synthetic. No consent protocols, ethical reviews or human subject considerations apply.

---

## Preprocessing and Uses

**What transformations were applied?**

No filtering, normalisation or cleaning was applied to the raw observations. Input coordinates sit naturally within `[0, 1]^n`. Outputs were preserved exactly as returned by the portal, including noise and outliers, so surrogate models cannot smooth out the genuine landscape irregularities.

Within the pipeline, the GP surrogate uses `normalize_y=True` during fitting to standardise outputs before kernel fitting — but the stored observations remain in their original form.

**Intended uses**

Training and updating GP, SVM and NN surrogate models. Generating and evaluating next-round candidate queries. Providing a reproducible audit trail of the optimisation strategy across all eleven rounds.

**Uses to avoid**

Training general-purpose neural networks expecting balanced or representative data — the dataset is heavily biased toward a few local peaks discovered early. Making claims of global optimality — with 21 observations per function in up to eight dimensions, large parts of the landscape are never sampled. Transferring findings to real-world optimisation problems without additional validation.

---

## Distribution and Maintenance

**Where is the dataset available?**

Hosted in this GitHub repository. The initial `.npy` files are in the `data/` folder. Round-by-round results are documented in each round's README and tracked cumulatively in `docs/results_summary.md`.

**Terms of use**

Academic capstone project. Non-commercial use only. External reuse should include attribution and clear acknowledgement of the sparse coverage and uncertainty limitations.

**Who maintains it?**

Maintained solely by Monalisa Saha. Updated once per round when portal results are received. The repository will be updated through Round 11 and then archived.

---

## Reflection

Writing this datasheet made the assumptions underlying the optimisation strategy much more explicit. The most important assumption — that nearby inputs produce similar outputs — is what makes the GP surrogate useful but also what makes it blind to discontinuous or needle-shaped peaks. Documenting the gaps made it clear that F1 and F8 are the functions where the dataset provides the weakest coverage, and where surrogate confidence should be treated most sceptically. The datasheet also clarified that the exploitation bias in later rounds is not a flaw in the data — it is an expected consequence of how adaptive search works, and anyone using this data for surrogate training should account for it.
