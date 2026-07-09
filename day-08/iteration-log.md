# Iteration Log — Improving 3 Weak Prompts

### Prompt 3
**Before:** "Make this better."
**After:** "Rewrite this incident summary to be more concise, max 3 sentences, keeping the root cause and resolution."
**What changed and why:** Added a specific task (rewrite), a length limit, and exactly what content must be preserved — removes all ambiguity about what "better" means.

### Prompt 7
**Before:** "Is this suspicious?"
**After:** "Is this login pattern suspicious? Reason step by step through timing, location, and account history, then give a Yes/No verdict with 1-sentence justification."
**What changed and why:** Added the specific factors to reason about and required a structured step-by-step answer plus a clear final verdict, instead of a vague open question.

### Prompt 9
**Before:** "Classify this alert."
**After:** "Classify this alert as True Positive / False Positive, and explain your reasoning in 1 sentence."
**What changed and why:** Defined the exact category options and required a short justification, so the answer is consistent and usable directly in a ticket instead of open-ended.
