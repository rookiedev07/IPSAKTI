/**
 * IP-SAKTI Sahayak Interactive Dashboard
 * Client logic for Layers 7, 8 & 9
 */

let currentScenarioId = "classical_chyawanprash";
let currentLanguage = "en";
let isCustomQuery = false;

document.addEventListener("DOMContentLoaded", () => {
  initLanguageSelector();
  loadScenarios();
  initCustomForm();
});

function initLanguageSelector() {
  const pills = document.querySelectorAll(".lang-pill");
  pills.forEach(pill => {
    pill.addEventListener("click", () => {
      pills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentLanguage = pill.getAttribute("data-lang");
      
      document.getElementById("active-lang-tag").textContent = currentLanguage.toUpperCase();

      if (isCustomQuery) {
        executeCustomQuery();
      } else {
        executeScenario(currentScenarioId);
      }
    });
  });
}

async function loadScenarios() {
  const listEl = document.getElementById("scenario-list");
  try {
    const res = await fetch("/api/scenarios");
    const scenarios = await res.json();

    listEl.innerHTML = "";
    scenarios.forEach((sc, idx) => {
      const item = document.createElement("div");
      item.className = `scenario-item ${sc.id === currentScenarioId ? "active" : ""}`;
      item.innerHTML = `
        <div class="scenario-name">${sc.name}</div>
        <div class="scenario-desc">${sc.description}</div>
      `;
      item.addEventListener("click", () => {
        document.querySelectorAll(".scenario-item").forEach(el => el.classList.remove("active"));
        item.classList.add("active");
        currentScenarioId = sc.id;
        isCustomQuery = false;
        executeScenario(sc.id);
      });
      listEl.appendChild(item);
    });

    // Execute first scenario by default
    executeScenario(currentScenarioId);
  } catch (err) {
    listEl.innerHTML = `<div class="error-msg">Error loading scenarios: ${err.message}</div>`;
  }
}

async function executeScenario(scenarioId) {
  try {
    const res = await fetch("/api/process-scenario", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        scenario_id: scenarioId,
        target_language: currentLanguage
      })
    });

    if (!res.ok) throw new Error("Failed to process scenario");
    const data = await res.json();
    renderDashboard(data);
  } catch (err) {
    console.error("Execution error:", err);
  }
}

function initCustomForm() {
  const btn = document.getElementById("btn-run-custom");
  btn.addEventListener("click", () => {
    isCustomQuery = true;
    document.querySelectorAll(".scenario-item").forEach(el => el.classList.remove("active"));
    executeCustomQuery();
  });
}

async function executeCustomQuery() {
  const pName = document.getElementById("custom-product").value.trim();
  const cat = document.getElementById("custom-category").value;
  const ingrRaw = document.getElementById("custom-ingredients").value.trim();
  const query = document.getElementById("custom-query").value.trim();

  const ingredients = ingrRaw ? ingrRaw.split(",").map(i => i.trim()) : [];

  try {
    const res = await fetch("/api/process-custom", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        product_name: pName,
        raw_user_query: query,
        category: cat,
        ingredients: ingredients,
        target_jurisdiction: "India",
        target_language: currentLanguage
      })
    });

    if (!res.ok) throw new Error("Failed to process custom query");
    const data = await res.json();
    renderDashboard(data);
  } catch (err) {
    console.error("Custom query error:", err);
  }
}

