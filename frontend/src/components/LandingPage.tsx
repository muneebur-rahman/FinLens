import React from 'react';
import { 
  ArrowRight, 
  Sparkles, 
  Shield, 
  Lock, 
  TrendingUp, 
  FileSpreadsheet, 
  FileText, 
  Layers, 
  Repeat, 
  AlertCircle, 
  Award, 
  Calculator, 
  PlayCircle,
  CheckCircle2
} from 'lucide-react';

interface LandingPageProps {
  onOpenUpload: () => void;
  onLoadDemo: () => void;
  onLoadSample: (sampleKey: 'a' | 'b' | 'c') => void;
  isLoading: boolean;
}

export const LandingPage: React.FC<LandingPageProps> = ({
  onOpenUpload,
  onLoadDemo,
  onLoadSample,
  isLoading,
}) => {
  return (
    <div className="relative overflow-hidden min-h-[calc(100vh-4rem)]">
      {/* Subtle Background glow orbs */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[650px] h-[650px] bg-emerald-500/10 rounded-full blur-[140px] pointer-events-none -z-10" />
      <div className="absolute top-1/3 right-10 w-[450px] h-[450px] bg-cyan-500/10 rounded-full blur-[120px] pointer-events-none -z-10" />

      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-4 pt-16 pb-20 text-center">
        {/* Brand Tag Pill */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900/80 border border-slate-700/80 text-xs text-emerald-400 font-medium mb-6 shadow-inner">
          <Sparkles className="w-3.5 h-3.5" />
          <span>The quiet clarity your money deserves</span>
        </div>

        {/* Main Headline */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-[1.1] mb-6">
          Understand your money.{' '}
          <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
            Before it disappears.
          </span>
        </h1>

        {/* Supporting text */}
        <p className="text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto mb-10 leading-relaxed font-normal">
          Upload your bank statement and let FinLens turn thousands of messy transactions into clear, actionable financial intelligence.
        </p>

        {/* Action CTAs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-14">
          <button
            id="landing-analyze-btn"
            onClick={onOpenUpload}
            disabled={isLoading}
            className="w-full sm:w-auto px-8 py-4 rounded-xl text-base font-bold bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 shadow-xl shadow-emerald-500/25 flex items-center justify-center gap-2 transition-all hover:scale-[1.02] active:scale-[0.98]"
          >
            <span>Analyze My Statement</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            id="landing-demo-btn"
            onClick={onLoadDemo}
            disabled={isLoading}
            className="w-full sm:w-auto px-8 py-4 rounded-xl text-base font-semibold bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-700/80 hover:border-slate-600 transition-all flex items-center justify-center gap-2 shadow-sm"
          >
            <PlayCircle className="w-4 h-4 text-amber-400" />
            <span>Try Demo</span>
          </button>
        </div>

        {/* Privacy & Trust Badge */}
        <div className="inline-flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 mb-16">
          <div className="flex items-center gap-1.5 text-emerald-400 font-medium">
            <Lock className="w-3.5 h-3.5" />
            <span>Privacy-First</span>
          </div>
          <span className="text-slate-600">•</span>
          <span>PDF or CSV</span>
          <span className="text-slate-600">•</span>
          <span>Your statement is the single source of truth</span>
        </div>

        {/* Quick Sample Statements Runner */}
        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 max-w-3xl mx-auto mb-20 text-left">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-white">Instant Test Statements</h3>
              <p className="text-xs text-slate-400">Want to test without downloading files? Run a verified sample instantly:</p>
            </div>
            <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-bold">
              3 Profiles
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <button
              onClick={() => onLoadSample('a')}
              disabled={isLoading}
              className="p-3.5 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 hover:border-emerald-500/40 transition-all group text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold text-white group-hover:text-emerald-400">Statement A</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">Corporate</span>
              </div>
              <p className="text-[11px] text-slate-400">Salary, Rent, Netflix, Spotify, Croma Anomaly & 80C Tax</p>
            </button>

            <button
              onClick={() => onLoadSample('b')}
              disabled={isLoading}
              className="p-3.5 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 hover:border-cyan-500/40 transition-all group text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold text-white group-hover:text-cyan-400">Statement B</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300">Freelancer</span>
              </div>
              <p className="text-[11px] text-slate-400">Client Retainer, Upwork, Zero Subscriptions, Phone Repair</p>
            </button>

            <button
              onClick={() => onLoadSample('c')}
              disabled={isLoading}
              className="p-3.5 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 hover:border-indigo-500/40 transition-all group text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold text-white group-hover:text-indigo-400">Statement C</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300">Minimalist</span>
              </div>
              <p className="text-[11px] text-slate-400">Utilities, Supermarket, Zero recurring leaks, Zero anomalies</p>
            </button>
          </div>
        </div>

        {/* 5 Core Value Pillars */}
        <div className="text-left mb-16">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-3">
              Intelligent Financial Architecture
            </h2>
            <p className="text-sm text-slate-400 max-w-xl mx-auto">
              FinLens parses the messy transaction strings from your bank and extracts pure financial intelligence.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Auto-Categorization */}
            <div className="glass-card p-6 rounded-2xl transition-all">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-4">
                <Layers className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">Auto-Categorization</h3>
              <p className="text-xs text-slate-300 leading-relaxed mb-4">
                Automatically understands where money is going across 16 categories with explainability reasons.
              </p>
              <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-mono text-slate-400">
                <div className="text-slate-500 line-through">UPI/5012/SWIGGY-BANGALORE</div>
                <div className="text-emerald-400 font-sans font-semibold mt-1">✓ Swiggy • Food & Dining (96% conf)</div>
              </div>
            </div>

            {/* Subscription Detection */}
            <div className="glass-card p-6 rounded-2xl transition-all">
              <div className="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400 mb-4">
                <Repeat className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">Subscription Detection</h3>
              <p className="text-xs text-slate-300 leading-relaxed mb-4">
                Find recurring payments, digital subscriptions, and hidden monthly leaks automatically from cadence and amount similarity.
              </p>
              <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-mono text-slate-400">
                <div className="text-slate-200 font-sans font-semibold">Netflix: ₹649/month</div>
                <div className="text-rose-400 mt-0.5">Recurring monthly cadence detected</div>
              </div>
            </div>

            {/* Anomaly Detection */}
            <div className="glass-card p-6 rounded-2xl transition-all">
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 mb-4">
                <AlertCircle className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">Anomaly Detection</h3>
              <p className="text-xs text-slate-300 leading-relaxed mb-4">
                Identifies transactions that don't match your baseline without alarmism. Always includes *Why was this flagged?*.
              </p>
              <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-mono text-slate-400">
                <div className="text-amber-300 font-sans font-semibold">Unusual transaction: ₹74,990</div>
                <div className="text-slate-400 mt-0.5">3.8x higher than typical Shopping median</div>
              </div>
            </div>

            {/* Financial Health */}
            <div className="glass-card p-6 rounded-2xl transition-all">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4">
                <Award className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">Financial Health Score</h3>
              <p className="text-xs text-slate-300 leading-relaxed mb-4">
                Turns spending, income and savings behavior into an understandable 0-100 score with transparent drivers.
              </p>
              <div className="flex items-center gap-3 p-3 rounded-lg bg-slate-900/80 border border-slate-800">
                <div className="text-2xl font-black text-emerald-400">78<span className="text-xs text-slate-400 font-normal">/100</span></div>
                <div className="text-[11px] text-slate-400">Positive savings cushion & controlled overhead</div>
              </div>
            </div>

            {/* Tax Helper */}
            <div className="glass-card p-6 rounded-2xl transition-all">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 mb-4">
                <Calculator className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">Tax Helper</h3>
              <p className="text-xs text-slate-300 leading-relaxed mb-4">
                Identify potentially tax-relevant transactions like House Rent (HRA/80GG), ELSS/NPS (80C), Mediclaim (80D), and donations.
              </p>
              <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-mono text-slate-400">
                <div className="text-cyan-300 font-sans font-semibold">Section 80C: ₹15,000</div>
                <div className="text-slate-400 mt-0.5">ELSS Tax Saver Fund Identified</div>
              </div>
            </div>

            {/* AI Assistant */}
            <div className="glass-card p-6 rounded-2xl transition-all">
              <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-4">
                <Sparkles className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">AI Assistant</h3>
              <p className="text-xs text-slate-300 leading-relaxed mb-4">
                Ask questions about your finances in plain English. Answers are strictly calculated from your statement dataset.
              </p>
              <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-mono text-slate-400">
                <div className="text-slate-300 font-sans italic">"How much did I spend on food?"</div>
                <div className="text-emerald-400 mt-1 font-sans font-medium">₹5,410 across 8 transactions</div>
              </div>
            </div>
          </div>
        </div>

        {/* Final CTA Banner */}
        <div className="p-8 sm:p-12 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-emerald-950/40 border border-emerald-500/20 text-center max-w-4xl mx-auto shadow-2xl">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white mb-4">
            Ready to clarify your finances?
          </h2>
          <p className="text-sm text-slate-300 max-w-xl mx-auto mb-8">
            Upload your statement now. No account creation required. Instant analysis in under 3 seconds.
          </p>
          <button
            onClick={onOpenUpload}
            className="px-8 py-3.5 rounded-xl text-sm font-bold bg-emerald-400 hover:bg-emerald-300 text-slate-950 transition-all shadow-lg shadow-emerald-400/20 inline-flex items-center gap-2"
          >
            <span>Analyze Bank Statement</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
