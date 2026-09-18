"""Fail on common privacy and GitHub-release problems."""
from __future__ import annotations
import argparse, re, subprocess
from pathlib import Path

TEXT = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".tsv", ".ps1", ".toml"}
PATTERNS = {
    "Windows absolute path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
    "GitHub token": re.compile(r"gh[opsu]_[A-Za-z0-9_]{20,}"),
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-mb", type=float, default=90.0)
    args = parser.parse_args()
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    names = subprocess.check_output(["git", "ls-files"], cwd=root, text=True).splitlines()
    failures = []
    for name in names:
        path = root / name
        if not path.is_file():
            continue
        size_mb = path.stat().st_size / 1024**2
        if size_mb > args.max_mb:
            failures.append(f"{name}: {size_mb:.1f} MB")
        if path.suffix.lower() in TEXT:
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                failures.append(f"{name}: invalid UTF-8")
                continue
            for label, pattern in PATTERNS.items():
                if pattern.search(content):
                    failures.append(f"{name}: contains {label}")
    prohibited = {"data", "dataset", "datasets", "raw", "raw_data"}
    for name in names:
        if prohibited & set(Path(name).parts):
            failures.append(f"{name}: raw-data directory is tracked")
    if failures:
        print("PRE-PUBLICATION CHECK FAILED")
        for failure in failures:
            print(" - " + failure)
        raise SystemExit(1)
    print("PRE-PUBLICATION CHECK PASSED")

if __name__ == "__main__":
    main()
