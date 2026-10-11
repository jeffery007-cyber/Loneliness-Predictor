"""generate_dataset.py
---------------------
Generates a synthetic dataset for training the MindSync digital loneliness
prediction model.

Each record simulates one completed assessment session across 4 parameters:
  Q1–Q5   : Smartphone Usage
  Q6–Q10  : Relationship / Love Failure
  Q11–Q15 : Betrayal / Trust Issues
  Q16–Q20 : Financial Difficulties

Each column holds a random integer 1–5 (Never=1 … Always=5).
  - TotalScore: sum of Q1–Q20 (range 20–100).
  - RiskLevel: categorical label derived from TotalScore.
        20–40  → Low
        41–70  → Moderate
        71–100 → High

Feature order is FIXED: Q1, Q2, …, Q20.  The prediction service and the
assessment controller must supply answers in this same order.

Output
------
dataset/digital_loneliness_dataset.csv  (1 000 rows, relative to project root)

Usage
-----
Run from the project root:
    python ml/generate_dataset.py
"""

import os

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NUM_RECORDS = 1000
NUM_QUESTIONS = 20
QUESTION_COLS = [f"Q{i}" for i in range(1, NUM_QUESTIONS + 1)]

# Output path is always relative to the project root, regardless of where
# the script is invoked from.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "dataset")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "digital_loneliness_dataset.csv")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def assign_risk_level(score: int) -> str:
    """Return the risk category string for a given total score.

    Args:
        score: Integer total score in the range 20–100.

    Returns:
        'Low', 'Moderate', or 'High'.
    """
    if score <= 40:
        return "Low"
    if score <= 70:
        return "Moderate"
    return "High"


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate_dataset() -> pd.DataFrame:
    """Build and return the synthetic assessment DataFrame.

    Generates NUM_RECORDS rows where each of the 20 question columns
    contains a uniformly random integer in [1, 5].  TotalScore and
    RiskLevel are derived deterministically from those values.

    Returns:
        pd.DataFrame with columns Q1–Q20, TotalScore, RiskLevel.
    """
    rng = np.random.default_rng(seed=42)  # fixed seed for reproducibility

    # To ensure all three risk classes are well represented, generate records
    # in equal thirds (~333 each) by controlling the per-question score range:
    #   Low      (score 20–40): questions average ≤ 2  → sample from [1, 2]
    #   Moderate (score 41–70): questions average ~3   → sample from [2, 4]
    #   High     (score 71–100): questions average ≥ 4 → sample from [4, 5]
    # Each third is generated independently then concatenated and shuffled.

    third = NUM_RECORDS // 3
    remainder = NUM_RECORDS - third * 3  # absorb rounding into Moderate

    low_data      = rng.integers(low=1, high=3, size=(third, NUM_QUESTIONS))           # 1–2
    moderate_data = rng.integers(low=2, high=5, size=(third + remainder, NUM_QUESTIONS))  # 2–4
    high_data     = rng.integers(low=4, high=6, size=(third, NUM_QUESTIONS))           # 4–5

    question_data = np.vstack([low_data, moderate_data, high_data])

    # Shuffle rows so the three blocks are interleaved.
    rng.shuffle(question_data)

    df = pd.DataFrame(question_data, columns=QUESTION_COLS)

    # Derive TotalScore and RiskLevel from the question columns.
    df["TotalScore"] = df[QUESTION_COLS].sum(axis=1)
    df["RiskLevel"] = df["TotalScore"].apply(assign_risk_level)

    return df


def save_dataset(df: pd.DataFrame) -> None:
    """Persist the DataFrame to CSV, creating the output directory if needed.

    Args:
        df: The DataFrame returned by generate_dataset().
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating dataset...")

    df = generate_dataset()
    save_dataset(df)

    # --- Summary ---
    print(f"Dataset saved to : {OUTPUT_FILE}")
    print(f"Total records    : {len(df)}")
    print(f"Columns          : {', '.join(df.columns.tolist())}")
    print("\nRiskLevel distribution:")
    print(df["RiskLevel"].value_counts().to_string())
    print("\nScore statistics:")
    print(df["TotalScore"].describe().to_string())
    print("\nDataset generation complete.")
