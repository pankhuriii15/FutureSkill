import React from 'react';
import { HardHat, Shield, Activity, Key, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Navbar({ onOpenKeyModal, apiKey, backendConnected, healthData }) {
  return (
    <header className="sticky top-0 z-40 w-full bg-slate-950/80 backdrop-blur-xl border-b border-slate-800/80 px-4 lg:px-8 py-3.5 transition-all">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
        {/* Brand & Platform Identity */}
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 p-0.5 shadow-lg shadow-amber-500/25 flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center text-amber-400">
              <HardHat className="w-5 h-5" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base lg:text-lg font-extrabold tracking-tight text-white">
                Multimodal Construction Intelligence Platform
              </h1>
              <span className="hidden sm:inline-block px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30">
                v2.4
              </span>
            </div>
            <div className="flex items-center gap-2 text-[11px] text-slate-400">
              <span className="font-mono text-slate-400">ID: 6ac4c98d1dcde6d7857c1642</span>
              <span>•</span>
              <span className="text-amber-400/90 font-medium">IS 456 & OSHA Compliant</span>
            </div>
          </div>
        </div>

        {/* Right Status Badges & Controls */}
        <div className="flex items-center gap-2.5 sm:gap-3">
          {/* Backend Health Pill */}
          <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs text-slate-300">
            <span className={`w-2 h-2 rounded-full ${backendConnected ? 'bg-emerald-400 animate-pulse' : 'bg-red-500'}`} />
            <span>FastAPI:</span>
            <span className={backendConnected ? 'text-emerald-400 font-semibold' : 'text-red-400'}>
              {backendConnected ? 'Operational' : 'Connecting...'}
            </span>
          </div>

          {/* AI Engine Status Button */}
          <button
            onClick={onOpenKeyModal}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold border transition ${
              apiKey
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20'
                : 'bg-amber-500/10 border-amber-500/30 text-amber-400 hover:bg-amber-500/20'
            }`}
          >
            <Key className="w-3.5 h-3.5" />
            <span>{apiKey ? 'Gemini 1.5 Active' : 'Demo Intelligence'}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
