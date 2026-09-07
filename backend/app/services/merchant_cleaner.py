import re
from typing import Tuple, Optional

# Pre-compiled regex patterns for standard banking prefixes and artifacts
CLEANUP_REGEXES = [
    re.compile(r"^UPI(?:-|\/)(?:CR|DR)?(?:-|\/)?", re.IGNORECASE),
    re.compile(r"^NEFT(?:-|\/)(?:CR|DR)?(?:-|\/)?", re.IGNORECASE),
    re.compile(r"^IMPS(?:-|\/)(?:P2A|P2P|P2U)?(?:-|\/)?", re.IGNORECASE),
    re.compile(r"^RTGS(?:-|\/)(?:CR|DR)?(?:-|\/)?", re.IGNORECASE),
    re.compile(r"^POS\s+(?:\d+\s+)?", re.IGNORECASE),
    re.compile(r"^BIL(?:-|\/)(?:IN|OUT)?(?:-|\/)?(?:\d+\/)?", re.IGNORECASE),
    re.compile(r"^ACH(?:-|\/|\s+)(?:CR|DR)?(?:-|\/|\s+)?", re.IGNORECASE),
    re.compile(r"^INB(?:-|\/|\s+)", re.IGNORECASE),
    re.compile(r"^TPT(?:-|\/|\s+)", re.IGNORECASE),
    re.compile(r"^ATM\s+(?:WDL|CASH|CWDR)\s*", re.IGNORECASE),
    re.compile(r"^ECOM\s+PUR\s*", re.IGNORECASE),
]

# Known merchant dictionary with canonical names and primary category hints
KNOWN_MERCHANTS = {
    # Food & Dining
    "swiggy": ("Swiggy", "Food & Dining"),
    "zomato": ("Zomato", "Food & Dining"),
    "mcdonalds": ("McDonald's", "Food & Dining"),
    "dominos": ("Domino's Pizza", "Food & Dining"),
    "starbucks": ("Starbucks", "Food & Dining"),
    "chaayos": ("Chaayos", "Food & Dining"),
    "chai point": ("Chai Point", "Food & Dining"),
    "kfc": ("KFC", "Food & Dining"),
    "burger king": ("Burger King", "Food & Dining"),
    "subway": ("Subway", "Food & Dining"),
    "eatfit": ("EatFit", "Food & Dining"),
    
    # Groceries
    "blinkit": ("Blinkit", "Groceries"),
    "zepto": ("Zepto", "Groceries"),
    "instamart": ("Swiggy Instamart", "Groceries"),
    "bigbasket": ("BigBasket", "Groceries"),
    "nature basket": ("Nature's Basket", "Groceries"),
    "dmart": ("DMart", "Groceries"),
    "spencer": ("Spencer's", "Groceries"),
    "more retail": ("More Supermarket", "Groceries"),
    "reliance fresh": ("Reliance Fresh", "Groceries"),
    "supermarket": ("Supermarket", "Groceries"),
    "kirana": ("Local Grocery Store", "Groceries"),
    
    # Shopping
    "amazon": ("Amazon", "Shopping"),
    "flipkart": ("Flipkart", "Shopping"),
    "myntra": ("Myntra", "Shopping"),
    "ajio": ("Ajio", "Shopping"),
    "nykaa": ("Nykaa", "Shopping"),
    "tata cliq": ("Tata CLiQ", "Shopping"),
    "zara": ("Zara", "Shopping"),
    "h&m": ("H&M", "Shopping"),
    "uniqlo": ("Uniqlo", "Shopping"),
    "croma": ("Croma Electronics", "Shopping"),
    "reliance digital": ("Reliance Digital", "Shopping"),
    "apple": ("Apple Store", "Shopping"),
    
    # Entertainment & Subscriptions
    "netflix": ("Netflix", "Entertainment"),
    "spotify": ("Spotify", "Entertainment"),
    "prime video": ("Amazon Prime Video", "Entertainment"),
    "hotstar": ("Disney+ Hotstar", "Entertainment"),
    "disney": ("Disney+ Hotstar", "Entertainment"),
    "youtube": ("YouTube Premium", "Entertainment"),
    "bookmyshow": ("BookMyShow", "Entertainment"),
    "pvr": ("PVR Cinemas", "Entertainment"),
    "inox": ("INOX Cinemas", "Entertainment"),
    "playstation": ("PlayStation Network", "Entertainment"),
    "steam": ("Steam Games", "Entertainment"),
    
    # Utilities & Bills
    "airtel": ("Airtel", "Utilities"),
    "jio": ("Reliance Jio", "Utilities"),
    "vodafone": ("Vodafone Idea", "Utilities"),
    "vi bill": ("Vodafone Idea", "Utilities"),
    "bescom": ("BESCOM Electricity", "Utilities"),
    "tatapower": ("Tata Power", "Utilities"),
    "adani electricity": ("Adani Electricity", "Utilities"),
    "mahavitaran": ("MSEDCL Electricity", "Utilities"),
    "mahanagar gas": ("Mahanagar Gas", "Utilities"),
    "indane": ("Indane LPG", "Utilities"),
    "bharat gas": ("Bharat Gas", "Utilities"),
    "act fibernet": ("ACT Fibernet", "Utilities"),
    "hathway": ("Hathway Broadband", "Utilities"),
    
    # Transport & Travel
    "uber": ("Uber", "Transport"),
    "ola": ("Ola Cabs", "Transport"),
    "rapido": ("Rapido", "Transport"),
    "metro": ("Metro Rail", "Transport"),
    "irctc": ("IRCTC", "Travel"),
    "makemytrip": ("MakeMyTrip", "Travel"),
    "goibibo": ("Goibibo", "Travel"),
    "indigo": ("IndiGo Airlines", "Travel"),
    "air india": ("Air India", "Travel"),
    "fastag": ("NHAI FASTag", "Transport"),
    "indian oil": ("Indian Oil Fuel", "Transport"),
    "hpcl": ("HP Petrol Pump", "Transport"),
    "bpcl": ("Bharat Petroleum", "Transport"),
    
    # Health & Medical
    "apollo": ("Apollo Pharmacy", "Healthcare"),
    "1mg": ("Tata 1mg", "Healthcare"),
    "pharmeasy": ("PharmEasy", "Healthcare"),
    "medplus": ("MedPlus Pharmacy", "Healthcare"),
    "netmeds": ("Netmeds", "Healthcare"),
    "practo": ("Practo Healthcare", "Healthcare"),
    "max healthcare": ("Max Healthcare", "Healthcare"),
    "fortis": ("Fortis Hospital", "Healthcare"),
    "manipal": ("Manipal Hospital", "Healthcare"),
    "star health": ("Star Health Insurance", "Healthcare"),
    
    # Investments & Finance
    "zerodha": ("Zerodha", "Investments"),
    "groww": ("Groww", "Investments"),
    "upstox": ("Upstox", "Investments"),
    "angelone": ("Angel One", "Investments"),
    "kuvera": ("Kuvera", "Investments"),
    "etmoney": ("ET Money", "Investments"),
    "uti mutual": ("UTI Mutual Fund", "Investments"),
    "hdfc mutual": ("HDFC Mutual Fund", "Investments"),
    "icici pru": ("ICICI Prudential MF", "Investments"),
    "sbi mutual": ("SBI Mutual Fund", "Investments"),
    "lic": ("Life Insurance Corp (LIC)", "Investments"),
    "nps": ("National Pension System (NPS)", "Investments"),
    "ppf": ("Public Provident Fund", "Investments"),
    
    # Rent & Housing
    "cred rent": ("Landlord (Rent via CRED)", "Rent"),
    "nobroker": ("NoBroker Rent", "Rent"),
    "housing.com": ("Housing Rent", "Rent"),
}

