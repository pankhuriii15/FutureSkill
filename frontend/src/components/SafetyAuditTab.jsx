import React, { useState } from 'react';
import { ShieldCheck, HardHat, AlertTriangle, Upload, Eye, FileDown, CheckCircle, XCircle, AlertOctagon, UserCheck, RefreshCw, Sparkles } from 'lucide-react';
import { createConstructionSampleImage } from '../utils/sampleImages';

export default function SafetyAuditTab({ apiKey, backendConnected }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [notes, setNotes] = useState('Inspect high-risk deck slab framing for fall protection and IS 2925 helmet compliance');
  const [loading, setLoading] = useState(false);
  const [auditResult, setAuditResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  // Handle custom file upload
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setErrorMsg('');
    }
  };

  // Load in-memory preset sample and run audit
  const loadPreset = async (presetType) => {
    setLoading(true);
    setErrorMsg('');
    try {
      const sample = await createConstructionSampleImage(presetType);
      setSelectedFile(sample.file);
      setPreviewUrl(sample.previewUrl);
      const newNotes = presetType === "safety_deck"
        ? "High-risk Level 14 deck slab formwork with rebar tying and perimeter edge danger"
        : "Excavation zone inspection with shoring nails and heavy equipment movements";
      setNotes(newNotes);

      // Run audit directly
      const formData = new FormData();
      formData.append("file", sample.file);
      formData.append("notes", newNotes);
      if (apiKey) formData.append("api_key", apiKey);

      const response = await fetch("/api/audit-safety", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setAuditResult(data);
      }
    } catch (err) {
      setErrorMsg("Failed to generate sample audit");
    } finally {
      setLoading(false);
    }
  };

  // Trigger Safety Audit via FastAPI
  const handleRunAudit = async () => {
    if (!selectedFile) {
      setErrorMsg("Please upload a construction photo or click a sample preset first.");
      return;
    }

    setLoading(true);
    setErrorMsg('');
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      if (notes) formData.append("notes", notes);
      if (apiKey) formData.append("api_key", apiKey);

      const response = await fetch("/api/audit-safety", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server returned ${response.status}`);
      }

      const data = await response.json();
      setAuditResult(data);
    } catch (err) {
      setErrorMsg(`Safety Audit Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Export JSON Report
  const handleDownloadReport = () => {
    if (!auditResult) return;
    const blob = new Blob([JSON.stringify(auditResult, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Safety_Audit_${auditResult.audit_id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Tab Banner / Epic Context */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl glass-panel border-amber-500/20 bg-gradient-to-r from-slate-900/90 via-slate-900/60 to-amber-950/20">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="pill pill-moderate">Epic 2: Safety Vision</span>
            <span className="text-xs text-slate-400">OSHA 1926 & IS 456 Standards</span>
          </div>
          <h2 className="text-xl lg:text-2xl font-extrabold text-white">
            Site Safety & PPE Compliance Audit
          </h2>
          <p className="text-xs lg:text-sm text-slate-300 max-w-2xl mt-1">
            Multimodal AI scans construction site images for worker PPE compliance (helmets, vests, harnesses, boots) and identifies critical workplace hazards with automated corrective actions.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => loadPreset("safety_deck")}
            className="btn-secondary text-xs"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            Sample: High-Risk Deck
          </button>
          <button
            onClick={() => loadPreset("safety_excavation")}
            className="btn-secondary text-xs"
          >
            <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
            Sample: Excavation Pit
          </button>
        </div>
      </div>

      {/* Main Grid: Upload & Inputs on Left, Results on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Upload & Context Column (5 cols) */}
        <div className="lg:col-span-5 space-y-5">
          {/* File Upload Dropzone */}
          <div className="glass-panel p-5 rounded-2xl space-y-4">
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider">
              1. Upload Site Inspection Photo
            </label>

            <div className="relative border-2 border-dashed border-slate-700 hover:border-amber-500/60 rounded-xl p-4 transition text-center bg-slate-950/40">
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              />

              {previewUrl ? (
                <div className="relative group">
                  <img
                    src={previewUrl}
                    alt="Site Preview"
                    className="w-full h-56 object-cover rounded-lg shadow-md border border-slate-700"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition rounded-lg flex items-center justify-center text-xs text-white gap-2">
                    <Upload className="w-4 h-4" /> Click or drag to replace image
                  </div>
                </div>
              ) : (
                <div className="py-8 space-y-2">
                  <div className="w-12 h-12 mx-auto rounded-full bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
                    <Upload className="w-6 h-6" />
                  </div>
                  <div className="text-sm font-semibold text-slate-200">
                    Drop construction photo here, or <span className="text-amber-400 underline">browse</span>
                  </div>
                  <p className="text-[11px] text-slate-400">Supports JPG, PNG, WebP up to 20MB</p>
                </div>
              )}
            </div>

            {/* Context & Notes */}
            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-slate-300">
                2. Site Context / Inspector Observations
              </label>
              <textarea
                rows={3}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="e.g. Scaffolding inspection at Level 4, check for worker harnesses..."
                className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-amber-500 font-sans"
              />
            </div>

            {/* Error Message */}
            {errorMsg && (
              <div className="p-3 rounded-xl bg-red-500/15 border border-red-500/30 text-xs text-red-300 flex items-start gap-2">
                <AlertOctagon className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                <span>{errorMsg}</span>
              </div>
            )}

            {/* Submit Action */}
            <button
              onClick={handleRunAudit}
              disabled={loading || !selectedFile}
              className="w-full btn-primary py-3"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-slate-900" />
                  <span>Analyzing Multimodal Vision...</span>
                </>
              ) : (
                <>
                  <ShieldCheck className="w-4 h-4 text-slate-900" />
                  <span>Run AI Safety & PPE Audit</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Column (7 cols) */}
        <div className="lg:col-span-7 space-y-5">
          {auditResult ? (
            <div className="space-y-5 animate-fadeIn">
              {/* Top Score & Status Metric Banner */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {/* Score Card */}
                <div className="glass-panel p-4 rounded-xl flex items-center justify-between">
                  <div>
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">Safety Score</span>
                    <div className="text-3xl font-extrabold text-white mt-0.5 flex items-baseline gap-1">
                      <span className={auditResult.safety_score >= 80 ? 'text-emerald-400' : auditResult.safety_score >= 60 ? 'text-amber-400' : 'text-red-400'}>
                        {auditResult.safety_score}
                      </span>
                      <span className="text-xs text-slate-500">/ 100</span>
                    </div>
                  </div>
                  <div className={`p-3 rounded-xl ${auditResult.safety_score >= 80 ? 'bg-emerald-500/15 text-emerald-400' : auditResult.safety_score >= 60 ? 'bg-amber-500/15 text-amber-400' : 'bg-red-500/15 text-red-400'}`}>
                    <ShieldCheck className="w-6 h-6" />
                  </div>
                </div>

                {/* Status Pill Card */}
                <div className="glass-panel p-4 rounded-xl flex items-center justify-between">
                  <div>
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">Compliance Status</span>
                    <div className="mt-1">
                      <span className={`pill ${
                        auditResult.overall_status === 'Compliant'
                          ? 'pill-compliant'
                          : auditResult.overall_status === 'High Risk' || auditResult.overall_status === 'Critical Violation'
                          ? 'pill-critical'
                          : 'pill-moderate'
                      }`}>
                        {auditResult.overall_status}
                      </span>
                    </div>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-800 text-slate-300">
                    <AlertTriangle className="w-5 h-5" />
                  </div>
                </div>

                {/* Workers Detected */}
                <div className="glass-panel p-4 rounded-xl flex items-center justify-between">
                  <div>
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">Workers Scanned</span>
                    <div className="text-2xl font-extrabold text-white mt-0.5">
                      {auditResult.workers_detected_count} <span className="text-xs font-normal text-slate-400">Identified</span>
                    </div>
                  </div>
                  <div className="p-3 rounded-xl bg-blue-500/15 text-blue-400">
                    <UserCheck className="w-5 h-5" />
                  </div>
                </div>
              </div>

              {/* PPE Detection Checklist */}
              <div className="glass-panel p-5 rounded-2xl space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <HardHat className="w-4 h-4 text-amber-400" />
                    <span>PPE Compliance Checklist (IS 2925 & OSHA 1926)</span>
                  </h3>
                  <span className="mono-badge text-[10px] text-slate-400">
                    Mode: {auditResult.execution_mode}
                  </span>
                </div>

                <div className="divide-y divide-slate-800/80">
                  {auditResult.ppe_checklist.map((item, idx) => (
                    <div key={idx} className="py-2.5 flex items-center justify-between text-xs gap-3">
                      <div className="space-y-0.5">
                        <div className="font-semibold text-slate-200">{item.item_name}</div>
                        <div className="text-[11px] text-slate-400">{item.details}</div>
                      </div>
                      <div className="flex items-center gap-3 shrink-0">
                        <div className="text-right">
                          <span className="font-mono text-slate-200">{item.compliance_percentage}%</span>
                          <span className="text-[10px] text-slate-500 block">({item.detected_count} / {item.detected_count + item.missing_count})</span>
                        </div>
                        <span className={`pill ${
                          item.status === 'Compliant' ? 'pill-compliant' : item.status === 'Partial' ? 'pill-moderate' : 'pill-critical'
                        }`}>
                          {item.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Identified Site Hazards */}
              <div className="glass-panel p-5 rounded-2xl space-y-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <AlertOctagon className="w-4 h-4 text-red-400" />
                  <span>Identified Site Hazards & Corrective Remedies ({auditResult.identified_hazards.length})</span>
                </h3>

                <div className="space-y-3">
                  {auditResult.identified_hazards.map((hazard, idx) => (
                    <div
                      key={idx}
                      className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2 hover:border-slate-700 transition"
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-bold text-xs text-white">{hazard.hazard_name}</span>
                        <span className={`pill ${hazard.severity === 'Critical' || hazard.severity === 'High' ? 'pill-critical' : 'pill-moderate'}`}>
                          {hazard.severity} Severity
                        </span>
                      </div>
                      <div className="text-[11px] text-slate-400">
                        <strong className="text-slate-300">Location:</strong> {hazard.location} • <strong className="text-slate-300">Standard:</strong> {hazard.standard_violation}
                      </div>
                      <div className="text-xs text-amber-200/90 bg-amber-500/10 p-2.5 rounded-lg border border-amber-500/20">
                        <strong className="text-amber-400">Remedy:</strong> {hazard.remedy}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Executive Summary & Recommendations */}
              <div className="glass-panel p-5 rounded-2xl space-y-3">
                <h3 className="text-sm font-bold text-white">Executive Audit Summary</h3>
                <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/40 p-3 rounded-xl border border-slate-800">
                  {auditResult.executive_summary}
                </p>

                <div className="pt-2">
                  <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block mb-2">
                    Priority Corrective Recommendations:
                  </span>
                  <ul className="space-y-1.5 text-xs text-slate-300">
                    {auditResult.recommendations.map((rec, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <CheckCircle className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Action Toolbar */}
              <div className="flex items-center justify-between pt-2">
                <div className="text-[11px] text-slate-400 font-mono">
                  Audit Ref: {auditResult.audit_id} • {auditResult.timestamp}
                </div>
                <button
                  onClick={handleDownloadReport}
                  className="btn-secondary text-xs flex items-center gap-2"
                >
                  <FileDown className="w-3.5 h-3.5 text-amber-400" />
                  <span>Download Audit Report (.JSON)</span>
                </button>
              </div>
            </div>
          ) : (
            /* Empty State */
            <div className="glass-panel p-10 rounded-2xl text-center space-y-3 border-dashed">
              <div className="w-16 h-16 mx-auto rounded-2xl bg-slate-800/60 border border-slate-700 flex items-center justify-center text-slate-400">
                <ShieldCheck className="w-8 h-8 text-amber-400/60" />
              </div>
              <h3 className="text-base font-bold text-white">Awaiting Site Image</h3>
              <p className="text-xs text-slate-400 max-w-sm mx-auto">
                Upload a construction site photo or select one of the high-risk presets on the left to initiate the multimodal safety & PPE inspection.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
