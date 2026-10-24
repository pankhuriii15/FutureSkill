import React, { useState } from 'react';
import { Activity, AlertTriangle, Upload, FileDown, Wrench, ShieldAlert, CheckCircle, Clock, Sparkles, RefreshCw, AlertOctagon } from 'lucide-react';
import { createConstructionSampleImage } from '../utils/sampleImages';

export default function CrackDiagnosticsTab({ apiKey }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [notes, setNotes] = useState('45 degree diagonal shear crack near beam support on reinforced concrete transfer girder');
  const [loading, setLoading] = useState(false);
  const [crackResult, setCrackResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setErrorMsg('');
    }
  };

  const loadPreset = async (presetType) => {
    setLoading(true);
    setErrorMsg('');
    try {
      const sample = await createConstructionSampleImage(presetType);
      setSelectedFile(sample.file);
      setPreviewUrl(sample.previewUrl);
      const newNotes = presetType === "crack_shear"
        ? "45° diagonal tension shear crack in RCC beam web under heavy superimposed load"
        : "Stepped masonry settlement crack propagating through mortar bed joints along plinth wall";
      setNotes(newNotes);

      const formData = new FormData();
      formData.append("file", sample.file);
      formData.append("notes", newNotes);
      if (apiKey) formData.append("api_key", apiKey);

      const response = await fetch("/api/diagnose-crack", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setCrackResult(data);
      }
    } catch (err) {
      setErrorMsg("Failed to generate sample crack diagnosis");
    } finally {
      setLoading(false);
    }
  };

  const handleRunDiagnosis = async () => {
    if (!selectedFile) {
      setErrorMsg("Please upload a concrete/wall photo or select a defect preset.");
      return;
    }

    setLoading(true);
    setErrorMsg('');
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      if (notes) formData.append("notes", notes);
      if (apiKey) formData.append("api_key", apiKey);

      const response = await fetch("/api/diagnose-crack", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server returned ${response.status}`);
      }

      const data = await response.json();
      setCrackResult(data);
    } catch (err) {
      setErrorMsg(`Crack Diagnostics Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    if (!crackResult) return;
    const blob = new Blob([JSON.stringify(crackResult, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Crack_Diagnosis_${crackResult.defect_id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl glass-panel border-cyan-500/20 bg-gradient-to-r from-slate-900/90 via-slate-900/60 to-cyan-950/20">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="pill pill-info">Epic 2: Concrete Forensics</span>
            <span className="text-xs text-slate-400">IS 456:2000 & ACI 224R-01</span>
          </div>
          <h2 className="text-xl lg:text-2xl font-extrabold text-white">
            Crack Diagnostics & Structural Integrity Analysis
          </h2>
          <p className="text-xs lg:text-sm text-slate-300 max-w-2xl mt-1">
            Computer vision analyzes surface fractures to classify defect types (Shear, Settlement, Hairline, Spalling), measure millimeter crack width, and prescribe engineering repairs.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => loadPreset("crack_shear")}
            className="btn-secondary text-xs"
          >
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            Sample: Shear Crack
          </button>
          <button
            onClick={() => loadPreset("crack_settlement")}
            className="btn-secondary text-xs"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            Sample: Settlement Crack
          </button>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Inputs (5 cols) */}
        <div className="lg:col-span-5 space-y-5">
          <div className="glass-panel p-5 rounded-2xl space-y-4">
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider">
              1. Upload Concrete / Masonry Defect Image
            </label>

            <div className="relative border-2 border-dashed border-slate-700 hover:border-cyan-500/60 rounded-xl p-4 transition text-center bg-slate-950/40">
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
                    alt="Crack Preview"
                    className="w-full h-56 object-cover rounded-lg shadow-md border border-slate-700"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition rounded-lg flex items-center justify-center text-xs text-white gap-2">
                    <Upload className="w-4 h-4" /> Click or drag to replace image
                  </div>
                </div>
              ) : (
                <div className="py-8 space-y-2">
                  <div className="w-12 h-12 mx-auto rounded-full bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
                    <Activity className="w-6 h-6" />
                  </div>
                  <div className="text-sm font-semibold text-slate-200">
                    Upload concrete or wall fracture image, or <span className="text-cyan-400 underline">browse</span>
                  </div>
                  <p className="text-[11px] text-slate-400">Supports JPG, PNG up to 20MB</p>
                </div>
              )}
            </div>

            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-slate-300">
                2. Structural Context & Location
              </label>
              <textarea
                rows={3}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="e.g. Beam support zone, slab soffit, masonry mortar joint..."
                className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 font-sans"
              />
            </div>

            {errorMsg && (
              <div className="p-3 rounded-xl bg-red-500/15 border border-red-500/30 text-xs text-red-300 flex items-start gap-2">
                <AlertOctagon className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                <span>{errorMsg}</span>
              </div>
            )}

            <button
              onClick={handleRunDiagnosis}
              disabled={loading || !selectedFile}
              className="w-full btn-primary py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-cyan-500/25 hover:shadow-cyan-500/40"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-white" />
                  <span>Diagnosing Structural Defect...</span>
                </>
              ) : (
                <>
                  <Activity className="w-4 h-4 text-white" />
                  <span>Diagnose Structural Defect</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Results (7 cols) */}
        <div className="lg:col-span-7 space-y-5">
          {crackResult ? (
            <div className="space-y-5 animate-fadeIn">
              {/* Metric Highlights */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {/* Defect Classification */}
                <div className="glass-panel p-4 rounded-xl flex items-center justify-between">
                  <div>
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">Defect Type</span>
                    <div className="text-base font-extrabold text-white mt-0.5">
                      {crackResult.defect_type}
                    </div>
                    <span className="text-[11px] text-cyan-400 font-mono">
                      {crackResult.confidence_score}% Confidence
                    </span>
                  </div>
                  <div className="p-3 rounded-xl bg-cyan-500/15 text-cyan-400">
                    <Activity className="w-5 h-5" />
                  </div>
                </div>

                {/* Estimated Crack Width */}
                <div className="glass-panel p-4 rounded-xl flex items-center justify-between">
                  <div>
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">Crack Width (mm)</span>
                    <div className="text-2xl font-extrabold text-white mt-0.5">
                      {crackResult.estimated_crack_width_mm} <span className="text-xs font-normal text-slate-400">mm</span>
                    </div>
                    <span className="text-[10px] text-slate-400">IS 456 Limit: 0.30mm</span>
                  </div>
                  <div className={`p-3 rounded-xl ${crackResult.estimated_crack_width_mm > 0.3 ? 'bg-red-500/15 text-red-400' : 'bg-emerald-500/15 text-emerald-400'}`}>
                    <ShieldAlert className="w-5 h-5" />
                  </div>
                </div>

                {/* Severity & Urgency */}
                <div className="glass-panel p-4 rounded-xl flex items-center justify-between">
                  <div>
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">Severity & Urgency</span>
                    <div className="mt-1 flex flex-col gap-1">
                      <span className={`pill ${
                        crackResult.severity_level === 'Severe' || crackResult.severity_level === 'Catastrophic'
                          ? 'pill-critical'
                          : crackResult.severity_level === 'Moderate' ? 'pill-moderate' : 'pill-compliant'
                      }`}>
                        {crackResult.severity_level}
                      </span>
                    </div>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-800 text-slate-300">
                    <Clock className="w-5 h-5" />
                  </div>
                </div>
              </div>

              {/* Structural Integrity Assessment */}
              <div className="glass-panel p-5 rounded-2xl space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <ShieldAlert className="w-4 h-4 text-red-400" />
                    <span>Structural Integrity Risk Assessment</span>
                  </h3>
                  <span className={`pill ${crackResult.urgency_rating.includes('Immediate') ? 'pill-critical' : 'pill-moderate'}`}>
                    {crackResult.urgency_rating}
                  </span>
                </div>

                <p className="text-xs text-slate-300 bg-slate-950/50 p-3.5 rounded-xl border border-slate-800 leading-relaxed">
                  {crackResult.structural_integrity_risk}
                </p>

                <div className="text-[11px] text-slate-400 flex items-center gap-2 pt-1">
                  <span className="font-semibold text-slate-300">Applicable Code References:</span>
                  {crackResult.applicable_standards.map((std, i) => (
                    <span key={i} className="mono-badge text-cyan-400">{std}</span>
                  ))}
                </div>
              </div>

              {/* Probable Root Causes */}
              <div className="glass-panel p-5 rounded-2xl space-y-2.5">
                <h3 className="text-sm font-bold text-white">Probable Structural Root Causes</h3>
                <ul className="space-y-1.5 text-xs text-slate-300">
                  {crackResult.probable_root_causes.map((cause, idx) => (
                    <li key={idx} className="flex items-start gap-2 bg-slate-950/40 p-2 rounded-lg border border-slate-800/80">
                      <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-1.5 shrink-0" />
                      <span>{cause}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Recommended Engineering Repairs & Workflow */}
              <div className="glass-panel p-5 rounded-2xl space-y-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Wrench className="w-4 h-4 text-amber-400" />
                  <span>Recommended Engineering Repair Methodology</span>
                </h3>

                <div className="flex flex-wrap gap-2 mb-2">
                  {crackResult.recommended_engineering_repairs.map((rep, idx) => (
                    <span key={idx} className="px-2.5 py-1 rounded-md text-[11px] font-medium bg-amber-500/10 border border-amber-500/30 text-amber-300">
                      {rep}
                    </span>
                  ))}
                </div>

                <div className="space-y-2 pt-1">
                  <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                    Execution Steps:
                  </span>
                  {crackResult.repair_steps.map((step, idx) => (
                    <div key={idx} className="flex items-start gap-2.5 text-xs text-slate-300">
                      <span className="w-5 h-5 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-[10px] font-bold text-cyan-400 shrink-0">
                        {idx + 1}
                      </span>
                      <span>{step}</span>
                    </div>
                  ))}
                </div>

                <div className="mt-3 p-3 rounded-xl bg-slate-900 border border-slate-800 text-[11px] text-slate-400">
                  <strong className="text-slate-200">Monitoring Protocol:</strong> {crackResult.monitoring_protocol}
                </div>
              </div>

              {/* Action Toolbar */}
              <div className="flex items-center justify-between pt-2">
                <div className="text-[11px] text-slate-400 font-mono">
                  Defect Ref: {crackResult.defect_id} • {crackResult.timestamp}
                </div>
                <button
                  onClick={handleDownloadReport}
                  className="btn-secondary text-xs flex items-center gap-2"
                >
                  <FileDown className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Download Diagnostics Report (.JSON)</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="glass-panel p-10 rounded-2xl text-center space-y-3 border-dashed">
              <div className="w-16 h-16 mx-auto rounded-2xl bg-slate-800/60 border border-slate-700 flex items-center justify-center text-slate-400">
                <Activity className="w-8 h-8 text-cyan-400/60" />
              </div>
              <h3 className="text-base font-bold text-white">Awaiting Crack Image</h3>
              <p className="text-xs text-slate-400 max-w-sm mx-auto">
                Upload a concrete, brick, or wall defect photograph to classify crack depth, measure width, and generate engineering repair protocols.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
