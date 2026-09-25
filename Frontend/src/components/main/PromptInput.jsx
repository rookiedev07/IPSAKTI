import React from "react";

const EXAMPLE_PROMPTS = [
  "Patent an ashwagandha extract under Indian Patents Act",
  "EU cosmetic product safety assessment (CPSR) filing",
  "Madrid System trademark registration for Ayurvedic brand",
  "FSSAI Ayurveda Aahar product compliance",
  "NBA Form III approval for biological resource use",
  "US FDA NDI notification for botanical supplement",
];

const PromptInput = ({ inputRef, prompt, onPromptChange, onSubmit, onKeyDown, disabled }) => {
  const handleChipClick = (text) => {
    if (disabled) return;
    onPromptChange(text);
    setTimeout(() => inputRef.current?.focus(), 50);
  };

  return (
    <div className="w-full">
      {/* Main prompt form */}
      <form onSubmit={onSubmit} className="prompt-focus-glow w-full">
        <div
          className="
            relative bg-[#131722]/95 border-2 border-white/15
            rounded-xl shadow-card-lg transition-all duration-300
            hover:border-white/30 hover:shadow-card-hover backdrop-blur-md
          "
        >
          {/* Textarea */}
          <textarea
            ref={inputRef}
            value={prompt}
            onChange={(e) => onPromptChange(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Describe your problem...&#10;The AI Multi-Agent Council will analyze, strategize, and solve it."
            rows={5}
            disabled={disabled}
            id="main-prompt-textarea"
            className="
              w-full px-5 pt-5 pb-14
              bg-transparent
              text-[13px] font-mono text-[#F1F3F9]
              tracking-wide leading-relaxed
              placeholder:text-white/30 placeholder:text-[12px] placeholder:font-sans
              focus:outline-none resize-none
              disabled:opacity-60 disabled:cursor-not-allowed
              rounded-xl
            "
          />

          {/* Bottom bar inside textarea */}
          <div className="absolute bottom-0 left-0 right-0 flex items-center justify-between px-4 pb-3">
            {/* Character count */}
            <span className="text-[9px] font-mono text-white/40">
              {prompt.length > 0 ? `${prompt.length} chars • Enter to submit` : "Enter to submit • Shift+Enter for new line"}
            </span>

            {/* Submit button with standard prompt-send arrow */}
            <button
              type="submit"
              disabled={disabled || !prompt.trim()}
              id="submit-prompt-btn"
              title="Send Problem"
              aria-label="Send Problem"
              className="
                group flex items-center justify-center
                w-9 h-9 sm:w-10 sm:h-10
                bg-emerald-500 hover:bg-emerald-400 active:scale-95
                disabled:bg-white/10 disabled:cursor-not-allowed disabled:text-white/30
                text-white
                rounded-xl border border-emerald-400/50 hover:border-emerald-300
                disabled:border-transparent
                shadow-[0_0_16px_rgba(16,185,129,0.35)] hover:shadow-[0_0_24px_rgba(16,185,129,0.55)]
                hover:-translate-y-0.5 active:translate-y-0
                transition-all duration-200
                cursor-pointer
              "
            >
              <svg
                className="w-4 h-4 sm:w-4.5 sm:h-4.5 transform transition-transform duration-200 group-hover:-translate-y-0.5"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="12" y1="19" x2="12" y2="5" />
                <polyline points="5 12 12 5 19 12" />
              </svg>
            </button>
          </div>
        </div>
      </form>

      {/* Example prompt chips */}
      {!disabled && prompt.length === 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          <span
            className="text-[8px] font-mono text-white/40 uppercase tracking-wider self-center shrink-0"
            style={{ fontFamily: "'Press Start 2P', monospace" }}
          >
            Try:
          </span>
          {EXAMPLE_PROMPTS.map((ex, i) => (
            <button
              key={i}
              onClick={() => handleChipClick(ex)}
              className="
                chip-entrance
                px-3 py-1.5
                bg-[#161B26]/85 hover:bg-[#1E2536]
                border border-white/10 hover:border-emerald-400/40 hover:text-emerald-300
                text-[10px] font-mono text-white/70 hover:text-white
                rounded-full shadow-sm
                transition-all duration-200 hover:-translate-y-0.5
                cursor-pointer text-left
              "
              style={{ "--chip-delay": `${0.3 + i * 0.06}s` }}
            >
              {ex}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default PromptInput;
