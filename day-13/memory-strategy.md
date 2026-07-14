# Memory Strategy — Long SOC Chat

## The Problem
A SOC analyst using an AI assistant across a full shift generates a long conversation — dozens of alerts discussed, investigated, and resolved. Left unmanaged, this conversation eventually exceeds the model's context window, causing early alerts (and their resolutions) to silently drop out of memory.

## Strategy

**1. Summarize old alerts, don't keep them raw.**
Once an alert has been triaged and closed, replace its full back-and-forth discussion with a 1-2 line summary: `"Alert #14 (2:03 PM): Failed logins from new geo — confirmed True Positive, account disabled."` This keeps the outcome available for reference without the full token cost of the original investigation.

**2. Keep recent alerts raw (sliding window).**
The last 5-10 alerts stay in full detail, unsummarized, since these are most likely to still need follow-up, cross-referencing, or a change in verdict as new information comes in.

**3. Drop context only after confirming resolution.**
An alert's full detail should only be summarized/dropped once it's marked resolved — actively open or escalated alerts stay raw regardless of age, since losing detail on something still being investigated is far more costly than losing detail on something already closed.

**4. Re-inject a running "shift summary" at the top.**
Instead of relying purely on chat history, maintain a short running summary block (updated each time an alert closes) that's re-sent with each new prompt — e.g. `"Shift so far: 12 alerts reviewed, 3 True Positives (IDs 4, 9, 14), 9 False Positives."` This keeps shift-level context available even after individual alert details have been dropped.

## When to Drop Old Context Entirely
Once an alert is resolved AND has been summarized into the running shift summary, its raw detail can be fully dropped from active context — the summary preserves what matters (verdict + why), and the full transcript isn't needed unless someone later needs to audit that specific decision (in which case it should be pulled from logs/tickets, not kept live in the AI's memory).
