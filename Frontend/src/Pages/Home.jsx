import React from "react";
import { useNavigate } from "react-router-dom";
import JokerCard from "../components/cards/JokerCard";

/* ------------------------------------------------
   Fan-card configuration
   4 cards fan left, 4 cards fan right.
   Index 0 = closest to Joker, index 3 = farthest.
   ------------------------------------------------ */
const BASE_DELAY = 1.0;     // seconds — wait for Joker entrance to finish
const STAGGER = 0.08;    // seconds between each card

const fanCards = [
  // ---- LEFT SIDE (negative X) ----
  { x: -100, rotate: -4, scale: 0.92, suit: "♠", color: "#171717" },
  { x: -195, rotate: -8, scale: 0.84, suit: "♥", color: "#C93636" },
  { x: -280, rotate: -12, scale: 0.76, suit: "♦", color: "#C93636" },
  { x: -355, rotate: -16, scale: 0.68, suit: "♣", color: "#171717" },

  // ---- RIGHT SIDE (positive X) ----
  { x: 100, rotate: 4, scale: 0.92, suit: "♣", color: "#171717" },
  { x: 195, rotate: 8, scale: 0.84, suit: "♦", color: "#C93636" },
  { x: 280, rotate: 12, scale: 0.76, suit: "♥", color: "#C93636" },
  { x: 355, rotate: 16, scale: 0.68, suit: "♠", color: "#171717" },
];

/* ------------------------------------------------
   Tiny card-back component used for the fan
   ------------------------------------------------ */
