# Chain-of-Thought (CoT) Notes

**Definition:** Chain-of-Thought prompting asks the model to reason through a problem step by step instead of jumping straight to a final answer. This makes its reasoning visible and usually more accurate on tasks with multiple logical steps.

**The "let's think step by step" trick:** Simply adding this phrase nudges the model to break the problem down instead of pattern-matching to a quick guess. It works because it shifts the model into a slower, more deliberate generation process, surfacing intermediate reasoning that also gives you a chance to catch mistakes early.

**Example 1:**
"A user's account had 5 failed logins, then 1 successful login, all within 2 minutes, from 2 different countries. Let's think step by step about whether this is a compromised account."

**Example 2:**
"This log shows 200 files renamed with a '.locked' extension in 30 seconds. Let's think step by step about what type of attack this is and what should happen next."

**When it helps:** Multi-step reasoning, math, correlating multiple log events, root-cause analysis — anything with more than one logical hop.

**When it doesn't help:** Simple lookups or single-fact answers (e.g. "What port does HTTPS use?") — adding CoT just adds unnecessary length with no accuracy gain.
