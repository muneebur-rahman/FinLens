import os
import csv
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

TEST_DIR = Path("d:/FineLens/test_data")
TEST_DIR.mkdir(parents=True, exist_ok=True)

# Statement A: Corporate Tech Employee (HDFC Bank Format)
STATEMENT_A_ROWS = [
    ["Date", "Narration", "Chq/Ref No", "Withdrawal (Dr)", "Deposit (Cr)", "Closing Balance"],
    ["01/01/2025", "NEFT CR-HDFC0000001-GOOGLE INDIA TECH-SALARY DEC", "HDFCN00129", "", "135000.00", "154200.00"],
    ["03/01/2025", "UPI/500312948/RENT PAYMENT TO LANDLORD RAJESH", "UPI500312", "32000.00", "", "122200.00"],
    ["04/01/2025", "UPI/500492812/SWIGGY BANGALORE/HDFC0012/ORDER", "UPI500492", "540.00", "", "121660.00"],
    ["05/01/2025", "BIL/IN/001923/BESCOM ELECTRICITY BILL/BILLDESK", "BIL001923", "2200.00", "", "119460.00"],
    ["06/01/2025", "BIL/IN/002481/AIRTEL FIBER BROADBAND/BILLDESK", "BIL002481", "1199.00", "", "118261.00"],
    ["07/01/2025", "ACH D- NETFLIX ENTERTAINMENT IN MUMBAI 400012", "ACH007123", "649.00", "", "117612.00"],
    ["08/01/2025", "POS 40192348 SPOTIFY INDIA SUBSCRIPTION", "POS401923", "119.00", "", "117493.00"],
    ["09/01/2025", "ACH D- CULT FIT HEALTHCARE FITNESS BANGALORE", "ACH009812", "1499.00", "", "115994.00"],
    ["10/01/2025", "NEFT DR-ZERODHA BROKING LTD-ELSS TAX SAVER MF 80C", "HDFCD0192", "15000.00", "", "100994.00"],
    ["11/01/2025", "UPI/501192834/UBER RIDES INDIA/HDFC", "UPI501192", "380.00", "", "100614.00"],
    ["12/01/2025", "BIL/IN/009182/STAR HEALTH MEDICLAIM INSURANCE 80D", "BIL009182", "11500.00", "", "89114.00"],
    ["14/01/2025", "UPI/501489123/ZOMATO RESTAURANT ORDER/HDFC", "UPI501489", "780.00", "", "88334.00"],
    ["16/01/2025", "AMZN MKTP IN*40192384 AMAZON INDIA RETAIL", "AMZN40192", "3400.00", "", "84934.00"],
    ["18/01/2025", "UPI/501823910/BLINKIT QUICK COMMERCE/HDFC", "UPI501823", "1450.00", "", "83484.00"],
    ["20/01/2025", "POS 491023 STARBUCKS COFFEE INDIRANAGAR", "POS491023", "620.00", "", "82864.00"],
    ["22/01/2025", "POS 901823 CROMA ELECTRONICS LAPTOP PURCHASE", "POS901823", "74990.00", "", "7874.00"],
    ["24/01/2025", "UPI/502419283/APOLLO PHARMACY BANGALORE", "UPI502419", "950.00", "", "6924.00"],
    ["28/01/2025", "ATM WDL CASH 280125 S1ACN002 INDIRANAGAR", "ATM280125", "4000.00", "", "2924.00"]
]

