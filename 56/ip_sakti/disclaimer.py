"""
The PS is explicit: the assistant must "clearly state that it provides
information and not legal advice." This is force-appended server-side to
every structured response, not left to the LLM to remember -- an LLM that
forgets the disclaimer on one response out of a hundred is still a
compliance failure for a tool like this.
"""

STANDARD_DISCLAIMER = (
    "This response provides general information to help you understand the "
    "relevant IP and regulatory landscape. It is NOT legal advice. Verify "
    "every citation against its primary source before relying on it, and "
    "consult a qualified IP attorney or regulatory professional before "
    "making filing, commercial, or compliance decisions."
)

ESCALATION_NOTE = (
    "This query touches on matters where a professional review is strongly "
    "recommended before taking action -- consider consulting a registered "
    "patent agent, IP attorney, or the relevant regulatory authority directly."
)


def build_footer(needs_escalation: bool = False) -> str:
    """Returns the disclaimer text to attach to every response, with an
    optional escalation note appended when confidence is low or the topic
    is high-stakes (e.g. ABS compliance, patent filing decisions)."""
    if needs_escalation:
        return f"{STANDARD_DISCLAIMER}\n\n{ESCALATION_NOTE}"
    return STANDARD_DISCLAIMER
