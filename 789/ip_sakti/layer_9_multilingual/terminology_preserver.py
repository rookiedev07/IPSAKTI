"""
Terminology Preserver and Dual Glossary Manager
Ensures legal, statutory, and Ayurvedic terms maintain semantic fidelity across English, Hindi, and Marathi.
"""

from typing import List, Dict
from ..core.schema import BilingualTerm, LanguageCode, AyurvedaCategory
from ..core.constants import DOMAIN_GLOSSARY


class TerminologyPreserver:
    """
    Manages dual-track terminology glossaries and statutory term alignments.
    """

    @classmethod
    def get_bilingual_glossary_for_output(
        cls,
        category: AyurvedaCategory,
        text_content: str,
        target_lang: LanguageCode
    ) -> List[BilingualTerm]:
        glossary_items: List[BilingualTerm] = []

        if target_lang == LanguageCode.EN:
            # If target language is English, provide canonical terms with Sanskrit/Hindi references
            target_key = "hi"
        elif target_lang == LanguageCode.HI:
            target_key = "hi"
        else:
            target_key = "mr"

        for term_key, term_info in DOMAIN_GLOSSARY.items():
            # Check if the concept is referenced in text or matches category
            if term_key.lower() in text_content.lower() or category.value.lower() in term_key.lower():
                glossary_items.append(
                    BilingualTerm(
                        english_term=term_info["en"],
                        local_term=term_info[target_key],
                        phonetic_or_devanagari=term_info[target_key],
                        statutory_context=term_info["definition"]
                    )
                )

        return glossary_items
