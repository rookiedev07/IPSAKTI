"""
Command-Line Interface (CLI) for IP-SAKTI Sahayak
Demonstrating Layers 7, 8, and 9 with real-time statutory verification,
confidence calibration, escalation routing, and multilingual output.
"""

import sys
import json
from typing import Optional
from .core.schema import LanguageCode, UpstreamAgentOutput, AyurvedaCategory, Jurisdiction
from .core.mock_upstream import list_mock_scenarios, get_mock_scenario
from .pipeline import IPSaktiPipeline


def run_cli():
    print("=" * 80)
    print("🌿 IP-SAKTI SAHAYAK (House of Cards Multi-Agent Framework)")
    print("   Layer 7: Verification Agent | Layer 8: Confidence & Escalation | Layer 9: Multilingual")
    print("=" * 80)

    pipeline = IPSaktiPipeline()

    while True:
        print("\nAvailable Benchmark Scenarios (simulating upstream Layers 1-6):")
        scenarios = list_mock_scenarios()
        for idx, sc in enumerate(scenarios, 1):
            print(f"  [{idx}] {sc['name']}")
            print(f"      ↳ {sc['description']}")
        print("  [5] Enter Custom Ayurveda IP Query")
        print("  [0] Exit")

        choice = input("\nSelect an option [0-5]: ").strip()

        if choice == "0":
            print("\nExiting IP-SAKTI Sahayak. Dhanyavad / Thank you!")
            break

        upstream_data: Optional[UpstreamAgentOutput] = None

        if choice in ["1", "2", "3", "4"]:
            sc_id = scenarios[int(choice) - 1]["id"]
            upstream_data = get_mock_scenario(sc_id)
        elif choice == "5":
            upstream_data = prompt_custom_query()
        else:
            print("Invalid option. Please choose between 0 and 5.")
            continue

        # Language selection
        print("\nSelect Output Language:")
        print("  [1] English (Default)")
        print("  [2] Hindi (हिन्दी)")
        print("  [3] Marathi (मराठी)")
        lang_choice = input("Select Language [1-3] (Default: 1): ").strip()

        lang_map = {"1": LanguageCode.EN, "2": LanguageCode.HI, "3": LanguageCode.MR}
        selected_lang = lang_map.get(lang_choice, LanguageCode.EN)

        print("\n" + "⏳" * 3 + " Executing Layer 7 -> Layer 8 -> Layer 9 Pipeline..." + "⏳" * 3)
        result = pipeline.process(upstream_data, target_language=selected_lang)

        render_terminal_output(result)


def prompt_custom_query() -> UpstreamAgentOutput:
    print("\n--- Enter Custom Ayurveda Product Details ---")
    p_name = input("Product / Formula Name: ").strip() or "Custom Herbal Compound"
    query = input("User Question (e.g. Can I patent this formulation?): ").strip() or "Can I patent this formulation in India?"
    ingr_raw = input("Key Herbal Ingredients (comma separated): ").strip() or "Tinospora cordifolia, Curcuma longa"
    ingredients = [i.strip() for i in ingr_raw.split(",") if i.strip()]

    print("\nSelect Ayurveda Category:")
    print("  [1] Classical Ayurvedic Medicine")
    print("  [2] Proprietary Ayurvedic Medicine")
    print("  [3] Phytopharmaceutical Drug")
    print("  [4] Ayurveda Aahar / Nutraceutical")
    cat_ch = input("Category [1-4] (Default: 1): ").strip()
    cat_map = {
        "1": AyurvedaCategory.CLASSICAL,
        "2": AyurvedaCategory.PROPRIETARY,
        "3": AyurvedaCategory.PHYTOPHARMACEUTICAL,
        "4": AyurvedaCategory.AYURVEDA_AAHAR
    }
    cat = cat_map.get(cat_ch, AyurvedaCategory.CLASSICAL)

    # Basic synthetic draft
    draft = (
        f"### IP Advisory for {p_name}\n"
        f"1. Classification: Analyzed under category '{cat.value}'.\n"
        f"2. Patentability: Evaluation of novelty and Section 3(p) Traditional Knowledge constraints under Patents Act 1970.\n"
        f"3. Compliance: Ayurvedic manufacturing licensing under Drugs & Cosmetics Rule 158B and Biodiversity compliance."
    )

    return UpstreamAgentOutput(
        query_id="QRY-CUSTOM-999",
        raw_user_query=query,
        product_name=p_name,
        detected_category=cat,
        botanical_and_herbal_ingredients=ingredients,
        proposed_use_or_claim="Therapeutic health formulation",
        target_jurisdiction=Jurisdiction.INDIA,
        synthesis_draft_text=draft,
        extracted_claims=[],
        citations_referenced=[],
        retrieved_evidence=[]
    )


def render_terminal_output(result):
    resp = result.layer_9_response
    l7 = result.layer_7_verification
    l8 = result.layer_8_confidence

    print("\n" + "=" * 80)
    print(f"📄 {resp.title}")
    print("=" * 80)
    print(f"🏷️  Category:   {resp.product_classification_badge}")
    print(f"🎯  Confidence: {resp.confidence_level_badge} [{resp.confidence_score_percent}%]")
    print(f"🌐  Language:   {resp.target_language.value.upper()}")
    print("-" * 80)

    # Layer 7 verification summary
    print("\n[LAYER 7: VERIFICATION AUDIT]")
    print(f"Status:             {'✅ PASSED' if l7.is_passed else '❌ FLAGGED / FAILED'}")
    print(f"Groundedness:       {int(l7.overall_groundedness_score * 100)}%")
    print(f"Citation Soundness: {int(l7.citation_soundness_score * 100)}%")
    print(f"Jurisdiction Coherence: {int(l7.jurisdiction_coherence_score * 100)}%")
    if l7.contradictions:
        print("\n⚠️  Detected Contradictions:")
        for c in l7.contradictions:
            print(f"   • [{c.severity.value}] {c.conflict_type}: {c.description}")

    # Layer 8 Safe Refusal or Escalation
    if resp.safe_refusal_notice:
        print("\n" + "!" * 80)
        print(resp.safe_refusal_notice)
        print("!" * 80)

    if resp.escalation_notice:
        print("\n[LAYER 8: HUMAN SPECIALIST ESCALATION DOSSIER]")
        print(f"Target Specialist:  {resp.escalation_notice['specialist_role']}")
        print(f"Urgency:            {resp.escalation_notice['urgency']}")
        print("Questions for Legal Counsel:")
        for q in resp.escalation_notice['questions_for_counsel']:
            print(f"   ❓ {q}")

    # Main Analysis
    print("\n[DETAILED LEGAL ANALYSIS]")
    print(resp.detailed_legal_analysis)

    # Actionable Steps
    print("\n[KEY ACTIONABLE STEPS]")
    for idx, step in enumerate(resp.key_actionable_steps, 1):
        print(f"  {idx}. {step}")

    # Citations
    if resp.verified_statutory_citations:
        print("\n[VERIFIED STATUTORY CITATIONS]")
        for cit in resp.verified_statutory_citations:
            print(f"  📌 [{cit['status']}] {cit['act']} - {cit['section_or_rule']}: {cit['summary']}")

    # Bilingual Glossary
    if resp.bilingual_glossary:
        print("\n[BILINGUAL DOMAIN GLOSSARY]")
        for term in resp.bilingual_glossary:
            print(f"  📖 {term.english_term} ⟷ {term.local_term} ({term.statutory_context})")

    # Statutory Disclaimer
    print("\n" + "-" * 80)
    print(resp.statutory_disclaimer)
    print("=" * 80 + "\n")
