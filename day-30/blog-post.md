# What I Learned Building an AI SOC Assistant in 30 Days

Thirty days ago I could write a decent prompt. I couldn't read a Windows Event Log, write a detection rule, or explain the NIST incident response lifecycle. Today I can do all three — and I built an AI assistant that ties them together. Here's what actually happened.

## The Three Tracks

The plan was structured around three skill tracks running in parallel: prompt engineering, AI loop engineering, and SOC analyst fundamentals.

**Prompt engineering (Days 4-10)** started with the basics — zero-shot vs few-shot, chain-of-thought, templates — and ended with a tested, reusable prompt library. The big shift wasn't learning tricks; it was learning that a good prompt is a piece of infrastructure. Write it once, reuse it everywhere.

**AI loop engineering (Days 11-17)** is where prompts became systems. ReAct loops, tool calling, memory management, testing agents like you'd test regular code. The lesson that stuck: an agent is only as good as its stopping conditions and its tool descriptions. Get those wrong and you get infinite loops or hallucinated tool calls.

**SOC fundamentals (Days 18-27)** was the deep end. SIEM architecture, Windows and Linux log analysis, Wireshark, malware static analysis, the NIST incident response lifecycle, threat intelligence, detection rules in Sigma and YARA, and Python automation for repetitive SOC tasks. This is where most of the actual learning-curve pain lived — logs are unforgiving, and there's no shortcut to knowing what Event ID 4688 means.

## The Capstone

Day 28 combined everything: an AI SOC Assistant that takes a raw alert, extracts indicators, calls tools to check IP reputation and search known IOCs, and returns a structured severity assessment with a recommendation. Building it made obvious how much each track depended on the others. Without the SOC knowledge, the assistant would confidently hallucinate severity levels. Without the loop engineering, it could only do one lookup at a time. Without the prompt engineering, its output would be unusable prose instead of something an analyst could act on in seconds.

A real example: an alert comes in about repeated failed logins from one IP. The assistant extracts the IP, checks its abuse score, cross-references it against a known-IOC list, finds a match to a known botnet C2, and returns: "CRITICAL — confirmed C2 communication, isolate host immediately." That whole chain took me three days to build properly. It takes the assistant under a second to run, and it would take a human analyst ten minutes per alert.

## What Went Wrong Along the Way

I trusted early LLM output without verification and got a hallucinated IP reputation score that didn't match reality — that's what pushed me to build a mandatory verification step before any action is recommended. I also underestimated how much manual log-reading you need before hunting for anomalies actually works; you can't spot "unusual" until you've internalized "normal."

## Advice If You're Starting This

Don't skip the fundamentals to get to the AI part faster — the AI is only useful once you know what a good detection or a false positive actually looks like. Treat AI as an advisor that drafts and suggests, never as the thing that gets the final say on isolating a machine or resetting an account. And ship daily, even when what you ship is just notes — the compounding effect of 30 small pushes beats a handful of heroic ones.

## What's Next

The foundation is done. Next is specialization — going deep on threat hunting, detection engineering, or building more of these AI-assisted SOC tools — instead of staying broad. The repo for this whole journey is public if you want to fork it and run your own version.
