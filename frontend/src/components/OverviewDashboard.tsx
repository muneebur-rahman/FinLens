import React from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  Wallet, 
  ShieldAlert, 
  Repeat, 
  ShieldCheck, 
  Sparkles, 
  ArrowUpRight, 
  ArrowDownRight,
  Info,
  Calendar,
  Layers,
  ChevronRight
} from 'lucide-react';
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  Tooltip, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  BarChart, 
  Bar, 
  Legend 
} from 'recharts';
import { DashboardData, NavView } from '../types';

interface OverviewDashboardProps {
  data: DashboardData;
  onNavigate: (view: NavView) => void;
  onOpenAssistant: () => void;
}

const formatCurrency = (amt: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amt);
};

export const OverviewDashboard: React.FC<OverviewDashboardProps> = ({
  data,
  onNavigate,
  onOpenAssistant,
}) => {
  const {
    total_income,
    total_expenses,
    net_savings,
    savings_rate,
    health_score,
    health_breakdown,
    category_breakdown,
    spending_trends,
    top_categories,
    recurring_monthly_spend,
    subscriptions,
    anomalies,
    tax_summary,
    filename,
    date_start,
    date_end,
    transaction_count,
    is_demo,
  } = data;

  const isNetPositive = net_savings >= 0;

  // Chart data formatting for pie
  const pieData = category_breakdown.filter((c) => c.total_amount > 0);

  return (
    <div className="space-y-8 animate-fadeIn pb-16">
      {/* Demo Mode Banner if active */}
      {is_demo && (
        <div className="p-3.5 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse" />
            <span className="text-xs font-semibold text-amber-300">
              DEMO MODE: Displaying simulated Indian bank statement. Upload your own statement to see real results.
            </span>
          </div>
          <button
            onClick={() => onNavigate('overview')}
            className="text-xs font-bold text-amber-400 hover:text-amber-200 underline underline-offset-2"
          >
            Upload Real
          </button>
        </div>
      )}

      {/* Statement Header Meta */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-bold text-white tracking-tight">
              Executive Financial Summary
            </h1>
            <span className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-mono">
              {filename}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5 text-slate-500" />
            <span>
              Period: <b className="text-slate-200">{date_start || 'N/A'}</b> to <b className="text-slate-200">{date_end || 'N/A'}</b>
            </span>
            <span className="text-slate-600">•</span>
            <span><b className="text-slate-200">{transaction_count}</b> transactions verified</span>
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            id="overview-ask-ai-btn"
            onClick={onOpenAssistant}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-xs font-semibold transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Ask FinLens AI</span>
          </button>
        </div>
      </div>

      {/* Top 4 KPI Metrics (Strictly derived from statement) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Income */}
        <div className="glass-card p-5 rounded-2xl border-slate-800 transition-all">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-400">Total Income</span>
            <div className="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-black text-white tracking-tight font-mono">
            {formatCurrency(total_income)}
          </div>
          <div className="flex items-center gap-1 mt-2 text-[11px] text-emerald-400 font-medium">
            <ArrowUpRight className="w-3.5 h-3.5" />
            <span>Verified inflows from statement</span>
          </div>
        </div>

        {/* Total Expenses */}
        <div className="glass-card p-5 rounded-2xl border-slate-800 transition-all">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-400">Total Expenses</span>
            <div className="w-8 h-8 rounded-xl bg-rose-500/10 text-rose-400 flex items-center justify-center">
              <TrendingDown className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-black text-white tracking-tight font-mono">
            {formatCurrency(total_expenses)}
          </div>
          <div className="flex items-center gap-1 mt-2 text-[11px] text-rose-400 font-medium">
            <ArrowDownRight className="w-3.5 h-3.5" />
            <span>{category_breakdown.length} spending categories active</span>
          </div>
        </div>

        {/* Net Savings */}
        <div className="glass-card p-5 rounded-2xl border-slate-800 transition-all">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-400">Net Savings</span>
            <div className={`w-8 h-8 rounded-xl flex items-center justify-center ${
              isNetPositive ? 'bg-teal-500/10 text-teal-400' : 'bg-rose-500/10 text-rose-400'
            }`}>
              <Wallet className="w-4 h-4" />
            </div>
          </div>
          <div className={`text-2xl font-black tracking-tight font-mono ${
            isNetPositive ? 'text-white' : 'text-rose-300'
          }`}>
            {formatCurrency(net_savings)}
          </div>
          <div className="flex items-center gap-1 mt-2 text-[11px] font-medium text-slate-400">
            <span>Savings Rate:</span>
            <b className={`font-mono ${savings_rate >= 20 ? 'text-emerald-400' : savings_rate > 0 ? 'text-amber-400' : 'text-rose-400'}`}>
              {savings_rate}%
            </b>
          </div>
        </div>

        {/* Financial Health Score */}
        <div 
          onClick={() => onNavigate('overview')}
          className="glass-card p-5 rounded-2xl border-slate-800 cursor-pointer hover:border-emerald-500/40 transition-all"
        >
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-400">Health Score</span>
            <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
              {health_breakdown?.rating || 'Calculated'}
            </span>
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-black text-emerald-400 font-mono">
              {health_score}
            </span>
            <span className="text-xs text-slate-500 font-medium">/ 100</span>
          </div>
          <div className="mt-2 text-[11px] text-slate-400 truncate">
            {health_breakdown?.whats_helping?.[0] || 'Derived from actual data'}
          </div>
        </div>
      </div>

      {/* Transparent Health Score Deep Dive Panel */}
      <div className="p-6 rounded-3xl bg-gradient-to-br from-slate-900/90 to-slate-950 border border-slate-800 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <h2 className="text-base font-bold text-white">
                Transparent Financial Health Score Engine
              </h2>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Calculated deterministically from your savings rate, expense-to-income ratio, recurring obligations, and transaction patterns.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-right">
              <div className="text-xs font-bold text-white">Score: {health_score}/100</div>
              <div className="text-[11px] text-emerald-400">{health_breakdown?.rating} Condition</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* What's Helping */}
          <div className="p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/20">
            <div className="flex items-center gap-2 mb-3">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-300">
                What's Helping
              </h3>
            </div>
            <ul className="space-y-2">
              {health_breakdown?.whats_helping?.map((item, idx) => (
                <li key={idx} className="text-xs text-slate-300 flex items-start gap-2">
                  <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* What Could Improve */}
          <div className="p-4 rounded-2xl bg-amber-500/5 border border-amber-500/20">
            <div className="flex items-center gap-2 mb-3">
              <span className="w-2 h-2 rounded-full bg-amber-400" />
              <h3 className="text-xs font-bold uppercase tracking-wider text-amber-300">
                What Could Improve
              </h3>
            </div>
            <ul className="space-y-2">
              {health_breakdown?.whats_improving?.length ? (
                health_breakdown.whats_improving.map((item, idx) => (
                  <li key={idx} className="text-xs text-slate-300 flex items-start gap-2">
                    <span className="text-amber-400 font-bold mt-0.5">⚠</span>
                    <span>{item}</span>
                  </li>
                ))
              ) : (
                <li className="text-xs text-slate-400 italic">
                  No immediate weaknesses detected in this statement period.
                </li>
              )}
            </ul>
          </div>
        </div>
      </div>

      {/* Spending Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Category Breakdown Donut Chart */}
        <div className="glass-card p-6 rounded-3xl border-slate-800 lg:col-span-1">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Layers className="w-4 h-4 text-emerald-400" />
              <span>Spending by Category</span>
            </h3>
            <button
              onClick={() => onNavigate('spending')}
              className="text-xs text-emerald-400 hover:text-emerald-300 flex items-center gap-0.5"
            >
              <span>Explore</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="h-64 relative flex items-center justify-center">
            {pieData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="total_amount"
                    nameKey="category"
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={95}
                    paddingAngle={3}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(val: any) => [formatCurrency(Number(val)), 'Total Spent']}
                    contentStyle={{
                      backgroundColor: '#0F172A',
                      borderColor: '#334155',
                      borderRadius: '12px',
                      fontSize: '12px',
                      color: '#F8FAFC',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-xs text-slate-500">No expense data available</div>
            )}
          </div>

          {/* Top 3 category chips */}
          <div className="space-y-2 mt-2 pt-4 border-t border-slate-800">
            {top_categories.slice(0, 3).map((c) => (
              <div key={c.category} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: c.color }} />
                  <span className="text-slate-300 font-medium">{c.category}</span>
                </div>
                <div className="text-right font-mono text-slate-400">
                  <span className="text-slate-200 font-semibold">{formatCurrency(c.total_amount)}</span>
                  <span className="text-[10px] text-slate-500 ml-1.5">({c.percentage}%)</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Spending Trend Line Chart */}
        <div className="glass-card p-6 rounded-3xl border-slate-800 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-cyan-400" />
                <span>Spending & Cash Flow Timeline</span>
              </h3>
              <p className="text-[11px] text-slate-400">
                Daily expense and income activity across statement timeline
              </p>
            </div>
            <div className="flex items-center gap-3 text-xs">
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-400" />
                <span className="text-slate-400">Expenses</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                <span className="text-slate-400">Income</span>
              </div>
            </div>
          </div>

          <div className="h-64">
            {spending_trends.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={spending_trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="expenseGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#F43F5E" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#F43F5E" stopOpacity={0.0}/>
                    </linearGradient>
                    <linearGradient id="incomeGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10B981" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#10B981" stopOpacity={0.0}/>
                    </linearGradient>
                  </defs>
                  <XAxis 
                    dataKey="period" 
                    stroke="#475569" 
                    fontSize={10} 
                    tickLine={false}
                    tickFormatter={(val) => val ? val.slice(5) : ''}
                  />
                  <YAxis 
                    stroke="#475569" 
                    fontSize={10} 
                    tickLine={false}
                    tickFormatter={(v) => `₹${v >= 1000 ? (v / 1000).toFixed(0) + 'k' : v}`}
                  />
                  <Tooltip
                    formatter={(val: any, name: any) => [formatCurrency(Number(val)), name === 'expenses' ? 'Outflow' : 'Inflow']}
                    contentStyle={{
                      backgroundColor: '#0F172A',
                      borderColor: '#334155',
                      borderRadius: '12px',
                      fontSize: '12px',
                    }}
                  />
                  <Area type="monotone" dataKey="expenses" stroke="#F43F5E" strokeWidth={2} fillOpacity={1} fill="url(#expenseGrad)" />
                  <Area type="monotone" dataKey="income" stroke="#10B981" strokeWidth={2} fillOpacity={1} fill="url(#incomeGrad)" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-500">
                Timeline data not available
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 3 Quick Domain Summaries (Subscriptions, Anomalies, Tax) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Subscriptions Card */}
        <div 
          onClick={() => onNavigate('subscriptions')}
          className="glass-card p-5 rounded-2xl border-slate-800 hover:border-emerald-500/30 cursor-pointer transition-all group"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center">
                <Repeat className="w-3.5 h-3.5" />
              </div>
              <h4 className="text-xs font-bold text-white">Subscriptions Detected</h4>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono">
              {subscriptions.length} detected
            </span>
          </div>

          <div className="text-xl font-bold text-white font-mono mb-1">
            {formatCurrency(recurring_monthly_spend)}
            <span className="text-xs text-slate-400 font-normal font-sans"> /month</span>
          </div>

          <p className="text-[11px] text-slate-400 line-clamp-2">
            {subscriptions.length > 0 
              ? `${subscriptions.map((s) => s.merchant).join(', ')} recurring commitments detected.`
              : 'No recurring subscriptions detected in this statement.'
            }
          </p>
        </div>

        {/* Anomalies Card */}
        <div 
          onClick={() => onNavigate('anomalies')}
          className="glass-card p-5 rounded-2xl border-slate-800 hover:border-amber-500/30 cursor-pointer transition-all group"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center">
                <ShieldAlert className="w-3.5 h-3.5" />
              </div>
              <h4 className="text-xs font-bold text-white">Anomaly Alerts</h4>
            </div>
            <span className={`text-[10px] px-2 py-0.5 rounded-full font-mono font-bold ${
              anomalies.length > 0 ? 'bg-amber-500/20 text-amber-300' : 'bg-slate-800 text-slate-400'
            }`}>
              {anomalies.length} flagged
            </span>
          </div>

          <div className="text-xl font-bold text-white font-mono mb-1">
            {anomalies.length}
            <span className="text-xs text-slate-400 font-normal font-sans"> outliers</span>
          </div>

          <p className="text-[11px] text-slate-400 line-clamp-2">
            {anomalies.length > 0 
              ? anomalies[0].reason
              : 'No unusual spending patterns detected relative to baseline.'
            }
          </p>
        </div>

        {/* Tax Helper Card */}
        <div 
          onClick={() => onNavigate('tax')}
          className="glass-card p-5 rounded-2xl border-slate-800 hover:border-cyan-500/30 cursor-pointer transition-all group"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center">
                <ShieldCheck className="w-3.5 h-3.5" />
              </div>
              <h4 className="text-xs font-bold text-white">Tax Helper</h4>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-cyan-300 font-mono">
              {tax_summary.items.length} items
            </span>
          </div>

          <div className="text-xl font-bold text-white font-mono mb-1">
            {formatCurrency(tax_summary.total_tax_relevant)}
            <span className="text-xs text-slate-400 font-normal font-sans"> potential</span>
          </div>

          <p className="text-[11px] text-slate-400 line-clamp-2">
            {tax_summary.items.length > 0 
              ? `Sections identified: ${Object.keys(tax_summary.by_section).join(', ')}.`
              : 'No eligible tax deductions detected in statement transactions.'
            }
          </p>
        </div>
      </div>
    </div>
  );
};
