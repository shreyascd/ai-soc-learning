# Day 25 – Reflection: False Positives vs False Negatives

**The core tension:**
A detection rule that catches everything (FN = 0) will also fire constantly on benign activity (high FP). A rule that only fires on confirmed threats (low FP) will miss subtle attacks (high FN).

**Real example:**
Rule: "Alert if PowerShell is executed with -enc flag" (encoding, often used to hide malware commands).

Too strict: Alerts on every encoded command ever, including legitimate admin scripts → 50 alerts/day, analysts ignore them → rule becomes useless.

Too loose: Only alerts if it also modifies registry AND creates new process AND connects to external IP → misses attacker who uses encoded PowerShell without persistence yet → breach happens undetected.

**The solution: Confidence scoring, not binary yes/no**

Instead of "alert or don't alert," score the threat:
- PowerShell with -enc: 30 points (suspicious, but could be legit)
- + Creates new process: +20 points (50 total, medium risk)
- + Contacts external IP: +20 points (70 total, high risk)
- + Modifies registry Run key: +20 points (90 total, critical, isolate immediately)

This lets you alert at different thresholds for different audiences:
- Threshold 50: Notify SOC analyst for triage.
- Threshold 70: Isolate machine and involve IR team.
- Threshold 90: Executive alert, potential breach.

**Why this matters for Day 25:**
Writing detection rules is not about being 100% accurate. It's about being useful. A rule that catches 80% of real attacks with 20% false positives is better than a rule that's 100% accurate but only fires once a month. You need the noise to find the signal.
