# Day 15 – Reflection

**RAG is better when:** the underlying data changes frequently (new logs, new tickets, new docs daily), the data is large or private, and cost/speed of updating matters — RAG only requires re-embedding new/changed documents, which is cheap and fast compared to retraining a model.

**Fine-tuning is better when:** the goal is changing the model's behavior, tone, or reasoning style itself rather than giving it new facts — for example, teaching it a very specific output format or domain-specific reasoning pattern that no amount of retrieved context alone would fix. Fine-tuning also makes more sense when the underlying data is relatively stable/small and updated rarely, since the upfront training cost only pays off if it doesn't need to be repeated often.

In short: RAG handles "the model doesn't know this fact yet" cheaply and dynamically; fine-tuning handles "the model doesn't behave the way I need it to," at a higher upfront cost that's worth it only when the data/behavior isn't constantly changing.
