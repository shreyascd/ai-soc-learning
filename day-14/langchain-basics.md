# LangChain Basics

**What is LangChain:** A framework for building applications on top of LLMs, instead of calling a raw API endpoint every time. Rather than manually managing prompt formatting, parsing responses, and wiring multiple calls together by hand, LangChain gives standard building blocks for these patterns — which matters once an app needs more than a single one-off API call, like chaining steps together or plugging in tools.

**What is a chain:** A chain is a defined sequence of steps that data flows through — typically prompt → LLM → output parser — where each step's output becomes the next step's input. Instead of writing that plumbing by hand every time, a chain packages it into one reusable, callable object.

**LLM wrapper:** A standardized interface LangChain provides around a specific model provider's API (OpenAI, Anthropic, etc.), so the rest of your code can call `.invoke()` the same way regardless of which underlying model you're actually using — swapping providers doesn't require rewriting your whole app.

**Prompt template:** A reusable prompt with `{variable}` placeholders, so the actual text sent to the model is generated dynamically at runtime rather than hardcoded — this is the same variable-based template concept from Day 7, now used as a formal building block inside a chain.

**Output parser:** A component that takes the model's raw text response and converts it into a more usable structure — plain string, JSON object, or a specific typed format — so the rest of your program doesn't have to manually clean up or parse free-form text.
