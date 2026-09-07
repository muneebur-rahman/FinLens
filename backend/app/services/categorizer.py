from typing import Tuple, Dict, Any, Optional
import re

CATEGORY_RULES = [
    # (Category, Keywords Regex, Explanation Template, Base Confidence)
    (
        "Salary",
        r"\b(?:salary|payroll|stipend|wages|corp salary|monthly pay)\b",
        "Categorized as Salary because narration matches corporate payroll or salary credit keywords.",
        0.95
    ),
    (
        "Freelance/Business Income",
        r"\b(?:upwork|fiverr|toptal|razorpay|stripe|consulting|invoice|retainer|client|freelance|vendor payment)\b",
        "Categorized as Freelance/Business Income because transaction corresponds to client invoice or payout gateway.",
        0.90
    ),
    (
        "Rent",
        r"\b(?:rent|landlord|house rent|lease|flat rent|nobroker|society maintenance|maintenance fee)\b",
        "Categorized as Rent because narration indicates residential rental or society maintenance payment.",
        0.95
    ),
    (
        "Food & Dining",
        r"\b(?:swiggy|zomato|restaurant|cafe|coffee|starbucks|mcdonald|domino|pizza|burger|dining|bistro|dhaba|barbeque|chaayos|chai point|subway|kfc)\b",
        "Categorized as Food & Dining because the merchant matches a food-delivery or dining establishment.",
        0.94
    ),
    (
        "Groceries",
        r"\b(?:blinkit|zepto|instamart|bigbasket|grofers|supermarket|kirana|dmart|grocery|provision|reliance fresh|nature basket|vegetable|fruits|dairy)\b",
        "Categorized as Groceries because merchant matches quick-commerce or grocery retail supplier.",
        0.93
    ),
    (
        "Shopping",
        r"\b(?:amazon|flipkart|myntra|ajio|nykaa|zara|h&m|retail|clothing|apparel|electronics|croma|reliance digital|ikea|decathlon|footwear)\b",
        "Categorized as Shopping because merchant matches e-commerce or retail merchant.",
        0.92
    ),
    (
        "Utilities",
        r"\b(?:electricity|power|bescom|tata power|adani electricity|water board|gas|lpg|indane|bharat gas|airtel|jio|vi bill|broadband|wifi|hathway|act fibernet|billdesk|recharge)\b",
        "Categorized as Utilities because transaction matches essential utility, telecom, or electricity billing.",
        0.94
    ),
    (
        "Transport",
        r"\b(?:uber|ola|rapido|fastag|toll|metro|fuel|petrol|diesel|indian oil|hpcl|bpcl|parking)\b",
        "Categorized as Transport because transaction matches ride-hailing, fuel, transit, or highway toll.",
        0.93
    ),
    (
        "Travel",
        r"\b(?:irctc|railway|makemytrip|goibibo|indigo|air india|hotel|resort|flight|booking\.com|airbnb|yatra|cleartrip)\b",
        "Categorized as Travel because transaction matches airline, train booking, or lodging hospitality.",
        0.92
    ),
    (
        "Entertainment",
        r"\b(?:netflix|spotify|prime video|hotstar|disney|youtube|bookmyshow|pvr|inox|cinema|theatre|steam|playstation|gaming|audible)\b",
        "Categorized as Entertainment because transaction matches digital streaming, cinema, or gaming platform.",
        0.95
    ),
    (
        "Healthcare",
        r"\b(?:pharmacy|hospital|apollo|1mg|pharmeasy|medplus|netmeds|clinic|doctor|practo|diagnostics|pathology|medical|dental|star health|max health)\b",
        "Categorized as Healthcare because merchant matches pharmacy, medical clinic, or healthcare service.",
        0.93
    ),
    (
        "Education",
        r"\b(?:school|college|university|tuition|udemy|coursera|edx|upgrad|simplilearn|books|course|exam fee|coaching)\b",
        "Categorized as Education because transaction matches educational institution, tuition, or e-learning platform.",
        0.91
    ),
    (
        "Investments",
        r"\b(?:zerodha|groww|upstox|mutual fund|sip|nps|ppf|etmoney|angel one|uti mf|hdfc mf|sbi mf|lic|stocks|securities|fixed deposit|fd booking)\b",
        "Categorized as Investments because transaction corresponds to brokerage, mutual fund, or capital assets.",
        0.95
    ),
    (
        "Cash Withdrawal",
        r"\b(?:atm|cash wdl|cwdr|cash withdrawal|self withdrawal)\b",
        "Categorized as Cash Withdrawal because transaction indicates physical cash disbursement from an ATM.",
        0.96
    ),
    (
        "Transfers",
        r"\b(?:transfer to|transfer from|self transfer|neft to|imps to|fund transfer|tpt)\b",
        "Categorized as Transfers because transaction is an inter-account or peer fund transfer.",
        0.85
    )
]

def categorize_transaction(
    merchant: str,
    raw_desc: str,
    txn_type: str,
    merchant_hint: Optional[str] = None
) -> Tuple[str, float, str]:
    """
    Categorizes a transaction with confidence rating and explainable reasoning.
    Returns: (category, confidence, explanation)
    """
    # 1. If merchant cleaner already resolved a definitive known merchant
    if merchant_hint:
        return (
            merchant_hint,
            0.96,
            f"Categorized as {merchant_hint} because merchant '{merchant}' matches known service provider."
        )

    full_text = f"{merchant} {raw_desc}".lower()

    # 2. Check if Credit + Salary
    if txn_type == "credit":
        if re.search(r"\b(?:salary|payroll|stipend|corp sal)\b", full_text):
            return (
                "Salary",
                0.97,
                f"Categorized as Salary because credit transaction narration identifies employer payroll."
            )
        if re.search(r"\b(?:dividend|interest|interest credited|int\.pd)\b", full_text):
            return (
                "Freelance/Business Income",
                0.90,
                f"Categorized as Freelance/Business Income because narration indicates interest or yield credit."
            )

    # 3. Match against regex patterns
    for cat, pattern, explanation, conf in CATEGORY_RULES:
        if re.search(pattern, full_text, re.IGNORECASE):
            # If it's a credit and pattern matched an expense category, adapt appropriately
            if txn_type == "credit" and cat in ["Food & Dining", "Shopping", "Entertainment", "Groceries"]:
                # Likely a refund or cashback
                return (
                    cat,
                    0.88,
                    f"Categorized as {cat} (Refund/Reversal) because merchant matches {cat.lower()} establishment."
                )
            return (cat, conf, explanation)

    # 4. Default Fallback
    if txn_type == "credit":
        return (
            "Freelance/Business Income",
            0.60,
            "Categorized as Freelance/Business Income as an uncategorized incoming credit."
        )
        
    return (
        "Other",
        0.50,
        "Categorized as Other because transaction description did not match standard merchant signatures."
    )
