# 🌿 IP-SAKTI Sahayak (PS #29)
### House of Cards Multi-Agent Framework — Layers 7, 8, and 9

An AI-driven statutory verification, confidence assessment, human escalation, and multilingual localization engine for Ayurveda Intellectual Property & Regulatory Compliance.

---

## 🏛️ System Architecture

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

## 📦 What Was Built

### 1. ✅ Layer 7: Verification Agent (`ip_sakti/layer_7_verification/`)
* **Claim Extraction & Proposition Mapping (`claim_extractor.py`)**: Normalizes free-form synthesis into verifiable legal claims.
* **Statutory Registry Checker (`citation_checker.py`)**: Cross-checks cited sections against the Patents Act 1970 (Sec 3(p), 3(d), 3(e)), Biological Diversity Act 2002/2023 (Sec 3, 4, 6(1), 7), Drugs & Cosmetics Rules 1945 (Rule 158B), and TKDL.
* **Contradiction Detection Engine (`contradiction_engine.py`)**: Detects critical legal conflicts (e.g. attempting to patent classical ASU formulations without novelty, missing NBA approvals, unlicensed drug claims).
* **Jurisdiction Coherence (`jurisdiction_verifier.py`)**: Ensures domestic vs foreign IP filing doctrines (USPTO 35 USC 101 vs Indian Patents Act) are not conflated.
* **Hallucination Guard (`hallucination_guard.py`)**: Computes claim-level groundedness against retrieved evidence passages.

### 2. 🎯 Layer 8: Confidence & Human Escalation (`ip_sakti/layer_8_confidence/`)
* **Confidence Scoring Engine (`confidence_engine.py`)**: Computes weighted scores:
  $$\text{Score} = (0.35 \times \text{Groundedness}) + (0.25 \times \text{Citations}) + (0.20 \times \text{Jurisdiction}) + (0.20 \times [1 - \text{Penalty}])$$
* **Safe Refusal & Abstention Handler (`refusal_handler.py`)**: Formulates strict statutory refusals when advice would result in legal/regulatory violations.
* **Escalation Router (`escalation_router.py`)**: Identifies when human review is required and assigns the right domain expert (*Patent Attorney*, *AYUSH Regulatory Consultant*, *NBA ABS Officer*).
* **Legal Escalation Dossier Generator (`escalation_dossier.py`)**: Assembles a brief with risk summary, flags, and targeted questions for legal counsel.

### 3. 🌐 Layer 9: Multilingual Layer (`ip_sakti/layer_9_multilingual/`)
* **Language Detector (`language_detector.py`)**: Detects English, Hindi (हिन्दी), and Marathi (मराठी).
* **Terminology Preserver (`terminology_preserver.py`)**: Dual-language glossaries preserving exact terms (e.g., *शास्त्रीय आयुर्वेदिक औषधि / पारंपारिक आयुर्वेदिक औषध*, *पूर्व कला*, *प्रवेश आणि लाभ वाटप*).
* **Domain-Specific Translator (`translator.py`)**: Localizes legal analyses, badges, and action steps into high-register Hindi and Marathi.
* **Localized Formatter (`localized_formatter.py`)**: Outputs complete responses with bilingual glossaries and localized statutory disclaimers.

---

## 🚀 Quickstart & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Interactive CLI
```bash
python main.py
```
*Select from benchmark scenarios or test custom Ayurveda products in English, Hindi, or Marathi.*

### 3. Launch Web Dashboard & REST API
```bash
python run_server.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser to view the interactive dashboard.

### 4. Run Test Suite
```bash
python -m pytest tests/ -v
```

---

## 📊 Benchmark Scenarios Tested

| Scenario ID | Product Case | Expected Behavior |
|---|---|---|
| `classical_chyawanprash` | Classical Chyawanprash formulation | **High Confidence (100%)**, Sec 3(p) non-patentability bar + Rule 158B(I)(A) classical proof confirmed. |
| `novel_phytopharmaceutical` | Standardized Giloy cordifolioside extract | **Medium/High Confidence**, Sec 3(d)/3(e) novelty check + NBA Sec 6(1) approval + Advisory Escalation. |
| `unsubstantiated_haldi_patent` | Turmeric-pepper simple mix claimed as novel | **Safe Refusal / Low Confidence**, Layer 7 flags critical contradiction, halts execution & outputs safe harbor. |
| `international_pct_export` | Ashwagandha nano-complex for US/EPO | **High Groundedness**, Multi-jurisdictional compliance with NBA Form III foreign filing clearance. |

---

## 📂 Project Structure

```
House of Cards/5 and 6/
├── ip_sakti/
│   ├── core/
│   │   ├── schema.py              # Pydantic & Data Models
│   │   ├── constants.py           # Statutory Registry & Glossaries
│   │   └── mock_upstream.py       # Upstream Simulator (Layers 1-6)
│   ├── layer_7_verification/      # Layer 7: Verification Agent
│   │   ├── claim_extractor.py
│   │   ├── citation_checker.py
│   │   ├── contradiction_engine.py
│   │   ├── jurisdiction_verifier.py
│   │   ├── hallucination_guard.py
│   │   └── verification_agent.py
│   ├── layer_8_confidence/        # Layer 8: Confidence & Escalation
│   │   ├── confidence_engine.py
│   │   ├── escalation_router.py
│   │   ├── escalation_dossier.py
│   │   └── refusal_handler.py
│   ├── layer_9_multilingual/      # Layer 9: Multilingual Engine
│   │   ├── language_detector.py
│   │   ├── terminology_preserver.py
│   │   ├── translator.py
│   │   └── localized_formatter.py
│   ├── pipeline.py                # Unified Pipeline Orchestrator
│   ├── api.py                     # FastAPI REST Endpoints
│   └── cli.py                     # Rich Terminal Interface
├── web/                           # Modern Interactive Web Dashboard
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/                         # Full Pytest Test Suite
│   ├── test_layer_7_verification.py
│   ├── test_layer_8_confidence.py
│   ├── test_layer_9_multilingual.py
│   └── test_full_pipeline.py
├── main.py                        # CLI entrypoint
├── run_server.py                  # Web server entrypoint
├── requirements.txt               # Dependencies
└── README.md                      # Documentation
```
