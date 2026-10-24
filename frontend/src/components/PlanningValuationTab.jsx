import React, { useState, useEffect } from 'react';
import { Building2, IndianRupee, Layers, Calendar, BarChart3, TrendingUp, Sparkles, Image as ImageIcon, ExternalLink, FileDown, RefreshCw } from 'lucide-react';

export default function PlanningValuationTab() {
  const [structureType, setStructureType] = useState('Residential High-Rise');
  const [builtUpSqft, setBuiltUpSqft] = useState(85000);
  const [locationTier, setLocationTier] = useState('Tier 1 (Mumbai, Delhi-NCR, Bengaluru)');
  const [completionPercentage, setCompletionPercentage] = useState(45);
  const [constructionGrade, setConstructionGrade] = useState('Premium');
  const [customPrompt, setCustomPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [valuationData, setValuationData] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  // Initial calculation on mount
  useEffect(() => {
    handleCalculate();
  }, []);

  const handleCalculate = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const response = await fetch('/api/calculate-valuation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          structure_type: structureType,
          built_up_sqft: Number(builtUpSqft),
          location_tier: locationTier,
          completion_percentage: Number(completionPercentage),
          construction_grade: constructionGrade,
          custom_prompt: customPrompt.trim() || null
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server returned ${response.status}`);
      }

      const data = await response.json();
      setValuationData(data);
    } catch (err) {
      setErrorMsg(`Valuation Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    if (!valuationData) return;
    const blob = new Blob([JSON.stringify(valuationData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Valuation_Report_${valuationData.calculation_id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const applyPreset = (preset) => {
    setStructureType(preset.structure_type);
    setBuiltUpSqft(preset.built_up_sqft);
    setLocationTier(preset.location_tier);
    setCompletionPercentage(preset.completion_percentage);
    setConstructionGrade(preset.construction_grade);
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl glass-panel border-emerald-500/20 bg-gradient-to-r from-slate-900/90 via-slate-900/60 to-emerald-950/20">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="pill pill-compliant">Epic 3: Planning & Valuation</span>
            <span className="text-xs text-slate-400">IS 456 & CPWD Schedule of Rates</span>
          </div>
          <h2 className="text-xl lg:text-2xl font-extrabold text-white">
            Project Planning, Cost & Real Estate Valuation (INR)
          </h2>
          <p className="text-xs lg:text-sm text-slate-300 max-w-2xl mt-1">
            Calculate construction budgets, CapEx incurred, current market valuation in Indian Crores/Lakhs, steel/cement thumb rules, and generate 3D architectural renders via Pollinations AI.
          </p>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => applyPreset({
              structure_type: "Residential High-Rise",
              built_up_sqft: 120000,
              location_tier: "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
              completion_percentage: 65,
              construction_grade: "Luxury"
            })}
            className="btn-secondary text-xs"
          >
            Mumbai High-Rise
          </button>
          <button
            onClick={() => applyPreset({
              structure_type: "Commercial Complex",
              built_up_sqft: 250000,
              location_tier: "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
              completion_percentage: 40,
              construction_grade: "Premium"
            })}
            className="btn-secondary text-xs"
          >
            Tech Campus BLR
          </button>
        </div>
      </div>

      {/* Main Grid: Parameters on Left, Output on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Controls Column (4 cols) */}
        <div className="lg:col-span-4 space-y-5">
          <div className="glass-panel p-5 rounded-2xl space-y-4">
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <Building2 className="w-4 h-4 text-emerald-400" />
              <span>Project Specification Parameters</span>
            </h3>

            {/* Structure Type */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Structure Type</label>
              <select
                value={structureType}
                onChange={(e) => setStructureType(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
              >
                <option value="Residential High-Rise">Residential High-Rise</option>
                <option value="Commercial Complex">Commercial Complex / IT Park</option>
                <option value="Villa / Row House">Luxury Villa / Row House</option>
                <option value="Industrial Warehouse">Industrial Warehouse / PEB</option>
                <option value="Infrastructure / Bridge">Infrastructure / Flyover</option>
              </select>
            </div>

            {/* Built-up Area */}
            <div className="space-y-1">
              <div className="flex justify-between items-center text-xs">
                <label className="font-semibold text-slate-300">Built-Up Area (sq. ft.)</label>
                <span className="font-mono text-emerald-400 font-bold">{Number(builtUpSqft).toLocaleString()} sqft</span>
              </div>
              <input
                type="number"
                min="1000"
                step="5000"
                value={builtUpSqft}
                onChange={(e) => setBuiltUpSqft(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white focus:outline-none focus:border-emerald-500 font-mono"
              />
              <div className="flex gap-1.5 pt-1">
                {[25000, 50000, 100000, 250000].map((area) => (
                  <button
                    key={area}
                    onClick={() => setBuiltUpSqft(area)}
                    className="px-2 py-1 text-[10px] rounded bg-slate-800 text-slate-300 hover:bg-slate-700 font-mono"
                  >
                    {area / 1000}k
                  </button>
                ))}
              </div>
            </div>

            {/* Location Tier */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Location Tier (Indian Market)</label>
              <select
                value={locationTier}
                onChange={(e) => setLocationTier(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
              >
                <option value="Tier 1 (Mumbai, Delhi-NCR, Bengaluru)">Tier 1 (Mumbai, Delhi-NCR, Bengaluru)</option>
                <option value="Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)">Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)</option>
                <option value="Tier 3 (Emerging Urban Centers)">Tier 3 (Emerging Urban Centers)</option>
              </select>
            </div>

            {/* Construction Grade */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Construction Grade</label>
              <div className="grid grid-cols-3 gap-1.5">
                {['Standard', 'Premium', 'Luxury'].map((grade) => (
                  <button
                    key={grade}
                    onClick={() => setConstructionGrade(grade)}
                    className={`py-1.5 text-xs font-semibold rounded-lg border transition ${
                      constructionGrade === grade
                        ? 'bg-emerald-500/20 border-emerald-500 text-emerald-400'
                        : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'
                    }`}
                  >
                    {grade}
                  </button>
                ))}
              </div>
            </div>

            {/* Completion Percentage Slider */}
            <div className="space-y-2 pt-1">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-300">Completion Milestone Progress</span>
                <span className="font-mono text-emerald-400 font-extrabold text-sm">{completionPercentage}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={completionPercentage}
                onChange={(e) => setCompletionPercentage(e.target.value)}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
              />
              <div className="flex justify-between text-[10px] text-slate-500">
                <span>0% Ground</span>
                <span>50% Superstructure</span>
                <span>100% Handover</span>
              </div>
            </div>

            {/* Generative 3D Visualizer Prompt */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                <span>Custom 3D Architecture Prompt (Pollinations AI)</span>
              </label>
              <textarea
                rows={2}
                value={customPrompt}
                onChange={(e) => setCustomPrompt(e.target.value)}
                placeholder="Leave blank to auto-generate ultra-photorealistic architectural render..."
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-slate-300 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
              />
            </div>

            {/* Error Message */}
            {errorMsg && (
              <div className="p-2.5 rounded-lg bg-red-500/15 border border-red-500/30 text-xs text-red-300">
                {errorMsg}
              </div>
            )}

            {/* Calculate Button */}
            <button
              onClick={handleCalculate}
              disabled={loading}
              className="w-full btn-primary py-3 bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-950 font-bold shadow-emerald-500/25"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-slate-950" />
                  <span>Computing Quantities & Valuation...</span>
                </>
              ) : (
                <>
                  <BarChart3 className="w-4 h-4 text-slate-950" />
                  <span>Update Valuation & Schedules</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Column (8 cols) */}
        <div className="lg:col-span-8 space-y-5">
          {valuationData && (
            <div className="space-y-5 animate-fadeIn">
              {/* Financial KPI Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                {/* Total Budget */}
                <div className="glass-panel p-4 rounded-xl space-y-1">
                  <span className="text-[10px] text-slate-400 uppercase font-semibold">Total Project Budget</span>
                  <div className="text-xl font-extrabold text-white">
                    {valuationData.total_budget_formatted}
                  </div>
                  <span className="text-[10px] text-slate-400 block font-mono">
                    ₹{valuationData.cost_per_sqft_inr}/sqft cost
                  </span>
                </div>

                {/* CapEx Incurred */}
                <div className="glass-panel p-4 rounded-xl space-y-1">
                  <span className="text-[10px] text-slate-400 uppercase font-semibold">CapEx Incurred to Date</span>
                  <div className="text-xl font-extrabold text-amber-400">
                    {valuationData.capex_incurred_formatted}
                  </div>
                  <span className="text-[10px] text-slate-400 block font-mono">
                    Rem: {valuationData.capex_remaining_formatted}
                  </span>
                </div>

                {/* Current Asset Valuation */}
                <div className="glass-panel p-4 rounded-xl space-y-1 border-emerald-500/30">
                  <span className="text-[10px] text-emerald-400 uppercase font-bold">Current Asset Valuation</span>
                  <div className="text-xl font-extrabold text-emerald-400">
                    {valuationData.current_asset_valuation_formatted}
                  </div>
                  <span className="text-[10px] text-slate-400 block">
                    At {valuationData.completion_percentage}% Progress
                  </span>
                </div>

                {/* Projected Completed Valuation */}
                <div className="glass-panel p-4 rounded-xl space-y-1">
                  <span className="text-[10px] text-slate-400 uppercase font-semibold">Projected Valuation</span>
                  <div className="text-xl font-extrabold text-cyan-400">
                    {valuationData.projected_completion_valuation_formatted}
                  </div>
                  <span className="text-[10px] text-cyan-400 font-bold block">
                    +{valuationData.estimated_roi_percentage}% Est. Margin
                  </span>
                </div>
              </div>

              {/* Milestone Progress Gantt Bar */}
              <div className="glass-panel p-5 rounded-2xl space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-emerald-400" />
                    <span>Construction Milestone Progress & Work Breakdown</span>
                  </h3>
                  <span className="pill pill-compliant">{valuationData.completion_percentage}% Incurred</span>
                </div>

                {/* Multi-stage Progress Bar */}
                <div className="w-full h-3 bg-slate-900 rounded-full overflow-hidden flex border border-slate-800">
                  <div
                    className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 transition-all duration-500 rounded-full"
                    style={{ width: `${valuationData.completion_percentage}%` }}
                  />
                </div>

                {/* Milestones List */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 pt-2">
                  {valuationData.milestones.map((ms, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-xs text-white">{ms.milestone_name}</span>
                        <span className={`pill text-[10px] ${
                          ms.status === 'Completed' ? 'pill-compliant' : ms.status === 'In Progress' ? 'pill-moderate' : 'pill-info'
                        }`}>
                          {ms.status}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400">{ms.description}</p>
                      <div className="text-[10px] text-slate-500 font-mono">
                        Stage Weight: {ms.weight_percentage}% • Target: {ms.target_days} days
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* IS 456 Material Estimation Requirements */}
              <div className="glass-panel p-5 rounded-2xl space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Layers className="w-4 h-4 text-amber-400" />
                    <span>Material Quantity Estimation (IS 456 Norms)</span>
                  </h3>
                  <span className="mono-badge text-[10px] text-slate-400">Total Built-up: {Number(valuationData.built_up_sqft).toLocaleString()} sqft</span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800">
                    <span className="text-[10px] text-slate-400 uppercase">Reinforcement Steel</span>
                    <div className="text-lg font-bold text-white font-mono mt-0.5">
                      {valuationData.materials.steel_tonnes.toLocaleString()} <span className="text-xs text-amber-400">MT</span>
                    </div>
                    <span className="text-[10px] text-slate-500">~4.2 kg/sq.ft thumb rule</span>
                  </div>

                  <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800">
                    <span className="text-[10px] text-slate-400 uppercase">Portland Cement</span>
                    <div className="text-lg font-bold text-white font-mono mt-0.5">
                      {valuationData.materials.cement_bags.toLocaleString()} <span className="text-xs text-amber-400">Bags</span>
                    </div>
                    <span className="text-[10px] text-slate-500">50kg bags (~0.40 bags/sqft)</span>
                  </div>

                  <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800">
                    <span className="text-[10px] text-slate-400 uppercase">Aggregates & Sand</span>
                    <div className="text-lg font-bold text-white font-mono mt-0.5">
                      {valuationData.materials.sand_aggregate_cum.toLocaleString()} <span className="text-xs text-amber-400">Cu.m</span>
                    </div>
                    <span className="text-[10px] text-slate-500">Coarse (20/10mm) & Fine sand</span>
                  </div>

                  <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800">
                    <span className="text-[10px] text-slate-400 uppercase">Ready-Mix Concrete (RMC)</span>
                    <div className="text-lg font-bold text-white font-mono mt-0.5">
                      {valuationData.materials.rmc_cum.toLocaleString()} <span className="text-xs text-amber-400">Cu.m</span>
                    </div>
                    <span className="text-[10px] text-slate-500">Pumpable M25/M30/M40 grade</span>
                  </div>

                  <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800">
                    <span className="text-[10px] text-slate-400 uppercase">Masonry AAC Blocks</span>
                    <div className="text-lg font-bold text-white font-mono mt-0.5">
                      {valuationData.materials.bricks_blocks_units.toLocaleString()} <span className="text-xs text-amber-400">Units</span>
                    </div>
                    <span className="text-[10px] text-slate-500">Fly-ash blocks / Red bricks</span>
                  </div>

                  <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800">
                    <span className="text-[10px] text-slate-400 uppercase">Primer & Surface Paint</span>
                    <div className="text-lg font-bold text-white font-mono mt-0.5">
                      {valuationData.materials.paint_liters.toLocaleString()} <span className="text-xs text-amber-400">Liters</span>
                    </div>
                    <span className="text-[10px] text-slate-500">Weathercoat & Interior emulsion</span>
                  </div>
                </div>
              </div>

              {/* Conceptual 3D Architectural Rendering via Pollinations AI */}
              <div className="glass-panel p-5 rounded-2xl space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <ImageIcon className="w-4 h-4 text-purple-400" />
                    <span>Conceptual 3D Architectural Rendering (Pollinations / Flux AI)</span>
                  </h3>
                  <a
                    href={valuationData.architectural_image_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-cyan-400 hover:underline flex items-center gap-1"
                  >
                    <span>Full Resolution</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>

                <div className="relative rounded-xl overflow-hidden border border-slate-700 shadow-xl bg-slate-950">
                  <img
                    src={valuationData.architectural_image_url}
                    alt="Conceptual 3D Architectural Render"
                    className="w-full h-72 sm:h-96 object-cover hover:scale-105 transition-transform duration-700"
                    loading="lazy"
                  />
                  <div className="absolute bottom-0 inset-x-0 p-3 bg-gradient-to-t from-slate-950/90 via-slate-950/60 to-transparent text-[11px] text-slate-300">
                    <span className="text-amber-400 font-semibold">Generative AI Visualizer Prompt:</span> {valuationData.architectural_visualization_prompt}
                  </div>
                </div>
              </div>

              {/* Action Toolbar */}
              <div className="flex items-center justify-between pt-2">
                <div className="text-[11px] text-slate-400 font-mono">
                  Valuation Ref: {valuationData.calculation_id} • {valuationData.timestamp}
                </div>
                <button
                  onClick={handleDownloadReport}
                  className="btn-secondary text-xs flex items-center gap-2"
                >
                  <FileDown className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Download Valuation Report (.JSON)</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
