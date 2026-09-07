import React, { useState, useRef } from 'react';
import { 
  X, 
  Upload, 
  FileText, 
  FileSpreadsheet, 
  ShieldCheck, 
  Lock, 
  AlertCircle,
  PlayCircle
} from 'lucide-react';

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onFileSelected: (file: File) => void;
  onTryDemo: () => void;
  onSelectSample: (sampleKey: 'a' | 'b' | 'c') => void;
}

export const UploadModal: React.FC<UploadModalProps> = ({
  isOpen,
  onClose,
  onFileSelected,
  onTryDemo,
  onSelectSample,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const validateAndUpload = (file: File) => {
    setErrorMessage(null);
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext !== 'csv' && ext !== 'pdf') {
      setErrorMessage('Please upload a valid .pdf or .csv bank statement file.');
      return;
    }
    onFileSelected(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndUpload(e.target.files[0]);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      <div 
        className="relative w-full max-w-xl p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-700/80 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          id="close-upload-modal-btn"
          onClick={onClose}
          className="absolute top-6 right-6 p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="mb-6">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold mb-2">
            <Lock className="w-3 h-3" />
            <span>Privacy-First Processing</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Analyze Bank Statement
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Your uploaded statement is the absolute single source of truth.
          </p>
        </div>

        {/* Error notification if any */}
        {errorMessage && (
          <div className="mb-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Drag and Drop Zone */}
        <div
          id="dropzone-area"
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`relative cursor-pointer border-2 border-dashed rounded-2xl p-8 text-center transition-all ${
            isDragging 
              ? 'border-emerald-400 bg-emerald-500/10 scale-[1.01]' 
              : 'border-slate-700 hover:border-emerald-500/60 hover:bg-slate-800/40 bg-slate-950/40'
          }`}
        >
          <input
            id="statement-file-input"
            ref={fileInputRef}
            type="file"
            accept=".csv,.pdf"
            onChange={handleFileInputChange}
            className="hidden"
          />

          <div className="w-14 h-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mx-auto mb-4 text-emerald-400 group-hover:scale-110 transition-transform">
            <Upload className="w-7 h-7" />
          </div>

          <h3 className="text-base font-bold text-white mb-1">
            Drop your bank statement here
          </h3>
          <p className="text-xs text-slate-400 mb-4">
            or <span className="text-emerald-400 font-semibold underline underline-offset-2">browse files</span> on your computer
          </p>

          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-[11px] text-slate-400">
            <span>PDF or CSV</span>
            <span>•</span>
            <span>Secure processing</span>
            <span>•</span>
            <span>Privacy-first</span>
          </div>
        </div>

        {/* Verified Sample Statements Quick-Run */}
        <div className="mt-6 pt-6 border-t border-slate-800/80">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-300">Or test with verified sample statement:</span>
            <button
              id="upload-modal-demo-btn"
              onClick={onTryDemo}
              className="text-xs text-amber-400 hover:text-amber-300 font-medium flex items-center gap-1"
            >
              <PlayCircle className="w-3.5 h-3.5" />
              <span>Launch Demo Mode</span>
            </button>
          </div>

          <div className="grid grid-cols-3 gap-2">
            <button
              id="sample-stmt-a-btn"
              onClick={() => onSelectSample('a')}
              className="p-2.5 rounded-xl bg-slate-800/50 hover:bg-slate-800 border border-slate-700/60 hover:border-emerald-500/40 text-left transition-all"
            >
              <div className="text-[11px] font-bold text-slate-200">Statement A</div>
              <div className="text-[10px] text-slate-400 truncate">Tech Salary & Subs</div>
            </button>
            <button
              id="sample-stmt-b-btn"
              onClick={() => onSelectSample('b')}
              className="p-2.5 rounded-xl bg-slate-800/50 hover:bg-slate-800 border border-slate-700/60 hover:border-cyan-500/40 text-left transition-all"
            >
              <div className="text-[11px] font-bold text-slate-200">Statement B</div>
              <div className="text-[10px] text-slate-400 truncate">Freelancer (0 Subs)</div>
            </button>
            <button
              id="sample-stmt-c-btn"
              onClick={() => onSelectSample('c')}
              className="p-2.5 rounded-xl bg-slate-800/50 hover:bg-slate-800 border border-slate-700/60 hover:border-indigo-500/40 text-left transition-all"
            >
              <div className="text-[11px] font-bold text-slate-200">Statement C</div>
              <div className="text-[10px] text-slate-400 truncate">Minimalist (0 Anom)</div>
            </button>
          </div>
        </div>

        {/* Privacy Note */}
        <div className="mt-4 flex items-center justify-center gap-2 text-[11px] text-slate-500">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
          <span>Your financial data is yours. Ephemeral processing with 1-click permanent deletion.</span>
        </div>
      </div>
    </div>
  );
};
