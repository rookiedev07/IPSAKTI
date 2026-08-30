import React from "react";

const MainHeader = ({ operator, onLogout }) => {
  return (
    <header className="relative z-20 w-full max-w-7xl mx-auto flex items-center justify-between px-4 py-2 sm:px-6 sm:py-2.5 border-b border-black/10">
      <div className="flex items-center gap-2">
        <span className="text-red-600 text-xs">♠</span>
        <span
          className="text-[8px] sm:text-[9px] font-black tracking-wider uppercase text-[#171717]"
          style={{ fontFamily: "'Press Start 2P', monospace" }}
        >
          HOUSE OF CARDS
        </span>
        <span className="hidden md:inline-block text-[8px] text-black/35 font-mono tracking-wider uppercase ml-1">
          • CONSOLE
        </span>
      </div>

      <div className="flex items-center gap-2">
        {operator && (
          <div className="hidden sm:flex items-center gap-1.5 px-2 py-0.5 bg-white border border-[#171717] rounded shadow-[1px_1px_0px_rgba(23,23,23,0.1)]">
            <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
            <span className="text-[8px] font-mono font-bold text-[#171717]">
              {operator.name || operator.email}
            </span>
          </div>
        )}

        <button
          onClick={onLogout}
          className="
            group px-2.5 py-1 bg-[#171717] hover:bg-red-600
            text-[#FFF8E7] text-[8px] tracking-wider uppercase font-bold
            rounded border border-[#171717] hover:border-red-600
            shadow-[2px_2px_0px_rgba(23,23,23,0.18)]
            hover:-translate-y-0.5 hover:shadow-[2px_3px_0px_rgba(23,23,23,0.22)]
            active:translate-y-0 active:shadow-[1px_1px_0px_rgba(23,23,23,0.18)]
            transition-all flex items-center gap-1 cursor-pointer
          "
          style={{ fontFamily: "'Press Start 2P', monospace" }}
        >
          <span className="text-red-400 group-hover:text-[#FFF8E7] transition-colors text-[7px]">♠</span>
          Logout
        </button>
      </div>
    </header>
  );
};

export default MainHeader;
