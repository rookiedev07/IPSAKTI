import React, { useState, useEffect } from "react";

const AGENT_STEPS = [
  { code: "01", role: "STRATEGIST", label: "Decomposing problem & formulating strategy", color: "text-slate-200" },
  { code: "02", role: "RESEARCHER", label: "Scanning statutory corpus & prior art", color: "text-teal-300" },
  { code: "03", role: "ARCHITECT",  label: "Constructing compliance schema & roadmap", color: "text-emerald-400" },
  { code: "04", role: "EXECUTOR",   label: "Synthesising deliverable & action plan", color: "text-sky-400" },
  { code: "05", role: "VERIFIER",   label: "Running 3-tier statutory verification", color: "text-emerald-400" },
];

/**
 * Inline agent-council progress panel.
 * Shows problem-solving progress through the 5-agent pipeline.
 *
 * Props:
 *  - active {boolean}       — show the panel
 *  - isComplete {boolean}   — all agents done, trigger onComplete
 *  - onComplete {function}  — called when all steps complete
 */
const AgentStatus = ({ active, onComplete, isComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [doneSteps, setDoneSteps] = useState([]);
  const [complete, setComplete] = useState(false);
  const STEP_DURATION = 1100; // ms per agent step

  /* reset when deactivated */
  useEffect(() => {
    if (!active) {
      setCurrentStep(0);
      setDoneSteps([]);
      setComplete(false);
    }
  }, [active]);

  /* advance through agents on a timer */
  useEffect(() => {
    if (!active || complete) return;

    const timer = setTimeout(() => {
      if (currentStep < AGENT_STEPS.length - 1) {
        setDoneSteps((d) => [...d, currentStep]);
        setCurrentStep((s) => s + 1);
      } else {
        // last step: mark done, wait briefly, then trigger completion
        setDoneSteps((d) => [...d, currentStep]);
        setComplete(true);
        setTimeout(() => { if (onComplete) onComplete(); }, 450);
      }
    }, STEP_DURATION);

    return () => clearTimeout(timer);
  }, [active, currentStep, complete, onComplete]);

  if (!active) return null;

  const progressPct = complete ? 100 : Math.round(((doneSteps.length) / AGENT_STEPS.length) * 100);

  return (
    <div className="results-entrance w-full mt-6">
      <div className="
        bg-[#131722]/95 border-2 border-white/15 rounded-xl
        shadow-card-lg overflow-hidden backdrop-blur-md
      ">
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-3 border-b border-white/10 bg-white/[0.02]">
          <div className="flex items-center gap-2.5">
            <span className="suit-spin text-emerald-400 text-base">✦</span>
            <span
              className="text-[9px] font-black tracking-[0.2em] uppercase text-[#F1F3F9]"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              ORCHESTRATING PROBLEM RESOLUTION...
            </span>
          </div>
          <span className="text-[8px] font-mono text-white/50 font-bold">{progressPct}%</span>
        </div>

        {/* Agent rows */}
        <div className="px-5 py-4 space-y-2.5">
          {AGENT_STEPS.map((agent, i) => {
            const isDone = doneSteps.includes(i);
            const isActive = currentStep === i && !complete;

            return (
              <div
                key={i}
                className="agent-row flex items-center gap-3"
                style={{ "--agent-delay": `${i * 0.08}s` }}
              >
                {/* Status indicator */}
                <div className="w-6 flex-shrink-0 flex items-center justify-center font-mono">
                  {isDone || complete ? (
                    <span className="text-emerald-400 text-xs font-black">✓</span>
                  ) : isActive ? (
                    <span className={`pulse-dot text-[8px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 border border-emerald-500/30 ${agent.color}`}>
                      {agent.code}
                    </span>
                  ) : (
                    <span className="text-white/20 text-[8px] font-bold px-1.5 py-0.5">
                      {agent.code}
                    </span>
                  )}
                </div>

                {/* Role label */}
                <span
                  className={`text-[8px] font-black w-24 shrink-0 ${
                    isDone || complete ? "text-emerald-400" : isActive ? "text-white" : "text-white/30"
                  }`}
                  style={{ fontFamily: "'Press Start 2P', monospace" }}
                >
                  {agent.role}
                </span>

                {/* Task description */}
                <span className={`text-[10px] font-mono flex-1 ${
                  isDone || complete ? "text-white/40 line-through decoration-emerald-500/40" : isActive ? "text-white/90" : "text-white/25"
                }`}>
                  {agent.label}
                </span>

                {/* Time indicator */}
                {(isDone || complete) && (
                  <span className="text-[7px] font-mono text-emerald-400 bg-emerald-950/50 border border-emerald-500/30 px-1.5 py-0.5 rounded font-bold shrink-0">DONE</span>
                )}
                {isActive && (
                  <span className="text-[7px] font-mono text-emerald-400 bg-emerald-950/50 border border-emerald-500/30 px-1.5 py-0.5 rounded font-bold shrink-0 pulse-dot">LIVE</span>
                )}
              </div>
            );
          })}
        </div>

        {/* Progress bar */}
        <div className="px-5 pb-4">
          <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-emerald-600 via-emerald-400 to-teal-300 rounded-full transition-all duration-700 ease-out"
              style={{ width: `${progressPct}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentStatus;
