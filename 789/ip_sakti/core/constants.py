"""
Legal and Regulatory Constants, Statutory Registry, and Glossaries
for IP-SAKTI Sahayak (Ayurveda IP & Regulatory Assistant)
"""

from typing import Dict, List, Any
from .schema import LanguageCode, SpecialistRole, ContradictionSeverity

# =====================================================================
# AUTHORITATIVE STATUTORY REGISTRY (India & International)
# =====================================================================
STATUTORY_REGISTRY = {
    # 1. Patents Act 1970 (India)
    "PATENTS_ACT_1970": {
        "full_title": "The Patents Act, 1970 (Act No. 39 of 1970)",
        "jurisdiction": "India",
        "key_sections": {
            "3(p)": {
                "title": "Traditional Knowledge Exclusion",
                "summary": "An invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is NOT patentable.",
                "remedial_guidance": "Must demonstrate synergistic novelty, unique non-obvious isolation process, or novel therapeutic application beyond traditional texts."
            },
            "3(d)": {
                "title": "Mere Discovery of New Form of Known Substance",
                "summary": "Mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy is not patentable.",
                "remedial_guidance": "Must provide comparative therapeutic efficacy data (in vivo/clinical) over standard extract."
            },
            "3(e)": {
                "title": "Mere Admixture Exclusion",
                "summary": "A substance obtained by a mere admixture resulting only in the aggregation of the properties of the components is not patentable.",
                "remedial_guidance": "Must demonstrate super-additive or synergistic chemical/biological interaction with data."
            },
            "10(4)(d)": {
                "title": "Disclosure of Source & Origin of Biological Material",
                "summary": "Mandatory specification of source and geographical origin of biological material used in invention in the patent specification.",
                "remedial_guidance": "Disclose exact Indian or international procurement location."
            }
        }
    },

    # 2. Biological Diversity Act 2002 / BD Amendment Act 2023 (India)
    "BIOLOGICAL_DIVERSITY_ACT": {
        "full_title": "The Biological Diversity Act, 2002 & Amendment Act, 2023",
        "jurisdiction": "India",
        "key_sections": {
            "3": {
                "title": "Access to Biological Resources by Non-Indians / Foreign Entities",
                "summary": "Foreign entities, non-residents, or Indian companies having foreign participation must obtain prior approval of the National Biodiversity Authority (NBA) for obtaining biological resources occurring in India.",
                "remedial_guidance": "Form I application to National Biodiversity Authority (NBA)."
            },
            "4": {
                "title": "Transfer of Research Results",
                "summary": "No person shall transfer results of any research relating to biological resources occurring in India to non-Indians without prior NBA approval.",
                "remedial_guidance": "Form II application to NBA."
            },
            "6(1)": {
                "title": "Prior Approval for Applying for IP Rights on Biological Resources",
                "summary": "No person shall apply for any intellectual property right in or outside India for any invention based on any research or information on a biological resource obtained from India without prior approval of the National Biodiversity Authority (NBA).",
                "remedial_guidance": "Mandatory Form III application to NBA prior to grant of patent."
            },
            "7": {
                "title": "Prior Intimation to State Biodiversity Board (SBB)",
                "summary": "Indian citizens or bodies corporate registered in India seeking biological resources for commercial utilization must give prior intimation to the concerned State Biodiversity Board.",
                "remedial_guidance": "Filing Form I with concerned State Biodiversity Board (SBB)."
            }
        }
    },

    # 3. Drugs and Cosmetics Act, 1940 & Drugs and Cosmetics Rules, 1945
    "DRUGS_AND_COSMETICS_ACT": {
        "full_title": "The Drugs and Cosmetics Act, 1940 & Rules, 1945 (Ayurveda, Siddha, Unani Provisions)",
        "jurisdiction": "India",
        "key_sections": {
            "3(a)": {
                "title": "Ayurvedic, Siddha or Unani (ASU) Drug Definition",
                "summary": "Medicines intended for internal or external use for or in the diagnosis, treatment, mitigation or prevention of disease or disorder in human beings or animals, and manufactured exclusively in accordance with the formulae described in the authoritative books of Ayurvedic, Siddha and Unani Tibb systems of medicine specified in the First Schedule.",
                "remedial_guidance": "Classify as Classical ASU drug if exact formula matches 54 First Schedule texts."
            },
            "3(h)": {
                "title": "Patent or Proprietary ASU Medicine Definition",
                "summary": "A drug which is a formulation containing only ingredients mentioned in the formulae of the First Schedule books but in a different combination or ratio, or manufactured through a distinct proprietary process.",
                "remedial_guidance": "Must comply with Rule 158B evidence requirements."
            },
            "Rule 158B": {
                "title": "Evidence of Safety and Efficacy for ASU Drugs",
                "summary": "Sets out requirements for issue of license to manufacture for sale of Ayurvedic, Siddha, or Unani drugs. Classical formulations require only textual proof from First Schedule books. Proprietary ASU formulations require published literature, proof of safety, or pilot clinical trial data depending on category.",
                "remedial_guidance": "Categorize into Rule 158B(I)(A) classical vs (I)(B) proprietary vs (II) new drug with safety data."
            },
            "Schedule T": {
                "title": "Good Manufacturing Practices (GMP) for ASU Drugs",
                "summary": "Mandatory GMP compliance covering factory premises, hygiene, raw material testing, and batch records for all ASU drug manufacturers.",
                "remedial_guidance": "GMP certification required from State Licensing Authority (SLA)."
            }
        }
    },

    # 4. Traditional Knowledge Digital Library (TKDL)
    "TKDL": {
        "full_title": "Traditional Knowledge Digital Library (CSIR & Ministry of AYUSH)",
        "jurisdiction": "India / International (WIPO Access)",
        "description": "Digitized repository of 400,000+ classical formulations from Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, Sharangadhara Samhita, Bhavaprakasha, Sahasrayogam, etc.",
        "key_doctrine": "Defensive prior-art shield preventing bio-piracy and wrongful grant of patents on pre-existing Ayurvedic knowledge."
    },

    # 5. International IP Treaties & Regimes
    "INTERNATIONAL_FRAMEWORKS": {
        "USPTO": {
            "statute": "35 U.S. Code §§ 101, 102, 103",
            "jurisdiction": "United States (USPTO)",
            "doctrine": "Subject matter eligibility (Alice/Mayo natural products doctrine) + Novelty and Non-obviousness over TKDL prior art."
        },
        "EPO": {
            "statute": "European Patent Convention (EPC) Articles 52, 53, 54, 56",
            "jurisdiction": "Europe (EPO)",
            "doctrine": "Patentability exclusions on therapeutic methods (Art 53(c)) and requirement of inventive step over traditional use."
        },
        "NAGOYA_PROTOCOL": {
            "statute": "Nagoya Protocol on Access to Genetic Resources and the Fair and Equitable Sharing of Benefits",
            "jurisdiction": "International (CBD / WIPO)",
            "doctrine": "Internationally Recognized Certificate of Compliance (IRCC) and PIC/MAT agreements for cross-border genetic/herbal trade."
        }
    }
}

