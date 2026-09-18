# Prediction-file schema

The labelled OOF CSV requires: cutter, pass, wear_true_um, wear_pred_um,
rul_true_passes, and rul_pred_passes. It must contain C1, C4, and C6 exactly,
with one row per cutter/pass pair.

The blind CSV requires: cutter, pass, wear_pred_um, and rul_pred_passes. It must
contain C2, C3, and C5 exactly. Do not add reference-label columns to the blind
file.

Recommended provenance columns include outer_fold, ensemble_seed, and
source_prediction_file. Each held-out prediction must originate only from
models that did not train or select hyperparameters using that cutter.

