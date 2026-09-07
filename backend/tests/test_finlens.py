import os
import pytest
from pathlib import Path
from app.database import init_db, get_session, get_transactions, delete_session
from app.parsers.csv_parser import parse_csv_statement
from app.parsers.pdf_parser import parse_pdf_statement
from app.pipeline import process_statement_pipeline
from app.services.ai_assistant import query_ai_assistant

TEST_DIR = Path("d:/FineLens/test_data")

@pytest.fixture(autouse=True)
def setup_database():
    init_db()

def test_statement_a_csv_parsing_and_pipeline():
    csv_path = TEST_DIR / "statement_a_corporate_salary.csv"
    with open(csv_path, "rb") as f:
        content = f.read()
        
    raw_txns = parse_csv_statement(content)
    assert len(raw_txns) == 18, f"Expected 18 transactions, got {len(raw_txns)}"
    
    res = process_statement_pipeline(raw_txns, "statement_a.csv", "CSV", is_demo=False)
    
    # 1. Exact Source-of-Truth financial totals
    assert res["total_income"] == 135000.0, f"Expected 135000.0, got {res['total_income']}"
    assert res["total_expenses"] == 151276.0, f"Expected 151276.0, got {res['total_expenses']}"
    assert res["net_savings"] == round(135000.0 - 151276.0, 2)
    
    # 2. Subscriptions
    subs = res["subscriptions"]
    assert len(subs) >= 2, f"Expected at least 2 subscriptions, got {len(subs)}"
    sub_merchants = [s["merchant"] for s in subs]
    assert "Netflix" in sub_merchants
    assert "Spotify" in sub_merchants
    
    # 3. Anomaly
    anomalies = res["anomalies"]
    assert len(anomalies) >= 1
    anom_merchants = [a["merchant"] for a in anomalies]
    assert "Croma Electronics" in anom_merchants
    
    # 4. Tax
    tax_items = res["tax_summary"]["items"]
    assert len(tax_items) >= 2
    tax_sections = [t["tax_section"] for t in tax_items]
    assert "80C" in tax_sections
    assert "80D" in tax_sections

def test_statement_a_pdf_parsing_and_pipeline():
    pdf_path = TEST_DIR / "statement_a_corporate_salary.pdf"
    with open(pdf_path, "rb") as f:
        content = f.read()
    raw_txns = parse_pdf_statement(content)
    assert len(raw_txns) >= 15
    res = process_statement_pipeline(raw_txns, "statement_a.pdf", "PDF", is_demo=False)
    assert res["total_income"] == 135000.0
    assert res["total_expenses"] > 100000.0
    assert len(res["subscriptions"]) >= 2

def test_statement_b_freelancer_pipeline():
    csv_path = TEST_DIR / "statement_b_freelancer_irregular.csv"
    with open(csv_path, "rb") as f:
        content = f.read()
        
    raw_txns = parse_csv_statement(content)
    res = process_statement_pipeline(raw_txns, "statement_b.csv", "CSV", is_demo=False)
    
    # 1. Completely different numbers
    assert res["total_income"] == 62500.0, f"Expected 62500.0, got {res['total_income']}"
    assert res["total_expenses"] == 16500.0, f"Expected 16500.0, got {res['total_expenses']}"
    assert res["net_savings"] == 46000.0
    assert res["savings_rate"] == 73.6
    
    # 2. ZERO subscriptions in Statement B
    assert len(res["subscriptions"]) == 0, "Statement B must have 0 subscriptions"
    assert res["recurring_monthly_spend"] == 0.0

def test_statement_c_minimalist_pipeline():
    csv_path = TEST_DIR / "statement_c_minimalist_no_subscriptions.csv"
    with open(csv_path, "rb") as f:
        content = f.read()
        
    raw_txns = parse_csv_statement(content)
    res = process_statement_pipeline(raw_txns, "statement_c.csv", "CSV", is_demo=False)
    
    assert res["total_income"] == 45000.0
    assert res["total_expenses"] == 9400.0
    assert len(res["subscriptions"]) == 0
    assert len(res["anomalies"]) == 0

def test_ai_assistant_grounding():
    csv_path = TEST_DIR / "statement_a_corporate_salary.csv"
    with open(csv_path, "rb") as f:
        raw_txns = parse_csv_statement(f.read())
    res = process_statement_pipeline(raw_txns, "statement_a.csv", "CSV", is_demo=False)
    
    txns = get_transactions(res["session_id"])
    sess = get_session(res["session_id"])
    
    # Q1: Food spending
    ans1 = query_ai_assistant("How much did I spend on food?", txns, sess, res)
    assert "₹" in ans1["answer"]
    assert "Food & Dining" in ans1["answer"]
    
    # Q2: Biggest expense
    ans2 = query_ai_assistant("What was my biggest expense?", txns, sess, res)
    assert "Croma Electronics" in ans2["answer"]
    assert "74,990" in ans2["answer"]
    
    # Q3: Subscriptions
    ans3 = query_ai_assistant("Do I have recurring subscriptions?", txns, sess, res)
    assert "Netflix" in ans3["answer"]
    assert "Spotify" in ans3["answer"]
    
    # Q4: Out of scope inquiry
    ans4 = query_ai_assistant("What is my credit score?", txns, sess, res)
    assert "cannot determine that from the uploaded statement" in ans4["answer"].lower()

def test_privacy_purge():
    csv_path = TEST_DIR / "statement_c_minimalist_no_subscriptions.csv"
    with open(csv_path, "rb") as f:
        raw_txns = parse_csv_statement(f.read())
    res = process_statement_pipeline(raw_txns, "statement_c.csv", "CSV", is_demo=False)
    sess_id = res["session_id"]
    
    assert get_session(sess_id) is not None
    assert len(get_transactions(sess_id)) > 0
    
    # Perform delete
    deleted = delete_session(sess_id)
    assert deleted is True
    assert get_session(sess_id) is None
    assert len(get_transactions(sess_id)) == 0
