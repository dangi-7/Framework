from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .database import get_session, init_db, session_scope
from .models import Evaluation
from .services.analytics import AnalyticsResult, run_analytics

app = FastAPI(title="EduGradeAI", version="2.0.0")
app.add_event_handler("startup", lambda: init_db())
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request, session: Session = Depends(get_session)):
    recent_evals = session.exec(
        select(Evaluation).order_by(Evaluation.created_at.desc()).limit(3)
    ).all()
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "recent_evaluations": recent_evals,
        },
    )


@app.get("/evaluate")
def evaluate_page(request: Request):
    return templates.TemplateResponse("evaluate.html", {"request": request})


@app.post("/evaluate")
def submit_evaluation(
    request: Request,
    app_name: str = Form(...),
    audience: str = Form("") ,
    summary: str = Form(""),
    pedagogical_design: int = Form(...),
    ui_ux: int = Form(...),
    engagement: int = Form(...),
    technical_performance: int = Form(...),
    learning_effectiveness: int = Form(...),
):
    ratings = [
        pedagogical_design,
        ui_ux,
        engagement,
        technical_performance,
        learning_effectiveness,
    ]
    quality_score = round(sum(ratings) / (len(ratings) * 5) * 100, 2)

    evaluation = Evaluation(
        app_name=app_name.strip(),
        audience=audience.strip() or None,
        summary=summary.strip() or None,
        pedagogical_design=pedagogical_design,
        ui_ux=ui_ux,
        engagement=engagement,
        technical_performance=technical_performance,
        learning_effectiveness=learning_effectiveness,
        quality_score=quality_score,
        created_at=datetime.utcnow(),
    )

    with session_scope() as session:
        session.add(evaluation)
        session.flush()
        eval_id = evaluation.id

    if not eval_id:
        raise HTTPException(status_code=500, detail="Unable to save evaluation")

    return RedirectResponse(url=f"/reports/{eval_id}", status_code=303)


@app.get("/reports")
def reports_page(request: Request, session: Session = Depends(get_session)):
    evaluations = session.exec(
        select(Evaluation).order_by(Evaluation.quality_score.desc())
    ).all()
    return templates.TemplateResponse(
        "reports.html",
        {"request": request, "evaluations": evaluations},
    )


@app.get("/reports/{evaluation_id}")
def report_detail(
    request: Request, evaluation_id: int, session: Session = Depends(get_session)
):
    evaluation = session.get(Evaluation, evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    insight = build_insights(evaluation)
    chart_data = build_chart_payload(evaluation)
    chart_json = json.dumps(chart_data)

    return templates.TemplateResponse(
        "report_detail.html",
        {
            "request": request,
            "evaluation": evaluation,
            "insight": insight,
            "chart_data": chart_json,
        },
    )


@app.get("/framework")
def framework_page(request: Request):
    return templates.TemplateResponse(
        "framework.html",
        {
            "request": request,
            "analytics": None,
            "dataset_name": None,
        },
    )


@app.post("/framework")
async def run_framework_analysis(request: Request, dataset: UploadFile = File(...)):
    file_bytes = await dataset.read()
    analytics_result: AnalyticsResult = run_analytics(file_bytes)
    analytics_dict = asdict(analytics_result)
    return templates.TemplateResponse(
        "framework.html",
        {
            "request": request,
            "analytics": analytics_dict,
            "dataset_name": dataset.filename,
        },
    )


def build_insights(evaluation: Evaluation) -> List[str]:
    scores = {
        "Pedagogical Design": evaluation.pedagogical_design,
        "UI & Usability": evaluation.ui_ux,
        "Engagement": evaluation.engagement,
        "Technical": evaluation.technical_performance,
        "Learning Impact": evaluation.learning_effectiveness,
    }
    best = max(scores, key=scores.get)
    worst = min(scores, key=scores.get)
    insights = [
        f"{best} is resonating with learners (score {scores[best]}/5). Consider showcasing successful flows to stakeholders.",
        f"{worst} needs immediate experimentation (score {scores[worst]}/5). Co-create improvements with 3 target users this week.",
    ]
    if evaluation.quality_score >= 80:
        insights.append("Overall quality is excellent. Focus on scaling adoption and measuring learning outcomes.")
    elif evaluation.quality_score >= 60:
        insights.append("Quality is solid but inconsistent. Prioritize guardrails to lift the weakest dimension.")
    else:
        insights.append("Foundational work required. Align team on success metrics and rebuild critical journeys.")
    return insights


def build_chart_payload(evaluation: Evaluation) -> dict:
    labels = [
        "Pedagogy",
        "UI/UX",
        "Engagement",
        "Technical",
        "Learning",
    ]
    data = [
        evaluation.pedagogical_design,
        evaluation.ui_ux,
        evaluation.engagement,
        evaluation.technical_performance,
        evaluation.learning_effectiveness,
    ]
    return {"labels": labels, "data": data}
