from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

LIKERT_COLUMNS = [
    "content_quality_q1",
    "content_quality_q2",
    "ui_usability_q1",
    "ui_usability_q2",
    "teacher_student_q1",
    "teacher_student_q2",
    "peer_q1",
    "peer_q2",
    "motivation_q1",
    "motivation_q2",
    "autonomy_q1",
    "autonomy_q2",
    "accessibility_q1",
    "reliability_q1",
    "instructor_support_q1",
    "instructor_support_q2",
    "satisfaction_q1",
    "satisfaction_q2",
]

NUMERIC_COLUMNS = ["achievement_score"]

FACTOR_ITEMS: Dict[str, List[str]] = {
    "content_quality": ["content_quality_q1", "content_quality_q2"],
    "ui_usability": ["ui_usability_q1", "ui_usability_q2"],
    "teacher_student_interaction": ["teacher_student_q1", "teacher_student_q2"],
    "peer_interaction": ["peer_q1", "peer_q2"],
    "motivation": ["motivation_q1", "motivation_q2"],
    "autonomy": ["autonomy_q1", "autonomy_q2"],
    "accessibility": ["accessibility_q1"],
    "reliability": ["reliability_q1"],
    "instructor_support": ["instructor_support_q1", "instructor_support_q2"],
    "satisfaction": ["satisfaction_q1", "satisfaction_q2"],
}

DIMENSION_FACTORS: Dict[str, List[str]] = {
    "platform_design": ["content_quality", "ui_usability"],
    "interaction": ["teacher_student_interaction", "peer_interaction"],
    "engagement": ["motivation", "autonomy"],
    "technical": ["accessibility", "reliability"],
}

PRIMARY_DIMENSIONS = [
    "platform_design_score",
    "interaction_score",
    "engagement_score",
    "technical_score",
    "instructor_support_score",
    "satisfaction_score",
]

MAX_LIKERT_VALUE = 5
MIN_LIKERT_VALUE = 1


@dataclass
class AnalyticsSummary:
    total_respondents: int
    imputed_columns: List[str]
    missing_columns: List[str]
    overall_mean: float
    overall_std_dev: float


@dataclass
class AnalyticsResult:
    summary: AnalyticsSummary
    descriptive_stats: Dict[str, Dict[str, float]]
    reliability: List[Dict[str, float]]
    correlations: Dict[str, Dict[str, float]]
    path_analysis: Dict[str, Dict[str, float]]
    insights: Dict[str, List[Dict[str, float]]]
    scores_preview: List[Dict[str, float]]


def load_dataset(file_bytes: bytes) -> pd.DataFrame:
    buffer = io.BytesIO(file_bytes)
    df = pd.read_csv(buffer)
    return df


def normalize_likert(series: pd.Series) -> pd.Series:
    return (series.fillna(MIN_LIKERT_VALUE) - MIN_LIKERT_VALUE) / (MAX_LIKERT_VALUE - MIN_LIKERT_VALUE) * 100


def compute_factor_scores(df: pd.DataFrame) -> pd.DataFrame:
    data = pd.DataFrame(index=df.index)
    for factor, columns in FACTOR_ITEMS.items():
        present_cols = [col for col in columns if col in df]
        if not present_cols:
            continue
        data[f"{factor}_score"] = normalize_likert(df[present_cols]).mean(axis=1)
    for dimension, factors in DIMENSION_FACTORS.items():
        present = [f"{factor}_score" for factor in factors if f"{factor}_score" in data]
        if present:
            data[f"{dimension}_score"] = data[present].mean(axis=1)
    if "instructor_support_score" not in data and "instructor_support_score" not in df:
        if "instructor_support_score" in df:
            data["instructor_support_score"] = df["instructor_support_score"]
        elif all(col in df for col in FACTOR_ITEMS["instructor_support"]):
            data["instructor_support_score"] = normalize_likert(df[FACTOR_ITEMS["instructor_support"]]).mean(axis=1)
    if "satisfaction_score" not in data and "satisfaction" in FACTOR_ITEMS:
        sat_cols = FACTOR_ITEMS["satisfaction"]
        if all(col in df for col in sat_cols):
            data["satisfaction_score"] = normalize_likert(df[sat_cols]).mean(axis=1)
    return data


def cronbach_alpha(df: pd.DataFrame) -> float:
    df = df.dropna(axis=0, how="any")
    k = df.shape[1]
    if k < 2:
        return float("nan")
    variance_sum = df.var(axis=0, ddof=1).sum()
    total_variance = df.sum(axis=1).var(ddof=1)
    if total_variance == 0:
        return float("nan")
    alpha = (k / (k - 1)) * (1 - variance_sum / total_variance)
    return float(alpha)


