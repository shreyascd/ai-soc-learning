# 5 Common AI Loop Failures

**1. Infinite loops**
What it looks like: Agent keeps calling the same tool or repeating the same action forever, never reaching a stopping condition.
Why it happens: No max-iteration limit set, or the stopping condition is never reached because the model keeps deciding it needs more information.
How to fix: Always set `ToolCallLimitMiddleware` or `ModelCallLimitMiddleware` to force an exit after N iterations. Example: `ToolCallLimitMiddleware(run_limit=10)`.

**2. Hallucinated tool arguments**
What it looks like: Agent calls a tool with plausible-sounding but completely made-up arguments (e.g. invents an IP that doesn't exist, or a filename it never saw).
Why it happens: The prompt doesn't clearly require the model to *get* values from tools before using them; the model guesses instead.
How to fix: Explicitly instruct in the system prompt: "Do not invent values. Always retrieve required values from tools before using them. If you don't have a value, say so."

**3. Wrong tool choice**
What it looks like: Agent picks a tool that technically runs but doesn't actually help answer the question — e.g. searching logs when it should check IP reputation.
Why it happens: Tool descriptions are vague or overlapping; the model doesn't understand which tool solves which problem.
How to fix: Write narrow, specific tool descriptions. Example: bad: `search(query) - search for data`, good: `search_logs(query, time_range) - find security log entries in SIEM by event text and time window`.

**4. Context overflow / losing memory mid-loop**
What it looks like: Early steps in the reasoning are forgotten; the agent repeats steps it already did or contradicts earlier conclusions.
Why it happens: The conversation history grows larger than the context window; older steps fall out of view.
How to fix: Use middleware like `SummarizationMiddleware` to compress old history, or pass a checkpointer for persistent state that doesn't rely on context alone.

**5. Bad output format**
What it looks like: Agent returns an answer but in the wrong format (free text instead of structured JSON, or too verbose when concise was requested).
Why it happens: No structured output schema specified; the model formats the final answer however it wants.
How to fix: Use structured output with Pydantic models or a `ResponseSchema` middleware to enforce the exact format needed before returning.
