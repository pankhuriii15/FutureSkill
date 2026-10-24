import React, { useState, useEffect } from 'react';
import { HardHat, Activity, TrendingUp, CloudLightning, Key, ExternalLink, ShieldCheck, Sparkles, HelpCircle } from 'lucide-react';
import Navbar from './components/Navbar';
import SafetyAuditTab from './components/SafetyAuditTab';
import CrackDiagnosticsTab from './components/CrackDiagnosticsTab';
import PlanningValuationTab from './components/PlanningValuationTab';
import DailySiteAssistantTab from './components/DailySiteAssistantTab';
import ApiConfigModal from './components/ApiConfigModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('safety');
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('gemini_api_key') || '');
  const [isKeyModalOpen, setIsKeyModalOpen] = useState(false);
  const [backendConnected, setBackendConnected] = useState(false);
  const [healthData, setHealthData] = useState(null);

  // Check backend health on mount
  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchHealth = async () => {
    try {
      const response = await fetch('/api/health');
      if (response.ok) {
        const data = await response.json();
        setBackendConnected(true);
        setHealthData(data);
      } else {
        setBackendConnected(false);
      }
    } catch {
      setBackendConnected(false);
    }
  };

  const handleSaveApiKey = (newKey) => {
    setApiKey(newKey);
    if (newKey) {
      localStorage.setItem('gemini_api_key', newKey);
    } else {
      localStorage.removeItem('gemini_api_key');
    }
  };

  const navTabs = [
    { id: 'safety', label: 'Site Safety & PPE Audit', icon: HardHat, epic: 'Epic 2' },
    { id: 'cracks', label: 'Crack Diagnostics', icon: Activity, epic: 'Epic 2' },
    { id: 'valuation', label: 'Planning & Valuation', icon: TrendingUp, epic: 'Epic 3' },
    { id: 'weather', label: 'Weather & Assistant', icon: CloudLightning, epic: 'Epic 5' },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[#080c14] text-slate-100 selection:bg-amber-500 selection:text-slate-950 font-sans">
      {/* Top Navbar */}
      <Navbar
        onOpenKeyModal={() => setIsKeyModalOpen(true)}
        apiKey={apiKey}
        backendConnected={backendConnected}
        healthData={healthData}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-6 space-y-6">
        {/* Navigation Tab Bar */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800/80 scrollbar-none">
          {navTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-xs font-bold transition whitespace-nowrap border ${
                  isActive
                    ? 'bg-amber-500/15 border-amber-500/60 text-amber-400 shadow-md shadow-amber-500/10'
                    : 'bg-slate-900/60 border-slate-800/80 text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-amber-400' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
                <span className={`text-[10px] px-1.5 py-0.2 rounded font-mono ${isActive ? 'bg-amber-500/30 text-amber-300' : 'bg-slate-800 text-slate-500'}`}>
                  {tab.epic}
                </span>
              </button>
            );
          })}
        </div>

        {/* Tab Content Panels */}
        <div className="transition-all duration-300">
          {activeTab === 'safety' && (
            <SafetyAuditTab apiKey={apiKey} backendConnected={backendConnected} />
          )}
          {activeTab === 'cracks' && (
            <CrackDiagnosticsTab apiKey={apiKey} backendConnected={backendConnected} />
          )}
          {activeTab === 'valuation' && (
            <PlanningValuationTab apiKey={apiKey} />
          )}
          {activeTab === 'weather' && (
            <DailySiteAssistantTab apiKey={apiKey} />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full border-t border-slate-800/80 bg-slate-950/80 py-6 px-4 lg:px-8 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="font-semibold text-slate-300">Multimodal Construction Intelligence Platform</span>
            <span>•</span>
            <span className="font-mono text-slate-400">ID: 6ac4c98d1dcde6d7857c1642</span>
            <span>•</span>
            <span className="text-amber-500">Generative AI Decision Support</span>
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer" className="text-slate-400 hover:text-amber-400 flex items-center gap-1 transition">
              <span>FastAPI OpenAPI Docs</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <span>•</span>
            <span>IS 456:2000 & OSHA 1926 Certified Reference Architecture</span>
          </div>
        </div>
      </footer>

      {/* Key Configuration Modal */}
      <ApiConfigModal
        isOpen={isKeyModalOpen}
        onClose={() => setIsKeyModalOpen(false)}
        apiKey={apiKey}
        onSaveKey={handleSaveApiKey}
        healthData={healthData}
      />
    </div>
  );
}
