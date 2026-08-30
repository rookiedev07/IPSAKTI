import React, { useState, useEffect, useRef } from "react";
import Card from "../cards/Cards";
import { cardData } from "../cards/cardData";

const AGENT_ROLES = [
  { name: "DEEPSEEK R1", sub: "NVIDIA NIM", role: "STRATEGIST", code: "AGENT-01", desc: "Orchestration & Logic" },
  { name: "DEEPSEEK V3", sub: "NVIDIA NIM", role: "RESEARCHER", code: "AGENT-02", desc: "Context & Search" },
  { name: "NEMOTRON 120B", sub: "NVIDIA NIM", role: "ARCHITECT", code: "AGENT-03", desc: "System Design" },
  { name: "LLAMA 3.2 11B", sub: "NVIDIA NIM", role: "EXECUTOR", code: "AGENT-04", desc: "Deliverable Generation" },
  { name: "DEEPSEEK VERIFIER", sub: "NVIDIA NIM", role: "VERIFIER", code: "AGENT-05", desc: "Statutory 3-Tier QA" },
];

const AGENT_STEPS = [
  { step: 1, tag: "♠ CALL 1/5: STRATEGIST", title: "Analyzing regulatory domain & statutory framework...", icon: "♠" },
  { step: 2, tag: "♥ CALL 2/5: RESEARCHER", title: "Cross-referencing First Schedule Samhitas, TKDL & gazettes...", icon: "♥" },
  { step: 3, tag: "♦ CALL 3/5: ARCHITECT", title: "Constructing boundary contracts & compliance schemas...", icon: "♦" },
  { step: 4, tag: "♣ CALL 4/5: EXECUTOR", title: "Synthesizing actionable Markdown roadmap table...", icon: "♣" },
  { step: 5, tag: "🛡️ CALL 5/5: VERIFIER", title: "Auditing 3-Tier statutory verification pipeline...", icon: "🛡️" },
];

