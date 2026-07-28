# SOC AI Prompt Pack v2 — 8 Production Prompts

Based on Days 4-27 learning. Each prompt is tested, structured, and ready to use.

---

## Prompt 1: Alert Triage (from Day 27)
**Purpose:** Quickly assess alert severity, extract IOCs, recommend action.
**Use when:** Alert fires, need to know if it's critical.
```
Analyze this security alert. Return: Severity (CRITICAL/HIGH/MEDIUM/LOW), IOCs, root cause hypothesis, next step, risk if ignored.

Alert: [paste alert]
```

---

## Prompt 2: Log Summarization
**Purpose:** Distill large log files into human-readable summary.
**Use when:** 1000+ log lines, need pattern.
```
Summarize the following security logs in 5 sentences. Highlight: What happened, who was involved, what data accessed, suspicious patterns, recommended action.

Logs:
[paste logs]

Summary:
```

---

## Prompt 3: Explain Security Concept
**Purpose:** Teach analyst unfamiliar concepts in simple terms.
**Use when:** Alert mentions unfamiliar attack, analyst needs quick education.
```
Explain [CONCEPT] to a security analyst in 3 sentences. Include: What it is, why it's dangerous, how to detect it.

Example: "Explain Kerberos golden ticket attack"
```

---

## Prompt 4: Draft Incident Report
**Purpose:** Generate first-pass incident report for executive review.
**Use when:** Incident happened, need to document.
```
Draft a brief incident report. Include: Timeline, what happened, who was affected, data impact, remediation steps, recommended preventive measures.

Incident details:
[brief description]

Report:
```

---

## Prompt 5: Threat Hunt Suggestion
**Purpose:** Based on observed threat, suggest what to hunt for.
**Use when:** Found 1 malware sample, want to find similar ones.
```
I found a malware sample with these characteristics: [describe indicators]. Suggest 3 threat hunting queries to find similar activity in my SIEM logs.

Characteristics:
[paste IOCs, patterns, behaviors]

Hunting Queries:
```

---

## Prompt 6: Detection Rule Feedback
**Purpose:** Improve detection rule to reduce false positives or catch more attacks.
**Use when:** Rule fires too often or misses real attacks.
```
I have a detection rule with high false positives. Help me improve it.

Current Rule: [paste rule]
False Positives: [describe false positives]
Missed Attacks: [any attacks it missed?]

Improved Rule:
```

---

## Prompt 7: Risk Assessment
**Purpose:** Quantify risk of a finding for executive communication.
**Use when:** Need to justify security investment or incident severity.
```
Assess the risk of this finding. Rate severity (1-10), explain business impact, estimate remediation cost, suggest priority.

Finding:
[describe security issue]

Risk Assessment:
```

---

## Prompt 8: Playbook Drafting
**Purpose:** Create incident response playbook steps.
**Use when:** New attack type, need to document response workflow.
```
Draft an incident response playbook for [INCIDENT_TYPE]. Include: Detection triggers, immediate actions (first 30 min), short-term containment (next 6 hours), long-term eradication, recovery steps, postmortem questions.

Incident Type: [e.g., Ransomware Detection]

Playbook:
```

---

## Usage Patterns

**For Triage:** Use Prompts 1 + 2 (triage + summarize logs).
**For Hunting:** Use Prompts 5 + 3 (suggest hunt + explain unfamiliar concepts).
**For Reporting:** Use Prompts 4 + 7 (draft report + risk assessment).
**For Automation:** Use Prompts 6 + 8 (improve rules + draft playbooks).

---

## Critical Rules

1. **Always verify AI output** — hash lookups on VirusTotal, IP reputation on AbuseIPDB. Don't trust hallucinations.
2. **Redact PII before pasting** — usernames, real IPs, real domains. Use placeholder names.
3. **AI suggests; human decides** — AI is advisor. Isolation/remediation decisions stay with analyst/IR team.
4. **Keep outputs in version control** — if using AI for playbook drafting, save to git for team review.
5. **Test on sample alerts first** — before using in production, test prompt on 3-5 real alerts from your org to validate.
