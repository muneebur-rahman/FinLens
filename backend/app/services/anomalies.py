from typing import List, Dict, Any
from collections import defaultdict
import numpy as np

def detect_anomalies(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyzes transactions relative to the user's own baseline spending.
    Flags unusual outliers with clear, non-alarmist explainability.
    """
    debits = [t for t in transactions if t["type"] == "debit" and t["amount"] > 0]
    if len(debits) < 3:
        return []

    anomalies = []
    total_debit_volume = sum(t["amount"] for t in debits)
    all_amounts = [t["amount"] for t in debits]
    global_median = float(np.median(all_amounts))

    # 1. Group by category to establish category baselines
    cat_txns = defaultdict(list)
    for t in debits:
        cat_txns[t["category"]].append(t)

    # 2. Check each debit
    for t in debits:
        amount = t["amount"]
        category = t["category"]
        merchant = t["merchant"]
        
        # Don't flag regular large rent or known salary transfers as anomalous
        if category in ["Rent", "Investments"]:
            continue

        cat_amounts = [x["amount"] for x in cat_txns[category]]
        cat_median = float(np.median(cat_amounts))
        cat_count = len(cat_amounts)

        flagged = False
        reason = ""
        severity = "notice"

        # Rule A: Extreme proportion of total period spending (>35% of total debit volume in diverse statements)
        if len(debits) >= 6 and total_debit_volume > 0 and (amount / total_debit_volume) >= 0.35 and amount >= 15000 and category not in ["Groceries", "Utilities"]:
            flagged = True
            severity = "high"
            pct = round((amount / total_debit_volume) * 100, 1)
            reason = f"Single transaction represents {pct}% of your total statement spending (₹{amount:,.2f})."

        # Rule B: Category outlier (transaction is >= 3x the median for that category, with minimum threshold)
        elif cat_count >= 3 and amount >= (3.0 * cat_median) and amount > (global_median * 2.5) and amount >= 5000:
            flagged = True
            severity = "medium"
            reason = f"₹{amount:,.2f} is {round(amount / cat_median, 1)}x higher than your typical {category} spending (median ₹{cat_median:,.2f})."

        # Rule C: General high value spike compared to overall median
        elif len(debits) >= 6 and amount > (global_median * 4.0) and amount >= 20000:
            flagged = True
            severity = "medium"
            reason = f"Unusually high spend of ₹{amount:,.2f} relative to overall typical transactions (median ₹{global_median:,.2f})."

        if flagged:
            anomaly_data = {
                "transaction_id": t["id"],
                "date": t["date"],
                "merchant": merchant,
                "amount": amount,
                "category": category,
                "reason": reason,
                "severity": severity
            }
            anomalies.append(anomaly_data)
            t["is_anomaly"] = True
            t["anomaly_reason"] = reason

    # Rule D: Duplicate charges (same merchant, exact same amount on same date)
    date_merchant_map = defaultdict(list)
    for t in debits:
        key = (t["date"], t["merchant"].lower(), t["amount"])
        date_merchant_map[key].append(t)

    for (dt, merch, amt), duplicates in date_merchant_map.items():
        if len(duplicates) > 1 and amt > 100:
            for dup in duplicates[1:]:
                # If not already flagged
                if not dup.get("is_anomaly"):
                    dup["is_anomaly"] = True
                    dup["anomaly_reason"] = f"Potential duplicate charge: ₹{amt:,.2f} to {dup['merchant']} recorded multiple times on {dt}."
                    anomalies.append({
                        "transaction_id": dup["id"],
                        "date": dt,
                        "merchant": dup["merchant"],
                        "amount": amt,
                        "category": dup["category"],
                        "reason": dup["anomaly_reason"],
                        "severity": "notice"
                    })

    return anomalies
