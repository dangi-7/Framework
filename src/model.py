"""
Statistical modeling module
Regression aur path analysis - relationships test karta hai
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import statsmodels.api as sm
import warnings

def run_simple_regression(df: pd.DataFrame, 
                         outcome: str, 
                         predictors: List[str]) -> Dict:
    """
    Simple OLS regression chalata hai
    
    Args:
        df: DataFrame with variables
        outcome: Dependent variable (result)
        predictors: Independent variables (causes)
    """
    # Data prepare karo (missing values remove karo)
    data = df[[outcome] + predictors].dropna()
    
    X = data[predictors]
    y = data[outcome]
    
    # Constant term add karo (intercept ke liye)
    X = sm.add_constant(X)
    
    # Model fit karo
    model = sm.OLS(y, X)
    results = model.fit()
    
    return {
        'r_squared': results.rsquared,
        'adj_r_squared': results.rsquared_adj,
        'f_statistic': results.fvalue,
        'f_pvalue': results.f_pvalue,
        'coefficients': results.params.to_dict(),
        'pvalues': results.pvalues.to_dict(),
        'summary': str(results.summary())
    }

def test_mediation(df: pd.DataFrame,
                   independent: str,
                   mediator: str,
                   dependent: str) -> Dict:
    """
    Mediation test karta hai (Baron & Kenny approach)
    
    Path: independent → mediator → dependent
    
    Example: platform_design → motivation → achievement
    """
    data = df[[independent, mediator, dependent]].dropna()
    
    print(f"\n  Testing mediation: {independent} → {mediator} → {dependent}")
    
    # Step 1: Total effect (c path)
    # dependent ~ independent
    X1 = sm.add_constant(data[[independent]])
    y1 = data[dependent]
    model1 = sm.OLS(y1, X1).fit()
    c_path = model1.params[independent]
    c_pvalue = model1.pvalues[independent]
    
    # Step 2: Effect on mediator (a path)
    # mediator ~ independent
    X2 = sm.add_constant(data[[independent]])
    y2 = data[mediator]
    model2 = sm.OLS(y2, X2).fit()
    a_path = model2.params[independent]
    a_pvalue = model2.pvalues[independent]
    
    # Step 3: Direct effect controlling for mediator (c' path)
    # dependent ~ independent + mediator
    X3 = sm.add_constant(data[[independent, mediator]])
    y3 = data[dependent]
    model3 = sm.OLS(y3, X3).fit()
    c_prime_path = model3.params[independent]
    b_path = model3.params[mediator]
    c_prime_pvalue = model3.pvalues[independent]
    b_pvalue = model3.pvalues[mediator]
    
    # Indirect effect calculate karo
    indirect_effect = a_path * b_path
    
    # Mediation type determine karo
    if c_pvalue < 0.05 and c_prime_pvalue >= 0.05:
        mediation_type = "Full mediation (complete)"
    elif c_pvalue < 0.05 and c_prime_pvalue < 0.05 and abs(c_prime_path) < abs(c_path):
        mediation_type = "Partial mediation"
    else:
        mediation_type = "No mediation"
    
    print(f"    Result: {mediation_type}")
    
    return {
        'total_effect': c_path,
        'direct_effect': c_prime_path,
        'indirect_effect': indirect_effect,
        'a_path': a_path,
        'b_path': b_path,
        'a_pvalue': a_pvalue,
        'b_pvalue': b_pvalue,
        'c_pvalue': c_pvalue,
        'c_prime_pvalue': c_prime_pvalue,
        'mediation_type': mediation_type
    }

def run_path_analysis(scores_df: pd.DataFrame) -> Dict:
    """
    Comprehensive path analysis - key hypotheses test karta hai
    
    Hypotheses:
    H1: Platform Design → Motivation → Achievement
    H2: Interaction → Satisfaction
    H3: Engagement → Achievement & Satisfaction
    """
    print("\n🔬 Running Path Analysis...")
    print("=" * 60)
    
    results = {}
    
    # H1: Platform Design → Motivation → Achievement
    print("\n📌 H1: Platform Design → Motivation → Achievement")
    if all(col in scores_df.columns for col in ['platform_design_score', 'motivation_score', 'achievement_score']):
        h1_result = test_mediation(
            scores_df,
            'platform_design_score',
            'motivation_score',
            'achievement_score'
        )
        results['H1_platform_motivation_achievement'] = h1_result
    
    # H2: Interaction → Satisfaction (direct effect)
    print("\n📌 H2: Interaction → Satisfaction")
    if all(col in scores_df.columns for col in ['interaction_score', 'satisfaction_score']):
        h2_result = run_simple_regression(
            scores_df,
            'satisfaction_score',
            ['interaction_score']
        )
        results['H2_interaction_satisfaction'] = h2_result
        print(f"    R² = {h2_result['r_squared']:.3f}, p = {h2_result['f_pvalue']:.4f}")
    
    # H3a: Engagement → Achievement
    print("\n📌 H3a: Engagement → Achievement")
    if all(col in scores_df.columns for col in ['engagement_score', 'achievement_score']):
        h3a_result = run_simple_regression(
            scores_df,
            'achievement_score',
            ['engagement_score']
        )
        results['H3a_engagement_achievement'] = h3a_result
        print(f"    R² = {h3a_result['r_squared']:.3f}, p = {h3a_result['f_pvalue']:.4f}")
    
    # H3b: Engagement → Satisfaction
    print("\n📌 H3b: Engagement → Satisfaction")
    if all(col in scores_df.columns for col in ['engagement_score', 'satisfaction_score']):
        h3b_result = run_simple_regression(
            scores_df,
            'satisfaction_score',
            ['engagement_score']
        )
        results['H3b_engagement_satisfaction'] = h3b_result
        print(f"    R² = {h3b_result['r_squared']:.3f}, p = {h3b_result['f_pvalue']:.4f}")
    
    # Multiple regression: All factors → Achievement
    print("\n📌 Multiple Regression: All Factors → Achievement")
    predictor_cols = ['platform_design_score', 'interaction_score', 
                     'engagement_score', 'technical_score', 'instructor_support_score']
    if all(col in scores_df.columns for col in predictor_cols + ['achievement_score']):
        multi_result = run_simple_regression(
            scores_df,
            'achievement_score',
            predictor_cols
        )
        results['multiple_achievement'] = multi_result
        print(f"    R² = {multi_result['r_squared']:.3f}, Adj R² = {multi_result['adj_r_squared']:.3f}")
    
    print("\n✅ Path analysis completed")
    print("=" * 60)
    
    return results

def generate_model_report(results: Dict) -> str:
    """
    Model results ka text report generate karta hai
    """
    report = []
    report.append("\n" + "=" * 70)
    report.append("     PATH ANALYSIS & REGRESSION RESULTS")
    report.append("=" * 70)
    
    # H1 Report
    if 'H1_platform_motivation_achievement' in results:
        h1 = results['H1_platform_motivation_achievement']
        report.append("\n📌 H1: Platform Design → Motivation → Achievement")
        report.append("-" * 70)
        report.append(f"  Total Effect (c):     {h1['total_effect']:7.3f}  (p={h1['c_pvalue']:.4f})")
        report.append(f"  Direct Effect (c'):   {h1['direct_effect']:7.3f}  (p={h1['c_prime_pvalue']:.4f})")
        report.append(f"  Indirect Effect:      {h1['indirect_effect']:7.3f}")
        report.append(f"  Result: {h1['mediation_type']}")
    
    # H2 Report
    if 'H2_interaction_satisfaction' in results:
        h2 = results['H2_interaction_satisfaction']
        report.append("\n📌 H2: Interaction → Satisfaction")
        report.append("-" * 70)
        report.append(f"  R² = {h2['r_squared']:.3f}")
        report.append(f"  F-statistic = {h2['f_statistic']:.3f}, p = {h2['f_pvalue']:.4f}")
    
    # H3 Reports
    if 'H3a_engagement_achievement' in results:
        h3a = results['H3a_engagement_achievement']
        report.append("\n📌 H3a: Engagement → Achievement")
        report.append("-" * 70)
        report.append(f"  R² = {h3a['r_squared']:.3f}")
        report.append(f"  F-statistic = {h3a['f_statistic']:.3f}, p = {h3a['f_pvalue']:.4f}")
    
    if 'H3b_engagement_satisfaction' in results:
        h3b = results['H3b_engagement_satisfaction']
        report.append("\n📌 H3b: Engagement → Satisfaction")
        report.append("-" * 70)
        report.append(f"  R² = {h3b['r_squared']:.3f}")
        report.append(f"  F-statistic = {h3b['f_statistic']:.3f}, p = {h3b['f_pvalue']:.4f}")
    
    report.append("\n" + "=" * 70)
    return "\n".join(report)


if __name__ == "__main__":
    # Test karne ke liye
    print("Testing model.py...")
    from data_loader import load_survey_data
    from scoring import compute_all_scores
    
    try:
        # Data load aur score karo
        df = load_survey_data('../data/synthetic_survey.csv')
        scores_df = compute_all_scores(df)
        
        # Path analysis run karo
        results = run_path_analysis(scores_df)
        
        # Report print karo
        report = generate_model_report(results)
        print(report)
        
    except Exception as e:
        print(f"Error: {e}")