const DealtCards = ({ visible, agents, isMatching, matchedData, onComplete }) => {
  const [flippedCards, setFlippedCards] = useState([]);
  const [activeStepIndex, setActiveStepIndex] = useState(0);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const hasTriggeredComplete = useRef(false);

  // The first 5 cards: Ace, 2, 3, 4, 5
  const activeCards = cardData.slice(0, 5);

  // Card flip sequence on deal
  useEffect(() => {
    if (!visible) {
      setFlippedCards([]);
      setActiveStepIndex(0);
      setElapsedSeconds(0);
      setIsCompleted(false);
      hasTriggeredComplete.current = false;
      return;
    }

    // 1.5s after cards settle from deal, flip the cards in a cascading wave
    const flipTimer = setTimeout(() => {
      activeCards.forEach((_, i) => {
        setTimeout(() => {
          setFlippedCards((prev) => [...prev, i]);
        }, i * 100);
      });
    }, 1500);

    return () => clearTimeout(flipTimer);
  }, [visible]);

  // Elapsed timer while waiting for backend
  useEffect(() => {
    if (!visible || isCompleted) return;

    const timer = setInterval(() => {
      setElapsedSeconds((prev) => {
        const next = prev + 1;
        // Dynamically align active agent step with realistic execution pacing:
        // Call 1 (Strategist): 0 - 7s
        // Call 2 (Researcher): 8 - 16s
        // Call 3 (Architect):  17 - 25s
        // Call 4 (Executor):   26 - 48s (table generation takes longer)
        // Call 5 (Verifier):   49s+
        if (next <= 7) {
          setActiveStepIndex(0);
        } else if (next <= 16) {
          setActiveStepIndex(1);
        } else if (next <= 25) {
          setActiveStepIndex(2);
        } else if (next <= 48) {
          setActiveStepIndex(3);
        } else {
          setActiveStepIndex(4);
        }
        return next;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [visible, isCompleted]);

  // When matchedData arrives and matching finishes, trigger smooth completion handoff
  useEffect(() => {
    if (visible && matchedData && !hasTriggeredComplete.current) {
      hasTriggeredComplete.current = true;
      setIsCompleted(true);
      setActiveStepIndex(4);

      // Brief 600ms victory flash, then trigger OutputScreen with 100% real live data
      const transitionTimer = setTimeout(() => {
        if (onComplete) onComplete();
      }, 600);

      return () => clearTimeout(transitionTimer);
    }
  }, [visible, matchedData, onComplete]);

  if (!visible) return null;

  const currentStep = AGENT_STEPS[activeStepIndex] || AGENT_STEPS[0];
  const progressPercent = isCompleted ? 100 : Math.min(95, Math.round(((activeStepIndex + 1) / 5) * 80 + (elapsedSeconds % 7) * 2.5));

  return (
    <div className="relative z-20 flex flex-col items-center justify-center w-full my-auto select-none pointer-events-auto">

      {/* Top Dynamic Status Banner */}
      <div className="banner-fade-slide mb-3 sm:mb-5 text-center">
        <div className={`inline-flex items-center gap-2 px-3 py-1.5 border-2 rounded shadow-[3px_3px_0px_rgba(23,23,23,0.14)] mb-1 transition-all duration-300 ${
          isCompleted 
            ? "bg-emerald-100 border-emerald-800 text-emerald-900" 
            : "bg-[#FFF8E7] border-[#171717] text-[#171717]"
        }`}>
          <span className={`w-2 h-2 rounded-full ${isCompleted ? "bg-emerald-600" : "bg-red-500 animate-ping"}`} />
          <span
            className="text-[8.5px] sm:text-[9.5px] font-black tracking-[0.15em] uppercase"
            style={{ fontFamily: "'Press Start 2P', monospace" }}
          >
            {isCompleted ? "✓ 5/5 AGENTS CONCLUDED • DOSSIER READY" : currentStep.tag}
          </span>
          <span className="text-[8px] font-mono px-1.5 py-0.2 bg-[#171717] text-[#FFF8E7] rounded font-bold">
            {elapsedSeconds}s
          </span>
        </div>

        {/* Live Task Subtitle & Progress Bar */}
        <div className="flex flex-col items-center gap-1 mt-1">
          <p className="text-[9.5px] font-mono text-[#171717] font-semibold tracking-tight">
            {isCompleted ? "100% Live AI Synthesis Finished • Mounting Dossier..." : currentStep.title}
          </p>
          
          {/* Progress Track */}
          <div className="w-48 sm:w-64 h-1.5 bg-black/10 rounded-full overflow-hidden border border-black/20 mt-0.5">
            <div 
              className={`h-full transition-all duration-500 rounded-full ${isCompleted ? "bg-emerald-600" : "bg-[#C93636]"}`}
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>
      </div>

      {/* 5 Dealt Cards Row with Active Agent Pulse */}
      <div className="flex items-center justify-center gap-3 sm:gap-4 md:gap-5 flex-nowrap max-w-full px-2">
        {activeCards.map((card, index) => {
          const roleInfo = (agents && agents[index]) || AGENT_ROLES[index] || {
            name: "AGENT",
            sub: "CORE",
            role: "SPECIALIST",
            code: `AGENT-0${index + 1}`,
            desc: "Specialist",
          };

          // Delta offsets from deck to card slots
          const dx = 310 - index * 85;
          const dy = 460;
          const delay = index * 0.14;
          const isFlipped = flippedCards.includes(index);
          const isCurrentlyActive = activeStepIndex === index && !isCompleted;

          return (
            <div
              key={`dealt-${card.rank}-${card.suit}`}
              className="deal-card-animate flex flex-col items-center group cursor-pointer"
              style={{
                "--deal-dx": `${dx}px`,
                "--deal-dy": `${dy}px`,
                "--deal-delay": `${delay}s`,
                "--deal-init-rot": `${16 + (4 - index) * 2}deg`,
              }}
            >
              {/* Card Container with Active Glow Effect */}
              <div className={`relative transition-all duration-300 group-hover:-translate-y-2 group-hover:scale-105 ${
                isCurrentlyActive 
                  ? "ring-4 ring-[#C93636] ring-offset-2 ring-offset-[#F6F3EA] rounded-xl scale-105 shadow-[0_0_20px_rgba(201,54,54,0.4)]" 
                  : isCompleted
                    ? "ring-2 ring-emerald-500/80 rounded-xl"
                    : ""
              }`}>
                <Card
                  rank={card.rank}
                  suit={card.suit}
                  color={card.color}
                  agentName={roleInfo.name}
                  agentSub={roleInfo.sub}
                  isFlipped={isFlipped}
                />

                {/* Top Corner Agent Badge */}
                <div className={`absolute top-2 right-2 z-10 px-1.5 py-0.5 rounded text-[7px] font-mono font-black ${
                  isCurrentlyActive 
                    ? "bg-[#C93636] text-white animate-pulse" 
                    : "bg-[#171717] text-[#FFF8E7]"
                }`}>
                  {isCurrentlyActive ? "ACTIVE" : roleInfo.code}
                </div>
              </div>

              {/* Under-card Agent Role Tag */}
              <div className="mt-3 text-center transition-all duration-300 group-hover:translate-y-0.5">
                <p
                  className={`text-[9px] font-black tracking-wider uppercase transition-colors duration-300 ${
                    isCurrentlyActive ? "text-[#C93636] scale-105 font-extrabold" : "text-[#171717]"
                  }`}
                  style={{ fontFamily: "'Press Start 2P', monospace" }}
                >
                  {roleInfo.role}
                </p>
                <p className="text-[8px] font-mono text-black/60 tracking-tight mt-0.5">
                  {roleInfo.desc}
                </p>
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
};

export default DealtCards;
