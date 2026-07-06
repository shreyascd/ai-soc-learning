# Prompt Patterns Explained

## Zero-shot Prompting
**Definition:** Ask the model directly with no examples given — just the instruction.
**When to use:** Simple, common tasks the model already understands well.
**Example:** "Summarize this log entry in one sentence."

## Few-shot Prompting
**Definition:** Give 2-3 examples of input/output pairs before asking your actual question, so the model learns the pattern you want.
**When to use:** Tasks with a specific format, style, or edge cases that zero-shot gets wrong.
**Example:**
```
Log: "Failed login from 10.0.0.5" → Category: Authentication
Log: "Port scan detected on 443" → Category: Reconnaissance
Log: "Malware signature match on file.exe" → Category: Malware
Log: "Multiple failed logins from 192.168.1.10" → Category:
```

## Role-based Prompting
**Definition:** Tell the model to act as a specific persona ("You are a SOC analyst...") before giving the task, so responses match that expert's tone and depth.
**When to use:** When you want domain-specific reasoning or a particular voice/expertise level.
**Example:** "You are a SOC analyst. Explain to a junior teammate why this alert is a false positive."

## Common Mistakes
- Vague instructions ("make it better") instead of specific asks.
- Missing context — model doesn't know your environment/goal.
- Not specifying output format — leads to inconsistent, hard-to-use responses.
