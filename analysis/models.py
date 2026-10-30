"""The models the workflow trains: each function returns a fresh, unfitted model. Built to the spec in AGENT_BRIEF.md.

    from analysis.models import MODELS
    model = MODELS["logreg"]()              # a new pipeline; analysis/evaluate.py fits it on the training rows only

Every preprocessing step (encoding, imputation, scaling) is inside the pipeline, so it learns from the
training rows only. analysis/__main__.py fits, scores and exports these; this module only builds them.
"""

from __future__ import annotations

from lightgbm import LGBMClassifier
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from analysis.data import encode


def baseline():
    """Gives every patient the training prevalence as their probability: the bar every model must beat."""
    return make_pipeline(DummyClassifier(strategy="prior"))


def logreg():
    return make_pipeline(encode(), SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=5000))


def knn():
    return make_pipeline(encode(), SimpleImputer(strategy="median"), StandardScaler(), KNeighborsClassifier(n_neighbors=25))


def rf():
    return make_pipeline(encode(), SimpleImputer(strategy="median"),
                         RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0, n_jobs=-1))


def lgbm():
    """LightGBM handles missing values itself, so it has no imputer."""
    return make_pipeline(encode(), LGBMClassifier(random_state=0, verbose=-1, n_jobs=8))


MODELS = {"baseline": baseline, "logreg": logreg, "knn": knn, "rf": rf, "lgbm": lgbm}
