"""
Language Detector
Detects user query language across English (EN), Hindi (HI), and Marathi (MR).
"""

import re
from typing import Tuple
from ..core.schema import LanguageCode


class LanguageDetector:
    """
    Identifies language from user text or query intent.
    Supports Devanagari script differentiation (Hindi vs Marathi) and Latin English.
    """

    MARATHI_MARKERS = {
        "आहे", "नाही", "करावे", "औषध", "औषधे", "कसे", "काय", "मिळेल", "नोंदणी",
        "हक्क", "झाले", "होते", "मध्ये", "साठी", "यांचे", "करणे", "केले", "वारसा"
    }

    HINDI_MARKERS = {
        "है", "नहीं", "करना", "दवा", "दवाई", "कैसे", "क्या", "मिलेगा", "पंजीकरण",
        "अधिकार", "हुआ", "था", "में", "के लिए", "उनका", "करना", "किए", "विरासत"
    }

    @classmethod
    def detect_language(cls, text: str, default_fallback: LanguageCode = LanguageCode.EN) -> LanguageCode:
        if not text or not text.strip():
            return default_fallback

        # Check for Devanagari Unicode Block (U+0900 to U+097F)
        devanagari_chars = re.findall(r"[\u0900-\u097F]", text)
        if not devanagari_chars or len(devanagari_chars) < 3:
            return LanguageCode.EN

        words = set(re.findall(r"[\u0900-\u097F]+", text))

        marathi_hits = len(words.intersection(cls.MARATHI_MARKERS))
        hindi_hits = len(words.intersection(cls.HINDI_MARKERS))

        if marathi_hits > hindi_hits:
            return LanguageCode.MR
        elif hindi_hits > marathi_hits:
            return LanguageCode.HI
        else:
            # Check for specific Marathi ligature / character 'ळ' (U+0933)
            if "ळ" in text:
                return LanguageCode.MR
            return LanguageCode.HI
