# Mock Function Call — Simulated Walkthrough

## Step 1: User Question
"Has IP 203.0.113.5 been flagged as malicious before?"

## Step 2: Model's JSON Response
```json
{
  "tool_call": "check_ip_reputation",
  "parameters": {
    "ip": "203.0.113.5"
  }
}
```
The model recognizes it can't know this from training data alone — reputation data changes constantly — so instead of guessing, it requests the tool.

## Step 3: Your Code's Response
```json
{
  "ip": "203.0.113.5",
  "reputation": "malicious",
  "categories": ["botnet", "spam"],
  "last_reported": "2026-07-10"
}
```
Your code actually calls the real IP reputation service/API and returns the structured result back to the model.

## Step 4: Model's Final Answer
"Yes — 203.0.113.5 has been flagged as malicious. It's associated with botnet and spam activity, with the most recent report on 2026-07-10. Recommend blocking this IP and checking if any internal systems have communicated with it recently."

## Observation
The model never actually "knew" the reputation itself — it knew *when* to ask, then used the real returned data to write an accurate, grounded final answer instead of guessing.
