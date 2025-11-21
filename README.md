# EduGradeAI – Python Edition

A full-stack FastAPI + Jinja project that delivers the "Creating a Framework for Quality Assurance in Educational App Design" experience entirely in Python. It blends a guided evaluation flow, storytelling-ready reports, and a research analytics lab that processes CSV survey data using pandas/scikit-learn.

## Features

- **Design evaluation workflow** – capture pedagogical, UX, engagement, technical, and learning effectiveness scores via an accessible form and auto-generate insight narratives.
- **Report hub** – compare every evaluation, drill into radar charts, and highlight strongest vs riskiest factors for stakeholders.
- **Framework lab** – upload Likert-scale survey data, run descriptive stats, Cronbach α, correlations, and light path analysis.
- **Modern UI** – crafted with custom CSS, gradients, and responsive layouts (no Node build step required).
- **Pure Python stack** – FastAPI, SQLModel (SQLite), Jinja templates, pandas, numpy, scikit-learn.

## Project Structure

```
EduGradeAI/
├── app/
│   ├── main.py                # FastAPI routes + views
│   ├── models.py              # SQLModel definitions
│   ├── database.py            # SQLite engine + helpers
│   ├── services/
│   │   └── analytics.py       # Survey analytics pipeline
│   ├── templates/             # Jinja2 pages (Home, Evaluate, Reports, Framework)
│   └── static/
│       ├── css/styles.css     # Modern UI styling
│       ├── js/app.js          # Small UX helpers
│       └── data/*.csv         # Template + synthetic datasets
├── data/                      # (Reserved for future exports)
├── requirements.txt           # Python dependencies
└── README.md
```

## Getting Started

1. **Create a virtual environment (recommended)**
   ```powershell
   cd "d:\Neha project\EduGradeAI"
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the development server**
   ```powershell
   uvicorn app.main:app --reload
   ```

4. Visit `http://127.0.0.1:8000` in your browser.

## Usage Tips

- Use the **Evaluate** tab to create reports; after submission you are redirected to a radar-based insight view.
- The **Framework Lab** accepts the provided `synthetic_survey.csv` or your own dataset; download `real_data_template.csv` for the required columns.
- All data is stored in `eduapp.db` (SQLite). Delete the file if you need a clean slate.

## Tech Stack

- FastAPI · SQLModel · SQLite
- Pandas · NumPy · Scikit-learn · SciPy
- Chart.js (CDN) for radar visualization
- Custom CSS inspired by Tailwind aesthetics

## Future Enhancements

- Export PDFs of each report.
- User authentication & cohort comparisons.
- Deeper SEM models when additional survey signals are available.

Enjoy showcasing this Python-first project in your college submission! 💡
