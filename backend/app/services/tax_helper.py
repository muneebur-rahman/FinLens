import re
from typing import List, Dict, Any

TAX_DISCLAIMER = (
    "FinLens is an organizational intelligence tool, NOT an official tax filing service or certified tax advice. "
    "Tax deductions are subject to individual regime eligibility (Old vs. New Tax Regime) and official documentation. "
    "Please consult a certified chartered accountant or tax professional before claiming deductions."
)

TAX_PATTERNS = [
    # Section 80C
    (
        "80C",
        "Investments & Savings (80C)",
        r"\b(?:elss|ppf|provident fund|epf|life insurance|lic|nps tier 1|tuition fee|national savings certificate|tax saver|sukanya samriddhi)\b",
        "Eligible under Section 80C for tax exemption (up to ₹1.5 Lakh ceiling under Old Regime)."
    ),
    # Section 80D
    (
        "80D",
        "Health Insurance (80D)",
        r"\b(?:health insurance|mediclaim|star health|max bupa|care health|hdfc ergo health|niva bupa|medical checkup)\b",
        "Eligible under Section 80D for medical insurance premium deductions."
    ),
    # Section 80G
    (
        "80G",
        "Charitable Donations (80G)",
        r"\b(?:donation|relief fund|pm cares|akshaya patra|cry|helpage|unicef|ngo|charity|giveindia|prime minister national relief)\b",
        "Eligible under Section 80G for charitable contribution deductions (50% or 100% deduction with receipt)."
    ),
    # Section 80GG / HRA
    (
        "80GG/HRA",
        "House Rent Exemption (HRA / 80GG)",
        r"\b(?:rent|landlord|house rent|flat rent|nobroker rent|cred rent)\b",
        "Potentially eligible for House Rent Allowance (HRA) exemption or Section 80GG deduction with valid rent receipts."
    ),
    # Section 80E
    (
        "80E",
        "Higher Education Loan (80E)",
        r"\b(?:education loan|student loan|tuition|study loan)\b",
        "Eligible under Section 80E for interest deduction on higher education loans."
    ),
    # Business / Professional Deductions
    (
        "Business",
        "Business & Professional Expenses",
        r"\b(?:aws|google cloud|azure|github|digitalocean|adobe|office supply|broadband|domain|hosting)\b",
        "Potentially claimable as direct business operational expenses for freelancers and professionals."
    )
]

def analyze_tax_transactions(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Identifies tax-relevant debit transactions and aggregates totals by section.
    """
    debits = [t for t in transactions if t["type"] == "debit" and t["amount"] > 0]
    tax_items = []
    by_section = {}
    total_tax_relevant = 0.0

    for t in debits:
        full_text = f"{t['merchant']} {t['raw_description']}".lower()
        amount = t["amount"]

        for section_code, section_title, pattern, reason in TAX_PATTERNS:
            if re.search(pattern, full_text):
                # Don't duplicate if already matched higher priority
                item = {
                    "transaction_id": t["id"],
                    "date": t["date"],
                    "merchant": t["merchant"],
                    "amount": amount,
                    "tax_section": section_code,
                    "tax_category": section_title,
                    "reason": reason
                }
                tax_items.append(item)
                
                t["is_tax_relevant"] = True
                t["tax_category"] = section_code
                t["tax_reason"] = reason

                by_section[section_code] = round(by_section.get(section_code, 0.0) + amount, 2)
                total_tax_relevant += amount
                break

    return {
        "total_tax_relevant": round(total_tax_relevant, 2),
        "by_section": by_section,
        "items": tax_items,
        "disclaimer": TAX_DISCLAIMER
    }
