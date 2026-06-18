"""
Round 1 — Setting the Baseline
================================
Pure random sampling. No surrogate model.

The challenge starts with ten initial observations per function (loaded from
the .npy files in data/). This script adds the first query — a deliberate
spread across the search space to see how each function responds.

At this stage there is no model to guide the search. Every input is sampled
uniformly at random from [0, 1]^n. The outputs won't all be good, and that's
the point — bad results are just as informative as good ones at this stage.
"""

import numpy as np

# ── Function definitions ───────────────────────────────────────────────────
# Each entry maps function ID → number of input dimensions.
# The functions represent real-world optimisation problems:
#   F1 (2D): Contamination source detection in a 2D radiation field
#   F2 (2D): A noisy ML model returning a log-likelihood score
#   F3 (3D): Drug compound optimisation — minimise adverse reactions
#   F4 (4D): Warehouse placement — tune a logistics model's four hyperparameters
#   F5 (4D): Chemical process yield — unimodal function with a single peak
#   F6 (5D): Recipe scoring — five ingredient amounts, total score is negative
#   F7 (6D): ML hyperparameter tuning — six parameters, maximise performance
#   F8 (8D): High-dimensional hyperparameter search

FUNCTION_DIMS = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8}


def load_initial_data(data_dir: str = "../data") -> dict:
    """
    Load the initial ten observations per function from .npy files.
    
    Returns a dict mapping function_id -> (X, y) where:
        X: np.ndarray of shape (10, dims) — input vectors
        y: np.ndarray of shape (10,)     — observed outputs
    """
    data = {}
    for fn_id in FUNCTION_DIMS:
        try:
            X = np.load(f"{data_dir}/initial_inputs_f{fn_id}.npy")
            y = np.load(f"{data_dir}/initial_outputs_f{fn_id}.npy")
            data[fn_id] = (X, y)
            print(f"  F{fn_id}: {len(y)} observations loaded, "
                  f"output range [{y.min():.4f}, {y.max():.4f}]")
        except FileNotFoundError:
            print(f"  F{fn_id}: data file not found — using placeholder")
            dims = FUNCTION_DIMS[fn_id]
            data[fn_id] = (np.random.uniform(0, 1, (10, dims)), np.random.randn(10))
    return data


def random_query(dims: int, seed: int = None) -> np.ndarray:
    """
    Sample a random point uniformly from [0, 1]^dims.
    
    This is Round 1 strategy — no model, no prior knowledge.
    Random sampling gives unbiased coverage of the search space,
    which is the right approach when you know nothing about a function.
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.uniform(0.0, 1.0, dims)


def format_for_portal(x: np.ndarray) -> str:
    """
    Format a query vector for submission to the BBO portal.
    
    The portal expects values separated by hyphens, each to 6 decimal places.
    Example: [0.5, 0.3, 0.7] -> "0.500000-0.300000-0.700000"
    """
    return "-".join(f"{v:.6f}" for v in x)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("BBO Round 1 — Random Baseline")
    print("=" * 55)
    
    print("\nLoading initial data...")
    data = load_initial_data()
    
    print("\nCurrent best per function (from initial data):")
    for fn_id, (X, y) in data.items():
        best_idx = np.argmax(y)
        print(f"  F{fn_id} ({FUNCTION_DIMS[fn_id]}D): "
              f"best = {y[best_idx]:.6e} at {X[best_idx]}")
    
    print("\nGenerating Round 1 queries (random):")
    np.random.seed(42)  # reproducible
    for fn_id, dims in FUNCTION_DIMS.items():
        query = random_query(dims)
        print(f"  F{fn_id}: {format_for_portal(query)}")
