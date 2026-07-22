# Day 21 – Reflection: Wireshark & Packet Analysis

**Why packet capture is different from logs:**

Logs tell you what the system thinks happened ("user X logged in"). Packets show what actually happened on the wire — every byte sent and received. A compromised machine might suppress its own logs or change them, but it can't lie about the packets it sends (unless it has kernel-level control, which is already "game over").

**When you need Wireshark:**
1. **Hunting for C2 communication** — beaconing patterns are obvious in packet timing, even if encrypted. Every 30 seconds, same size packet to the same IP = suspicious, even if you can't decrypt it.
2. **Finding exfiltration** — large transfers to unexpected IPs stand out in packet stats.
3. **Spotting plaintext credentials** — HTTP Basic Auth, unencrypted FTP logins, config files with passwords — all visible in packets.
4. **Reverse-engineering malware C2** — follow TCP stream to see the exact messages sent between malware and attacker.

**When logs are enough:**
- Authentication auditing (who logged in when) — logs are cleaner.
- Summarizing what a user accessed over days (file access patterns) — packet-level detail would be overwhelming.
- Compliance reporting (action trails) — logs are structured for audit.

**In practice, you use both:**
- Logs say "something weird happened on this host at 2:14 AM."
- Packet capture on that host during that timeframe shows exactly what was sent/received.
- Together they tell the full story.

**Why plain-text HTTP is still a security risk:**
Even though HTTPS is standard now, many internal services (admin panels, monitoring dashboards) still run on HTTP. If that traffic passes through an attacker-controlled network (or a compromised internal switch), credentials and sensitive data are visible in plaintext. A PCAP would immediately expose it.
