"""
Visualization module
Charts aur plots banata hai - bar charts, heatmaps, radar charts, boxplots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional

# Seaborn style set
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def plot_factor_bars(scores_df: pd.DataFrame, save_path: Optional[str] = None):
    """
    Factor scores ke liye bar chart with 95% confidence intervals
    """
    from scipy import stats
    
    print("\n📊 Creating factor bar chart...")
    
    # Select score columns  
    score_cols = [col for col in scores_df.columns 
                  if col.endswith('_score') and col != 'overall_framework_score']
    
    # Calculate Means and confidence intervals 
    means = []
    ci_lower = []
    ci_upper = []
    labels = []
    
    for col in score_cols:
        data = scores_df[col].dropna()
        mean = data.mean()
        ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=stats.sem(data))
        
        means.append(mean)
        ci_lower.append(mean - ci[0])
        ci_upper.append(ci[1] - mean)
        labels.append(col.replace('_score', '').replace('_', ' ').title())
    
    # Create bar chart 
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x_pos = np.arange(len(labels))
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(labels)))
    
    bars = ax.bar(x_pos, means, yerr=[ci_lower, ci_upper], 
                  capsize=5, color=colors, alpha=0.8, 
                  edgecolor='black', linewidth=1.5)
    
    # Labels and formatting
    ax.set_xlabel('Factors', fontsize=14, fontweight='bold')
    ax.set_ylabel('Score (0-100)', fontsize=14, fontweight='bold')
    ax.set_title('Quality Assurance Evaluation: Factor Scores with 95% CI', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)
    ax.set_ylim(0, 105)
    ax.grid(axis='y', alpha=0.3)
    
    # Horizontal line at 50 (mid-point)
    ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='Mid-point (50)')
    ax.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved to {save_path}")
    
    plt.show()
    print("  ✓ Factor bar chart created")

def plot_correlation_heatmap(corr_matrix: pd.DataFrame, save_path: Optional[str] = None):
    """
    Correlation matrix ka heatmap banata hai
    """
    print("\n🔥 Creating correlation heatmap...")
    
    # Create Labels ko readable 
    labels = [col.replace('_score', '').replace('_', ' ').title() 
              for col in corr_matrix.columns]
    
    # Create Heatmap 
    fig, ax = plt.subplots(figsize=(14, 12))
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn', 
                center=0, vmin=-1, vmax=1,
                square=True, linewidths=0.5,
                cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"},
                xticklabels=labels, yticklabels=labels,
                ax=ax)
    
    ax.set_title('Correlation Matrix: E-Learning Factors', 
                 fontsize=16, fontweight='bold', pad=20)
    
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved to {save_path}")
    
    plt.show()
    print("  ✓ Correlation heatmap created")

def plot_radar_chart(scores_df: pd.DataFrame, 
                     respondent_id: Optional[str] = None,
                     use_mean: bool = True,
                     save_path: Optional[str] = None):
    """
    Radar (spider) chart banata hai - ek respondent ya average profile ke liye
    """
    print("\n🕸️ Creating radar chart...")
    
    # Main factors select
    factors = ['platform_design_score', 'interaction_score', 
               'engagement_score', 'technical_score', 
               'instructor_support_score', 'satisfaction_score']
    
    factors_available = [f for f in factors if f in scores_df.columns]
    
    # Data select
    if use_mean:
        values = [scores_df[f].mean() for f in factors_available]
        title = 'Average E-Learning Profile (All Respondents)'
    else:
        if respondent_id is None:
            respondent_id = scores_df['respondent_id'].iloc[0]
        row = scores_df[scores_df['respondent_id'] == respondent_id].iloc[0]
        values = [row[f] for f in factors_available]
        title = f'E-Learning Profile: Respondent {respondent_id}'
    
    # Labels
    labels = [f.replace('_score', '').replace('_', ' ').title() 
              for f in factors_available]
    
    # Angles calculate
    num_vars = len(factors_available)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]  # Complete the circle
    angles += angles[:1]
    
    # Radar chart banao
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    ax.plot(angles, values, 'o-', linewidth=2, color='#2E86AB', label='Score')
    ax.fill(angles, values, alpha=0.25, color='#2E86AB')
    
    # Formatting
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=11)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], size=9)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(title, size=14, fontweight='bold', pad=30)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved to {save_path}")
    
    plt.show()
    print("  ✓ Radar chart created")

def plot_boxplots(scores_df: pd.DataFrame, save_path: Optional[str] = None):
    """
    Saare factors ke liye boxplots banata hai (distribution dekhne ke liye)
    """
    print("\n📦 Creating boxplots...")
    
    # Select score columns  
    score_cols = [col for col in scores_df.columns 
                  if col.endswith('_score') and col != 'respondent_id']
    
    # Prepare Data  
    data_to_plot = []
    labels = []
    
    for col in score_cols:
        data_to_plot.append(scores_df[col].dropna().values)
        labels.append(col.replace('_score', '').replace('_', '\n').title())
    
    # Create Boxplot 
    fig, ax = plt.subplots(figsize=(16, 8))
    
    bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                    notch=True, showmeans=True,
                    boxprops=dict(facecolor='lightblue', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2),
                    meanprops=dict(marker='D', markerfacecolor='green', markersize=8))
    
    # Formatting
    ax.set_xlabel('Factors', fontsize=14, fontweight='bold')
    ax.set_ylabel('Score (0-100)', fontsize=14, fontweight='bold')
    ax.set_title('Distribution of E-Learning Factor Scores', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 105)
    
    # Legend
    ax.legend([bp['medians'][0], bp['means'][0]], 
              ['Median', 'Mean'], loc='upper right')
    
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved to {save_path}")
    
    plt.show()
    print("  ✓ Boxplots created")

def plot_achievement_vs_factors(scores_df: pd.DataFrame, save_path: Optional[str] = None):
    """
    Achievement vs different factors - scatter plots with regression lines
    """
    print("\n📈 Creating achievement comparison plots...")
    
    if 'achievement_score' not in scores_df.columns:
        print("  ⚠ Achievement score not found, skipping...")
        return
    
    # Main factors to compare
    factors = ['platform_design_score', 'interaction_score', 
               'engagement_score', 'motivation_score']
    
    factors_available = [f for f in factors if f in scores_df.columns]
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()
    
    for idx, factor in enumerate(factors_available[:4]):
        ax = axes[idx]
        
        # Data
        x = scores_df[factor].dropna()
        y = scores_df.loc[x.index, 'achievement_score']
        
        # Scatter plot
        ax.scatter(x, y, alpha=0.6, s=50, color='steelblue', edgecolor='black')
        
        # Regression line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "r--", alpha=0.8, linewidth=2, label=f'Trend line')
        
        # Correlation
        corr = x.corr(y)
        
        # Labels
        factor_name = factor.replace('_score', '').replace('_', ' ').title()
        ax.set_xlabel(f'{factor_name} Score', fontsize=11, fontweight='bold')
        ax.set_ylabel('Achievement Score', fontsize=11, fontweight='bold')
        ax.set_title(f'{factor_name} vs Achievement (r={corr:.3f})', 
                     fontsize=12, fontweight='bold')
        ax.grid(alpha=0.3)
        ax.legend()
    
    plt.suptitle('Relationship between Factors and Achievement', 
                 fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved to {save_path}")
    
    plt.show()
    print("  ✓ Achievement comparison plots created")


if __name__ == "__main__":
    # For Testing
    print("Testing visualize.py...")
    from data_loader import load_survey_data
    from scoring import compute_all_scores
    from analysis import compute_correlations
    
    try:
        # Load data and score 
        df = load_survey_data('../data/synthetic_survey.csv')
        scores_df = compute_all_scores(df)
        
        # Visualizations banao
        plot_factor_bars(scores_df)
        
        corr_matrix = compute_correlations(scores_df)
        plot_correlation_heatmap(corr_matrix)
        
        plot_radar_chart(scores_df, use_mean=True)
        
        plot_boxplots(scores_df)
        
        plot_achievement_vs_factors(scores_df)
        
        print("\n✅ All visualizations created successfully!")
        
    except Exception as e:
        print(f"Error: {e}")