const FanCardBack = ({ suit, color }) => {
  const isRed = color === "#C93636";
  return (
    <div
      className={`
        w-[240px] h-[352px]
        rounded-lg
        bg-[#FFF8E7]
        border-[4px]
        ${isRed ? "border-[#C93636]" : "border-[#171717]"}
        shadow-[6px_7px_0px_rgba(23,23,23,0.14)]
        overflow-hidden select-none
        relative
      `}
    >
      {/* Retro dot texture */}
      <div
        className="
          absolute inset-0 pointer-events-none
          opacity-[0.06]
          bg-[radial-gradient(#171717_0.8px,transparent_0.8px)]
          bg-[size:6px_6px]
        "
      />

      {/* Central suit watermark */}
      <div className="absolute inset-0 flex items-center justify-center">
        <span
          className="text-8xl opacity-[0.10] font-black select-none"
          style={{ color }}
        >
          {suit}
        </span>
      </div>

      {/* Diagonal crosshatch pattern */}
      <div
        className="absolute inset-4 rounded border-2 opacity-[0.08]"
        style={{ borderColor: color }}
      />
      <div
        className="absolute inset-6 rounded border opacity-[0.05]"
        style={{ borderColor: color }}
      />

      {/* Top-left mini suit */}
      <div className="absolute top-3 left-3">
        <span className="text-xl font-black" style={{ color }}>
          {suit}
        </span>
      </div>

      {/* Bottom-right mini suit */}
      <div className="absolute bottom-3 right-3 rotate-180">
        <span className="text-xl font-black" style={{ color }}>
          {suit}
        </span>
      </div>

      {/* Vintage highlight */}
      <div className="absolute top-0 left-0 w-full h-10 bg-white/25 pointer-events-none" />
    </div>
  );
};


const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#F6F3EA] text-[#171717] flex flex-col relative overflow-hidden px-6 py-8">

      {/* Background decorative elements */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">

        {/* Soft red glow */}
        <div className="absolute top-[-150px] left-[-150px] w-[400px] h-[400px] bg-red-200/30 blur-[110px] rounded-full" />

        {/* Soft black/gray glow */}
        <div className="absolute bottom-[-150px] right-[-150px] w-[400px] h-[400px] bg-gray-300/40 blur-[110px] rounded-full" />

        {/* Decorative suits */}

        {/* Spade */}
        <div className="absolute top-28 left-10 text-black/10 text-7xl rotate-12">
          ♠
        </div>

        {/* Heart */}
        <div className="absolute bottom-28 right-10 text-red-300/40 text-7xl -rotate-12">
          ♥
        </div>

        {/* Diamond */}
        <div className="absolute top-1/2 right-20 text-red-300/30 text-6xl rotate-12">
          ♦
        </div>

        {/* Club */}
        <div className="absolute top-1/3 left-20 text-black/10 text-6xl -rotate-12">
          ♣
        </div>

      </div>


      {/* Header */}
      <header className="relative z-10 flex flex-col items-center pt-2">

        <p
          className="text-[9px] sm:text-[10px] tracking-[0.35em] text-black/40 uppercase mb-3"
          style={{
            fontFamily: "'Press Start 2P', monospace",
          }}
        >
          AI Orchestration System
        </p>

        <h1
          className="text-xl sm:text-2xl font-black tracking-tight uppercase"
          style={{
            fontFamily: "'Press Start 2P', monospace",
          }}
        >
          Welcome{" "}
          <span className="text-red-600">
            To
          </span>{" "}
          House of Cards
        </h1>

      </header>


      {/* Main Card Area */}
      <main className="relative z-10 flex-1 flex items-center justify-center w-full">

        <div
          className="
            relative
            w-full
            max-w-[1400px]
            h-[520px]
            flex
            items-center
            justify-center
          "
        >

          {/* Fan cards — behind the Joker */}
          {fanCards.map((card, i) => (
            <div
              key={i}
              className="fan-card"
              style={{
                "--fan-x": `${card.x}px`,
                "--fan-rotate": `${card.rotate}deg`,
                "--fan-scale": `${card.scale}`,
                "--fan-delay": `${BASE_DELAY + i * STAGGER}s`,
                zIndex: 40 - i,
              }}
            >
              <FanCardBack suit={card.suit} color={card.color} />
            </div>
          ))}

          {/* Joker — always on top */}
          <div
            className="
              relative
              z-50
              joker-entrance
            "
          >
            <JokerCard />
          </div>

          {/* CTA Button — appears after all animations */}
          <div
            className="
              absolute
              bottom-2
              left-1/2
              -translate-x-1/2
              z-50
              cta-fade-in
            "
          >
            <button
              onClick={() => navigate('/login')}
              className="
                group
                relative
                px-8 py-3
                -ml-[150px]
                bg-[#171717]
                text-[#FFF8E7]
                text-[11px]
                tracking-[0.25em]
                uppercase
                font-black
                rounded-md
                border-[3px]
                border-[#171717]
                shadow-[4px_5px_0px_rgba(23,23,23,0.18)]
                transition-all
                duration-300
                hover:bg-red-600
                hover:border-red-600
                hover:-translate-y-1
                hover:shadow-[6px_8px_0px_rgba(23,23,23,0.22)]
                active:translate-y-0
                active:shadow-[2px_3px_0px_rgba(23,23,23,0.18)]
              "
              style={{
                fontFamily: "'Press Start 2P', monospace",
              }}
            >
              <span className="relative z-10  flex items-center gap-3">
                <span className="text-red-400 group-hover:text-[#FFF8E7] transition-colors">♠</span>
                Deal the Cards
                <span className="text-red-400 group-hover:text-[#FFF8E7] transition-colors">♠</span>
              </span>
            </button>
          </div>

        </div>

      </main>


      {/* Footer */}
      <footer className="relative z-10 flex flex-col items-center text-center pb-2">

        <div className="flex items-center gap-3 mb-5">

          <span className="text-black/20 text-lg">♠</span>

          <div className="w-12 h-[2px] bg-black/10 rounded-full" />

          <span className="text-red-400 text-lg">♥</span>

          <div className="w-12 h-[2px] bg-black/10 rounded-full" />

          <span className="text-red-400 text-lg">♦</span>

          <div className="w-12 h-[2px] bg-black/10 rounded-full" />

          <span className="text-black/20 text-lg">♣</span>

        </div>

        <p
          className="text-[10px] sm:text-xs md:text-sm text-black/55 tracking-[0.12em] uppercase leading-relaxed"
          style={{
            fontFamily: "'Press Start 2P', monospace",
          }}
        >
          You give the problem.
          <br />

          <span className="text-red-600">
            The Joker builds the team.
          </span>
        </p>

        <p className="mt-4 text-[9px] text-black/30 tracking-[0.3em] uppercase">
          AI • AGENTS • ORCHESTRATION
        </p>

      </footer>

    </div>
  );
};

export default Home;