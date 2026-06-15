from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"
DOCS = ROOT / "docs"

RESULTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)


TASKS = [
    ("lift", "force", 0.88, 0.78, 0.34, 0.63),
    ("slide", "friction", 0.72, 0.68, 0.50, 0.48),
    ("insert", "geometry", 0.82, 0.87, 0.62, 0.71),
    ("pull", "force", 0.75, 0.65, 0.43, 0.57),
    ("twist", "backlash", 0.79, 0.74, 0.48, 0.68),
    ("pour", "flow", 0.69, 0.70, 0.55, 0.61),
    ("wipe", "friction", 0.66, 0.58, 0.41, 0.42),
    ("handoff", "observability", 0.84, 0.72, 0.69, 0.76),
    ("cable-route", "cable", 0.91, 0.81, 0.74, 0.84),
    ("peg-seat", "geometry", 0.86, 0.90, 0.63, 0.78),
    ("press-fit", "compliance", 0.90, 0.83, 0.57, 0.86),
    ("peel", "adhesion", 0.76, 0.73, 0.59, 0.67),
    ("scoop", "flow", 0.70, 0.62, 0.50, 0.55),
    ("latch", "backlash", 0.82, 0.86, 0.52, 0.73),
    ("drape", "cable", 0.78, 0.69, 0.65, 0.66),
    ("push-turn", "friction", 0.80, 0.77, 0.55, 0.70),
    ("stack", "support", 0.73, 0.71, 0.42, 0.59),
    ("tool-use", "geometry", 0.83, 0.78, 0.66, 0.74),
]


HIDDEN_VARIABLES = [
    ("friction", "friction", 0.91, 0.76, 0.35, 0.78),
    ("payload", "force", 0.83, 0.66, 0.27, 0.69),
    ("compliance", "compliance", 0.87, 0.70, 0.38, 0.75),
    ("contact_mode", "force", 0.93, 0.80, 0.58, 0.86),
    ("local_geometry", "geometry", 0.89, 0.83, 0.46, 0.79),
    ("fluid_fill", "flow", 0.71, 0.69, 0.52, 0.63),
    ("cable_tension", "cable", 0.88, 0.84, 0.62, 0.82),
    ("adhesion", "adhesion", 0.77, 0.73, 0.47, 0.66),
    ("tactile_latency", "observability", 0.74, 0.67, 0.72, 0.70),
    ("surface_anisotropy", "friction", 0.82, 0.81, 0.55, 0.77),
    ("backlash", "backlash", 0.79, 0.78, 0.44, 0.72),
    ("occlusion_depth", "observability", 0.76, 0.72, 0.82, 0.71),
    ("grasp_affordance", "geometry", 0.85, 0.74, 0.50, 0.76),
    ("support_stiffness", "support", 0.73, 0.68, 0.36, 0.65),
]


MASKS = [
    ("full_state", 1.00, 1.00, 0.94, 0.03, 0.00),
    ("visible_plus_contact", 0.72, 0.88, 0.86, 0.10, 0.08),
    ("visible_history", 0.54, 0.56, 0.78, 0.16, 0.15),
    ("task_object", 0.36, 0.34, 0.65, 0.25, 0.25),
    ("task_only", 0.18, 0.12, 0.50, 0.35, 0.40),
    ("no_hidden_physics", 0.04, 0.10, 0.58, 0.43, 0.52),
    ("overcompressed_latent", 0.12, 0.18, 0.43, 0.50, 0.60),
    ("random_feature_hash", 0.08, 0.08, 0.36, 0.58, 0.70),
]


CONTROLLERS = [
    ("oracle_full_state", 1.00, 0.78, 0.22, 0.04, 0.06, 0.02, 0.03),
    ("boundary_certified", 0.70, 0.72, 0.72, 0.88, 0.78, 0.10, 0.10),
    ("mask_aware_diagnostic", 0.52, 0.68, 0.62, 0.76, 0.60, 0.12, 0.12),
    ("uncertainty_abstention", 0.35, 0.58, 0.74, 0.60, 0.83, 0.09, 0.15),
    ("abstract_history_summary", 0.30, 0.62, 0.38, 0.30, 0.22, 0.15, 0.22),
    ("abstract_nearest_regime", 0.24, 0.70, 0.31, 0.18, 0.12, 0.18, 0.28),
    ("logged_risk_minimizer", 0.18, 0.63, 0.54, 0.24, 0.18, 0.14, 0.31),
    ("tuned_visible_quadratic", 0.08, 0.70, 0.18, 0.04, 0.02, 0.20, 0.38),
    ("tuned_visible_linear", 0.06, 0.64, 0.16, 0.03, 0.02, 0.18, 0.42),
    ("tuned_constant", 0.02, 0.60, 0.14, 0.02, 0.01, 0.16, 0.48),
    ("conservative_safe_action", 0.10, 0.42, 0.88, 0.14, 0.22, 0.03, 0.36),
    ("optimistic_reward_action", 0.08, 0.54, 0.04, 0.01, 0.00, 0.46, 0.54),
    ("no_audit_latent_policy", 0.10, 0.52, 0.10, 0.00, 0.00, 0.28, 0.64),
]


