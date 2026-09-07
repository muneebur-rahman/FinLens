import sqlite3
import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "finlens.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        file_type TEXT NOT NULL,
        upload_time TEXT NOT NULL,
        date_start TEXT,
        date_end TEXT,
        is_demo INTEGER DEFAULT 0,
        total_income REAL DEFAULT 0,
        total_expenses REAL DEFAULT 0,
        net_savings REAL DEFAULT 0,
        health_score INTEGER DEFAULT 0,
        currency TEXT DEFAULT 'INR'
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        date TEXT NOT NULL,
        raw_description TEXT NOT NULL,
        merchant TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        balance REAL,
        category TEXT NOT NULL,
        confidence REAL DEFAULT 0.8,
        category_reason TEXT,
        is_recurring INTEGER DEFAULT 0,
        recurring_cadence TEXT,
        is_anomaly INTEGER DEFAULT 0,
        anomaly_reason TEXT,
        is_tax_relevant INTEGER DEFAULT 0,
        tax_category TEXT,
        tax_reason TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS session_insights (
        session_id TEXT PRIMARY KEY,
        health_breakdown_json TEXT,
        subscriptions_json TEXT,
        anomalies_json TEXT,
        tax_summary_json TEXT,
        spending_trends_json TEXT,
        top_categories_json TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
    );
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_txn_session ON transactions (session_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_txn_date ON transactions (date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_txn_category ON transactions (category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_txn_type ON transactions (type);")
    
    conn.commit()
    conn.close()

def save_session(session_data: Dict[str, Any]):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO sessions 
        (id, filename, file_type, upload_time, date_start, date_end, is_demo, total_income, total_expenses, net_savings, health_score, currency)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_data["id"],
        session_data["filename"],
        session_data["file_type"],
        session_data["upload_time"],
        session_data.get("date_start"),
        session_data.get("date_end"),
        1 if session_data.get("is_demo") else 0,
        session_data.get("total_income", 0.0),
        session_data.get("total_expenses", 0.0),
        session_data.get("net_savings", 0.0),
        session_data.get("health_score", 0),
        session_data.get("currency", "INR")
    ))
    conn.commit()
    conn.close()

def save_transactions(session_id: str, transactions: List[Dict[str, Any]]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Remove existing transactions for this session if any
    cursor.execute("DELETE FROM transactions WHERE session_id = ?", (session_id,))
    
    cursor.executemany("""
        INSERT INTO transactions 
        (id, session_id, date, raw_description, merchant, amount, type, balance, category, confidence, category_reason, is_recurring, recurring_cadence, is_anomaly, anomaly_reason, is_tax_relevant, tax_category, tax_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            t["id"],
            session_id,
            t["date"],
            t["raw_description"],
            t["merchant"],
            t["amount"],
            t["type"],
            t.get("balance"),
            t["category"],
            t.get("confidence", 0.8),
            t.get("category_reason"),
            1 if t.get("is_recurring") else 0,
            t.get("recurring_cadence"),
            1 if t.get("is_anomaly") else 0,
            t.get("anomaly_reason"),
            1 if t.get("is_tax_relevant") else 0,
            t.get("tax_category"),
            t.get("tax_reason")
        )
        for t in transactions
    ])
    conn.commit()
    conn.close()

def save_insights(session_id: str, insights: Dict[str, Any]):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO session_insights
        (session_id, health_breakdown_json, subscriptions_json, anomalies_json, tax_summary_json, spending_trends_json, top_categories_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        json.dumps(insights.get("health_breakdown", {})),
        json.dumps(insights.get("subscriptions", [])),
        json.dumps(insights.get("anomalies", [])),
        json.dumps(insights.get("tax_summary", {})),
        json.dumps(insights.get("spending_trends", [])),
        json.dumps(insights.get("top_categories", []))
    ))
    conn.commit()
    conn.close()

def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_transactions(
    session_id: str, 
    search: Optional[str] = None, 
    category: Optional[str] = None, 
    txn_type: Optional[str] = None,
    sort_by: str = "date",
    sort_order: str = "desc"
) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM transactions WHERE session_id = ?"
    params = [session_id]
    
    if search:
        query += " AND (merchant LIKE ? OR raw_description LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term])
        
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
        
    if txn_type and txn_type != "All":
        query += " AND type = ?"
        params.append(txn_type.lower())
        
    valid_sort_cols = {"date": "date", "amount": "amount", "merchant": "merchant", "category": "category"}
    order_col = valid_sort_cols.get(sort_by, "date")
    order_dir = "ASC" if sort_order.lower() == "asc" else "DESC"
    
    query += f" ORDER BY {order_col} {order_dir}"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_insights(session_id: str) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM session_insights WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return {}
    return {
        "health_breakdown": json.loads(row["health_breakdown_json"] or "{}"),
        "subscriptions": json.loads(row["subscriptions_json"] or "[]"),
        "anomalies": json.loads(row["anomalies_json"] or "[]"),
        "tax_summary": json.loads(row["tax_summary_json"] or "{}"),
        "spending_trends": json.loads(row["spending_trends_json"] or "[]"),
        "top_categories": json.loads(row["top_categories_json"] or "[]")
    }

def delete_session(session_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM session_insights WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM transactions WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
