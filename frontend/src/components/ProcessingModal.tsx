import React, { useEffect, useState } from 'react';
import { 
  CheckCircle2, 
  Loader2, 
  Sparkles, 
  BrainCircuit, 
  Layers, 
  Repeat, 
  AlertTriangle, 
  HeartHandshake, 
  Receipt 
} from 'lucide-react';

interface ProcessingModalProps {
  isOpen: boolean;
  filename: string;
  onComplete: () => void;
}

const STAGES = [
  { id: 1, title: 'Extracting transactions', icon: <Receipt className="w-4 h-4" /> },
  { id: 2, title: 'Cleaning transaction data', icon: <BrainCircuit className="w-4 h-4" /> },
  { id: 3, title: 'Understanding merchants', icon: <Sparkles className="w-4 h-4" /> },
  { id: 4, title: 'Categorizing spending', icon: <Layers className="w-4 h-4" /> },
  { id: 5, title: 'Detecting recurring payments', icon: <Repeat className="w-4 h-4" /> },
  { id: 6, title: 'Checking unusual activity', icon: <AlertTriangle className="w-4 h-4" /> },
  { id: 7, title: 'Calculating financial health', icon: <HeartHandshake className="w-4 h-4" /> },
  { id: 8, title: 'Finding tax-relevant transactions', icon: <CheckCircle2 className="w-4 h-4" /> },
];

export const ProcessingModal: React.FC<ProcessingModalProps> = ({
  isOpen,
  filename,
  onComplete,
}) => {
  const [completedStages, setCompletedStages] = useState<number[]>([]);
  const [currentStage, setCurrentStage] = useState<number>(1);

  useEffect(() => {
    if (!isOpen) {
      setCompletedStages([]);
      setCurrentStage(1);
      return;
    }

    let current = 1;
    // Sequential stage stepping (approx 250ms per stage = ~2.2s total smooth experience)
    const interval = setInterval(() => {
      setCompletedStages((prev) => [...prev, current]);
      current += 1;
      setCurrentStage(current);

      if (current > STAGES.length) {
        clearInterval(interval);
        setTimeout(() => {
          onComplete();
        }, 350);
      }
    }, 240);

    return () => clearInterval(interval);
  }, [isOpen, onComplete]);

  if (!isOpen) return null;

  const progressPercent = Math.min(100, Math.round((completedStages.length / STAGES.length) * 100));

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-lg animate-fadeIn">
      <div className="w-full max-w-md p-8 rounded-3xl bg-slate-900 border border-slate-700/80 shadow-2xl text-center">
        {/* Animated Visual Header */}
        <div className="relative w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center mx-auto mb-5 glow-emerald">
          <Loader2 className="w-8 h-8 text-emerald-400 animate-spin" />
          <div className="absolute inset-0 rounded-2xl bg-emerald-500/10 animate-ping opacity-25" />
        </div>

        <h3 className="text-xl font-extrabold text-white tracking-tight mb-1">
          Reading your statement...
        </h3>
        <p className="text-xs text-slate-400 font-mono truncate max-w-xs mx-auto mb-6">
          {filename}
        </p>

        {/* Progress Bar */}
        <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden mb-6">
          <div 
            className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 transition-all duration-300 rounded-full"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* Sequential Stages List */}
        <div className="space-y-2.5 text-left mb-6">
          {STAGES.map((stage) => {
            const isFinished = completedStages.includes(stage.id);
            const isCurrent = currentStage === stage.id;

            return (
              <div
                key={stage.id}
                className={`flex items-center justify-between p-2 rounded-xl transition-all ${
                  isFinished
                    ? 'bg-slate-800/40 text-slate-200'
                    : isCurrent
                    ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-300'
                    : 'text-slate-500'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <span className={isFinished ? 'text-emerald-400' : isCurrent ? 'text-emerald-300' : 'text-slate-600'}>
                    {stage.icon}
                  </span>
                  <span className={`text-xs font-medium ${isFinished ? 'text-slate-200' : isCurrent ? 'text-white font-semibold' : 'text-slate-500'}`}>
                    {stage.title}
                  </span>
                </div>

                <div>
                  {isFinished ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  ) : isCurrent ? (
                    <Loader2 className="w-3.5 h-3.5 text-emerald-400 animate-spin" />
                  ) : (
                    <span className="w-2 h-2 rounded-full bg-slate-700 inline-block" />
                  )}
                </div>
              </div>
            );
          })}
        </div>

        <div className="text-[11px] text-slate-500">
          Calculating exact figures from statement source data...
        </div>
      </div>
    </div>
  );
};
