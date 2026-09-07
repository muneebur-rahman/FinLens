import React from 'react';
import { ShieldAlert, AlertCircle, CheckCircle, Info, HelpCircle } from 'lucide-react';
import { AnomalyItem } from '../types';

interface AnomaliesViewProps {
  anomalies: AnomalyItem[];
}

const formatCurrency = (amt: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(amt);
};

export const AnomaliesView: React.FC<AnomaliesViewProps> = ({ anomalies }) => {
  const hasAnomalies = anomalies && anomalies.length > 0;

  return (
    <div className="space-y-6 animate-fadeIn pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            <span>Unusual Spending & Anomaly Alerts</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Behavioral outliers detected by evaluating transaction amounts and category medians from your statement baseline.
          </p>
        </div>
        <div className="text-xs font-mono text-slate-400">
          <b className="text-amber-400">{anomalies.length}</b> unusual outlier(s) flagged
        </div>
      </div>

      {/* Non-alarmist notice */}
      <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 flex items-start gap-3">
        <Info className="w-4 h-4 text-slate-400 flex-shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <b>Explainable AI Note:</b> An anomaly does NOT mean fraud or unauthorized activity. It signifies a transaction that deviates significantly in amount, category proportion, or frequency compared to the rest of your statement.
        </p>
      </div>

      {/* Anomalies List or Empty State */}
      {!hasAnomalies ? (
        <div className="p-12 rounded-3xl bg-slate-900/40 border border-slate-800 text-center max-w-lg mx-auto">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mx-auto mb-4 text-emerald-400">
            <CheckCircle className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-white mb-2">
            No unusual spending patterns detected.
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            All debit transactions in this statement align consistently with expected spending baselines, category medians, and transaction frequencies.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {anomalies.map((anom) => (
            <div
              key={anom.transaction_id}
              className="p-6 rounded-3xl bg-slate-900/80 border border-amber-500/30 shadow-lg space-y-4 hover:border-amber-500/50 transition-all"
            >
              {/* Header */}
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 uppercase tracking-wider font-mono">
                      Unusual Transaction
                    </span>
                    <span className="text-xs text-slate-400 font-mono">
                      {anom.date}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-white mt-1.5">
                    {anom.merchant}
                  </h3>
                  <span className="text-xs text-slate-400">
                    Category: <b className="text-slate-200">{anom.category}</b>
                  </span>
                </div>

                <div className="text-right font-mono">
                  <div className="text-2xl font-black text-amber-300">
                    {formatCurrency(anom.amount)}
                  </div>
                </div>
              </div>

              {/* Explainable AI Block */}
              <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-1.5">
                <div className="flex items-center gap-1.5 text-xs font-bold text-amber-400">
                  <HelpCircle className="w-3.5 h-3.5" />
                  <span>Why was this flagged?</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {anom.reason}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
