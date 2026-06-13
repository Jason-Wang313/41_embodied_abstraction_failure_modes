import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DOCS = ROOT / "docs"
OUT.mkdir(exist_ok=True)
DOCS.mkdir(exist_ok=True)


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


def success_for_squeeze(data, squeeze, subset):
    load = data["load"]
    mu = data["mu"]
    grasp_quality = data["grasp_quality"]
    damage = np.maximum(0.0, squeeze - (0.78 - 0.10 * load))
    slip = np.maximum(0.0, (0.30 - mu) - 0.18 * grasp_quality - 0.12 * squeeze)
    success = (damage < 0.1) & (slip <= 0.0)
    return float(success[subset].mean())


def tuned_abstraction_stress():
    data = simulate(seed=0, n=8000)
    train = np.arange(0, 4000)
    test = np.arange(4000, 8000)
    visible_goal = data["visible_goal"]

    best_constant = None
    for squeeze in np.linspace(0.10, 0.95, 171):
        policy = np.full_like(visible_goal, squeeze)
        train_success = success_for_squeeze(data, policy, train)
        if best_constant is None or train_success > best_constant["train_success"]:
            best_constant = {
                "model": "Tuned constant abstraction",
                "parameter": f"squeeze={squeeze:.3f}",
                "train_success": train_success,
                "test_success": success_for_squeeze(data, policy, test),
            }

    best_visible = None
    for intercept in np.linspace(0.10, 0.95, 86):
        for slope in np.linspace(-0.30, 0.30, 61):
            policy = np.clip(intercept + slope * (visible_goal - 0.5), 0.0, 1.0)
            train_success = success_for_squeeze(data, policy, train)
            if best_visible is None or train_success > best_visible["train_success"]:
                best_visible = {
                    "model": "Tuned visible-goal abstraction",
                    "parameter": f"intercept={intercept:.3f}; slope={slope:.3f}",
                    "train_success": train_success,
                    "test_success": success_for_squeeze(data, policy, test),
                }

    rows = [
        {
            "model": "Original abstract controller",
            "parameter": "fixed high squeeze",
            "train_success": float(data["success_abs"][train].mean()),
            "test_success": float(data["success_abs"][test].mean()),
        },
        {
            "model": "Full-state controller",
            "parameter": "uses friction/load",
            "train_success": float(data["success_full"][train].mean()),
            "test_success": float(data["success_full"][test].mean()),
        },
        best_constant,
        best_visible,
    ]

    csv_path = DOCS / "tuned_abstraction_stress.csv"
    csv_path.write_text(
        "model,parameter,train_success,test_success\n"
        + "\n".join(
            f"{row['model']},{row['parameter']},{row['train_success']:.6f},{row['test_success']:.6f}"
            for row in rows
        )
        + "\n",
        encoding="utf-8",
    )
    table_rows = [
        f"{row['model']} & {row['train_success']:.3f} & {row['test_success']:.3f} \\\\"
        for row in rows
    ]
    table = (
        "\\begin{table}[t]\n"
        "\\centering\n"
        "\\caption{V2 tuned-abstraction stress. A tuned constant abstract controller beats the full-state controller on held-out trials, invalidating the original toy evidence as support for the paper's thesis.}\n"
        "\\label{tab:tuned-abstraction}\n"
        "\\begin{tabular}{lcc}\n"
        "\\toprule\n"
        "Controller & Train success & Test success \\\\\n"
        "\\midrule\n"
        + "\n".join(table_rows)
        + "\n\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}\n"
    )
    (DOCS / "tuned_abstraction_stress_table.tex").write_text(table, encoding="utf-8")
    print(json.dumps(rows, indent=2))


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
                "Original interpretation: the abstract controller can be close in action-space to the full controller while still failing more often because the deleted variables control the feasible physical regime.",
                "",
                "## V2 tuned-abstraction stress",
                "",
                "- Original abstract controller: 0.187 held-out success",
                "- Full-state controller: 0.962 held-out success",
                "- Tuned constant abstraction: 0.987 held-out success",
                "- Tuned visible-goal abstraction: 0.987 held-out success",
                "",
                "V2 interpretation: the original toy interpretation is invalid. The environment can be solved by a tuned abstract constant action, so the old success gap reflects a weak abstract policy rather than a necessary failure of abstraction.",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    if "--stress-only" in sys.argv:
        tuned_abstraction_stress()
    else:
        main()
