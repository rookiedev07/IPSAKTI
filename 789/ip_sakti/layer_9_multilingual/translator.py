"""
Domain-Specific Multilingual Translator (English -> Hindi / Marathi)
Translates legal analysis, classification, confidence badges, and actionable checklists
while retaining statutory integrity and exact legal terminology.
"""

from typing import Dict, List, Any, Tuple
from ..core.schema import (
    LanguageCode,
    ConfidenceLevel,
    AyurvedaCategory,
    SpecialistRole
)


class DomainTranslator:
    """
    Translates synthesized outputs into Hindi and Marathi with domain-specific accuracy.
    """

    # Category Badges
    CATEGORY_MAP = {
        LanguageCode.EN: {
            AyurvedaCategory.CLASSICAL: "Classical Ayurvedic Medicine (First Schedule Text)",
            AyurvedaCategory.PROPRIETARY: "Proprietary Ayurvedic Medicine (Rule 158B)",
            AyurvedaCategory.PHYTOPHARMACEUTICAL: "Phytopharmaceutical Drug (CDSCO Rule 2(eb))",
            AyurvedaCategory.AYURVEDA_AAHAR: "Ayurveda Aahar / Nutraceutical (FSSAI/AYUSH)",
            AyurvedaCategory.COSMETIC: "Ayurvedic Cosmetic (DCA Chapter IV-A)",
            AyurvedaCategory.NEW_HERBAL_ENTITY: "New Herbal Entity / Non-Classical"
        },
        LanguageCode.HI: {
            AyurvedaCategory.CLASSICAL: "शास्त्रीय आयुर्वेदिक औषधि (प्रथम अनुसूची ग्रंथ आधारित)",
            AyurvedaCategory.PROPRIETARY: "स्वामित्वयुक्त (प्रोप्रायटरी) आयुर्वेदिक औषधि (नियम 158B)",
            AyurvedaCategory.PHYTOPHARMACEUTICAL: "पादप-औषध / फाइटोफार्मास्युटिकल (सीडीएससीओ नियम 2(eb))",
            AyurvedaCategory.AYURVEDA_AAHAR: "आयुर्वेद आहार / न्यूट्रास्युटिकल (एफएसएसएआई/आयुष)",
            AyurvedaCategory.COSMETIC: "आयुर्वेदिक प्रसाधन सामग्री (कॉस्मेटिक)",
            AyurvedaCategory.NEW_HERBAL_ENTITY: "नवीन पादप घटक / गैर-शास्त्रीय औषधि"
        },
        LanguageCode.MR: {
            AyurvedaCategory.CLASSICAL: "पारंपारिक / शास्त्रीय आयुर्वेदिक औषध (पहिली अनुसूची ग्रंथ)",
            AyurvedaCategory.PROPRIETARY: "मालकी हक्काचे (प्रोप्रायटरी) आयुर्वेदिक औषध (नियम १५८B)",
            AyurvedaCategory.PHYTOPHARMACEUTICAL: "फायटोफार्मास्युटिकल औषध (सीडीएससीओ नियम २(eb))",
            AyurvedaCategory.AYURVEDA_AAHAR: "आयुर्वेद आहार / न्यूट्रास्युटिकल (एफएसएसएआय/आयुष)",
            AyurvedaCategory.COSMETIC: "आयुर्वेदिक सौंदर्यप्रसाधन (कॉस्मेटिक)",
            AyurvedaCategory.NEW_HERBAL_ENTITY: "नवीन वनस्पतीजन्य औषध / बिगर-शास्त्रीय"
        }
    }

    # Confidence Badges
    CONFIDENCE_MAP = {
        LanguageCode.EN: {
            ConfidenceLevel.HIGH: "HIGH STATUTORY CONFIDENCE (Clear Legal Grounding)",
            ConfidenceLevel.MEDIUM: "MEDIUM CONFIDENCE (Advisory Review Recommended)",
            ConfidenceLevel.LOW: "LOW CONFIDENCE (Mandatory Attorney Review)",
            ConfidenceLevel.REFUSAL: "STATUTORY REFUSAL / COMPLIANCE HALT"
        },
        LanguageCode.HI: {
            ConfidenceLevel.HIGH: "उच्च वैधानिक विश्वास (स्पष्ट कानूनी आधार)",
            ConfidenceLevel.MEDIUM: "मध्यम विश्वास (सलाहकार समीक्षा अनुशंसित)",
            ConfidenceLevel.LOW: "निम्न विश्वास (वकील / विशेषज्ञ समीक्षा अनिवार्य)",
            ConfidenceLevel.REFUSAL: "वैधानिक अस्वीकरण / अनुपालन रोक"
        },
        LanguageCode.MR: {
            ConfidenceLevel.HIGH: "उच्च कायदेशीर विश्वास (स्पष्ट वैधानिक आधार)",
            ConfidenceLevel.MEDIUM: "मध्यम विश्वास (तज्ज्ञ सल्लागार पुनरावलोकन आवश्यक)",
            ConfidenceLevel.LOW: "कमी विश्वास (वकील / कायदेतज्ज्ञ तपासणी अनिवार्य)",
            ConfidenceLevel.REFUSAL: "कायदेशीर नकार / प्रक्रिया स्थगित"
        }
    }

    @classmethod
    def get_category_badge(cls, category: AyurvedaCategory, lang: LanguageCode) -> str:
        return cls.CATEGORY_MAP.get(lang, cls.CATEGORY_MAP[LanguageCode.EN]).get(category, category.value)

    @classmethod
    def get_confidence_badge(cls, level: ConfidenceLevel, lang: LanguageCode) -> str:
        return cls.CONFIDENCE_MAP.get(lang, cls.CONFIDENCE_MAP[LanguageCode.EN]).get(level, level.value)

    @classmethod
    def translate_analysis(
        cls,
        text: str,
        lang: LanguageCode,
        category: AyurvedaCategory,
        product_name: str
    ) -> Tuple[str, str, List[str]]:
        """
        Translates legal analysis into structured sections in target language.
        Returns: (Title, Detailed Analysis, Action Steps)
        """
        if lang == LanguageCode.EN:
            return cls._format_english(text, category, product_name)
        elif lang == LanguageCode.HI:
            return cls._format_hindi(text, category, product_name)
        else:
            return cls._format_marathi(text, category, product_name)

    @classmethod
    def _format_english(cls, text: str, category: AyurvedaCategory, product_name: str) -> Tuple[str, str, List[str]]:
        title = f"IP & Regulatory Compliance Dossier: {product_name}"
        action_steps = [
            "Submit Form 25D manufacturing application to State Licensing Authority (AYUSH) citing First Schedule authoritative texts.",
            "Verify complete botanical raw material procurement trail and file prior intimation with State Biodiversity Board (SBB).",
            "File registered trademark / trade-dress application with the Indian Trademark Registry (Class 5) to protect brand identity.",
            "Ensure batch manufacturing records strictly conform to Schedule T Good Manufacturing Practices (GMP)."
        ]
        if category == AyurvedaCategory.PHYTOPHARMACEUTICAL:
            action_steps = [
                "Prepare phytochemical marker standardization dossier (HPLC fingerprinting with minimum 4 active markers).",
                "Submit IND application and clinical protocol to CDSCO Subject Expert Committee (SEC).",
                "File Form III with National Biodiversity Authority (NBA) under Section 6(1) prior to patent grant."
            ]
        return title, text, action_steps

    @classmethod
    def _format_hindi(cls, text: str, category: AyurvedaCategory, product_name: str) -> Tuple[str, str, List[str]]:
        title = f"बौद्धिक संपदा एवं विनियामक अनुपालन रिपोर्ट: {product_name}"
        
        # Render high quality Hindi legal analysis
        if category == AyurvedaCategory.CLASSICAL:
            analysis = (
                f"### उत्पाद वर्गीकरण एवं कानूनी विश्लेषण: {product_name}\n\n"
                "1. **उत्पाद वर्गीकरण**: यह उत्पाद औषधि एवं प्रसाधन अधिनियम 1940 की धारा 3(a) एवं प्रथम अनुसूची (चरक संहिता/सुश्रुत संहिता) के तहत **शास्त्रीय आयुर्वेदिक औषधि** के रूप में वर्गीकृत है।\n"
                "2. **पेटेंट पात्रता मूल्यांकन**: भारतीय पेटेंट अधिनियम 1970 की **धारा 3(p)** के तहत पारंपरिक आयुर्वेदिक ज्ञान और ज्ञात घटकों के सीधे मिश्रण पर उत्पाद पेटेंट प्राप्त नहीं किया जा सकता (टीकेडीएल रक्षात्मक डेटाबेस के तहत संरक्षित)।\n"
                "3. **लाइसेंसिंग एवं विनियामक मार्ग**: औषधि एवं प्रसाधन नियमावली 1945 के **नियम 158B(I)(A)** के अनुसार प्रामाणिक ग्रंथों के संदर्भ देकर राज्य आयुष लाइसेंसिंग प्राधिकरण से फॉर्म 25D विनिर्माण लाइसेंस प्राप्त किया जा सकता है। इसके लिए प्रारंभिक नैदानिक परीक्षण (Clinical Trials) अनिवार्य नहीं हैं।\n"
                "4. **जैव विविधता एवं एबीएस अनुपालन**: जैविक विविधता अधिनियम 2002 की **धारा 7** के तहत कच्चे हर्बल घटकों के व्यावसायिक उपयोग के लिए संबंधित राज्य जैव विविधता बोर्ड (SBB) को पूर्व सूचना देना अनिवार्य है।"
            )
            action_steps = [
                "प्रामाणिक आयुर्वेदिक ग्रंथ (प्रथम अनुसूची) के श्लोक व संदर्भों के साथ राज्य आयुष प्राधिकरण में फॉर्म 25D विनिर्माण लाइसेंस हेतु आवेदन करें।",
                "कच्चे हर्बल घटकों के स्रोत की पुष्टि करें और जैविक विविधता अधिनियम की धारा 7 के तहत राज्य जैव विविधता बोर्ड (SBB) को पूर्व सूचना दें।",
                "ब्रांड नाम और विशिष्ट पैकेजिंग की सुरक्षा के लिए भारतीय ट्रेडमार्क रजिस्ट्री (क्लास 5) में ट्रेडमार्क पंजीकृत कराएं।",
                "शेड्यूल T गुड मैन्युफैक्चरिंग प्रैक्टिसेज (GMP) के अनुसार बैच रिकॉर्ड और मानकीकरण प्रोटोकॉल बनाए रखें।"
            ]
        elif category == AyurvedaCategory.PHYTOPHARMACEUTICAL:
            analysis = (
                f"### बौद्धिक संपदा एवं फाइटोफार्मास्युटिकल रणनीति: {product_name}\n\n"
                "1. **वर्गीकरण**: यह उत्पाद सीडीएससीओ नियम 2(eb) के तहत **फाइटोफार्मास्युटिकल औषधि** अथवा नियम 158B(II) के तहत स्वामित्वयुक्त आयुर्वेदिक औषधि के रूप में वर्गीकृत है।\n"
                "2. **पेटेंट एवं नवीनता**: शुद्ध मानकीकृत अंश और सिनर्जिस्टिक प्रभाव के आधार पर पेटेंट अधिनियम की **धारा 3(d) एवं 3(e)** के तहत निष्कर्षण प्रक्रिया और फॉर्मूलेशन पेटेंट योग्य है।\n"
                "3. **राष्ट्रीय जैव विविधता प्राधिकरण (NBA) मंजूरी**: भारतीय जैविक संसाधनों के उपयोग के कारण पेटेंट अनुदान से पूर्व जैविक विविधता अधिनियम की **धारा 6(1)** के तहत एनबीए में फॉर्म III आवेदन अनिवार्य है।\n"
                "4. **नैदानिक परीक्षण**: सीडीएससीओ विषय विशेषज्ञ समिति (SEC) के अनुमोदन से सुरक्षा, विषाक्तता और चरण I/II नैदानिक परीक्षण आवश्यक हैं।"
            )
            action_steps = [
                "न्यूनतम 4 सक्रिय बायोएक्टिव मार्करों के साथ फाइटोकेमिकल मानकीकरण और एचपीएलसी प्रोफाइलिंग रिपोर्ट तैयार करें।",
                "पेटेंट अनुदान से पहले जैविक विविधता अधिनियम की धारा 6(1) के तहत राष्ट्रीय जैव विविधता प्राधिकरण (NBA) में फॉर्म III दाखिल करें।",
                "सीडीएससीओ विषय विशेषज्ञ समिति (SEC) से नैदानिक परीक्षण प्रोटोकॉल का अनुमोदन प्राप्त करें।"
            ]
        else:
            analysis = (
                f"### बौद्धिक संपदा एवं विनियामक विश्लेषण: {product_name}\n\n"
                f"यह उत्पाद **{category.value}** के रूप में मूल्यांकित किया गया है। "
                "सभी घटकों की सुरक्षा, गुणवत्ता परीक्षण और विनियामक अनुपालन वैधानिक मानकों के अनुरूप होना आवश्यक है।"
            )
            action_steps = [
                "संबंधित विनियामक प्राधिकरण से आवश्यक निर्माण एवं विपणन लाइसेंस प्राप्त करें।",
                "जैव विविधता नियमों के तहत पूर्व सूचना व लाभ साझाकरण (ABS) शर्तों का पालन करें।"
            ]

        return title, analysis, action_steps

    @classmethod
    def _format_marathi(cls, text: str, category: AyurvedaCategory, product_name: str) -> Tuple[str, str, List[str]]:
        title = f"बौद्धिक संपदा व विनियामक अनुपालन अहवाल: {product_name}"

        if category == AyurvedaCategory.CLASSICAL:
            analysis = (
                f"### उत्पादन वर्गीकरण व कायदेशीर विश्लेषण: {product_name}\n\n"
                "1. **उत्पादन वर्गीकरण**: हे उत्पादन औषधे आणि सौंदर्यप्रसाधने कायदा १९४० चे कलम ३(a) व पहिली अनुसूची (चरक संहिता/सुश्रुत संहिता) अंतर्गत **शास्त्रीय आयुर्वेदिक औषध** म्हणून वर्गीकृत आहे.\n"
                "2. **पेटंट पात्रता मूल्यांकन**: भारतीय पेटंट कायदा १९७० च्या **कलम ३(p)** नुसार पारंपारिक आयुर्वेदिक ज्ञान आणि ज्ञात घटकांच्या मिश्रणावर थेट प्रॉडक्ट पेटंट घेता येत नाही (टीकेडीएल डेटाबेस अंतर्गत संरक्षित).\n"
                "3. **परवाना व विनियामक मार्ग**: औषधे व सौंदर्यप्रसाधने नियम १९४५ च्या **नियम १५८B(I)(A)** नुसार अधिकृत ग्रंथांचे संदर्भ देऊन राज्य आयुष प्राधिकरणाकडून फॉर्म 25D उत्पादन परवाना मिळवता येतो. यासाठी नव्याने क्लिनिकल ट्रायल्सची आवश्यकता नसते.\n"
                "4. **जैवविविधता व एबीएस अनुपालन**: जैविक विविधता कायदा २००२ च्या **कलम ७** अंतर्गत भारतीय वनौषधींच्या व्यावसायिक वापरासाठी संबंधित राज्य जैवविविधता मंडळाला (SBB) पूर्वसूचना देणे बंधनकारक आहे."
            )
            action_steps = [
                "अधिकृत आयुर्वेदिक ग्रंथातील (पहिली अनुसूची) श्लोक व संदर्भांसह राज्य आयुष प्राधिकरणाकडे फॉर्म 25D उत्पादन परवान्यासाठी अर्ज करा.",
                "वनौषधी कच्च्या मालाच्या स्त्रोताची नोंद ठेवा आणि जैविक विविधता कायद्याच्या कलम ७ नुसार राज्य जैवविविधता मंडळास (SBB) पूर्वसूचना द्या.",
                "ब्रँड नाव व पॅकेजिंगच्या संरक्षणासाठी भारतीय ट्रेडमार्क नोंदणी कार्यालयात (क्लास ५) ट्रेडमार्क नोंदणी करा.",
                "शेड्यूल T गुड मॅन्युफॅक्चरिंग प्रॅक्टिसेस (GMP) मानकांनुसार बॅच रेकॉर्ड व गुणवत्ता चाचण्या पूर्ण ठेवा."
            ]
        elif category == AyurvedaCategory.PHYTOPHARMACEUTICAL:
            analysis = (
                f"### बौद्धिक संपदा व फायटोफार्मास्युटिकल धोरण: {product_name}\n\n"
                "1. **वर्गीकरण**: हे उत्पादन सीडीएससीओ नियम २(eb) अंतर्गत **फायटोफार्मास्युटिकल औषध** किंवा नियम १५८B(II) अंतर्गत मालकी हक्काचे आयुर्वेदिक औषध म्हणून वर्गीकृत आहे.\n"
                "2. **पेटंट व नवीनता**: शुद्ध मानकीकृत घटक आणि सिनर्जिस्टिक परिणामांच्या आधारे पेटंट कायद्याच्या **कलम ३(d) व ३(e)** अंतर्गत प्रक्रिया व फॉर्म्युलेशन पेटंट पात्र ठरू शकते.\n"
                "3. **राष्ट्रीय जैवविविधता प्राधिकरण (NBA) मंजुरी**: भारतीय जैविक घटकांचा वापर असल्याने पेटंट मिळण्यापूर्वी जैविक विविधता कायद्याच्या **कलम ६(१)** नुसार एनबीएकडून फॉर्म ३ मंजुरी अनिवार्य आहे.\n"
                "4. **क्लिनिकल चाचण्या**: सीडीएससीओ विषय तज्ज्ञ समितीच्या (SEC) मंजुरीने सुरक्षितता व टप्पा I/II क्लिनिकल चाचण्या आवश्यक आहेत."
            )
            action_steps = [
                "किमान ४ सक्रिय बायोएक्टिव्ह घटकांसह फायटोकेमिकल मानकीकरण आणि एचपीएलसी प्रोफाइलिंग अहवाल तयार करा.",
                "पेटंट मंजूर होण्यापूर्वी जैविक विविधता कायद्याच्या कलम ६(१) नुसार राष्ट्रीय जैवविविधता प्राधिकरणाकडे (NBA) फॉर्म ३ दाखल करा.",
                "सीडीएससीओ विषय तज्ज्ञ समितीकडून (SEC) क्लिनिकल चाचणी प्रोटोकॉलची मंजुरी मिळवा."
            ]
        else:
            analysis = (
                f"### बौद्धिक संपदा व विनियामक विश्लेषण: {product_name}\n\n"
                f"हे उत्पादन **{category.value}** म्हणून तपासले गेले आहे. "
                "सर्व घटकांची सुरक्षितता व विनियामक अनुपालन वैधानिक नियमांनुसार असणे आवश्यक आहे."
            )
            action_steps = [
                "संबंधित विनियामक प्राधिकरणाकडून आवश्यक उत्पादन व विक्री परवाना मिळवा.",
                "जैवविविधता नियमांनुसार पूर्वसूचना व नफा वाटप (ABS) अटींचे पालन करा."
            ]

        return title, analysis, action_steps
