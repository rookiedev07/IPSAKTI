import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * Normalizes raw LLM markdown text to ensure proper table parsing:
 * 1. Insures each table row is on its own separate line (fixes collapsed `| |` rows).
 * 2. Insures blank lines before and after table blocks so remark-gfm parser triggers reliably.
 */
function normalizeMarkdown(rawText) {
  if (!rawText || typeof rawText !== "string") return "";

  let text = rawText;

  // 1. Fix collapsed table rows where multiple rows were concatenated without newlines e.g. `| cell | | next row |`
  text = text.replace(/\|\s*\|\s*([0-9\u0966-\u096F\w\u0900-\u097F*#])/g, '|\n| $1');

  // 2. Fix collapsed table delimiter row e.g. `| Header | |---|---|`
  text = text.replace(/\|\s*(\|\s*[-:]+[-| :]*\|)/g, '|\n$1');
  text = text.replace(/(\|[ -:]+\|)\s*\|/g, '$1\n|');

  // 3. Ensure a blank line before any table block starting with `|`
  text = text.replace(/([^\n])\n(\|[^\n]+\|)/g, '$1\n\n$2');

  // 4. Ensure a blank line after any table block
  text = text.replace(/(\|[^\n]+\|)\n([^|\n])/g, '$1\n\n$2');

  return text;
}

/**
 * MarkdownRenderer — IP-SAKTI Problem Solver Design System
 * Renders LLM-generated markdown (tables, headers, bold, lists, code, blockquotes)
 * with styling matched to parchment aesthetic.
 */
const MarkdownRenderer = ({ content, className = "" }) => {
  if (!content) return null;

  const formattedContent = normalizeMarkdown(content);

  return (
    <div className={`hoc-markdown ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // ── HEADINGS ──────────────────────────────────────────────────────
          h1: ({ children }) => (
            <h1
              className="text-[11px] font-black uppercase tracking-widest text-emerald-400 mt-4 mb-2 pb-1 border-b border-white/10"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2
              className="text-[10px] font-black uppercase tracking-widest text-emerald-400 mt-3 mb-1.5 pb-1 border-b border-white/10"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-[11px] font-bold text-white uppercase tracking-wide mt-3 mb-1">
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-[11px] font-bold text-slate-300 mt-2 mb-1">
              {children}
            </h4>
          ),

          // ── PARAGRAPH ─────────────────────────────────────────────────────
          p: ({ children }) => (
            <p className="text-[12px] font-sans text-white/85 leading-relaxed mb-2">
              {children}
            </p>
          ),

          // ── BOLD / ITALIC ─────────────────────────────────────────────────
          strong: ({ children }) => (
            <strong className="font-bold text-white">{children}</strong>
          ),
          em: ({ children }) => (
            <em className="italic text-white/70">{children}</em>
          ),

          // ── UNORDERED LIST ────────────────────────────────────────────────
          ul: ({ children }) => (
            <ul className="list-none pl-0 space-y-1 mb-2">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal pl-5 space-y-1 mb-2 text-[12px] font-sans text-white/85">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="flex items-start gap-2 text-[12px] font-sans text-white/85 leading-relaxed">
              <span className="text-emerald-400 font-black mt-0.5 shrink-0 text-[10px]">&#9670;</span>
              <span>{children}</span>
            </li>
          ),

          // ── HORIZONTAL RULE ───────────────────────────────────────────────
          hr: () => (
            <hr className="border-t border-white/10 my-3" />
          ),

          // ── BLOCKQUOTE ────────────────────────────────────────────────────
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-emerald-500/60 pl-3 my-2 bg-emerald-950/25 py-2 pr-2 rounded-r text-[11px] font-sans text-emerald-100/90 italic">
              {children}
            </blockquote>
          ),

          // ── INLINE CODE ───────────────────────────────────────────────────
          code: ({ inline, children }) => {
            if (inline) {
              return (
                <code className="bg-white/10 text-emerald-300 font-mono text-[10.5px] px-1.5 py-0.5 rounded border border-white/15">
                  {children}
                </code>
              );
            }
            return (
              <pre className="bg-[#0B0D12] text-emerald-300 font-mono text-[10.5px] p-3 rounded-md overflow-x-auto my-2 leading-relaxed border border-white/10">
                <code>{children}</code>
              </pre>
            );
          },

          // ── TABLE ─────────────────────────────────────────────────────────
          table: ({ children }) => (
            <div className="overflow-x-auto my-3 rounded-lg border border-white/15 shadow-[0_4px_20px_rgba(0,0,0,0.5)] bg-[#121622]">
              <table className="w-full text-[11px] font-sans border-collapse">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-[#191E2C] text-white border-b border-white/15">
              {children}
            </thead>
          ),
          tbody: ({ children }) => (
            <tbody className="divide-y divide-white/10 bg-[#121622]">
              {children}
            </tbody>
          ),
          tr: ({ children }) => (
            <tr className="transition-colors hover:bg-white/[0.04] even:bg-white/[0.015]">
              {children}
            </tr>
          ),
          th: ({ children }) => (
            <th
              className="px-3 py-2.5 text-left font-black text-[9.5px] uppercase tracking-wider text-emerald-300 whitespace-nowrap border-r border-white/10 last:border-r-0"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="px-3 py-2.5 text-[11px] text-white/80 leading-snug border-r border-white/10 last:border-r-0 align-top">
              {children}
            </td>
          ),

          // ── LINK ──────────────────────────────────────────────────────────
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noreferrer"
              className="text-sky-400 hover:text-sky-300 hover:underline font-mono text-[10.5px]"
            >
              {children}
            </a>
          ),
        }}
      >
        {formattedContent}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
