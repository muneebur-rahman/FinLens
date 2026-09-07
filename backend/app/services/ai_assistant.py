import re
from typing import List, Dict, Any, Optional

def query_ai_assistant(
    message: str,
    transactions: List[Dict[str, Any]],
    session_data: Dict[str, Any],
    insights: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Answers user queries strictly grounded in the uploaded statement dataset.
    Never fabricates facts, numbers, or external data.
    """
    msg = message.strip().lower()
    total_income = session_data.get("total_income", 0.0)
    total_expenses = session_data.get("total_expenses", 0.0)
    net_savings = session_data.get("net_savings", 0.0)
    health_score = session_data.get("health_score", 0)
    subscriptions = insights.get("subscriptions", [])
    anomalies = insights.get("anomalies", [])
    tax_summary = insights.get("tax_summary", {})
    
    debits = [t for t in transactions if t["type"] == "debit"]
    credits = [t for t in transactions if t["type"] == "credit"]

    # 1. Food / Dining / Groceries spending
    if any(k in msg for k in ["food", "dining", "eat", "restaurant", "groceries", "swiggy", "zomato"]):
        food_txns = [t for t in debits if t["category"] in ["Food & Dining", "Groceries"]]
        food_total = sum(t["amount"] for t in food_txns)
        food_only = sum(t["amount"] for t in debits if t["category"] == "Food & Dining")
        groc_only = sum(t["amount"] for t in debits if t["category"] == "Groceries")
        
        # If user asked specifically about a merchant like Swiggy
        if "swiggy" in msg:
            swiggy_txns = [t for t in debits if "swiggy" in t["merchant"].lower()]
            swiggy_total = sum(t["amount"] for t in swiggy_txns)
            return {
                "answer": f"Based on your statement, you spent **₹{swiggy_total:,.2f}** across {len(swiggy_txns)} transaction(s) on Swiggy.",
                "data_points": {"swiggy_total": swiggy_total, "count": len(swiggy_txns)}
            }
        elif "zomato" in msg:
            zomato_txns = [t for t in debits if "zomato" in t["merchant"].lower()]
            zomato_total = sum(t["amount"] for t in zomato_txns)
            return {
                "answer": f"Based on your statement, you spent **₹{zomato_total:,.2f}** across {len(zomato_txns)} transaction(s) on Zomato.",
                "data_points": {"zomato_total": zomato_total, "count": len(zomato_txns)}
            }

        return {
            "answer": (
                f"You spent a total of **₹{food_total:,.2f}** on food & groceries in this statement period.\n\n"
                f"• **Food & Dining**: ₹{food_only:,.2f}\n"
                f"• **Groceries & Supplies**: ₹{groc_only:,.2f}\n\n"
                f"This represents **{round((food_total / total_expenses * 100) if total_expenses > 0 else 0, 1)}%** of your total expenses."
            ),
            "data_points": {"food_total": food_total, "dining": food_only, "groceries": groc_only}
        }

    # 2. Biggest / Largest expense
    if any(k in msg for k in ["biggest", "largest", "highest", "most expensive"]):
        if not debits:
            return {"answer": "There are no debit expenses recorded in this statement."}
        sorted_debits = sorted(debits, key=lambda x: x["amount"], reverse=True)
        top = sorted_debits[0]
        top_3 = sorted_debits[:3]
        
        top_list_str = "\n".join([
            f"• **{t['merchant']}** on {t['date']}: ₹{t['amount']:,.2f} ({t['category']})"
            for t in top_3
        ])
        return {
            "answer": (
                f"Your biggest single expense was **₹{top['amount']:,.2f}** to **{top['merchant']}** "
                f"on {top['date']} (categorized under *{top['category']}*).\n\n"
                f"**Top 3 Expenses:**\n{top_list_str}"
            ),
            "data_points": {"top_merchant": top["merchant"], "top_amount": top["amount"], "date": top["date"]}
        }

    # 3. Savings / How much saved
    if any(k in msg for k in ["how much did i save", "saved", "savings", "net savings"]):
        rate = round((net_savings / total_income * 100), 1) if total_income > 0 else 0
        if net_savings >= 0:
            return {
                "answer": (
                    f"According to your uploaded statement:\n\n"
                    f"• **Total Inflows (Income)**: ₹{total_income:,.2f}\n"
                    f"• **Total Outflows (Expenses)**: ₹{total_expenses:,.2f}\n"
                    f"• **Net Savings**: **₹{net_savings:,.2f}**\n\n"
                    f"Your calculated savings rate is **{rate}%** of your total income."
                ),
                "data_points": {"income": total_income, "expenses": total_expenses, "net_savings": net_savings, "savings_rate": rate}
            }
        else:
            return {
                "answer": (
                    f"In this statement period, your total expenses exceeded your income:\n\n"
                    f"• **Income**: ₹{total_income:,.2f}\n"
                    f"• **Expenses**: ₹{total_expenses:,.2f}\n"
                    f"• **Deficit**: **-₹{abs(net_savings):,.2f}**\n\n"
                    f"You spent {round((total_expenses / total_income * 100), 1) if total_income > 0 else 0}% of your incoming funds."
                ),
                "data_points": {"income": total_income, "expenses": total_expenses, "net_savings": net_savings}
            }

    # 4. Total Income / Inflows
    if any(k in msg for k in ["total income", "how much did i earn", "salary", "inflow", "inflows"]):
        salary_txns = [t for t in credits if t["category"] == "Salary"]
        sal_total = sum(t["amount"] for t in salary_txns)
        return {
            "answer": (
                f"Your total incoming deposits across this statement were **₹{total_income:,.2f}** across {len(credits)} credit transactions.\n"
                + (f"• Direct salary credits: ₹{sal_total:,.2f}\n" if sal_total > 0 else "")
                + f"• All other inflows: ₹{(total_income - sal_total):,.2f}"
            ),
            "data_points": {"total_income": total_income, "salary": sal_total}
        }

    # 5. Total Expenses / Outflows
    if any(k in msg for k in ["total expense", "total spend", "how much did i spend", "outflows"]):
        return {
            "answer": (
                f"Your total expenses across this statement period were **₹{total_expenses:,.2f}** across {len(debits)} debit transactions."
            ),
            "data_points": {"total_expenses": total_expenses, "count": len(debits)}
        }

    # 6. Subscriptions / Recurring payments
    if any(k in msg for k in ["subscription", "subscriptions", "recurring", "monthly payment", "monthly leak"]):
        if not subscriptions:
            return {
                "answer": "No recurring subscriptions were detected in this uploaded statement. All transactions were one-time or variable expenditures.",
                "data_points": {"subscriptions_count": 0}
            }
        sub_list_str = "\n".join([
            f"• **{s['merchant']}**: ₹{s['average_amount']:,.2f}/{s['cadence']} ({s['occurrences']} occurrence(s))"
            for s in subscriptions
        ])
        monthly_total = sum(s["average_amount"] for s in subscriptions)
        return {
            "answer": (
                f"I detected **{len(subscriptions)} recurring subscription(s)** in your statement, with an estimated recurring monthly spend of **₹{monthly_total:,.2f}**:\n\n"
                f"{sub_list_str}"
            ),
            "data_points": {"count": len(subscriptions), "monthly_total": monthly_total, "subscriptions": subscriptions}
        }

    # 7. Anomalies / Flagged transactions
    if any(k in msg for k in ["flagged", "anomaly", "anomalies", "unusual", "suspicious", "why was this flagged"]):
        if not anomalies:
            return {
                "answer": "No unusual spending patterns or anomalies were detected in this statement. Your spending remained within expected bounds.",
                "data_points": {"anomalies_count": 0}
            }
        anom_str = "\n".join([
            f"• **₹{a['amount']:,.2f}** to **{a['merchant']}** on {a['date']} — *{a['reason']}*"
            for a in anomalies
        ])
        return {
            "answer": (
                f"FinLens flagged **{len(anomalies)} unusual transaction(s)** in this statement:\n\n"
                f"{anom_str}\n\n"
                f"*Note: These are behavioral outliers relative to your statement baseline, not automatic fraud indicators.*"
            ),
            "data_points": {"count": len(anomalies), "anomalies": anomalies}
        }

    # 8. Tax deductions / Rent / 80C
    if any(k in msg for k in ["tax", "80c", "80d", "80g", "deduction", "hra", "rent tax"]):
        items = tax_summary.get("items", [])
        if not items:
            return {
                "answer": "No tax-relevant payments (such as rent receipts, Section 80C investments, health insurance, or charity donations) were identified in this statement.",
                "data_points": {"tax_total": 0.0}
            }
        sec_str = "\n".join([
            f"• **Section {sec}**: ₹{amt:,.2f}"
            for sec, amt in tax_summary.get("by_section", {}).items()
        ])
        return {
            "answer": (
                f"I identified **₹{tax_summary.get('total_tax_relevant', 0):,.2f}** in potentially tax-relevant transactions:\n\n"
                f"{sec_str}\n\n"
                f"*Reminder: FinLens is an organizational tool. Please verify deduction rules with a qualified tax accountant.*"
            ),
            "data_points": tax_summary
        }

    # Strictly handle queries about information not in statement (Check first)
    out_of_scope_keywords = ["credit score", "cibil", "pan card", "aadhaar", "stock price", "crypto price", "forecast", "tomorrow", "weather"]
    if any(k in msg for k in out_of_scope_keywords):
        return {
            "answer": (
                "I cannot determine that from the uploaded statement. "
                "Bank statements only contain recorded monetary debits, credits, dates, and transaction narrations."
            )
        }

    # 9. Financial Health Score
    if any(k in msg for k in ["health score", "financial health", "my score", "rate my finances", "health rating"]):
        breakdown = insights.get("health_breakdown", {})
        helping = "\n".join([f"✓ {h}" for h in breakdown.get("whats_helping", [])])
        improving = "\n".join([f"⚠ {i}" for h in breakdown.get("whats_improving", []) for i in [h]])
        return {
            "answer": (
                f"Your calculated Financial Health Score is **{health_score} / 100** ({breakdown.get('rating', 'Good')}).\n\n"
                f"**What is helping:**\n{helping}\n\n"
                + (f"**What could improve:**\n{improving}\n\n" if improving else "")
                + f"This score was computed directly from your savings rate, recurring expense burden, and spending stability."
            ),
            "data_points": {"score": health_score, "breakdown": breakdown}
        }

    # 12. General fallback grounded in statement summary
    return {
        "answer": (
            f"Based on your uploaded statement ({session_data.get('filename', 'Current Statement')}):\n\n"
            f"• **Date Period**: {session_data.get('date_start', 'N/A')} to {session_data.get('date_end', 'N/A')}\n"
            f"• **Transactions Analyzed**: {len(transactions)} ({len(debits)} debits, {len(credits)} credits)\n"
            f"• **Income**: ₹{total_income:,.2f} | **Expenses**: ₹{total_expenses:,.2f}\n"
            f"• **Net Savings**: ₹{net_savings:,.2f}\n\n"
            f"You can ask me specific questions like *'How much did I spend on food?'*, *'What was my biggest expense?'*, *'Do I have recurring subscriptions?'*, or *'Why was a transaction flagged?'*."
        )
    }
