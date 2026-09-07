import React from 'react';
import { Layers, PieChart as PieIcon, TrendingDown, DollarSign } from 'lucide-react';
import { 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell, 
  Tooltip, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis 
} from 'recharts';
import { CategoryBreakdownItem } from '../types';

interface SpendingViewProps {
  categories: CategoryBreakdownItem[];
  totalExpenses: number;
}

const formatCurrency = (amt: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amt);
};

export const SpendingView: React.FC<SpendingViewProps> = ({
  categories,
  totalExpenses,
}) => {
  const activeCategories = categories.filter((c) => c.total_amount > 0);

  return (
    <div className="space-y-6 animate-fadeIn pb-16">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-emerald-400" />
          <span>Spending Breakdown & Analytics</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Detailed category distributions and rankings derived from your verified statement debits.
        </p>
      </div>

      {/* Top Total */}
      <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs text-slate-400">Total Statement Outflows</span>
          <div className="text-3xl font-black text-white font-mono mt-0.5">
            {formatCurrency(totalExpenses)}
          </div>
        </div>
        <div className="text-xs font-mono text-slate-400">
          Spread across <b className="text-emerald-400">{activeCategories.length}</b> distinct categories
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Donut Chart */}
        <div className="glass-card p-6 rounded-3xl border-slate-800">
          <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <PieIcon className="w-4 h-4 text-emerald-400" />
            <span>Category Distribution</span>
          </h3>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={activeCategories}
                  dataKey="total_amount"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={110}
                  paddingAngle={3}
                >
                  {activeCategories.map((entry, idx) => (
                    <Cell key={`cell-${idx}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(val: any) => [formatCurrency(Number(val)), 'Spent']}
                  contentStyle={{
                    backgroundColor: '#0F172A',
                    borderColor: '#334155',
                    borderRadius: '12px',
                    fontSize: '12px',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Horizontal Bar Ranking */}
        <div className="glass-card p-6 rounded-3xl border-slate-800">
          <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <TrendingDown className="w-4 h-4 text-cyan-400" />
            <span>Top Categories Ranked</span>
          </h3>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={activeCategories.slice(0, 7)}
                layout="vertical"
                margin={{ top: 10, right: 30, left: 40, bottom: 5 }}
              >
                <XAxis 
                  type="number" 
                  stroke="#475569" 
                  fontSize={10}
                  tickFormatter={(v) => `₹${v >= 1000 ? (v / 1000).toFixed(0) + 'k' : v}`}
                />
                <YAxis 
                  type="category" 
                  dataKey="category" 
                  stroke="#94A3B8" 
                  fontSize={11}
                  width={90}
                />
                <Tooltip
                  formatter={(val: any) => [formatCurrency(Number(val)), 'Amount']}
                  contentStyle={{
                    backgroundColor: '#0F172A',
                    borderColor: '#334155',
                    borderRadius: '12px',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="total_amount" fill="#10B981" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Category List with Progress Bars */}
      <div className="rounded-3xl border border-slate-800 p-6 bg-slate-900/60">
        <h3 className="text-sm font-bold text-white mb-4">
          All Active Spending Categories
        </h3>
        <div className="space-y-4">
          {activeCategories.map((c) => (
            <div key={c.category} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2 font-medium text-slate-200">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: c.color }} />
                  <span>{c.category}</span>
                  <span className="text-[11px] text-slate-500 font-mono">({c.count} transactions)</span>
                </div>
                <div className="font-mono text-slate-300">
                  <b className="text-white">{formatCurrency(c.total_amount)}</b>
                  <span className="text-slate-500 text-[11px] ml-2 font-normal">({c.percentage}%)</span>
                </div>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div 
                  className="h-full rounded-full transition-all duration-500" 
                  style={{ width: `${Math.min(100, c.percentage)}%`, backgroundColor: c.color }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
