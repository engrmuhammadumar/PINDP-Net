"""Reproduce cutter-wise and pooled metrics from labelled OOF predictions."""

from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def calculate(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    residual = y_pred - y_true
    return {
        "n": int(len(y_true)),
        "bias": float(np.mean(residual)),
        "mae": float(np.mean(np.abs(residual))),
        "rmse": float(np.sqrt(np.mean(np.square(residual)))),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path,
                        default=Path("metrics/reproduced_oof_metrics.csv"))
    args = parser.parse_args()
    frame = pd.read_csv(args.predictions)
    required = {"cutter", "wear_true_um", "wear_pred_um",
                "rul_true_passes", "rul_pred_passes"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    rows = []
    groups = [(str(c), g) for c, g in frame.groupby("cutter", sort=True)]
    groups.append(("POOLED", frame))
    targets = [
        ("wear", "wear_true_um", "wear_pred_um", "um"),
        ("direct_rul_head", "rul_true_passes", "rul_pred_passes", "passes"),
    ]
    for cutter, group in groups:
        for target, true_col, pred_col, unit in targets:
            result = calculate(group[true_col].to_numpy(float),
                               group[pred_col].to_numpy(float))
            rows.append({"cutter": cutter, "target": target, "unit": unit, **result})
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    result_frame = pd.DataFrame(rows)
    result_frame.to_csv(output, index=False)
    print(result_frame.to_string(index=False))
    print(f"Saved: {output.resolve()}")


if __name__ == "__main__":
    main()

