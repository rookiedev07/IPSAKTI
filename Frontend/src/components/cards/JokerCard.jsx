import React, { useEffect, useState } from "react";
import jokerImage from "../../assets/joker.png";

const messages = [
  "AI ORCHESTRATOR",
  "GIVE ME YOUR PROBLEM",
  "I'LL ANALYZE IT",
  "I'LL BUILD THE TEAM",
  "LET THE CARDS FALL",
];

const JokerCard = ({ children, large = false, hideBottomLabel = false }) => {
  const [introComplete, setIntroComplete] = useState(false);

  const [messageIndex, setMessageIndex] = useState(0);
  const [displayText, setDisplayText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  /* ========================= */
  /* INTRO ANIMATION */
  /* ========================= */

  useEffect(() => {
    const timer = setTimeout(() => {
      setIntroComplete(true);
    }, 1800);

    return () => clearTimeout(timer);
  }, []);


  /* ========================= */
  /* TYPEWRITER */
  /* ========================= */

  useEffect(() => {
    if (!introComplete) return;

    const currentMessage = messages[messageIndex];

    const typingSpeed = isDeleting ? 35 : 70;

    const timer = setTimeout(() => {

      if (!isDeleting) {

        setDisplayText(
          currentMessage.slice(0, displayText.length + 1)
        );

        if (displayText.length + 1 === currentMessage.length) {
          setTimeout(() => {
            setIsDeleting(true);
          }, 1200);
        }

      } else {

        setDisplayText(
          currentMessage.slice(0, displayText.length - 1)
        );

        if (displayText.length === 1) {

          setIsDeleting(false);

          setMessageIndex(
            (prev) => (prev + 1) % messages.length
          );

        }
      }

    }, typingSpeed);

    return () => clearTimeout(timer);

  }, [
    displayText,
    isDeleting,
    messageIndex,
    introComplete,
  ]);


  return (
    <div
      className={`
        relative
        ${large ? "w-[320px] h-[460px]" : "w-[240px] h-[352px]"}

        rounded-lg

        bg-[#FFF8E7]

        border-[4px]
        border-[#171717]

        shadow-[8px_9px_0px_rgba(23,23,23,0.18)]

        overflow-hidden
        select-none

        transition-all
        duration-300

        hover:-translate-y-4
        hover:rotate-1

        hover:shadow-[12px_15px_0px_rgba(23,23,23,0.22)]
      `}
    >

      {/* ========================= */}
      {/* RETRO PAPER TEXTURE */}
      {/* ========================= */}

      <div
        className="
          absolute
          inset-0
          pointer-events-none

          opacity-[0.08]

          bg-[radial-gradient(#171717_0.8px,transparent_0.8px)]
          bg-[size:6px_6px]
        "
      />


      {/* ========================= */}
      {/* TOP LEFT JOKER */}
      {/* ========================= */}

      <div
        className="
          absolute

          top-4
          left-2

          text-[#171717]

          z-20
        "
      >

        <span
          className="
            text-[18px]
            font-black
          "
          style={{
            fontFamily: "monospace",
            writingMode: "vertical-rl",
            textOrientation: "upright",
          }}
        >
          JOKER
        </span>

      </div>


      {/* ========================= */}
      {/* JOKER IMAGE */}
      {/* ========================= */}

      <div
        className={`
          absolute

          left-1/2
          -translate-x-1/2

          w-[280px]
          h-[280px]

          flex
          items-center
          justify-center

          transition-all
          duration-[1000ms]

          ease-[cubic-bezier(0.22,1,0.36,1)]

          ${introComplete
            ? "top-[-18px]"
            : "top-[22px]"
          }
        `}
      >

        <img
          src={jokerImage}
          alt="Joker"
          className="
            w-full
            h-full

            object-contain

            drop-shadow-[3px_5px_0px_rgba(23,23,23,0.15)]
          "
        />

      </div>


      {/* ========================= */}
      {/* TYPEWRITER AREA / CHILDREN SLOT */}
      {/* ========================= */}

      {children ? (
        /* When children are provided, render them instead of typewriter */
        <div
          className={`
            absolute
            left-[12px]
            right-[12px]
            top-[235px]
            bottom-[16px]
            transition-all
            duration-500
            ${introComplete
              ? "opacity-100 translate-y-0"
              : "opacity-0 translate-y-4"
            }
          `}
        >
          {children}
        </div>
      ) : (
        /* Default typewriter + divider */
        <>
          <div
            className={`
              absolute
              left-[32px]
              right-[32px]
              bottom-[72px]
              h-[72px]
              flex
              items-center
              justify-center
              text-center
              transition-all
              duration-500
              ${introComplete
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-4"
              }
            `}
          >
            <p
              className="
                text-[14px]
                leading-[1.6]
                font-black
                tracking-[0.08em]
                text-[#171717]
              "
              style={{
                fontFamily: "monospace",
              }}
            >
              {displayText}
              <span className="animate-pulse">
                _
              </span>
            </p>
          </div>

          <div
            className={`
              absolute
              left-1/2
              -translate-x-1/2
              bottom-[58px]
              w-[64px]
              h-[3px]
              bg-[#171717]
              transition-all
              duration-500
              ${introComplete
                ? "opacity-100 scale-x-100"
                : "opacity-0 scale-x-0"
              }
            `}
          />
        </>
      )}


      {!hideBottomLabel && (
        <div
          className="
            absolute
            bottom-4
            right-2
            text-[#171717]
            rotate-180
            z-20
          "
        >
          <span
            className="
              text-[18px]
              font-black
            "
            style={{
              fontFamily: "monospace",
              writingMode: "vertical-rl",
              textOrientation: "upright",
            }}
          >
            JOKER
          </span>
        </div>
      )}


      {/* ========================= */}
      {/* VINTAGE HIGHLIGHT */}
      {/* ========================= */}

      <div
        className="
          absolute

          top-0
          left-0

          w-full
          h-12

          bg-white/30

          pointer-events-none
        "
      />

    </div>
  );
};

export default JokerCard;