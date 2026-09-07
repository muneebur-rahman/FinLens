import React from 'react';
import { Repeat, Calendar, CheckCircle, AlertCircle, Sparkles } from 'lucide-react';
import { SubscriptionItem } from '../types';

interface SubscriptionsViewProps {
  subscriptions: SubscriptionItem[];
  recurringMonthlySpend: number;
}

const formatCurrency = (amt: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(amt);
};

export const SubscriptionsView: React.FC<SubscriptionsViewProps> = ({
  subscriptions,
  recurringMonthlySpend,
}) => {
  const hasSubs = subscriptions && subscriptions.length > 0;

  return (
    <div className="space-y-6 animate-fadeIn pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Repeat className="w-5 h-5 text-purple-400" />
            <span>Subscription & Recurring Leak Detector</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Detects recurring cadences, streaming subscriptions, utilities, and software services from your actual transactions.
          </p>
        </div>
      </div>

      {/* Top Banner KPI */}
      <div className="p-6 rounded-3xl bg-gradient-to-br from-purple-950/40 via-slate-900 to-slate-900 border border-purple-500/20 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-semibold text-purple-300 uppercase tracking-wider">
              Estimated Recurring Monthly Spend
            </span>
            <div className="text-3xl sm:text-4xl font-black text-white font-mono mt-1">
              {formatCurrency(recurringMonthlySpend)}
              <span className="text-sm text-slate-400 font-normal font-sans"> /month</span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Projected annual commitment: <b className="text-slate-200 font-mono">{formatCurrency(recurringMonthlySpend * 12)}</b>
            </p>
          </div>

          <div className="text-right">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/20 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" />
              <span>{subscriptions.length} Subscriptions Detected</span>
            </span>
          </div>
        </div>
      </div>

      {/* Subscription Cards or Empty State */}
      {!hasSubs ? (
        <div className="p-12 rounded-3xl bg-slate-900/40 border border-slate-800 text-center max-w-lg mx-auto">
          <div className="w-12 h-12 rounded-2xl bg-slate-800 flex items-center justify-center mx-auto mb-4 text-slate-400">
            <CheckCircle className="w-6 h-6 text-emerald-400" />
          </div>
          <h3 className="text-base font-bold text-white mb-2">
            No recurring subscriptions detected.
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Your uploaded statement does not contain any recurring monthly commitments, digital subscriptions, or membership charges. All outflows were variable or one-time transactions.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {subscriptions.map((sub, idx) => (
            <div
              key={idx}
              className="glass-card p-5 rounded-2xl border-slate-800 hover:border-purple-500/40 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-base font-bold text-white tracking-tight">
                    {sub.merchant}
                  </span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/20">
                    {sub.cadence}
                  </span>
                </div>

                <div className="text-2xl font-black text-purple-300 font-mono mb-2">
                  {formatCurrency(sub.average_amount)}
                  <span className="text-xs text-slate-400 font-normal font-sans"> /{sub.cadence === 'monthly' ? 'month' : sub.cadence}</span>
                </div>

                <p className="text-xs text-slate-400 mb-4 leading-relaxed">
                  {sub.detection_reason}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-500 font-mono">
                <span>Occurrences: <b className="text-slate-300">{sub.occurrences}</b></span>
                <span>Last charged: <b className="text-slate-300">{sub.last_date}</b></span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
