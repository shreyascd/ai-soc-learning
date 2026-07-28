# AI Alert Triage Prompt

Use this prompt with Claude to triage security alerts. Paste the alert text below and Claude will return structured assessment.

---

## Prompt Template

```
You are a SOC analyst triage expert. Analyze the following security alert and provide:
1. Severity (CRITICAL/HIGH/MEDIUM/LOW)
2. Extracted IOCs (IPs, domains, file hashes, usernames)
3. Root cause hypothesis (what likely happened)
4. Recommended next action (1-2 steps)
5. Risk if not acted on (what could happen if ignored)

Format output as structured data. Be concise.

Alert:
[PASTE ALERT HERE]

Respond with:
- Severity: [rating + confidence %]
- IOCs: [IP, domain, hash, etc]
- Root Cause: [1 sentence]
- Next Action: [1-2 steps]
- Risk: [1 sentence]
```

---

## Example 1: Brute Force Alert

**Input:**
```
Alert ID: 12345
Rule: Multiple Failed Logins
Details: User 'admin' from IP 203.0.113.5 had 45 failed login attempts in 5 minutes, then 1 successful login at 23:47 UTC.
Timestamp: 2026-07-28 23:52 UTC
Source System: Domain Controller
```

**Expected Output:**
```
Severity: CRITICAL (95% confidence)
IOCs: 
  - IP: 203.0.113.5 (attacker source)
  - Username: admin (target)
Root Cause: Successful brute-force attack on admin account. Attacker likely used password list, gained access after 45 attempts.
Next Action: 
  1. Isolate affected system from network immediately
  2. Force password reset for admin account + all domain admin accounts
Risk: Attacker now has domain admin access; can move laterally, install persistence, steal all domain data.
```

---

## Example 2: Unusual DNS Query Alert

**Input:**
```
Alert ID: 67890
Rule: Suspicious DNS Pattern
Details: Host 10.0.1.50 (WORKSTATION-01) queried domain 'malicious-payload.ru' 47 times in 2 minutes. Response: NXDOMAIN (domain doesn't exist).
Timestamp: 2026-07-28 08:14 UTC
```

**Expected Output:**
```
Severity: HIGH (85% confidence)
IOCs:
  - Domain: malicious-payload.ru (known malware C2)
  - IP: 10.0.1.50 (compromised workstation)
Root Cause: Malware on WORKSTATION-01 attempting to beacon to C2, but domain is sinkholed or blocked. Rapid retries indicate persistence.
Next Action:
  1. Run EDR scan on WORKSTATION-01 for malware (look for processes creating DNS queries)
  2. Block domain malicious-payload.ru at firewall + DNS
Risk: Malware active; if C2 domain becomes available, attacker can command the system. Lateral movement likely.
```

---

## Example 3: File Hash Detected

**Input:**
```
Alert ID: 23456
Rule: Known Malware Detected
File Hash (SHA256): e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
File Path: C:\Users\jsmith\Downloads\invoice_urgent.exe
Detection Time: 2026-07-28 14:22 UTC
Detection Source: Windows Defender
VirusTotal: 52/60 vendors detect as Emotet trojan
```

**Expected Output:**
```
Severity: CRITICAL (99% confidence)
IOCs:
  - File Hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (Emotet malware)
  - Username: jsmith (infected user)
  - File: C:\Users\jsmith\Downloads\invoice_urgent.exe (malware payload)
Root Cause: User downloaded and executed malicious file disguised as invoice. VirusTotal confirms Emotet trojan (52/60 vendors). Likely phishing attack.
Next Action:
  1. Isolate jsmith's machine from network immediately
  2. Scan for lateral movement (check network logs for suspicious outbound connections from that host)
Risk: Emotet is banking trojan + botnet. Attacker has system access, can steal credentials, encrypt files, move laterally.
```

---

## Tips for Using This Prompt

1. **Paste raw alert data** — including timestamp, source, alert rule name.
2. **Include context** — any related alerts, user info, system importance.
3. **Trust the structure** — severity + IOCs + hypothesis + action + risk. Follow this pattern.
4. **Verify before acting** — AI might hallucinate; verify IOCs with VirusTotal/TI before isolating production systems.
5. **Use for first pass** — AI triage outputs should be reviewed by human analyst before major actions.
