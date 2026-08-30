# Walkthrough: PS #29 IP-SAKTI Sahayak (Layers 7, 8, 9)

We have built a modular, production-ready, and fully tested implementation of **Layer 7 (Verification Agent)**, **Layer 8 (Confidence & Human Escalation)**, and **Layer 9 (Multilingual Layer)** for **PS #29 IP-SAKTI Sahayak** (Ayurveda IP & Regulatory Assistant based on the House of Cards multi-agent framework).

---

## 🏛️ Architecture Overview

```text
                    USER
                      ↓
              ┌───────────────┐
              │ HOUSE OF CARDS │
              └───────┬───────┘
                      ↓
             BEST PROMPT MATCH
                      ↓
                    JOKER
                      ↓
          ┌───────────┼───────────┐
          ↓           ↓           ↓
    CLASSIFICATION    IP/RAG    PRIOR-ART
        AGENT          AGENT       AGENT
          │           │           │
          └───────────┼───────────┘
                      ↓
               JURISDICTION
                      ↓
        =================================
        👉 BUILT IN THIS REPOSITORY:
        =================================
                      ↓
         ✅ LAYER 7: VERIFICATION AGENT
          (Groundedness • Statutes • Contradictions)
                      ↓
         🎯 LAYER 8: CONFIDENCE & ESCALATION
          (High/Med/Low • Safe Refusal • Attorney Dossier)
                      ↓
         🌐 LAYER 9: MULTILINGUAL LAYER
          (EN • HI • MR • Dual Domain Glossaries)
                      ↓
                 FINAL ANSWER
```

---

## 🛠️ Components Created

### 1. Core Schema, Statutory Registry & Upstream Simulator (`ip_sakti/core/`)
- [`schema.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/core/schema.py): Type-safe Pydantic models for claims, citations, verification findings, confidence scores, escalation dossiers, and multilingual outputs.
- [`constants.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/core/constants.py): Complete statutory registry containing:
  - **Patents Act 1970**: Section 3(p) (TKDL bar), Section 3(d) (enhanced efficacy), Section 3(e) (admixture bar), Section 10 (biological source disclosure).
  - **Biological Diversity Act 2002/2023**: Section 3, 4, 6(1) (NBA IPR approval), Section 7 (SBB intimation).
  - **Drugs & Cosmetics Act 1940 & Rules 1945**: Rule 158B, First Schedule 54 classical texts, Schedule T GMP.
  - **TKDL Registry & International Equivalents**: USPTO 35 USC 101/102/103, EPO EPC Art 52/53.
  - **Statutory Disclaimers**: In English, Hindi, and Marathi.
- [`mock_upstream.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/core/mock_upstream.py): Upstream simulator representing Layers 1–6 across 4 realistic Ayurveda scenarios:
  1. *Classical Chyawanprash Formulation*
  2. *Novel Phytopharmaceutical Giloy Fraction*
  3. *Unsubstantiated Turmeric-Pepper Patent Claim*
  4. *International PCT Export Filing (India -> US/EPO)*

---

### 2. Layer 7: Verification Agent (`ip_sakti/layer_7_verification/`)
- [`claim_extractor.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_7_verification/claim_extractor.py): Normalizes free-form synthesis into discrete propositions.
- [`citation_checker.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_7_verification/citation_checker.py): Verifies validity of cited statutory sections.
- [`contradiction_engine.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_7_verification/contradiction_engine.py): Catches critical statutory conflicts (e.g., Classical ASU claimed as patentable, bio-resources used without NBA Section 6 approval).
- [`jurisdiction_verifier.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_7_verification/jurisdiction_verifier.py): Prevents cross-jurisdiction confusion.
- [`hallucination_guard.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_7_verification/hallucination_guard.py): Computes groundedness against retrieved evidence.
- [`verification_agent.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_7_verification/verification_agent.py): Layer 7 orchestrator returning structured `VerificationResult`.

---

### 3. Layer 8: Confidence & Human Escalation (`ip_sakti/layer_8_confidence/`)
- [`confidence_engine.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_8_confidence/confidence_engine.py): Computes weighted confidence:
  $$\text{Score} = (0.35 \times \text{Groundedness}) + (0.25 \times \text{Citations}) + (0.20 \times \text{Jurisdiction}) + (0.20 \times [1 - \text{Penalty}])$$
