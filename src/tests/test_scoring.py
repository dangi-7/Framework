"""
Unit tests for scoring module
pytest se testing karne ke liye
"""

import pytest
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../src')

from scoring import (likert_to_score, compute_factor_score, 
                     compute_all_scores, FACTOR_ITEMS)

# Test data banao
@pytest.fixture
def sample_data():
    """Simple test data"""
    data = {
        'respondent_id': ['R001', 'R002', 'R003'],
        'timestamp': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'content_quality_q1': [5, 4, 3],
        'content_quality_q2': [5, 4, 3],
        'ui_usability_q1': [4, 3, 2],
        'ui_usability_q2': [4, 3, 2],
        'teacher_student_q1': [5, 4, 3],
        'teacher_student_q2': [5, 4, 3],
        'peer_q1': [3, 3, 3],
        'peer_q2': [3, 3, 3],
        'motivation_q1': [5, 4, 3],
        'motivation_q2': [5, 4, 3],
        'autonomy_q1': [4, 4, 4],
        'autonomy_q2': [4, 4, 4],
        'accessibility_q1': [5, 5, 5],
        'reliability_q1': [4, 4, 4],
        'instructor_support_q1': [5, 4, 3],
        'instructor_support_q2': [5, 4, 3],
        'achievement_score': [90, 80, 70],
        'satisfaction_q1': [5, 4, 3],
        'satisfaction_q2': [5, 4, 3]
    }
    return pd.DataFrame(data)

def test_likert_to_score():
    """Test Likert to 0-100 conversion"""
    assert likert_to_score(1) == 0
    assert likert_to_score(3) == 50
    assert likert_to_score(5) == 100
    assert likert_to_score(2) == 25
    assert likert_to_score(4) == 75

def test_compute_factor_score(sample_data):
    """Test factor score calculation"""
    # Content quality test
    content_scores = compute_factor_score(sample_data, 'content_quality')
    
    # Check length
    assert len(content_scores) == 3
    
    # Check values are in 0-100 range
    assert all(content_scores >= 0)
    assert all(content_scores <= 100)
    
    # First respondent ka score check karo (both q1 and q2 = 5)
    # Mean = 5, Score = (5-1)/4*100 = 100
    assert content_scores.iloc[0] == 100

def test_compute_all_scores(sample_data):
    """Test complete scoring function"""
    scores_df = compute_all_scores(sample_data)
    
    # Check shape
    assert len(scores_df) == 3
    assert 'respondent_id' in scores_df.columns
    assert 'overall_framework_score' in scores_df.columns
    
    # Check all factor scores exist
    for factor in FACTOR_ITEMS.keys():
        assert f'{factor}_score' in scores_df.columns
    
    # Check values are valid
    for col in scores_df.columns:
        if col.endswith('_score'):
            assert all(scores_df[col] >= 0)
            assert all(scores_df[col] <= 100)

def test_overall_score_with_custom_weights(sample_data):
    """Test overall score with custom weights"""
    custom_weights = {
        'platform_design_score': 0.3,
        'interaction_score': 0.2,
        'engagement_score': 0.2,
        'technical_score': 0.2,
        'instructor_support_score': 0.1
    }
    
    scores_df = compute_all_scores(sample_data, weights=custom_weights)
    
    # Overall score hona chahiye
    assert 'overall_framework_score' in scores_df.columns
    
    # Values valid hone chahiye
    assert all(scores_df['overall_framework_score'] >= 0)
    assert all(scores_df['overall_framework_score'] <= 100)

def test_missing_values():
    """Test handling of missing values"""
    data = {
        'respondent_id': ['R001', 'R002'],
        'timestamp': ['2024-01-01', '2024-01-02'],
        'content_quality_q1': [5, np.nan],  # Missing value
        'content_quality_q2': [5, 4],
        'ui_usability_q1': [4, 3],
        'ui_usability_q2': [4, 3],
        'teacher_student_q1': [5, 4],
        'teacher_student_q2': [5, 4],
        'peer_q1': [3, 3],
        'peer_q2': [3, 3],
        'motivation_q1': [5, 4],
        'motivation_q2': [5, 4],
        'autonomy_q1': [4, 4],
        'autonomy_q2': [4, 4],
        'accessibility_q1': [5, 5],
        'reliability_q1': [4, 4],
        'instructor_support_q1': [5, 4],
        'instructor_support_q2': [5, 4],
        'achievement_score': [90, 80],
        'satisfaction_q1': [5, 4],
        'satisfaction_q2': [5, 4]
    }
    df = pd.DataFrame(data)
    
    # Should handle missing values gracefully
    scores_df = compute_all_scores(df)
    assert len(scores_df) == 2

def test_edge_cases():
    """Test edge cases - all 1s, all 5s"""
    # All minimum ratings
    data_min = {
        'respondent_id': ['R001'],
        'timestamp': ['2024-01-01'],
        'content_quality_q1': [1],
        'content_quality_q2': [1],
        'ui_usability_q1': [1],
        'ui_usability_q2': [1],
        'teacher_student_q1': [1],
        'teacher_student_q2': [1],
        'peer_q1': [1],
        'peer_q2': [1],
        'motivation_q1': [1],
        'motivation_q2': [1],
        'autonomy_q1': [1],
        'autonomy_q2': [1],
        'accessibility_q1': [1],
        'reliability_q1': [1],
        'instructor_support_q1': [1],
        'instructor_support_q2': [1],
        'achievement_score': [0],
        'satisfaction_q1': [1],
        'satisfaction_q2': [1]
    }
    df_min = pd.DataFrame(data_min)
    scores_df_min = compute_all_scores(df_min)
    
    # All scores should be 0 (except achievement which is already 0)
    for col in scores_df_min.columns:
        if col.endswith('_score') and col != 'respondent_id' and col != 'achievement_score':
            assert scores_df_min[col].iloc[0] == 0 or abs(scores_df_min[col].iloc[0]) < 0.01
    
    # All maximum ratings
    data_max = {
        'respondent_id': ['R001'],
        'timestamp': ['2024-01-01'],
        'content_quality_q1': [5],
        'content_quality_q2': [5],
        'ui_usability_q1': [5],
        'ui_usability_q2': [5],
        'teacher_student_q1': [5],
        'teacher_student_q2': [5],
        'peer_q1': [5],
        'peer_q2': [5],
        'motivation_q1': [5],
        'motivation_q2': [5],
        'autonomy_q1': [5],
        'autonomy_q2': [5],
        'accessibility_q1': [5],
        'reliability_q1': [5],
        'instructor_support_q1': [5],
        'instructor_support_q2': [5],
        'achievement_score': [100],
        'satisfaction_q1': [5],
        'satisfaction_q2': [5]
    }
    df_max = pd.DataFrame(data_max)
    scores_df_max = compute_all_scores(df_max)
    
    # All scores should be 100 (approximately)
    for col in scores_df_max.columns:
        if col.endswith('_score') and col != 'respondent_id':
            assert scores_df_max[col].iloc[0] >= 99  # Allow small rounding error


# Run tests
if __name__ == "__main__":
    print("Running tests...")
    pytest.main([__file__, '-v'])