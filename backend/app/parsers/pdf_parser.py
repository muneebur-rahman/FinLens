import io
import re
from typing import List, Dict, Any, Optional
import pdfplumber
from datetime import datetime
from app.parsers.csv_parser import clean_amount_str, parse_date_str

DATE_PATTERN = re.compile(
    r"^(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s+[A-Za-z]{3}\s+\d{2,4}|\d{4}[-/]\d{2}[-/]\d{2})"
)

def parse_pdf_statement(file_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Extracts transactions across all pages of a PDF bank statement.
    Attempts table extraction first; falls back to text line matching if needed.
    """
    transactions = []
    
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        if not pdf.pages:
            raise ValueError("The uploaded PDF has no pages.")
            
        # Strategy 1: Table Extraction across pages
        for page_idx, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue
                    
                # Identify column headers in table
                header_idx = -1
                date_col = -1
                desc_col = -1
                debit_col = -1
                credit_col = -1
                balance_col = -1
                
                for r_idx, row in enumerate(table[:5]):
                    row_strs = [str(cell).lower().strip() if cell else "" for cell in row]
                    for c_idx, cell in enumerate(row_strs):
                        if any(k in cell for k in ["date", "txn date", "value date"]):
                            date_col = c_idx
                        elif any(k in cell for k in ["narration", "particulars", "description", "details", "remarks"]):
                            desc_col = c_idx
                        elif any(k in cell for k in ["debit", "withdrawal", "dr"]):
                            debit_col = c_idx
                        elif any(k in cell for k in ["credit", "deposit", "cr"]):
                            credit_col = c_idx
                        elif any(k in cell for k in ["balance", "closing", "net bal"]):
                            balance_col = c_idx
                            
                    if date_col != -1 and (debit_col != -1 or credit_col != -1):
                        header_idx = r_idx
                        break
                        
                if header_idx != -1 and desc_col != -1:
                    # Process subsequent rows
                    for row in table[header_idx + 1:]:
                        if not row or len(row) <= max(date_col, desc_col):
                            continue
                        raw_date = row[date_col] if date_col < len(row) else None
                        norm_date = parse_date_str(raw_date)
                        if not norm_date:
                            continue
                            
                        desc = str(row[desc_col] if desc_col < len(row) and row[desc_col] else "").strip()
                        if not desc:
                            continue
                            
                        debit_val = clean_amount_str(row[debit_col]) if (debit_col != -1 and debit_col < len(row)) else None
                        credit_val = clean_amount_str(row[credit_col]) if (credit_col != -1 and credit_col < len(row)) else None
                        bal_val = clean_amount_str(row[balance_col]) if (balance_col != -1 and balance_col < len(row)) else None
                        
                        amt = 0.0
                        txn_type = "debit"
                        if debit_val is not None and abs(debit_val) > 0:
                            amt = abs(debit_val)
                            txn_type = "debit"
                        elif credit_val is not None and abs(credit_val) > 0:
                            amt = abs(credit_val)
                            txn_type = "credit"
                        else:
                            continue
                            
                        transactions.append({
                            "raw_date": norm_date,
                            "raw_description": desc,
                            "amount": round(amt, 2),
                            "type": txn_type,
                            "balance": round(bal_val, 2) if bal_val is not None else None
                        })
                        
        # Strategy 2: If table extraction found fewer than 2 transactions, fall back to line regex
        if len(transactions) < 2:
            transactions = []
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                for line in text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                        
                    date_match = DATE_PATTERN.match(line)
                    if date_match:
                        raw_date_str = date_match.group(1)
                        norm_date = parse_date_str(raw_date_str)
                        if not norm_date:
                            continue
                            
                        remainder = line[date_match.end():].strip()
                        # Look for numbers at the end (debit/credit/balance)
                        # e.g. "UPI-SWIGGY-1234 450.00 52100.00"
                        tokens = remainder.split()
                        if len(tokens) >= 2:
                            # Try parsing last tokens as numbers
                            amounts = []
                            desc_tokens = []
                            for token in tokens:
                                cleaned = clean_amount_str(token)
                                if cleaned is not None and re.match(r"^\(?[\d,]+(?:\.\d{1,2})?\)?(?:dr|cr)?$", token, re.IGNORECASE):
                                    amounts.append(cleaned)
                                else:
                                    desc_tokens.append(token)
                                    
                            if amounts:
                                desc = " ".join(desc_tokens)
                                if "cr" in remainder.lower() or "deposit" in remainder.lower():
                                    t_type = "credit"
                                    amt = abs(amounts[0])
                                else:
                                    t_type = "debit"
                                    amt = abs(amounts[0])
                                    
                                bal = amounts[1] if len(amounts) > 1 else None
                                transactions.append({
                                    "raw_date": norm_date,
                                    "raw_description": desc if desc else "Bank Transaction",
                                    "amount": round(amt, 2),
                                    "type": t_type,
                                    "balance": round(bal, 2) if bal is not None else None
                                })

    if not transactions:
        raise ValueError("We couldn't read this statement. Please try another PDF or CSV.")
        
    return transactions