# =====================================================================
# FIRST SCHEDULE 54 AUTHORITATIVE AYURVEDIC BOOKS (Sample Representative)
# =====================================================================
FIRST_SCHEDULE_TEXTS = [
    "Charaka Samhita", "Sushruta Samhita", "Ashtanga Sangraha", "Ashtanga Hridaya",
    "Bhavaprakasha", "Sharangadhara Samhita", "Chakradatta", "Bhaishajya Ratnavali",
    "Rasendra Sara Sangraha", "Rasa Tarangini", "Sahasrayogam", "Ayurvedic Formulary of India (AFI)",
    "Ayurvedic Pharmacopoeia of India (API)", "Yoga Ratnakara", "Gada Nigraha"
]

# =====================================================================
# MULTILINGUAL DOMAIN GLOSSARY (Ayurveda + IP Law)
# =====================================================================
DOMAIN_GLOSSARY: Dict[str, Dict[str, str]] = {
    "Classical Ayurvedic Medicine": {
        "en": "Classical Ayurvedic Medicine",
        "hi": "शास्त्रीय आयुर्वेदिक औषधि",
        "mr": "पारंपारिक / शास्त्रीय आयुर्वेदिक औषध",
        "definition": "Medicine manufactured strictly according to First Schedule authoritative texts."
    },
    "Proprietary Ayurvedic Medicine": {
        "en": "Proprietary Ayurvedic Medicine",
        "hi": "स्वामित्वयुक्त (प्रोप्रायटरी) आयुर्वेदिक औषधि",
        "mr": "मालकी हक्काचे (प्रोप्रायटरी) आयुर्वेदिक औषध",
        "definition": "Formulation using authoritative ingredients but in a novel ratio, form, or process."
    },
    "Phytopharmaceutical Drug": {
        "en": "Phytopharmaceutical Drug",
        "hi": "फाइटोफार्मास्युटिकल औषधि (पादप-औषध)",
        "mr": "फायटोफार्मास्युटिकल औषध (वनस्पतीजन्य औषध)",
        "definition": "Purified standardized fraction with defined markers evaluated via modern clinical trials."
    },
    "Ayurveda Aahar": {
        "en": "Ayurveda Aahar / Nutraceutical",
        "hi": "आयुर्वेद आहार (खाद्य सुरक्षा एवं मानक)",
        "mr": "आयुर्वेद आहार (अन्न सुरक्षा आणि मानके)",
        "definition": "Food prepared according to Ayurveda recipes governed by FSSAI & AYUSH."
    },
    "Prior Art": {
        "en": "Prior Art",
        "hi": "पूर्व कला / पूर्व ज्ञान (प्रायर आर्ट)",
        "mr": "पूर्व कला / पूर्वीची ज्ञात माहिती (प्रायर आर्ट)",
        "definition": "Existing public knowledge before the filing date of a patent application."
    },
    "Section 3(p) Traditional Knowledge": {
        "en": "Section 3(p) Traditional Knowledge Exclusion",
        "hi": "धारा 3(p) - पारंपरिक ज्ञान पेटेंट अपवर्जन",
        "mr": "कलम ३(p) - पारंपारिक ज्ञान पेटंट अपवाद",
        "definition": "Bar under Indian Patents Act 1970 prohibiting patenting of traditional herbal knowledge."
    },
    "National Biodiversity Authority (NBA)": {
        "en": "National Biodiversity Authority (NBA)",
        "hi": "राष्ट्रीय जैव विविधता प्राधिकरण (एनबीए)",
        "mr": "राष्ट्रीय जैवविविधता प्राधिकरण (एनबीए)",
        "definition": "Statutory body in India regulating access to biological resources and IP approvals."
    },
    "Access and Benefit Sharing (ABS)": {
        "en": "Access and Benefit Sharing (ABS)",
        "hi": "पहुंच और लाभ साझाकरण (एबीएस)",
        "mr": "प्रवेश आणि लाभ वाटप (एबीएस)",
        "definition": "Mandatory mechanism to share commercial returns with local indigenous biodiversity custodians."
    },
    "State Biodiversity Board (SBB)": {
        "en": "State Biodiversity Board (SBB)",
        "hi": "राज्य जैव विविधता बोर्ड (एसबीबी)",
        "mr": "राज्य जैवविविधता मंडळ (एसबीबी)",
        "definition": "State-level authority requiring prior intimation for commercial utilization of bio-resources."
    },
    "Rule 158B": {
        "en": "Rule 158B (Drugs & Cosmetics Rules)",
        "hi": "नियम 158B (दवा एवं सौंदर्य प्रसाधन नियमावली)",
        "mr": "नियम १५८B (औषधे व सौंदर्यप्रसाधने नियम)",
        "definition": "Statutory rule specifying safety and efficacy proof requirements for ASU drug licensing."
    },
    "Novelty": {
        "en": "Novelty",
        "hi": "नवीनता (नॉवेल्टी)",
        "mr": "नवीनता (नॉव्हेल्टी)",
        "definition": "Legal requirement that an invention has not been disclosed anywhere in the world."
    },
    "Inventive Step": {
        "en": "Inventive Step / Non-obviousness",
        "hi": "आविष्कारक कदम (इनवेंटिव स्टेप)",
        "mr": "संशोधनात्मक पायरी (इनव्हेन्टिव्ह स्टेप)",
        "definition": "Feature that is not obvious to a person skilled in the art."
    },
    "Traditional Knowledge Digital Library": {
        "en": "Traditional Knowledge Digital Library (TKDL)",
        "hi": "पारंपरिक ज्ञान डिजिटल लाइब्रेरी (टीकेडीएल)",
        "mr": "पारंपारिक ज्ञान डिजिटल लायब्ररी (टीकेडीएल)",
        "definition": "Defensive database protecting traditional Ayurveda formulations from wrongful patents."
    }
}

