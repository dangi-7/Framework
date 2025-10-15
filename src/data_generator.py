"""
Synthetic data generator
Testing ke liye realistic survey data generate karta hai
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_survey(n_respondents: int = 50, seed: int = 42) -> pd.DataFrame:
    """
    Synthetic survey data generate karta hai with realistic correlations
    
    Args:
        n_respondents: Kitne respondents chahiye
        seed: Random seed (reproducibility ke liye)
    
    Returns:
        DataFrame with survey responses
    """
    np.random.seed(seed)
    
    print(f"\n🎲 Generating synthetic survey data for {n_respondents} respondents...")
    
    data = {}
    
    # Respondent IDs
    data['respondent_id'] = [f'R{i:03d}' for i in range(1, n_respondents + 1)]
    
    # Timestamps (last 30 days)
    base_date = datetime.now() - timedelta(days=30)
    data['timestamp'] = [base_date + timedelta(days=np.random.randint(0, 30),
                                                hours=np.random.randint(0, 24))
                         for _ in range(n_respondents)]
    
    # Generate correlated Likert responses
    # Base quality level for each respondent (overall experience)
    base_quality = np.random.normal(3.5, 0.8, n_respondents)
    base_quality = np.clip(base_quality, 1, 5)
    
    # Content Quality (usually high)
    data['content_quality_q1'] = np.clip(
        np.round(base_quality + np.random.normal(0.3, 0.5, n_respondents)), 1, 5
    ).astype(int)
    data['content_quality_q2'] = np.clip(
        np.round(data['content_quality_q1'] + np.random.normal(0, 0.3, n_respondents)), 1, 5
    ).astype(int)
    
    # UI Usability (moderate to high)
    data['ui_usability_q1'] = np.clip(
        np.round(base_quality + np.random.normal(0, 0.6, n_respondents)), 1, 5
    ).astype(int)
    data['ui_usability_q2'] = np.clip(
        np.round(data['ui_usability_q1'] + np.random.normal(0, 0.4, n_respondents)), 1, 5
    ).astype(int)
    
    # Teacher-Student Interaction (varies more)
    data['teacher_student_q1'] = np.clip(
        np.round(base_quality + np.random.normal(-0.2, 0.7, n_respondents)), 1, 5
    ).astype(int)
    data['teacher_student_q2'] = np.clip(
        np.round(data['teacher_student_q1'] + np.random.normal(0, 0.3, n_respondents)), 1, 5
    ).astype(int)
    
    # Peer Interaction (lower average, more variance)
    data['peer_q1'] = np.clip(
        np.round(base_quality + np.random.normal(-0.5, 0.8, n_respondents)), 1, 5
    ).astype(int)
    data['peer_q2'] = np.clip(
        np.round(data['peer_q1'] + np.random.normal(0, 0.4, n_respondents)), 1, 5
    ).astype(int)
    
    # Motivation (correlated with content quality)
    motivation_base = 0.6 * data['content_quality_q1'] + 0.4 * base_quality
    data['motivation_q1'] = np.clip(
        np.round(motivation_base + np.random.normal(0, 0.5, n_respondents)), 1, 5
    ).astype(int)
    data['motivation_q2'] = np.clip(
        np.round(data['motivation_q1'] + np.random.normal(0, 0.3, n_respondents)), 1, 5
    ).astype(int)
    
    # Autonomy (independent learners)
    data['autonomy_q1'] = np.clip(
        np.round(base_quality + np.random.normal(0.2, 0.6, n_respondents)), 1, 5
    ).astype(int)
    data['autonomy_q2'] = np.clip(
        np.round(data['autonomy_q1'] + np.random.normal(0, 0.3, n_respondents)), 1, 5
    ).astype(int)
    
    # Accessibility (usually good)
    data['accessibility_q1'] = np.clip(
        np.round(base_quality + np.random.normal(0.4, 0.5, n_respondents)), 1, 5
    ).astype(int)
    
    # Reliability (technical factor)
    data['reliability_q1'] = np.clip(
        np.round(base_quality + np.random.normal(0.3, 0.6, n_respondents)), 1, 5
    ).astype(int)
    
    # Instructor Support (important factor)
    data['instructor_support_q1'] = np.clip(
        np.round(base_quality + np.random.normal(0, 0.7, n_respondents)), 1, 5
    ).astype(int)
    data['instructor_support_q2'] = np.clip(
        np.round(data['instructor_support_q1'] + np.random.normal(0, 0.3, n_respondents)), 1, 5
    ).astype(int)
    
    # Achievement Score (0-100, correlated with motivation and content)
    achievement_base = (
        15 * data['content_quality_q1'] +
        10 * data['motivation_q1'] +
        5 * data['instructor_support_q1'] +
        20  # Base score
    )
    data['achievement_score'] = np.clip(
        achievement_base + np.random.normal(0, 8, n_respondents), 0, 100
    )
    
    # Satisfaction (correlated with overall experience)
    satisfaction_base = 0.7 * base_quality + 0.3 * data['motivation_q1']
    data['satisfaction_q1'] = np.clip(
        np.round(satisfaction_base + np.random.normal(0, 0.4, n_respondents)), 1, 5
    ).astype(int)
    data['satisfaction_q2'] = np.clip(
        np.round(data['satisfaction_q1'] + np.random.normal(0, 0.3, n_respondents)), 1, 5
    ).astype(int)
    
    # DataFrame banao
    df = pd.DataFrame(data)
    
    # Kuch missing values add karo (realistic banane ke liye)
    missing_rate = 0.05  # 5% missing
    for col in df.columns:
        if col not in ['respondent_id', 'timestamp']:
            mask = np.random.random(n_respondents) < missing_rate
            df.loc[mask, col] = np.nan
    
    print(f"✅ Generated {len(df)} survey responses with realistic correlations")
    print(f"   - Content quality mean: {df['content_quality_q1'].mean():.2f}")
    print(f"   - Motivation mean: {df['motivation_q1'].mean():.2f}")
    print(f"   - Achievement mean: {df['achievement_score'].mean():.2f}")
    print(f"   - Missing data: ~{missing_rate*100:.0f}% per variable")
    
    return df

def create_template_csv(filepath: str = '../data/real_data_template.csv'):
    """
    Empty template CSV banata hai (users ko fill karne ke liye)
    """
    print(f"\n📄 Creating template CSV...")
    
    columns = [
        'respondent_id', 'timestamp',
        'content_quality_q1', 'content_quality_q2',
        'ui_usability_q1', 'ui_usability_q2',
        'teacher_student_q1', 'teacher_student_q2',
        'peer_q1', 'peer_q2',
        'motivation_q1', 'motivation_q2',
        'autonomy_q1', 'autonomy_q2',
        'accessibility_q1', 'reliability_q1',
        'instructor_support_q1', 'instructor_support_q2',
        'achievement_score',
        'satisfaction_q1', 'satisfaction_q2'
    ]
    
    # Empty DataFrame with just column headers
    df_template = pd.DataFrame(columns=columns)
    
    # Save to CSV
    df_template.to_csv(filepath, index=False)
    print(f"✅ Template saved to {filepath}")
    print(f"   Columns: {len(columns)}")
    print("   Fill this template with your real survey data!")


if __name__ == "__main__":
    # Synthetic data generate karo
    df_synthetic = generate_synthetic_survey(n_respondents=50, seed=42)
    
    # Save karo
    df_synthetic.to_csv('../data/synthetic_survey.csv', index=False)
    print(f"\n💾 Synthetic data saved to '../data/synthetic_survey.csv'")
    
    # Template banao
    create_template_csv('../data/real_data_template.csv')
    
    print("\n✅ Data generation complete!")