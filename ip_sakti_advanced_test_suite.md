# IP-SAKTI SAHAYAK — ADVANCED BENCHMARK TEST SUITE

## Benchmark Round 2

**Total Test Cases:** 15  
**India / National:** 5  
**International:** 5  
**Mixed / Multi-Jurisdiction:** 5

---

## Purpose

This benchmark is designed to test jurisdiction detection, domain routing, source relevance, statutory verification, confidence calibration, and especially parallel handling of mixed multi-jurisdiction queries.

# INDIA / NATIONAL QUERIES

## TC-NAT-04 — Classical Formulation Manufacturing Compliance

### User Query

> I want to manufacture a classical Ayurvedic formulation mentioned in the Ayurvedic Formulary of India and sell it across multiple states in India. What manufacturing licence, GMP requirements, labelling requirements, and regulatory approvals do I need?

### Expected Jurisdiction

**India**

### Expected Domains

- AYUSH Manufacturing
- ASU Drug Regulation
- GMP Compliance
- Labelling Compliance

### Expected Primary Regulatory Pathway

**Indian AYUSH / Classical ASU Manufacturing Pathway**

### Expected Authorities / Sources

- Ministry of AYUSH
- Drugs and Cosmetics legal framework
- Relevant ASU manufacturing provisions
- Ayurvedic Formulary of India

### Expected System Behaviour

- Identify classical formulation where facts support it
- Separate manufacturing, GMP and labelling requirements
- Avoid patent/proprietary rules unless triggered

### Structured Test Output

```text
Test ID: TC-NAT-04
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-NAT-05 — Indian Patentability and Traditional Knowledge

### User Query

> I have developed a new extraction process for Neem leaves that produces a higher concentration of active compounds. Can I patent the process in India even though Neem is already known in traditional medicine?

### Expected Jurisdiction

**India**

### Expected Domains

- Patentability
- Traditional Knowledge
- Prior Art

### Expected Primary Regulatory Pathway

**Indian Patentability and Prior-Art Assessment**

### Expected Authorities / Sources

- Indian Patents Act
- Relevant patentability provisions
- IP India
- TKDL where relevant

### Expected System Behaviour

- Distinguish known material from a potentially novel process
- Analyse novelty and inventive step separately
- Do not automatically reject because Neem is traditional knowledge

### Structured Test Output

```text
Test ID: TC-NAT-05
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-NAT-06 — Ayurveda Aahar Advertising Compliance

### User Query

> We are launching an Ayurveda-based food product in India and want to advertise that it improves immunity and prevents viral infections. Can we make these claims on the packaging and in social media advertisements?

### Expected Jurisdiction

**India**

### Expected Domains

- FSSAI
- Ayurveda Aahar
- Advertising Claims
- Food Labelling

### Expected Primary Regulatory Pathway

**FSSAI Ayurveda Aahar and Claims Compliance**

### Expected Authorities / Sources

- FSSAI
- Ayurveda Aahar Regulations
- Relevant labelling and advertising rules

### Expected System Behaviour

- Separate wellness claims from disease prevention/cure claims
- Flag high-risk claims
- Do not treat the product as an AYUSH drug without factual basis

### Structured Test Output

```text
Test ID: TC-NAT-06
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-NAT-07 — Proprietary Ayurvedic Product Classification

### User Query

> Our company has created a new Ayurvedic formulation by combining five herbs in a ratio that is not found in any classical Ayurvedic text. We want to manufacture and sell it in India. How will it be classified and what regulatory pathway applies?

### Expected Jurisdiction

**India**

### Expected Domains

- AYUSH Product Regulation
- Product Classification
- Manufacturing Compliance

### Expected Primary Regulatory Pathway

**Indian Patent/Proprietary ASU Medicine Classification Pathway**

### Expected Authorities / Sources

- Ministry of AYUSH
- Relevant Drugs and Cosmetics Rules
- ASU regulatory sources

### Expected System Behaviour

- Classify classical versus patent/proprietary based on facts
- Select the correct manufacturing pathway
- Avoid unrelated patentability conclusions

### Structured Test Output

```text
Test ID: TC-NAT-07
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-NAT-08 — Geographical Indication and Herbal Product Branding

### User Query

> We want to use the name of a famous Indian geographical region on our herbal product because the herbs traditionally come from that area. Are there any Geographical Indication or intellectual property restrictions we should check before branding the product?

### Expected Jurisdiction

**India**

### Expected Domains

- Geographical Indication
- Trademark
- Branding
- Intellectual Property

### Expected Primary Regulatory Pathway

**Indian GI and Branding Compliance Assessment**

### Expected Authorities / Sources

- GI Registry / IP India
- Geographical Indications legal framework
- Relevant trademark resources

