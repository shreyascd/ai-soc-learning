# Zero-shot vs Few-shot Comparison

## Task 1: Classify log severity

**Zero-shot:** "Classify this log's severity: 'Failed login attempt from 192.168.1.5'"
Output: Low severity — a single failed login.

**Few-shot:**
```
Log: "3 failed logins in 1 min" → Severity: Medium
Log: "Malware detected on endpoint" → Severity: High
Log: "Failed login attempt from 192.168.1.5" → Severity:
```
Output: Low — matches the single-attempt pattern shown in examples, consistent with format.

## Task 2: Extract IP + action from a log line

**Zero-shot:** "Extract the IP and action: 'Blocked connection from 45.33.22.11 to port 22'"
Output: IP: 45.33.22.11, Action: Blocked connection to port 22

**Few-shot:**
```
Log: "Allowed traffic from 10.0.0.5 to port 443" → IP: 10.0.0.5, Action: Allowed, Port: 443
Log: "Blocked connection from 45.33.22.11 to port 22" → IP: 45.33.22.11, Action: Blocked, Port:
```
Output: 22 — few-shot gave a cleaner, structured 3-field output matching the exact format shown.

## Task 3: Determine if an alert is a false positive

**Zero-shot:** "Is this alert a false positive? 'Antivirus flagged a script used by IT for routine patching.'"
Output: Likely a false positive since it matches expected IT activity.

**Few-shot:**
```
Alert: "AV flagged Windows Update process" → False Positive (known system process)
Alert: "AV flagged unknown encoded PowerShell script" → Real Threat (obfuscation is suspicious)
Alert: "Antivirus flagged a script used by IT for routine patching." → 
```
Output: False Positive (known, expected IT activity) — few-shot reasoning was more consistent with the labeling style needed for a ticket.

## Comparison Table

| Task | Zero-shot Output Quality | Few-shot Output Quality |
|------|--------------------------|--------------------------|
| Classify severity | Reasonable but unstructured | More consistent, matched label format |
| Extract IP + action | Correct but format varies | Clean, structured output |
| False positive check | Correct reasoning | Correct + matched exact labeling convention |
