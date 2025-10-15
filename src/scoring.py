"""
Scoring module
Likert responses (1-5) ko 0-100 scores mein convert karta hai
"""

import pandas as pd
import numpy as np
from typing import Dict, List

# Har factor mein kaun se questions hain
FACTOR_ITEMS = {
    'content_quality': ['content_quality_q1', 'content_quality_q2'],
    'ui_usability': ['ui_usability_q1', 'ui_usability_q2'],
    'teacher_student_interaction': ['teacher_student_q1', 'teacher_student_q2'],
    'peer_interaction': ['peer_q1', 'peer_q2'],
    'motivation': ['motivation_q1', 'motivation_q2'],
    'autonomy': ['autonomy_q1', 'autonomy_q2'],
    'accessibility': ['accessibility_q1'],
    'reliability': ['reliability_q1'],
    'instructor_support': ['instructor_support_q1', 'instructor_support_q2'],
    'satisfaction': ['satisfaction_q1', 'satisfaction_q2']
}

# Higher-level dimensions (factors ko group karna)
DIMENSION_FACTORS = {
    'platform_design': ['content_quality', 'ui_usability'],
    'interaction': ['teacher_student_interaction', 'peer_interaction'],
    'engagement': ['motivation', 'autonomy'],
    'technical': ['accessibility', 'reliability']
}

def likert_to_score(likert_mean: float) -> float:
    """
    Likert scale mean (1-5) ko 0-100 score mein convert karta hai
    Formula: score = (mean - 1) / 4 * 100
    
    Example:
    - Likert mean = 1 → Score = 0
    - Likert mean = 3 → Score = 50
    - Likert mean = 5 → Score = 100
    """
    return (likert_mean - 1) / 4 * 100

def compute_factor_score(df: pd.DataFrame, factor_name: str) -> pd.Series:
    """
    Ek factor ke liye score calculate karta hai
    Uske items ka average lekar 0-100 mein convert karta hai
    """
    items = FACTOR_ITEMS.get(factor_name, [])
    if not items:
        raise ValueError(f"Unknown factor: {factor_name}")
    
    # Items ka mean calculate karo (NaN ignore karke)
    item_means = df[items].mean(axis=1)
    
    # 0-100 scale mein convert karo
    scores = item_means.apply(likert_to_score)
    
    return scores

def compute_all_scores(df: pd.DataFrame, weights: Dict[str, float] = None) -> pd.DataFrame:
    """
    Saare factor scores aur overall framework score calculate karta hai
    
    Args:
        df: Input DataFrame with Likert responses
        weights: Optional - factors ke liye custom weights
    
    Returns:
        DataFrame with respondent_id and all scores
    """
    print("\n📊 Computing scores...")
    result_df = pd.DataFrame()
    result_df['respondent_id'] = df['respondent_id']
    
    # Har factor ka score calculate karo
    print("  Calculating factor scores...")
    for factor in FACTOR_ITEMS.keys():
        result_df[f'{factor}_score'] = compute_factor_score(df, factor)
        print(f"    ✓ {factor}")
    
    # Achievement score add karo (already 0-100 mein hai)
    if 'achievement_score' in df.columns:
        result_df['achievement_score'] = df['achievement_score']
        print(f"    ✓ achievement")
    
    # Dimension scores calculate karo (factors ka average)
    print("  Calculating dimension scores...")
    for dimension, factors in DIMENSION_FACTORS.items():
        factor_cols = [f'{f}_score' for f in factors]
        result_df[f'{dimension}_score'] = result_df[factor_cols].mean(axis=1)
        print(f"    ✓ {dimension}")
    
    # Overall framework score calculate karo (weighted average)
    print("  Calculating overall framework score...")
    if weights is None:
        # Default: equal weights for main dimensions + instructor_support
        main_factors = ['platform_design_score', 'interaction_score', 
                       'engagement_score', 'technical_score', 
                       'instructor_support_score']
        weights = {f: 1/len(main_factors) for f in main_factors}
    
    # Weighted average calculate karo
    overall = sum(result_df[factor] * weight 
                  for factor, weight in weights.items())
    result_df['overall_framework_score'] = overall
    
    print(f"✅ Scores computed for {len(result_df)} respondents")
    return result_df

def get_factor_items() -> Dict[str, List[str]]:
    """Factor composition dictionary return karta hai"""
    return FACTOR_ITEMS.copy()

def get_default_weights() -> Dict[str, float]:
    """Default weights return karta hai"""
    main_factors = ['platform_design_score', 'interaction_score', 
                   'engagement_score', 'technical_score', 
                   'instructor_support_score']
    return {f: 1/len(main_factors) for f in main_factors}


if __name__ == "__main__":
    # Test karne ke liye
    print("Testing scoring.py...")
    from data_loader import load_survey_data
    
    try:
        # Data load karo
        df = load_survey_data('../data/synthetic_survey.csv')
        
        # Scores calculate karo
        scores_df = compute_all_scores(df)
        
        print("\n📈 Score Summary:")
        print(scores_df.describe())
        
        print(f"\n🎯 Overall Framework Score:")
        print(f"   Mean: {scores_df['overall_framework_score'].mean():.2f}")
        print(f"   Std:  {scores_df['overall_framework_score'].std():.2f}")
        
    except Exception as e:
        print(f"Error: {e}")