import uuid
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict

from app.services.merchant_cleaner import clean_merchant_name
from app.services.categorizer import categorize_transaction
from app.services.subscriptions import detect_subscriptions
from app.services.anomalies import detect_anomalies
from app.services.health_score import calculate_health_score
from app.services.tax_helper import analyze_tax_transactions
from app.database import save_session, save_transactions, save_insights

CATEGORY_COLORS = {
    "Food & Dining": "#F59E0B",
    "Groceries": "#10B981",
    "Shopping": "#EC4899",
    "Rent": "#6366F1",
    "Utilities": "#06B6D4",
    "Transport": "#8B5CF6",
    "Entertainment": "#F43F5E",
    "Healthcare": "#14B8A6",
    "Education": "#3B82F6",
    "Travel": "#F97316",
    "Investments": "#10B981",
    "Transfers": "#64748B",
    "Salary": "#22C55E",
    "Freelance/Business Income": "#14B8A6",
    "Cash Withdrawal": "#94A3B8",
    "Other": "#A1A1AA"
}

def process_statement_pipeline(
    raw_txns: List[Dict[str, Any]], 
    filename: str, 
    file_type: str, 
    is_demo: bool = False
) -> Dict[str, Any]:
    """
    Core FinLens processing pipeline:
    Raw transactions -> Cleaned & Normalized -> Subscriptions -> Anomalies -> Health Score -> Tax -> DB
    """
    if not raw_txns:
        raise ValueError("No valid transactions to process.")

    session_id = f"sess_{uuid.uuid4().hex[:12]}"
    upload_time = datetime.now().isoformat()

    # Step 1: Normalization, Merchant Cleaning, and Auto-Categorization
    normalized_txns = []
    dates = []
    
    for item in raw_txns:
        raw_date = item["raw_date"]
        raw_desc = item["raw_description"]
        amt = float(item["amount"])
        t_type = item["type"].lower()
        bal = item.get("balance")
        
        dates.append(raw_date)
        
        # Clean merchant & get hint
        clean_merch, hint = clean_merchant_name(raw_desc)
        
        # Categorize
        cat, conf, cat_reason = categorize_transaction(clean_merch, raw_desc, t_type, hint)
        
        normalized_txns.append({
            "id": f"txn_{uuid.uuid4().hex[:8]}",
            "date": raw_date,
            "raw_description": raw_desc,
            "merchant": clean_merch,
            "amount": amt,
            "type": t_type,
            "balance": bal,
            "category": cat,
            "confidence": round(conf, 2),
            "category_reason": cat_reason,
            "is_recurring": False,
            "recurring_cadence": None,
            "is_anomaly": False,
            "anomaly_reason": None,
            "is_tax_relevant": False,
            "tax_category": None,
            "tax_reason": None
        })

    # Sort all transactions chronologically
    normalized_txns.sort(key=lambda x: x["date"])
    date_start = normalized_txns[0]["date"] if normalized_txns else None
    date_end = normalized_txns[-1]["date"] if normalized_txns else None

    # Step 2: Subscriptions Detection
    subscriptions, recurring_monthly_spend = detect_subscriptions(normalized_txns)

    # Step 3: Anomaly Detection
    anomalies = detect_anomalies(normalized_txns)

    # Step 4: Tax Deductions Analysis
    tax_summary = analyze_tax_transactions(normalized_txns)

    # Step 5: Metrics & Spending Aggregations
    total_income = round(sum(t["amount"] for t in normalized_txns if t["type"] == "credit"), 2)
    total_expenses = round(sum(t["amount"] for t in normalized_txns if t["type"] == "debit"), 2)
    net_savings = round(total_income - total_expenses, 2)
    savings_rate = round((net_savings / total_income * 100), 1) if total_income > 0 else 0.0

    # Category breakdown (for debit expenses)
    cat_spend = defaultdict(float)
    cat_counts = defaultdict(int)
    for t in normalized_txns:
        if t["type"] == "debit" and t["amount"] > 0:
            cat_spend[t["category"]] += t["amount"]
            cat_counts[t["category"]] += 1

    category_breakdown = []
    for cat, amt in cat_spend.items():
        pct = round((amt / total_expenses * 100), 1) if total_expenses > 0 else 0.0
        category_breakdown.append({
            "category": cat,
            "total_amount": round(amt, 2),
            "percentage": pct,
            "count": cat_counts[cat],
            "color": CATEGORY_COLORS.get(cat, "#64748B")
        })
    category_breakdown.sort(key=lambda x: x["total_amount"], reverse=True)
    top_categories = category_breakdown[:5]

    # Spending Trends over time
    # Group by date or period
    trend_map = defaultdict(lambda: {"expenses": 0.0, "income": 0.0})
    for t in normalized_txns:
        d = t["date"]
        if t["type"] == "debit":
            trend_map[d]["expenses"] += t["amount"]
        else:
            trend_map[d]["income"] += t["amount"]

    spending_trends = []
    for d in sorted(trend_map.keys()):
        spending_trends.append({
            "period": d,
            "expenses": round(trend_map[d]["expenses"], 2),
            "income": round(trend_map[d]["income"], 2)
        })

    # Step 6: Transparent Financial Health Score
    health_breakdown = calculate_health_score(
        total_income=total_income,
        total_expenses=total_expenses,
        recurring_monthly_spend=recurring_monthly_spend,
        category_totals=cat_spend,
        anomalies=anomalies
    )
    health_score = health_breakdown["score"]

    # Step 7: Persist into SQLite
    session_record = {
        "id": session_id,
        "filename": filename,
        "file_type": file_type,
        "upload_time": upload_time,
        "date_start": date_start,
        "date_end": date_end,
        "is_demo": is_demo,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
        "health_score": health_score,
        "currency": "INR"
    }
    save_session(session_record)
    save_transactions(session_id, normalized_txns)
    save_insights(session_id, {
        "health_breakdown": health_breakdown,
        "subscriptions": subscriptions,
        "anomalies": anomalies,
        "tax_summary": tax_summary,
        "spending_trends": spending_trends,
        "top_categories": top_categories
    })

    return {
        "session_id": session_id,
        "filename": filename,
        "is_demo": is_demo,
        "upload_time": upload_time,
        "date_start": date_start,
        "date_end": date_end,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "health_score": health_score,
        "health_breakdown": health_breakdown,
        "category_breakdown": category_breakdown,
        "spending_trends": spending_trends,
        "top_categories": top_categories,
        "recurring_monthly_spend": recurring_monthly_spend,
        "subscriptions": subscriptions,
        "anomalies": anomalies,
        "tax_summary": tax_summary,
        "transaction_count": len(normalized_txns)
    }
