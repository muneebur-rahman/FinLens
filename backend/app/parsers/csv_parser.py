import io
import re
import csv
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd

DATE_COL_CANDIDATES = [
    "date", "txn date", "transaction date", "value date", "trans date", 
    "posting date", "txn_date", "booking date"
]

DESC_COL_CANDIDATES = [
    "narration", "description", "particulars", "transaction remarks", 
    "details", "remarks", "memo", "payee", "transaction details"
]

DEBIT_COL_CANDIDATES = [
    "debit", "withdrawal", "withdrawal amt", "withdrawal amount", 
    "dr", "dr amount", "paid out", "debit amount", "debit (inr)"
]

CREDIT_COL_CANDIDATES = [
    "credit", "deposit", "deposit amt", "deposit amount", 
    "cr", "cr amount", "paid in", "credit amount", "credit (inr)"
]

AMOUNT_COL_CANDIDATES = [
    "amount", "txn amount", "transaction amount", "net amount"
]

TYPE_COL_CANDIDATES = [
    "type", "cr/dr", "txn type", "transaction type", "dr/cr"
]

BALANCE_COL_CANDIDATES = [
    "balance", "closing balance", "available balance", "net balance", "bal"
]

def clean_amount_str(val: Any) -> Optional[float]:
    if val is None or pd.isna(val):
        return None
    s = str(val).strip()
    if not s or s.lower() in ["nan", "none", "-", "null", "nil"]:
        return None
    
    # Check if negative formatted as (1,234.56)
    is_negative = False
    if s.startswith("(") and s.endswith(")"):
        is_negative = True
        s = s[1:-1]
    elif s.endswith(" Dr") or s.endswith(" DR") or s.startswith("-"):
        is_negative = True
        s = re.sub(r"(?i)\s*dr$", "", s).lstrip("-")
    elif s.endswith(" Cr") or s.endswith(" CR") or s.startswith("+"):
        s = re.sub(r"(?i)\s*cr$", "", s).lstrip("+")
        
    # Remove currency symbols and commas
    s = re.sub(r"[^\d.]", "", s)
    try:
        amt = float(s)
        return -amt if is_negative else amt
    except (ValueError, TypeError):
        return None

