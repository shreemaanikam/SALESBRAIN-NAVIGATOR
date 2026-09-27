"""
SalesBrain Navigator — Model Training, Evaluation, Comparison & Selection

Trains multiple regression models for transaction-level profit prediction,
evaluates them on a chronological holdout set, optionally builds an ensemble,
and selects the best model.
"""

import os
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import pandas as pd
import joblib
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor,
    VotingRegressor,
    StackingRegressor,
)
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from backend.app.ml.features import (
    TARGET,
    ALL_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    chronological_split,
    prepare_features,
    validate_no_leakage,
    get_feature_report,
)
from backend.app.ml.preprocessing import build_pipeline, get_feature_names

logger = logging.getLogger(__name__)

# Default artifact directory
ARTIFACTS_DIR = os.environ.get("ML_ARTIFACTS_DIR", "backend/app/ml/artifacts")


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate regression metrics."""
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    return {
        "mae": round(float(mae), 4),
        "mse": round(float(mse), 4),
        "rmse": round(float(rmse), 4),
        "r2": round(float(r2), 4),
    }


def get_model_candidates() -> Dict[str, Any]:
    """Return a dictionary of model name -> unfitted estimator."""
    return {
        "DummyRegressor (Baseline)": DummyRegressor(strategy="mean"),
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=15, random_state=42),
        "Random Forest": RandomForestRegressor(
            n_estimators=100, max_depth=15, random_state=42, n_jobs=-1
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42
        ),
        "Extra Trees": ExtraTreesRegressor(
            n_estimators=100, max_depth=15, random_state=42, n_jobs=-1
        ),
    }


def train_and_evaluate_all(
    df: pd.DataFrame,
    test_ratio: float = 0.2,
) -> Tuple[Dict[str, Dict], Dict[str, Any], pd.DataFrame, pd.DataFrame]:
    """
    Train all candidate models and evaluate on chronological holdout.

    Returns:
        results: dict of model_name -> {metrics, pipeline}
        split_info: metadata about the split
        train_df: training DataFrame
        test_df: testing DataFrame
    """
    # Validate features
    validate_no_leakage(ALL_FEATURES)

    # Chronological split
    train_df, test_df = chronological_split(df, test_ratio=test_ratio)

    # Extract features and target
    X_train, y_train = prepare_features(train_df)
    X_test, y_test = prepare_features(test_df)

    split_info = {
        "train_size": len(train_df),
        "test_size": len(test_df),
        "train_date_range": {
            "start": str(train_df["order_date"].min()),
            "end": str(train_df["order_date"].max()),
        },
        "test_date_range": {
            "start": str(test_df["order_date"].min()),
            "end": str(test_df["order_date"].max()),
        },
        "target_train_mean": round(float(y_train.mean()), 2),
        "target_train_std": round(float(y_train.std()), 2),
        "target_test_mean": round(float(y_test.mean()), 2),
        "target_test_std": round(float(y_test.std()), 2),
    }

    logger.info(f"Train: {split_info['train_size']} rows, Test: {split_info['test_size']} rows")

    # Train individual models
    results = {}
    candidates = get_model_candidates()

    for name, estimator in candidates.items():
        logger.info(f"Training: {name}")
        try:
            pipeline = build_pipeline(estimator)
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            metrics = evaluate_model(y_test.values, y_pred)
            results[name] = {"metrics": metrics, "pipeline": pipeline}
            logger.info(f"  {name}: R²={metrics['r2']}, MAE={metrics['mae']}")
        except Exception as e:
            logger.error(f"  {name} failed: {e}")
            results[name] = {"metrics": {"mae": None, "mse": None, "rmse": None, "r2": None}, "pipeline": None, "error": str(e)}

    # Build ensemble from top performers (excluding baseline and failures)
    viable = {
        k: v for k, v in results.items()
        if v.get("pipeline") is not None
        and v["metrics"]["r2"] is not None
        and "Dummy" not in k
    }

    if len(viable) >= 2:
        # VotingRegressor ensemble
        top_models = sorted(viable.items(), key=lambda x: x[1]["metrics"]["r2"], reverse=True)[:3]
        voting_estimators = [
            (name.replace(" ", "_").lower(), v["pipeline"].named_steps["model"])
            for name, v in top_models
        ]

        try:
            from backend.app.ml.preprocessing import build_preprocessor
            voting = VotingRegressor(estimators=voting_estimators)
            ensemble_pipeline = build_pipeline(voting)
            ensemble_pipeline.fit(X_train, y_train)
            y_pred_ens = ensemble_pipeline.predict(X_test)
            ens_metrics = evaluate_model(y_test.values, y_pred_ens)
            results["Voting Ensemble"] = {"metrics": ens_metrics, "pipeline": ensemble_pipeline}
            logger.info(f"  Voting Ensemble: R²={ens_metrics['r2']}, MAE={ens_metrics['mae']}")
        except Exception as e:
            logger.warning(f"  Ensemble failed: {e}")

    return results, split_info, train_df, test_df


def select_best_model(results: Dict[str, Dict]) -> Tuple[str, Dict]:
    """
    Select the best model by R² on the holdout test set.
    Prefer simpler models when R² difference is < 0.005.
    """
    viable = {
        k: v for k, v in results.items()
        if v.get("pipeline") is not None
        and v["metrics"]["r2"] is not None
    }

    if not viable:
        raise RuntimeError("No viable trained model found")

    # Sort by R² descending
    ranked = sorted(viable.items(), key=lambda x: x[1]["metrics"]["r2"], reverse=True)
    best_name, best_data = ranked[0]

    # Simplicity preference: if a simpler model is within 0.005 R², prefer it
    simplicity_order = [
        "Linear Regression",
        "Decision Tree",
        "Random Forest",
        "Gradient Boosting",
        "Extra Trees",
        "Voting Ensemble",
    ]

    for simple_name in simplicity_order:
        if simple_name in viable and simple_name != best_name:
            simple_r2 = viable[simple_name]["metrics"]["r2"]
            if best_data["metrics"]["r2"] - simple_r2 < 0.005:
                logger.info(
                    f"Preferring simpler '{simple_name}' (R²={simple_r2}) over "
                    f"'{best_name}' (R²={best_data['metrics']['r2']}) — within 0.005 threshold"
                )
                best_name = simple_name
                best_data = viable[simple_name]
                break

    return best_name, best_data


def save_artifacts(
    best_name: str,
    best_data: Dict,
    results: Dict,
    split_info: Dict,
    df: pd.DataFrame,
    artifacts_dir: str = ARTIFACTS_DIR,
) -> Dict[str, str]:
    """Save the selected model and metadata to disk."""
    Path(artifacts_dir).mkdir(parents=True, exist_ok=True)
    saved_files = {}

    # 1. Save the best pipeline
    model_path = os.path.join(artifacts_dir, "profit_model.joblib")
    joblib.dump(best_data["pipeline"], model_path)
    saved_files["model"] = model_path

    # 2. Save model metadata
    metadata = {
        "selected_model": best_name,
        "target": TARGET,
        "features": ALL_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "metrics": best_data["metrics"],
        "split_info": split_info,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "use_case": "Transaction-level profit estimation (sales known at prediction time)",
        "caveat": "Predictions are estimates based on historical patterns. Validate before acting.",
    }
    metadata_path = os.path.join(artifacts_dir, "model_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2, default=str)
    saved_files["metadata"] = metadata_path

    # 3. Save comparison CSV
    comparison_rows = []
    for name, data in results.items():
        row = {"model": name}
        row.update(data.get("metrics", {}))
        if "error" in data:
            row["error"] = data["error"]
        comparison_rows.append(row)

    comparison_df = pd.DataFrame(comparison_rows)
    comparison_path = os.path.join(artifacts_dir, "model_comparison.csv")
    comparison_df.to_csv(comparison_path, index=False)
    saved_files["comparison"] = comparison_path

    # 4. Save feature importance (for tree-based models)
    try:
        model = best_data["pipeline"].named_steps["model"]
        preprocessor = best_data["pipeline"].named_steps["preprocessor"]

        if hasattr(model, "feature_importances_"):
            feature_names = get_feature_names(preprocessor)
            importances = model.feature_importances_

            if len(feature_names) == len(importances):
                fi_df = pd.DataFrame({
                    "feature": feature_names,
                    "importance": importances,
                }).sort_values("importance", ascending=False)
                fi_path = os.path.join(artifacts_dir, "feature_importance.csv")
                fi_df.to_csv(fi_path, index=False)
                saved_files["feature_importance"] = fi_path
        elif hasattr(model, "estimators_"):
            # Voting ensemble — try to get from first estimator
            for est_name, est in model.estimators:
                if hasattr(est, "feature_importances_"):
                    feature_names = get_feature_names(preprocessor)
                    importances = est.feature_importances_
                    if len(feature_names) == len(importances):
                        fi_df = pd.DataFrame({
                            "feature": feature_names,
                            "importance": importances,
                            "source_model": est_name,
                        }).sort_values("importance", ascending=False)
                        fi_path = os.path.join(artifacts_dir, "feature_importance.csv")
                        fi_df.to_csv(fi_path, index=False)
                        saved_files["feature_importance"] = fi_path
                    break
    except Exception as e:
        logger.warning(f"Could not extract feature importance: {e}")

    # 5. Save feature report
    feature_report = get_feature_report(df)
    report_path = os.path.join(artifacts_dir, "feature_report.json")
    with open(report_path, "w") as f:
        json.dump(feature_report, f, indent=2, default=str)
    saved_files["feature_report"] = report_path

    return saved_files


def run_training_pipeline(dataset_path: str = None) -> Dict[str, Any]:
    """
    Full training pipeline: load data, train, evaluate, select, save.

    Can be run as:
        python -m backend.app.ml.train
    """
    from dotenv import load_dotenv
    load_dotenv()

    if dataset_path is None:
        dataset_path = os.environ.get("DATASET_PATH", "dataset/Cleaned_SuperStore.csv")

    artifacts_dir = os.environ.get("ML_ARTIFACTS_DIR", ARTIFACTS_DIR)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    logger.info(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

    # Drop rows with missing target or essential features
    initial_count = len(df)
    required = ALL_FEATURES + [TARGET, "order_date"]
    df = df.dropna(subset=[TARGET, "order_date"])
    logger.info(f"Rows after dropping missing target/date: {len(df)} (dropped {initial_count - len(df)})")

    logger.info("Starting model training and evaluation...")
    results, split_info, train_df, test_df = train_and_evaluate_all(df)

    logger.info("Selecting best model...")
    best_name, best_data = select_best_model(results)
    logger.info(f"Selected: {best_name} — R²={best_data['metrics']['r2']}, MAE={best_data['metrics']['mae']}")

    logger.info("Saving artifacts...")
    saved = save_artifacts(best_name, best_data, results, split_info, df, artifacts_dir)

    summary = {
        "selected_model": best_name,
        "metrics": best_data["metrics"],
        "split_info": split_info,
        "saved_files": saved,
        "all_results": {k: v.get("metrics", {}) for k, v in results.items()},
    }

    logger.info("=" * 60)
    logger.info("TRAINING COMPLETE")
    logger.info(f"Selected: {best_name}")
    logger.info(f"R²: {best_data['metrics']['r2']}")
    logger.info(f"MAE: {best_data['metrics']['mae']}")
    logger.info(f"RMSE: {best_data['metrics']['rmse']}")
    logger.info("=" * 60)

    return summary


if __name__ == "__main__":
    run_training_pipeline()
