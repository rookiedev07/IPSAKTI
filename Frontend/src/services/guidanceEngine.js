/**
 * guidanceEngine.js — House of Cards ↔ IP-SAKTI Frontend Bridge
 *
 * Calls POST /api/prompt/orchestrate and maps the backend 9-layer response
 * to the exact shape consumed by AnswerView, EvidencePanel, ContextPanel, etc.
 *
 * ┌─────────────────────────────────────────────────────────┐
 * │  Backend field          → Frontend field                │
 * ├─────────────────────────────────────────────────────────┤
 * │  architecture.overview  → shortAnswer (cleaned prose)   │
 * │  architecture.dataFlow  → keyFindings (bullet strings)  │
 * │  architecture.overview  → whyItMatters (2nd paragraph)  │
 * │  deliverableContent     → deliverableContent (markdown) │
 * │  citations[]            → sources[] (EvidencePanel fmt) │
 * │  escalationDossier      → nextSteps [{step,desc}]       │
 * │  confidence             → confidenceScore (0-1)         │
 * │  confidenceRating       → confidenceLevel string        │
 * └─────────────────────────────────────────────────────────┘
 */

import { orchestratePromptApi, classifyProductApi } from './api';

// ─── Markdown stripping ───────────────────────────────────────────────────────
/** Strip markdown syntax for use in plain-text fields */
function stripMarkdown(text = '') {
  return text
    .replace(/#{1,6}\s+/g, '')          // headings
    .replace(/\*{1,3}([^*]+)\*{1,3}/g, '$1') // bold/italic
    .replace(/`{1,3}[^`]*`{1,3}/g, '')  // code
    .replace(/^\s*[-*•]\s+/gm, '')       // list markers
    .replace(/\|[-: ]+\|[-| :]+/g, '')   // table separator rows
    .replace(/\|/g, ' ')                 // table pipes
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // links → label
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/** Extract clean paragraph sentences (no markdown noise) */
function extractParagraphSentences(rawMarkdown = '', maxChars = 420) {
  // Remove section headings and their content markers
  const cleaned = stripMarkdown(rawMarkdown);
  // Split into non-empty sentences
  const sentences = cleaned
    .split(/(?<=[.!?])\s+/)
    .map(s => s.trim())
    .filter(s => s.length > 20 && !/^(tier|section|\d+\.)/i.test(s));

  let out = '';
  for (const s of sentences) {
    if (out.length + s.length > maxChars) break;
    out += (out ? ' ' : '') + s;
  }
  return out || cleaned.slice(0, maxChars);
}

/** Extract the second paragraph (or half of text) as "why this matters" */
function extractWhyItMatters(rawMarkdown = '') {
  const cleaned = stripMarkdown(rawMarkdown);
  const paragraphs = cleaned.split(/\n{2,}/).map(p => p.trim()).filter(p => p.length > 40);
  // Prefer 2nd paragraph; if only one, take second half of it
  if (paragraphs.length >= 2) return paragraphs[1].slice(0, 500);
  if (paragraphs.length === 1) {
    const p = paragraphs[0];
    const mid = Math.floor(p.length / 2);
    const splitAt = p.indexOf(' ', mid);
    return splitAt > -1 ? p.slice(splitAt + 1).slice(0, 400) : p.slice(0, 400);
  }
  return '';
}

// ─── Confidence parsing ───────────────────────────────────────────────────────
function parseConfidenceScore(raw) {
  if (!raw) return 0.85;
  if (typeof raw === 'number') return Math.min(1, Math.max(0, raw));
  const pct = parseFloat(String(raw).replace('%', ''));
  if (!isNaN(pct)) return Math.min(1, Math.max(0, pct > 1 ? pct / 100 : pct));
  return 0.85;
}

function mapConfidenceLevel(rating) {
  const r = (rating || '').toLowerCase();
  if (r === 'high') return 'high';
  if (r.includes('medium') || r.includes('moderate')) return 'moderate';
  if (r === 'low') return 'review';
  return 'moderate';
}

// ─── Source mapping (backend → EvidencePanel shape) ──────────────────────────
/**
 * Backend citation shape: { id, title, summary, section_or_article, authority, url, ... }
 * EvidencePanel needs:   { id, domain, topic, text, source_name, source_url, jurisdiction, confidence }
 */
function mapCitationToSource(citation, index) {
  if (!citation) return null;

  // Derive domain from citation id prefix
  const id = citation.id || '';
  let domain = 'patent_law';
  if (/^abs-|biodiv|nba/i.test(id))        domain = 'biodiversity_abs';
  else if (/^tm-|trademark/i.test(id))      domain = 'trademark_gi';
  else if (/^gi-/i.test(id))               domain = 'trademark_gi';
  else if (/^fssai|aahar|food/i.test(id))  domain = 'food_regulatory';
  else if (/^eu-|ec-/i.test(id))           domain = 'international_regulatory';
  else if (/^intl-|wipo|pct/i.test(id))    domain = 'international_regulatory';
  else if (/^in-|patent|tkdl|sec-3/i.test(id)) domain = 'patent_law';

  const jurisdiction = citation.jurisdiction
    || (/^eu-|ec-/i.test(id) ? 'EU' : /^intl-|wipo/i.test(id) ? 'International' : 'India');

  // Build readable topic from title + section
  const section = citation.section_or_article ? ` — ${citation.section_or_article}` : '';
  const topic = (citation.title || citation.id || `Statutory Source ${index + 1}`) + section;

  // Use summary as the display text
  const text = citation.summary || citation.text || citation.content || '';

  // Source name = authority or title
  const source_name = citation.authority || citation.title || citation.id || 'Official Statutory Register';

  return {
    id: citation.id || `src-${index}`,
    domain,
    topic,
    text,
    source_name,
    source_url: citation.url || citation.source_url || null,
    jurisdiction,
    confidence: citation.score ? citation.score / 100 : null,
  };
}

// ─── Key findings builder ─────────────────────────────────────────────────────
/**
 * Build AnswerView keyFindings (array of plain strings) from:
 * - backend citations (most authoritative)
 * - strategy text (first 3 distinct bullet-like facts)
 * - verification text (statutory validation results)
 */
function buildKeyFindings(strategyText = '', citations = [], verificationText = '') {
  const findings = [];

  // 1. From citations — pull the most critical statutory facts
  const citsToUse = (citations || []).slice(0, 3);
  citsToUse.forEach(c => {
    const section = c.section_or_article ? ` (${c.section_or_article})` : '';
    const summary = (c.summary || '').slice(0, 200);
    if (summary) {
      findings.push(`${c.title || c.id}${section}: ${summary}`);
    }
  });

  // 2. If we have fewer than 3, supplement from strategy bullet points
  if (findings.length < 3) {
    const bulletRegex = /^[-•*]\s+(.+)$/gm;
    const stratBullets = [...(strategyText || '').matchAll(bulletRegex)];
    stratBullets
      .map(m => m[1].trim())
      .filter(b => b.length > 30 && !findings.some(f => f.includes(b.slice(0, 30))))
      .slice(0, 3 - findings.length)
      .forEach(b => findings.push(stripMarkdown(b).slice(0, 250)));
  }

  // 3. Last resort: extract sentences from strategy
  if (findings.length < 2) {
    const sentences = stripMarkdown(strategyText)
      .split(/(?<=[.!?])\s+/)
      .filter(s => s.length > 60)
      .slice(0, 3 - findings.length);
    sentences.forEach(s => findings.push(s.slice(0, 250)));
  }

  // 4. Verifier result
  if (verificationText) {
    const vLines = verificationText
      .split('\n')
      .map(l => l.replace(/^[✓✗•\-*]+\s*/, '').trim())
      .filter(l => l.length > 15 && l.length < 200)
      .slice(0, 2);
    vLines.forEach(l => findings.push(l));
  }

  return findings.filter(Boolean).slice(0, 5);
}

// ─── Next Steps builder ───────────────────────────────────────────────────────
/**
 * Build [{step, desc}] array from escalation dossier questions or
 * deliverable content bullet points.
 */
function buildNextSteps(escalationDossier, deliverableContent = '') {
  // Prefer escalation questions — rephrase as action items
  if (escalationDossier?.keyQuestions?.length) {
    return escalationDossier.keyQuestions.slice(0, 4).map((q, i) => ({
      step: `Due Diligence Step ${i + 1}`,
      desc: stripMarkdown(q).slice(0, 280),
    }));
  }

  // Extract bullet points from deliverable (outside the table)
  const afterTable = deliverableContent.replace(/\|.+\n/g, '').replace(/^[-|: ]+$/gm, '');
  const bulletRegex = /^[-•*]\s+(.+)$/gm;
  const bullets = [...afterTable.matchAll(bulletRegex)];
  if (bullets.length >= 2) {
    return bullets.slice(0, 4).map((m, i) => {
      const text = stripMarkdown(m[1]).slice(0, 280);
      const colonIdx = text.indexOf(':');
      if (colonIdx > 0 && colonIdx < 60) {
        return { step: text.slice(0, colonIdx).trim(), desc: text.slice(colonIdx + 1).trim() };
      }
      return { step: `Recommended Action ${i + 1}`, desc: text };
    });
  }

  // Fallback defaults
  return [
    { step: 'Conduct TKDL & Prior Art Search', desc: 'Verify whether active botanicals or combinations are codified in classical texts (Charaka Samhita, Sushruta Samhita, TKDL database).' },
    { step: 'Document Biological Resource Provenance', desc: 'Catalog state, forest division, or agro-climatic source of all plant matter for Section 10(4) origin disclosures.' },
    { step: 'Assess NBA / SBB Registration Status', desc: 'Submit Form I (NBA for foreign-linked entities) or Form III (SBB intimation for domestic businesses) before any commercial filing.' },
    { step: 'Review Claims with AYUSH Patent Specialist', desc: 'Engage an accredited patent agent familiar with Section 3(p) jurisprudence to draft defensive or process-focused claims.' },
  ];
}

// ─── Jurisdiction analysis ────────────────────────────────────────────────────
function buildJurisdictionAnalysis(deliverableContent = '') {
  // Try to extract India-specific and International points from deliverable
  const indiaPoints = [];
  const intlPoints = [];

  // Look for India-related statute mentions in deliverable
  const indiaStatutes = (deliverableContent || '').match(
    /(?:Section 3\([a-z]\)|Rule 158B|AYUSH|CDSCO|FSSAI|InPASS|TKDL|NBA|Patents Act|Biological Diversity)[^|\n]*/gi
  );
  if (indiaStatutes) {
    indiaStatutes.slice(0, 3).forEach(s =>
      indiaPoints.push(stripMarkdown(s).slice(0, 180))
    );
  }

  // Look for International mentions
  const intlStatutes = (deliverableContent || '').match(
    /(?:PCT|WIPO|USPTO|EMA|US FDA|21 CFR|GRATK|Nagoya|Madrid Protocol)[^|\n]*/gi
  );
  if (intlStatutes) {
    intlStatutes.slice(0, 3).forEach(s =>
      intlPoints.push(stripMarkdown(s).slice(0, 180))
    );
  }

  return {
    india: {
      title: 'India (AYUSH / IPO / CDSCO / FSSAI)',
      points: indiaPoints.length >= 2 ? indiaPoints : [
        'Governed by Indian Patents Act 1970 (Section 3(p), Section 10(4)).',
        'Dual regulator: Ministry of AYUSH (ASU classical/proprietary) vs CDSCO (Phytopharmaceuticals).',
        'Strict domestic biological material disclosure and NBA Section 6(1A) compliance required.',
        'FSSAI Ayurveda Aahara regulations restrict health claims without prior statutory validation.',
      ],
    },
    international: {
      title: 'International (WIPO / US FDA / EMA)',
      points: intlPoints.length >= 2 ? intlPoints : [
        'WIPO GRATK Treaty (May 2024): Mandatory disclosure of genetic resources and traditional knowledge origins.',
        'USPTO, EPO, and UKPTO actively cross-examine TKDL prior art during examination.',
        'US FDA regulates herbal formulations as Dietary Supplements (DSHEA 1994) or Botanical Drugs (Phase 1–3 trials required).',
        'EMA Herbal Medicinal Products Directive (HMPC) requires 30 years of medicinal use evidence.',
      ],
    },
  };
}

// ─── Primary domain label ─────────────────────────────────────────────────────
function buildPrimaryDomain(backendData) {
  const sub = backendData?.subcategory || backendData?.category || '';
  if (sub) return sub.replace(/_/g, ' ').replace(/\bAYURVEDA\b/i, 'Ayurveda');
  const domainId = backendData?.architecture?.jurisdiction?.mode;
  if (domainId === 'INTERNATIONAL') return 'International IP & Regulatory';
  return 'Regulatory & IP Guidance';
}

// ═══════════════════════════════════════════════════════════════════════════════
// Main export
// ═══════════════════════════════════════════════════════════════════════════════
export async function generateGuidance({ query, jurisdiction = 'India', attachedFile = null, lang = 'en' }) {

  // ── 1. Fast client-side classification (always available) ─────────────────
  const classification = await classifyProductApi(query);

  // ── 2. Backend orchestration call ─────────────────────────────────────────
  let backendData = null;
  try {
    backendData = await orchestratePromptApi(query, lang, jurisdiction);
  } catch (err) {
    console.error('[guidanceEngine] Backend call failed:', err.message);
  }

  // ── 3. Map backend response → frontend shape ───────────────────────────────
  if (backendData?.success) {
    const arch              = backendData.architecture || {};
    const strategyRaw       = arch.overview || '';
    const dataFlow          = arch.dataFlow || [];
    const citations         = backendData.citations || [];
    const deliverable       = backendData.deliverableContent || '';
    const verificationText  = backendData.verificationReport || arch.verification || '';
    const escalationDossier = backendData.escalationDossier || arch.escalationDossier || null;
    const jurisdictionObj   = backendData.jurisdiction || {};

    // Confidence
    const rawConfidence  = backendData.confidence;
    const confidenceScore = parseConfidenceScore(rawConfidence);
    const confidenceLevel = mapConfidenceLevel(backendData.confidenceRating);

    // Short answer — first clean paragraph from strategy
    const shortAnswer = extractParagraphSentences(strategyRaw, 460) || query;

    // Why it matters — second paragraph from strategy
    const whyItMatters = extractWhyItMatters(strategyRaw)
      || 'Misclassifying an Ayurvedic product can trigger regulatory seizure under the Drugs & Cosmetics Act or cancellation of FSSAI licenses due to non-compliant therapeutic advertising.';

    // Key findings from citations + strategy bullets
    const keyFindings = buildKeyFindings(strategyRaw, citations, verificationText);

    // Next steps
    const nextSteps = buildNextSteps(escalationDossier, deliverable);

    // Sources — map from backend citations to EvidencePanel shape
    const sources = citations
      .map((c, i) => mapCitationToSource(c, i))
      .filter(Boolean);

    // Jurisdiction analysis
    const jurisdictionAnalysis = buildJurisdictionAnalysis(deliverable);

    // Primary domain label
    const primaryDomain = buildPrimaryDomain(backendData);

    // Clarifying questions — empty (backend doesn't produce them currently)
    const clarifyingQuestions = [];

    const limitations = [
      'This guidance reflects statutory provisions and regulatory notifications as of 2024–2026. Local State Biodiversity Board rules may enforce localized interpretations.',
      'Prior art clearance cannot guarantee absolute patent grant due to unpublished pending applications or undocumented oral traditional knowledge not cataloged in TKDL.',
      'This output is designed for research and exploratory planning. Formal legal opinions require engagement of an accredited patent attorney.',
    ];

    return {
      id:                  `res_${Date.now()}`,
      timestamp:            new Date().toISOString(),
      query,
      attachedFile:         attachedFile ? { name: attachedFile.name, size: attachedFile.size } : null,
      jurisdiction,
      primaryDomain,
      confidenceScore,
      confidenceLevel,
      shortAnswer,
      keyFindings,
      whyItMatters,
      nextSteps,
      classification,
      sources,
      jurisdictionAnalysis,
      clarifyingQuestions,
      limitations,
      // Rich backend content — rendered by DeliverablePanel
      deliverableContent:  deliverable,
      agents:              backendData.agents || [],
      logs:                backendData.logs || [],
      hash:                backendData.hash || '',
      escalationDossier,
      architecture:        arch,
      tabTitle:            backendData.tabTitle || 'COMPLIANCE DOSSIER',
      howGenerated: {
        signals:               classification.matched_signals || [],
        rationale:             classification.rationale || '',
        retrievalSourcesCount: sources.length,
        statutesScanned:       ['Patents Act 1970 §3(p)', 'Biological Diversity Act 2002', 'FSSAI 2022', 'WIPO GRATK 2024'],
        source:                backendData.source || 'nim_deepseek_5agent',
        modelUsed:             arch.modelUsed || 'NVIDIA NIM',
      },
    };
  }

  // ── 4. Client-side fallback when backend is unreachable ───────────────────
  console.warn('[guidanceEngine] Using client-side fallback — backend offline or returned error.');
  return buildClientSideFallback({ query, jurisdiction, attachedFile, lang, classification });
}

// ─── Client-side fallback (backend offline) ───────────────────────────────────
function buildClientSideFallback({ query, jurisdiction, attachedFile, lang, classification }) {
  const queryLower = query.toLowerCase();
  const isPatent    = /patent|3\(p\)|inventive|novelty|prior art|tkdl|exclusion/i.test(queryLower);
  const isAbs       = /abs|biodiversity|nba|access and benefit|foreign|export|sbb/i.test(queryLower);
  const isFood      = /food|aahar|supplement|nutraceutical|fssai|dietary/i.test(queryLower);
  const isCosmetic  = /cosmetic|cream|lotion|face|skin|shampoo/i.test(queryLower);
  const isPhyto     = /phytopharmaceutical|standardized extract|cdsco|rule 122e|purified fraction/i.test(queryLower);

  let primaryDomain  = 'Regulatory & IP Guidance';
  let confidenceScore = 0.72;
  if (isPatent)  { primaryDomain = 'Indian Patent Act Section 3(p) & Prior Art'; confidenceScore = 0.78; }
  if (isAbs)     { primaryDomain = 'Biological Diversity Act & ABS'; confidenceScore = 0.76; }
  if (isFood)    { primaryDomain = 'FSSAI Ayurveda Aahara Regulations'; confidenceScore = 0.80; }

  let shortAnswer = '';
  if (isPatent) shortAnswer = 'Under Section 3(p) of the Indian Patents Act 1970, formulations that merely aggregate known traditional Ayurvedic properties cannot be patented. Non-obvious synergistic combinations supported by empirical data clearing TKDL prior art can qualify for patent protection.';
  else if (isAbs) shortAnswer = 'Under the Biological Diversity Act 2002, accessing Indian biological resources for commercial use or IP filing requires prior NBA clearance (Form III for patent-linked IPR) and SBB intimation under Section 6(1).';
  else if (isFood) shortAnswer = 'Products formulated as Ayurveda Aahara fall under FSSAI 2022 regulations and are strictly barred from claiming to cure, treat, or mitigate human diseases in advertising or labeling.';
  else if (isPhyto) shortAnswer = 'Purified plant fractions with specific therapeutic claims are regulated by CDSCO as phytopharmaceutical drugs under Rule 122E — not as ASU medicines under AYUSH — and require formal clinical validation.';
  else if (isCosmetic) shortAnswer = 'Herbal cosmetics are regulated under the Drugs and Cosmetics Act and cannot lawfully make therapeutic or curative medicinal claims in labeling or advertising.';
  else shortAnswer = `Based on Indian regulatory standards, this formulation aligns with the '${classification.category.replace(/_/g, ' ')}' pathway. Compliance requires verifying classical text grounding, ensuring absence of prohibited medicinal claims, and confirming NBA intimation requirements.`;

  const keyFindings = isPatent ? [
    'Section 3(p) Bar: Examiners cross-check TKDL and reject claims where each herb\'s property is documented in traditional lore — even novel combinations may fail.',
    'Mandatory Biological Material Disclosure (Section 10(4)): Applicants must disclose the exact geographic source of botanical inputs or face pre-grant opposition under Section 25(1)(j).',
    'Patent Amendment Rules 2024: Pre-grant opposition reply windows tightened to 2 months under amended Rule 55.',
  ] : isAbs ? [
    'NBA Clearance Mandate: Section 6 requires approval before any patent grant based on biological resources sourced in India.',
    'Section 6(1A) 2024 Update: Domestic Indian entities must register with NBA before a patent can be sealed — closing prior loopholes.',
    'Benefit Sharing Levies: Commercialization triggers 0.1%–0.5% ex-factory revenue sharing or negotiated MAT benefit-sharing agreements.',
  ] : [
    `Regulatory Classification: Classified as '${classification.category.replace(/_/g, ' ')}' with ${classification.confidence} confidence based on detected formulation signals.`,
    'Labeling & Claim Boundaries: Prohibited from using disease-cure vocabulary under the Drugs and Magic Remedies (Objectionable Advertisements) Act 1954.',
    'Dual Track Architecture: Distinct evidentiary standards exist between AYUSH classical licenses (Rule 158B) and CDSCO new drug pathways.',
  ];

  if (classification.contradiction_flag) keyFindings.push(`⚠️ Regulatory Risk: ${classification.contradiction_flag}`);

  const whyItMatters = isPatent
    ? 'Filing a patent on traditional herbal knowledge without establishing synergistic non-obviousness invites costly pre-grant opposition by CSIR/TKDL and risk of immediate revocation.'
    : isAbs
    ? 'Failure to secure NBA approval or SBB intimation before commercialization or IP filing is a punishable statutory violation with severe financial penalties and freezing of patent grants.'
    : 'Misclassifying an Ayurvedic product can lead to regulatory seizure under the Drugs & Cosmetics Act or cancellation of FSSAI licenses due to non-compliant therapeutic advertising.';

  return {
    id:              `res_${Date.now()}`,
    timestamp:        new Date().toISOString(),
    query,
    attachedFile:     attachedFile ? { name: attachedFile.name, size: attachedFile.size } : null,
    jurisdiction,
    primaryDomain,
    confidenceScore,
    confidenceLevel:  confidenceScore >= 0.80 ? 'high' : 'moderate',
    shortAnswer,
    keyFindings,
    whyItMatters,
    nextSteps: [
      { step: 'Conduct TKDL & Prior Art Search', desc: 'Verify whether active botanicals or combinations are already codified in classical texts like Charaka Samhita or Bhavaprakasha and TKDL database.' },
      { step: 'Document Biological Resource Provenance', desc: 'Catalog state, forest division, or agro-climatic source of all plant matter to satisfy Section 10(4) origin disclosures.' },
      { step: 'Assess NBA / SBB Registration Status', desc: 'Submit Form I (NBA for foreign-linked entities) or Form III (SBB intimation for domestic businesses) before any patent or commercial filing.' },
      { step: 'Review Claims with AYUSH Patent Specialist', desc: 'Engage an accredited patent agent familiar with Section 3(p) jurisprudence to draft defensive or process-focused claims.' },
    ],
    classification,
    sources:              [],
    jurisdictionAnalysis: buildJurisdictionAnalysis(''),
    clarifyingQuestions:  [],
    limitations: [
      'This guidance reflects statutory provisions as of 2024–2026. Local State Biodiversity Board rules may enforce localized interpretations.',
      'Prior art clearance cannot guarantee absolute patent grant due to unpublished pending applications.',
      'This output is for research and exploratory planning. Formal legal opinions require an accredited patent attorney.',
    ],
    deliverableContent:   '',
    agents:               [],
    logs:                 [],
    hash:                 '',
    escalationDossier:    null,
    architecture:         {},
    tabTitle:             'COMPLIANCE DOSSIER',
    howGenerated: {
      signals:               classification.matched_signals || [],
      rationale:             classification.rationale || '',
      retrievalSourcesCount: 0,
      statutesScanned:       ['Patents Act 1970 §3(p)', 'Biological Diversity Act 2002', 'FSSAI 2022', 'WIPO GRATK 2024'],
      source:                'client_fallback',
      modelUsed:             'Client-side Rules Engine',
    },
  };
}