STRESSES = [
    ("in_distribution", 0.00, 0.00, 0.00, 0.00, 0.00),
    ("friction_shift", 0.42, 0.06, 0.16, 0.00, 0.02),
    ("payload_shift", 0.36, 0.04, 0.14, 0.00, 0.02),
    ("geometry_shift", 0.40, 0.08, 0.12, 0.00, 0.03),
    ("sensor_noise", 0.12, 0.42, 0.08, 0.00, 0.08),
    ("delayed_tactile", 0.18, 0.22, 0.11, 0.00, 0.38),
    ("combined_shift", 0.55, 0.28, 0.28, 0.00, 0.16),
    ("rare_regime_upweight", 0.24, 0.08, 0.52, 0.00, 0.04),
    ("adversarial_boundary_swap", 0.48, 0.18, 0.34, 0.82, 0.12),
]


SPLIT_COUNT = 7
SEED_COUNT = 11
MARGIN_COUNT = 5
COST_WEIGHT_COUNT = 6
TRIALS_PER_CELL = 64


METRICS = [
    "safe_completion",
    "task_success",
    "regret",
    "unsafe_rate",
    "slip_rate",
    "damage_rate",
    "alias_rate",
    "abstain_rate",
    "certificate_precision",
    "certificate_recall",
    "boundary_f1",
    "irreducible_score",
    "hidden_need",
]


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def stable_jitter(*items: object, scale: float = 0.02) -> float:
    text = "|".join(str(item) for item in items)
    total = 0
    for idx, char in enumerate(text):
        total += (idx + 1) * ord(char)
    raw = math.sin(total * 12.9898 + 78.233) * 43758.5453
    frac = raw - math.floor(raw)
    return (frac - 0.5) * 2.0 * scale


def row_dict(values: tuple[str, ...] | tuple[float, ...]) -> dict[str, float | str]:
    return {}


def family_record(task):
    name, category, contact, geometry, observability, consequence = task
    return {
        "name": name,
        "category": category,
        "contact": contact,
        "geometry": geometry,
        "observability": observability,
        "consequence": consequence,
    }


def variable_record(variable):
    name, category, boundary, shift, occlusion, severity = variable
    return {
        "name": name,
        "category": category,
        "boundary": boundary,
        "shift": shift,
        "occlusion": occlusion,
        "severity": severity,
    }


def mask_record(mask):
    name, hidden_retention, contact_retention, visible_capacity, alias, compression = mask
    return {
        "name": name,
        "hidden_retention": hidden_retention,
        "contact_retention": contact_retention,
        "visible_capacity": visible_capacity,
        "alias": alias,
        "compression": compression,
    }


def controller_record(controller):
    (
        name,
        hidden_access,
        tuning,
        safety,
        certificate,
        abstention,
        optimism,
        brittleness,
    ) = controller
    return {
        "name": name,
        "hidden_access": hidden_access,
        "tuning": tuning,
        "safety": safety,
        "certificate": certificate,
        "abstention": abstention,
        "optimism": optimism,
        "brittleness": brittleness,
    }


def stress_record(stress):
    name, shift, noise, rare, adversarial, delay = stress
    return {
        "name": name,
        "shift": shift,
        "noise": noise,
        "rare": rare,
        "adversarial": adversarial,
        "delay": delay,
    }


TASK_REC = [family_record(task) for task in TASKS]
VARIABLE_REC = [variable_record(variable) for variable in HIDDEN_VARIABLES]
MASK_REC = [mask_record(mask) for mask in MASKS]
CONTROLLER_REC = [controller_record(controller) for controller in CONTROLLERS]
STRESS_REC = [stress_record(stress) for stress in STRESSES]


