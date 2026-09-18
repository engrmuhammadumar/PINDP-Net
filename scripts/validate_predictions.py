"""Validate labelled OOF and blind prediction CSV files."""

from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

OOF_COLUMNS = {"cutter", "pass", "wear_true_um", "wear_pred_um",
               "rul_true_passes", "rul_pred_passes"}
BLIND_COLUMNS = {"cutter", "pass", "wear_pred_um", "rul_pred_passes"}
LABELLED = {"C1", "C4", "C6"}
BLIND = {"C2", "C3", "C5"}


def validate(path: Path, mode: str) -> None:
    frame = pd.read_csv(path)
    required = OOF_COLUMNS if mode == "oof" else BLIND_COLUMNS
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"{path}: missing columns: {missing}")
    frame["cutter"] = frame["cutter"].astype(str).str.upper()
    expected = LABELLED if mode == "oof" else BLIND
    actual = set(frame["cutter"].unique())
    if actual != expected:
        raise ValueError(f"{path}: expected {sorted(expected)}, got {sorted(actual)}")
    if frame.duplicated(["cutter", "pass"]).any():
        raise ValueError(f"{path}: duplicate cutter/pass rows")
    numeric = sorted(required - {"cutter"})
    values = frame[numeric].apply(pd.to_numeric, errors="coerce").to_numpy(float)
    if not np.isfinite(values).all() or (frame["pass"] < 1).any():
        raise ValueError(f"{path}: invalid required numeric values")
    if mode == "blind":
        forbidden = {"wear_true_um", "rul_true_passes",
                     "wear_reference_um", "rul_reference_passes"}
        leaked = sorted(forbidden & set(frame.columns))
        if leaked:
            raise ValueError(f"{path}: blind reference columns: {leaked}")
    print(f"PASS: {path} ({len(frame)} rows)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--oof", type=Path)
    parser.add_argument("--blind", type=Path)
    args = parser.parse_args()
    if not args.oof and not args.blind:
        parser.error("provide --oof and/or --blind")
    if args.oof:
        validate(args.oof, "oof")
    if args.blind:
        validate(args.blind, "blind")


if __name__ == "__main__":
    main()
