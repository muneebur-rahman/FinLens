from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TransactionModel(BaseModel):
    id: str
    date: str
    raw_description: str
    merchant: str
    amount: float
    type: str  # "debit" | "credit"
    balance: Optional[float] = None
    category: str
    confidence: float = 0.85
    category_reason: Optional[str] = None
    is_recurring: bool = False
    recurring_cadence: Optional[str] = None
    is_anomaly: bool = False
    anomaly_reason: Optional[str] = None
    is_tax_relevant: bool = False
    tax_category: Optional[str] = None
    tax_reason: Optional[str] = None

class HealthScoreBreakdown(BaseModel):
    score: int
    rating: str  # "Excellent" | "Good" | "Fair" | "Needs Attention"
    savings_rate_pct: float
    expense_ratio_pct: float
    recurring_burden_pct: float
    discretionary_pct: float
    whats_helping: List[str]
    whats_improving: List[str]

class SubscriptionItem(BaseModel):
    merchant: str
    average_amount: float
    cadence: str  # "monthly", "weekly", "annual"
    occurrences: int
    last_date: str
    total_spent: float
    category: str
    detection_reason: str

class AnomalyItem(BaseModel):
    transaction_id: str
    date: str
    merchant: str
    amount: float
    category: str
    reason: str
    severity: str  # "high", "medium", "notice"

class TaxItem(BaseModel):
    transaction_id: str
    date: str
    merchant: str
    amount: float
    tax_section: str  # "80C", "80D", "80G", "80GG/HRA", "Business"
    tax_category: str
    reason: str

class TaxSummary(BaseModel):
    total_tax_relevant: float
    by_section: Dict[str, float]
    items: List[TaxItem]
    disclaimer: str

class SpendingTrendPoint(BaseModel):
    period: str  # Date or Month e.g., "2025-01" or "2025-01-15"
    expenses: float
    income: float

class CategoryBreakdownItem(BaseModel):
    category: str
    total_amount: float
    percentage: float
    count: int
    color: str

class DashboardData(BaseModel):
    session_id: str
    filename: str
    is_demo: bool
    upload_time: str
    date_start: Optional[str]
    date_end: Optional[str]
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate: float
    health_score: int
    health_breakdown: HealthScoreBreakdown
    category_breakdown: List[CategoryBreakdownItem]
    spending_trends: List[SpendingTrendPoint]
    top_categories: List[CategoryBreakdownItem]
    recurring_monthly_spend: float
    subscriptions: List[SubscriptionItem]
    anomalies: List[AnomalyItem]
    tax_summary: TaxSummary
    transaction_count: int

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    answer: str
    citations: Optional[List[Dict[str, Any]]] = None
    data_points: Optional[Dict[str, Any]] = None