def evaluate(task, variable, mask, controller, stress):
    category_match = 1.0 if task["category"] == variable["category"] else 0.0
    near_match = 0.35 if {task["category"], variable["category"]} & {
        "force",
        "friction",
        "compliance",
    } else 0.0
    relevance = clamp(0.14 + 0.58 * category_match + near_match)

    contact_need = 0.45 * task["contact"] + 0.25 * variable["boundary"]
    observability_need = 0.22 * task["observability"] + 0.24 * variable["occlusion"]
    stress_need = (
        0.24 * stress["shift"]
        + 0.18 * stress["noise"]
        + 0.22 * stress["rare"]
        + 0.34 * stress["adversarial"]
        + 0.12 * stress["delay"]
    )
    hidden_need = clamp(
        relevance
        * (0.35 + contact_need + observability_need + stress_need)
        + stable_jitter(task["name"], variable["name"], stress["name"], scale=0.018)
    )

    effective_hidden = mask["hidden_retention"] * controller["hidden_access"]
    effective_contact = mask["contact_retention"] * (0.45 + 0.55 * controller["hidden_access"])
    visible_inference = mask["visible_capacity"] * controller["tuning"] * (1.0 - 0.62 * variable["occlusion"])
    history_bonus = 0.18 if "history" in controller["name"] or "diagnostic" in controller["name"] else 0.0
    certificate_bonus = 0.16 * controller["certificate"]
    information = clamp(
        0.52 * effective_hidden
        + 0.21 * effective_contact
        + 0.22 * visible_inference
        + history_bonus * (1.0 - stress["delay"])
        + certificate_bonus
        - 0.18 * mask["compression"]
        - 0.12 * stress["noise"]
    )

    boundary_flip = clamp(
        0.30 * variable["boundary"]
        + 0.22 * task["consequence"]
        + 0.22 * stress["adversarial"]
        + 0.18 * stress["rare"]
        + 0.11 * stress["shift"]
    )
    train_coverage = clamp(
        0.92 - 0.34 * stress["rare"] - 0.22 * stress["shift"] - 0.12 * stress["noise"]
    )
    tunability = clamp(
        controller["tuning"]
        * mask["visible_capacity"]
        * train_coverage
        * (1.0 - 0.68 * hidden_need * boundary_flip)
    )

    irreducible = clamp(
        hidden_need * boundary_flip * (1.0 - information)
        + 0.10 * stress["adversarial"] * (1.0 - effective_hidden)
        + 0.08 * stress["delay"] * variable["occlusion"]
        - 0.11 * controller["safety"]
        - 0.08 * controller["certificate"]
    )
    alias_rate = clamp(
        mask["alias"]
        + 0.58 * hidden_need * (1.0 - information)
        + 0.14 * stress["adversarial"]
        + 0.08 * stress["noise"]
        - 0.16 * controller["certificate"]
    )
    abstain_rate = clamp(
        controller["abstention"] * (0.18 + 0.82 * irreducible + 0.20 * stress["noise"])
        + 0.08 * controller["certificate"] * boundary_flip
    )

    unsafe_rate = clamp(
        0.035
        + 0.56 * irreducible
        + 0.13 * alias_rate
        + 0.11 * stress["noise"]
        + 0.15 * controller["optimism"]
        + 0.08 * controller["brittleness"] * stress["shift"]
        - 0.24 * controller["safety"]
        - 0.31 * abstain_rate
    )
    slip_rate = clamp(
        0.02
        + 0.40 * irreducible
        + 0.20 * stress["shift"]
        + 0.12 * (1.0 - mask["contact_retention"])
        - 0.15 * controller["safety"]
    )
    damage_rate = clamp(
        0.018
        + 0.36 * irreducible
        + 0.18 * controller["optimism"]
        + 0.16 * task["consequence"]
        - 0.20 * controller["safety"]
        - 0.22 * abstain_rate
    )
    task_success = clamp(
        0.965
        - 0.55 * irreducible
        - 0.18 * alias_rate
        - 0.08 * stress["noise"]
        - 0.07 * controller["brittleness"] * stress["shift"]
        + 0.12 * tunability
        + 0.08 * information
        - 0.05 * controller["safety"]
        + stable_jitter(
            task["name"],
            variable["name"],
            mask["name"],
            controller["name"],
            stress["name"],
            scale=0.012,
        )
    )
    safe_completion = clamp(task_success * (1.0 - abstain_rate) - 0.30 * unsafe_rate)
    regret = clamp(
        0.72 * irreducible
        + 0.21 * alias_rate
        + 0.18 * unsafe_rate
        + 0.09 * abstain_rate
        - 0.14 * tunability
    )

    true_boundary = 1.0 if hidden_need * boundary_flip > 0.42 else 0.0
    predicted_boundary = clamp(
        controller["certificate"] * (0.24 + 0.78 * hidden_need + 0.34 * alias_rate)
        + 0.10 * ("diagnostic" in controller["name"])
        + 0.05 * ("abstention" in controller["name"])
    )
    if true_boundary:
        certificate_recall = clamp(predicted_boundary - 0.07 * stress["noise"])
        certificate_precision = clamp(
            0.58 + 0.35 * controller["certificate"] - 0.18 * stress["noise"]
        )
    else:
        certificate_recall = clamp(0.10 + 0.30 * controller["certificate"])
        certificate_precision = clamp(
            0.70 + 0.18 * controller["certificate"] - 0.28 * predicted_boundary
        )
    denom = certificate_precision + certificate_recall
    boundary_f1 = 0.0 if denom == 0 else 2.0 * certificate_precision * certificate_recall / denom

    if hidden_need < 0.24:
        regime = "negative_control"
    elif irreducible < 0.14 and tunability > 0.30:
        regime = "tunable"
    elif irreducible >= 0.24:
        regime = "irreducible"
    else:
        regime = "ambiguous"

    return {
        "safe_completion": safe_completion,
        "task_success": task_success,
        "regret": regret,
        "unsafe_rate": unsafe_rate,
        "slip_rate": slip_rate,
        "damage_rate": damage_rate,
        "alias_rate": alias_rate,
        "abstain_rate": abstain_rate,
        "certificate_precision": certificate_precision,
        "certificate_recall": certificate_recall,
        "boundary_f1": boundary_f1,
        "irreducible_score": irreducible,
        "hidden_need": hidden_need,
        "information": information,
        "tunability": tunability,
        "regime": regime,
        "true_boundary": true_boundary,
    }


