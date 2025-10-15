# 📚 Framework for Quality Assurance in Educational apps

---

## 🎯 Features

✅ **Multi-dimensional Evaluation**
- Platform Design (Content Quality + UI Usability)
- Interaction (Teacher-Student + Peer)
- Engagement (Motivation + Autonomy)
- Technical Factors (Accessibility + Reliability)
- Instructor Support
- Outcomes (Achievement + Satisfaction)

✅ **Statistical Analysis**
- Cronbach's Alpha (Reliability)
- Pearson Correlations
- Descriptive Statistics with 95% CI
- Missing data handling

✅ **Advanced Modeling**
- Path Analysis
- Mediation Testing
- Multiple Regression
- Structural Equation Modeling concepts

✅ **Beautiful Visualizations**
- Factor bar charts with confidence intervals
- Correlation heatmaps
- Radar (spider) charts
- Boxplots for distributions
- Achievement comparison plots

✅ **Interactive Dashboard**
- Streamlit-based web interface
- File upload functionality
- Customizable factor weights
- Downloadable reports

---

## 🚀 Quick Start (5 Minutes Setup!)

### 1️⃣ Prerequisites
```bash
# Check Python version (3.8+ required)
python --version
```

### 2️⃣ Clone/Download Project
```bash
# Create project folder
mkdir elearning_framework
cd elearning_framework
```

### 3️⃣ Install Dependencies
```bash
# Install all required libraries
pip install -r requirements.txt
```

### 4️⃣ Generate Sample Data
```bash
# Go to src folder and run data generator
cd src
python data_generator.py
cd ..
```

### 5️⃣ Launch Dashboard
```bash
# Run Streamlit app
streamlit run src/app.py
```


---

## 📁 Project Structure

```
Framework for Quality Assurance in Educational apps/
│
├── README.md                 # Yeh file (documentation)
├── requirements.txt          # Python dependencies list
│
├── data/
│   ├── synthetic_survey.csv      # Sample data (auto-generated)
│   └── real_data_template.csv    # Template for your data
│
├── src/
│   ├── __init__.py              # Package initializer
│   ├── data_loader.py           # CSV loading & validation
│   ├── scoring.py               # Likert → 0-100 scoring
│   ├── analysis.py              # Statistical analysis
│   ├── model.py                 # Regression & path analysis
│   ├── visualize.py             # Plotting functions
│   ├── app.py                   # Streamlit dashboard
│   └── data_generator.py        # Synthetic data creator
│
├── notebooks/
│   └── demo.ipynb               # Jupyter notebook demo
│
└── tests/
    └── test_scoring.py          # Unit tests (pytest)
```

---

## 📊 Data Format

### Required CSV Columns:

| Column Name | Type | Range | Description |
|-------------|------|-------|-------------|
| respondent_id | string | - | Unique identifier for each respondent |
| timestamp | datetime | - | Survey submission time |
| content_quality_q1 | int | 1-5 | Likert: Content relevance |
| content_quality_q2 | int | 1-5 | Likert: Content depth |
| ui_usability_q1 | int | 1-5 | Likert: Interface ease of use |
| ui_usability_q2 | int | 1-5 | Likert: Navigation clarity |
| teacher_student_q1 | int | 1-5 | Likert: Teacher responsiveness |
| teacher_student_q2 | int | 1-5 | Likert: Feedback quality |
| peer_q1 | int | 1-5 | Likert: Peer collaboration |
| peer_q2 | int | 1-5 | Likert: Community engagement |
| motivation_q1 | int | 1-5 | Likert: Learning motivation |
| motivation_q2 | int | 1-5 | Likert: Course enthusiasm |
| autonomy_q1 | int | 1-5 | Likert: Self-paced control |
| autonomy_q2 | int | 1-5 | Likert: Learning flexibility |
| accessibility_q1 | int | 1-5 | Likert: Device accessibility |
| reliability_q1 | int | 1-5 | Likert: Platform stability |
| instructor_support_q1 | int | 1-5 | Likert: Support availability |
| instructor_support_q2 | int | 1-5 | Likert: Support quality |
| achievement_score | float | 0-100 | Academic performance score |
| satisfaction_q1 | int | 1-5 | Likert: Overall satisfaction |
| satisfaction_q2 | int | 1-5 | Likert: Recommendation likelihood |

**Template download:** `data/real_data_template.csv`

---

## 💻 Usage Examples

### Command Line Usage

#### 1. Load and Score Data
```python
from src.data_loader import load_survey_data
from src.scoring import compute_all_scores

# Load CSV
df = load_survey_data('data/synthetic_survey.csv')

# Compute scores
scores_df = compute_all_scores(df)
print(scores_df.head())
```

#### 2. Statistical Analysis
```python
from src.analysis import compute_reliability, compute_correlations

# Reliability analysis (Cronbach's Alpha)
reliability = compute_reliability(df)
print(reliability)

# Correlation matrix
corr_matrix = compute_correlations(scores_df)
print(corr_matrix)
```

#### 3. Generate Visualizations
```python
from src.visualize import plot_factor_bars, plot_correlation_heatmap

# Bar chart with confidence intervals
plot_factor_bars(scores_df, save_path='factor_bars.png')

# Correlation heatmap
plot_correlation_heatmap(corr_matrix, save_path='correlations.png')
```

