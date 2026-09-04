import numpy as np
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def direction_accuracy(y_true, y_pred, current):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    current = np.asarray(current)
    return float((np.sign(y_true-current) == np.sign(y_pred-current)).mean())

def evaluate(y_true, y_pred, current):
    r2 = float(r2_score(y_true, y_pred))
    pearson = float(pearsonr(y_true, y_pred).statistic)
    spearman = float(spearmanr(y_true, y_pred).statistic)
    da = direction_accuracy(y_true, y_pred, current)
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(mean_squared_error(y_true, y_pred) ** 0.5)

    # Project-specific composite, NOT an industry-standard statistic.
    corr_accuracy_index = 100 * (
        0.35 * ((pearson + 1) / 2) +
        0.25 * ((spearman + 1) / 2) +
        0.25 * da +
        0.15 * max(0, min(1, r2))
    )

    return {
        "R2": r2,
        "Pearson_r": pearson,
        "Spearman_rho": spearman,
        "Direction_Accuracy": da,
        "MAE": mae,
        "RMSE": rmse,
        "Correlation_Accuracy_Index": corr_accuracy_index,
    }
