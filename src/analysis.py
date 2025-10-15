"""
Statistical analysis module
Reliability (Cronbach's α), correlations, aur descriptive statistics
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Tuple

def cronbach_alpha(item_scores: pd.DataFrame) -> float:
    """
    Cronbach's alpha calculate karta hai (reliability measure)
    
    Alpha values:
    > 0.9 = Excellent
    > 0.8 = Good
    > 0.7 = Acceptable
    > 0.6 = Questionable
    < 0.6 = Poor
    """
    item_scores = item_scores.dropna()
    n_items = item_scores.shape[1]
    
    if n_items < 2:
        return np.nan
    
    # Har item ka variance aur total variance calculate karo
    item_vars = item_scores.var(axis=0, ddof=1)
    total_var = item_scores.sum(axis=1).var(ddof=1)
    
    # Cronbach's alpha formula
    alpha = (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)
    
    return alpha

def compute_reliability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Har factor ke liye Cronbach's alpha calculate karta hai
    """
    from scoring import FACTOR_ITEMS
    
    print("\n🔬 Computing reliability (Cronbach's Alpha)...")
    results = []
    
    for factor, items in FACTOR_ITEMS.items():
        # Check karo ki saare items available hain
        available_items = [item for item in items if item in df.columns]
        
        if len(available_items) >= 2:
            alpha = cronbach_alpha(df[available_items])
            n_items = len(available_items)
            
            # Interpretation
            if alpha >= 0.9:
                interpretation = "Excellent"
            elif alpha >= 0.8:
                interpretation = "Good"
            elif alpha >= 0.7:
                interpretation = "Acceptable"
            elif alpha >= 0.6:
                interpretation = "Questionable"
            else:
                interpretation = "Poor"
            
            results.append({
                'factor': factor,
                'cronbach_alpha': alpha,
                'n_items': n_items,
                'interpretation': interpretation
            })
            print(f"  ✓ {factor:30s} α={alpha:.3f} ({interpretation})")
        else:
            results.append({
                'factor': factor,
                'cronbach_alpha': np.nan,
                'n_items': len(available_items),
                'interpretation': 'Too few items'
            })
            print(f"  ⚠ {factor:30s} Too few items")
    
    return pd.DataFrame(results)

def compute_correlations(scores_df: pd.DataFrame) -> pd.DataFrame:
    """
    Saare factor scores ke beech Pearson correlations calculate karta hai
    """
    print("\n📊 Computing correlations...")
    # Sirf score columns select karo
    score_cols = [col for col in scores_df.columns if col.endswith('_score')]
    
    # Correlation matrix calculate karo
    corr_matrix = scores_df[score_cols].corr(method='pearson')
    
    print(f"  ✓ Correlation matrix computed ({len(score_cols)}x{len(score_cols)})")
    return corr_matrix

def compute_descriptive_stats(scores_df: pd.DataFrame) -> pd.DataFrame:
    """
    Saare factors ke liye descriptive statistics calculate karta hai
    Mean, SD, Min, Max, aur 95% Confidence Intervals
    """
    print("\n📈 Computing descriptive statistics...")
    score_cols = [col for col in scores_df.columns if col.endswith('_score')]
    
    # Basic descriptive stats
    stats_df = scores_df[score_cols].describe().T
    
    # 95% Confidence Intervals add karo
    for col in score_cols:
        data = scores_df[col].dropna()
        if len(data) > 1:
            ci = stats.t.interval(0.95, len(data)-1, 
                                 loc=data.mean(), 
                                 scale=stats.sem(data))
            stats_df.loc[col, 'ci_lower'] = ci[0]
            stats_df.loc[col, 'ci_upper'] = ci[1]
    
    print(f"  ✓ Stats computed for {len(score_cols)} variables")
    return stats_df

def test_correlation_significance(scores_df: pd.DataFrame, 
                                  var1: str, var2: str) -> Dict:
    """
    Do variables ke beech correlation significant hai ya nahi test karta hai
    """
    data1 = scores_df[var1].dropna()
    data2 = scores_df[var2].dropna()
    
    # Common indices use karo
    common_idx = data1.index.intersection(data2.index)
    data1 = data1.loc[common_idx]
    data2 = data2.loc[common_idx]
    
    # Pearson correlation test
    r, p_value = stats.pearsonr(data1, data2)
    
    return {
        'correlation': r,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'n': len(data1)
    }

def generate_analysis_report(df: pd.DataFrame, scores_df: pd.DataFrame) -> str:
    """
    Comprehensive analysis report generate karta hai (text format)
    """
    report = []
    report.append("=" * 70)
    report.append("     FRAMEWORK FOR QUALTIY ASSURANCE IN EDUCATIONAL APPS- ANALYSIS REPORT")
    report.append("=" * 70)
    report.append("")
    
    # Sample info
    report.append(f"📊 Sample Size: {len(scores_df)} respondents")
    report.append("")
    
    # Reliability analysis
    report.append("🔬 RELIABILITY ANALYSIS (Cronbach's Alpha)")
    report.append("-" * 70)
    reliability = compute_reliability(df)
    for _, row in reliability.iterrows():
        if not pd.isna(row['cronbach_alpha']):
            report.append(f"  {row['factor']:35s} α = {row['cronbach_alpha']:.3f} ({row['interpretation']}, n={row['n_items']} items)")
        else:
            report.append(f"  {row['factor']:35s} {row['interpretation']}")
    report.append("")
    
    # Descriptive statistics
    report.append("📈 DESCRIPTIVE STATISTICS (0-100 scale)")
    report.append("-" * 70)
    desc_stats = compute_descriptive_stats(scores_df)
    for idx, row in desc_stats.iterrows():
        factor_name = idx.replace('_score', '').replace('_', ' ').title()
        report.append(f"  {factor_name:35s} M={row['mean']:6.2f}  SD={row['std']:6.2f}  95%CI=[{row['ci_lower']:6.2f}, {row['ci_upper']:6.2f}]")
    report.append("")
    
    # Key correlations
    report.append("🔗 KEY CORRELATIONS")
    report.append("-" * 70)
    
    key_pairs = [
        ('platform_design_score', 'motivation_score', 'Platform Design ↔ Motivation'),
        ('interaction_score', 'satisfaction_score', 'Interaction ↔ Satisfaction'),
        ('motivation_score', 'achievement_score', 'Motivation ↔ Achievement'),
        ('engagement_score', 'achievement_score', 'Engagement ↔ Achievement'),
        ('engagement_score', 'satisfaction_score', 'Engagement ↔ Satisfaction')
    ]
    
    for var1, var2, label in key_pairs:
        if var1 in scores_df.columns and var2 in scores_df.columns:
            result = test_correlation_significance(scores_df, var1, var2)
            sig_marker = " **" if result['significant'] else ""
            report.append(f"  {label:40s} r={result['correlation']:6.3f}  (p={result['p_value']:.4f}){sig_marker}")
    
    report.append("")
    report.append("  ** Significant at p < 0.05")
    report.append("")
    report.append("=" * 70)
    
    return "\n".join(report)


if __name__ == "__main__":
    # Test karne ke liye
    print("Testing analysis.py...")
    from data_loader import load_survey_data
    from scoring import compute_all_scores
    
    try:
        # Data load aur score karo
        df = load_survey_data('../data/synthetic_survey.csv')
        scores_df = compute_all_scores(df)
        
        # Report generate karo
        report = generate_analysis_report(df, scores_df)
        print(report)
        
    except Exception as e:
        print(f"Error: {e}")