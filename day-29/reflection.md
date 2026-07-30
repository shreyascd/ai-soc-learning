# Day 29 – Reflection: Detection vs Hunting

**The paradox:**
Detection is passive: "Alert if this pattern matches."
Hunting is active: "Let me find this pattern even if no alert exists."

Mature SOCs do both. Detection catches the low-hanging fruit (known attacks). Hunting finds novel attacks (things the detection rules don't cover yet).

**Why hunting matters:**
An attacker's first goal is to avoid triggering alerts. So they use novel techniques, obfuscated code, slow movements (1 login per hour over weeks instead of 45 in 5 minutes). Detection rules catch the obvious. Hunting finds the subtle.

**Why 29 days got you here:**
- Days 1-27 taught you to defend reactively (build rules, respond to alerts).
- Days 28-29 teach you to defend proactively (hunt, anticipate, find threats first).

**What a mature analyst does:**
Spends 70% of time on reactively handling alerts (triage, response).
Spends 30% of time on proactive hunting (finding new threats).

You can now do both. Most junior analysts can only do the first.

**The next level (optional, after 31 days):**
- Deeper forensics (memory dumps, disk imaging)
- Red team exercises (offensive security)
- Threat modeling (what does this application need to protect against?)
- Career specialization (analyst → threat hunter → reverse engineer → security architect)

But the foundation is solid. You understand SOC, you can code, you can detect, you can hunt, you can automate, and you can use AI to be faster. That's the beginning of a strong career in security.
