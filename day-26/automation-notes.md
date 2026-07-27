# 5 SOC Tasks to Automate + SOAR Concept

## Why Automate?
Manual SOC work is repetitive: parse logs, look up IPs, write reports, repeat 100 times. Automation saves time, reduces errors, and lets analysts focus on judgment calls that need humans.

## 5 SOC Tasks Worth Automating

**1. IOC Enrichment (IP Lookup)**
What it is: Alert fires: "Connection to 203.0.113.5" → analyst manually checks VirusTotal, AbuseIPDB, notes if malicious.
Why automate: Do this for every IP automatically. Attach reputation score to alert before analyst sees it.
Script: Query AbuseIPDB/VirusTotal API for each IP, return score.

**2. Log Parsing & Extraction**
What it is: Analyst reads auth.log, manually extracts failed logins, counts per IP, formats as report.
Why automate: Parse logs programmatically, extract fields, aggregate, save as CSV.
Script: Read log file, regex to extract IPs/usernames/timestamps, group, write CSV.

**3. Alert Triage & Deduplication**
What it is: Alert fires 50 times for same incident (same source IP, same attack pattern, 2-minute window).
Why automate: Deduplicate alerts (merge into single ticket), suppress noisy rules.
Script: Check if alert already exists for this IP/indicator in past 30 minutes; if yes, append to existing ticket instead of creating new.

**4. Report Generation**
What it is: Analyst reviews 200 alerts, manually writes executive summary: "20 phishing attempts, 5 compromised IPs, 0 critical, 15 medium."
Why automate: Count alert types, severity, affected systems, generate templated report.
Script: Query SIEM for all alerts in past 24h, aggregate by type/severity, render HTML report.

**5. Automated Response (SOAR)**
What it is: Confirmed malware detected; analyst manually: blocks IP at firewall, kills process on endpoint, disables user account.
Why automate: Chain: detect → block → kill → disable.
Script: SOAR playbook triggers on detection; automatically executes response steps.

---

## SOAR (Security Orchestration, Automation, Response)

SOAR is a platform that automates the full incident response workflow: detection → enrichment → triage → response.

**Example SOAR Workflow:**
1. Alert: "Ransomware detected on host WORKSTATION-01"
2. Enrichment: Query TI → file hash is known Conti ransomware (99% confidence)
3. Triage: Mark as CRITICAL
4. Automated Response:
   - Kill process on WORKSTATION-01
   - Block IP at firewall
   - Isolate host from network
   - Disable user account
   - Create incident ticket
   - Notify IR team
5. Human Review: Incident commander reviews automated actions, approves or rolls back.

**Why SOAR matters:** Without it, steps 4a-4e would take an analyst 30 minutes of manual clicking. SOAR does it in 30 seconds.

---

## Scripts vs Playbooks vs Runbooks

**Script:** Single-purpose automation. Example: `lookup_ip.py` takes one IP, returns reputation.
- Reusable, simple, easy to test.
- Limited scope.

**Playbook:** Chained workflows triggered by an event. Example: "On ransomware detection, run these 5 scripts in sequence."
- Automated orchestration.
- Requires a SOAR platform or workflow engine.

**Runbook:** Manual instructions for humans. Example: "If ransomware detected: 1. Isolate host. 2. Notify IR lead. 3. Preserve evidence. 4. Contact backup admin."
- For when automation isn't ready or decisions need human judgment.
- Reduces time-to-action even if not fully automated.

---

## When NOT to Automate

**High-judgment decisions:** "Is this a real attack or false positive?" → Needs human analysis.
**Novel incidents:** Never seen before attack pattern → No automation rule exists yet.
**Legal/compliance actions:** "Delete user account" or "notify law enforcement" → Requires approval chain, can't be fully automated.

Automate the repetitive, low-judgment work. Keep humans in the loop for decisions that matter.
