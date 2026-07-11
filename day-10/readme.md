# SOC Alert Triage Prompt — README

## What It Does
Takes a raw security alert description and returns a step-by-step reasoning trace plus a final True Positive / False Positive verdict, formatted consistently enough to drop directly into a ticket.

## How to Use
1. Copy the prompt template from `polished-prompt.md`.
2. Replace `{alert_text}` with your actual alert description.
3. Paste into ChatGPT or Claude.
4. Read the "Reasoning" line to sanity-check the logic, then use the "Verdict" line for your ticket.

## Inputs
A single alert description in plain English — can come from a SIEM alert, EDR flag, or manual observation. Works best with concrete details: what happened, when, and any relevant account/system context.

## Outputs
Two fields:
- **Reasoning** – 1-2 sentences explaining the logic behind the verdict.
- **Verdict** – either `True Positive` or `False Positive`.

## Limitations
- Only outputs a binary verdict — doesn't yet handle "needs more investigation" as a third option.
- Quality depends heavily on how much detail is in the alert text; vague alerts ("something weird happened") will get vague reasoning back.
- Not a replacement for analyst judgment — meant to speed up first-pass triage, not replace escalation review for ambiguous or high-severity cases.
- Hasn't been tested yet on multi-alert/correlated incidents (multiple related alerts describing one bigger attack).
