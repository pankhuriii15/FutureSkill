import React, { useState, useEffect } from 'react';
import { CloudLightning, Wind, CloudRain, Sun, ShieldAlert, Bot, Send, CheckSquare, Sparkles, RefreshCw, BookOpen, AlertTriangle } from 'lucide-react';

export default function DailySiteAssistantTab({ apiKey }) {
  // Weather state
  const [selectedCondition, setSelectedCondition] = useState('High Wind (>45 km/h)');
  const [sitePhase, setSitePhase] = useState('Concrete Pouring & Curing');
  const [tempCelsius, setTempCelsius] = useState(34);
  const [windKmh, setWindKmh] = useState(48);
  const [weatherData, setWeatherData] = useState(null);
  const [loadingWeather, setLoadingWeather] = useState(false);

  // Chatbot state
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I am StrucAI, your Principal Resident Construction Engineering Assistant. You can ask me regarding IS 456:2000 specifications, OSHA safety compliance, formwork stripping schedules, concrete mix proportions, or site troubleshooting protocols.',
      references: ['IS 456:2000', 'OSHA 1926'],
      timestamp: 'Just now'
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [loadingChat, setLoadingChat] = useState(false);

  // Fetch weather advisory on mount & change
  useEffect(() => {
    fetchWeatherAdvisory();
  }, [selectedCondition, sitePhase]);

  const fetchWeatherAdvisory = async () => {
    setLoadingWeather(true);
    try {
      const response = await fetch('/api/weather-advisory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          condition: selectedCondition,
          site_phase: sitePhase,
          temperature_celsius: Number(tempCelsius),
          wind_speed_kmh: Number(windKmh)
        })
      });
      if (response.ok) {
        const data = await response.json();
        setWeatherData(data);
      }
    } catch (err) {
      console.error('Weather advisory fetch error:', err);
    } finally {
      setLoadingWeather(false);
    }
  };

  const handleSendMessage = async (textToSend) => {
    const query = textToSend || inputQuery;
    if (!query.trim()) return;

    const newMessages = [...messages, { role: 'user', content: query, timestamp: 'Now' }];
    setMessages(newMessages);
    setInputQuery('');
    setLoadingChat(true);

    try {
      const response = await fetch('/api/site-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages.map(m => ({ role: m.role, content: m.content })),
          site_context: `Active Condition: ${selectedCondition}. Phase: ${sitePhase}. Ambient: ${tempCelsius}°C, Wind: ${windKmh} km/h`,
          api_key: apiKey || null
        })
      });

      if (response.ok) {
        const data = await response.json();
        setMessages([...newMessages, {
          role: 'assistant',
          content: data.reply,
          references: data.references || [],
          suggested_followups: data.suggested_followups || [],
          timestamp: 'Now'
        }]);
      } else {
        throw new Error('Chat service error');
      }
    } catch (err) {
      setMessages([...newMessages, {
        role: 'assistant',
        content: 'Per IS 456:2000, ensure all site activities adhere to approved quality assurance and safety inspection test plans. Please check network connectivity or retry your engineering query.',
        references: ['IS 456:2000'],
        timestamp: 'Now'
      }]);
    } finally {
      setLoadingChat(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl glass-panel border-purple-500/20 bg-gradient-to-r from-slate-900/90 via-slate-900/60 to-purple-950/20">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="pill pill-info">Epic 5: Daily Intelligence</span>
            <span className="text-xs text-slate-400">Weather-Aware Advisory & IS 456 Assistant</span>
          </div>
          <h2 className="text-xl lg:text-2xl font-extrabold text-white">
            Daily Site Assistant & Weather-Aware Advisory
          </h2>
          <p className="text-xs lg:text-sm text-slate-300 max-w-2xl mt-1">
            Real-time weather threat analysis with automatic crane suspension, electrical safety, and concrete curing directives, alongside an interactive construction engineering chatbot.
          </p>
        </div>
      </div>

      {/* Weather Condition Chips */}
      <div className="glass-panel p-5 rounded-2xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <label className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <CloudLightning className="w-4 h-4 text-amber-400" />
            <span>Select Simulated Weather Condition</span>
          </label>
          <span className="text-xs text-slate-400">
            Active Phase: <strong className="text-slate-200">{sitePhase}</strong>
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
          {[
            { label: 'High Wind (>45 km/h)', icon: Wind, color: 'text-amber-400' },
            { label: 'Heavy Rain / Monsoon', icon: CloudRain, color: 'text-cyan-400' },
            { label: 'Extreme Heat (>40°C)', icon: Sun, color: 'text-orange-400' },
            { label: 'Severe Thunderstorm', icon: CloudLightning, color: 'text-red-400' },
            { label: 'Normal / Mild', icon: Sparkles, color: 'text-emerald-400' }
          ].map((item) => {
            const Icon = item.icon;
            const isSelected = selectedCondition === item.label;
            return (
              <button
                key={item.label}
                onClick={() => {
                  setSelectedCondition(item.label);
                  if (item.label.includes('Wind')) setWindKmh(52);
                  if (item.label.includes('Heat')) setTempCelsius(42);
                }}
                className={`p-3 rounded-xl border flex flex-col items-center gap-2 text-center transition ${
                  isSelected
                    ? 'bg-amber-500/15 border-amber-500/60 shadow-lg shadow-amber-500/10'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 text-slate-400'
                }`}
              >
                <Icon className={`w-5 h-5 ${item.color}`} />
                <span className={`text-xs font-semibold ${isSelected ? 'text-white' : 'text-slate-300'}`}>
                  {item.label}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Dynamic Weather Protocol Alerts */}
      {weatherData && (
        <div className="space-y-4 animate-fadeIn">
          {/* Headline Alert Banner */}
          <div className={`p-4 rounded-2xl border flex items-start gap-3 ${
            weatherData.risk_level === 'Critical' || weatherData.risk_level === 'High'
              ? 'bg-red-500/15 border-red-500/30 text-red-200'
              : weatherData.risk_level === 'Moderate'
              ? 'bg-amber-500/15 border-amber-500/30 text-amber-200'
              : 'bg-emerald-500/15 border-emerald-500/30 text-emerald-200'
          }`}>
            <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5 text-amber-400" />
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-sm text-white">{weatherData.weather_headline}</span>
                <span className="pill pill-critical text-[10px]">{weatherData.operational_status}</span>
              </div>
              <p className="text-xs text-slate-300 mt-1">
                Risk Classification: <strong className="text-white">{weatherData.risk_level}</strong> • Updated at: {weatherData.timestamp}
              </p>
            </div>
          </div>

          {/* Protocols Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {weatherData.safety_protocols.map((protocol, idx) => (
              <div key={idx} className="glass-panel p-4 rounded-xl space-y-2 border-slate-800">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">{protocol.category}</span>
                  <span className={`pill text-[9px] ${
                    protocol.action_level === 'HALT OPERATION' ? 'pill-critical' : protocol.action_level === 'RESTRICTED PROTOCOL' ? 'pill-moderate' : 'pill-compliant'
                  }`}>
                    {protocol.action_level}
                  </span>
                </div>
                <h4 className="text-xs font-bold text-white">{protocol.protocol_title}</h4>
                <p className="text-[11px] text-slate-300 leading-relaxed">{protocol.detailed_procedure}</p>
                <div className="text-[10px] text-slate-500 font-mono pt-1">
                  Standard: {protocol.code_reference}
                </div>
              </div>
            ))}
          </div>

          {/* Concrete & Crane Specific Directive Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1.5">
              <span className="text-xs font-bold text-amber-400 flex items-center gap-1.5">
                <Wind className="w-4 h-4" />
                <span>Crane & Rigging Operating Mandate</span>
              </span>
              <p className="text-xs text-slate-300 leading-relaxed">{weatherData.crane_lifting_advisory}</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1.5">
              <span className="text-xs font-bold text-cyan-400 flex items-center gap-1.5">
                <CloudRain className="w-4 h-4" />
                <span>IS 456 Concrete Curing & Pouring Protocol</span>
              </span>
              <p className="text-xs text-slate-300 leading-relaxed">{weatherData.concrete_curing_advisory}</p>
            </div>
          </div>
        </div>
      )}

      {/* Interactive Multi-turn Site Chatbot Section */}
      <div className="glass-panel p-5 rounded-2xl space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-purple-500/15 border border-purple-500/30 text-purple-400">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">StrucAI: Construction Engineering Assistant</h3>
              <p className="text-[11px] text-slate-400">IS 456:2000, OSHA 1926, and National Building Code 2016 Knowledge Base</p>
            </div>
          </div>
          <span className="mono-badge text-[10px] text-purple-400">Multi-Turn Active</span>
        </div>

        {/* Quick Suggested Prompt Chips */}
        <div className="flex flex-wrap gap-1.5">
          {[
            'Formwork stripping times per IS 456 Clause 11.3?',
            'What is the minimum curing duration for OPC vs PPC concrete?',
            'What is the water-cement ratio for M25 / M30 design mix?',
            'How is development length (Ld) calculated for Fe 500 rebar?',
            'Maximum allowable concrete crack width under IS 456?'
          ].map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(prompt)}
              className="text-[11px] px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 transition"
            >
              {prompt}
            </button>
          ))}
        </div>

        {/* Messages Stream */}
        <div className="h-80 overflow-y-auto space-y-3 p-4 rounded-xl bg-slate-950/70 border border-slate-800">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-2xl p-3.5 text-xs leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-amber-500 text-slate-950 font-medium'
                    : 'bg-slate-900 border border-slate-800 text-slate-200'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {msg.references && msg.references.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-slate-800 flex flex-wrap gap-1 items-center text-[10px]">
                    <span className="text-slate-400 font-semibold">Citations:</span>
                    {msg.references.map((ref, rIdx) => (
                      <span key={rIdx} className="mono-badge text-cyan-400">{ref}</span>
                    ))}
                  </div>
                )}
              </div>
              <span className="text-[9px] text-slate-500 mt-0.5 px-1">{msg.timestamp}</span>
            </div>
          ))}

          {loadingChat && (
            <div className="flex items-center gap-2 text-xs text-purple-400 p-2">
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              <span>StrucAI is consulting IS codes and engineering standards...</span>
            </div>
          )}
        </div>

        {/* Input Field */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder="Ask about IS 456 clauses, rebar lap lengths, dewatering, curing protocols..."
            className="flex-1 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
          />
          <button
            type="submit"
            disabled={loadingChat || !inputQuery.trim()}
            className="btn-primary px-4 py-2.5 bg-gradient-to-r from-purple-500 to-indigo-600 text-white shadow-purple-500/25"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