function renderDashboard(data) {
  const resp = data.layer_9_response;
  const l7 = data.layer_7_verification;
  const l8 = data.layer_8_confidence;

  // Header & Status
  document.getElementById("product-badge").textContent = resp.product_classification_badge;
  document.getElementById("query-id-tag").textContent = `ID: ${resp.query_id}`;

  const confBadge = document.getElementById("conf-badge");
  confBadge.textContent = `${resp.confidence_level_badge} (${resp.confidence_score_percent}%)`;
  confBadge.className = `badge badge-conf conf-${l8.overall_confidence.toLowerCase()}`;

  // Layer 7 Verification Panel
  const l7Pill = document.getElementById("l7-status-pill");
  l7Pill.textContent = l7.is_passed ? "PASSED" : "FLAGGED / CONTRADICTION";
  l7Pill.className = `pill-status ${l7.is_passed ? "" : "status-flagged"}`;

  const cPct = Math.round((l7.citation_soundness_score || 0.95) * 100);
  const aPct = Math.round((l7.applicability_score ?? 1.0) * 100);
  const concPct = Math.round((l7.conclusion_justification_score ?? 1.0) * 100);
  const gPct = Math.round((l7.overall_groundedness_score || 0.90) * 100);

  document.getElementById("val-citation").textContent = `${cPct}%`;
  document.getElementById("fill-citation").style.width = `${cPct}%`;

  document.getElementById("val-applicability").textContent = `${aPct}%`;
  document.getElementById("fill-applicability").style.width = `${aPct}%`;

  document.getElementById("val-conclusion").textContent = `${concPct}%`;
  document.getElementById("fill-conclusion").style.width = `${concPct}%`;

  document.getElementById("val-groundedness").textContent = `${gPct}%`;
  document.getElementById("fill-groundedness").style.width = `${gPct}%`;

  document.getElementById("l7-summary-text").textContent = l7.verification_summary;

  // Layer 8 Confidence Panel
  document.getElementById("val-conf-percent").textContent = `${resp.confidence_score_percent}%`;
  document.getElementById("circle-score").style.setProperty("--score-pct", `${resp.confidence_score_percent}%`);
  document.getElementById("conf-justification-text").textContent = l8.confidence_justification;

  const l8Pill = document.getElementById("l8-status-pill");
  l8Pill.textContent = l8.escalation_dossier.urgency_level;
  l8Pill.className = `pill-status ${l8.escalation_dossier.urgency_level === "NORMAL" ? "" : "status-immediate"}`;

  const escTag = document.getElementById("escalation-tag");
  if (l8.escalation_dossier.is_escalation_required) {
    escTag.classList.remove("hidden");
    document.getElementById("escalation-tag-msg").textContent = `Escalation: ${l8.escalation_dossier.target_specialist}`;
  } else {
    escTag.classList.add("hidden");
  }

  // Safe Refusal Box
  const refusalBox = document.getElementById("refusal-box");
  if (resp.safe_refusal_notice) {
    refusalBox.classList.remove("hidden");
    document.getElementById("refusal-text").textContent = resp.safe_refusal_notice;
  } else {
    refusalBox.classList.add("hidden");
  }

  // Escalation Dossier Box
  const dossierBox = document.getElementById("escalation-dossier-box");
  if (resp.escalation_notice) {
    dossierBox.classList.remove("hidden");
    document.getElementById("dossier-specialist").textContent = `Target: ${resp.escalation_notice.specialist_role} (${resp.escalation_notice.urgency})`;
    document.getElementById("dossier-brief-text").textContent = resp.escalation_notice.expert_brief;

    const qList = document.getElementById("dossier-questions-list");
    qList.innerHTML = "";
    (resp.escalation_notice.questions_for_counsel || []).forEach(q => {
      const li = document.createElement("li");
      li.textContent = q;
      qList.appendChild(li);
    });
  } else {
    dossierBox.classList.add("hidden");
  }

  // Layer 9 Response Rendering
  document.getElementById("resp-title").textContent = resp.title;
  document.getElementById("resp-exec-summary").textContent = resp.executive_summary;
  document.getElementById("resp-legal-analysis").textContent = resp.detailed_legal_analysis;

  // Action Steps
  const stepsContainer = document.getElementById("resp-action-steps");
  stepsContainer.innerHTML = "";
  resp.key_actionable_steps.forEach((step, idx) => {
    const card = document.createElement("div");
    card.className = "step-card";
    card.innerHTML = `
      <span class="step-num">${idx + 1}</span>
      <span class="step-text">${step}</span>
    `;
    stepsContainer.appendChild(card);
  });

  // Citations Grid
  const citGrid = document.getElementById("resp-citations-grid");
  citGrid.innerHTML = "";
  if (resp.verified_statutory_citations && resp.verified_statutory_citations.length > 0) {
    resp.verified_statutory_citations.forEach(c => {
      const card = document.createElement("div");
      card.className = "citation-card";
      card.innerHTML = `
        <div class="cit-header">
          <span class="cit-act">${c.act}</span>
          <span class="cit-sec">${c.section_or_rule}</span>
        </div>
        <div class="cit-summary">${c.summary}</div>
      `;
      citGrid.appendChild(card);
    });
  } else {
    citGrid.innerHTML = `<div class="info-badge">No direct statutory citations referenced</div>`;
  }

  // Bilingual Glossary Grid
  const glossGrid = document.getElementById("resp-glossary-grid");
  glossGrid.innerHTML = "";
  if (resp.bilingual_glossary && resp.bilingual_glossary.length > 0) {
    resp.bilingual_glossary.forEach(item => {
      const termEl = document.createElement("div");
      termEl.className = "glossary-item";
      termEl.innerHTML = `
        <div class="term-pair">
          <span class="term-en">${item.english_term}</span>
          <span class="term-arrow">⟷</span>
          <span class="term-local">${item.local_term}</span>
        </div>
        <div class="term-def">${item.statutory_context}</div>
      `;
      glossGrid.appendChild(termEl);
    });
  } else {
    glossGrid.innerHTML = `<div class="info-badge">Standard statutory terminology applied</div>`;
  }

  // Localized Disclaimer
  document.getElementById("resp-disclaimer").textContent = resp.statutory_disclaimer;
}
