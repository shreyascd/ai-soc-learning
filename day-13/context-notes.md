# Context Window Notes

**What a context window is:** The total amount of text — measured in tokens, not words or characters — that a model can "see" at once in a single request. This includes everything: the system prompt, the conversation history, and the model's own response being generated. Once the total goes past the limit, the oldest content has to be dropped or summarized, because the model literally cannot process more than its window allows.

**Token limits for 3 popular models (approximate):**
- GPT-4 — ~128k tokens
- Claude — ~200k tokens
- Gemini — ~1M tokens

**Why long conversations break down without memory management:**
As a conversation grows, every new message still has to include the full prior history for the model to "remember" earlier context. Once that history exceeds the context window, the oldest messages start getting silently dropped or truncated — the model isn't "forgetting" out of confusion, it literally no longer has that text in front of it. This causes it to repeat earlier questions, contradict something it said 50 messages ago, or lose track of the actual goal of a long task, unless the conversation is deliberately managed (via summarization or a sliding window) to keep the most relevant information inside the limit.
