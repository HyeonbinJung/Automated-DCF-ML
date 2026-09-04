import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV, ElasticNetCV

def make_models(random_state=42):
    return {
        "Ridge": Pipeline([
            ("scaler", StandardScaler()),
            ("model", RidgeCV(alphas=np.logspace(-4, 3, 30)))
        ]),
        "ElasticNet": Pipeline([
            ("scaler", StandardScaler()),
            ("model", ElasticNetCV(
                alphas=np.logspace(-4, 0.5, 20),
                l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9],
                cv=5,
                max_iter=20000,
                random_state=random_state
            ))
        ])
    }
