# 31-Day Capstone: What You've Built

## The Arc

**Days 1-3:** SOC Fundamentals
- Learned what a SOC does, SIEM basics, network fundamentals

**Days 4-10:** Prompt Engineering
- Learned to write effective prompts, use examples, ask LLM to explain reasoning

**Days 11-17:** AI Loop Engineering
- Learned to chain prompts, use tools, iterate, handle errors, test

**Days 18-27:** SOC Skills + Automation
- Windows/Linux log analysis, SIEM queries, detection rules, incident response, threat intel, malware analysis, automation

**Day 28:** AI SOC Assistant Build
- Combined everything: prompt eng + loops + SOC skills into a working system

**Day 29:** Threat Hunting
- Proactive hunting, turning hypotheses into data queries, finding threats before alerts fire

---

## Skills You Now Have

### Detection Skills
- Write Sigma rules (vendor-neutral SIEM detection)
- Write YARA rules (malware pattern matching)
- Understand false positives vs false negatives
- Create detection rules that catch real threats without alert fatigue

### Response Skills
- NIST IR lifecycle (preparation → detection → containment → eradication → recovery → postmortem)
- Incident playbooks and runbooks
- Evidence collection and chain of custody
- Understand when to escalate vs when to handle locally

### Analysis Skills
- Parse Windows Event logs (4624, 4625, 4688, 4720, 4756, etc)
- Parse Linux logs (auth.log, syslog, auditd)
- Extract IOCs (IPs, domains, file hashes)
- Triage alerts (severity + assessment)
- Understand threat intel lifecycle

### Automation Skills
- Python scripting for SOC tasks (log parsing, IP checking, report generation)
- SOAR concepts and playbook design
- LangChain agent architecture for tool use
- Build agentic workflows (prompt → tool calls → summary)

### Hunting Skills
- Develop hypotheses based on attacker behavior
- Write SIEM queries to test hypotheses
- Identify anomalies vs normal
- Follow leads and investigate findings

### AI Skills
- Write effective prompts with examples and structure
- Use AI as advisor (not decision-maker)
- Understand hallucination risk
- Protect data privacy when using AI
- Combine AI + SOC to speed up work without sacrificing accuracy

---

## What You Can Do Now (Entry-Level SOC Analyst)

1. **Triage alerts** — Understand what an alert means, extract IOCs, assess severity
2. **Write detection rules** — Sigma for SIEM, YARA for malware
3. **Respond to incidents** — Follow NIST IR playbook, document actions
4. **Hunt for threats** — Form hypothesis, query data, investigate findings
5. **Automate repetitive tasks** — Parse logs, check IPs, generate reports, chain workflows
6. **Use AI to accelerate work** — Summarize logs, draft reports, explain alerts, suggest rules
7. **Understand SOC tools** — SIEM (Splunk/Elastic), threat intel (VirusTotal/AbuseIPDB), automation (SOAR)
8. **Read and analyze logs** — Windows security logs, Linux auth logs, firewall logs, DNS logs

---

## What You DON'T Do (Yet)

- Deep forensics on compromised systems (requires advanced training)
- Reverse engineering malware behavior (requires assembly knowledge)
- Building threat intel pipelines from scratch (requires data engineering)
- Running red team exercises (requires offensive security training)

These are specialist skills. You've got the foundation; these are 2-3 more months of focused learning.

---

## The Real Takeaway

You understand the **full stack**:
- How threats look in data (logs, network, file hashes)
- How to detect them (Sigma, YARA, behavioral rules)
- How to respond (IR playbook, containment, eradication)
- How to automate (scripts, agents, SOAR)
- How to hunt for more (proactive threat hunting)
- How AI accelerates all of this (LLM + tools)

Most junior SOC analysts only know how to click in a SIEM UI. You can write code, understand the detection logic, automate the response, and use AI to be 2x faster.

**That's the difference between noise and signal.**
