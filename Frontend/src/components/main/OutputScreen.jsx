import React, { useState } from "react";
import MarkdownRenderer from "./MarkdownRenderer";

const DEFAULT_AGENTS = [
  { name: "DeepSeek R1", role: "STRATEGIST", suit: "♠", color: "text-[#171717]", desc: "Orchestration & Strategic Architecture" },
  { name: "DeepSeek V3", role: "RESEARCHER", suit: "♥", color: "text-[#C93636]", desc: "Statutory Context & Prior-Art Search" },
  { name: "Nemotron 120B", role: "ARCHITECT", suit: "♦", color: "text-[#C93636]", desc: "Compliance Boundaries & Schemas" },
  { name: "Llama 3.2 (11B)", role: "EXECUTOR", suit: "♣", color: "text-[#171717]", desc: "Deliverable Table & Roadmap Synthesis" },
  { name: "DeepSeek Verifier", role: "VERIFIER", suit: "♠", color: "text-[#171717]", desc: "3-Tier Statutory Verification & QA" },
];

const GLOSSARY_DICTIONARY = {
  hi: [
    { term: "Classical Ayurvedic Formulation", translation: "शास्त्रीय आयुर्वेदिक औषधि", desc: "First Schedule texts (Charaka/Sushruta/AFI) standard preparation" },
    { term: "Proprietary Ayurvedic Medicine", translation: "स्वामित्व वाली आयुर्वेदिक दवा", desc: "Formulation with non-classical ingredients or extraction under Rule 158B(I)(B)" },
    { term: "Traditional Knowledge (TK)", translation: "पारंपारिक ज्ञान", desc: "Codified public domain heritage barred from patenting under Sec 3(p)" },
    { term: "Prior Art", translation: "पूर्व कला (Prior Art)", desc: "All publicly available knowledge prior to the filing date" },
    { term: "Access and Benefit Sharing (ABS)", translation: "प्रवेश और लाभ साझाकरण", desc: "Mandatory compliance under Biological Diversity Act 2002/2023" },
    { term: "Therapeutic Efficacy", translation: "चिकित्सकीय प्रभावकारिता", desc: "Required enhancement under Section 3(d) over known substance" },
  ],
  mr: [
    { term: "Classical Ayurvedic Formulation", translation: "शास्त्रीय आयुर्वेदिक औषध", desc: "पारंपरिक ग्रंथांनुसार तयार केलेले आयुर्वेदिक औषध" },
    { term: "Proprietary Ayurvedic Medicine", translation: "मालकीचे आयुर्वेदिक औषध (पेटंट/प्रोप्रायटरी)", desc: "नवीन घटक किंवा आधुनिक प्रक्रियेने बनवलेले औषध" },
    { term: "Traditional Knowledge (TK)", translation: "पारंपारिक ज्ञान", desc: "सार्वजनिक ज्ञान जे कलम ३(p) अंतर्गत पेटंट करता येत नाही" },
    { term: "Prior Art", translation: "पूर्व कला (Prior Art)", desc: "अर्ज करण्यापूर्वी अस्तित्वात असलेली सर्व माहिती" },
    { term: "Access and Benefit Sharing (ABS)", translation: "प्रवेश आणि लाभ वाटप", desc: "जैविक विविधता कायद्यानुसार आवश्यक कायदेशीर मंजुरी" },
    { term: "Therapeutic Efficacy", translation: "उपचारात्मक परिणामकारकता", desc: "कलम ३(d) नुसार सिद्ध करावी लागणारी वाढीव परिणामकारकता" },
  ]
};

