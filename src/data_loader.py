"""
Data loading and validation module
Yeh file CSV data ko load karti hai aur validate karti hai
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

# Required columns jo CSV mein hone chahiye
REQUIRED_COLUMNS = {
    'respondent_id': str,
    'timestamp': str,
}

# Likert scale questions (1-5 rating wale)
LIKERT_COLUMNS = [
    'content_quality_q1', 'content_quality_q2',
    'ui_usability_q1', 'ui_usability_q2',
    'teacher_student_q1', 'teacher_student_q2',
    'peer_q1', 'peer_q2',
    'motivation_q1', 'motivation_q2',
    'autonomy_q1', 'autonomy_q2',
    'accessibility_q1', 'reliability_q1',
    'instructor_support_q1', 'instructor_support_q2',
    'satisfaction_q1', 'satisfaction_q2'
]

# Numeric columns
NUMERIC_COLUMNS = ['achievement_score']

def validate_schema(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    DataFrame mein sahi columns hain ya nahi check karta hai
    """
    errors = []
    
    # Required columns check karo
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")
    
    # Likert columns check karo
    for col in LIKERT_COLUMNS:
        if col not in df.columns:
            errors.append(f"Missing Likert column: {col}")
    
    # Numeric columns check karo
    for col in NUMERIC_COLUMNS:
        if col not in df.columns:
            errors.append(f"Missing numeric column: {col}")
    
    return len(errors) == 0, errors

def check_missing_data(df: pd.DataFrame) -> Dict[str, float]:
    """
    Kitna data missing hai calculate karta hai
    """
    missing_pct = (df.isnull().sum() / len(df) * 100).to_dict()
    return {k: v for k, v in missing_pct.items() if v > 0}

def impute_missing(df: pd.DataFrame, threshold: float = 0.20) -> pd.DataFrame:
    """
    Missing values ko average se fill karta hai (agar 20% se kam missing ho)
    """
    df_copy = df.copy()
    missing_info = check_missing_data(df_copy)
    
    for col, pct in missing_info.items():
        if col in LIKERT_COLUMNS or col in NUMERIC_COLUMNS:
            if pct < threshold * 100:
                # Mean se fill karo
                mean_val = df_copy[col].mean()
                df_copy[col].fillna(mean_val, inplace=True)
                print(f"✓ Imputed {col}: {pct:.1f}% missing (filled with mean={mean_val:.2f})")
            else:
                print(f"⚠ WARNING: {col} has {pct:.1f}% missing (>20% threshold)")
    
    return df_copy

def load_survey_data(filepath: str, impute: bool = True) -> pd.DataFrame:
    """
    Main function - CSV file ko load aur validate karta hai
    """
    # CSV load karo
    print(f"\n📂 Loading file: {filepath}")
    df = pd.read_csv(filepath)
    print(f"✓ Loaded {len(df)} responses from {filepath}")
    
    # Schema validate karo
    is_valid, errors = validate_schema(df)
    if not is_valid:
        print("\n❌ Schema validation failed:")
        for error in errors:
            print(f"  - {error}")
        raise ValueError(f"Schema validation failed with {len(errors)} errors")
    
    print("✓ Schema validation passed")
    
    # Missing data check karo
    missing_info = check_missing_data(df)
    if missing_info:
        print(f"\n⚠ Missing data detected in {len(missing_info)} columns:")
        for col, pct in missing_info.items():
            print(f"  - {col}: {pct:.1f}%")
    
    # Missing values impute karo
    if impute and missing_info:
        print("\n🔧 Imputing missing values...")
        df = impute_missing(df)
    
    # Timestamp ko datetime mein convert karo
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    # Likert ranges validate karo (1-5 hona chahiye)
    print("\n🔍 Validating Likert ranges (should be 1-5)...")
    for col in LIKERT_COLUMNS:
        if col in df.columns:
            invalid = df[(df[col] < 1) | (df[col] > 5)][col].count()
            if invalid > 0:
                print(f"⚠ WARNING: {col} has {invalid} values outside 1-5 range")
    
    print(f"\n✅ Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


if __name__ == "__main__":
    # Test karne ke liye
    print("Testing data_loader.py...")
    try:
        df = load_survey_data('../data/synthetic_survey.csv')
        print("\n📊 First 5 rows:")
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")