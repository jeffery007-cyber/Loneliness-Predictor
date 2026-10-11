"""train_model.py
-----------------
Trains a Random Forest classifier on the MindSync digital loneliness
dataset and persists the fitted model to disk for use by the Flask
prediction service.

Pipeline
--------
1. Load  dataset/digital_loneliness_dataset.csv
2. Split into features (Q1–Q20) and target (RiskLevel)
3. 80 / 20 train-test split (random_state=42)
4. Fit a RandomForestClassifier (n_estimators=100, random_state=42)
5. Evaluate: accuracy, classification report, confusion matrix
6. Save the model to ml/models/random_forest_model.pkl via joblib

Usage
-----
Run from the project root:
    python ml/train_model.py
"""

import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


# ---------------------------------------------------------------------------
# Paths  (always resolved relative to the project root)
# ---------------------------------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset", "digital_loneliness_dataset.csv")
MODEL_DIR    = os.path.join(PROJECT_ROOT, "ml", "models")
MODEL_PATH   = os.path.join(MODEL_DIR, "random_forest_model.pkl")

# The 20 question columns used as input features.
FEATURE_COLS = [f"Q{i}" for i in range(1, 21)]
TARGET_COL   = "RiskLevel"


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------

def load_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load the CSV dataset and return features X and target y.

    Returns:
        X: DataFrame of shape (n_samples, 20) containing Q1–Q20 scores.
        y: Series of shape (n_samples,) containing RiskLevel labels.

    Raises:
        FileNotFoundError: If the dataset CSV does not exist at DATASET_PATH.
    """
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at '{DATASET_PATH}'.\n"
            "Run  python ml/generate_dataset.py  first."
        )

    df = pd.read_csv(DATASET_PATH)

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    print(f"Dataset loaded     : {len(df)} records, {len(FEATURE_COLS)} features")
    print(f"Class distribution :\n{y.value_counts().to_string()}\n")

    return X, y


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split features and target into training and test sets.

    Args:
        X: Feature DataFrame.
        y: Target Series.

    Returns:
        X_train, X_test, y_train, y_test — 80 / 20 split.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training samples   : {len(X_train)}")
    print(f"Test samples       : {len(X_test)}\n")

    return X_train, X_test, y_train, y_test


def train(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> RandomForestClassifier:
    """Fit a RandomForestClassifier on the training data.

    Args:
        X_train: Training features.
        y_train: Training labels.

    Returns:
        The fitted RandomForestClassifier instance.
    """
    print("Training RandomForestClassifier...")

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print("Training complete.\n")
    return model


def evaluate(
    model: RandomForestClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> None:
    """Print accuracy, classification report, and confusion matrix.

    Args:
        model:  Fitted classifier.
        X_test: Test features.
        y_test: True test labels.
    """
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print(f"Accuracy           : {accuracy * 100:.2f}%\n")

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    labels = sorted(y_test.unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    # Pretty-print the confusion matrix with label headers.
    header = f"{'':>12}" + "".join(f"{lbl:>12}" for lbl in labels)
    print(header)
    for label, row in zip(labels, cm):
        row_str = f"{label:>12}" + "".join(f"{val:>12}" for val in row)
        print(row_str)
    print()


def save_model(model: RandomForestClassifier) -> None:
    """Persist the fitted model to disk using joblib.

    Creates ml/models/ automatically if it does not already exist.

    Args:
        model: The fitted RandomForestClassifier to save.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to     : {MODEL_PATH}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("  MindSync – Random Forest Model Training")
    print("=" * 55 + "\n")

    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    model = train(X_train, y_train)
    evaluate(model, X_test, y_test)
    save_model(model)

    print("\nModel trained successfully.")
