import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import (
    init_db, get_session, get_transactions, get_insights, delete_session
)
from app.models import DashboardData, ChatRequest, ChatResponse
from app.parsers.csv_parser import parse_csv_statement
from app.parsers.pdf_parser import parse_pdf_statement
from app.services.demo_generator import get_demo_statement_data
from app.services.ai_assistant import query_ai_assistant
from app.pipeline import process_statement_pipeline

app = FastAPI(
    title="FinLens API",
    description="AI-powered Financial Intelligence Engine for Bank Statement Analysis",
    version="1.0.0"
)

# Enable CORS for local Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://finlens-amber.vercel.app"], #change 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "FinLens Financial Intelligence Engine"}

@app.post("/api/upload")
async def upload_statement(file: UploadFile = File(...)):
    filename = file.filename or "statement"
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    
    if ext not in ["csv", "pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF or CSV bank statement.")
        
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        
    try:
        if ext == "csv":
            raw_txns = parse_csv_statement(content)
        else:
            raw_txns = parse_pdf_statement(content)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=422, 
            detail=f"We couldn't read this statement. Please try another PDF or CSV. Error: {str(e)}"
        )
        
    if not raw_txns:
        raise HTTPException(status_code=422, detail="We couldn't identify transactions in this file.")

    try:
        dashboard_result = process_statement_pipeline(
            raw_txns=raw_txns,
            filename=filename,
            file_type=ext.upper(),
            is_demo=False
        )
        return dashboard_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process statement pipeline: {str(e)}")

@app.post("/api/demo")
def load_demo_statement():
    raw_txns = get_demo_statement_data()
    dashboard_result = process_statement_pipeline(
        raw_txns=raw_txns,
        filename="HDFC_Bank_Demo_Statement.csv",
        file_type="DEMO",
        is_demo=True
    )
    return dashboard_result

@app.get("/api/sessions/{session_id}/dashboard")
def get_dashboard_data(session_id: str):
    sess = get_session(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found or has been deleted.")
        
    insights = get_insights(session_id)
    txns = get_transactions(session_id)
    
    total_income = sess["total_income"]
    total_expenses = sess["total_expenses"]
    net_savings = sess["net_savings"]
    savings_rate = round((net_savings / total_income * 100), 1) if total_income > 0 else 0.0
    
    return {
        "session_id": sess["id"],
        "filename": sess["filename"],
        "is_demo": bool(sess["is_demo"]),
        "upload_time": sess["upload_time"],
        "date_start": sess["date_start"],
        "date_end": sess["date_end"],
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "health_score": sess["health_score"],
        "health_breakdown": insights.get("health_breakdown", {}),
        "category_breakdown": insights.get("top_categories", []),
        "spending_trends": insights.get("spending_trends", []),
        "top_categories": insights.get("top_categories", []),
        "recurring_monthly_spend": sum(s.get("average_amount", 0) for s in insights.get("subscriptions", [])),
        "subscriptions": insights.get("subscriptions", []),
        "anomalies": insights.get("anomalies", []),
        "tax_summary": insights.get("tax_summary", {}),
        "transaction_count": len(txns)
    }

@app.get("/api/sessions/{session_id}/transactions")
def list_session_transactions(
    session_id: str,
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    sort_by: str = Query("date"),
    sort_order: str = Query("desc")
):
    sess = get_session(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found.")
    txns = get_transactions(
        session_id=session_id,
        search=search,
        category=category,
        txn_type=type,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return {"transactions": txns, "total": len(txns)}

@app.get("/api/sessions/{session_id}/subscriptions")
def get_session_subscriptions(session_id: str):
    sess = get_session(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found.")
    insights = get_insights(session_id)
    subs = insights.get("subscriptions", [])
    monthly_spend = sum(s.get("average_amount", 0) for s in subs)
    return {
        "subscriptions": subs,
        "estimated_recurring_monthly_spend": round(monthly_spend, 2),
        "has_subscriptions": len(subs) > 0
    }

@app.get("/api/sessions/{session_id}/anomalies")
def get_session_anomalies(session_id: str):
    sess = get_session(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found.")
    insights = get_insights(session_id)
    anomalies = insights.get("anomalies", [])
    return {
        "anomalies": anomalies,
        "count": len(anomalies),
        "has_anomalies": len(anomalies) > 0
    }

@app.get("/api/sessions/{session_id}/tax")
def get_session_tax(session_id: str):
    sess = get_session(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found.")
    insights = get_insights(session_id)
    return insights.get("tax_summary", {})

@app.post("/api/sessions/{session_id}/chat")
def chat_with_assistant(session_id: str, request: ChatRequest):
    sess = get_session(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found or has been deleted.")
        
    txns = get_transactions(session_id)
    insights = get_insights(session_id)
    
    response = query_ai_assistant(
        message=request.message,
        transactions=txns,
        session_data=sess,
        insights=insights
    )
    return response

@app.delete("/api/sessions/{session_id}")
def purge_session(session_id: str):
    deleted = delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found or already deleted.")
    return {"status": "success", "message": "All session data and transactions have been permanently deleted."}