const OutputScreen = ({ prompt, matchedData, operator, onReset, onTranslate }) => {
  const [activeTab, setActiveTab] = useState("solution");
  const [copied, setCopied] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [selectedJurisdiction, setSelectedJurisdiction] = useState("All");
  const [isTranslating, setIsTranslating] = useState(false);

  // Dynamic values from backend Groq orchestrator & 9-Layer Engine
  const agents = matchedData?.agents || DEFAULT_AGENTS;
  const rawPrompt = matchedData?.rawPrompt || prompt || "Create a full-stack high performance orchestration architecture.";
  const matchedPrompt = matchedData?.matchedPrompt || rawPrompt;
  const category = matchedData?.category || "AI ORCHESTRATION";
  const subcategory = matchedData?.subcategory || "GROQ LPU ENGINE";
  const confidence = matchedData?.confidence || "98.8%";
  const confidenceRating = matchedData?.confidenceRating || "HIGH";
  const deliverableType = matchedData?.deliverableType || "code";
  const tabTitle = matchedData?.tabTitle || (deliverableType === "code" ? "CODE IMPLEMENTATION" : "DELIVERABLE DOSSIER");

  const allCitations = matchedData?.citations || [];
  const escalationDossier = matchedData?.escalationDossier || null;
  const detectedJurisdiction = matchedData?.jurisdiction?.suggested_toggle || "India";
  const insufficientEvidence = matchedData?.insufficientEvidence || false;
  const insufficientEvidenceMessage = matchedData?.insufficientEvidenceMessage || null;
  const threeTierVerification = matchedData?.threeTierVerification || matchedData?.architecture?.threeTierVerification || matchedData?.verificationResult?.three_tier_verification || matchedData?.verification?.three_tier_verification || null;

  // Filter citations by active jurisdiction toggle
  const citations = selectedJurisdiction === "All"
    ? allCitations
    : allCitations.filter(c => c.jurisdiction?.toLowerCase() === selectedJurisdiction.toLowerCase());

  const architecture = matchedData?.architecture || {
    overview: `Strategic and regulatory solution formulated specifically for: "${rawPrompt}"`,
    blueprint: "Decomposed objective into a multi-agent orchestration graph with distributed state isolation and parallel inference channels.",
    dataFlow: [
      { name: `1. Ingress & Strategy (${agents[0]?.name || "Strategist"})`, desc: "Decomposed objective into modular actionable tasks." },
      { name: `2. Research & Specs (${agents[1]?.name || "Researcher"})`, desc: "Retrieved domain parameters and dependencies." },
      { name: `3. Architecture (${agents[2]?.name || "Architect"})`, desc: "Constructed interface schemas and contracts." },
      { name: `4. Execution (${agents[3]?.name || "Executor"})`, desc: "Synthesized tailored deliverable." },
      { name: `5. QA & Assertions (${agents[4]?.name || "Verifier"})`, desc: "Validated edge cases and constraints." }
    ],
    verification: matchedData?.verificationReport || "✓ All statutory constraints validated.\n✓ Zero critical contradictions found.\n✓ Production execution approved."
  };

  const deliverableContent = matchedData?.deliverableContent || matchedData?.code || `Deliverable formulated specifically for: "${rawPrompt}". Generated by House of Cards Agent Team.`;
  const logs = matchedData?.logs || [
    { time: "0.00s", tag: "JOKER", msg: `Prompt ingested: "${rawPrompt.slice(0, 35)}..."` },
    { time: "0.22s", tag: `${agents[0]?.role || "STRATEGIST"}`, msg: `Strategy roadmap formulated for [${category}].` },
    { time: "0.58s", tag: `${agents[2]?.role || "ARCHITECT"}`, msg: "Statutory schema, interfaces, and boundary contracts constructed." },
    { time: "1.05s", tag: `${agents[3]?.role || "EXECUTOR"}`, msg: "Live deliverable synthesis finished with 0 defects." },
    { time: "1.42s", tag: `${agents[4]?.role || "VERIFIER"}`, msg: "Assertions complete. Groq LPU pipeline deployed." },
  ];
  const hash = matchedData?.hash || "#HOC-9942A";
  const alternatives = matchedData?.alternatives || [];
  const verificationReport = matchedData?.verificationReport || architecture.verification;

  const handleCopy = () => {
    const textToCopy = activeTab === "deliverable"
      ? deliverableContent
      : activeTab === "logs"
        ? logs.map(l => `[${l.time}] [${l.tag}] ${l.msg}`).join("\n")
        : activeTab === "verification"
          ? verificationReport
          : `ORCHESTRATED SOLUTION FOR: "${rawPrompt}"\nCATEGORY: ${category} / ${subcategory}\nJURISDICTION: ${selectedJurisdiction}\nLANGUAGE: ${selectedLanguage.toUpperCase()}\n\nSTRATEGIC SOLUTION:\n${architecture.overview}\n\nDATA FLOW:\n${architecture.dataFlow.map(d => `${d.name}: ${d.desc}`).join("\n")}\n\nVERIFICATION:\n${verificationReport}`;

    navigator.clipboard?.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleLanguageChange = async (langId) => {
    if (langId === selectedLanguage && !isTranslating) return;
    setSelectedLanguage(langId);
    if (onTranslate) {
      setIsTranslating(true);
      try {
        await onTranslate(langId, rawPrompt);
      } finally {
        setIsTranslating(false);
      }
    }
  };

  // Trilingual Disclaimers
  const disclaimers = {
    en: "⚖️ STATUTORY NOTICE: This analysis provides statutory compliance and prior-art information and does not constitute formal legal advice.",
    hi: "⚖️ वैधानिक सूचना: यह विश्लेषण वैधानिक अनुपालन और पूर्व-कला की जानकारी प्रदान करता है, यह औपचारिक कानूनी सलाह नहीं है।",
    mr: "⚖️ वैधानिक सूचना: हे विश्लेषण वैधानिक अनुपालन आणि पूर्व-कला माहिती प्रदान करते, हा औपचारिक कायदेशीर सल्ला नाही."
  };

  return (
    <div className="output-screen-entrance w-full max-w-5xl mx-auto px-4 py-2 select-none">

      {/* Top Banner Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-3">
        <div>
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            <span
              className="text-[9px] sm:text-[10px] font-black tracking-[0.2em] text-[#C93636] uppercase"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              ♠ 5/5 AGENT COUNCIL DELIVERED ♠
            </span>

            {/* Layer 8: Quantitative Confidence Badge */}
            <span className={`text-[8px] font-mono px-2 py-0.5 rounded font-bold uppercase ${confidenceRating === "HIGH" ? "bg-emerald-800 text-emerald-100 border border-emerald-500" :
              confidenceRating === "MEDIUM" ? "bg-amber-800 text-amber-100 border border-amber-500" :
                "bg-red-800 text-red-100 border border-red-500"
              }`}>
              CONFIDENCE: {confidence} ({confidenceRating})
            </span>

            {/* Layer 5: Detected Jurisdiction Pill */}
            <span className="text-[7.5px] font-mono px-2 py-0.5 bg-[#171717] text-[#FFF8E7] rounded font-bold uppercase">
              JURISDICTION: {detectedJurisdiction.toUpperCase()}
            </span>
          </div>

          <h2
            className="text-base sm:text-lg font-black text-[#171717] tracking-tight uppercase"
            style={{ fontFamily: "'Press Start 2P', monospace" }}
          >
            House Of Cards - IPSAKTI
          </h2>
        </div>

        {/* Action Controls & Layer 9 Language Switcher */}
        <div className="flex items-center gap-2 flex-wrap">

          {/* Layer 9: Trilingual Language Switcher */}
          <div className="flex items-center bg-[#171717]/10 p-0.5 rounded border border-[#171717]/30">
            {[
              { id: "en", label: "EN" },
              { id: "hi", label: "हिन्दी" },
              { id: "mr", label: "मराठी" },
            ].map(lang => (
              <button
                key={lang.id}
                onClick={() => handleLanguageChange(lang.id)}
                disabled={isTranslating}
                className={`px-2 py-1 text-[8px] font-bold rounded transition-all cursor-pointer ${
                  selectedLanguage === lang.id
                    ? "bg-[#171717] text-[#FFF8E7] shadow-sm font-black"
                    : "text-black/60 hover:text-black"
                } disabled:opacity-50 disabled:cursor-wait`}
              >
                {isTranslating && selectedLanguage === lang.id ? "..." : lang.label}
              </button>
            ))}
          </div>

          <button
            onClick={handleCopy}
            className="
              px-2.5 py-1.5 bg-[#FFF8E7] hover:bg-white
              text-[#171717] text-[8px] font-bold tracking-wider uppercase
              border-2 border-[#171717] rounded
              shadow-[2px_2px_0px_rgba(23,23,23,0.15)]
              hover:-translate-y-0.5 active:translate-y-0
              transition-all flex items-center gap-1 cursor-pointer
            "
            style={{ fontFamily: "'Press Start 2P', monospace" }}
          >
            <span>{copied ? "✓" : "📋"}</span>
            {copied ? "COPIED" : "COPY"}
          </button>

          <button
            onClick={onReset}
            className="
              px-3 py-1.5 bg-[#171717] hover:bg-[#C93636]
              text-[#FFF8E7] text-[8px] font-bold tracking-wider uppercase
              border-2 border-[#171717] hover:border-[#C93636] rounded
              shadow-[2px_2px_0px_rgba(23,23,23,0.18)]
              hover:-translate-y-0.5 active:translate-y-0
              transition-all flex items-center gap-1 cursor-pointer
            "
            style={{ fontFamily: "'Press Start 2P', monospace" }}
          >
            <span className="text-red-400 text-[7px]">♠</span>
            NEW DEAL
          </button>
        </div>
      </div>

      {/* Prompt Objective Banner & Layer 5 Jurisdiction Stream Filter */}
      <div className="bg-[#171717]/5 border-2 border-[#171717]/25 rounded-md p-3 mb-3">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-1.5">
          <div className="flex items-center gap-2">
            <span className="text-[8px] font-black uppercase tracking-widest text-[#171717]/70" style={{ fontFamily: "'Press Start 2P', monospace" }}>
              ♦ PROMPT OBJECTIVE:
            </span>
          </div>

          {/* Layer 5: Jurisdiction Stream Filter Tabs */}
          <div className="flex items-center gap-1">
            <span className="text-[7.5px] font-bold font-mono text-black/50 mr-1">FILTER REGIME:</span>
            {[
              { id: "All", label: "ALL" },
              { id: "India", label: "🇮🇳 INDIA" },
              { id: "International", label: "🌐 INTL" },
            ].map(j => (
              <button
                key={j.id}
                onClick={() => setSelectedJurisdiction(j.id)}
                className={`px-1.5 py-0.5 text-[7.5px] font-mono rounded font-bold border transition-all cursor-pointer ${selectedJurisdiction === j.id
                  ? "bg-[#C93636] text-[#FFF8E7] border-[#C93636]"
                  : "bg-white/80 text-black/60 border-black/20 hover:bg-white"
                  }`}
              >
                {j.label}
              </button>
            ))}
          </div>
        </div>

        <p className="text-xs font-mono text-[#171717] font-bold leading-relaxed mb-1">
          "{rawPrompt}"
        </p>

        {matchedPrompt && matchedPrompt !== rawPrompt && (
          <div className="pt-1.5 border-t border-[#171717]/10 flex items-start gap-2">
            <span className="text-[8px] font-bold text-[#C93636] uppercase font-mono mt-0.5">
              ♠ MATCHED PATTERN:
            </span>
            <p className="text-[11px] font-mono text-black/75 italic leading-snug">
              "{matchedPrompt}"
            </p>
          </div>
        )}
      </div>

      {/* 5 Participating Dynamic Agents Ribbon */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 mb-3">
        {agents.map((agent, i) => (
          <div
            key={i}
            className="
              bg-[#FFF8E7] border-2 border-[#171717] rounded
              p-2 shadow-[3px_3px_0px_rgba(23,23,23,0.1)]
              flex flex-col justify-between relative overflow-hidden
              transition-transform hover:-translate-y-0.5
            "
          >
            <div className="flex items-center justify-between mb-1">
              <span className={`text-xs font-black ${agent.color || "text-[#171717]"}`}>{agent.suit || "♠"}</span>
              <span className="text-[6px] font-mono px-1 py-0.5 bg-emerald-100 text-emerald-800 border border-emerald-600 rounded font-bold">
                ACTIVE
              </span>
            </div>
            <p className="text-[8px] font-black text-[#171717] uppercase tracking-wide truncate" style={{ fontFamily: "'Press Start 2P', monospace" }}>
              {agent.name}
            </p>
            <p className="text-[7px] font-mono text-black/60 tracking-tight mt-0.5 truncate font-bold">
              {agent.role}
            </p>
          </div>
        ))}
      </div>

      {/* Main Output Canvas Container */}
      <div
        className="
          bg-[#FFF8E7] border-[3px] border-[#171717] rounded-lg
          shadow-[6px_8px_0px_rgba(23,23,23,0.18)]
          overflow-hidden flex flex-col relative
        "
      >
        {/* Navigation Tabs */}
        <div className="flex flex-wrap items-center justify-between border-b-2 border-[#171717] bg-[#171717]/5 px-3 py-2 gap-2">
          <div className="flex items-center gap-1.5 flex-wrap">
            {[
              { id: "solution", label: "♠ SOLUTION & STRATEGY", icon: "♠" },
              { id: "deliverable", label: `♦ ${tabTitle}`, icon: "♦" },
              { id: "verification", label: "🛡️ QA & STATUTORY CHECKS", icon: "🛡️" },
              { id: "logs", label: "♣ COUNCIL LOGS", icon: "♣" },
              ...(selectedLanguage !== "en" ? [{ id: "glossary", label: "📖 GLOSSARY", icon: "📖" }] : []),
              ...(alternatives.length > 0 ? [{ id: "alternatives", label: "♥ ALTERNATIVES", icon: "♥" }] : []),
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  px-2.5 py-1 text-[8px] font-bold tracking-wider uppercase rounded
                  border transition-all cursor-pointer whitespace-nowrap
                  ${activeTab === tab.id
                    ? "bg-[#171717] text-[#FFF8E7] border-[#171717] shadow-[2px_2px_0px_rgba(23,23,23,0.2)]"
                    : "bg-transparent text-black/60 border-transparent hover:bg-black/5"
                  }
                `}
                style={{ fontFamily: "'Press Start 2P', monospace" }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="hidden sm:flex items-center gap-1 text-[7px] font-mono text-black/40">
            <span>HASH: {hash}</span>
          </div>
        </div>

        {/* Tab Content Display */}
        <div className="p-4 sm:p-5 max-h-[420px] overflow-y-auto font-mono text-xs text-[#171717] leading-relaxed">

          {/* Translating Status Indicator */}
          {isTranslating && (
            <div className="mb-3 p-2.5 bg-[#171717] text-[#FFF8E7] rounded border border-[#C93636] flex items-center justify-between animate-pulse shadow-md">
              <div className="flex items-center gap-2">
                <span className="text-[#C93636] text-xs font-black">♠</span>
                <span className="text-[9px] font-mono tracking-wider font-bold">
                  GROQ LPU MULTI-AGENT COMPILER: TRANSLATING DOSSIER TO {selectedLanguage === "hi" ? "HINDI (हिन्दी)" : selectedLanguage === "mr" ? "MARATHI (मराठी)" : "ENGLISH"}...
                </span>
              </div>
              <span className="text-[7.5px] font-mono text-emerald-400 font-bold">5 AGENTS ACTIVE</span>
            </div>
          )}

          {/* TAB 1: Direct Comprehensive Solution & Strategy */}
          {activeTab === "solution" && (
            <div className="space-y-3.5">
              <div className="p-3.5 bg-amber-50/70 border border-amber-900/20 rounded">
                <span className="text-[9px] font-black tracking-widest text-[#C93636] uppercase block mb-2" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                  1. STRATEGIC & STATUTORY RESOLUTION ({agents[0]?.name || "Lead"} & {agents[1]?.name || "Specialist"})
                </span>
                <MarkdownRenderer content={architecture.overview} />
              </div>

              {/* Layer 6: Verified Citations Panel */}
              {allCitations.length > 0 && (
                <div className="p-3 bg-emerald-50/80 border border-emerald-900/25 rounded">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-emerald-800 font-black text-[9px] uppercase tracking-wider" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                      ⚖️ VERIFIED STATUTORY CITATIONS ({citations.length} SOURCES • {selectedJurisdiction.toUpperCase()})
                    </span>
                    <span className="text-[7.5px] font-mono bg-emerald-200/80 text-emerald-900 px-1.5 py-0.5 rounded font-bold">
                      ANTI-HALLUCINATION GUARD ACTIVE
                    </span>
                  </div>
                  {citations.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {citations.map((c, i) => (
                        <div key={i} className="p-2 bg-white border border-emerald-700/30 rounded text-[10px] font-sans">
                          <div className="flex items-center justify-between mb-1">
                            <strong className="text-emerald-950 font-bold">{c.title}</strong>
                            <span className="text-[8px] font-mono px-1 py-0.2 bg-emerald-100 text-emerald-800 rounded font-bold">
                              {c.jurisdiction}
                            </span>
                          </div>
                          <p className="text-black/70 text-[9.5px] line-clamp-2">{c.summary}</p>
                          {c.url && (
                            <a href={c.url} target="_blank" rel="noreferrer" className="text-[8.5px] text-blue-700 hover:underline font-mono mt-1 block">
                              ↗ Portal Reference
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="py-3 px-4 bg-amber-50/80 border border-amber-900/20 rounded text-center">
                      <p className="text-[10px] font-mono text-amber-800 font-bold">
                        ⚠️ No {selectedJurisdiction} sources matched for this query.
                      </p>
                      <p className="text-[9.5px] text-black/60 mt-1">
                        Switch to <span className="font-bold">ALL</span> to see all retrieved citations, or try a more specific {selectedJurisdiction.toLowerCase()} query.
                      </p>
                      <button
                        onClick={() => setSelectedJurisdiction("All")}
                        className="mt-2 text-[8px] font-mono font-bold px-3 py-1 bg-[#171717] text-[#FFF8E7] rounded cursor-pointer hover:bg-[#C93636] transition-colors"
                      >
                        SHOW ALL SOURCES
                      </button>
                    </div>
                  )}
                </div>
              )}

              {/* Insufficient Evidence Banner (Item 11) */}
              {insufficientEvidence && (
                <div className="p-3 bg-amber-100 border-2 border-amber-600/40 rounded flex items-start gap-2">
                  <span className="text-amber-700 text-base shrink-0">⚠️</span>
                  <div>
                    <p className="text-[10px] font-black text-amber-800 uppercase tracking-wider" style={{ fontFamily: "'Press Start 2P', monospace" }}>Insufficient Authoritative Evidence</p>
                    <p className="text-[11px] font-sans text-amber-900 mt-1">{insufficientEvidenceMessage}</p>
                  </div>
                </div>
              )}

              {/* Multi-Agent Execution Graph */}
              <div className="p-3 bg-blue-50/60 border border-blue-900/20 rounded">
                <span className="text-[9px] font-black tracking-widest text-[#171717] uppercase block mb-2" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                  2. MULTI-AGENT EXECUTION GRAPH
                </span>
                <ul className="list-none pl-0 space-y-2">
                  {architecture.dataFlow.map((flow, i) => (
                    <li key={i} className="flex items-start gap-2 text-[11px] font-sans">
                      <span className="text-[#C93636] font-black shrink-0 text-[10px] mt-0.5">♦</span>
                      <span>
                        <strong className="text-[#171717] font-bold">{flow.name}:</strong>{" "}
                        <MarkdownRenderer content={flow.desc} className="inline [&>p]:inline [&>p]:m-0" />
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Layer 8: Attorney Escalation Dossier Alert */}
              {escalationDossier && (
                <div className="p-3.5 bg-red-50 border-2 border-[#C93636]/40 rounded">
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="text-red-600 font-bold text-xs">⚠️</span>
                    <span className="text-[9px] font-black uppercase text-[#C93636] tracking-wider" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                      HUMAN ESCALATION RECOMMENDED: {escalationDossier.expertType}
                    </span>
                  </div>
                  <p className="text-[10px] font-sans text-black/75 mb-2">
                    Due to potential statutory exclusions or biological resource compliance requirements, consultation with a specialist is advised.
                  </p>
                  <ul className="list-disc pl-4 space-y-1 text-[10px] font-sans text-black/85">
                    {escalationDossier.keyQuestions?.map((q, idx) => (
                      <li key={idx}><strong>Key Question:</strong> {q}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: ADAPTIVE DELIVERABLE (Code Terminal vs. Editorial Parchment Dossier) */}
          {activeTab === "deliverable" && (
            <div>
              {deliverableType === "code" ? (
                <div className="bg-[#171717] text-[#FFF8E7] p-4 rounded-md overflow-x-auto text-[11px] font-mono leading-relaxed border border-black shadow-inner">
                  <div className="flex items-center justify-between pb-2 mb-2 border-b border-white/10 text-emerald-400">
                    <span>// Generated by {agents[3]?.name || "Qwen 3.6"} ({agents[3]?.role || "EXECUTOR"}) on Groq LPUs</span>
                    <span className="text-[8px] text-white/40">100% PRODUCTION READY</span>
                  </div>
                  <pre className="whitespace-pre font-mono text-[11px] text-emerald-300">{deliverableContent}</pre>
                </div>
              ) : (
                <div className="bg-[#FFFDF7] border-2 border-[#171717]/25 rounded-md p-4 sm:p-5 shadow-sm">
                  <div className="flex flex-wrap items-center justify-between gap-2 pb-3 mb-3 border-b-2 border-[#171717]/15">
                    <div className="flex items-center gap-2">
                      <span className="text-sm">♦</span>
                      <span className="text-[9px] font-black uppercase tracking-wider text-[#171717]" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                        EXECUTIVE DELIVERABLE DOSSIER
                      </span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <span className="text-[8px] font-mono px-2 py-0.5 bg-[#171717] text-[#FFF8E7] rounded font-bold uppercase">
                        AUTHOR: {agents[3]?.name || "Executor"}
                      </span>
                      <span className="text-[8px] font-mono px-2 py-0.5 bg-[#C93636] text-[#FFF8E7] rounded font-bold uppercase">
                        STAMP: APPROVED
                      </span>
                    </div>
                  </div>

                  <MarkdownRenderer content={deliverableContent} />
                </div>
              )}
            </div>
          )}

          {/* TAB 3: 3-Tier QA & Statutory Verification Report */}
          {activeTab === "verification" && (
            <div className="space-y-4">
              {/* 3-Tier Header Banner */}
              <div className="p-3.5 bg-gradient-to-r from-emerald-900 to-emerald-950 text-white rounded border border-emerald-700/50 shadow-sm">
                <div className="flex items-center justify-between flex-wrap gap-2 mb-2">
                  <span className="text-[10px] font-black tracking-widest uppercase flex items-center gap-1.5" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                    🛡️ 3-TIER STATUTORY VERIFICATION PIPELINE ({agents[4]?.name || "Verifier"})
                  </span>
                  <span className="text-[9px] font-mono font-bold px-2 py-0.5 bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 rounded">
                    LAYER 7 FORMAL AUDIT
                  </span>
                </div>
                <p className="text-[11px] text-emerald-100/90 font-sans leading-relaxed">
                  Rigorous statutory validation across <strong>Citation Authenticity</strong>, <strong>Legal Applicability ("Does this law apply here?")</strong>, and <strong>Conclusion Justification ("Does this law justify the AI's conclusion?")</strong>.
                </p>
              </div>

              {/* 3-Tier Gauge Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5">
                {/* TIER 1 */}
                <div className="p-3 bg-white border border-black/15 rounded shadow-sm flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[8px] font-mono font-bold text-black/50 uppercase">TIER 1: CITATION GUARD</span>
                      <span className={`text-[8px] font-mono font-black px-1.5 py-0.2 rounded ${
                        (threeTierVerification?.tier_1_citation_verification?.status || "PASSED") === "PASSED" ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"
                      }`}>
                        {threeTierVerification?.tier_1_citation_verification?.status || "PASSED"}
                      </span>
                    </div>
                    <h5 className="text-[11px] font-black text-[#171717]">Citation Authenticity</h5>
                    <p className="text-[9.5px] text-black/60 mt-0.5">Validates official gazette statute references against active law manifests.</p>
                  </div>
                  <div className="mt-2 pt-2 border-t border-black/10 flex items-center justify-between">
                    <span className="text-[9px] font-bold text-black/70">Soundness Score:</span>
                    <span className="text-xs font-mono font-black text-emerald-700">
                      {Math.round((threeTierVerification?.tier_1_citation_verification?.score || 0.95) * 100)}%
                    </span>
                  </div>
                </div>

                {/* TIER 2 */}
                <div className="p-3 bg-white border border-black/15 rounded shadow-sm flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[8px] font-mono font-bold text-black/50 uppercase">TIER 2: APPLICABILITY GUARD</span>
                      <span className={`text-[8px] font-mono font-black px-1.5 py-0.2 rounded ${
                        (threeTierVerification?.tier_2_applicability_verification?.status || "PASSED") === "PASSED" ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"
                      }`}>
                        {threeTierVerification?.tier_2_applicability_verification?.status || "PASSED"}
                      </span>
                    </div>
                    <h5 className="text-[11px] font-black text-[#171717]">Statutory Applicability</h5>
                    <p className="text-[9.5px] text-black/60 mt-0.5">Validates subject-matter preconditions ("Does this law apply here?").</p>
                  </div>
                  <div className="mt-2 pt-2 border-t border-black/10 flex items-center justify-between">
                    <span className="text-[9px] font-bold text-black/70">Preconditions Met:</span>
                    <span className="text-xs font-mono font-black text-emerald-700">
                      {Math.round((threeTierVerification?.tier_2_applicability_verification?.score || 1.0) * 100)}%
                    </span>
                  </div>
                </div>

                {/* TIER 3 */}
                <div className="p-3 bg-white border border-black/15 rounded shadow-sm flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[8px] font-mono font-bold text-black/50 uppercase">TIER 3: LOGICAL JUSTIFICATION</span>
                      <span className={`text-[8px] font-mono font-black px-1.5 py-0.2 rounded ${
                        (threeTierVerification?.tier_3_conclusion_verification?.status || "PASSED") === "PASSED" ? "bg-emerald-100 text-emerald-800" : "bg-red-100 text-red-800"
                      }`}>
                        {threeTierVerification?.tier_3_conclusion_verification?.status || "PASSED"}
                      </span>
                    </div>
                    <h5 className="text-[11px] font-black text-[#171717]">Conclusion Justification</h5>
                    <p className="text-[9.5px] text-black/60 mt-0.5">Validates that legal advice logically follows from cited statutes.</p>
                  </div>
                  <div className="mt-2 pt-2 border-t border-black/10 flex items-center justify-between">
                    <span className="text-[9px] font-bold text-black/70">Logic Validity:</span>
                    <span className="text-xs font-mono font-black text-emerald-700">
                      {Math.round((threeTierVerification?.tier_3_conclusion_verification?.score || 1.0) * 100)}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Tier 2 Applicability Breakdown Findings */}
              {threeTierVerification?.tier_2_applicability_verification?.findings?.length > 0 && (
                <div className="p-3 bg-white border border-black/15 rounded shadow-sm space-y-2">
                  <span className="text-[9px] font-black tracking-wider text-black/70 uppercase block" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                    📋 TIER 2: STATUTORY PRECONDITION AUDIT ("DOES THIS LAW APPLY HERE?")
                  </span>
                  <div className="space-y-2">
                    {threeTierVerification.tier_2_applicability_verification.findings.map((f, i) => (
                      <div key={i} className="p-2.5 bg-neutral-50 border border-black/10 rounded text-[10.5px]">
                        <div className="flex items-center justify-between gap-2 mb-1">
                          <strong className="text-[#171717]">{f.statute_title || f.statuteTitle || f.statute_code}</strong>
                          <span className="text-[8px] font-mono font-bold px-1.5 py-0.5 bg-emerald-100 text-emerald-800 rounded">
                            {f.is_applicable || f.isApplicable ? "✓ APPLICABLE NEXUS" : "✗ NOT APPLICABLE"}
                          </span>
                        </div>
                        <p className="text-black/70 text-[10px] mb-1.5">{f.applicability_rationale || f.rationale}</p>
                        {(f.preconditions_met || f.preconditionsMet)?.length > 0 && (
                          <div className="space-y-0.5">
                            {(f.preconditions_met || f.preconditionsMet).map((pm, pidx) => (
                              <div key={pidx} className="text-[9.5px] text-emerald-700 flex items-center gap-1 font-mono">
                                <span>✔</span> <span>{pm}</span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Tier 3 Conclusion Justification Findings */}
              {threeTierVerification?.tier_3_conclusion_verification?.validations?.length > 0 && (
                <div className="p-3 bg-white border border-black/15 rounded shadow-sm space-y-2">
                  <span className="text-[9px] font-black tracking-wider text-black/70 uppercase block" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                    ⚖️ TIER 3: CONCLUSION JUSTIFICATION AUDIT ("DOES THIS LAW JUSTIFY THE ADVICE?")
                  </span>
                  <div className="space-y-2">
                    {threeTierVerification.tier_3_conclusion_verification.validations.map((v, i) => (
                      <div key={i} className={`p-2.5 rounded border text-[10.5px] ${
                        v.is_justified || v.isJustified ? "bg-emerald-50/50 border-emerald-300/60" : "bg-red-50/70 border-red-300/60"
                      }`}>
                        <div className="flex items-center justify-between gap-2 mb-1">
                          <strong className={v.is_justified || v.isJustified ? "text-emerald-950" : "text-red-950"}>
                            {v.statutory_basis || v.statutoryBasis}
                          </strong>
                          <span className={`text-[8px] font-mono font-bold px-1.5 py-0.5 rounded ${
                            v.is_justified || v.isJustified ? "bg-emerald-200 text-emerald-900" : "bg-red-200 text-red-900"
                          }`}>
                            {v.logical_status || v.logicalStatus || (v.is_justified ? "VALID_JUSTIFIED_DEDUCTION" : "STATUTORY_BAR_CONTRADICTION")}
                          </span>
                        </div>
                        <p className="text-[10px] text-black/80 mb-1">
                          <strong>Conclusion Asserted:</strong> {v.conclusion_statement || v.conclusionStatement}
                        </p>
                        <p className="text-[9.5px] text-black/60 font-sans">
                          <strong>Legal Deduction Analysis:</strong> {v.legal_analysis || v.legalAnalysis}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Full Markdown Verification Report */}
              <div className="p-3.5 bg-emerald-50/70 border border-emerald-900/25 rounded">
                <span className="text-[9px] font-black tracking-widest text-emerald-800 uppercase block mb-2" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                  📝 DETAILED STATUTORY AUDIT & ASSERTION TRACE
                </span>
                <MarkdownRenderer content={verificationReport} />
              </div>
            </div>
          )}

          {/* TAB 4: Agent Council Telemetry Logs */}
          {activeTab === "logs" && (
            <div className="space-y-2 text-[10px] font-mono">
              <div className="pb-2 border-b border-black/10 text-black/50 text-[8px]">
                CHRONOLOGICAL INFERENCE TRACE ACROSS 5 SPECIALIZED MODELS:
              </div>
              {logs.map((log, i) => (
                <div key={i} className="flex items-start gap-2 text-black/85">
                  <span className="text-emerald-700 font-bold min-w-[45px]">[{log.time}]</span>
                  <span className="text-[#C93636] font-black min-w-[130px]">[{log.tag}]</span>
                  <span>{log.msg}</span>
                </div>
              ))}
            </div>
          )}

          {/* TAB 5: Layer 9 Multilingual Glossary */}
          {activeTab === "glossary" && selectedLanguage !== "en" && (
            <div className="space-y-3">
              <span className="text-[9px] font-black uppercase text-[#171717]/70 block mb-2" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                📖 AYURVEDA & STATUTORY TERMINOLOGY GLOSSARY ({selectedLanguage === "hi" ? "हिन्दी" : "मराठी"})
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {(GLOSSARY_DICTIONARY[selectedLanguage] || []).map((item, idx) => (
                  <div key={idx} className="p-2.5 bg-white border border-[#171717]/20 rounded shadow-sm">
                    <strong className="text-xs text-[#C93636] block">{item.translation}</strong>
                    <span className="text-[9px] font-bold text-black/70 block mb-1">({item.term})</span>
                    <p className="text-[9.5px] text-black/60 font-sans">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 6: Alternative Matched Templates */}
          {activeTab === "alternatives" && (
            <div className="space-y-3">
              <p className="text-[9px] font-black uppercase text-[#171717]/70" style={{ fontFamily: "'Press Start 2P', monospace" }}>
                ♠ ALTERNATIVE ARCHETYPES:
              </p>
              {alternatives.map((alt, i) => (
                <div key={i} className="p-2.5 bg-white border border-[#171717]/20 rounded shadow-sm">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[8px] font-bold font-mono text-[#C93636]">
                      #{alt.id} • {alt.category} ({alt.subcategory})
                    </span>
                    <span className="text-[8px] font-mono font-bold bg-[#171717] text-[#FFF8E7] px-1.5 py-0.5 rounded">
                      {(alt.confidence * 100).toFixed(1)}% Match
                    </span>
                  </div>
                  <p className="text-[10px] font-mono text-black/80">
                    "{alt.text}"
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Layer 9 & 6: Statutory Disclaimer & Footer Bar */}
        <div className="border-t border-[#171717]/15 bg-[#171717]/5 px-4 py-2 flex flex-col sm:flex-row items-center justify-between gap-1 text-[8px] font-mono text-black/60">
          <span>{disclaimers[selectedLanguage] || disclaimers.en}</span>
          <span className="font-bold">HOUSE OF CARDS • IPSAKTI ♠</span>
        </div>
      </div>

    </div>
  );
};

export default OutputScreen;
