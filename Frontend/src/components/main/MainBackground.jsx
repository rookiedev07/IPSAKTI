import React from "react";

const MainBackground = () => (
  <div className="absolute inset-0 pointer-events-none overflow-hidden select-none bg-[#0B0D12]">
    {/* Deep ambient dark glows */}
    <div className="absolute top-[-100px] left-[-100px] w-[500px] h-[500px] bg-emerald-600/[0.07] blur-[150px] rounded-full" />
    <div className="absolute bottom-[-100px] right-[-100px] w-[500px] h-[500px] bg-indigo-600/[0.09] blur-[160px] rounded-full" />
    <div className="absolute top-[30%] right-[15%] w-[380px] h-[380px] bg-blue-600/[0.05] blur-[130px] rounded-full" />

    {/* Dark Dot Matrix overlay */}
    <div className="absolute inset-0 dot-paper opacity-80" />

    {/* Ambient problem-oriented architectural watermarks */}
    <div className="absolute top-24 left-8 text-white/[0.025] font-mono text-4xl sm:text-5xl select-none font-black tracking-widest">// 01_DECOMPOSE</div>
    <div className="absolute bottom-24 right-8 text-emerald-400/[0.04] font-mono text-4xl sm:text-5xl select-none font-black tracking-widest">// RESOLUTION</div>
    <div className="absolute top-1/2 right-[6%] text-sky-400/[0.025] font-mono text-3xl select-none font-black tracking-wider">[ COUNCIL.EXEC ]</div>
    <div className="absolute top-1/3 left-[6%] text-emerald-400/[0.03] font-mono text-3xl select-none font-black tracking-wider">{`{ STATUTORY_QA }`}</div>
  </div>
);

export default MainBackground;
