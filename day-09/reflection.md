# Day 9 – Reflection

- Learned why a SIEM exists in the first place — it's not just a tool, it's a solution to the problem of logs being scattered across too many machines to check manually.
- The pipeline (collect → normalize → correlate → alert → review) makes more sense as a flow now, especially why normalization has to happen before correlation can work at all.
- Got a clearer picture of the different SIEM options out there — free/open-source (Wazuh, Security Onion, ELK) vs commercial (Splunk, QRadar) — and roughly when each gets used.
- What was confusing: exactly how correlation rules are written/tuned in practice — the concept makes sense, but the actual rule-writing process still feels abstract without hands-on tool access yet.
- What I'd do differently: get a free Wazuh or Security Onion instance running soon so the pipeline stops being theoretical and I can see real correlation rules firing.
- Next step: push everything for today to GitHub repo under day-09/.