- [`refusal_handler.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_8_confidence/refusal_handler.py): Generates safe statutory refusals with recommended safe harbors.
- [`escalation_router.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_8_confidence/escalation_router.py): Routes high-risk/ambiguous cases to designated human specialists (*Patent Attorney*, *AYUSH Regulatory Consultant*, *NBA ABS Officer*).
- [`escalation_dossier.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_8_confidence/escalation_dossier.py): Assembles a briefing with risk flags and targeted questions for counsel.

---

### 4. Layer 9: Multilingual Layer (`ip_sakti/layer_9_multilingual/`)
- [`language_detector.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_9_multilingual/language_detector.py): Automatically detects English, Hindi (हिन्दी), and Marathi (मराठी).
- [`terminology_preserver.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_9_multilingual/terminology_preserver.py): Dual-language glossaries preserving exact terms (*शास्त्रीय आयुर्वेदिक औषधि*, *पूर्व कला*, *प्रवेश आणि लाभ वाटप*).
- [`translator.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_9_multilingual/translator.py): Translates legal analysis, badges, and action steps into high-register Hindi and Marathi.
- [`localized_formatter.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/layer_9_multilingual/localized_formatter.py): Renders the final output with bilingual glossaries and localized statutory disclaimers.

---

### 5. Orchestration, Web UI, API & CLI
- [`pipeline.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/pipeline.py): End-to-end pipeline linking Layers 7 -> 8 -> 9.
- [`main.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/main.py) & [`cli.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/cli.py): Rich interactive CLI.
- [`run_server.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/run_server.py) & [`api.py`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/ip_sakti/api.py): FastAPI server with REST endpoints.
- [`web/`](file:///c:/Users/vishal/Desktop/House%20of%20Cards/5%20and%206/web/index.html): Interactive Web Dashboard with visual architecture flow, live language switching (EN/HI/MR), verification meters, confidence gauges, and escalation dossiers.

---

## 🧪 Verification & Test Results

The test suite executed with **100% pass rate** across all 12 unit and integration test cases:

```bash
$ python -m pytest tests/ -v
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-9.1.1, pluggy-1.6.0
collected 12 items

tests/test_full_pipeline.py::test_full_pipeline_all_scenarios PASSED     [  8%]
tests/test_full_pipeline.py::test_full_pipeline_refusal_behaviour PASSED [ 16%]
tests/test_layer_7_verification.py::test_verification_agent_classical_success PASSED [ 25%]
tests/test_layer_7_verification.py::test_verification_agent_detects_critical_flaw PASSED [ 33%]
tests/test_layer_7_verification.py::test_citation_checker_authenticity PASSED [ 41%]
tests/test_layer_7_verification.py::test_contradiction_engine_direct PASSED [ 50%]
tests/test_layer_8_confidence.py::test_confidence_engine_high_score PASSED [ 58%]
tests/test_layer_8_confidence.py::test_confidence_engine_refusal_on_critical_contra PASSED [ 66%]
tests/test_layer_8_confidence.py::test_confidence_engine_phytopharmaceutical_escalation PASSED [ 75%]
tests/test_layer_9_multilingual.py::test_language_detector PASSED        [ 83%]
tests/test_layer_9_multilingual.py::test_localized_formatter_hindi PASSED [ 91%]
tests/test_layer_9_multilingual.py::test_localized_formatter_marathi PASSED [100%]

============================= 12 passed in 0.24s ==============================
```

---

## 🚀 How to Run

1. **Interactive CLI**:
   ```bash
   python main.py
   ```
2. **Web Dashboard**:
   ```bash
   python run_server.py
   ```
   *Open [http://localhost:8000](http://localhost:8000) in your browser.*
