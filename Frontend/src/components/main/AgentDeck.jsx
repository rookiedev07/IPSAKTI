import React from "react";
import Card from "../cards/Cards";
import { cardData } from "../cards/cardData";

const AgentDeck = ({ visible, dealtCount = 0 }) => {
  // If 5 cards (Ace to 5) are dealt, card at index 5 (Rank 6) is on top
  const topIndex = dealtCount >= 5 ? 5 : 0;
  const currentTopCard = cardData[topIndex];
  const remainingDeckCards = cardData.slice(topIndex + 1);
  const remainingCount = cardData.length - (dealtCount >= 5 ? 5 : 0);

  return (
    <div
      className={`
        absolute
        transition-all duration-[800ms] ease-[cubic-bezier(0.22,1,0.36,1)]
        ${visible
          ? "opacity-100 translate-x-0 scale-100"
          : "opacity-0 translate-x-[80px] scale-90 pointer-events-none"
        }
      `}
      style={{
        bottom: "-90px",
        right: "-90px",
      }}
    >
      <div className="flex flex-col items-center gap-4 select-none">

        {/* Deck label */}
        <p
          className="text-[9px] font-black tracking-[0.2em] uppercase text-[#171717]/50 transition-colors"
          style={{ fontFamily: "'Press Start 2P', monospace" }}
        >
          ♠ Agent Deck ♠
        </p>

        {/* Stacked deck */}
        <div className="relative w-[150px] h-[220px]">

          {/* Background stack cards — depth illusion */}
          {remainingDeckCards.slice(0, 5).map((_, i) => (
            <div
              key={`stack-${i}`}
              className="absolute inset-0"
              style={{
                transform: `translate(${(5 - i) * 1.5}px, ${(5 - i) * 1.5}px)`,
                zIndex: i,
              }}
            >
              <div
                className="
                  w-full h-full rounded-md
                  bg-[#FFF8E7] border-[3px] border-[#171717]
                  shadow-[2px_2px_0px_rgba(23,23,23,0.08)]
                  overflow-hidden relative
                "
              >
                <div
                  className="
                    absolute inset-0 pointer-events-none opacity-[0.06]
                    bg-[radial-gradient(#171717_0.7px,transparent_0.7px)]
                    bg-[size:5px_5px]
                  "
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-4xl text-[#171717]/10 font-black">♠</span>
                </div>
                <div className="absolute inset-2 rounded border border-[#171717]/10" />
              </div>
            </div>
          ))}

          {/* Top card on deck — changes to 6 when 5 cards are dealt */}
          <div
            key={`top-card-${currentTopCard.rank}`}
            className="absolute inset-0 transition-all duration-500 animate-fadeIn"
            style={{ zIndex: 10 }}
          >
            <Card
              rank={currentTopCard.rank}
              suit={currentTopCard.suit}
              color={currentTopCard.color}
            />
          </div>

          {/* Card count badge */}
          <div
            className="
              absolute -bottom-3 -right-3 z-20
              w-8 h-8 rounded-full
              bg-[#171717] border-2 border-[#FFF8E7]
              shadow-[2px_2px_0px_rgba(23,23,23,0.18)]
              flex items-center justify-center
              transition-all duration-300
            "
          >
            <span
              className="text-[8px] text-[#FFF8E7] font-black"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              {remainingCount}
            </span>
          </div>
        </div>

        {/* Deck info */}
        <p className="text-[8px] text-black/40 tracking-[0.15em] uppercase font-mono mt-1">
          {dealtCount >= 5 ? `${remainingCount} reserve agents` : `${cardData.length} agents ready`}
        </p>
      </div>
    </div>
  );
};

export default AgentDeck;
