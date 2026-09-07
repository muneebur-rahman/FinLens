export interface Transaction {
  id: string;
  session_id?: string;
  date: string;
  raw_description: string;
  merchant: string;
  amount: number;
  type: 'debit' | 'credit';
  balance: number | null;
  category: string;
  confidence: number;
  category_reason: string | null;
  is_recurring: boolean;
  recurring_cadence: string | null;
  is_anomaly: boolean;
  anomaly_reason: string | null;
  is_tax_relevant: boolean;
  tax_category: string | null;
  tax_reason: string | null;
}

export interface HealthScoreBreakdown {
  score: number;
  rating: string;
  savings_rate_pct: number;
  expense_ratio_pct: number;
  recurring_burden_pct: number;
  discretionary_pct: number;
  whats_helping: string[];
  whats_improving: string[];
}

export interface SubscriptionItem {
  merchant: string;
  average_amount: number;
  cadence: string;
  occurrences: number;
  last_date: string;
  total_spent: number;
  category: string;
  detection_reason: string;
}

export interface AnomalyItem {
  transaction_id: string;
  date: string;
  merchant: string;
  amount: number;
  category: string;
  reason: string;
  severity: 'high' | 'medium' | 'notice';
}

export interface TaxItem {
  transaction_id: string;
  date: string;
  merchant: string;
  amount: number;
  tax_section: string;
  tax_category: string;
  reason: string;
}

export interface TaxSummary {
  total_tax_relevant: number;
  by_section: Record<string, number>;
  items: TaxItem[];
  disclaimer: string;
}

export interface CategoryBreakdownItem {
  category: string;
  total_amount: number;
  percentage: number;
  count: number;
  color: string;
}

export interface SpendingTrendPoint {
  period: string;
  expenses: number;
  income: number;
}

export interface DashboardData {
  session_id: string;
  filename: string;
  is_demo: boolean;
  upload_time: string;
  date_start: string | null;
  date_end: string | null;
  total_income: number;
  total_expenses: number;
  net_savings: number;
  savings_rate: number;
  health_score: number;
  health_breakdown: HealthScoreBreakdown;
  category_breakdown: CategoryBreakdownItem[];
  spending_trends: SpendingTrendPoint[];
  top_categories: CategoryBreakdownItem[];
  recurring_monthly_spend: number;
  subscriptions: SubscriptionItem[];
  anomalies: AnomalyItem[];
  tax_summary: TaxSummary;
  transaction_count: number;
}

export type NavView = 
  | 'overview' 
  | 'transactions' 
  | 'spending' 
  | 'subscriptions' 
  | 'anomalies' 
  | 'tax' 
  | 'assistant' 
  | 'settings';
