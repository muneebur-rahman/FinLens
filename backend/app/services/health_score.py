from typing import List, Dict, Any

def calculate_health_score(
    total_income: float,
    total_expenses: float,
    recurring_monthly_spend: float,
    category_totals: Dict[str, float],
    anomalies: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes a transparent, 100% data-derived Financial Health Score (0-100)
    with exact explanations of positive drivers and areas for improvement.
    """
    whats_helping = []
    whats_improving = []

    # Handle edge case of 0 income statement
    if total_income <= 0:
        savings_rate_pct = 0.0
        expense_ratio_pct = 999.0
        recurring_burden_pct = 0.0
        score = max(20, min(50, int(60 - (total_expenses / 2000))))
        whats_improving.append("No recorded income deposits in this statement period to offset expenses.")
        if total_expenses > 0:
            whats_improving.append(f"Statement recorded ₹{total_expenses:,.2f} in net outflows with 0 income inflows.")
        return {
            "score": score,
            "rating": "Needs Attention",
            "savings_rate_pct": 0.0,
            "expense_ratio_pct": 100.0,
            "recurring_burden_pct": 0.0,
            "discretionary_pct": 0.0,
            "whats_helping": ["Statement transactions processed successfully."],
            "whats_improving": whats_improving
        }

    # 1. Savings Rate Pillar (30 pts)
    net_savings = total_income - total_expenses
    savings_rate = net_savings / total_income
    savings_rate_pct = round(savings_rate * 100, 1)

    if savings_rate >= 0.35:
        p1 = 30
        whats_helping.append(f"High savings rate of {savings_rate_pct}% (retaining ₹{net_savings:,.2f} of ₹{total_income:,.2f} income).")
    elif savings_rate >= 0.20:
        p1 = 24
        whats_helping.append(f"Healthy savings buffer of {savings_rate_pct}%, meeting standard financial prudence guidelines.")
    elif savings_rate >= 0.10:
        p1 = 18
        whats_helping.append(f"Positive savings cushion of {savings_rate_pct}%.")
        whats_improving.append("Consider targeting a 20%+ savings rate by trimming flexible discretionary categories.")
    elif savings_rate >= 0.0:
        p1 = 10
        whats_improving.append(f"Slim savings rate of {savings_rate_pct}% leaves limited buffer for unexpected expenses.")
    else:
        p1 = 4
        whats_improving.append(f"Expenses exceeded income by ₹{abs(net_savings):,.2f} ({savings_rate_pct}% deficit).")

    # 2. Expense-to-Income Ratio Pillar (25 pts)
    expense_ratio = total_expenses / total_income
    expense_ratio_pct = round(expense_ratio * 100, 1)

    if expense_ratio <= 0.60:
        p2 = 25
        whats_helping.append(f"Controlled overall spending at {expense_ratio_pct}% of total income.")
    elif expense_ratio <= 0.80:
        p2 = 20
        whats_helping.append(f"Moderate outflow ratio of {expense_ratio_pct}% within standard budgeting targets.")
    elif expense_ratio <= 0.95:
        p2 = 12
        whats_improving.append(f"High expense ratio of {expense_ratio_pct}%; more than 85% of monthly inflows are consumed.")
    else:
        p2 = 5
        whats_improving.append(f"Expenses consume {expense_ratio_pct}% of income.")

    # 3. Discretionary Spending Ratio Pillar (15 pts)
    discretionary_categories = ["Food & Dining", "Shopping", "Entertainment", "Travel"]
    discretionary_spend = sum(category_totals.get(c, 0.0) for c in discretionary_categories)
    discretionary_ratio = (discretionary_spend / total_expenses) if total_expenses > 0 else 0
    discretionary_pct = round(discretionary_ratio * 100, 1)

    if discretionary_ratio <= 0.30:
        p3 = 15
        whats_helping.append(f"Well-disciplined discretionary spend ({discretionary_pct}% across dining, shopping & entertainment).")
    elif discretionary_ratio <= 0.50:
        p3 = 10
    else:
        p3 = 5
        # Identify top discretionary culprit
        top_disc = sorted([(c, category_totals.get(c, 0.0)) for c in discretionary_categories], key=lambda x: x[1], reverse=True)
        if top_disc and top_disc[0][1] > 0:
            culprit, c_amt = top_disc[0]
            whats_improving.append(f"High discretionary ratio ({discretionary_pct}% of expenses), led by {culprit} at ₹{c_amt:,.2f}.")

    # 4. Recurring Subscription Burden (15 pts)
    recurring_burden = (recurring_monthly_spend / total_income) if total_income > 0 else 0
    recurring_burden_pct = round(recurring_burden * 100, 1)

    if recurring_burden <= 0.05:
        p4 = 15
        if recurring_monthly_spend > 0:
            whats_helping.append(f"Minimal subscription leak: recurring commitments are only {recurring_burden_pct}% of income (₹{recurring_monthly_spend:,.2f}/mo).")
        else:
            whats_helping.append("Zero recurring subscription overhead detected.")
    elif recurring_burden <= 0.12:
        p4 = 11
        whats_helping.append(f"Manageable recurring subscription volume at {recurring_burden_pct}% of income.")
    else:
        p4 = 5
        whats_improving.append(f"Recurring monthly payments consume {recurring_burden_pct}% of your income (₹{recurring_monthly_spend:,.2f}/mo).")

    # 5. Stability & Anomaly Health (15 pts)
    anomaly_count = len(anomalies)
    if anomaly_count == 0:
        p5 = 15
        whats_helping.append("Clean spending consistency: no abnormal or irregular transaction spikes detected.")
    elif anomaly_count == 1:
        p5 = 11
        whats_improving.append(f"1 unusual outlier transaction flagged: {anomalies[0]['reason']}")
    else:
        p5 = 6
        whats_improving.append(f"{anomaly_count} spending outliers flagged that deviate significantly from your baseline.")

    raw_score = p1 + p2 + p3 + p4 + p5
    score = max(10, min(99, raw_score))

    if score >= 82:
        rating = "Excellent"
    elif score >= 68:
        rating = "Good"
    elif score >= 50:
        rating = "Fair"
    else:
        rating = "Needs Attention"

    return {
        "score": score,
        "rating": rating,
        "savings_rate_pct": savings_rate_pct,
        "expense_ratio_pct": expense_ratio_pct,
        "recurring_burden_pct": recurring_burden_pct,
        "discretionary_pct": discretionary_pct,
        "whats_helping": whats_helping[:3],  # Top 3 clear drivers
        "whats_improving": whats_improving[:3]  # Top 3 actionable areas
    }
