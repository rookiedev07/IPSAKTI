import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import JokerCard from "../components/cards/JokerCard";
import MainBackground from "../components/main/MainBackground";
import MainHeader from "../components/main/MainHeader";
import MainFooter from "../components/main/MainFooter";
import PromptInput from "../components/main/PromptInput";
import AgentDeck from "../components/main/AgentDeck";
import AgentStatus from "../components/main/AgentStatus";
import DealtCards from "../components/main/DealtCards";
import OutputScreen from "../components/main/OutputScreen";
import { matchPrompt } from "../services/promptService";

const Main = () => {
  const navigate = useNavigate();
  const [operator, setOperator] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [phase, setPhase] = useState("center"); // "center" → "shifted"
  const [jokerReady, setJokerReady] = useState(false);
  const [cardsDealt, setCardsDealt] = useState(false);
  const [showOutput, setShowOutput] = useState(false);
  const [matchedData, setMatchedData] = useState(null);
  const [isMatching, setIsMatching] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    const stored = localStorage.getItem("hoc_operator");
    if (stored) {
      try {
        setOperator(JSON.parse(stored));
      } catch (e) {
        console.error("Error parsing operator data", e);
      }
    }
    // Joker entrance
    setTimeout(() => setJokerReady(true), 300);
  }, []);

  // Auto-focus input once joker settles
  useEffect(() => {
    if (jokerReady && phase === "center" && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 800);
    }
  }, [jokerReady, phase]);

  const handleLogout = () => {
    localStorage.removeItem("hoc_token");
    localStorage.removeItem("hoc_operator");
    navigate("/login");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    setPhase("shifted");
    setCardsDealt(false);
    setShowOutput(false);
    setMatchedData(null);
    setIsMatching(true);

    try {
      // Asynchronously call the Prompt Engine API while animations play
      const result = await matchPrompt(prompt, { language: "en" });
      setMatchedData(result);
    } catch (err) {
      console.error("Error matching prompt:", err);
    } finally {
      setIsMatching(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInitializationComplete = () => {
    setCardsDealt(true);
  };

  const handleOutputTransition = () => {
    setShowOutput(true);
  };

  const handleReset = () => {
    setShowOutput(false);
    setCardsDealt(false);
    setPhase("center");
    setPrompt("");
    setMatchedData(null);
  };

  /**
   * Re-fetches the current prompt in the selected target language.
   * Called by OutputScreen when the user switches the language toggle.
   */
  const handleTranslate = async (targetLanguage, promptOverride) => {
    const textToMatch = promptOverride || prompt || matchedData?.rawPrompt;
    if (!textToMatch || !textToMatch.trim()) return;
    try {
      const result = await matchPrompt(textToMatch, { language: targetLanguage });
      setMatchedData(result);
    } catch (err) {
      console.error("Translation re-fetch error:", err);
    }
  };

  return (
    <div className="min-h-screen bg-[#F6F3EA] text-[#171717] flex flex-col relative overflow-hidden">

      <MainBackground />

      <MainHeader operator={operator} onLogout={handleLogout} />

      {/* ===== Main Content ===== */}
      <main className="relative z-10 flex-1 flex items-center justify-center px-4 py-4 sm:py-6">
        {showOutput ? (
          <div className="w-full flex items-center justify-center">
            <OutputScreen
              prompt={prompt}
              matchedData={matchedData}
              operator={operator}
              onReset={handleReset}
              onTranslate={handleTranslate}
            />
          </div>
        ) : (
          <div className="relative flex items-center justify-center w-full max-w-[1300px] min-h-[480px]">

            {/* ---- JOKER CARD (center → slides left) ---- */}
            <div
              className="transition-all duration-[900ms] ease-[cubic-bezier(0.22,1,0.36,1)] z-30"
              style={{
                transform: phase === "center"
                  ? "translateX(0px)"
                  : "translateX(calc(-50vw + 184px))",
              }}
            >
              <div
                className={`
                  transition-all duration-[800ms] ease-[cubic-bezier(0.22,1,0.36,1)]
                  ${jokerReady
                    ? "opacity-100 translate-y-0 scale-100"
                    : "opacity-0 translate-y-[140px] scale-95"
                  }
                `}
              >
                {/* Glow behind joker */}
                <div className="absolute -inset-6 bg-red-400/10 blur-[40px] rounded-full pointer-events-none" />

                <JokerCard large hideBottomLabel>
                  <PromptInput
                    inputRef={inputRef}
                    prompt={prompt}
                    onPromptChange={setPrompt}
                    onSubmit={handleSubmit}
                    onKeyDown={handleKeyDown}
                    disabled={phase === "shifted"}
                  />
                  <AgentStatus
                    active={phase === "shifted"}
                    onComplete={handleInitializationComplete}
                    isDealt={cardsDealt}
                  />
                </JokerCard>
              </div>
            </div>

            {/* ---- STAGE: 5 DEALT CARDS (Ace to 5) — shifted higher top-right ---- */}
            {phase === "shifted" && (
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-20 translate-x-6 sm:translate-x-12 md:translate-x-20 lg:translate-x-24 -translate-y-20 sm:-translate-y-28 md:-translate-y-36 lg:-translate-y-40">
                <DealtCards
                  visible={cardsDealt}
                  agents={matchedData?.agents}
                  isMatching={isMatching}
                  matchedData={matchedData}
                  onComplete={handleOutputTransition}
                />
              </div>
            )}

            {/* ---- DECK (appears bottom-right after submit, updates to 6 after deal) ---- */}
            <AgentDeck
              visible={phase === "shifted"}
              dealtCount={cardsDealt ? 5 : 0}
            />

          </div>
        )}
      </main>

      <MainFooter />
    </div>
  );
};

export default Main;
