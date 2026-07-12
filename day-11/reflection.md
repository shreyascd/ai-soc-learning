# Day 11 – Reflection

**When a loop clearly beats a single prompt:**
1. Multi-step alert investigation, where the first answer needs to be checked against actual log data before a final verdict can be trusted — a single prompt can't fetch and re-check new information mid-answer.
2. Iterative report writing, where a draft gets critiqued and rewritten until it hits a quality bar — a single prompt only ever gives you the first attempt.

**When a loop is overkill:**
1. Simple factual questions like "what port does DNS use" — looping adds no value since there's nothing to check or improve.
2. Quick one-off classifications with obvious answers — spending 3 extra steps critiquing an already-correct simple answer just wastes time for no quality gain.
