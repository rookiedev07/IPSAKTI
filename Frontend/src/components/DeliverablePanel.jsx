import React, { useState } from 'react';
import { FileText, ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';

/**
 * Renders a markdown table from the backend deliverableContent.
 * Falls back gracefully if the content has no table.
 */
export default function DeliverablePanel({ deliverableContent = '', tabTitle = 'COMPLIANCE DOSSIER' }) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!deliverableContent || deliverableContent.trim().length < 20) return null;

  // ── Parse markdown table ──────────────────────────────────────────────────
  const lines = deliverableContent.split('\n');
  const tableLines = lines.filter(l => l.trim().startsWith('|') && !l.match(/^\|[-: ]+\|/));
  const hasParsableTable = tableLines.length >= 2;

  let headers = [];
  let rows = [];

  if (hasParsableTable) {
    headers = tableLines[0]
      .split('|')
      .map(h => h.trim())
      .filter(Boolean);
    rows = tableLines.slice(1).map(row =>
      row.split('|').map(cell => cell.trim()).filter(Boolean)
    ).filter(row => row.length > 0);
  }

  // ── Prose content (bullets after the table) ───────────────────────────────
  const afterTableIdx = lines.findIndex((l, i) => i > 1 && l.trim() && !l.trim().startsWith('|') && !l.match(/^[-:| ]+$/));
  const prose = afterTableIdx > -1
    ? lines.slice(afterTableIdx).join('\n').trim()
    : '';

  const handleCopy = () => {
    navigator.clipboard.writeText(deliverableContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="bg-white rounded-2xl border border-borderLight shadow-soft mb-6 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-cream-100">
        <button
          type="button"
          onClick={() => setIsCollapsed(v => !v)}
          className="flex items-center gap-2 text-left group flex-1"
        >
          <div className="w-7 h-7 rounded-lg bg-forest-800 text-cream-50 flex items-center justify-center shrink-0">
            <FileText className="w-3.5 h-3.5" />
          </div>
          <div>
            <span className="text-xs uppercase tracking-wider font-semibold text-charcoal-900 block">
              {tabTitle}
            </span>
            <span className="text-[10px] text-charcoal-500">
              {hasParsableTable ? `${rows.length} stage${rows.length !== 1 ? 's' : ''} · ${headers.length} columns` : 'Statutory roadmap'}
            </span>
          </div>
          {isCollapsed
            ? <ChevronDown className="w-4 h-4 text-charcoal-400 ml-auto" />
            : <ChevronUp className="w-4 h-4 text-charcoal-400 ml-auto" />
          }
        </button>

        <button
          type="button"
          onClick={handleCopy}
          title="Copy full dossier"
          className="ml-3 p-1.5 rounded-lg text-charcoal-500 hover:bg-cream-50 transition-colors"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
        </button>
      </div>

      {!isCollapsed && (
        <div className="p-4 sm:p-5">
          {/* Table rendering */}
          {hasParsableTable ? (
            <div className="overflow-x-auto rounded-xl border border-borderLight">
              <table className="w-full text-[12px] border-collapse min-w-[640px]">
                <thead>
                  <tr className="bg-forest-800 text-cream-50">
                    {headers.map((h, i) => (
                      <th
                        key={i}
                        className="px-3 py-2.5 text-left font-semibold text-[11px] uppercase tracking-wide whitespace-nowrap first:rounded-tl-xl last:rounded-tr-xl"
                      >
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row, ri) => (
                    <tr
                      key={ri}
                      className={`border-t border-borderLight/60 ${ri % 2 === 0 ? 'bg-white' : 'bg-cream-50/50'} hover:bg-sage-50/40 transition-colors`}
                    >
                      {headers.map((_, ci) => (
                        <td
                          key={ci}
                          className={`px-3 py-2.5 text-charcoal-800 leading-snug align-top ${ci === 0 ? 'font-semibold text-forest-900 whitespace-nowrap' : ''}`}
                        >
                          {row[ci] || '—'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            /* No table found — render as formatted prose */
            <div className="text-[13px] text-charcoal-800 leading-relaxed whitespace-pre-wrap">
              {deliverableContent
                .replace(/#{1,6}\s+/g, '')
                .replace(/\*{1,3}([^*]+)\*{1,3}/g, '$1')
                .replace(/\|[-: |]+\n/g, '')
                .trim()}
            </div>
          )}

          {/* Prose / bullet points after table */}
          {prose && (
            <div className="mt-4 pt-4 border-t border-cream-100 space-y-2">
              {prose.split('\n').filter(l => l.trim()).map((line, i) => {
                const isBullet = /^[-•*]\s+/.test(line.trim());
                const isBold   = /^\*\*/.test(line.trim());
                const clean    = line.replace(/^[-•*]\s+/, '').replace(/\*{1,3}/g, '').trim();
                if (!clean) return null;
                if (isBullet) {
                  return (
                    <div key={i} className="flex items-start gap-2 text-[12.5px] text-charcoal-700">
                      <span className="w-1.5 h-1.5 rounded-full bg-forest-700 mt-1.5 shrink-0" />
                      <span>{clean}</span>
                    </div>
                  );
                }
                if (isBold || /^#+/.test(line.trim())) {
                  return <p key={i} className="text-xs font-semibold text-charcoal-900 mt-3">{clean.replace(/^#+\s*/, '')}</p>;
                }
                return <p key={i} className="text-[12px] text-charcoal-600 leading-relaxed">{clean}</p>;
              })}
            </div>
          )}
        </div>
      )}
    </section>
  );
}
