"""Create SHA-256 records for tracked release files."""
from __future__ import annotations
import argparse, csv, hashlib, subprocess
from pathlib import Path

def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("audits/release_sha256.csv"))
    args = parser.parse_args()
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    names = subprocess.check_output(["git", "ls-files"], cwd=root, text=True).splitlines()
    output = args.output.resolve()
    rows = []
    for name in names:
        path = root / name
        if path.resolve() != output and path.is_file():
            rows.append({"relative_path": path.relative_to(root).as_posix(),
                         "size_bytes": path.stat().st_size, "sha256": digest(path)})
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["relative_path", "size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Hashed {len(rows)} tracked files: {output}")

if __name__ == "__main__":
    main()
