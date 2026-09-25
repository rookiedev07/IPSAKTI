import React from "react";

const MainFooter = () => (
  <footer className="relative z-10 border-t border-white/10 py-3 px-4 bg-[#0A0C11]/50 backdrop-blur-sm">
    <div className="max-w-5xl mx-auto flex items-center justify-between gap-4">
      <p className="text-[8px] font-mono text-white/40 tracking-[0.2em] uppercase">
        AI • AGENTS • PROBLEM RESOLUTION • IP-SAKTI
      </p>
      <div className="flex items-center gap-2 text-[10px] text-white/30 font-mono font-bold">
        <span>[ DECOMPOSE ]</span>
        <span>•</span>
        <span>[ SYNTHESIZE ]</span>
        <span>•</span>
        <span>[ VERIFY ]</span>
      </div>
    </div>
  </footer>
);

export default MainFooter;
