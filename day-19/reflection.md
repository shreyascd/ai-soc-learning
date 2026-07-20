# Day 19 – Reflection

**How to spot a brute-force attack in Windows logs:**

The clearest signal is Event ID 4625 (failed logon) — if the same IP is trying the same account 20+ times in 2 minutes, it's definitely brute-force. But the sophistication is that an attacker can also try many different accounts from the same IP (credential stuffing), so "10 failed logins, 10 different users, same IP" is also brute-force — just a different variant.

**Why Windows logs are harder to analyze than you'd think:**

Event ID 4624 (successful logon) is noisy — every user logging in generates one, so on a medium-sized network, thousands per day. Finding the signal (attacker's successful login) in that noise requires either:
1. Knowing what "normal" looks like for that user (baseline), so abnormal stands out.
2. Correlating 4624 with suspicious follow-up events (new admin account, file access to sensitive shares).
3. Combining 4624 with source IP reputation data (known botnet IP, etc.).

A SIEM with correlation rules does this automatically. Without one, a SOC analyst would have to manually review thousands of successful logins to find one anomaly — which is why manually hunting through Windows logs doesn't scale beyond a tiny network.