def describe_metrics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    stats: Dict[str, Dict[str, float]] = {}
    for column in df.columns:
        clean = df[column].dropna()
        if clean.empty:
            continue
        stats[column] = {
            "mean": float(clean.mean()),
            "std_dev": float(clean.std(ddof=1)) if clean.size > 1 else 0.0,
            "min": float(clean.min()),
            "max": float(clean.max()),
            "ci_low": float(clean.mean() - 1.96 * (clean.std(ddof=1) / np.sqrt(clean.size))) if clean.size > 1 else float(clean.mean()),
            "ci_high": float(clean.mean() + 1.96 * (clean.std(ddof=1) / np.sqrt(clean.size))) if clean.size > 1 else float(clean.mean()),
        }
    return stats


def correlation_matrix(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    if df.empty:
        return {}
    corr = df.corr(numeric_only=True)
    matrix: Dict[str, Dict[str, float]] = {}
    for row in corr.index:
        matrix[row] = {col: float(corr.loc[row, col]) for col in corr.columns}
    return matrix


def regression_summary(features: pd.DataFrame, target: pd.Series) -> Dict[str, float]:
    clean = pd.concat([features, target], axis=1).dropna()
    if clean.shape[0] < 5:
        return {}
    x = clean[features.columns].values
    y = clean[target.name].values
    model = LinearRegression()
    model.fit(x, y)
    predictions = model.predict(x)
    ss_res = float(np.sum((y - predictions) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r_squared = 1 - ss_res / ss_tot if ss_tot else 0.0
    return {
        "r_squared": r_squared,
        "coefficients": {col: float(coef) for col, coef in zip(features.columns, model.coef_)},
        "intercept": float(model.intercept_),
    }


def generate_insights(scores: pd.DataFrame) -> Dict[str, List[Dict[str, float]]]:
    if scores.empty:
        return {"strengths": [], "improvements": []}
    mean_scores = scores.mean().sort_values(ascending=False)
    strengths = mean_scores.head(3)
    improvements = mean_scores.tail(3)
    return {
        "strengths": [
            {"name": name, "score": float(value)}
            for name, value in strengths.items()
        ],
        "improvements": [
            {"name": name, "score": float(value)}
            for name, value in improvements.items()
        ],
    }


def run_analytics(file_bytes: bytes) -> AnalyticsResult:
    df = load_dataset(file_bytes)
    missing_columns = [col for col in LIKERT_COLUMNS if col not in df.columns]
    if missing_columns:
        for col in missing_columns:
            df[col] = MIN_LIKERT_VALUE
    scores = compute_factor_scores(df)
    descriptive = describe_metrics(scores)

    reliability_rows: List[Dict[str, float]] = []
    for factor, columns in FACTOR_ITEMS.items():
        present = [col for col in columns if col in df]
        if len(present) < 2:
            continue
        alpha = cronbach_alpha(df[present])
        reliability_rows.append({"factor": factor, "alpha": float(alpha)})

    correlations = correlation_matrix(scores)

    path_models = {}
    if all(col in scores.columns for col in ["platform_design_score", "engagement_score", "interaction_score", "satisfaction_score"]):
        features = scores[["platform_design_score", "engagement_score", "interaction_score"]]
        target = scores["satisfaction_score"].copy()
        target.name = target.name or "satisfaction_score"
        satisfaction_summary = regression_summary(features, target)
        if satisfaction_summary:
            path_models["satisfaction"] = satisfaction_summary
    if "achievement_score" in df:
        features = scores[[col for col in scores.columns if col.endswith("_score")]]
        target = normalize_likert(df["achievement_score"]).copy()
        target.name = "achievement_score"
        achievement_summary = regression_summary(features, target)
        if achievement_summary:
            path_models["achievement"] = achievement_summary

    insights = generate_insights(scores)
    overall_series = scores.mean(axis=1) if not scores.empty else pd.Series(dtype=float)
    summary = AnalyticsSummary(
        total_respondents=int(len(df.index)),
        imputed_columns=missing_columns,
        missing_columns=[col for col in NUMERIC_COLUMNS if col not in df.columns],
        overall_mean=float(overall_series.mean()) if not overall_series.empty else 0.0,
        overall_std_dev=float(overall_series.std(ddof=1)) if overall_series.size > 1 else 0.0,
    )
    preview_rows = []
    for _, row in scores.head(5).iterrows():
        preview_rows.append({col: float(val) if pd.notna(val) else 0.0 for col, val in row.items()})

    return AnalyticsResult(
        summary=summary,
        descriptive_stats=descriptive,
        reliability=reliability_rows,
        correlations=correlations,
        path_analysis=path_models,
        insights=insights,
        scores_preview=preview_rows,
    )
