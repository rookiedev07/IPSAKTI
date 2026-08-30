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
 * MarkdownRenderer — House of Cards IP-SAKTI Design System
 * Renders LLM-generated markdown (tables, headers, bold, lists, code, blockquotes)
 * with styling matched exactly to the parchment / card-stock aesthetic.
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
              className="text-[11px] font-black uppercase tracking-widest text-[#C93636] mt-4 mb-2 pb-1 border-b border-[#171717]/20"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2
              className="text-[10px] font-black uppercase tracking-widest text-[#C93636] mt-3 mb-1.5 pb-1 border-b border-[#171717]/15"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-[11px] font-bold text-[#171717] uppercase tracking-wide mt-3 mb-1">
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-[11px] font-bold text-[#171717]/80 mt-2 mb-1">
              {children}
            </h4>
          ),

          // ── PARAGRAPH ─────────────────────────────────────────────────────
          p: ({ children }) => (
            <p className="text-[12px] font-sans text-black/90 leading-relaxed mb-2">
              {children}
            </p>
          ),

          // ── BOLD / ITALIC ─────────────────────────────────────────────────
          strong: ({ children }) => (
            <strong className="font-bold text-[#171717]">{children}</strong>
          ),
          em: ({ children }) => (
            <em className="italic text-black/75">{children}</em>
          ),

          // ── UNORDERED LIST ────────────────────────────────────────────────
          ul: ({ children }) => (
            <ul className="list-none pl-0 space-y-1 mb-2">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal pl-5 space-y-1 mb-2 text-[12px] font-sans text-black/90">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="flex items-start gap-2 text-[12px] font-sans text-black/90 leading-relaxed">
              <span className="text-[#C93636] font-black mt-0.5 shrink-0 text-[10px]">&#9670;</span>
              <span>{children}</span>
            </li>
          ),

          // ── HORIZONTAL RULE ───────────────────────────────────────────────
          hr: () => (
            <hr className="border-t border-[#171717]/15 my-3" />
          ),

          // ── BLOCKQUOTE ────────────────────────────────────────────────────
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-[#C93636]/50 pl-3 my-2 bg-amber-50/60 py-2 pr-2 rounded-r text-[11px] font-sans text-black/80 italic">
              {children}
            </blockquote>
          ),

          // ── INLINE CODE ───────────────────────────────────────────────────
          code: ({ inline, children }) => {
            if (inline) {
              return (
                <code className="bg-[#171717]/8 text-[#C93636] font-mono text-[10.5px] px-1.5 py-0.5 rounded border border-[#171717]/15">
                  {children}
                </code>
              );
            }
            return (
              <pre className="bg-[#171717] text-emerald-300 font-mono text-[10.5px] p-3 rounded-md overflow-x-auto my-2 leading-relaxed">
                <code>{children}</code>
              </pre>
            );
          },

          // ── TABLE ─────────────────────────────────────────────────────────
          table: ({ children }) => (
            <div className="overflow-x-auto my-3 rounded-md border-2 border-[#171717]/30 shadow-[3px_3px_0px_rgba(23,23,23,0.12)] bg-white">
              <table className="w-full text-[11px] font-sans border-collapse">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-[#171717] text-[#FFF8E7] border-b-2 border-[#171717]">
              {children}
            </thead>
          ),
          tbody: ({ children }) => (
            <tbody className="divide-y divide-[#171717]/15 bg-white">
              {children}
            </tbody>
          ),
          tr: ({ children }) => (
            <tr className="transition-colors hover:bg-amber-50/80 even:bg-[#171717]/[0.02]">
              {children}
            </tr>
          ),
          th: ({ children }) => (
            <th
              className="px-3 py-2.5 text-left font-black text-[9.5px] uppercase tracking-wider text-[#FFF8E7] whitespace-nowrap border-r border-white/10 last:border-r-0"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="px-3 py-2.5 text-[11px] text-black/85 leading-snug border-r border-[#171717]/10 last:border-r-0 align-top">
              {children}
            </td>
          ),

          // ── LINK ──────────────────────────────────────────────────────────
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noreferrer"
              className="text-blue-700 hover:underline font-mono text-[10.5px]"
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