def parse_date_str(val: Any) -> Optional[str]:
    if not val or pd.isna(val):
        return None
    s = str(val).strip().split()[0]  # Strip time component if present
    
    formats = [
        "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%y", "%d-%m-%y",
        "%d-%b-%Y", "%d-%b-%y", "%d %b %Y", "%d %b %y",
        "%m/%d/%Y", "%m-%d-%Y", "%Y/%m/%d"
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(s, fmt)
            # Ensure reasonable year range (2000-2099)
            if 2000 <= dt.year <= 2099:
                return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

def find_header_row(lines: List[str]) -> Tuple[int, List[str]]:
    """
    Examines lines to identify where the real column header row begins.
    Scores rows by how many banking column names they contain.
    """
    best_idx = 0
    best_score = -1
    best_headers = []
    
    for idx, line in enumerate(lines[:30]):  # check up to first 30 lines
        # Parse CSV line
        try:
            reader = csv.reader(io.StringIO(line))
            cols = [c.strip().lower() for c in next(reader, [])]
        except Exception:
            continue
            
        if not cols or len(cols) < 3:
            continue
            
        score = 0
        for c in cols:
            for cand in DATE_COL_CANDIDATES + DESC_COL_CANDIDATES + DEBIT_COL_CANDIDATES + CREDIT_COL_CANDIDATES + AMOUNT_COL_CANDIDATES:
                if cand in c or c in cand:
                    score += 2
                    break
        if score > best_score and score >= 4:
            best_score = score
            best_idx = idx
            best_headers = cols
            
    return best_idx, best_headers

def parse_csv_statement(content: bytes) -> List[Dict[str, Any]]:
    """
    Parses arbitrary CSV bank statements into normalized raw transactions.
    """
    text = ""
    for enc in ["utf-8", "latin-1", "cp1252"]:
        try:
            text = content.decode(enc)
            break
        except UnicodeDecodeError:
            continue
            
    if not text:
        raise ValueError("Could not decode CSV content with standard encodings.")
        
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("The uploaded CSV statement appears to be empty.")
        
    header_idx, headers = find_header_row(lines)
    
    # Read using pandas from header_idx
    csv_stream = io.StringIO("\n".join(lines[header_idx:]))
    df = pd.read_csv(csv_stream, dtype=str)
    
    # Normalize column names in df
    df.columns = [str(c).strip() for c in df.columns]
    col_map = {c.lower(): c for c in df.columns}
    
    # Identify key columns
    date_col = None
    for cand in DATE_COL_CANDIDATES:
        for c_lower, c_orig in col_map.items():
            if cand == c_lower or cand in c_lower:
                date_col = c_orig
                break
        if date_col:
            break
            
    desc_col = None
    for cand in DESC_COL_CANDIDATES:
        for c_lower, c_orig in col_map.items():
            if cand == c_lower or cand in c_lower:
                desc_col = c_orig
                break
        if desc_col:
            break
            
    debit_col = None
    credit_col = None
    amount_col = None
    type_col = None
    balance_col = None
    
    for cand in DEBIT_COL_CANDIDATES:
        for c_lower, c_orig in col_map.items():
            if cand == c_lower or (cand in c_lower and "credit" not in c_lower):
                debit_col = c_orig
                break
        if debit_col:
            break
            
    for cand in CREDIT_COL_CANDIDATES:
        for c_lower, c_orig in col_map.items():
            if cand == c_lower or (cand in c_lower and "debit" not in c_lower):
                credit_col = c_orig
                break
        if credit_col:
            break
            
    for cand in AMOUNT_COL_CANDIDATES:
        for c_lower, c_orig in col_map.items():
            if cand == c_lower:
                amount_col = c_orig
                break
        if amount_col:
            break
            
    for cand in TYPE_COL_CANDIDATES:
        for c_lower, c_orig in col_map.items():
            if cand == c_lower:
                type_col = c_orig
                break
        if type_col:
            break
            
    for cand in BALANCE_COL_CANDIDATES:
        for c_lower, c_orig in col_map.items():
            if cand == c_lower or cand in c_lower:
                balance_col = c_orig
                break
        if balance_col:
            break
            
    if not date_col or not desc_col:
        raise ValueError("Could not identify mandatory Date and Description/Narration columns in this CSV.")
        
    transactions = []
    
    for idx, row in df.iterrows():
        raw_date = row.get(date_col)
        norm_date = parse_date_str(raw_date)
        if not norm_date:
            continue  # Skip header/total/blank rows
            
        raw_desc = str(row.get(desc_col, "")).strip()
        if not raw_desc or raw_desc.lower() in ["total", "closing balance", "opening balance"]:
            continue
            
        # Determine amount and type
        amount = 0.0
        txn_type = "debit"
        
        if debit_col and credit_col:
            debit_val = clean_amount_str(row.get(debit_col))
            credit_val = clean_amount_str(row.get(credit_col))
            
            if debit_val is not None and abs(debit_val) > 0:
                amount = abs(debit_val)
                txn_type = "debit"
            elif credit_val is not None and abs(credit_val) > 0:
                amount = abs(credit_val)
                txn_type = "credit"
            else:
                continue
        elif amount_col:
            amt_val = clean_amount_str(row.get(amount_col))
            if amt_val is None or amt_val == 0:
                continue
                
            if type_col:
                t_val = str(row.get(type_col, "")).strip().upper()
                if "CR" in t_val or "CREDIT" in t_val or "DEP" in t_val:
                    txn_type = "credit"
                    amount = abs(amt_val)
                else:
                    txn_type = "debit"
                    amount = abs(amt_val)
            else:
                if amt_val < 0:
                    txn_type = "debit"
                    amount = abs(amt_val)
                else:
                    txn_type = "credit"
                    amount = abs(amt_val)
        else:
            continue
            
        balance = None
        if balance_col:
            balance = clean_amount_str(row.get(balance_col))
            
        transactions.append({
            "raw_date": norm_date,
            "raw_description": raw_desc,
            "amount": round(amount, 2),
            "type": txn_type,
            "balance": round(balance, 2) if balance is not None else None
        })
        
    if not transactions:
        raise ValueError("We couldn't identify transactions in this CSV file.")
        
    return transactions
