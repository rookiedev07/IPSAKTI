import React from "react";
import { useNavigate } from "react-router-dom";

const MainHeader = () => {
  const navigate = useNavigate();

  return (
    <header className="header-entrance relative z-20 w-full border-b border-white/10 bg-[#0E1117]/85 backdrop-blur-md sticky top-0">
      <div className="max-w-5xl mx-auto flex items-center justify-between px-4 py-2.5 sm:px-6">
        {/* Logo */}
        <div
          onClick={() => navigate("/")}
          className="flex items-center gap-2.5 cursor-pointer hover:opacity-85 transition-opacity group"
          title="IP-SAKTI Problem Solver Console"
        >
          {/* Council Icon Emblem */}
          <div className="w-7 h-7 rounded-lg bg-[#181C26] border border-white/15 flex items-center justify-center text-emerald-400 shadow-[0_2px_10px_rgba(0,0,0,0.5)] group-hover:scale-105 group-hover:border-emerald-500/40 transition-all">
            <svg
              className="w-4 h-4 text-emerald-400"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polygon points="12 2 2 7 12 12 22 7 12 2" />
              <polyline points="2 17 12 22 22 17" />
              <polyline points="2 12 12 17 22 12" />
            </svg>
          </div>
          <div className="flex flex-col">
            <span
              className="text-[8px] sm:text-[9px] font-black tracking-wider uppercase text-[#F1F3F9] leading-tight"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              IP-SAKTI
            </span>
            <span className="text-[7px] font-mono text-white/40 tracking-widest uppercase">
              PROBLEM COUNCIL CONSOLE
            </span>
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-2">
          {/* Status badge */}
          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 bg-[#141822] border border-white/10 rounded-full shadow-sm">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 pulse-dot" />
            <span className="text-[8px] font-mono font-bold text-white/90 tracking-wider uppercase">
              COUNCIL READY
            </span>
          </div>

          {/* Pipeline badges replacing card suits */}
          <div className="hidden md:flex items-center gap-1 font-mono text-[7px] font-bold text-white/50">
            <span className="px-1.5 py-0.5 bg-[#161A24] border border-white/10 rounded shadow-sm text-slate-300">01 STRAT</span>
            <span className="px-1.5 py-0.5 bg-[#161A24] border border-white/10 rounded shadow-sm text-emerald-400">02 RES</span>
            <span className="px-1.5 py-0.5 bg-[#161A24] border border-white/10 rounded shadow-sm text-emerald-400">03 ARCH</span>
            <span className="px-1.5 py-0.5 bg-[#161A24] border border-white/10 rounded shadow-sm text-slate-300">04 EXEC</span>
            <span className="px-1.5 py-0.5 bg-[#161A24] border border-white/10 rounded shadow-sm text-emerald-400">05 QA</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default MainHeader;