# =====================================================================
# LOCALIZED STATUTORY DISCLAIMERS
# =====================================================================
STATUTORY_DISCLAIMERS = {
    LanguageCode.EN: (
        "⚖️ STATUTORY LEGAL & REGULATORY DISCLAIMER: This automated report is generated by IP-SAKTI Sahayak "
        "as an AI-assisted analytical advisory tool. It is provided for informational and preliminary compliance "
        "planning purposes only under the Indian Patents Act 1970, Drugs & Cosmetics Act 1940, Biological Diversity "
        "Act 2002/2023, and relevant AYUSH guidelines. This output does not constitute formal legal counsel, statutory "
        "patent opinion, or official licensing authorization. Formal filing of patent applications, NBA Form III approvals, "
        "and manufacturing licenses must be reviewed and certified by a qualified Registered Patent Agent / Legal Practitioner."
    ),
    LanguageCode.HI: (
        "⚖️ वैधानिक कानूनी और विनियामक अस्वीकरण: यह स्वचालित रिपोर्ट आईपी-शक्ति सहायक (IP-SAKTI Sahayak) द्वारा एक "
        "एआई-सहायक विश्लेषणात्मक सलाहकार उपकरण के रूप में तैयार की गई है। यह केवल भारतीय पेटेंट अधिनियम 1970, औषधि एवं प्रसाधन "
        "अधिनियम 1940, जैविक विविधता अधिनियम 2002/2023 और प्रासंगिक आयुष दिशानिर्देशों के तहत सूचनात्मक और प्रारंभिक अनुपालन "
        "योजना के उद्देश्यों के लिए प्रदान की गई है। यह आउटपुट औपचारिक कानूनी सलाह, पेटेंट राय या आधिकारिक लाइसेंसिंग प्राधिकरण "
        "का गठन नहीं करता है। पेटेंट आवेदनों, एनबीए फॉर्म III अनुमोदन और विनिर्माण लाइसेंस के अंतिम दाखिल करने से पहले एक "
        "पंजीकृत पेटेंट एजेंट / कानूनी विशेषज्ञ द्वारा समीक्षा अनिवार्य है।"
    ),
    LanguageCode.MR: (
        "⚖️ कायदेशीर व विनियामक अस्वीकरण: हा स्वयंचलित अहवाल आयपी-शक्ती सहायक (IP-SAKTI Sahayak) द्वारे एक कृत्रिम बुद्धिमत्ता "
        "(AI) विश्लेषणात्मक सल्लागार साधन म्हणून तयार केला गेला आहे. हा अहवाल केवळ भारतीय पेटंट कायदा १९७०, औषधे आणि सौंदर्यप्रसाधने "
        "कायदा १९४०, जैविक विविधता कायदा २००२/२०२३ आणि आयुष मार्गदर्शक तत्त्वांच्या प्राथमिक माहिती व अनुपालनासाठी दिला आहे. "
        "हा आउटपुट अंतिम कायदेशीर सल्ला किंवा अधिकृत परवाना मानला जाऊ नये. पेटंट अर्ज, राष्ट्रीय जैवविविधता प्राधिकरण (NBA) फॉर्म ३ मंजुरी, "
        "किंवा उत्पादन परवाना अंतिम करण्यापूर्वी नोंदणीकृत पेटंट वकील / कायदेशीर तज्ज्ञांचा सल्ला घेणे बंधनकारक आहे."
    )
}
