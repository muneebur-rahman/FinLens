from datetime import datetime
from typing import List, Dict, Any, Tuple
from collections import defaultdict

KNOWN_SUBSCRIPTION_MERCHANTS = {
    "netflix", "spotify", "prime video", "disney+ hotstar", "youtube premium", 
    "apple.com/bill", "google play", "audible", "icloud", "chatgpt", 
    "adobe", "microsoft 365", "github", "cult.fit", "gym"
}

def detect_subscriptions(transactions: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], float]:
    """
    Analyzes debit transactions to identify recurring subscription patterns.
    Returns (list_of_detected_subscriptions, estimated_recurring_monthly_spend).
    Strictly data-driven: Never invents subscriptions if none exist.
    """
    # Filter debit transactions
    debits = [t for t in transactions if t["type"] == "debit" and t["amount"] > 0]
    if not debits:
        return [], 0.0

    # Group by merchant key
    merchant_groups = defaultdict(list)
    for t in debits:
        m_clean = t["merchant"].strip()
        merchant_groups[m_clean].append(t)

    detected_subscriptions = []
    total_monthly_spend = 0.0

    for merchant, txns in merchant_groups.items():
        m_lower = merchant.lower()
        
        # Sort chronologically
        sorted_txns = sorted(txns, key=lambda x: x["date"])
        count = len(sorted_txns)
        
        is_known_sub = any(k in m_lower for k in KNOWN_SUBSCRIPTION_MERCHANTS)
        
        # Case 1: Multi-occurrence transactions (>= 2)
        if count >= 2:
            amounts = [t["amount"] for t in sorted_txns]
            avg_amt = sum(amounts) / count
            max_amt = max(amounts)
            min_amt = min(amounts)
            
            # Check amount variance (allow small variance of 5-10% for utility/currency fluctuations)
            variance_ratio = (max_amt - min_amt) / avg_amt if avg_amt > 0 else 0
            
            # Check day intervals between consecutive transactions
            dates = [datetime.strptime(t["date"], "%Y-%m-%d") for t in sorted_txns]
            intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates) - 1)]
            avg_interval = sum(intervals) / len(intervals) if intervals else 0

            # Monthly recurrence: intervals ~ 25 to 35 days
            if 25 <= avg_interval <= 35 and variance_ratio <= 0.15:
                detected_subscriptions.append({
                    "merchant": merchant,
                    "average_amount": round(avg_amt, 2),
                    "cadence": "monthly",
                    "occurrences": count,
                    "last_date": sorted_txns[-1]["date"],
                    "total_spent": round(sum(amounts), 2),
                    "category": sorted_txns[0].get("category", "Entertainment"),
                    "detection_reason": f"Detected recurring monthly cadence (avg {int(avg_interval)} days apart, ₹{round(avg_amt, 2)})."
                })
                total_monthly_spend += avg_amt
                continue
                
            # Weekly recurrence: intervals ~ 6 to 9 days
            elif 6 <= avg_interval <= 9 and variance_ratio <= 0.10:
                detected_subscriptions.append({
                    "merchant": merchant,
                    "average_amount": round(avg_amt, 2),
                    "cadence": "weekly",
                    "occurrences": count,
                    "last_date": sorted_txns[-1]["date"],
                    "total_spent": round(sum(amounts), 2),
                    "category": sorted_txns[0].get("category", "Services"),
                    "detection_reason": f"Detected recurring weekly payment (every ~7 days, ₹{round(avg_amt, 2)})."
                })
                total_monthly_spend += (avg_amt * 4.33)  # Normalize weekly to monthly
                continue
                
            # If known subscription provider with identical amounts even if statement spans single interval
            if is_known_sub and variance_ratio <= 0.05:
                detected_subscriptions.append({
                    "merchant": merchant,
                    "average_amount": round(avg_amt, 2),
                    "cadence": "monthly",
                    "occurrences": count,
                    "last_date": sorted_txns[-1]["date"],
                    "total_spent": round(sum(amounts), 2),
                    "category": sorted_txns[0].get("category", "Entertainment"),
                    "detection_reason": f"Confirmed recurring digital subscription service ({merchant}, ₹{round(avg_amt, 2)}/mo)."
                })
                total_monthly_spend += avg_amt
                continue

        # Case 2: Exactly 1 occurrence, but matches a prominent digital subscription provider
        elif count == 1 and is_known_sub:
            txn = sorted_txns[0]
            detected_subscriptions.append({
                "merchant": merchant,
                "average_amount": round(txn["amount"], 2),
                "cadence": "monthly",
                "occurrences": 1,
                "last_date": txn["date"],
                "total_spent": round(txn["amount"], 2),
                "category": txn.get("category", "Entertainment"),
                "detection_reason": f"Digital recurring subscription service ({merchant}, ₹{round(txn['amount'], 2)}/mo)."
            })
            total_monthly_spend += txn["amount"]

    # Mark transactions that belong to detected subscriptions
    sub_merchants = {s["merchant"] for s in detected_subscriptions}
    for t in transactions:
        if t["merchant"] in sub_merchants:
            t["is_recurring"] = True
            t["recurring_cadence"] = "monthly"

    return detected_subscriptions, round(total_monthly_spend, 2)
