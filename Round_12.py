"""
Round 12 — Final Refinement / Stability Check
=============================================

This round continues the full BBO optimisation pipeline used in earlier rounds:

1. Gaussian Process surrogate
2. UCB acquisition function
3. SVM promising-region filter
4. Neural Network gradient nudge

At this stage, the strategy is mostly exploitation:
- Preserve confirmed best regions
- Avoid large exploratory jumps
- Apply small controlled nudges only where previous rounds showed improvement
- Keep unstable functions close to their best known coordinates
"""

import numpy as np
import torch
import torch.nn as nn
import warnings

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")


# ── Function dimensions ────────────────────────────────────────────────────

FUNCTION_DIMS = {
    1: 2,
    2: 2,
    3: 3,
    4: 4,
    5: 4,
    6: 5,
    7: 6,
    8: 8,
}


# ── Round 12 configuration ─────────────────────────────────────────────────
# Lower beta = more exploitation
# Smaller step = safer final-round adjustment

FUNCTION_CONFIG = {
    1: {"beta": 1.20, "step": 0.010, "svm_percentile": 30},
    2: {"beta": 1.40, "step": 0.012, "svm_percentile": 30},
    3: {"beta": 1.60, "step": 0.012, "svm_percentile": 35},
    4: {"beta": 0.80, "step": 0.000, "svm_percentile": 25},  # return to confirmed best
    5: {"beta": 0.90, "step": 0.008, "svm_percentile": 25},  # one more careful push
    6: {"beta": 1.20, "step": 0.010, "svm_percentile": 30},
    7: {"beta": 1.00, "step": 0.010, "svm_percentile": 25},
    8: {"beta": 0.90, "step": 0.008, "svm_percentile": 25},
}


# ── Load accumulated data ──────────────────────────────────────────────────

def load_data(data_dir: str = "../data") -> dict:
    """
    Load accumulated input/output observations for each function.

    Expected file names:
        inputs_f1.npy, outputs_f1.npy
        inputs_f2.npy, outputs_f2.npy
        ...
        inputs_f8.npy, outputs_f8.npy

    If your files have different names, update the paths below.
    """
    data = {}

    for fn_id, dims in FUNCTION_DIMS.items():
        try:
            X = np.load(f"{data_dir}/inputs_f{fn_id}.npy")
            y = np.load(f"{data_dir}/outputs_f{fn_id}.npy")
        except FileNotFoundError:
            X = np.load(f"{data_dir}/initial_inputs_f{fn_id}.npy")
            y = np.load(f"{data_dir}/initial_outputs_f{fn_id}.npy")

        data[fn_id] = (X, y)

        best_idx = np.argmax(y)
        print(
            f"F{fn_id}: {len(y)} observations | "
            f"best={y[best_idx]:.6f} at {X[best_idx]}"
        )

    return data


# ── Gaussian Process surrogate ─────────────────────────────────────────────

def fit_gp(X: np.ndarray, y: np.ndarray) -> GaussianProcessRegressor:
    """
    Fit a Gaussian Process surrogate.

    Matern 2.5 is retained because it has worked consistently throughout
    the project and is flexible enough for non-linear black-box functions.
    """
    kernel = (
        ConstantKernel(1.0, (1e-3, 1e3))
        * Matern(length_scale=np.ones(X.shape[1]), nu=2.5)
        + WhiteKernel(noise_level=1e-6)
    )

    gp = GaussianProcessRegressor(
        kernel=kernel,
        normalize_y=True,
        n_restarts_optimizer=8,
        random_state=42,
    )

    gp.fit(X, y)
    return gp


# ── UCB acquisition ────────────────────────────────────────────────────────

def ucb_score(
    gp: GaussianProcessRegressor,
    candidates: np.ndarray,
    beta: float
) -> np.ndarray:
    """
    Upper Confidence Bound acquisition.

    score = predicted mean + beta * uncertainty
    """
    mean, std = gp.predict(candidates, return_std=True)
    return mean + beta * std


# ── SVM promising-region filter ────────────────────────────────────────────

def svm_filter(
    X: np.ndarray,
    y: np.ndarray,
    candidates: np.ndarray,
    percentile: int
) -> np.ndarray:
    """
    Classify top-performing observations as promising and filter candidates.

    This prevents the GP from selecting points in regions that the data
    already suggests are weak.
    """
    threshold = np.percentile(y, 100 - percentile)
    labels = (y >= threshold).astype(int)

    if labels.sum() < 2 or (1 - labels).sum() < 2:
        return np.ones(len(candidates), dtype=bool)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    candidates_scaled = scaler.transform(candidates)

    svm = SVC(kernel="rbf", C=1.0, gamma="scale")
    svm.fit(X_scaled, labels)

    return svm.predict(candidates_scaled) == 1


