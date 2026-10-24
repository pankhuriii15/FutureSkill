import React, { useState } from 'react';
import { Key, ShieldCheck, Cpu, Info, Check, X, AlertTriangle, ExternalLink } from 'lucide-react';

export default function ApiConfigModal({ isOpen, onClose, apiKey, onSaveKey, healthData }) {
  const [keyInput, setKeyInput] = useState(apiKey || '');
  const [isSaved, setIsSaved] = useState(false);

  if (!isOpen) return null;

  const handleSave = () => {
    onSaveKey(keyInput.trim());
    setIsSaved(true);
    setTimeout(() => {
      setIsSaved(false);
      onClose();
    }, 1200);
  };

  const handleClear = () => {
    setKeyInput('');
    onSaveKey('');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md">
      <div className="w-full max-w-xl glass-panel-amber p-6 rounded-2xl relative shadow-2xl">
        {/* Close Button */}
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-2 rounded-lg bg-slate-800/50 hover:bg-slate-700/60 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-3 mb-5">
          <div className="p-3 rounded-xl bg-amber-500/15 border border-amber-500/30 text-amber-400">
            <Key className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">AI Engine & Gemini API Configuration</h2>
            <p className="text-xs text-slate-400">Manage LLM connectivity with seamless intelligent demonstration fallback</p>
          </div>
        </div>

        {/* Status indicator */}
        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-700/60 mb-5 flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span className="text-slate-300 font-medium">Multimodal AI Engine:</span>
          </div>
          <span className={`pill ${apiKey ? 'pill-compliant' : 'pill-moderate'}`}>
            {apiKey ? 'Active (Gemini 1.5 Flash)' : 'Autonomous Demo Mode Active'}
          </span>
        </div>

        {/* Input Field */}
        <div className="space-y-2 mb-4">
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Google Gemini API Key
          </label>
          <div className="relative">
            <input
              type="password"
              value={keyInput}
              onChange={(e) => setKeyInput(e.target.value)}
              placeholder="AIzaSy..."
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-amber-500 font-mono"
            />
          </div>
          <p className="text-[11px] text-slate-400 flex items-center gap-1.5 mt-1">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 inline" />
            Keys are retained locally in client storage and forwarded exclusively to Google Generative Language API.
          </p>
        </div>

        {/* Fallback Explanation Box */}
        <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-200/90 mb-5 leading-relaxed">
          <div className="flex items-center gap-1.5 font-semibold text-amber-400 mb-1">
            <Info className="w-4 h-4" />
            <span>Turnkey Autonomous Fallback</span>
          </div>
          If no API key is supplied, the platform automatically activates high-fidelity domain demonstration intelligence adhering to IS 456:2000 and OSHA 1926 standards.
        </div>

        {/* Architecture Badges */}
        <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-400 mb-6 bg-slate-900/50 p-3 rounded-xl border border-slate-800">
          <div><strong className="text-slate-200">Platform ID:</strong> {healthData?.platform_id || '6ac4c98d1dcde6d7857c1642'}</div>
          <div><strong className="text-slate-200">FastAPI Core:</strong> v{healthData?.version || '2.4.0'}</div>
          <div><strong className="text-slate-200">Vision Engine:</strong> Multimodal LLM</div>
          <div><strong className="text-slate-200">3D Render:</strong> Pollinations / Flux API</div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between gap-3 pt-2 border-t border-slate-800">
          <button
            onClick={handleClear}
            className="px-3 py-2 text-xs text-slate-400 hover:text-red-400 transition"
          >
            Clear Stored Key
          </button>
          <div className="flex gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="btn-primary text-xs px-5 py-2"
            >
              {isSaved ? <Check className="w-4 h-4" /> : <ShieldCheck className="w-4 h-4" />}
              {isSaved ? 'Configured!' : 'Save & Connect'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