### Expected System Behaviour

- Separate GI issues from trademark issues
- Verify whether the geographical name is actually protected
- Avoid unrelated manufacturing analysis

### Structured Test Output

```text
Test ID: TC-NAT-08
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

# INTERNATIONAL QUERIES

## TC-INT-04 — United States Dietary Supplement Requirements

### User Query

> We want to sell an Ashwagandha capsule in the United States as a dietary supplement. What FDA manufacturing, labelling, and compliance requirements should we consider?

### Expected Jurisdiction

**United States**

### Expected Domains

- US FDA
- Dietary Supplements
- Manufacturing
- Labelling

### Expected Primary Regulatory Pathway

**US Dietary Supplement Compliance Pathway**

### Expected Authorities / Sources

- FDA
- Official US dietary supplement framework
- Relevant CFR provisions
- Dietary supplement cGMP requirements

### Expected System Behaviour

- Distinguish dietary supplements from drugs
- Retrieve supplement-specific sources
- Do not introduce IND requirements unless triggered

### Structured Test Output

```text
Test ID: TC-INT-04
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-INT-05 — European Herbal Medicinal Product Registration

### User Query

> We want to market a traditional herbal medicinal product in France. What European regulatory pathway and traditional-use evidence requirements should we investigate?

### Expected Jurisdiction

**European Union / France**

### Expected Domains

- EU Herbal Medicine
- Traditional Use Registration

### Expected Primary Regulatory Pathway

**EU Traditional Herbal Medicinal Product Registration**

### Expected Authorities / Sources

- EUR-Lex
- European Commission
- EMA where applicable
- Relevant French competent authority

### Expected System Behaviour

- Correctly detect EU/France
- Focus on herbal medicinal product requirements
- Avoid Indian laws unless India is part of the facts

### Structured Test Output

```text
Test ID: TC-INT-05
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-INT-06 — International Trademark Protection

### User Query

> Our Indian Ayurveda brand is already registered in India. We now want trademark protection in Japan, Australia and the United Kingdom. What international trademark filing options should we evaluate?

### Expected Jurisdiction

**International / Target Markets**

### Expected Domains

- International Trademark
- Madrid System
- Trademark Strategy

### Expected Primary Regulatory Pathway

**International Trademark Registration Strategy**

### Expected Authorities / Sources

- WIPO Madrid System
- Official trademark authorities where relevant

### Expected System Behaviour

- Identify Madrid System where applicable
- Avoid PCT unless patents are involved
- Separate target-market trademark requirements

### Structured Test Output

```text
Test ID: TC-INT-06
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-INT-07 — US Botanical Drug IND Pathway

### User Query

> We are developing a standardized herbal extract as a prescription drug in the United States. What FDA pathway should we investigate before starting clinical trials?

### Expected Jurisdiction

**United States**

### Expected Domains

- US FDA Drug Regulation
- IND
- Clinical Development
- Botanical Drugs

### Expected Primary Regulatory Pathway

**US FDA Botanical Drug / IND Pathway**

### Expected Authorities / Sources

- FDA
- 21 CFR Part 312
- FDA botanical drug guidance where relevant

### Expected System Behaviour

- Classify the product as a drug-development scenario
- Retrieve IND-specific sources
- Do not retrieve dietary supplement rules as the primary pathway

### Structured Test Output

```text
Test ID: TC-INT-07
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-INT-08 — PCT International Patent Filing

### User Query

> We have developed a potentially patentable herbal extraction technology and want to seek patent protection in multiple countries. How does the PCT international filing system fit into our strategy?

### Expected Jurisdiction

**International**

### Expected Domains

- International Patent
- PCT
- Patent Filing Strategy

### Expected Primary Regulatory Pathway

**PCT International Patent Filing Pathway**

### Expected Authorities / Sources

- WIPO PCT
- Official PCT resources

### Expected System Behaviour

- Focus on PCT filing strategy
- Avoid Madrid trademark sources
- Avoid ABS sources unless biological-resource facts trigger them

### Structured Test Output

```text
Test ID: TC-INT-08
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

# MIXED / MULTI-JURISDICTION QUERIES

## TC-MIX-07 — India Patent + US FDA Drug Development

### User Query

> We developed a standardized Ashwagandha extract in India. Can we patent the extraction process in India and later develop the product as a prescription botanical drug in the United States?

### Expected Jurisdiction

**India + United States**

### Expected Domains

- Indian Patent
- US FDA Drug Regulation

### Expected Primary Regulatory Pathway

**Parallel India Patent + US FDA Botanical Drug Tracks**

### Expected Authorities / Sources

- Indian patent authorities/law
- FDA
- 21 CFR Part 312 where applicable

### Expected System Behaviour

