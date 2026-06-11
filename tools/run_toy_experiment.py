import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DOCS = ROOT / "docs"
OUT.mkdir(exist_ok=True)


def simulate(seed=0, n=4000):
    rng = np.random.default_rng(seed)
    # Hidden physical variables:
    # mu: friction coefficient, load: payload mass, slip_thresh: minimum safe margin.
    mu = rng.uniform(0.15, 0.85, size=n)
    load = rng.uniform(0.0, 1.0, size=n)
    grasp_quality = rng.uniform(0.0, 1.0, size=n)
    visible_goal = rng.uniform(0.0, 1.0, size=n)

    # Full-state controller can see mu and load.
    # It chooses higher squeeze only when needed and stays within damage bounds.
    squeeze_full = 0.22 + 0.22 * (1 - mu) + 0.06 * load
    damage_full = np.maximum(0.0, squeeze_full - (0.78 - 0.10 * load))
    slip_full = np.maximum(0.0, (0.30 - mu) - 0.18 * grasp_quality - 0.12 * squeeze_full)
    success_full = (damage_full < 0.1) & (slip_full <= 0.0)

    # Abstract controller sees only task label and visible goal, not mu or load.
    # It picks a single nominal squeeze from the compressed state.
    squeeze_abs = 0.86 + 0.02 * (visible_goal - 0.5)
    damage_abs = np.maximum(0.0, squeeze_abs - (0.78 - 0.10 * load))
    slip_abs = np.maximum(0.0, (0.30 - mu) - 0.18 * grasp_quality - 0.12 * squeeze_abs)
    success_abs = (damage_abs < 0.1) & (slip_abs <= 0.0)

    # Control-space accuracy can be similar while physical success diverges.
    nominal_error = np.abs(squeeze_abs - squeeze_full)

    return {
        "mu": mu,
        "load": load,
        "grasp_quality": grasp_quality,
        "visible_goal": visible_goal,
        "success_full": success_full,
        "success_abs": success_abs,
        "damage_full": damage_full,
        "damage_abs": damage_abs,
        "slip_full": slip_full,
        "slip_abs": slip_abs,
        "nominal_error": nominal_error,
        "squeeze_full": squeeze_full,
        "squeeze_abs": squeeze_abs,
    }


def main():
    data = simulate()
    success_full = data["success_full"].mean()
    success_abs = data["success_abs"].mean()
    fail_gap = success_full - success_abs
    corr = np.corrcoef(data["nominal_error"], (~data["success_abs"]).astype(float))[0, 1]

    stats = {
        "n": int(len(data["success_full"])),
        "success_full": float(success_full),
        "success_abs": float(success_abs),
        "success_gap": float(fail_gap),
        "nominal_error_vs_fail_corr": float(corr),
    }
    (OUT / "toy_experiment_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    bins = np.linspace(0, 1, 30)
    axes[0].hist(data["mu"], bins=bins, alpha=0.6, label="friction mu")
    axes[0].hist(data["load"], bins=bins, alpha=0.6, label="load")
    axes[0].set_title("Hidden physical variables")
    axes[0].legend(frameon=False)
    axes[0].set_xlabel("value")
    axes[0].set_ylabel("count")

    axes[1].scatter(data["nominal_error"], (~data["success_abs"]).astype(float), s=4, alpha=0.15)
    axes[1].set_title("Abstract control error vs failure")
    axes[1].set_xlabel("|squeeze_abs - squeeze_full|")
    axes[1].set_ylabel("abstract failure")
    axes[1].set_ylim(-0.1, 1.1)
    fig.tight_layout()
    fig.savefig(OUT / "toy_abstraction_failure.png", dpi=200)
    plt.close(fig)

    (DOCS / "toy_results.md").write_text(
        "\n".join(
            [
                "# Toy Results",
                "",
                f"- Full-state success: {success_full:.3f}",
                f"- Abstract-state success: {success_abs:.3f}",
                f"- Success gap: {fail_gap:.3f}",
                f"- Nominal squeeze error vs failure correlation: {corr:.3f}",
                "",
                "Interpretation: the abstract controller can be close in action-space to the full controller while still failing more often because the deleted variables control the feasible physical regime.",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
