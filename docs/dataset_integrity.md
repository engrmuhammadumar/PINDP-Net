# Dataset Integrity Audit

The metadata-only audit covers 1,893 PHM 2010 source CSV files. It excludes
945 locally generated `.npz` files from the source-data manifest.

## Duplicate-content observation

The audited local dataset copy contains one byte-identical pair:

- `c4/c4/c_4_001.csv`
- `c4/c4/c_4_002.csv`

Both files have SHA-256:

`28ea2a40c36f8008bcfbe0de34e7fb6294c5a4442bd85fb240413dd59eba9c08`

The corresponding reference-wear records for cuts 1 and 2 are different.
The exact wear values are not reproduced in this repository.

Both source files are retained unchanged. Because both belong to cutter C4,
the duplication does not cross cutter-level training and evaluation folds.
It nevertheless creates a repeated-input/different-target observation that
must be considered when interpreting results involving C4.

This duplicate has not yet been independently verified against a canonical
archive obtained directly from the dataset provider. It is therefore reported
as an observation about the local dataset copy used for the study.

## Published audit files

- `dataset_manifest.csv`: relative filenames, sizes, and SHA-256 hashes
- `dataset_duplicate_hashes.csv`: duplicate-content records
- `dataset_integrity_summary.json`: machine-readable audit summary
