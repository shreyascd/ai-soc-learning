# PCAP Analysis Report Template

## Report: [Incident Date] Network Traffic Analysis

**Analyst:** [Your name]  
**Date Analyzed:** [Today's date]  
**PCAP File:** [filename.pcap]  
**Time Period Captured:** [Start time - End time]  
**Total Packets:** [X] | **File Size:** [Y MB]  

---

## Executive Summary
Brief (2-3 sentence) overview of what the traffic shows and key findings.

Example: "Traffic analysis of [filename] reveals suspicious outbound connections from internal host 10.0.1.50 to external IP 203.0.113.5 on port 4444. DNS queries to known malware-domain registry match beaconing patterns consistent with C2 communication."

---

## Key Findings

### 1. Top Talkers (Most Active IPs)
| Source IP | Destination IP | Protocol | Packets | Bytes | Activity |
|-----------|-----------------|----------|---------|-------|----------|
| 10.0.1.50 | 203.0.113.5 | TCP | 1,250 | 2.3 MB | Outbound to suspicious IP |
| 10.0.1.50 | 8.8.8.8 | DNS | 145 | 8.5 KB | DNS queries |
| 10.0.0.1 | 10.0.1.50 | TCP | 89 | 1.2 MB | Gateway communication |

**Analysis:** Host 10.0.1.50 is most active, primarily communicating outbound to 203.0.113.5 (suspicious).

---

### 2. Suspicious IPs / Domains
- **203.0.113.5** — Multiple failed TCP connections on port 4444; not in known corporate IP ranges. **Action:** Check IP reputation against threat intelligence feeds.
- **malicious-beacon.com** — DNS queries every 30 seconds; matches known C2 domain list. **Action:** Block domain at firewall.

---

### 3. Traffic Patterns
- **Beaconing pattern detected:** 10.0.1.50 → 203.0.113.5:4444, every ~30 seconds, consistent size packets (512 bytes).
  - **Interpretation:** Likely C2 check-in; attacker on 10.0.1.50 communicating to command server.
- **Data exfiltration risk:** No large outbound file transfers detected, but repetitive small packets suggest potential tunneling.

---

### 4. Plaintext Credentials or Sensitive Data
- HTTP requests to internal site include `Basic Auth` header with base64 username:password. **Action:** Notify user to reset password immediately; enforce HTTPS for admin panel.
- No HTTPS encryption observed on sensitive connections (admin panel accessed over HTTP). **Action:** Enforce TLS/SSL.

---

### 5. Unusual Ports or Protocols
- TCP port 4444 (custom C2 port, not standard service). **Verdict:** Suspicious, investigate further.
- Port 443 (HTTPS) traffic to 203.0.113.5 but with expired certificate. **Verdict:** Likely MITM or C2 over HTTPS.

---

## Recommendations

1. **Immediate Actions:**
   - Isolate host 10.0.1.50 from the network and scan for malware.
   - Block IP 203.0.113.5 at the firewall (egress block).
   - Force password reset for any account that logged in over HTTP.

2. **Investigation Next Steps:**
   - Run forensics on 10.0.1.50 (memory dump, disk image, process list).
   - Check logs on 10.0.1.50 for the time period of PCAP to see what was actually executed.
   - Review proxy logs to see if 203.0.113.5 is already known as malicious.

3. **Long-term:**
   - Deploy endpoint detection and response (EDR) to catch beaconing faster.
   - Enforce HTTPS for all internal services.
   - Implement SSL/TLS certificate pinning for critical services.

---

## Conclusion
Traffic analysis indicates [compromised host / data exfiltration / C2 communication] with high confidence. Immediate isolation and forensic analysis recommended.
