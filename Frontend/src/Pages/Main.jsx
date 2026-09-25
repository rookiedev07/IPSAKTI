import React, { useState, useEffect, useRef } from "react";
import MainBackground from "../components/main/MainBackground";
import MainHeader from "../components/main/MainHeader";
import MainFooter from "../components/main/MainFooter";
import PromptInput from "../components/main/PromptInput";
import AgentStatus from "../components/main/AgentStatus";
import OutputScreen from "../components/main/OutputScreen";
import { matchPrompt } from "../services/promptService";

/**
 * Main Console — single-page, problem-oriented layout.
 *
 * States:
 *  idle     → prompt input centred on screen
 *  loading  → inline AgentStatus progress panel below prompt
 *  result   → OutputScreen replaces progress panel; prompt collapses to a summary bar
 */
const Main = () => {
  const [phase, setPhase] = useState("idle");     // "idle" | "loading" | "result"
  const [prompt, setPrompt] = useState("");
  const [matchedData, setMatchedData] = useState(null);
  const [isMatching, setIsMatching] = useState(false);
  const [orchestrationComplete, setOrchestrationComplete] = useState(false);
  const inputRef = useRef(null);

  /* Auto-focus prompt on mount */
  useEffect(() => {
    setTimeout(() => inputRef.current?.focus(), 300);
  }, []);

  /* When orchestration progress is complete AND API data is ready → show results */
  useEffect(() => {
    if (orchestrationComplete && !isMatching) {
      setPhase("result");
    }
  }, [orchestrationComplete, isMatching]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim() || phase === "loading") return;

    setPhase("loading");
    setMatchedData(null);
    setOrchestrationComplete(false);
    setIsMatching(true);

    try {
      const result = await matchPrompt(prompt.trim(), { language: "en" });
      setMatchedData(result);
    } catch (err) {
      console.error("[HOC] Prompt orchestration error:", err);
    } finally {
      setIsMatching(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleAgentsDone = () => {
    setOrchestrationComplete(true);
  };

  const handleTranslate = async (targetLanguage, promptOverride) => {
    const text = promptOverride || prompt || matchedData?.rawPrompt;
    if (!text?.trim()) return;
    try {
      const result = await matchPrompt(text, { language: targetLanguage });
      setMatchedData(result);
    } catch (err) {
      console.error("[HOC] Translation error:", err);
    }
  };

  const handleReset = () => {
    setPhase("idle");
    setPrompt("");
    setMatchedData(null);
    setOrchestrationComplete(false);
    setIsMatching(false);
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  return (
    <div className="min-h-screen bg-[#0B0D12] text-[#F1F3F9] flex flex-col relative selection:bg-emerald-500/30 selection:text-white">
      <MainBackground />
      <MainHeader />

      <main className="relative z-10 flex-1 flex flex-col justify-center px-4 sm:px-6 py-4">
        <div className={`w-full max-w-3xl mx-auto flex flex-col ${phase === "result" ? "pt-2" : "my-auto py-2"}`}>

          {/* ── HERO TEXT (only when idle) ── */}
          {phase === "idle" && (
            <div className="page-entrance pt-2 pb-5 text-center">
              <p
                className="text-[8px] sm:text-[9px] tracking-[0.35em] text-white/40 uppercase mb-3"
                style={{ fontFamily: "'Press Start 2P', monospace" }}
              >
                AI Orchestration System
              </p>
              <h1
                className="text-lg sm:text-xl font-black tracking-tight uppercase mb-1 text-[#F1F3F9]"
                style={{ fontFamily: "'Press Start 2P', monospace" }}
              >
                What's your{" "}
                <span className="text-emerald-400">problem?</span>
              </h1>
              <p className="text-[10px] font-mono text-white/50 mt-2">
                Describe it below — our 5-agent AI council will analyze, strategize, and solve it.
              </p>
            </div>
          )}

          {/* ── PROMPT BAR (idle = full, loading/result = compact sticky) ── */}
          {phase === "idle" ? (
            /* Full prompt input */
            <div className="page-entrance" style={{ animationDelay: "0.1s" }}>
              <PromptInput
                inputRef={inputRef}
                prompt={prompt}
                onPromptChange={setPrompt}
                onSubmit={handleSubmit}
                onKeyDown={handleKeyDown}
                disabled={false}
              />
            </div>
          ) : (
            /* Compact sticky prompt summary bar */
            <div className="pt-2 pb-2">
              <div className="
                flex items-center gap-3
                bg-[#131722] border border-white/10
                rounded-xl px-4 py-3 shadow-card
              ">
                <span className="text-emerald-400 font-mono font-black shrink-0 text-xs">▶</span>
                <p className="text-[11px] font-mono text-[#F1F3F9] flex-1 line-clamp-2 leading-relaxed">
                  "{prompt}"
                </p>
                <button
                  onClick={handleReset}
                  id="new-problem-btn"
                  className="
                    shrink-0 flex items-center gap-1.5
                    px-3 py-1.5 bg-[#1C212E] hover:bg-emerald-600
                    text-[#F1F3F9] text-[7px] tracking-[0.2em] uppercase font-black
                    rounded-lg border border-white/15 hover:border-emerald-500
                    shadow-[0_2px_8px_rgba(0,0,0,0.4)]
                    hover:-translate-y-0.5 active:translate-y-0
                    transition-all cursor-pointer
                  "
                  style={{ fontFamily: "'Press Start 2P', monospace" }}
                >
                  <span className="text-emerald-400 text-[9px]">↺</span>
                  NEW QUERY
                </button>
              </div>
            </div>
          )}

          {/* ── LOADING: Agent Council Progress ── */}
          {phase === "loading" && (
            <AgentStatus
              active
              isComplete={orchestrationComplete}
              onComplete={handleAgentsDone}
            />
          )}

          {/* ── RESULT: Output Screen ── */}
          {phase === "result" && (
            <div className="results-entrance mt-4">
              <OutputScreen
                prompt={prompt}
                matchedData={matchedData}
                onReset={handleReset}
                onTranslate={handleTranslate}
              />
            </div>
          )}

        </div>
      </main>

      <MainFooter />
    </div>
  );
};

export default Main;
