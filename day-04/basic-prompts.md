# 5 Basic Prompts

### Prompt 1
**Prompt:** "Explain what a firewall does in 2 sentences."
**Response:** A firewall monitors and filters incoming/outgoing network traffic based on security rules, blocking anything that doesn't match allowed criteria. It acts as a barrier between a trusted internal network and untrusted external networks like the internet.
**Rating:** 5/5 — clear, correct, exactly the length asked.

### Prompt 2
**Prompt:** "List 3 common SOC analyst tools."
**Response:** SIEM (e.g. Splunk), EDR (e.g. CrowdStrike), and packet analysis tools (e.g. Wireshark).
**Rating:** 5/5 — accurate and relevant examples.

### Prompt 3
**Prompt:** "Write a one-line cron job to run a backup script every day at 2 AM."
**Response:** `0 2 * * * /path/to/backup.sh`
**Rating:** 5/5 — correct cron syntax.

### Prompt 4
**Prompt:** "What's the difference between authentication and authorization?"
**Response:** Authentication verifies who you are (login), authorization determines what you're allowed to do once verified (permissions).
**Rating:** 5/5 — concise and accurate.

### Prompt 5
**Prompt:** "Give me the exact CVE number for the most critical vulnerability found this week."
**Response:** Gave a plausible-sounding but unverifiable CVE number without a real source.
**Rating:** 2/5 — this is where hallucination risk shows up; needs to be cross-checked against a real CVE database, not trusted directly.
