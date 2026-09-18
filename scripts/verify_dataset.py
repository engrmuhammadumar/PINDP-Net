"""Create a metadata manifest for locally obtained PHM 2010 source files."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

CUTTERS = ("c1", "c2", "c3", "c4", "c5", "c6")
RAW_SUFFIXES = frozenset({".csv", ".wfs"})


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 digest of a file."""
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)

    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Create a metadata manifest for local PHM 2010 source files. "
            "Derived and unsupported file types are skipped."
        )
    )
    parser.add_argument(
        "--dataset-root",
        type=Path,
        required=True,
        help="Local PHM 2010 dataset directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("audits/dataset_manifest.csv"),
        help="Destination CSV manifest.",
    )
    parser.add_argument(
        "--hash",
        action="store_true",
        help="Calculate SHA-256 hashes; this may take considerable time.",
    )
    args = parser.parse_args()

    root = args.dataset_root.expanduser().resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Dataset directory not found: {root}")

    missing = [name for name in CUTTERS if not (root / name).is_dir()]
    if missing:
        raise FileNotFoundError(
            "Missing cutter directories: " + ", ".join(missing)
        )

    rows = []
    included_counts = {}
    skipped_counts = {}

    for cutter in CUTTERS:
        cutter_directory = root / cutter
        all_files = sorted(
            path for path in cutter_directory.rglob("*") if path.is_file()
        )
        source_files = [
            path
            for path in all_files
            if path.suffix.lower() in RAW_SUFFIXES
        ]

        if not source_files:
            raise FileNotFoundError(
                f"No supported source files found in: {cutter_directory}"
            )

        included_counts[cutter] = len(source_files)
        skipped_counts[cutter] = len(all_files) - len(source_files)

        for path in source_files:
            rows.append(
                {
                    "cutter": cutter.upper(),
                    "relative_path": path.relative_to(root).as_posix(),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256_file(path) if args.hash else "",
                }
            )

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "cutter",
                "relative_path",
                "size_bytes",
                "sha256",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset root: {root}")
    print(f"Included extensions: {', '.join(sorted(RAW_SUFFIXES))}")

    for cutter in CUTTERS:
        print(
            f"{cutter.upper()}: "
            f"included={included_counts[cutter]}, "
            f"skipped={skipped_counts[cutter]}"
        )

    print(f"Source files included: {len(rows)}")
    print(f"Other files skipped: {sum(skipped_counts.values())}")
    print(f"Manifest saved: {output}")

    if not args.hash:
        print("SHA-256 calculation skipped. Add --hash to generate hashes.")


if __name__ == "__main__":
    main()