# Statement B: Freelancer / Contractor (ICICI Bank Format)
STATEMENT_B_ROWS = [
    ["Txn Date", "Transaction Details", "Cheque No", "Debit", "Credit", "Balance"],
    ["05/01/2025", "UPI/500512839/UPWORK ESCROW CLIENT INVOICE/ICICI", "UPI500512", "", "28000.00", "34200.00"],
    ["08/01/2025", "UPI/500819283/DMART SUPERMARKET PROVISIONS/ICICI", "UPI500819", "4250.00", "", "29950.00"],
    ["12/01/2025", "POS 301928 INDIAN OIL PETROL PUMP FUEL", "POS301928", "1800.00", "", "28150.00"],
    ["15/01/2025", "UPI/501592812/ZEPTO GROCERY DELIVERY/ICICI", "UPI501592", "820.00", "", "27330.00"],
    ["19/01/2025", "NEFT CR-ICIC0001-DESIGN STUDIO CLIENT RETAINER", "ICICN0918", "", "34500.00", "61830.00"],
    ["21/01/2025", "UPI/502192834/LOCAL CAFE DINING/ICICI", "UPI502192", "640.00", "", "61190.00"],
    ["23/01/2025", "POS 819283 QUICK MOBILE PHONE SCREEN REPAIR", "POS819283", "8500.00", "", "52690.00"],
    ["27/01/2025", "UPI/502719283/PHARMACY MEDICINES/ICICI", "UPI502719", "490.00", "", "52200.00"]
]

# Statement C: Minimalist (Zero subscriptions, zero anomalies)
STATEMENT_C_ROWS = [
    ["Date", "Description", "Debit", "Credit", "Balance"],
    ["01/01/2025", "NEFT CR-SALARY FOR JAN 2025", "", "45000.00", "47800.00"],
    ["04/01/2025", "SUPERMARKET GROCERY PROVISIONS", "6500.00", "", "41300.00"],
    ["07/01/2025", "BESCOM ELECTRICITY BILL PAYMENT", "1400.00", "", "39900.00"],
    ["10/01/2025", "BWSSB WATER SUPPLY BILL", "450.00", "", "39450.00"],
    ["15/01/2025", "BMTC MONTHLY BUS PASS RECHARGE", "1050.00", "", "38400.00"]
]

def create_csv(filename: str, rows: list):
    path = TEST_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Created CSV: {path}")

def create_pdf(filename: str, bank_title: str, rows: list):
    pdf_path = str(TEST_DIR / filename)
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []

    # Bank Header
    title_style = ParagraphStyle(
        name="BankTitle",
        parent=styles["Heading1"],
        fontSize=14,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=6
    )
    sub_style = ParagraphStyle(
        name="SubText",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12
    )

    elements.append(Paragraph(f"<b>{bank_title}</b> — Statement of Account", title_style))
    elements.append(Paragraph("Account No: 50100492819230 • Branch: Indiranagar, Bangalore • Period: 01/01/2025 to 31/01/2025", sub_style))
    elements.append(Spacer(1, 10))

    # Table formatting
    table_data = []
    # Header
    table_data.append([Paragraph(f"<b>{c}</b>", styles["Normal"]) for c in rows[0]])
    # Data rows
    for r in rows[1:]:
        row_cells = []
        for idx, cell in enumerate(r):
            text = str(cell)
            # Use smaller font for narration
            cell_style = ParagraphStyle(
                name=f"Cell_{idx}",
                parent=styles["Normal"],
                fontSize=8,
                textColor=colors.HexColor("#1F2937")
            )
            row_cells.append(Paragraph(text, cell_style))
        table_data.append(row_cells)

    col_widths = [65, 220, 65, 65, 65, 70] if len(rows[0]) == 6 else [80, 250, 70, 70, 80]
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    elements.append(t)
    doc.build(elements)
    print(f"Created PDF: {pdf_path}")

if __name__ == "__main__":
    create_csv("statement_a_corporate_salary.csv", STATEMENT_A_ROWS)
    create_pdf("statement_a_corporate_salary.pdf", "HDFC BANK LIMITED", STATEMENT_A_ROWS)
    
    create_csv("statement_b_freelancer_irregular.csv", STATEMENT_B_ROWS)
    create_pdf("statement_b_freelancer_irregular.pdf", "ICICI BANK LIMITED", STATEMENT_B_ROWS)
    
    create_csv("statement_c_minimalist_no_subscriptions.csv", STATEMENT_C_ROWS)
    print("All test statement datasets created successfully!")