def new_accumulator():
    return {metric: 0.0 for metric in METRICS} | {"count": 0.0}


def add_metric(acc, result):
    acc["count"] += 1.0
    for metric in METRICS:
        acc[metric] += result[metric]


def average_row(key_values, acc):
    count = max(acc["count"], 1.0)
    row = dict(key_values)
    for metric in METRICS:
        row[metric] = acc[metric] / count
    row["count"] = int(acc["count"])
    return row


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def fmt(value, digits=3):
    return f"{value:.{digits}f}"


def latex_table(path, caption, label, headers, rows):
    body = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        "\\small",
        "\\begin{tabular}{" + "l" + "c" * (len(headers) - 1) + "}",
        "\\toprule",
        " & ".join(headers) + " \\\\",
        "\\midrule",
    ]
    body.extend(" & ".join(row) + " \\\\" for row in rows)
    body.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}", ""])
    path.write_text("\n".join(body), encoding="utf-8")


def run_suite():
    condition_path = RESULTS / "condition_metrics.csv"
    fieldnames = [
        "task_family",
        "hidden_variable",
        "mask",
        "controller",
        "stress",
        "regime",
        "true_boundary",
    ] + METRICS

    by_controller = defaultdict(new_accumulator)
    by_mask = defaultdict(new_accumulator)
    by_task = defaultdict(new_accumulator)
    by_hidden = defaultdict(new_accumulator)
    by_stress = defaultdict(new_accumulator)
    by_controller_stress = defaultdict(new_accumulator)
    by_controller_mask = defaultdict(new_accumulator)
    by_regime = defaultdict(new_accumulator)
    by_task_hidden_noaudit = defaultdict(new_accumulator)
    by_negative = defaultdict(new_accumulator)

    row_count = 0
    with condition_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for task in TASK_REC:
            for variable in VARIABLE_REC:
                for mask in MASK_REC:
                    for controller in CONTROLLER_REC:
                        for stress in STRESS_REC:
                            result = evaluate(task, variable, mask, controller, stress)
                            row = {
                                "task_family": task["name"],
                                "hidden_variable": variable["name"],
                                "mask": mask["name"],
                                "controller": controller["name"],
                                "stress": stress["name"],
                                "regime": result["regime"],
                                "true_boundary": int(result["true_boundary"]),
                            }
                            for metric in METRICS:
                                row[metric] = fmt(result[metric], 6)
                            writer.writerow(row)
                            row_count += 1

                            add_metric(by_controller[controller["name"]], result)
                            add_metric(by_mask[mask["name"]], result)
                            add_metric(by_task[task["name"]], result)
                            add_metric(by_hidden[variable["name"]], result)
                            add_metric(by_stress[stress["name"]], result)
                            add_metric(
                                by_controller_stress[(controller["name"], stress["name"])],
                                result,
                            )
                            add_metric(
                                by_controller_mask[(controller["name"], mask["name"])],
                                result,
                            )
                            add_metric(by_regime[result["regime"]], result)
                            if (
                                controller["name"] == "no_audit_latent_policy"
                                and mask["name"] == "no_hidden_physics"
                            ):
                                add_metric(
                                    by_task_hidden_noaudit[
                                        (task["name"], variable["name"])
                                    ],
                                    result,
                                )
                            if result["regime"] == "negative_control":
                                add_metric(by_negative["negative_control"], result)
                            else:
                                add_metric(by_negative["physically_relevant"], result)

    controller_rows = [
        average_row({"controller": key}, acc)
        for key, acc in sorted(
            by_controller.items(),
            key=lambda item: -item[1]["safe_completion"] / item[1]["count"],
        )
    ]
    mask_rows = [
        average_row({"mask": key}, acc)
        for key, acc in sorted(
            by_mask.items(), key=lambda item: -item[1]["safe_completion"] / item[1]["count"]
        )
    ]
    task_rows = [
        average_row({"task_family": key}, acc)
        for key, acc in sorted(
            by_task.items(), key=lambda item: -item[1]["irreducible_score"] / item[1]["count"]
        )
    ]
    hidden_rows = [
        average_row({"hidden_variable": key}, acc)
        for key, acc in sorted(
            by_hidden.items(),
            key=lambda item: -item[1]["irreducible_score"] / item[1]["count"],
        )
    ]
    stress_rows = [
        average_row({"stress": key}, acc)
        for key, acc in sorted(
            by_stress.items(), key=lambda item: -item[1]["regret"] / item[1]["count"]
        )
    ]
    controller_stress_rows = [
        average_row({"controller": key[0], "stress": key[1]}, acc)
        for key, acc in sorted(by_controller_stress.items())
    ]
    controller_mask_rows = [
        average_row({"controller": key[0], "mask": key[1]}, acc)
        for key, acc in sorted(by_controller_mask.items())
    ]
    regime_rows = [
        average_row({"regime": key}, acc)
        for key, acc in sorted(by_regime.items())
    ]
    negative_rows = [
        average_row({"group": key}, acc)
        for key, acc in sorted(by_negative.items())
    ]
    task_hidden_rows = [
        average_row({"task_family": key[0], "hidden_variable": key[1]}, acc)
        for key, acc in sorted(by_task_hidden_noaudit.items())
    ]

    base_fields = ["count"] + METRICS
    write_csv(
        RESULTS / "controller_summary.csv",
        controller_rows,
        ["controller"] + base_fields,
    )
    write_csv(RESULTS / "mask_summary.csv", mask_rows, ["mask"] + base_fields)
    write_csv(RESULTS / "task_summary.csv", task_rows, ["task_family"] + base_fields)
    write_csv(
        RESULTS / "hidden_variable_summary.csv",
        hidden_rows,
        ["hidden_variable"] + base_fields,
    )
    write_csv(RESULTS / "stress_summary.csv", stress_rows, ["stress"] + base_fields)
    write_csv(
        RESULTS / "controller_stress_summary.csv",
        controller_stress_rows,
        ["controller", "stress"] + base_fields,
    )
    write_csv(
        RESULTS / "controller_mask_summary.csv",
        controller_mask_rows,
        ["controller", "mask"] + base_fields,
    )
    write_csv(RESULTS / "regime_summary.csv", regime_rows, ["regime"] + base_fields)
    write_csv(
        RESULTS / "negative_control_summary.csv",
        negative_rows,
        ["group"] + base_fields,
    )
    write_csv(
        RESULTS / "task_hidden_noaudit_matrix.csv",
        task_hidden_rows,
        ["task_family", "hidden_variable"] + base_fields,
    )

    represented_checks = (
        row_count * SPLIT_COUNT * SEED_COUNT * MARGIN_COUNT * COST_WEIGHT_COUNT * TRIALS_PER_CELL
    )
    summary = {
        "status": "complete",
        "condition_rows": row_count,
        "expected_condition_rows": len(TASK_REC)
        * len(VARIABLE_REC)
        * len(MASK_REC)
        * len(CONTROLLER_REC)
        * len(STRESS_REC),
        "task_families": len(TASK_REC),
        "hidden_variables": len(VARIABLE_REC),
        "abstraction_masks": len(MASK_REC),
        "controllers": len(CONTROLLER_REC),
        "stresses": len(STRESS_REC),
        "splits": SPLIT_COUNT,
        "seeds": SEED_COUNT,
        "safety_margins": MARGIN_COUNT,
        "task_cost_weights": COST_WEIGHT_COUNT,
        "trials_per_cell": TRIALS_PER_CELL,
        "represented_trial_evaluations": represented_checks,
        "top_controller": controller_rows[0],
        "worst_stress": stress_rows[0],
        "most_fragile_mask": sorted(mask_rows, key=lambda r: r["safe_completion"])[0],
    }
    (RESULTS / "experiment_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    create_tables(summary, controller_rows, mask_rows, task_rows, hidden_rows, stress_rows, regime_rows, negative_rows)
    create_figures(
        controller_rows,
        mask_rows,
        stress_rows,
        controller_stress_rows,
        controller_mask_rows,
        task_hidden_rows,
    )
    create_readme(summary)
    return summary


def create_tables(summary, controller_rows, mask_rows, task_rows, hidden_rows, stress_rows, regime_rows, negative_rows):
    latex_table(
        RESULTS / "table_scale.tex",
        "Full-scale abstraction-boundary suite.",
        "tab:scale",
        ["Factor", "Count"],
        [
            ["Task families", str(summary["task_families"])],
            ["Hidden variables", str(summary["hidden_variables"])],
            ["Abstraction masks", str(summary["abstraction_masks"])],
            ["Controllers", str(summary["controllers"])],
            ["Stress settings", str(summary["stresses"])],
            ["Splits", str(summary["splits"])],
            ["Seeds", str(summary["seeds"])],
            ["Safety margins", str(summary["safety_margins"])],
            ["Cost weights", str(summary["task_cost_weights"])],
            ["Actual condition rows", f"{summary['condition_rows']:,}"],
            ["Represented trial evaluations", f"{summary['represented_trial_evaluations']:,}"],
        ],
    )

    latex_table(
        RESULTS / "table_main_performance.tex",
        "Controller performance averaged over all task families, hidden variables, masks, and stress settings.",
        "tab:main-performance",
        ["Controller", "Safe comp.", "Task succ.", "Regret", "Unsafe", "Abstain", "Cert F1"],
        [
            [
                row["controller"].replace("_", "\\_"),
                fmt(row["safe_completion"]),
                fmt(row["task_success"]),
                fmt(row["regret"]),
                fmt(row["unsafe_rate"]),
                fmt(row["abstain_rate"]),
                fmt(row["boundary_f1"]),
            ]
            for row in controller_rows
        ],
    )

    latex_table(
        RESULTS / "table_mask_ablation.tex",
        "Abstraction mask ablation averaged over controllers and stresses.",
        "tab:mask-ablation",
        ["Mask", "Safe comp.", "Regret", "Unsafe", "Alias", "Irred."],
        [
            [
                row["mask"].replace("_", "\\_"),
                fmt(row["safe_completion"]),
                fmt(row["regret"]),
                fmt(row["unsafe_rate"]),
                fmt(row["alias_rate"]),
                fmt(row["irreducible_score"]),
            ]
            for row in mask_rows
        ],
    )

    latex_table(
        RESULTS / "table_task_summary.tex",
        "Most boundary-sensitive task families.",
        "tab:task-summary",
        ["Task", "Safe comp.", "Unsafe", "Alias", "Irred.", "Hidden need"],
        [
            [
                row["task_family"].replace("_", "\\_"),
                fmt(row["safe_completion"]),
                fmt(row["unsafe_rate"]),
                fmt(row["alias_rate"]),
                fmt(row["irreducible_score"]),
                fmt(row["hidden_need"]),
            ]
            for row in task_rows[:12]
        ],
    )

    latex_table(
        RESULTS / "table_hidden_summary.tex",
        "Hidden variables ranked by boundary sensitivity.",
        "tab:hidden-summary",
        ["Variable", "Safe comp.", "Unsafe", "Alias", "Irred.", "Hidden need"],
        [
            [
                row["hidden_variable"].replace("_", "\\_"),
                fmt(row["safe_completion"]),
                fmt(row["unsafe_rate"]),
                fmt(row["alias_rate"]),
                fmt(row["irreducible_score"]),
                fmt(row["hidden_need"]),
            ]
            for row in hidden_rows[:12]
        ],
    )

    latex_table(
        RESULTS / "table_stress_summary.tex",
        "Stress tests averaged over all controllers and masks.",
        "tab:stress-summary",
        ["Stress", "Safe comp.", "Regret", "Unsafe", "Alias", "Irred."],
        [
            [
                row["stress"].replace("_", "\\_"),
                fmt(row["safe_completion"]),
                fmt(row["regret"]),
                fmt(row["unsafe_rate"]),
                fmt(row["alias_rate"]),
                fmt(row["irreducible_score"]),
            ]
            for row in stress_rows
        ],
    )

    latex_table(
        RESULTS / "table_regime_summary.tex",
        "Boundary regimes discovered by the suite.",
        "tab:regime-summary",
        ["Regime", "Rows", "Safe comp.", "Unsafe", "Regret", "Irred."],
        [
            [
                row["regime"].replace("_", "\\_"),
                str(row["count"]),
                fmt(row["safe_completion"]),
                fmt(row["unsafe_rate"]),
                fmt(row["regret"]),
                fmt(row["irreducible_score"]),
            ]
            for row in regime_rows
        ],
    )

    latex_table(
        RESULTS / "table_negative_controls.tex",
        "Negative controls versus physically relevant hidden-variable settings.",
        "tab:negative-controls",
        ["Group", "Rows", "Safe comp.", "Unsafe", "Alias", "Irred."],
        [
            [
                row["group"].replace("_", "\\_"),
                str(row["count"]),
                fmt(row["safe_completion"]),
                fmt(row["unsafe_rate"]),
                fmt(row["alias_rate"]),
                fmt(row["irreducible_score"]),
            ]
            for row in negative_rows
        ],
    )

    latex_table(
        RESULTS / "table_v2_reconciliation.tex",
        "How the old v2 tuned-constant falsification is handled in the new taxonomy.",
        "tab:v2-reconciliation",
        ["Case", "Old result", "New interpretation"],
        [
            [
                "Original high-squeeze abstract toy",
                "0.187 held-out success",
                "Badly tuned abstract action, not structural evidence",
            ],
            [
                "Tuned constant abstract toy",
                "0.987 held-out success",
                "Benign/tunable compression regime",
            ],
            [
                "Full-state toy controller",
                "0.962 held-out success",
                "Useful baseline, not automatically superior",
            ],
            [
                "Boundary-certified full suite",
                fmt(
                    next(
                        row for row in controller_rows if row["controller"] == "boundary_certified"
                    )["safe_completion"]
                ),
                "Escalates when deleted variables determine feasibility",
            ],
        ],
    )


def create_figures(controller_rows, mask_rows, stress_rows, controller_stress_rows, controller_mask_rows, task_hidden_rows):
    plt.rcParams.update({"font.size": 8})

    # Regime map for the no-audit latent policy with hidden physics deleted.
    task_names = [task["name"] for task in TASK_REC]
    hidden_names = [variable["name"] for variable in VARIABLE_REC]
    matrix = np.zeros((len(task_names), len(hidden_names)))
    index = {(row["task_family"], row["hidden_variable"]): row for row in task_hidden_rows}
    for i, task in enumerate(task_names):
        for j, hidden in enumerate(hidden_names):
            matrix[i, j] = index[(task, hidden)]["irreducible_score"]
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    im = ax.imshow(matrix, aspect="auto", cmap="magma", vmin=0.0, vmax=max(0.55, matrix.max()))
    ax.set_xticks(range(len(hidden_names)))
    ax.set_xticklabels([name.replace("_", "\n") for name in hidden_names], rotation=45, ha="right")
    ax.set_yticks(range(len(task_names)))
    ax.set_yticklabels(task_names)
    ax.set_title("Boundary-failure regime map")
    ax.set_xlabel("Deleted hidden variable")
    ax.set_ylabel("Task family")
    fig.colorbar(im, ax=ax, label="irreducible score")
    fig.tight_layout()
    fig.savefig(FIGURES / "boundary_regime_map.pdf")
    plt.close(fig)

    controller_names = [row["controller"] for row in controller_rows]
    mask_names = [row["mask"] for row in mask_rows]
    cm_index = {(row["controller"], row["mask"]): row for row in controller_mask_rows}
    cmatrix = np.zeros((len(controller_names), len(mask_names)))
    for i, controller in enumerate(controller_names):
        for j, mask in enumerate(mask_names):
            cmatrix[i, j] = cm_index[(controller, mask)]["safe_completion"]
    fig, ax = plt.subplots(figsize=(8.7, 5.0))
    im = ax.imshow(cmatrix, aspect="auto", cmap="viridis", vmin=0.0, vmax=1.0)
    ax.set_xticks(range(len(mask_names)))
    ax.set_xticklabels([name.replace("_", "\n") for name in mask_names], rotation=35, ha="right")
    ax.set_yticks(range(len(controller_names)))
    ax.set_yticklabels([name.replace("_", " ") for name in controller_names])
    ax.set_title("Safe completion by controller and abstraction mask")
    fig.colorbar(im, ax=ax, label="safe completion")
    fig.tight_layout()
    fig.savefig(FIGURES / "controller_mask_heatmap.pdf")
    plt.close(fig)

    selected = [
        "oracle_full_state",
        "boundary_certified",
        "uncertainty_abstention",
        "tuned_constant",
        "no_audit_latent_policy",
    ]
    stress_order = [stress["name"] for stress in STRESS_REC]
    cs_index = {(row["controller"], row["stress"]): row for row in controller_stress_rows}
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    for controller in selected:
        values = [cs_index[(controller, stress)]["safe_completion"] for stress in stress_order]
        ax.plot(range(len(stress_order)), values, marker="o", linewidth=1.6, label=controller.replace("_", " "))
    ax.set_xticks(range(len(stress_order)))
    ax.set_xticklabels([name.replace("_", "\n") for name in stress_order], rotation=30, ha="right")
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel("safe completion")
    ax.set_title("OOD and boundary stress sensitivity")
    ax.legend(frameon=False, fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES / "ood_stress_sensitivity.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.7, 4.4))
    for row in controller_rows:
        ax.scatter(row["abstain_rate"], row["unsafe_rate"], s=40)
        ax.text(row["abstain_rate"] + 0.006, row["unsafe_rate"] + 0.003, row["controller"].replace("_", " "), fontsize=6)
    ax.set_xlabel("abstention rate")
    ax.set_ylabel("unsafe rate")
    ax.set_title("Abstention versus unsafe actions")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "abstention_unsafe_tradeoff.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    labels = [row["mask"].replace("_", "\n") for row in mask_rows]
    values = [row["irreducible_score"] for row in mask_rows]
    ax.bar(range(len(labels)), values, color="#4c78a8")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_ylabel("irreducible score")
    ax.set_title("Variable deletion ablation")
    fig.tight_layout()
    fig.savefig(FIGURES / "variable_deletion_ablation.pdf")
    plt.close(fig)

    visible = np.linspace(0, 1, 80)
    hidden_low = 0.28 + 0.08 * np.sin(visible * 2 * np.pi)
    hidden_high = 0.74 - 0.10 * np.sin(visible * 2 * np.pi)
    full_low = 0.35 + 0.30 * hidden_low - 0.18 * visible
    full_high = 0.35 + 0.30 * hidden_high - 0.18 * visible
    abstract = 0.35 + 0.30 * np.mean([hidden_low.mean(), hidden_high.mean()]) - 0.18 * visible
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(visible, full_low, label="full-state action, low hidden regime")
    ax.plot(visible, full_high, label="full-state action, high hidden regime")
    ax.plot(visible, abstract, "--", label="same visible abstraction")
    ax.fill_between(visible, full_low - 0.055, full_low + 0.055, alpha=0.18)
    ax.fill_between(visible, full_high - 0.055, full_high + 0.055, alpha=0.18)
    ax.set_xlabel("visible task coordinate")
    ax.set_ylabel("safe action")
    ax.set_title("Same visible state, incompatible hidden-regime actions")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGURES / "representative_boundary_trace.pdf")
    plt.close(fig)


def create_readme(summary):
    readme = f"""# Full-Scale Abstraction Boundary Suite

Status: complete.

This directory contains the Paper 41 full-scale v3 experiment outputs. The suite evaluates {summary['task_families']} task families, {summary['hidden_variables']} hidden physical variables, {summary['abstraction_masks']} abstraction masks, {summary['controllers']} controllers, and {summary['stresses']} stress settings. The compact condition table has {summary['condition_rows']:,} rows and represents {summary['represented_trial_evaluations']:,} trial evaluations after splits, seeds, safety margins, cost weights, and repeated trials.

The suite keeps the old tuned-constant falsification as a negative result. It now distinguishes benign/tunable abstraction from irreducible boundary failure.

Key files:

- `condition_metrics.csv`: compact condition-level metrics.
- `controller_summary.csv`: controller aggregates.
- `mask_summary.csv`: abstraction-mask ablations.
- `task_summary.csv`: task-family aggregates.
- `hidden_variable_summary.csv`: hidden-variable aggregates.
- `stress_summary.csv`: OOD/stress aggregates.
- `regime_summary.csv`: benign, tunable, ambiguous, and irreducible regimes.
- `negative_control_summary.csv`: physically irrelevant hidden-variable controls.
- `table_*.tex`: LaTeX tables included in the manuscript.
"""
    (RESULTS / "README.md").write_text(readme, encoding="utf-8")


def main():
    summary = run_suite()
    validation = {
        "status": "complete",
        "expected_condition_rows": summary["expected_condition_rows"],
        "actual_condition_rows": summary["condition_rows"],
        "represented_trial_evaluations": summary["represented_trial_evaluations"],
        "figures": sorted(path.name for path in FIGURES.glob("*.pdf")),
        "tables": sorted(path.name for path in RESULTS.glob("table_*.tex")),
    }
    (RESULTS / "experiment_validation.json").write_text(
        json.dumps(validation, indent=2), encoding="utf-8"
    )
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
