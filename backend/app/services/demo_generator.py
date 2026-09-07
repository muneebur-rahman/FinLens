import uuid
from datetime import datetime
from typing import List, Dict, Any

DEMO_TRANSACTIONS = [
    # Salary & Inflows
    {"date": "2025-01-01", "raw": "NEFT CR-HDFC0000001-TECHCORP INDIA PVT LTD-SALARY JAN 2025", "merchant": "TechCorp India", "amount": 115000.00, "type": "credit", "bal": 128450.00},
    {"date": "2025-01-18", "raw": "UPI/CR/501823910/FREELANCE UI DESIGN/CLIENT/HDFC", "merchant": "Client UI Project", "amount": 18500.00, "type": "credit", "bal": 105650.00},
    
    # Rent & Housing
    {"date": "2025-01-03", "raw": "UPI/500329104/RENT PAYMENT TO LANDLORD RAJESH/HDFC", "merchant": "Landlord (House Rent)", "amount": 28000.00, "type": "debit", "bal": 100450.00},
    
    # Utilities
    {"date": "2025-01-05", "raw": "BIL/IN/001923/BESCOM ELECTRICITY BILL/BILLDESK", "merchant": "BESCOM Electricity", "amount": 2450.00, "type": "debit", "bal": 98000.00},
    {"date": "2025-01-06", "raw": "BIL/IN/002481/AIRTEL BROADBAND FIBER/BILLDESK", "merchant": "Airtel Broadband", "amount": 1179.00, "type": "debit", "bal": 96821.00},
    
    # Subscriptions (Recurring)
    {"date": "2025-01-07", "raw": "ACH D- NETFLIX ENTERTAINMENT IN MUMBAI 400012", "merchant": "Netflix", "amount": 649.00, "type": "debit", "bal": 96172.00},
    {"date": "2025-01-08", "raw": "POS 40192348 SPOTIFY INDIA SUBSCRIPTION", "merchant": "Spotify", "amount": 119.00, "type": "debit", "bal": 96053.00},
    {"date": "2025-01-09", "raw": "ACH D- CULT FIT HEALTHCARE FITNESS BANGALORE", "merchant": "Cult.fit", "amount": 1499.00, "type": "debit", "bal": 94554.00},
    
    # Investments & Tax Deductions (80C & 80D)
    {"date": "2025-01-10", "raw": "NEFT DR-ZERODHA BROKING LTD-EQUITY SIP JAN", "merchant": "Zerodha Mutual Fund SIP", "amount": 15000.00, "type": "debit", "bal": 79554.00},
    {"date": "2025-01-12", "raw": "BIL/IN/009182/STAR HEALTH INSURANCE PREMIUM 80D", "merchant": "Star Health Insurance", "amount": 9500.00, "type": "debit", "bal": 70054.00},
    
    # Food & Dining
    {"date": "2025-01-04", "raw": "UPI/500412389/SWIGGY BANGALORE/HDFC0012/ORDER", "merchant": "Swiggy", "amount": 420.00, "type": "debit", "bal": 97580.00},
    {"date": "2025-01-09", "raw": "UPI/500912444/ZOMATO RESTAURANT/HDFC/ORDER", "merchant": "Zomato", "amount": 680.00, "type": "debit", "bal": 93874.00},
    {"date": "2025-01-14", "raw": "UPI/501489123/SWIGGY GOURMET/HDFC/ORDER", "merchant": "Swiggy", "amount": 850.00, "type": "debit", "bal": 69204.00},
    {"date": "2025-01-20", "raw": "POS 491023 STARBUCKS COFFEE INDIRANAGAR", "merchant": "Starbucks", "amount": 540.00, "type": "debit", "bal": 68664.00},
    {"date": "2025-01-26", "raw": "UPI/502619481/DOMINOS PIZZA BANGALORE/HDFC", "merchant": "Domino's Pizza", "amount": 720.00, "type": "debit", "bal": 67944.00},
    
    # Groceries
    {"date": "2025-01-05", "raw": "UPI/500581923/BLINKIT GROCERY DELIVERY/HDFC", "merchant": "Blinkit", "amount": 1280.00, "type": "debit", "bal": 95541.00},
    {"date": "2025-01-15", "raw": "POS 401823 NATURES BASKET INDIRANAGAR", "merchant": "Nature's Basket", "amount": 3450.00, "type": "debit", "bal": 64494.00},
    {"date": "2025-01-23", "raw": "UPI/502391028/ZEPTO QUICK COMMERCE/HDFC", "merchant": "Zepto", "amount": 960.00, "type": "debit", "bal": 63534.00},
    
    # Transport
    {"date": "2025-01-11", "raw": "UPI/501192834/UBER RIDES INDIA/HDFC", "merchant": "Uber", "amount": 340.00, "type": "debit", "bal": 69714.00},
    {"date": "2025-01-17", "raw": "POS 301928 INDIAN OIL PETROL PUMP BANGALORE", "merchant": "Indian Oil Fuel", "amount": 2500.00, "type": "debit", "bal": 61034.00},
    {"date": "2025-01-25", "raw": "UPI/502519283/FASTAG RECHARGE NHAI/HDFC", "merchant": "FASTag", "amount": 1000.00, "type": "debit", "bal": 60034.00},
    
    # Shopping
    {"date": "2025-01-13", "raw": "AMZN MKTP IN*40192384 AMAZON INDIA", "merchant": "Amazon", "amount": 2890.00, "type": "debit", "bal": 66314.00},
    
    # Anomaly (Unusually high electronics purchase)
    {"date": "2025-01-21", "raw": "POS 901823 CROMA ELECTRONICS INDIRANAGAR BLR", "merchant": "Croma Electronics", "amount": 24999.00, "type": "debit", "bal": 35035.00},
    
    # Healthcare
    {"date": "2025-01-16", "raw": "POS 401928 APOLLO PHARMACY BANGALORE", "merchant": "Apollo Pharmacy", "amount": 890.00, "type": "debit", "bal": 60144.00},
    
    # Cash Withdrawal
    {"date": "2025-01-22", "raw": "ATM WDL CASH 220125 S1ACN002 INDIRANAGAR", "merchant": "ATM Cash Withdrawal", "amount": 5000.00, "type": "debit", "bal": 30035.00}
]

def get_demo_statement_data() -> List[Dict[str, Any]]:
    txns = []
    for item in DEMO_TRANSACTIONS:
        txns.append({
            "raw_date": item["date"],
            "raw_description": item["raw"],
            "amount": item["amount"],
            "type": item["type"],
            "balance": item.get("bal")
        })
    return txns
