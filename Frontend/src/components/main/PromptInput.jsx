import React from "react";

const PromptInput = ({ inputRef, prompt, onPromptChange, onSubmit, onKeyDown, disabled }) => {
  return (
    <form onSubmit={onSubmit}>
      {/* Label */}
      <p
        className="text-[7px] font-black tracking-[0.15em] uppercase text-[#171717]/50 text-center mb-1.5"
        style={{ fontFamily: "'Press Start 2P', monospace" }}
      >
        ♦ What's your play? ♦
      </p>

      {/* Textarea */}
      <div className="relative h-full">
        <textarea
          ref={inputRef}
          value={prompt}
          onChange={(e) => onPromptChange(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Describe your problem... The Joker will assemble the right agents."
          rows={6}
          disabled={disabled}
          className="
            w-full
            px-2.5 py-2
            bg-[#171717]/5
            border-2 border-[#171717]/20
            focus:border-[#C93636]
            focus:bg-white/60
            rounded
            text-[11px]
            font-mono
            text-[#171717]
            tracking-wide
            leading-relaxed
            placeholder:text-black/25
            placeholder:text-[10px]
            focus:outline-none
            resize-none
            transition-all duration-300
            disabled:opacity-60
          "
          style={{ fontFamily: "monospace" }}
        />

        {/* Submit button */}
        <button
          type="submit"
          disabled={disabled || !prompt.trim()}
          className="
            absolute bottom-2.5 right-1.5
            px-2 py-1
            bg-[#171717] hover:bg-[#C93636]
            disabled:bg-[#171717]/30 disabled:cursor-default
            text-[#FFF8E7] text-[7px]
            tracking-[0.15em] uppercase font-black
            rounded border border-[#171717]
            hover:border-[#C93636]
            disabled:border-transparent
            shadow-[1px_1px_0px_rgba(23,23,23,0.12)]
            hover:-translate-y-0.5
            active:translate-y-0
            transition-all duration-200
            flex items-center gap-1
            cursor-pointer
          "
          style={{ fontFamily: "'Press Start 2P', monospace" }}
        >
          <span className="text-red-400  text-[6px]">♠</span>
          DEAL
        </button>
      </div>
    </form>
  );
};

export default PromptInput;