- Split into India patent track and US regulatory track
- Do not merge patentability with FDA approval
- Verify each jurisdiction independently

### Structured Test Output

```text
Test ID: TC-MIX-07
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-MIX-08 — Indian Classical Product + EU Export

### User Query

> We manufacture a classical Ayurvedic formulation in India and want to export it to Germany. What Indian manufacturing compliance and European import or product-regulatory requirements should we evaluate?

### Expected Jurisdiction

**India + European Union / Germany**

### Expected Domains

- AYUSH Manufacturing
- Export Compliance
- EU Product Regulation

### Expected Primary Regulatory Pathway

**Parallel India Manufacturing + Germany/EU Market Entry Tracks**

### Expected Authorities / Sources

- Indian AYUSH authorities
- EU/German competent sources

### Expected System Behaviour

- Run India and EU tracks separately
- Ask for product classification if required
- Do not assume one jurisdiction's approval automatically satisfies the other

### Structured Test Output

```text
Test ID: TC-MIX-08
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-MIX-09 — Indian Biological Resource + International Patent Strategy

### User Query

> A company wants to use a biological resource sourced from India in a new invention and seek patent protection through the PCT. What Indian biodiversity/ABS issues and international patent filing steps need separate analysis?

### Expected Jurisdiction

**India + International**

### Expected Domains

- ABS/Biodiversity
- Indian Compliance
- International Patent
- PCT

### Expected Primary Regulatory Pathway

**Parallel Indian ABS + PCT Patent Filing Tracks**

### Expected Authorities / Sources

- Current Indian biodiversity framework
- NBA official resources where applicable
- WIPO PCT

### Expected System Behaviour

- Analyse ABS applicability based on facts
- Do not automatically declare a specific NBA form mandatory
- Keep PCT and Indian ABS reasoning separate

### Structured Test Output

```text
Test ID: TC-MIX-09
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-MIX-10 — India Trademark + International Brand Expansion

### User Query

> Our Ayurveda brand is registered in India and we want to protect the same brand internationally while also checking whether our product name conflicts with any protected geographical indication in India. What IP tracks should we follow?

### Expected Jurisdiction

**India + International**

### Expected Domains

- Indian Trademark
- Geographical Indication
- International Trademark

### Expected Primary Regulatory Pathway

**Parallel Indian IP Clearance + International Trademark Strategy**

### Expected Authorities / Sources

- IP India
- GI Registry
- WIPO Madrid System

### Expected System Behaviour

- Create separate GI, Indian trademark and international trademark tracks
- Avoid patent/PCT sources
- Combine only after independent verification

### Structured Test Output

```text
Test ID: TC-MIX-10
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

## TC-MIX-11 — India Ayurveda Aahar + US Dietary Supplement Market

### User Query

> We currently sell an Ayurveda-based wellness food product in India and want to launch a similar Ashwagandha product in the United States as a dietary supplement. What Indian compliance issues and US FDA requirements should be analysed separately?

### Expected Jurisdiction

**India + United States**

### Expected Domains

- FSSAI
- Ayurveda Aahar
- US FDA Dietary Supplement
- Labelling

### Expected Primary Regulatory Pathway

**Parallel Indian Food Compliance + US Dietary Supplement Compliance**

### Expected Authorities / Sources

- FSSAI
- Relevant Indian food regulations
- FDA
- Relevant US dietary supplement regulations

### Expected System Behaviour

- Split Indian and US compliance
- Do not assume product classification transfers automatically
- Separate Indian claims rules from US claims rules

### Structured Test Output

```text
Test ID: TC-MIX-11
Expected Jurisdiction:
Detected Jurisdiction:
Effective Jurisdiction:
Detected Domain(s):
Selected Agent Council:
Primary Regulatory Pathway:
Relevant Sources Retrieved:
Irrelevant Sources Blocked:
Verification Result:
Confidence Score:
Escalation Status:
Final Result: PASS / PARTIAL / FAIL
```

### Pass Criteria

- [ ] Correct jurisdiction detected
- [ ] Correct domain(s) identified
- [ ] Relevant sources retrieved
- [ ] Irrelevant sources blocked
- [ ] Correct agent council selected
- [ ] Verification matches retrieved evidence
- [ ] Confidence reflects evidence completeness

---

# FINAL BENCHMARK SUMMARY

| Category | Total | PASS | PARTIAL | FAIL |
|---|---:|---:|---:|---:|
| India / National | 5 | | | |
| International | 5 | | | |
| Mixed | 5 | | | |
| **TOTAL** | **15** | | | |

## Key Evaluation Rule

For mixed queries, the system should not select only one dominant legal domain. It should split the query into independent jurisdiction/domain tracks, retrieve and verify sources for each track separately, and only then synthesize the final response.