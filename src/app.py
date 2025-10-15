"""
Streamlit Web Application
Interactive dashboard for Framework for Quality Assurance in Educational apps
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# Import our modules
from data_loader import load_survey_data, validate_schema
from scoring import compute_all_scores, get_default_weights, FACTOR_ITEMS
from analysis import (compute_reliability, compute_correlations, 
                     compute_descriptive_stats, generate_analysis_report)
from model import run_path_analysis, generate_model_report
from visualize import (plot_factor_bars, plot_correlation_heatmap, 
                      plot_radar_chart, plot_boxplots, plot_achievement_vs_factors)

# Page config
st.set_page_config(
    page_title="Framework for Quality Assurance",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📚 Framework for Quality Assurance in Educational apps</div>', 
            unsafe_allow_html=True)

st.markdown("""
### A Comprehensive Tool for Evaluating E-Learning Platforms

This framework evaluates online learning platforms across six key dimensions:
- **Platform Design:** Content quality and UI usability
- **Interaction:** Teacher-student and peer interactions
- **Engagement:** Learner motivation and autonomy
- **Technical Factors:** Accessibility and system reliability
- **Instructor Support:** Quality and availability of instructional assistance
- **Outcomes:** Academic achievement and learner satisfaction

**Features:**
- Multi-factor scoring system (Likert scale to 0-100)
- Statistical reliability analysis (Cronbach's α)
- Correlation and regression modeling
- Path analysis for testing causal relationships
- Interactive visualizations and downloadable reports
""")

# Sidebar
st.sidebar.title("⚙️ Settings")

# Data upload option
data_source = st.sidebar.radio(
    "Data Source:",
    ["📁 Upload CSV", "🎲 Use Sample Data"]
)

df = None
scores_df = None

# Data loading
if data_source == "📁 Upload CSV":
    uploaded_file = st.sidebar.file_uploader(
        "Upload your survey data (CSV format)",
        type=['csv'],
        help="File must contain required columns as per schema"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success(f"✅ File loaded: {len(df)} responses")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading file: {e}")
else:
    # Use sample data
    try:
        df = pd.read_csv('data/synthetic_survey.csv')
        st.sidebar.success(f"✅ Sample data loaded: {len(df)} responses")
    except:
        st.sidebar.warning("⚠️ Sample data not found. Please run data_generator.py first!")

# Main content
if df is not None:
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Data Overview", 
        "🎯 Scores", 
        "📈 Analysis", 
        "🔬 Models",
        "📄 Reports"
    ])
    
    # TAB 1: Data Overview
    with tab1:
        st.header("📊 Data Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Respondents", len(df))
        with col2:
            st.metric("Total Questions", len([c for c in df.columns if c.endswith(('_q1', '_q2'))]))
        with col3:
            missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
            st.metric("Missing Data %", f"{missing_pct:.1f}%")
        
        st.subheader("📋 Schema Validation")
        is_valid, errors = validate_schema(df)
        if is_valid:
            st.success("✅ Schema validation passed!")
        else:
            st.error("❌ Schema validation failed:")
            for error in errors:
                st.write(f"- {error}")
        
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        st.subheader("📊 Descriptive Statistics")
        st.dataframe(df.describe(), use_container_width=True)
    
    # TAB 2: Scores
    with tab2:
        st.header("🎯 Factor Score Calculation")
        
        st.markdown("""
        **Scoring Method:**
        - Each factor is composed of multiple Likert-scale items (1-5)
        - Factor scores are calculated as: `(mean - 1) / 4 × 100`
        - This converts ratings to a 0-100 scale for easier interpretation
        - Overall framework score is a weighted average of dimension scores
        """)
        
        # Weight customization
        st.subheader("⚖️ Customize Factor Weights")
        st.write("Adjust weights for overall framework score calculation (default = equal weights)")
        
        default_weights = get_default_weights()
        weights = {}
        
        col1, col2 = st.columns(2)
        with col1:
            weights['platform_design_score'] = st.slider(
                "Platform Design", 0.0, 1.0, 
                default_weights['platform_design_score'], 0.05
            )
            weights['interaction_score'] = st.slider(
                "Interaction", 0.0, 1.0, 
                default_weights['interaction_score'], 0.05
            )
            weights['engagement_score'] = st.slider(
                "Engagement", 0.0, 1.0, 
                default_weights['engagement_score'], 0.05
            )
        
        with col2:
            weights['technical_score'] = st.slider(
                "Technical Factors", 0.0, 1.0, 
                default_weights['technical_score'], 0.05
            )
            weights['instructor_support_score'] = st.slider(
                "Instructor Support", 0.0, 1.0, 
                default_weights['instructor_support_score'], 0.05
            )
        
        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v/total_weight for k, v in weights.items()}
        
        st.info(f"Total weight: {sum(weights.values()):.2f} (normalized to 1.0)")
        
        # Compute scores
        if st.button("🔄 Compute Scores", type="primary"):
            with st.spinner("Computing scores..."):
                scores_df = compute_all_scores(df, weights)
                st.session_state['scores_df'] = scores_df
                st.success("✅ Scores computed successfully!")
        
        # Display scores
        if 'scores_df' in st.session_state:
            scores_df = st.session_state['scores_df']
            
            st.subheader("📊 Score Summary")
            
            # Overall score
            overall_mean = scores_df['overall_framework_score'].mean()
            overall_std = scores_df['overall_framework_score'].std()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Overall Score (Mean)", f"{overall_mean:.1f}")
            with col2:
                st.metric("Standard Deviation", f"{overall_std:.1f}")
            with col3:
                st.metric("Minimum Score", f"{scores_df['overall_framework_score'].min():.1f}")
            with col4:
                st.metric("Maximum Score", f"{scores_df['overall_framework_score'].max():.1f}")
            
            st.subheader("📋 Complete Score Table")
            st.dataframe(scores_df, use_container_width=True)
            
            # Download option
            csv = scores_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Scores (CSV)",
                data=csv,
                file_name="elearning_scores.csv",
                mime="text/csv"
            )
    
    # TAB 3: Analysis
    with tab3:
        st.header("📈 Statistical Analysis")
        
        if 'scores_df' in st.session_state:
            scores_df = st.session_state['scores_df']
            
            # Reliability Analysis
            st.subheader("🔬 Reliability Analysis (Cronbach's Alpha)")
            st.markdown("""
            Cronbach's α measures internal consistency:
            - **α ≥ 0.9:** Excellent reliability
            - **α ≥ 0.8:** Good reliability  
            - **α ≥ 0.7:** Acceptable reliability
            - **α < 0.7:** Questionable reliability
            """)
            reliability_df = compute_reliability(df)
            st.dataframe(reliability_df, use_container_width=True)
            
            # Descriptive Stats
            st.subheader("📊 Descriptive Statistics (0-100 Scale)")
            desc_stats = compute_descriptive_stats(scores_df)
            st.dataframe(desc_stats, use_container_width=True)
            
            # Correlations
            st.subheader("🔗 Correlation Matrix")
            corr_matrix = compute_correlations(scores_df)
            
            fig, ax = plt.subplots(figsize=(12, 10))
            import seaborn as sns
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn', 
                       center=0, square=True, ax=ax)
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)
            
            # Visualizations
            st.subheader("📊 Visualizations")
            
            viz_option = st.selectbox(
                "Select visualization type:",
                ["Bar Chart", "Boxplots", "Radar Chart", "Achievement Analysis"]
            )
            
            if viz_option == "Bar Chart":
                fig, ax = plt.subplots(figsize=(14, 6))
                plot_factor_bars(scores_df)
                st.pyplot(plt.gcf())
            
            elif viz_option == "Boxplots":
                fig, ax = plt.subplots(figsize=(14, 6))
                plot_boxplots(scores_df)
                st.pyplot(plt.gcf())
            
            elif viz_option == "Radar Chart":
                respondent_option = st.radio(
                    "Profile type:",
                    ["Average (All Respondents)", "Individual Respondent"]
                )
                
                if respondent_option == "Average (All Respondents)":
                    fig, ax = plt.subplots(figsize=(8, 8))
                    plot_radar_chart(scores_df, use_mean=True)
                    st.pyplot(plt.gcf())
                else:
                    resp_id = st.selectbox(
                        "Select respondent:",
                        scores_df['respondent_id'].tolist()
                    )
                    fig, ax = plt.subplots(figsize=(8, 8))
                    plot_radar_chart(scores_df, respondent_id=resp_id, use_mean=False)
                    st.pyplot(plt.gcf())
            
            elif viz_option == "Achievement Analysis":
                fig, ax = plt.subplots(figsize=(14, 10))
                plot_achievement_vs_factors(scores_df)
                st.pyplot(plt.gcf())
        
        else:
            st.info("⚠️ Please compute scores in the 'Scores' tab first!")
    
    # TAB 4: Models
    with tab4:
        st.header("🔬 Path Analysis & Regression Models")
        
        if 'scores_df' in st.session_state:
            scores_df = st.session_state['scores_df']
            
            st.markdown("""
            **Research Hypotheses Tested:**
            - **H1:** Platform Design → Motivation → Achievement (mediation model)
            - **H2:** Interaction → Satisfaction (direct effect)
            - **H3a:** Engagement → Achievement
            - **H3b:** Engagement → Satisfaction
            
            These models test causal relationships between framework dimensions and learning outcomes.
            """)
            
            if st.button("▶️ Run Path Analysis", type="primary"):
                with st.spinner("Running statistical models..."):
                    results = run_path_analysis(scores_df)
                    st.session_state['model_results'] = results
                    st.success("✅ Path analysis completed!")
            
            if 'model_results' in st.session_state:
                results = st.session_state['model_results']
                report = generate_model_report(results)
                
                st.subheader("📊 Results Summary")
                st.text(report)
                
                # Detailed results
                st.subheader("📋 Detailed Model Output")
                for key, value in results.items():
                    with st.expander(f"🔍 {key}"):
                        if isinstance(value, dict):
                            for k, v in value.items():
                                if k != 'summary':
                                    st.write(f"**{k}:** {v}")
        else:
            st.info("⚠️ Please compute scores in the 'Scores' tab first!")
    
    # TAB 5: Reports
    with tab5:
        st.header("📄 Comprehensive Evaluation Report")
        
        if 'scores_df' in st.session_state:
            scores_df = st.session_state['scores_df']
            
            st.subheader("📝 Full Analysis Report")
            report = generate_analysis_report(df, scores_df)
            
            st.text_area(
                "Report Content:", 
                report, 
                height=400,
                help="Copy this report for your records"
            )
            
            # Download report
            st.download_button(
                label="📥 Download Report (TXT)",
                data=report,
                file_name="elearning_evaluation_report.txt",
                mime="text/plain"
            )
            
        else:
            st.info("⚠️ Please compute scores in the 'Scores' tab first!")

else:
    st.info("👆 Please upload data or select sample data from the sidebar")
    
    # Instructions
    st.markdown("""
    ### 📖 How to Use This Framework:
    
    1. **Upload Data:** Use the sidebar to upload your CSV file or select sample data
    2. **Validate Schema:** Check the Data Overview tab to ensure your data is properly formatted
    3. **Compute Scores:** Navigate to the Scores tab, adjust weights if needed, and compute factor scores
    4. **Analyze Results:** View statistical analysis, reliability metrics, and visualizations in the Analysis tab
    5. **Test Hypotheses:** Run path analysis models in the Models tab
    6. **Generate Report:** Download a comprehensive evaluation report from the Reports tab
    
    ### 📋 Required CSV Format:
    
    Your CSV file must contain these columns:
    - `respondent_id`: Unique identifier for each survey respondent
    - `timestamp`: Date and time of survey completion
    - Likert-scale items (1-5 ratings): `content_quality_q1`, `ui_usability_q1`, etc.
    - `achievement_score`: Academic performance score (0-100)
    
    A template file is available in `data/real_data_template.csv`
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>📚Framework for Quality Assurance of Educational Apps v1.0</p>
    <p>Built with Python, Pandas, Streamlit | For research and educational assessment</p>
</div>
""", unsafe_allow_html=True)