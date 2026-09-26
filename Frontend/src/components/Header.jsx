import React from 'react';
import { Menu, Compass, Database } from 'lucide-react';
import LanguageSelector from './LanguageSelector';
import { translations } from '../utils/translations';

export default function Header({
  workspaceTitle = 'Research Workspace',
  onOpenMobileMenu,
  onOpenMobileContext,
  jurisdiction = 'India',
  onToggleJurisdiction,
  currentLang = 'en',
  onSelectLang
}) {
  const t = translations[currentLang] || translations.en;

  return (
    <header className="h-14 px-3 sm:px-5 bg-white border-b border-[#E5DFD3] flex items-center justify-between shrink-0 select-none gap-2">

      {/* Left: Hamburger + Title */}
      <div className="flex items-center gap-2 min-w-0">
        {/* Mobile menu button */}
        <button
          type="button"
          onClick={onOpenMobileMenu}
          aria-label="Open navigation menu"
          className="p-1.5 rounded-lg text-charcoal-600 hover:text-charcoal-900 hover:bg-cream-100 lg:hidden focus:outline-none shrink-0"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Title — truncated so it never overflows */}
        <div className="flex items-center gap-1.5 min-w-0">
          <Compass className="w-4 h-4 text-forest-800 shrink-0 hidden sm:block" />
          <h2 className="text-xs sm:text-sm font-semibold text-charcoal-900 tracking-tight truncate">
            {workspaceTitle}
          </h2>
        </div>
      </div>

      {/* Right: Jurisdiction + Language + Context */}
      <div className="flex items-center gap-1.5 sm:gap-2.5 shrink-0">

        {/* Jurisdiction pill — collapses to icons on xs */}
        <div className="flex items-center bg-[#F4EFE6] p-0.5 rounded-full border border-[#E0D8CA] text-[10px] sm:text-[11px] font-medium">
          <button
            type="button"
            onClick={() => onToggleJurisdiction('India')}
            className={`px-2 sm:px-2.5 py-0.5 rounded-full transition-all duration-150 whitespace-nowrap ${
              jurisdiction === 'India'
                ? 'bg-forest-800 text-cream-50 font-semibold shadow-xs'
                : 'text-charcoal-700 hover:text-charcoal-900'
            }`}
          >
            {/* Short label on mobile, full label on sm+ */}
            <span className="sm:hidden">IND</span>
            <span className="hidden sm:inline">{t.jurisdictionIndia}</span>
          </button>
          <button
            type="button"
            onClick={() => onToggleJurisdiction('International')}
            className={`px-2 sm:px-2.5 py-0.5 rounded-full transition-all duration-150 whitespace-nowrap ${
              jurisdiction === 'International'
                ? 'bg-forest-800 text-cream-50 font-semibold shadow-xs'
                : 'text-charcoal-700 hover:text-charcoal-900'
            }`}
          >
            <span className="sm:hidden">INTL</span>
            <span className="hidden sm:inline">{t.jurisdictionIntl}</span>
          </button>
        </div>

        {/* Language Selector */}
        <LanguageSelector currentLang={currentLang} onSelectLang={onSelectLang} />

        {/* Context panel toggle — mobile/tablet only */}
        {onOpenMobileContext && (
          <button
            type="button"
            onClick={onOpenMobileContext}
            aria-label="Open context panel"
            className="p-1.5 rounded-lg text-charcoal-600 hover:text-charcoal-900 hover:bg-cream-100 lg:hidden focus:outline-none shrink-0"
            title="Open Context & Evidence"
          >
            <Database className="w-4 h-4 text-forest-800" />
          </button>
        )}
      </div>
    </header>
  );
}
