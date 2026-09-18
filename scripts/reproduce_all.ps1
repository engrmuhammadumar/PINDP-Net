$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$RepoRoot = (git rev-parse --show-toplevel).Trim()
if (-not $RepoRoot) { throw "Run this script inside the Git repository." }
Set-Location $RepoRoot

python -m py_compile scripts/verify_dataset.py scripts/validate_predictions.py scripts/compute_metrics.py scripts/summarize_latency.py scripts/build_release_manifest.py scripts/prepublish_check.py

$PathConfig = "configs/dataset_paths.local.json"
if (Test-Path $PathConfig) {
    $Config = Get-Content $PathConfig -Raw | ConvertFrom-Json
    python scripts/verify_dataset.py --dataset-root $Config.dataset_root --output audits/dataset_manifest.csv --hash
} else {
    Write-Warning "Dataset check skipped: create the local path config."
}

$Oof = "predictions/pindpnet_oof_labelled.csv"
$Blind = "predictions/pindpnet_blind_c2_c3_c5.csv"
if ((Test-Path $Oof) -and (Test-Path $Blind)) {
    python scripts/validate_predictions.py --oof $Oof --blind $Blind
    python scripts/compute_metrics.py --predictions $Oof
} else {
    Write-Warning "Prediction checks skipped: final CSV files are absent."
}

$Latency = "latency/end_to_end_latency_samples.csv"
if (Test-Path $Latency) {
    python scripts/summarize_latency.py --samples $Latency
} else {
    Write-Warning "Latency check skipped: raw samples are absent."
}

python scripts/prepublish_check.py
python scripts/build_release_manifest.py
Write-Host "Verification completed."