def clean_merchant_name(raw_text: str) -> Tuple[str, Optional[str]]:
    """
    Cleans messy bank transaction narrations and returns:
    (Clean Merchant Name, Hinted Category or None)
    """
    if not raw_text:
        return "Unknown Merchant", None

    text = str(raw_text).strip()
    
    # Check known merchants first (case-insensitive substring)
    lower_text = text.lower()
    for key, (canonical_name, category) in KNOWN_MERCHANTS.items():
        # Match whole word or bounded substring
        if re.search(r'\b' + re.escape(key) + r'\b', lower_text) or key in lower_text:
            return canonical_name, category
            
    # Remove standard bank prefixes
    cleaned = text
    for pattern in CLEANUP_REGEXES:
        cleaned = pattern.sub("", cleaned).strip()
        
    # Remove typical UPI reference suffixes e.g., /1234567890/HDFC00012/XX or @okaxis, @okhdfcbank
    cleaned = re.sub(r"\/[A-Z0-9_-]+(?:\/[A-Z0-9_-]+)*$", "", cleaned)
    cleaned = re.sub(r"@[a-zA-Z0-9_.-]+", "", cleaned)
    
    # Remove reference numbers, masked card digits like XXXXXX1234, dates, timestamps
    cleaned = re.sub(r"\b\d{6,}\b", "", cleaned)
    cleaned = re.sub(r"\b(?:XX|X{3,})\d{3,4}\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b\d{2}[-/]\d{2}[-/]\d{2,4}\b", "", cleaned)
    cleaned = re.sub(r"\b\d{2}:\d{2}(?::\d{2})?\b", "", cleaned)
    
    # Remove trailing city/location if common
    cleaned = re.sub(r"\b(BANGALORE|BENGALURU|MUMBAI|DELHI|GURGAON|HYDERABAD|PUNE|CHENNAI|KOLKATA|NOIDA|AHMEDABAD)\b", "", cleaned, flags=re.IGNORECASE)
    
    # Strip extraneous punctuation and multiple spaces
    cleaned = re.sub(r"[-_/\\*#:]+", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    
    # Check if empty after cleaning
    if not cleaned or len(cleaned) < 2:
        return "Bank Transfer / Counterparty", None
        
    # Special heuristics
    cleaned_lower = cleaned.lower()
    if "salary" in cleaned_lower or "payroll" in cleaned_lower:
        return cleaned.title(), "Salary"
    if "rent" in cleaned_lower:
        return cleaned.title(), "Rent"
    if "atm" in cleaned_lower or "cash" in cleaned_lower:
        return "ATM Cash Withdrawal", "Cash Withdrawal"
    if "interest" in cleaned_lower:
        return "Bank Interest", "Freelance/Business Income"
    if "dividend" in cleaned_lower:
        return "Dividend Payout", "Investments"
        
    # Return formatted title
    # Keep uppercase for short acronyms like 'SBI', 'HDFC', 'TCS'
    words = cleaned.split()
    formatted_words = [w.upper() if len(w) <= 4 and w.isupper() else w.title() for w in words]
    formatted_name = " ".join(formatted_words[:4]) # Keep max 4 words for clean UI
    
    return formatted_name, None
