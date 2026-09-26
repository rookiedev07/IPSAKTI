import { searchKnowledgeBase } from './knowledgeBaseData';

const BASE_URL = import.meta.env.VITE_API_URL || '';

// ─── Health Check ────────────────────────────────────────────────────────────
export async function checkBackendHealth() {
  try {
    const res = await fetch(`${BASE_URL}/api/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(60000), // 60s to handle Render free tier cold start
    });
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.info('Backend health check note:', err.message);
  }
  return { status: 'offline', prompts_loaded: 0 };
}

// ─── Orchestrate (primary backend call) ──────────────────────────────────────
/**
 * Calls POST /api/prompt/orchestrate with { prompt, language, jurisdiction }
 * Returns the full backend response object.
 */
export async function orchestratePromptApi(userPrompt, language = 'en', jurisdiction = 'India') {
  const res = await fetch(`${BASE_URL}/api/prompt/orchestrate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: userPrompt, language, jurisdiction }),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.message || `Backend error ${res.status}`);
  }

  return res.json();
}

// ─── Knowledge Base Query (with client-side fallback) ────────────────────────
export async function queryKnowledgeApi(query, topK = 4, domainFilter = null) {
  try {
    const res = await fetch(`${BASE_URL}/api/query-knowledge`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, top_k: topK, domain_filter: domainFilter }),
      signal: AbortSignal.timeout(8000),
    });
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn('Using client-side knowledge base retrieval:', err.message);
  }

  // Fallback to client-side knowledge base retrieval
  const results = searchKnowledgeBase(query, domainFilter);
  return {
    matched: results.length > 0,
    results: results.slice(0, topK),
    query,
    note:
      results.length > 0
        ? null
        : 'No high-confidence match found. Escalate for manual regulatory verification.',
  };
}

// ─── Product Classification (client-side rule evaluation) ────────────────────
export async function classifyProductApi(productDescription) {
  const desc = productDescription.toLowerCase();
  let category = 'proprietary_ayurvedic_medicine';
  let confidence = 'moderate';
  let matched_signals = [];
  let contradiction_flag = null;

  if (/charaka|sushruta|ashtanga hridaya|classical text|as per shastra|shastriya/i.test(desc)) {
    category = 'classical_ayurvedic_medicine';
    matched_signals.push('classical text reference');
    confidence = 'high';
  } else if (
    /standardized extract|purified fraction|phytopharmaceutical|isolated compound/i.test(desc)
  ) {
    category = 'phytopharmaceutical';
    matched_signals.push('standardized bioactive fraction');
    confidence = 'high';
  } else if (
    /supplement|nutraceutical|dietary|health drink|functional food|aahar/i.test(desc)
  ) {
    category = 'ayurveda_aahar_nutraceutical';
    matched_signals.push('food/nutraceutical indicator');
    confidence = 'high';
  } else if (/cream|lotion|shampoo|face wash|skin care|soap|cosmetic/i.test(desc)) {
    category = 'cosmetic';
    matched_signals.push('topical cosmetic formulation');
    confidence = 'high';
  } else if (/novel compound|new molecule|synthesized|never used before/i.test(desc)) {
    category = 'new_non_classical_drug';
    matched_signals.push('novel synthetic/untraditional compound');
    confidence = 'high';
  } else {
    matched_signals.push('ayurvedic composition principles');
  }

  if (category === 'cosmetic' || category === 'ayurveda_aahar_nutraceutical') {
    if (/\b(cures?|treats?|heals?|therapeutic|prevents disease)\b/i.test(desc)) {
      contradiction_flag = `Category '${category}' cannot legally claim disease cure/treatment under Drugs & Cosmetics / FSSAI rules.`;
    }
  }

  return {
    category,
    confidence,
    matched_signals,
    contradiction_flag,
    used_llm_fallback: false,
    rationale: `Classified based on formulation signals: ${matched_signals.join(', ')}.`,
    available_categories: [
      'classical_ayurvedic_medicine',
      'proprietary_ayurvedic_medicine',
      'new_non_classical_drug',
      'phytopharmaceutical',
      'ayurveda_aahar_nutraceutical',
      'cosmetic',
    ],
  };
}

// ─── Legacy helper (kept for any existing callers) ───────────────────────────
export async function matchPromptApi(userPrompt) {
  try {
    const data = await orchestratePromptApi(userPrompt);
    return data;
  } catch (err) {
    console.warn('matchPromptApi error:', err.message);
    return null;
  }
}
