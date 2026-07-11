# One Polished Prompt — SOC Alert Triage

## Use Case
Triaging a security alert: deciding if it's a True Positive or False Positive, with reasoning, so it can go straight into a ticket.

## The Prompt (combines role + template + few-shot + CoT)

```
You are a SOC L1 analyst triaging alerts.

Here are 2 examples of how to reason and format your answer:

Alert: "AV flagged Windows Update process as suspicious."
Reasoning: This matches a known, expected system process; Windows Update is a legitimate signed process commonly misflagged by heuristic AV rules.
Verdict: False Positive

Alert: "5 failed logins followed by 1 success, from a new country, within 2 minutes."
Reasoning: The short time window combined with a geographic jump makes physical travel implausible; this pattern matches credential stuffing or account takeover.
Verdict: True Positive

Now triage this alert, using the same step-by-step reasoning and format:

Alert: {alert_text}

Reasoning:
Verdict:
```

## Tested on 3 Inputs

### Input 1
**Alert:** "User admin ran PowerShell with base64-encoded command at 2 AM, outside business hours."
**Output:**
Reasoning: Encoded PowerShell is a common obfuscation technique used to hide malicious commands from basic string-based detection, and running it at 2 AM outside business hours is inconsistent with normal admin activity.
Verdict: True Positive

### Input 2
**Alert:** "Backup service account logged into 5 servers within 1 minute, as it does every night at 1 AM."
**Output:**
Reasoning: This matches a known, scheduled automation pattern (backup service), consistent timing every night, and expected behavior for that account.
Verdict: False Positive

### Input 3
**Alert:** "New admin account created on a domain controller, no ticket or change request on file."
**Output:**
Reasoning: Admin account creation is a high-privilege action; the absence of an associated change request breaks the expected process, which is a strong indicator of unauthorized privilege escalation.
Verdict: True Positive

## Why This Prompt Works
- **Role-based** – "You are a SOC L1 analyst" sets the right expertise level and tone.
- **Few-shot** – 2 examples lock in exactly how reasoning + verdict should look.
- **CoT** – asking for "Reasoning" before "Verdict" forces step-by-step thinking instead of a snap judgment.
- **Template** – `{alert_text}` variable makes this reusable for any new alert without rewriting the prompt.
