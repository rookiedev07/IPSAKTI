import React from "react";

const Card = ({ rank, suit, color, agentName, agentSub, isFlipped = false }) => {
  const isRed = color === "red";

  const mainColor = isRed ? "text-[#C93636]" : "text-[#171717]";
  const lineColor = isRed ? "bg-[#C93636]" : "bg-[#171717]";

  return (
    <div
      className={`
        relative
        w-[150px]
        h-[220px]
        rounded-md
        bg-[#FFF8E7]
        border-[3px]
        ${isRed ? "border-[#C93636]" : "border-[#171717]"}
        shadow-[5px_6px_0px_rgba(23,23,23,0.18)]
        overflow-hidden
        select-none
        transition-all
        duration-300
        hover:-translate-y-3
        hover:rotate-1
        hover:shadow-[8px_10px_0px_rgba(23,23,23,0.22)]
      `}
    >

      {/* Retro paper texture */}
      <div
        className="
          absolute
          inset-0
          pointer-events-none
          opacity-[0.08]
          bg-[radial-gradient(#171717_0.7px,transparent_0.7px)]
          bg-[size:5px_5px]
        "
      />

      {/* Top Left */}
      <div
        className={`
          absolute
          top-3
          left-4
          flex
          flex-col
          items-center
          leading-none
          ${mainColor}
        `}
      >
        <span
          className="text-2xl font-black"
          style={{
            fontFamily: "monospace",
          }}
        >
          {rank}
        </span>

        <span className="text-xl mt-0.5">
          {suit}
        </span>
      </div>


      {/* Center 3D Flip Container */}
      <div className="absolute inset-0 card-flip-container flex items-center justify-center p-3">
        <div className={`card-flip-inner ${isFlipped ? "is-flipped" : ""}`}>

          {/* FRONT: Classic Large Spade */}
          <div className={`card-flip-front ${mainColor}`}>
            <span
              className="
                text-7xl
                font-black
                leading-none
                drop-shadow-[2px_2px_0px_rgba(23,23,23,0.12)]
              "
            >
              {suit}
            </span>

            {/* Single retro line */}
            <div
              className={`
                mt-3
                w-12
                h-[3px]
                ${lineColor}
              `}
            />
          </div>

          {/* BACK: Revealed Agent Name */}
          <div className={`card-flip-back ${mainColor}`}>
            <div className="flex flex-col items-center justify-center text-center px-1">
              <div className="w-8 h-8 rounded-full bg-[#171717]/5 border-2 border-[#171717] flex items-center justify-center mb-1.5 shadow-[1px_2px_0px_rgba(23,23,23,0.1)]">
                <span className="text-sm font-black text-[#C93636]">♠</span>
              </div>
              <span
                className="text-[12px] font-black tracking-wider uppercase text-[#171717] leading-tight"
                style={{ fontFamily: "'Press Start 2P', monospace" }}
              >
                {agentName || "AGENT"}
              </span>
              {agentSub && (
                <span className="text-[7px] font-mono tracking-widest text-[#171717]/60 uppercase mt-1 font-bold">
                  {agentSub}
                </span>
              )}
              <div
                className={`
                  mt-2
                  w-10
                  h-[2.5px]
                  ${lineColor}
                `}
              />
            </div>
          </div>

        </div>
      </div>


      {/* Bottom Right */}
      <div
        className={`
          absolute
          bottom-3
          right-4
          flex
          flex-col
          items-center
          leading-none
          rotate-180
          ${mainColor}
        `}
      >
        <span
          className="text-2xl font-black"
          style={{
            fontFamily: "monospace",
          }}
        >
          {rank}
        </span>

        <span className="text-xl mt-0.5">
          {suit}
        </span>
      </div>


      {/* Vintage highlight */}
      <div
        className="
          absolute
          top-0
          left-0
          w-full
          h-8
          bg-white/30
          pointer-events-none
        "
      />

    </div>
  );
};

export default Card;