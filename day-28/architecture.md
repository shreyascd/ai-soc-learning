# AI SOC Assistant Architecture

## End-to-End Flow

```
┌─────────────────┐
│  Security Alert │ (input: alert text)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  LLM Triage & Planning      │ (Claude analyzes alert, decides what to check)
│  "This looks like brute     │
│   force. I should check:    │
│   1. IP reputation          │
│   2. Known malware IOCs"    │
└────────┬────────────────────┘
         │
         ▼
    ┌────────────────────────────────────────────┐
    │       Tool Calls (LangChain Agent)         │
    ├────────────┬─────────────────┐──────────┐  │
    │ Tool 1     │ Tool 2          │ Tool 3   │  │
    │ Check IP   │ Search IOCs     │ (future) │  │
    │ Reputation │ in Known DB     │          │  │
    └────────────┴─────────────────┴──────────┘  │
         │ (return results)                      │
    └────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  LLM Summary & Report Generation        │
│  "Based on tool results: IP is high     │
│   abuse score, matches Emotet IOC,      │
│   severity CRITICAL, recommend isolate" │
└────────┬────────────────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Structured Output (JSON)    │
│  - severity: CRITICAL        │
│  - IOCs: [IP, domain, hash]  │
│  - recommendation: isolate   │
│  - reasoning: [explanation]  │
└──────────────────────────────┘
```

## Components

**1. Alert Input**
Raw security alert (text). Could be:
- "Connection to 203.0.113.5:4444 detected"
- "Multiple failed logins for admin from 192.0.2.10"
- "File hash detected: d41d8cd98f00b204e..."

**2. LLM (Claude via LangChain)**
- Reads alert
- Plans what information is needed
- Decides which tools to call
- Interprets tool results
- Generates summary + recommendation

**3. Tools (Agent Tool Definitions)**
Tool 1: `check_ip_reputation(ip)` → queries AbuseIPDB → returns abuse score, reports count
Tool 2: `search_known_iocs(indicator)` → searches internal IOC database → returns matches

**4. Memory**
Keeps alert context across tool calls. Example:
- Turn 1: "Alert: Connection to 203.0.113.5"
- Tool Call: check_ip_reputation("203.0.113.5") → score: 85
- Turn 2: "Score is 85. Now let me search if this IP appears in known IOCs"
- Tool Call: search_known_iocs("203.0.113.5") → matches: Emotet C2 (high confidence)

Drop old alerts from memory (keep window small, e.g., 1-3 alerts max).

**5. Output Format**
Structured markdown report:
```
## Alert Triage Report
**Severity:** CRITICAL
**Source Alert:** [original text]
**Extracted IOCs:**
  - IP: 203.0.113.5 (abuse score 85, Emotet C2)
  - Port: 4444 (non-standard)
**Assessment:** Confirmed malware C2 communication
**Recommendation:** Isolate host immediately, notify IR team
```

## Why This Architecture?

1. **Sequential reasoning:** LLM thinks step-by-step instead of guessing. "I need to check reputation, then search IOCs."
2. **Tool grounding:** LLM can call real tools (reputation APIs, IOC databases) instead of hallucinating.
3. **Memory context:** Alert context flows through entire conversation. No need to repeat alert in each tool call.
4. **Human-interpretable:** Output is structured + includes reasoning so analyst can understand why assistant recommended action.

## What Could Go Wrong?

- **LLM decides wrong tools:** "Alert about ransomware" but LLM only calls IP checker, forgets to check file hash. → Mitigate: Use detailed tool descriptions.
- **Tool failure:** API down, invalid input. → Mitigate: Graceful error handling, fallback to cached data.
- **Hallucinated IOCs:** LLM invents an IOC that doesn't exist in alert. → Mitigate: Always validate tool inputs before calling.
- **Over-calling tools:** Assistant makes 50 API calls for 1 alert. → Mitigate: Set max tool call limit (e.g., 5 calls).