#### 4. Run Path Analysis
```python
from src.model import run_path_analysis

# Test hypotheses
results = run_path_analysis(scores_df)
print(results)
```

### Web Dashboard Usage

1. **Launch app:**
   ```bash
   streamlit run src/app.py
   ```

2. **Upload data:**
   - Sidebar → "Upload CSV" option
   - Select your CSV file

3. **Compute scores:**
   - Go to "Scores" tab
   - Adjust weights (optional)
   - Click "Compute Scores"

4. **Explore analysis:**
   - "Analysis" tab → View statistics & visualizations
   - "Models" tab → Run path analysis
   - "Reports" tab → Download comprehensive report

---

## 🔢 Scoring Method

### 1. Item Level (Raw Responses)
- Likert scale: 1 (Strongly Disagree) to 5 (Strongly Agree)

### 2. Factor Level (Aggregated Scores)
```
Formula: score = (mean_of_items - 1) / 4 × 100

Examples:
- Mean = 1 → Score = 0
- Mean = 3 → Score = 50
- Mean = 5 → Score = 100
```

### 3. Overall Framework Score
```
Weighted average of main dimensions:
- Platform Design (default weight: 0.20)
- Interaction (default weight: 0.20)
- Engagement (default weight: 0.20)
- Technical (default weight: 0.20)
- Instructor Support (default weight: 0.20)
```


---

## 📈 Analysis Methods

### Reliability Analysis
- **Cronbach's Alpha** computed for each factor
- Interpretation:
  - α ≥ 0.9: Excellent
  - α ≥ 0.8: Good
  - α ≥ 0.7: Acceptable
  - α < 0.7: Questionable

### Correlation Analysis
- **Pearson correlation** between all factors
- Significance testing (p < 0.05)

### Path Analysis
Tests key hypotheses:
- **H1:** Platform Design → Motivation → Achievement
- **H2:** Interaction → Satisfaction
- **H3:** Engagement → Achievement & Satisfaction

---

## 🧪 Testing

### Run Unit Tests
```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src tests/
```

### Test Individual Modules
```bash
cd src
python data_loader.py      # Test data loading
python scoring.py          # Test scoring
python analysis.py         # Test analysis
```

---

## 📦 Dependencies

```
pandas>=2.0.0          # Data manipulation
numpy>=1.24.0          # Numerical computing
scipy>=1.10.0          # Scientific computing
statsmodels>=0.14.0    # Statistical models
matplotlib>=3.7.0      # Plotting
seaborn>=0.12.0        # Enhanced visualizations
streamlit>=1.28.0      # Web dashboard
openpyxl>=3.1.0        # Excel export
pingouin>=0.5.3        # Statistical functions
pytest>=7.4.0          # Testing framework
```

---

## 🛠️ Customization

### Change Factor Weights
```python
custom_weights = {
    'platform_design_score': 0.30,
    'interaction_score': 0.25,
    'engagement_score': 0.20,
    'technical_score': 0.15,
    'instructor_support_score': 0.10
}

scores_df = compute_all_scores(df, weights=custom_weights)
```

### Add New Factors
1. Edit `scoring.py` → Add to `FACTOR_ITEMS` dictionary
2. Add corresponding columns in your CSV
3. Update validation in `data_loader.py`

### Modify Hypotheses
Edit `model.py` → `run_path_analysis()` function

---

## 🐛 Troubleshooting

### Common Issues

**1. Module not found error**
```bash
pip install <module_name>
```

**2. Streamlit not opening**
```bash
# Check if streamlit is installed
pip show streamlit

# Reinstall if needed
pip install --upgrade streamlit

# Run with full path
python -m streamlit run src/app.py
```

**3. Data file not found**
```bash
# Make sure you're in the correct directory
pwd  # Check current location

# Generate sample data
cd src
python data_generator.py
cd ..
```

**4. Permission denied (Windows)**
```bash
pip install --user -r requirements.txt
```

---

## 📚 Learning Resources

### Understanding the Framework
- **Likert Scales:** 1-5 rating system
- **Cronbach's Alpha:** Reliability measure
- **Path Analysis:** Testing causal relationships
- **Mediation:** X → M → Y relationships

### Python Libraries
- [Pandas Documentation](https://pandas.pydata.org/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)

---

## 🤝 Contributing

Contributions welcome! Areas to improve:
- Additional visualization types
- More statistical tests
- Enhanced UI/UX
- Multilingual support
- Export to PowerPoint/PDF

---

## 📄 License

MIT License - Free to use and modify

---

## 📞 Support

**Issues?** 
- Check the troubleshooting section
- Review error messages carefully
- Google the specific error

**Questions about methodology?**
- Review the academic literature on e-learning evaluation
- Check statistical textbooks for analysis methods

---

## 🎓 Citation

If you use this framework in research:

```
Framework for Quality Assurance in Educational App(2024)
A comprehensive Python-based toolkit for evaluating online learning platforms
GitHub: [your-repo-url]
```

---

## ✨ Acknowledgments

Built with:
- Python 🐍
- Streamlit 🎈
- Pandas 🐼
- Matplotlib 📊
- And lots of ☕

---

**Happy Analyzing! 📚🚀**

*Made with ❤️ for educators and researchers*