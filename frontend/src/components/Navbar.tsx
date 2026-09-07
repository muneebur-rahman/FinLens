import React from 'react';
import { 
  Compass, 
  ReceiptText, 
  PieChart, 
  Repeat, 
  AlertTriangle, 
  ShieldCheck, 
  Bot, 
  Settings, 
  Upload, 
  Trash2, 
  Sparkles 
} from 'lucide-react';
import { NavView } from '../types';

interface NavbarProps {
  currentView: NavView;
  onViewChange: (view: NavView) => void;
  onOpenUpload: () => void;
  onOpenAssistant: () => void;
  onDeleteSession: () => void;
  isDemo: boolean;
  hasSession: boolean;
  filename?: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentView,
  onViewChange,
  onOpenUpload,
  onOpenAssistant,
  onDeleteSession,
  isDemo,
  hasSession,
  filename,
}) => {
  const navItems: { id: NavView; label: string; icon: React.ReactNode }[] = [
    { id: 'overview', label: 'Overview', icon: <Compass className="w-4 h-4" /> },
    { id: 'transactions', label: 'Transactions', icon: <ReceiptText className="w-4 h-4" /> },
    { id: 'spending', label: 'Spending', icon: <PieChart className="w-4 h-4" /> },
    { id: 'subscriptions', label: 'Subscriptions', icon: <Repeat className="w-4 h-4" /> },
    { id: 'anomalies', label: 'Alerts', icon: <AlertTriangle className="w-4 h-4" /> },
    { id: 'tax', label: 'Tax Helper', icon: <ShieldCheck className="w-4 h-4" /> },
    { id: 'assistant', label: 'AI Assistant', icon: <Bot className="w-4 h-4" /> },
    { id: 'settings', label: 'Settings', icon: <Settings className="w-4 h-4" /> },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo & Tagline */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => hasSession ? onViewChange('overview') : undefined}>
            <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400/20 to-teal-500/10 border border-emerald-500/30 glow-emerald">
              <Sparkles className="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                  FinLens
                </span>
                {hasSession && (
                  <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full border ${
                    isDemo 
                      ? 'bg-amber-500/10 text-amber-300 border-amber-500/30' 
                      : 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
                  }`}>
                    {isDemo ? 'Demo Mode' : 'Real Statement'}
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                The quiet clarity your money deserves.
              </p>
            </div>
          </div>

          {/* Nav Items (Visible when session is active) */}
          {hasSession && (
            <nav className="hidden md:flex items-center gap-1 bg-slate-900/60 p-1 rounded-xl border border-slate-800">
              {navItems.map((item) => {
                const isActive = currentView === item.id;
                return (
                  <button
                    key={item.id}
                    id={`nav-${item.id}`}
                    onClick={() => onViewChange(item.id)}
                    className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg transition-all ${
                      isActive
                        ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 shadow-sm'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                    }`}
                  >
                    {item.icon}
                    {item.label}
                  </button>
                );
              })}
            </nav>
          )}

          {/* Action Buttons */}
          <div className="flex items-center gap-2">
            {hasSession && (
              <>
                <button
                  id="open-assistant-btn"
                  onClick={onOpenAssistant}
                  className="relative flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800/80 hover:bg-slate-700/80 text-cyan-300 border border-cyan-500/30 transition-colors shadow-sm"
                  title="Ask FinLens Assistant"
                >
                  <Bot className="w-3.5 h-3.5 text-cyan-400" />
                  <span className="hidden sm:inline">Ask AI</span>
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                </button>

                <button
                  id="delete-session-btn"
                  onClick={onDeleteSession}
                  className="p-2 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors border border-transparent hover:border-rose-500/20"
                  title="Delete statement and clear all data (Privacy purge)"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </>
            )}

            <button
              id="upload-new-btn"
              onClick={onOpenUpload}
              className="flex items-center gap-2 px-3.5 py-1.5 text-xs font-semibold rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 shadow-md shadow-emerald-500/20 transition-all active:scale-95"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>{hasSession ? 'Upload New' : 'Analyze Statement'}</span>
            </button>
          </div>
        </div>

        {/* Mobile Navigation bar */}
        {hasSession && (
          <div className="md:hidden flex items-center gap-1 overflow-x-auto py-2 border-t border-slate-800/60 scrollbar-none">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onViewChange(item.id)}
                className={`flex items-center gap-1 px-2.5 py-1 text-[11px] font-medium rounded-md whitespace-nowrap transition-colors ${
                  currentView === item.id
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {item.icon}
                {item.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </header>
  );
};
