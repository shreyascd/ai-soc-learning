# Self-Assessment — Prompt Engineering (End of Phase 2)

**Rating: 6/10**

## 3 Strengths
1. Comfortable structuring prompts with role + context + instruction + output format instead of writing vague one-liners.
2. Know when to reach for few-shot vs zero-shot depending on whether the task needs a specific format.
3. Can build a reusable template with variables instead of rewriting a prompt from scratch each time.

## 3 Things to Improve
1. Haven't yet handled multi-alert/correlated scenarios — only single-alert triage so far.
2. Need more practice on failure modes — deliberately trying to break a prompt to see where it gives inconsistent or wrong answers.
3. Haven't measured prompts against a real dataset of alerts yet — everything so far is example-based, not tested at volume.

## Goal for Next 20 Days
Move from "writing good individual prompts" to "chaining prompts into a workflow" (Phase 3 / AI Loop Engineering) — starting with a simple multi-step pipeline where one prompt's output feeds into the next, so triage, investigation, and reporting can happen as a connected loop instead of one-off prompts.
