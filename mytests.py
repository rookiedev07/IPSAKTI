"""IP-SAKTI SAHAYAK — Advanced Benchmark Test Suite Generator
Generates: ip_sakti_advanced_test_suite.md

Run:
    python generate_test_suite.py
"""

from pathlib import Path

OUTPUT_FILE = "ip_sakti_advanced_test_suite.md"

tests = {
    "INDIA / NATIONAL QUERIES": [
        {
            "id": "TC-NAT-04",
            "title": "Classical Formulation Manufacturing Compliance",
            "query": "I want to manufacture a classical Ayurvedic formulation mentioned in the Ayurvedic Formulary of India and sell it across multiple states in India. What manufacturing licence, GMP requirements, labelling requirements, and regulatory approvals do I need?",
            "jurisdiction": "India",
            "domains": ["AYUSH Manufacturing", "ASU Drug Regulation", "GMP Compliance", "Labelling Compliance"],
            "pathway": "Indian AYUSH / Classical ASU Manufacturing Pathway",
            "sources": ["Ministry of AYUSH", "Drugs and Cosmetics legal framework", "Relevant ASU manufacturing provisions", "Ayurvedic Formulary of India"],
            "expected": ["Identify classical formulation where facts support it", "Separate manufacturing, GMP and labelling requirements", "Avoid patent/proprietary rules unless triggered"],
        },
        {
            "id": "TC-NAT-05",
            "title": "Indian Patentability and Traditional Knowledge",
            "query": "I have developed a new extraction process for Neem leaves that produces a higher concentration of active compounds. Can I patent the process in India even though Neem is already known in traditional medicine?",
            "jurisdiction": "India",
            "domains": ["Patentability", "Traditional Knowledge", "Prior Art"],
            "pathway": "Indian Patentability and Prior-Art Assessment",
            "sources": ["Indian Patents Act", "Relevant patentability provisions", "IP India", "TKDL where relevant"],
            "expected": ["Distinguish known material from a potentially novel process", "Analyse novelty and inventive step separately", "Do not automatically reject because Neem is traditional knowledge"],
        },
        {
            "id": "TC-NAT-06",
            "title": "Ayurveda Aahar Advertising Compliance",
            "query": "We are launching an Ayurveda-based food product in India and want to advertise that it improves immunity and prevents viral infections. Can we make these claims on the packaging and in social media advertisements?",
            "jurisdiction": "India",
            "domains": ["FSSAI", "Ayurveda Aahar", "Advertising Claims", "Food Labelling"],
            "pathway": "FSSAI Ayurveda Aahar and Claims Compliance",
            "sources": ["FSSAI", "Ayurveda Aahar Regulations", "Relevant labelling and advertising rules"],
            "expected": ["Separate wellness claims from disease prevention/cure claims", "Flag high-risk claims", "Do not treat the product as an AYUSH drug without factual basis"],
        },
        {
            "id": "TC-NAT-07",
            "title": "Proprietary Ayurvedic Product Classification",
            "query": "Our company has created a new Ayurvedic formulation by combining five herbs in a ratio that is not found in any classical Ayurvedic text. We want to manufacture and sell it in India. How will it be classified and what regulatory pathway applies?",
            "jurisdiction": "India",
            "domains": ["AYUSH Product Regulation", "Product Classification", "Manufacturing Compliance"],
            "pathway": "Indian Patent/Proprietary ASU Medicine Classification Pathway",
            "sources": ["Ministry of AYUSH", "Relevant Drugs and Cosmetics Rules", "ASU regulatory sources"],
            "expected": ["Classify classical versus patent/proprietary based on facts", "Select the correct manufacturing pathway", "Avoid unrelated patentability conclusions"],
        },
        {
            "id": "TC-NAT-08",
            "title": "Geographical Indication and Herbal Product Branding",
            "query": "We want to use the name of a famous Indian geographical region on our herbal product because the herbs traditionally come from that area. Are there any Geographical Indication or intellectual property restrictions we should check before branding the product?",
            "jurisdiction": "India",
            "domains": ["Geographical Indication", "Trademark", "Branding", "Intellectual Property"],
            "pathway": "Indian GI and Branding Compliance Assessment",
            "sources": ["GI Registry / IP India", "Geographical Indications legal framework", "Relevant trademark resources"],
            "expected": ["Separate GI issues from trademark issues", "Verify whether the geographical name is actually protected", "Avoid unrelated manufacturing analysis"],
        },
    ],

    "INTERNATIONAL QUERIES": [
        {
            "id": "TC-INT-04",
            "title": "United States Dietary Supplement Requirements",
            "query": "We want to sell an Ashwagandha capsule in the United States as a dietary supplement. What FDA manufacturing, labelling, and compliance requirements should we consider?",
            "jurisdiction": "United States",
            "domains": ["US FDA", "Dietary Supplements", "Manufacturing", "Labelling"],
            "pathway": "US Dietary Supplement Compliance Pathway",
            "sources": ["FDA", "Official US dietary supplement framework", "Relevant CFR provisions", "Dietary supplement cGMP requirements"],
            "expected": ["Distinguish dietary supplements from drugs", "Retrieve supplement-specific sources", "Do not introduce IND requirements unless triggered"],
        },
        {
            "id": "TC-INT-05",
            "title": "European Herbal Medicinal Product Registration",
            "query": "We want to market a traditional herbal medicinal product in France. What European regulatory pathway and traditional-use evidence requirements should we investigate?",
            "jurisdiction": "European Union / France",
            "domains": ["EU Herbal Medicine", "Traditional Use Registration"],
            "pathway": "EU Traditional Herbal Medicinal Product Registration",
            "sources": ["EUR-Lex", "European Commission", "EMA where applicable", "Relevant French competent authority"],
            "expected": ["Correctly detect EU/France", "Focus on herbal medicinal product requirements", "Avoid Indian laws unless India is part of the facts"],
        },
        {
            "id": "TC-INT-06",
            "title": "International Trademark Protection",
            "query": "Our Indian Ayurveda brand is already registered in India. We now want trademark protection in Japan, Australia and the United Kingdom. What international trademark filing options should we evaluate?",
            "jurisdiction": "International / Target Markets",
            "domains": ["International Trademark", "Madrid System", "Trademark Strategy"],
            "pathway": "International Trademark Registration Strategy",
            "sources": ["WIPO Madrid System", "Official trademark authorities where relevant"],
            "expected": ["Identify Madrid System where applicable", "Avoid PCT unless patents are involved", "Separate target-market trademark requirements"],
        },
        {
            "id": "TC-INT-07",
            "title": "US Botanical Drug IND Pathway",
            "query": "We are developing a standardized herbal extract as a prescription drug in the United States. What FDA pathway should we investigate before starting clinical trials?",
            "jurisdiction": "United States",
            "domains": ["US FDA Drug Regulation", "IND", "Clinical Development", "Botanical Drugs"],
            "pathway": "US FDA Botanical Drug / IND Pathway",
            "sources": ["FDA", "21 CFR Part 312", "FDA botanical drug guidance where relevant"],
            "expected": ["Classify the product as a drug-development scenario", "Retrieve IND-specific sources", "Do not retrieve dietary supplement rules as the primary pathway"],
        },
        {
            "id": "TC-INT-08",
            "title": "PCT International Patent Filing",
            "query": "We have developed a potentially patentable herbal extraction technology and want to seek patent protection in multiple countries. How does the PCT international filing system fit into our strategy?",
            "jurisdiction": "International",
            "domains": ["International Patent", "PCT", "Patent Filing Strategy"],
            "pathway": "PCT International Patent Filing Pathway",
            "sources": ["WIPO PCT", "Official PCT resources"],
            "expected": ["Focus on PCT filing strategy", "Avoid Madrid trademark sources", "Avoid ABS sources unless biological-resource facts trigger them"],
        },
    ],

    "MIXED / MULTI-JURISDICTION QUERIES": [
        {
            "id": "TC-MIX-07",
            "title": "India Patent + US FDA Drug Development",
            "query": "We developed a standardized Ashwagandha extract in India. Can we patent the extraction process in India and later develop the product as a prescription botanical drug in the United States?",
            "jurisdiction": "India + United States",
            "domains": ["Indian Patent", "US FDA Drug Regulation"],
            "pathway": "Parallel India Patent + US FDA Botanical Drug Tracks",
            "sources": ["Indian patent authorities/law", "FDA", "21 CFR Part 312 where applicable"],
            "expected": ["Split into India patent track and US regulatory track", "Do not merge patentability with FDA approval", "Verify each jurisdiction independently"],
        },
        {
            "id": "TC-MIX-08",
            "title": "Indian Classical Product + EU Export",
            "query": "We manufacture a classical Ayurvedic formulation in India and want to export it to Germany. What Indian manufacturing compliance and European import or product-regulatory requirements should we evaluate?",
            "jurisdiction": "India + European Union / Germany",
            "domains": ["AYUSH Manufacturing", "Export Compliance", "EU Product Regulation"],
            "pathway": "Parallel India Manufacturing + Germany/EU Market Entry Tracks",
            "sources": ["Indian AYUSH authorities", "EU/German competent sources"],
            "expected": ["Run India and EU tracks separately", "Ask for product classification if required", "Do not assume one jurisdiction's approval automatically satisfies the other"],
        },
        {
            "id": "TC-MIX-09",
            "title": "Indian Biological Resource + International Patent Strategy",
            "query": "A company wants to use a biological resource sourced from India in a new invention and seek patent protection through the PCT. What Indian biodiversity/ABS issues and international patent filing steps need separate analysis?",
            "jurisdiction": "India + International",
            "domains": ["ABS/Biodiversity", "Indian Compliance", "International Patent", "PCT"],
            "pathway": "Parallel Indian ABS + PCT Patent Filing Tracks",
            "sources": ["Current Indian biodiversity framework", "NBA official resources where applicable", "WIPO PCT"],
            "expected": ["Analyse ABS applicability based on facts", "Do not automatically declare a specific NBA form mandatory", "Keep PCT and Indian ABS reasoning separate"],
        },
        {
            "id": "TC-MIX-10",
            "title": "India Trademark + International Brand Expansion",
            "query": "Our Ayurveda brand is registered in India and we want to protect the same brand internationally while also checking whether our product name conflicts with any protected geographical indication in India. What IP tracks should we follow?",
            "jurisdiction": "India + International",
            "domains": ["Indian Trademark", "Geographical Indication", "International Trademark"],
            "pathway": "Parallel Indian IP Clearance + International Trademark Strategy",
            "sources": ["IP India", "GI Registry", "WIPO Madrid System"],
            "expected": ["Create separate GI, Indian trademark and international trademark tracks", "Avoid patent/PCT sources", "Combine only after independent verification"],
        },
        {
            "id": "TC-MIX-11",
            "title": "India Ayurveda Aahar + US Dietary Supplement Market",
            "query": "We currently sell an Ayurveda-based wellness food product in India and want to launch a similar Ashwagandha product in the United States as a dietary supplement. What Indian compliance issues and US FDA requirements should be analysed separately?",
            "jurisdiction": "India + United States",
            "domains": ["FSSAI", "Ayurveda Aahar", "US FDA Dietary Supplement", "Labelling"],
            "pathway": "Parallel Indian Food Compliance + US Dietary Supplement Compliance",
            "sources": ["FSSAI", "Relevant Indian food regulations", "FDA", "Relevant US dietary supplement regulations"],
            "expected": ["Split Indian and US compliance", "Do not assume product classification transfers automatically", "Separate Indian claims rules from US claims rules"],
        },
    ],
}


