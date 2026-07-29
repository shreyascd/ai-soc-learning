#!/usr/bin/env python3
"""
AI SOC Assistant - LangChain Agent
Combines prompt engineering + tool use + SOC knowledge into working assistant.
Requires: pip install langchain langchain-anthropic

Usage:
  export ANTHROPIC_API_KEY="your-key"
  export ABUSEIPDB_API_KEY="your-key"
  python3 assistant-skeleton.py
"""

import json
import os
import re
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.tools import tool

# Mock IOC database (in production: load from real threat feed)
KNOWN_IOCS = {
    "203.0.113.5": {"type": "IP", "threat": "Emotet C2", "confidence": 99},
    "malware-beacon.com": {"type": "domain", "threat": "Emotet C2", "confidence": 98},
    "d41d8cd98f00b204e9800998ecf8427e": {"type": "hash", "threat": "Emotet trojan", "confidence": 96},
}

# Mock reputation data
MOCK_IP_SCORES = {
    "203.0.113.5": 85,
    "192.0.2.10": 45,
    "198.51.100.1": 10,
}


@tool
def check_ip_reputation(ip: str) -> dict:
    """Check IP reputation score (0-100, higher = more abuse). Uses mock data."""
    if ip in MOCK_IP_SCORES:
        score = MOCK_IP_SCORES[ip]
        return {
            "ip": ip,
            "abuse_score": score,
            "interpretation": "HIGH RISK" if score > 75 else "MEDIUM RISK" if score > 25 else "LOW RISK"
        }
    return {"ip": ip, "abuse_score": "unknown", "interpretation": "No data"}


@tool
def search_known_iocs(indicator: str) -> dict:
    """Search indicator (IP, domain, hash) in known malware IOC database."""
    indicator_lower = indicator.lower()
    if indicator_lower in KNOWN_IOCS:
        data = KNOWN_IOCS[indicator_lower]
        return {
            "indicator": indicator,
            "found": True,
            "threat": data["threat"],
            "confidence": f"{data['confidence']}%"
        }
    return {"indicator": indicator, "found": False, "threat": None}


def extract_indicators_from_alert(alert_text: str) -> dict:
    """Extract IPs, domains, file hashes from alert text."""
    indicators = {
        "ips": re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', alert_text),
        "domains": re.findall(r'(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?', alert_text.lower()),
        "hashes": re.findall(r'\b[a-f0-9]{32}\b|\b[a-f0-9]{40}\b|\b[a-f0-9]{64}\b', alert_text.lower()),
    }
    return indicators


class SOCAssistant:
    def __init__(self):
        """Initialize the AI SOC Assistant with LangChain agent."""
        self.agent = create_agent(
            model="anthropic:claude-sonnet-4-6",
            tools=[check_ip_reputation, search_known_iocs],
            system_prompt=(
                "You are an AI SOC analyst assistant. When given a security alert:\n"
                "1. Identify the threat type (brute force, malware, C2, etc)\n"
                "2. Extract indicators (IPs, domains, hashes)\n"
                "3. Check reputation and IOC database for each indicator\n"
                "4. Assess severity (CRITICAL/HIGH/MEDIUM/LOW)\n"
                "5. Recommend action (isolate/block/monitor/investigate)\n"
                "Be concise. Prioritize high-confidence threats."
            ),
            middleware=[ModelCallLimitMiddleware(run_limit=10)],
        )
        self.alert_history = []  # Keep last 3 alerts for context
    
    def triage_alert(self, alert_text: str) -> dict:
        """Triage a security alert and return structured assessment."""
        # Extract indicators upfront (faster than LLM extraction)
        indicators = extract_indicators_from_alert(alert_text)
        
        # Build prompt with extracted indicators
        prompt = f"""
Triage this security alert:

{alert_text}

Pre-extracted indicators:
- IPs: {indicators['ips'] or 'none'}
- Domains: {indicators['domains'] or 'none'}
- Hashes: {indicators['hashes'] or 'none'}

For each indicator, check reputation and search IOC database.
Then provide:
1. Severity (CRITICAL/HIGH/MEDIUM/LOW)
2. Assessment (what likely happened)
3. Extracted IOCs with threat info
4. Recommended action
"""
        
        # Run agent
        result = self.agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        
        # Extract final answer
        final_answer = ""
        for msg in result["messages"]:
            if msg.__class__.__name__ == "AIMessage" and msg.content and not getattr(msg, "tool_calls", None):
                final_answer = msg.content
                break
        
        # Store in history (keep last 3)
        self.alert_history.append(alert_text)
        if len(self.alert_history) > 3:
            self.alert_history.pop(0)
        
        return {
            "alert": alert_text,
            "assessment": final_answer,
            "indicators": indicators,
        }
    
    def format_report(self, triage_result: dict) -> str:
        """Format triage result as structured markdown report."""
        report = f"""
## AI SOC Assistant - Alert Triage Report

**Original Alert:**
{triage_result['alert']}

**Extracted Indicators:**
- IPs: {', '.join(triage_result['indicators']['ips']) or 'None'}
- Domains: {', '.join(triage_result['indicators']['domains']) or 'None'}
- Hashes: {', '.join(triage_result['indicators']['hashes']) or 'None'}

**Assessment:**
{triage_result['assessment']}

---
*Generated by AI SOC Assistant (Day 28)*
"""
        return report


def main():
    """Test the assistant on sample alerts."""
    assistant = SOCAssistant()
    
    # Sample alerts to test
    sample_alerts = [
        "Alert: Multiple failed logins for admin from IP 203.0.113.5. 45 attempts in 5 minutes.",
        "Alert: Connection to 192.0.2.10:4444 detected from WORKSTATION-01. Traffic pattern matches C2 beacon.",
        "Alert: File downloaded from email: malware_payload.exe (hash: d41d8cd98f00b204e9800998ecf8427e). VirusTotal: 52/60 detect as trojan.",
    ]
    
    for i, alert in enumerate(sample_alerts, 1):
        print(f"\n{'='*80}")
        print(f"Processing Sample Alert {i}...")
        print(f"{'='*80}")
        
        result = assistant.triage_alert(alert)
        report = assistant.format_report(result)
        print(report)
        
        # Save to file
        with open(f"day28_alert_triage_{i}.md", "w") as f:
            f.write(report)
    
    print(f"\n{'='*80}")
    print("Triage complete. Reports saved to day28_alert_triage_*.md")


if __name__ == "__main__":
    main()
