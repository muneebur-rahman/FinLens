import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  ArrowUpDown, 
  X, 
  Info, 
  AlertCircle, 
  ShieldCheck, 
  Repeat, 
  ArrowDownLeft, 
  ArrowUpRight,
  ReceiptText
} from 'lucide-react';
import { Transaction } from '../types';
import { fetchTransactions } from '../api';

interface TransactionsViewProps {
  sessionId: string;
}

const ALL_CATEGORIES = [
  'All',
  'Salary',
  'Freelance/Business Income',
  'Food & Dining',
  'Groceries',
  'Shopping',
  'Rent',
  'Utilities',
  'Transport',
  'Entertainment',
  'Healthcare',
  'Education',
  'Travel',
  'Investments',
  'Transfers',
  'Cash Withdrawal',
  'Other'
];

const formatCurrency = (amt: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(amt);
};

export const TransactionsView: React.FC<TransactionsViewProps> = ({ sessionId }) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedType, setSelectedType] = useState('All');
  const [sortBy, setSortBy] = useState('date');
  const [sortOrder, setSortOrder] = useState<'desc' | 'asc'>('desc');
  const [selectedTxn, setSelectedTxn] = useState<Transaction | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await fetchTransactions(sessionId, {
        search: search.trim() || undefined,
        category: selectedCategory,
        type: selectedType,
        sort_by: sortBy,
        sort_order: sortOrder,
      });
      setTransactions(res.transactions);
    } catch (err) {
      console.error('Failed to load transactions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [sessionId, search, selectedCategory, selectedType, sortBy, sortOrder]);

  const toggleSort = (col: string) => {
    if (sortBy === col) {
      setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc');
    } else {
      setSortBy(col);
      setSortOrder('desc');
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ReceiptText className="w-5 h-5 text-emerald-400" />
            <span>Transaction Ledger & Intelligence</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Every transaction extracted from your statement. Click any row to inspect categorization reasoning & flags.
          </p>
        </div>
        <div className="text-xs font-mono text-slate-400">
          Showing <b className="text-white">{transactions.length}</b> records
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col md:flex-row items-center gap-3">
        {/* Search Input */}
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            id="transaction-search-input"
            type="text"
            placeholder="Search merchant, narration, or keywords..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-slate-950/60 border border-slate-700/80 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
          />
          {search && (
            <button
              onClick={() => setSearch('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Category Dropdown */}
        <div className="w-full md:w-auto">
          <select
            id="transaction-category-filter"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="w-full px-3 py-2 bg-slate-950/60 border border-slate-700/80 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-emerald-500 cursor-pointer"
          >
            {ALL_CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {cat === 'All' ? 'All Categories' : cat}
              </option>
            ))}
          </select>
        </div>

        {/* Type Filter */}
        <div className="flex items-center gap-1 bg-slate-950/60 p-1 rounded-xl border border-slate-700/80 w-full md:w-auto">
          {['All', 'Debit', 'Credit'].map((t) => (
            <button
              key={t}
              onClick={() => setSelectedType(t)}
              className={`flex-1 md:flex-none px-3 py-1 rounded-lg text-xs font-medium transition-colors ${
                selectedType === t 
                  ? 'bg-slate-800 text-white shadow-sm font-semibold' 
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Transactions Table */}
      <div className="rounded-2xl border border-slate-800 overflow-hidden bg-slate-900/40 shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-900/90 border-b border-slate-800 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                <th 
                  className="py-3 px-4 cursor-pointer hover:text-slate-200"
                  onClick={() => toggleSort('date')}
                >
                  <div className="flex items-center gap-1">
                    <span>Date</span>
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th 
                  className="py-3 px-4 cursor-pointer hover:text-slate-200"
                  onClick={() => toggleSort('merchant')}
                >
                  <div className="flex items-center gap-1">
                    <span>Merchant / Cleaned</span>
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="py-3 px-4 hidden md:table-cell">Raw Narration</th>
                <th 
                  className="py-3 px-4 cursor-pointer hover:text-slate-200"
                  onClick={() => toggleSort('category')}
                >
                  <div className="flex items-center gap-1">
                    <span>Category</span>
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="py-3 px-4 text-center">Flags</th>
                <th 
                  className="py-3 px-4 text-right cursor-pointer hover:text-slate-200"
                  onClick={() => toggleSort('amount')}
                >
                  <div className="flex items-center justify-end gap-1">
                    <span>Amount</span>
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-500">
                    Loading statement transactions...
                  </td>
                </tr>
              ) : transactions.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-500">
                    No transactions match your search or filters.
                  </td>
                </tr>
              ) : (
                transactions.map((t) => {
                  const isDebit = t.type === 'debit';
                  return (
                    <tr
                      key={t.id}
                      id={`txn-row-${t.id}`}
                      onClick={() => setSelectedTxn(t)}
                      className="hover:bg-slate-800/40 cursor-pointer transition-colors group"
                    >
                      <td className="py-3 px-4 font-mono text-slate-400 whitespace-nowrap">
                        {t.date}
                      </td>

                      <td className="py-3 px-4 font-semibold text-white group-hover:text-emerald-300 transition-colors whitespace-nowrap">
                        {t.merchant}
                      </td>

                      <td className="py-3 px-4 text-slate-400 max-w-xs truncate hidden md:table-cell font-mono text-[11px]">
                        {t.raw_description}
                      </td>

                      <td className="py-3 px-4 whitespace-nowrap">
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-slate-800 text-slate-200 border border-slate-700/60">
                          {t.category}
                        </span>
                      </td>

                      <td className="py-3 px-4 whitespace-nowrap text-center">
                        <div className="flex items-center justify-center gap-1.5">
                          {t.is_recurring && (
                            <span 
                              className="p-1 rounded bg-purple-500/10 text-purple-400"
                              title="Recurring subscription detected"
                            >
                              <Repeat className="w-3 h-3" />
                            </span>
                          )}
                          {t.is_anomaly && (
                            <span 
                              className="p-1 rounded bg-amber-500/10 text-amber-400"
                              title="Unusual transaction outlier flagged"
                            >
                              <AlertCircle className="w-3 h-3" />
                            </span>
                          )}
                          {t.is_tax_relevant && (
                            <span 
                              className="p-1 rounded bg-cyan-500/10 text-cyan-400"
                              title={`Tax-relevant (${t.tax_category})`}
                            >
                              <ShieldCheck className="w-3 h-3" />
                            </span>
                          )}
                        </div>
                      </td>

                      <td className="py-3 px-4 text-right font-mono font-bold whitespace-nowrap">
                        <span className={isDebit ? 'text-rose-400' : 'text-emerald-400'}>
                          {isDebit ? '-' : '+'} {formatCurrency(t.amount)}
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Transaction Detail Slide-Over Drawer */}
      {selectedTxn && (
        <div className="fixed inset-0 z-50 flex items-center justify-end bg-slate-950/70 backdrop-blur-sm animate-fadeIn">
          <div 
            className="w-full max-w-md h-full bg-slate-900 border-l border-slate-800 p-6 overflow-y-auto shadow-2xl flex flex-col justify-between"
            onClick={(e) => e.stopPropagation()}
          >
            <div>
              {/* Drawer Header */}
              <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-6">
                <div>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono">
                    {selectedTxn.id}
                  </span>
                  <h3 className="text-xl font-bold text-white mt-1">
                    {selectedTxn.merchant}
                  </h3>
                </div>
                <button
                  id="close-txn-drawer-btn"
                  onClick={() => setSelectedTxn(null)}
                  className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Amount and Direction */}
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 mb-6">
                <span className="text-xs text-slate-500">Transaction Amount</span>
                <div className={`text-3xl font-black font-mono mt-0.5 ${
                  selectedTxn.type === 'debit' ? 'text-rose-400' : 'text-emerald-400'
                }`}>
                  {selectedTxn.type === 'debit' ? '-' : '+'} {formatCurrency(selectedTxn.amount)}
                </div>
                <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-800/80 text-xs text-slate-400">
                  <span>Date: <b className="text-slate-200">{selectedTxn.date}</b></span>
                  <span>Type: <b className="uppercase text-slate-200">{selectedTxn.type}</b></span>
                </div>
              </div>

              {/* Raw Bank Narration */}
              <div className="mb-6">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Original Raw Narration
                </h4>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 text-xs font-mono text-slate-300 break-words">
                  {selectedTxn.raw_description}
                </div>
              </div>

              {/* Explainable AI: Why Categorized This Way */}
              <div className="mb-6 p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400" />
                  <h4 className="text-xs font-bold text-emerald-300 uppercase tracking-wider">
                    Why FinLens Categorized This As {selectedTxn.category}
                  </h4>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {selectedTxn.category_reason || 'Categorized automatically based on merchant signatures and keywords.'}
                </p>
                <div className="mt-2 text-[11px] text-emerald-400/80 font-mono">
                  Confidence score: {(selectedTxn.confidence * 100).toFixed(0)}%
                </div>
              </div>

              {/* Explainable AI: Anomaly Reason if flagged */}
              {selectedTxn.is_anomaly && (
                <div className="mb-6 p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertCircle className="w-4 h-4 text-amber-400" />
                    <h4 className="text-xs font-bold text-amber-300 uppercase tracking-wider">
                      Why This Transaction Was Flagged
                    </h4>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {selectedTxn.anomaly_reason}
                  </p>
                  <p className="text-[11px] text-slate-400 mt-2 italic">
                    Note: FinLens flags unusual spending patterns relative to your personal statement baseline, not fraud.
                  </p>
                </div>
              )}

              {/* Explainable AI: Tax Relevance */}
              {selectedTxn.is_tax_relevant && (
                <div className="mb-6 p-4 rounded-2xl bg-cyan-500/10 border border-cyan-500/30">
                  <div className="flex items-center gap-2 mb-2">
                    <ShieldCheck className="w-4 h-4 text-cyan-400" />
                    <h4 className="text-xs font-bold text-cyan-300 uppercase tracking-wider">
                      Tax Relevance ({selectedTxn.tax_category})
                    </h4>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {selectedTxn.tax_reason}
                  </p>
                </div>
              )}

              {/* Recurring Status */}
              {selectedTxn.is_recurring && (
                <div className="p-4 rounded-2xl bg-purple-500/10 border border-purple-500/30">
                  <div className="flex items-center gap-2 mb-1">
                    <Repeat className="w-4 h-4 text-purple-400" />
                    <h4 className="text-xs font-bold text-purple-300 uppercase tracking-wider">
                      Recurring Subscription
                    </h4>
                  </div>
                  <p className="text-xs text-slate-300">
                    Recurring {selectedTxn.recurring_cadence || 'monthly'} pattern detected for {selectedTxn.merchant}.
                  </p>
                </div>
              )}
            </div>

            <div className="pt-6 border-t border-slate-800">
              <button
                onClick={() => setSelectedTxn(null)}
                className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition-colors"
              >
                Close Details
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
