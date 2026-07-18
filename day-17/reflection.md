# Day 17 – Reflection

Testing an AI loop is harder than testing regular code because:
1. **Non-determinism** – the same input can produce different outputs depending on LLM temperature, model version, or even just randomness in sampling. An answer that was right yesterday might be reformatted today.
2. **Tool interdependence** – the agent's correctness depends not just on the model's reasoning, but on the tools working correctly. If a tool breaks, the whole loop fails, even if the model's logic is sound.
3. **Emergent failures** – failures that don't happen on simple inputs can emerge on complex multi-step queries, so a comprehensive test suite needs edge cases and multi-step scenarios, not just happy paths.

**How to track if an agent is "working":**
- Does it reach a stopping condition (vs infinite loop)?
- Does it call the right tool(s) in a sensible order?
- Does the final answer actually answer the question, or is it off-topic?
- How many steps/tool calls did it take (is it efficient)?

Logging every step is the only way to debug this — without seeing which tool was called, what the result was, and how the model reacted, you're flying blind when something goes wrong.
