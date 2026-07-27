#!/usr/bin/env python3
"""
Mini SOAR - Simplified Security Orchestration
Chain: Parse auth.log → Extract failed login IPs → Check reputation → Generate report
Usage: python3 mini-soar.py /var/log/auth.log
"""

import sys
import re
import csv
import requests
import os
from collections import defaultdict
from datetime import datetime


def parse_auth_log(logfile: str) -> dict:
    """Parse auth.log and extract failed login IPs."""
    failed_logins = defaultdict(list)
    
    try:
        with open(logfile, 'r') as f:
            for line in f:
                # Match "Failed password for [user] from [IP]"
                match = re.search(r'Failed password for (\w+) from (\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    user = match.group(1)
                    ip = match.group(2)
                    failed_logins[ip].append({"user": user, "line": line.strip()})
    except FileNotFoundError:
        print(f"Error: File not found: {logfile}")
        sys.exit(1)
    
    return failed_logins


def check_ip_abuse_batch(ips: list) -> dict:
    """Check multiple IPs against AbuseIPDB."""
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    if not api_key:
        print("Warning: ABUSEIPDB_API_KEY not set. Using mock data.")
        # Mock data for demo
        return {
            ip: {"score": 45 + (i % 50), "reports": i % 20}
            for i, ip in enumerate(ips)
        }
    
    results = {}
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": api_key, "Accept": "application/json"}
    
    for ip in ips:
        try:
            response = requests.get(url, params={"ipAddress": ip}, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results[ip] = {
                    "score": data["data"].get("abuseConfidenceScore", 0),
                    "reports": data["data"].get("totalReports", 0),
                }
            else:
                results[ip] = {"score": "N/A", "reports": "N/A"}
        except:
            results[ip] = {"score": "ERROR", "reports": "ERROR"}
    
    return results


def generate_report(failed_logins: dict, ip_scores: dict) -> str:
    """Generate text report."""
    report = []
    report.append("=" * 80)
    report.append("INCIDENT RESPONSE REPORT - Failed Login Analysis")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 80)
    report.append("")
    
    # Summary
    report.append(f"[Summary]")
    report.append(f"Total unique IPs with failed logins: {len(failed_logins)}")
    high_risk = sum(1 for ip in failed_logins if ip_scores.get(ip, {}).get("score", 0) > 75)
    medium_risk = sum(1 for ip in failed_logins if 25 < ip_scores.get(ip, {}).get("score", 0) <= 75)
    report.append(f"High risk IPs (>75): {high_risk}")
    report.append(f"Medium risk IPs (25-75): {medium_risk}")
    report.append("")
    
    # Details
    report.append("[Details]")
    for ip in sorted(failed_logins.keys(), key=lambda x: ip_scores.get(x, {}).get("score", 0), reverse=True):
        score = ip_scores.get(ip, {}).get("score", "N/A")
        reports = ip_scores.get(ip, {}).get("reports", "N/A")
        attempts = len(failed_logins[ip])
        
        risk_label = ""
        if isinstance(score, int) and score > 75:
            risk_label = "🚨 HIGH RISK"
        elif isinstance(score, int) and score > 25:
            risk_label = "⚠️  MEDIUM RISK"
        else:
            risk_label = "✓ LOW RISK"
        
        report.append(f"\nIP: {ip} {risk_label}")
        report.append(f"  Abuse Score: {score}")
        report.append(f"  Total AbuseIPDB Reports: {reports}")
        report.append(f"  Failed Logins in this log: {attempts}")
        report.append(f"  Targeted users: {', '.join(set(f['user'] for f in failed_logins[ip]))}")
    
    report.append("")
    report.append("=" * 80)
    report.append("End of Report")
    report.append("=" * 80)
    
    return "\n".join(report)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 mini-soar.py <auth_log_file>")
        print("Example: python3 mini-soar.py /var/log/auth.log")
        sys.exit(1)
    
    logfile = sys.argv[1]
    
    print("[Mini SOAR Workflow]")
    print("Step 1: Parse auth.log...")
    failed_logins = parse_auth_log(logfile)
    print(f"  ✓ Found {len(failed_logins)} unique IPs with failed logins")
    
    print("Step 2: Check IP reputation...")
    ip_scores = check_ip_abuse_batch(list(failed_logins.keys()))
    print(f"  ✓ Checked {len(ip_scores)} IPs")
    
    print("Step 3: Generate report...")
    report = generate_report(failed_logins, ip_scores)
    print(report)
    
    # Save report
    report_file = f"day26_incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()
