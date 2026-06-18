# Black-Box Optimisation (BBO) Capstone

**Monalisa Saha** · Imperial College London Professional Certificate in ML & AI  
Reading, UK · [LinkedIn](https://www.linkedin.com/in/monnaliisa-saha/)

---

This repository documents an eleven-round optimisation challenge across eight hidden black-box functions. The goal: find the input that maximises each function's output — without ever seeing the equation, the gradient, or the shape of the landscape. One query per function per week. Every choice counts.

**Project Documentation**
- [Datasheet for Dataset](DATASHEET.md) — composition, collection process, gaps and assumptions
- [Model Card](MODEL_CARD.md) — pipeline details, strategy evolution, performance and limitations

---

## The Eight Functions

| Function | Dimensions | Real-world scenario |
|----------|-----------|---------------------|
| F1 | 2D | Radiation source detection — only proximity to the source gives a non-zero signal |
| F2 | 2D | Noisy ML model scoring — outputs carry noise and the landscape has multiple local peaks |
| F3 | 3D | Drug discovery — find the compound combination that minimises adverse reactions |
| F4 | 4D | Warehouse logistics — tune the hyperparameters of a costly placement model |
| F5 | 4D | Chemical process yield — unimodal function, one clear peak to find |
| F6 | 5D | Recipe scoring — five ingredient amounts, total score is negative by design |
| F7 | 6D | ML hyperparameter tuning — six parameters, maximise model performance |
| F8 | 8D | High-dimensional hyperparameter search — find the strongest local maximum |

All inputs are in `[0, 1]^n`. All tasks are maximisation problems.

---

## Pipeline

Built incrementally across rounds — one component added at a time:

```
Round 1   Random sampling — establish baseline
Round 2   Gaussian Process (GP) surrogate added
Round 3   UCB acquisition function added
Round 4   SVM region filter added
Round 5   Neural Network gradient refinement added
Round 6+  Per-function configuration and tuning
```

From Round 6 onwards, the full pipeline per function:

```
GP   → fits a probabilistic surface: mean prediction + uncertainty per candidate
UCB  → scores candidates: mean + (beta × std) where beta is tuned per function
SVM  → filters out unpromising regions using top 30% of observations as positive class
NN   → computes gradient at current best; nudges final query in improving direction
```

---

## Results

| Round | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 |
|-------|-----|-----|------|-----|------|------|-----|------|
| R1 | ~0 | 0.1051 | -0.0319 | -0.2441 | ~800 | -1.007 | 0.747 | 9.820 |
| R2 | ~0 | 0.230 | -0.028 | -0.180 | ~900 | -0.900 | 0.950 | 9.870 |
| R3 | 2.8e-9 | 0.410 | **-0.0045** | 0.120 | 1200 | **-0.2957** | 1.200 | **9.9250** |
| R4 | 1.2e-9 | 0.380 | -0.018 | 0.310 | 1450 | -0.650 | 1.400 | 9.880 |
| R5 | **2.68e-9** | 0.490 | -0.022 | 0.280 | 1800 | -0.710 | 1.550 | 9.900 |
| R6 | 3.6e-10 | **0.6202** | -0.016 | 0.499 | 2366.81 | -0.793 | 1.7982 | 9.9238 |
| R7 | 2.68e-9 | 0.537 | -0.022 | **0.5534** | 2512.64 | -0.792 | **1.8116** | 9.9236 |
| R8 | 1.65e-9 | 0.523 | -0.020 | 0.361 | 2583.58 | -0.717 | 1.791 | 9.9222 |
| R9 | 2.68e-9 | 0.441 | -0.028 | 0.553 | 2699.31 | -0.707 | 1.807 | 9.9228 |
| R10 | 2.62e-9 | 0.564 | -0.036 | 0.486 | **2798.79** | -0.698 | 1.804 | 9.9230 |
| R11 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

**Bold** = all-time best for that function. Add Round 11 results as a new row when available.

---

## Repository Structure

```
## Repository Structure

├── README.md
├── DATASHEET.md            — dataset motivation, composition and limitations
├── MODEL_CARD.md           — pipeline details, strategy evolution and performance
├── requirements.txt
├── Round_01_README.md      — Round 1: what happened and why
├── Round_01.py             — Round 1: script with full inline explanations
├── Round_02_README.md
├── Round_02.py
├── Round_03_README.md
├── Round_03.py
├── Round_04_README.md
├── Round_04.py
├── Round_05_README.md
├── Round_05.py
├── Round_06_README.md
├── Round_06.py
├── Round_07_README.md
├── Round_07.py
├── Round_08_README.md
├── Round_08.py
├── Round_09_README.md
├── Round_09.py
├── Round_10_README.md
├── Round_10.py
├── Round_11_README.md
└── Round_11.py
```

---

## Running the Scripts

```bash
pip install -r requirements.txt
cd Round_05
python round_05.py
```

Scripts use placeholder observations — replace `X_obs` and `y_obs` with accumulated portal data before running.

**Stack:** Python 3.10 · NumPy · scikit-learn · PyTorch · Matplotlib
