# Threat Hunting — From Detection to Discovery

## What is Threat Hunting?

Detection waits for alerts. Hunting goes looking for threats before alerts fire.

**Detection:** "Alert fires when brute-force detected" (reactive).
**Hunting:** "Let me search logs for failed login patterns I haven't written alerts for yet" (proactive).

Hunting is detective work. You have a hypothesis (e.g., "there might be lateral movement") and you go prove or disprove it using data (logs, network traffic, file systems).

---

## Threat Hunting Workflow

**Phase 1: Develop Hypothesis**
"Based on what I know about attacker behavior, what would I expect to see?"
Examples:
- "If an attacker got domain admin, they'd add new accounts or modify group memberships."
- "If there's C2 communication, I'd see repeated DNS queries to the same domain."
- "If data was exfiltrated, I'd see large file transfers to external IPs."

**Phase 2: Gather Data**
Run queries against your data sources (SIEM, logs, network captures).
Example query: "Show me all new user account creations in past 30 days, ordered by timestamp."

**Phase 3: Analyze Patterns**
Look for anomalies (what's different from baseline).
- Normal: 1 new account per week (IT provisioning).
- Anomaly: 10 new accounts in 1 hour at 2 AM.

**Phase 4: Investigate Findings**
Dig deeper. Ask follow-up questions.
- "Those 10 accounts — who created them? What are they used for?"
- "Check if any of those accounts accessed sensitive file shares."
- "See if they generated any suspicious process execution."

**Phase 5: Escalate or Document**
If you find actual threat: escalate to IR team.
If you find nothing: document your hypothesis and findings (improves future hunts).

---

## 5 High-ROI Threat Hunts

### Hunt 1: Lateral Movement via New Admin Accounts
**Hypothesis:** Attacker gains initial access, creates new admin account for persistence.
**Query:** 
```
EventID: 4720 (user created) OR 4722 (user enabled) OR 4756 (user added to group)
Filter for: Domain Admins, Enterprise Admins, or local Administrators groups
Timeframe: Last 30 days
Sort by: timestamp
```
**What to look for:** 
- Accounts created outside business hours?
- Accounts created by unexpected users (not your IT team)?
- Accounts never used, but sitting in admin group?

**ROI:** High. If you find unauthorized admin accounts, it's a confirmed breach.

---

### Hunt 2: C2 Beaconing via DNS
**Hypothesis:** Malware on internal machine is trying to contact C2 server via DNS queries.
**Query:**
```
DNS queries from internal IPs to external domains
Filter for: Repeated queries to same domain (>5 in 5 minutes)
Filter for: Unusual domain patterns (random subdomains, no HTTPS, etc)
Timeframe: Last 7 days
```
**What to look for:**
- Same IP querying random.malware-c2.com 47 times in 2 minutes (retry loop)?
- Query to domain that doesn't resolve (sinkholed by defenders)?
- Query to known malware C2 domain (check TI)?

**ROI:** Very high. Beaconing pattern is almost always malware.

---

### Hunt 3: Data Exfiltration via Large Transfers
**Hypothesis:** Attacker stole data, now uploading to external server.
**Query:**
```
Outbound network connections with large byte counts
Filter for: >100 MB transferred
Filter for: Destination = external IP (not known cloud provider)
Timeframe: Last 7 days
```
**What to look for:**
- 10 GB transferred to 203.0.113.5 at 3 AM?
- Multiple machines transferring data to same external IP?
- Transfer to IP in high-risk country (check IP geolocation)?

**ROI:** Critical if found. Data theft is the main attacker goal.

---

### Hunt 4: Process Injection & Privilege Escalation
**Hypothesis:** Attacker used exploit to escalate from user to admin.
**Query:**
```
Process creation events (Event 4688) with suspicious patterns
Filter for: Parent process = explorer.exe, child process = system process (svchost, services, lsass)
Filter for: Process command line contains "powershell", "-enc", or other obfuscation
Timeframe: Last 30 days
```
**What to look for:**
- explorer.exe spawning powershell with base64-encoded command?
- Unusual process tree (grandparent → parent → child)?
- Process creation from unexpected directory (not C:\Windows\System32)?

**ROI:** High. Process injection is classic privilege escalation.

---

### Hunt 5: Persistence via Scheduled Tasks or Registry Modifications
**Hypothesis:** Attacker left persistence mechanism (backdoor that survives reboot).
**Query:**
```
Scheduled task creation (Event 4698 or schtasks.exe execution)
Filter for: Task run time = system startup or every 1 minute
Filter for: Task action = C:\Windows\Temp\[random].exe or powershell
Timeframe: Last 30 days
```
**What to look for:**
- Scheduled task running exe from Temp folder?
- Task created with suspicious name (not IT automation)?
- Task runs hidden (no UI)?

**ROI:** High. Persistence means attacker can come back even after you remove initial malware.

---

## Tips for Effective Hunting

1. **Start with TI:** Check known malicious IPs, domains, file hashes before hunting blind.
2. **Baseline first:** Know what "normal" looks like before hunting for anomalies.
3. **Follow the chain:** One finding leads to 3 more questions. Follow them.
4. **Document hypothesis:** Write down what you expected to find BEFORE hunting (avoid confirmation bias).
5. **Time-box:** Set a time limit (e.g., 2 hours). If you don't find anything, move on and document.
6. **Share findings:** Tell team what you hunted and what you found (or didn't find). Collective knowledge improves hunting.
