import React, { useState, useEffect } from "react";

const statusMessages = [
  "ANALYZING PROMPT...",
  "SCANNING AGENT DECK...",
  "SELECTING AGENTS...",
  "ASSEMBLING THE TEAM...",
  "DEALING THE CARDS...",
];

const AgentStatus = ({ active, onComplete, isDealt }) => {
  const [messageIndex, setMessageIndex] = useState(0);
  const [displayText, setDisplayText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);
  const [showCursor, setShowCursor] = useState(true);
  const [finished, setFinished] = useState(false);

  useEffect(() => {
    if (!active) {
      setDisplayText("");
      setMessageIndex(0);
      setIsDeleting(false);
      setFinished(false);
      return;
    }

    if (finished) return;

    const currentMessage = statusMessages[messageIndex];
    const typingSpeed = isDeleting ? 20 : 35;

    const timer = setTimeout(() => {
      if (!isDeleting) {
        setDisplayText(currentMessage.slice(0, displayText.length + 1));

        if (displayText.length + 1 === currentMessage.length) {
          // If this was the last message ("DEALING THE CARDS...")
          if (messageIndex === statusMessages.length - 1) {
            setTimeout(() => {
              setFinished(true);
              if (onComplete) onComplete();
            }, 600);
          } else {
            setTimeout(() => setIsDeleting(true), 700);
          }
        }
      } else {
        setDisplayText(currentMessage.slice(0, displayText.length - 1));

        if (displayText.length === 1) {
          setIsDeleting(false);
          setMessageIndex((prev) => prev + 1);
        }
      }
    }, typingSpeed);

    return () => clearTimeout(timer);
  }, [displayText, isDeleting, messageIndex, active, finished, onComplete]);

  // Blinking cursor
  useEffect(() => {
    const interval = setInterval(() => setShowCursor((c) => !c), 530);
    return () => clearInterval(interval);
  }, []);

  if (!active) return null;

  return (
    <div className="mt-2 text-center select-none">
      {/* Typewriter text or Dealt Status */}
      <p
        className="
          text-[10px]
          font-black
          tracking-[0.1em]
          text-[#C93636]
          min-h-[16px]
          flex items-center justify-center
        "
        style={{ fontFamily: "monospace" }}
      >
        {finished ? (
          <span className="text-[#171717] font-bold tracking-widest text-[9px]">
            ♠ <span className="text-[#C93636]">5 AGENTS DEALT</span> ♠
          </span>
        ) : (
          <>
            {displayText}
            <span
              className="inline-block w-[1.5px] h-[10px] bg-[#C93636] ml-0.5 align-middle"
              style={{ opacity: showCursor ? 1 : 0 }}
            />
          </>
        )}
      </p>

      {/* Progress dots */}
      <div className="flex items-center justify-center gap-1.5 mt-1.5">
        {statusMessages.map((_, i) => (
          <div
            key={i}
            className={`
              w-1.5 h-1.5 rounded-full border border-[#171717]/20
              transition-all duration-300
              ${finished || i <= messageIndex
                ? "bg-[#C93636] border-[#C93636] scale-110 shadow-[0_0_4px_rgba(201,54,54,0.4)]"
                : "bg-transparent"
              }
            `}
          />
        ))}
      </div>
    </div>
  );
};

export default AgentStatus;