def bullet(items):
    return "\n".join(f"- {item}" for item in items)


lines = [
    "# IP-SAKTI SAHAYAK — ADVANCED BENCHMARK TEST SUITE",
    "",
    "## Benchmark Round 2",
    "",
    "**Total Test Cases:** 15  ",
    "**India / National:** 5  ",
    "**International:** 5  ",
    "**Mixed / Multi-Jurisdiction:** 5",
    "",
    "---",
    "",
    "## Purpose",
    "",
    "This benchmark is designed to test jurisdiction detection, domain routing, source relevance, statutory verification, confidence calibration, and especially parallel handling of mixed multi-jurisdiction queries.",
    "",
]

for section, section_tests in tests.items():
    lines += [f"# {section}", ""]
    for t in section_tests:
        lines += [
            f"## {t['id']} — {t['title']}",
            "",
            "### User Query",
            "",
            f"> {t['query']}",
            "",
            "### Expected Jurisdiction",
            "",
            f"**{t['jurisdiction']}**",
            "",
            "### Expected Domains",
            "",
            bullet(t["domains"]),
            "",
            "### Expected Primary Regulatory Pathway",
            "",
            f"**{t['pathway']}**",
            "",
            "### Expected Authorities / Sources",
            "",
            bullet(t["sources"]),
            "",
            "### Expected System Behaviour",
            "",
            bullet(t["expected"]),
            "",
            "### Structured Test Output",
            "",
            "```text",
            f"Test ID: {t['id']}",
            "Expected Jurisdiction:",
            "Detected Jurisdiction:",
            "Effective Jurisdiction:",
            "Detected Domain(s):",
            "Selected Agent Council:",
            "Primary Regulatory Pathway:",
            "Relevant Sources Retrieved:",
            "Irrelevant Sources Blocked:",
            "Verification Result:",
            "Confidence Score:",
            "Escalation Status:",
            "Final Result: PASS / PARTIAL / FAIL",
            "```",
            "",
            "### Pass Criteria",
            "",
            "- [ ] Correct jurisdiction detected",
            "- [ ] Correct domain(s) identified",
            "- [ ] Relevant sources retrieved",
            "- [ ] Irrelevant sources blocked",
            "- [ ] Correct agent council selected",
            "- [ ] Verification matches retrieved evidence",
            "- [ ] Confidence reflects evidence completeness",
            "",
            "---",
            "",
        ]

lines += [
    "# FINAL BENCHMARK SUMMARY",
    "",
    "| Category | Total | PASS | PARTIAL | FAIL |",
    "|---|---:|---:|---:|---:|",
    "| India / National | 5 | | | |",
    "| International | 5 | | | |",
    "| Mixed | 5 | | | |",
    "| **TOTAL** | **15** | | | |",
    "",
    "## Key Evaluation Rule",
    "",
    "For mixed queries, the system should not select only one dominant legal domain. It should split the query into independent jurisdiction/domain tracks, retrieve and verify sources for each track separately, and only then synthesize the final response.",
]

Path(OUTPUT_FILE).write_text("\n".join(lines), encoding="utf-8")

print(f"Successfully created: {OUTPUT_FILE}")
print(f"Total test cases: 15")
print("Categories: 5 India + 5 International + 5 Mixed")