# ── Neural network surrogate ───────────────────────────────────────────────

class NNSurrogate(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x):
        return self.net(x)


def train_nn(
    X: np.ndarray,
    y: np.ndarray,
    epochs: int = 600,
    weight_decay: float = 1e-3
) -> NNSurrogate:
    """
    Train a small neural network surrogate.

    Used mainly for gradient direction, not as the sole decision-maker.
    """
    torch.manual_seed(42)

    model = NNSurrogate(X.shape[1])
    optimiser = torch.optim.Adam(
        model.parameters(),
        lr=0.01,
        weight_decay=weight_decay,
    )
    loss_fn = nn.MSELoss()

    X_t = torch.FloatTensor(X)
    y_t = torch.FloatTensor(y.reshape(-1, 1))

    model.train()
    for _ in range(epochs):
        optimiser.zero_grad()
        loss = loss_fn(model(X_t), y_t)
        loss.backward()
        optimiser.step()

    return model


def nn_gradient_nudge(
    model: NNSurrogate,
    x_start: np.ndarray,
    step_size: float
) -> np.ndarray:
    """
    Take a small gradient step in the direction predicted to improve output.
    """
    if step_size == 0:
        return x_start.copy()

    x_t = torch.FloatTensor(x_start).requires_grad_(True)

    model.eval()
    output = model(x_t)
    output.backward()

    grad = x_t.grad.detach().numpy()
    norm = np.linalg.norm(grad)

    if norm < 1e-8:
        return x_start.copy()

    grad = grad / norm
    x_new = x_start + step_size * grad

    return np.clip(x_new, 0.0, 1.0)


# ── Candidate generation ──────────────────────────────────────────────────

def generate_candidates(
    X: np.ndarray,
    dims: int,
    n_random: int = 15000,
    n_local: int = 5000,
    local_scale: float = 0.025
) -> np.ndarray:
    """
    Generate both global and local candidates.

    Global candidates preserve exploration.
    Local candidates focus around the current best point.
    """
    random_candidates = np.random.uniform(0.0, 1.0, (n_random, dims))

    best_region = X[-1]
    local_candidates = best_region + np.random.normal(
        0.0,
        local_scale,
        size=(n_local, dims)
    )
    local_candidates = np.clip(local_candidates, 0.0, 1.0)

    return np.vstack([random_candidates, local_candidates])


# ── Main query generation ─────────────────────────────────────────────────

def generate_query(fn_id: int, X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Generate the Round 12 query for one function.
    """
    config = FUNCTION_CONFIG[fn_id]
    dims = FUNCTION_DIMS[fn_id]

    best_idx = np.argmax(y)
    x_best = X[best_idx]

    # Special final-round rules based on observed project behaviour
    if fn_id == 4:
        # F4 was sensitive: exact confirmed best is safer than nudging
        return x_best.copy()

    if fn_id == 5:
        # F5 showed repeated improvement from pushing x1.
        # Keep other coordinates near best, gently increase x1.
        query = x_best.copy()
        query[0] = min(1.0, query[0] + 0.015)
        return query

    gp = fit_gp(X, y)

    candidates = generate_candidates(
        X=X,
        dims=dims,
        n_random=15000,
        n_local=5000,
        local_scale=0.025,
    )

    mask = svm_filter(
        X=X,
        y=y,
        candidates=candidates,
        percentile=config["svm_percentile"],
    )

    filtered = candidates[mask] if mask.sum() > 0 else candidates

    scores = ucb_score(gp, filtered, beta=config["beta"])
    gp_choice = filtered[np.argmax(scores)]

    # NN gradient refinement
    nn_model = train_nn(X, y)
    refined = nn_gradient_nudge(
        model=nn_model,
        x_start=gp_choice,
        step_size=config["step"],
    )

    # Conservative final-stage rule:
    # If the refined point moves too far from the current best, pull it back.
    distance = np.linalg.norm(refined - x_best)

    if distance > 0.12:
        refined = 0.75 * x_best + 0.25 * refined

    return np.clip(refined, 0.0, 1.0)


# ── Formatting ────────────────────────────────────────────────────────────

def format_for_portal(x: np.ndarray) -> str:
    """
    Format query for portal submission.
    """
    return "-".join(f"{v:.6f}" for v in x)


# ── Run script ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 65)
    print("BBO Round 12 — Final Refinement / Stability Strategy")
    print("=" * 65)

    np.random.seed(42)

    print("\nLoading accumulated data...\n")
    data = load_data()

    print("\nRound 12 queries for portal submission:\n")

    for fn_id, (X, y) in data.items():
        query = generate_query(fn_id, X, y)
        formatted = format_for_portal(query)

        print(f"Function {fn_id} ({FUNCTION_DIMS[fn_id]}D):")
        print(f"{formatted}\n")
