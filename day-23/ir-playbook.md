# Incident Response Playbook Template

Use this template for each incident type (phishing, ransomware, compromised account, etc.). Update based on lessons learned.

---

## Playbook: [Incident Type]
**Example: Ransomware Detected**

### Severity Criteria
- **Critical:** Ransomware on file server, >100 machines encrypted, business halted.
- **High:** Ransomware on 10-50 machines, some data encrypted, partial outage.
- **Medium:** Ransomware on <10 machines, limited data, business continues.
- **Low:** Ransomware in isolated lab or test environment, no production impact.

### Phase 1: Preparation
- Backup strategy: daily backups, stored offline.
- Communication plan: who to notify (CEO, legal, customers, law enforcement).
- Recovery plan: we have clean images to rebuild servers.
- Team: Incident Commander, SOC analyst, sysadmin, legal contact assigned.

### Phase 2: Detection & Analysis
**Trigger:** Alert from AV/EDR showing ransomware file signature detected or encryption activity detected.

**Actions:**
1. Verify it's real (not false positive) → check infected endpoint in person or via EDR.
2. Scope: Which machines infected? Which shares accessed? How many files encrypted?
3. Severity: Calculate impact (# machines, $ revenue if systems down).
4. Timeline: When was first infection? When was lateral movement? Now?

**Deliverable:** Incident ticket with scope, severity, and timeline.

### Phase 3: Containment
**Short-term (first 30 minutes):**
1. Isolate infected machines from network (unplug ethernet cable or kill Wi-Fi).
2. Kill any suspicious processes (use EDR to stop encryption running).
3. Block attacker's C2 IP at firewall (if known).
4. Disable affected user accounts (to prevent lateral movement).

**Long-term (next 6 hours):**
1. Update antivirus signatures with new ransomware sample.
2. Scan all machines for the same malware.
3. Patch entry point (phishing link, unpatched server).
4. Force password reset for affected users.

### Phase 4: Eradication
1. Confirm attacker is gone (hunt for persistence: hidden accounts, backdoors, scheduled tasks).
2. Remove all instances of ransomware (verify with multiple scans).
3. Patch systems and applications.
4. Rebuild from clean images (don't patch over ransomware).

### Phase 5: Recovery
1. Restore data from clean backups (only after eradication is confirmed).
2. Bring systems back online one at a time, monitor for re-infection.
3. Restore user access with least privilege.
4. Verify business functions are working.

### Phase 6: Post-Incident
1. **Postmortem:** How did attacker get in? (Phishing link? Unpatched server?)
2. **Update playbook:** Did we miss anything?
3. **Training:** Brief team on lessons learned.
4. **Metrics:** Detection time (1h), Containment time (30m), Recovery time (4h), Total impact ($X).

---

## Communication Plan

**Immediately (within 1 hour):**
- Notify CIO, CEO, Legal.
- Document all actions for potential evidence/litigation.

**Within 4 hours:**
- Brief board of directors (for public company).
- Notify customers (if their data affected).

**Within 24 hours:**
- Post-incident meeting with full team.
- Plan for public statement / press release.

---

## Roles & Responsibilities

| Role | Responsible For |
|------|-----------------|
| Incident Commander | Coordinates all actions, timeline, decisions |
| SOC Analyst | Detection, monitoring, alerting |
| Sysadmin | Isolation, patching, rebuilding |
| Forensics Lead | Evidence collection, chain of custody |
| Legal/Compliance | External notifications, regulatory reporting |
| Communications | Internal/external messaging |
