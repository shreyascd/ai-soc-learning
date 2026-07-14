def estimate_tokens(text: str) -> int:
    """Rough token estimate: tokens ≈ words × 1.3"""
    words = len(text.split())
    return round(words * 1.3)


samples = {
    "short": "Failed login attempt from 192.168.1.5 at 14:32.",
    "medium": (
        "A user account triggered 5 failed login attempts followed by one "
        "successful login, all within 2 minutes, from two different countries. "
        "This pattern is consistent with credential stuffing or an account "
        "takeover attempt and should be escalated for further review."
    ),
    "long": (
        "During a routine SIEM review, the analyst noticed a service account "
        "that normally only logs into three specific servers had authenticated "
        "against twelve additional servers within a 10 minute window. Further "
        "investigation showed that this account also executed several "
        "PowerShell commands with base64-encoded parameters, none of which "
        "matched its usual scheduled backup tasks. Given the unusual scope of "
        "access, the off-pattern timing, and the use of obfuscated commands, "
        "the analyst escalated the alert as a likely case of credential misuse "
        "or lateral movement by an attacker who had compromised the service "
        "account, and recommended immediately disabling the account pending "
        "further forensic review of affected systems."
    ),
}

for label, text in samples.items():
    tokens = estimate_tokens(text)
    print(f"{label}: {len(text.split())} words -> ~{tokens} tokens")
