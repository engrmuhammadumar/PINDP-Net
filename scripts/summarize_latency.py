"""Recompute latency summary statistics from released raw samples."""

from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--output", type=Path,
                        default=Path("latency/reproduced_latency_summary.json"))
    args = parser.parse_args()
    frame = pd.read_csv(args.samples)
    if "latency_ms" not in frame:
        raise ValueError("Expected a latency_ms column")
    values = pd.to_numeric(frame["latency_ms"], errors="raise").to_numpy(float)
    if len(values) < 2 or not np.isfinite(values).all() or (values <= 0).any():
        raise ValueError("Need at least two finite positive samples")
    summary = {
        "n": int(len(values)),
        "mean_ms": float(np.mean(values)),
        "sd_ms": float(np.std(values, ddof=1)),
        "median_ms": float(np.median(values)),
        "p95_ms": float(np.percentile(values, 95)),
        "p99_ms": float(np.percentile(values, 99)),
        "minimum_ms": float(np.min(values)),
        "maximum_ms": float(np.max(values)),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

