import React from "react";
import Card from "../cards/Cards";
import { cardData } from "./cardData";

const Deck = () => {
  return (
    <div className="flex items-center justify-center gap-3 flex-wrap max-w-[1200px]">
      {cardData.map((card, index) => (
        <Card
          key={`${card.rank}-${card.suit}`}
          rank={card.rank}
          suit={card.suit}
          color={card.color}
        />
      ))}
    </div>
  );
};

export default Deck;