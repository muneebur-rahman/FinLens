import React, { useState } from 'react';
import { Settings, ShieldCheck, Trash2, FileText, Lock, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { DashboardData } from '../types';

interface SettingsViewProps {
  data: DashboardData;
  onPurgeData: () => void;
}

export const SettingsView: React.FC<SettingsViewProps> = ({ data, onPurgeData }) => {
  const [confirmDelete, setConfirmDelete] = useState(false);

  return (
    <div className="space-y-6 animate-fadeIn max-w-3xl pb-16">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Settings className="w-5 h-5 text-slate-400" />
          <span>Statement & Privacy Settings</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Review active statement metadata and manage privacy controls.
        </p>
      </div>

      {/* Privacy Pledge Card */}
      <div className="p-6 rounded-3xl bg-emerald-950/20 border border-emerald-500/20 shadow-lg space-y-3">
        <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
          <Lock className="w-4 h-4" />
          <span>Your financial data is yours.</span>
        </div>
        <p className="text-xs text-slate-300 leading-relaxed">
          FinLens is built with an ephemeral, privacy-first architecture. Statement data is processed locally and in your isolated session. We do not sell, share, or train general AI models on your personal financial statements.
        </p>
        <div className="flex items-center gap-4 text-[11px] text-emerald-400/90 pt-2 font-medium">
          <span className="flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Encrypted local session</span>
          </span>
          <span className="flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Instant permanent data purge</span>
          </span>
        </div>
      </div>

      {/* Statement Metadata Details */}
      <div className="rounded-3xl bg-slate-900 border border-slate-800 p-6 space-y-4">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <FileText className="w-4 h-4 text-cyan-400" />
          <span>Active Statement Details</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono">
          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
            <span className="text-slate-500 block text-[10px] uppercase font-sans">Filename</span>
            <span className="text-white font-semibold">{data.filename}</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
            <span className="text-slate-500 block text-[10px] uppercase font-sans">Session ID</span>
            <span className="text-slate-300 truncate block">{data.session_id}</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
            <span className="text-slate-500 block text-[10px] uppercase font-sans">Statement Window</span>
            <span className="text-white font-semibold">
              {data.date_start || 'N/A'} → {data.date_end || 'N/A'}
            </span>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
            <span className="text-slate-500 block text-[10px] uppercase font-sans">Transactions Parsed</span>
            <span className="text-white font-semibold">{data.transaction_count} items</span>
          </div>
        </div>
      </div>

      {/* Danger Zone: Permanent Purge */}
      <div className="rounded-3xl border border-rose-500/30 bg-rose-950/10 p-6 space-y-4">
        <div className="flex items-center gap-2 text-rose-400 font-bold text-sm">
          <AlertTriangle className="w-4 h-4" />
          <span>Data Deletion & Privacy Control</span>
        </div>
        <p className="text-xs text-slate-300 leading-relaxed">
          Permanently delete this statement, all parsed transactions, detected subscriptions, anomalies, and insights from the database. This action cannot be undone.
        </p>

        {confirmDelete ? (
          <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-500/40 space-y-3 animate-fadeIn">
            <p className="text-xs font-semibold text-rose-300">
              Are you sure you want to permanently delete all data for "{data.filename}"?
            </p>
            <div className="flex items-center gap-3">
              <button
                id="confirm-purge-btn"
                onClick={onPurgeData}
                className="px-4 py-2 rounded-xl bg-rose-500 hover:bg-rose-600 text-xs font-bold text-white transition-colors"
              >
                Yes, Delete Everything Now
              </button>
              <button
                onClick={() => setConfirmDelete(false)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <button
            id="initial-purge-btn"
            onClick={() => setConfirmDelete(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-bold transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            <span>Delete Statement Data</span>
          </button>
        )}
      </div>
    </div>
  );
};
