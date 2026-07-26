# Detection-as-Code: Sigma & YARA Rules

## What is Detection-as-Code?
Instead of clicking in a SIEM UI to create a detection rule ("IF this field = that value THEN alert"), write the rule as code. Benefits:
- Version control (git tracks every change).
- Reproducibility (same rule runs everywhere).
- Testing (you can test the rule against sample data before deploying).
- Portability (a Sigma rule works on Splunk, Elastic, any SIEM that supports Sigma).

## Sigma Rules (SIEM-Agnostic Detection)

Sigma is a generic detection rule format. Write once, deploy to Splunk, Elastic, Microsoft Sentinel, Qradar, etc.

**Example: Brute-Force Detection**
```yaml
title: Brute Force Login Attempt (Sigma)
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4625  # Failed logon
    - source_ip: 203.0.113.5  # From this IP
  timeframe: 5m
  condition: selection | count(target_user) by source_ip > 10  # 10+ failures in 5 min
action: alert
```

**Anatomy:**
- `logsource` — what data source (Windows Event ID, Syslog, network logs).
- `detection/selection` — what to match (EventID 4625 = failed logon).
- `timeframe` — within what time window?
- `condition` — how many matches = alert? (>10 failures = alert).

**Strengths:**
- Easy to read, non-technical people can understand it.
- Portable — compile to SPL (Splunk), KQL (Elastic), etc.

**Weakness:**
- Limited to log-based detection; doesn't handle binary patterns.

---

## YARA Rules (File/Binary Pattern Matching)

YARA matches patterns in files (malware, config files, etc.). Used by antivirus, EDR, threat hunters.

**Example: Emotet Malware Pattern**
```
rule Emotet_Botnet {
    meta:
        description = "Detects Emotet botnet samples"
        author = "Malware Research Team"
        date = "2026-07-25"
    strings:
        $s1 = "WinInetGetProxyForUrl" ascii
        $s2 = {48 8D 15 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ??}  // Binary signature
        $s3 = /C2-IP: [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/  // Regex
    condition:
        all of them
}
```

**Anatomy:**
- `meta` — author, description, date (metadata).
- `strings` — what to match: text ($s1), binary hex ($s2), regex ($s3).
- `condition` — "all of them" means all 3 strings must be present.

**Strengths:**
- Matches binary patterns, file signatures, obfuscated strings.
- Fast, efficient, used in production EDR.

**Weakness:**
- Obfuscated malware can evade string-based rules (needs behavioral detection).

---

## Use Case Development Workflow

**Step 1: Identify Threat**
"Attacker uses brute-force to break into admin accounts."

**Step 2: Define Detection**
"Alert when 1 IP has 10+ failed logons in 5 minutes."

**Step 3: Write Rule**
Write Sigma rule (brute-force detection above).

**Step 4: Test Rule**
Run against 1 week of historical logs. Do you get expected alerts? Any false positives?

**Step 5: Tune**
If too noisy (100 alerts/day), increase threshold to 20 failures. If misses real attacks, lower to 5 failures.

**Step 6: Deploy**
Push rule to SIEM. Monitor. Iterate based on feedback.

---

## False Positives vs False Negatives

**False Positive (FP):** Rule fires, but it's not actually a threat. Example: a script that tries 15 passwords in a minute (legit automation) triggers the brute-force rule.
- Cost: Analyst wasted time, alert fatigue.
- Risk: Can't trust the rule anymore.

**False Negative (FN):** Rule doesn't fire, but it should have. Example: attacker uses 1 IP but staggered logins (1 per minute over 30 minutes = 30 total), stays under your 10-in-5-minutes threshold.
- Cost: Attacker gets in undetected.
- Risk: Breach, data loss.

**Which is worse?**
FN is worse (you miss the attack). But too many FPs and you disable the rule entirely. Balance is key: aim for high confidence (FP) over high sensitivity (FN).
