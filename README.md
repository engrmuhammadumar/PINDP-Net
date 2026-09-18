# PINDP-Net Reproducibility Package

This repository supports verification of PINDP-Net for tool-wear prediction
and remaining-useful-life estimation using the PHM 2010 milling benchmark.

## Release status

This repository is currently a verification scaffold. It must not be described
as a complete public release until the genuine study implementation, final
configurations, prediction files, plotted values, and permitted checkpoints or
archive links have been added and independently checked.

## Dataset and access

The raw PHM 2010 files are third-party data and are not redistributed. Obtain
them from the official provider and arrange the authorized local copy with
outer directories `c1` through `c6`.

Copy `configs/dataset_paths.example.json` to
`configs/dataset_paths.local.json`, then set `dataset_root` to the authorized
local dataset directory. The local configuration is excluded from Git.

## Evaluation protocol

The labelled cutters use cutter-level outer folds:

| Evaluation cutter | Training cutters |
| --- | --- |
| C1 | C4 and C6 |
| C4 | C1 and C6 |
| C6 | C1 and C4 |

C2, C3, and C5 are blind-inference trajectories. They are excluded from
reference-dependent accuracy and calibration calculations.

All preprocessing, feature selection, model selection, calibration, and model
fitting must use only the training cutters in the applicable outer fold.

## Dataset integrity

The source-file manifest and known duplicate-content observation are documented
in [`docs/dataset_integrity.md`](docs/dataset_integrity.md).

The published audit contains relative filenames, sizes, and SHA-256 hashes, but
does not contain raw sensor measurements or private absolute dataset paths.

## Repository contents

- `src/`: genuine feature extraction, preprocessing, model, and training code
- `notebooks/`: reproducible analysis notebooks
- `configs/`: protocol, configuration, and local-path template files
- `splits/`: cutter-level split definitions
- `predictions/`: final per-pass OOF and blind predictions
- `metrics/`: reproduced metrics and diagnostic outputs
- `latency/`: end-to-end timing samples and protocol audit
- `figures/`: final manuscript figures and exact plotted values
- `audits/`: dataset-integrity and release manifests
- `scripts/`: validation and reproduction utilities
- `docs/`: schemas, availability text, integrity notes, and release checklist
- `checkpoints/`: checkpoint guidance; model binaries are ignored by default

## Computational timing

The reported 2.35 ms/sample value is model-only forward latency. It excludes
feature extraction, preprocessing, data transfer, and ensemble aggregation.

The separately measured raw-pass-to-output median is 2561.479 ms/pass on the
reported test workstation. This supports pass-level feasibility under the
tested protocol, not deterministic hard-real-time performance.

## Run verification

From PowerShell:

```powershell
python -m pip install -r requirements-verification.txt
Copy-Item configs/dataset_paths.example.json configs/dataset_paths.local.json
powershell -ExecutionPolicy Bypass -File scripts/reproduce_all.ps1
```

The local dataset configuration must be edited before running the verification.

## Required before public release

Before making the repository public, add and verify:

- The genuine feature extraction and preprocessing implementation
- The exact model, training, inference, uncertainty, and evaluation code
- Fold-specific configurations, seeds, and inner-selection splits
- Final labelled OOF and blind-inference prediction files
- Genuine direct-baseline outputs
- Exact values used in manuscript figures
- Final diagnostic and latency records
- Verified checkpoints or a durable archive link
- A source-code license
- A versioned archival release and DOI, if claimed

Never substitute synthetic, shifted, digitized, or plot-derived trajectories
for unavailable baseline outputs.

## License

A source-code license will be selected before public release. No source-code
license will grant permission to redistribute or relicense the PHM 2010
dataset.
