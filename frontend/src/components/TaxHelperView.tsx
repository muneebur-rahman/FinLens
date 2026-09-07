import React from 'react';
import { ShieldCheck, AlertCircle, FileText, CheckCircle2, Info } from 'lucide-react';
import { TaxSummary } from '../types';

interface TaxHelperViewProps {
  taxSummary: TaxSummary;
}

const formatCurrency = (amt: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(amt);
};

export const TaxHelperView: React.FC<TaxHelperViewProps> = ({ taxSummary }) => {
  const { total_tax_relevant, by_section, items, disclaimer } = taxSummary;
  const hasItems = items && items.length > 0;

  return (
    <div className="space-y-6 animate-fadeIn pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
            <span>Tax Helper & Deduction Finder</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Identifies transactions potentially eligible for income tax deductions under the Indian Income Tax Act.
          </p>
        </div>
      </div>

      {/* Mandatory Regulatory Disclaimer Box */}
      <div className="p-4 rounded-2xl bg-cyan-950/20 border border-cyan-500/30 text-xs text-cyan-200/90 flex items-start gap-3">
        <Info className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-cyan-300">Important Disclaimer: </span>
          {disclaimer}
        </div>
      </div>

      {/* Top Banner KPI */}
      <div className="p-6 rounded-3xl bg-gradient-to-br from-cyan-950/40 via-slate-900 to-slate-900 border border-cyan-500/20 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-semibold text-cyan-300 uppercase tracking-wider">
              Total Potential Tax-Relevant Outflows
            </span>
            <div className="text-3xl sm:text-4xl font-black text-white font-mono mt-1">
              {formatCurrency(total_tax_relevant)}
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Aggregated across <b className="text-slate-200">{items.length}</b> verified tax-relevant transactions.
            </p>
          </div>

          {/* Section Badges */}
          <div className="flex flex-wrap items-center gap-2">
            {Object.entries(by_section).map(([sec, amt]) => (
              <div
                key={sec}
                className="px-3 py-1.5 rounded-xl bg-slate-800/80 border border-slate-700 text-xs font-mono"
              >
                <span className="text-cyan-400 font-semibold">{sec}: </span>
                <span className="text-white font-bold">{formatCurrency(amt)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Itemized Tax Transactions */}
      <div>
        <h3 className="text-sm font-bold text-white mb-4">
          Potential Tax-Relevant Transactions
        </h3>

        {!hasItems ? (
          <div className="p-12 rounded-3xl bg-slate-900/40 border border-slate-800 text-center max-w-lg mx-auto">
            <CheckCircle2 className="w-8 h-8 text-slate-500 mx-auto mb-3" />
            <h4 className="text-sm font-bold text-white mb-1">
              No tax-relevant items detected
            </h4>
            <p className="text-xs text-slate-400">
              This statement did not contain transactions typically eligible for 80C, 80D, 80G or HRA deductions.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {items.map((item, idx) => (
              <div
                key={idx}
                className="glass-card p-5 rounded-2xl border-slate-800 hover:border-cyan-500/40 transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-white font-mono">
                      {item.date}
                    </span>
                    <span className="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 font-mono">
                      Section {item.tax_section}
                    </span>
                  </div>

                  <h4 className="text-base font-bold text-white mb-1">
                    {item.merchant}
                  </h4>
                  <div className="text-xs text-slate-400 mb-3">
                    {item.tax_category}
                  </div>

                  <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300">
                    <span className="text-cyan-400 font-semibold">Reason: </span>
                    {item.reason}
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
                  <span className="text-xs text-slate-500">Claimable Outflow</span>
                  <span className="text-base font-bold font-mono text-cyan-300">
                    {formatCurrency(item.amount)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
