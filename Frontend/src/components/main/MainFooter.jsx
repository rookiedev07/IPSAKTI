import React from "react";

const MainFooter = () => {
  return (
    <footer className="relative z-10 text-center py-3 border-t border-black/10">
      <div className="flex items-center justify-center gap-3 mb-2">
        <span className="text-black/20 text-sm">♠</span>
        <div className="w-8 h-[2px] bg-black/10 rounded-full" />
        <span className="text-red-400 text-sm">♥</span>
        <div className="w-8 h-[2px] bg-black/10 rounded-full" />
        <span className="text-red-400 text-sm">♦</span>
        <div className="w-8 h-[2px] bg-black/10 rounded-full" />
        <span className="text-black/20 text-sm">♣</span>
      </div>
      <p className="text-[8px] text-black/40 tracking-[0.25em] uppercase font-mono">
        AI • AGENTS • ORCHESTRATION • HOUSE OF CARDS
      </p>
    </footer>
  );
};

export default MainFooter;
