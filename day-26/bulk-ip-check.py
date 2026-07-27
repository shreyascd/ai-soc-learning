#!/usr/bin/env python3
"""
Bulk IP Reputation Checker
Reads IPs from file, checks each against AbuseIPDB (free tier), outputs CSV report.
Requires: pip install requests
Set: export ABUSEIPDB_API_KEY="your-key"
Usage: python3 bulk-ip-check.py <ip_list_file>
Example: python3 bulk-ip-check.py failed_logins.txt
"""

import sys
import os
import csv
import requests
import time
from datetime import datetime

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"
RATE_LIMIT_DELAY = 1  # 1 second between requests (free tier is limited)


def check_ip_abuse(ip: str) -> dict:
    """Query AbuseIPDB for single IP."""
    if not ABUSEIPDB_API_KEY:
        return {"ip": ip, "error": "API key not set", "score": "N/A", "reports": "N/A"}
    
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90,
    }
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(ABUSEIPDB_URL, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "ip": ip,
                "abuse_score": data["data"].get("abuseConfidenceScore", 0),
                "total_reports": data["data"].get("totalReports", 0),
                "is_whitelisted": data["data"].get("isWhitelisted", False),
                "error": None,
            }
        elif response.status_code == 429:
            return {"ip": ip, "error": "Rate limited", "score": "N/A", "reports": "N/A"}
        else:
            return {"ip": ip, "error": f"HTTP {response.status_code}", "score": "N/A", "reports": "N/A"}
    except Exception as e:
        return {"ip": ip, "error": str(e), "score": "N/A", "reports": "N/A"}


def read_ips_from_file(filepath: str) -> list:
    """Read IPs from file (one per line)."""
    ips = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                ip = line.strip()
                if ip and not ip.startswith("#"):  # Skip empty lines and comments
                    ips.append(ip)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    return ips


def write_csv_report(results: list, output_file: str = "ip_report.csv"):
    """Write results to CSV."""
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["ip", "abuse_score", "total_reports", "is_whitelisted", "error"])
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    print(f"\nReport saved to: {output_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 bulk-ip-check.py <ip_list_file>")
        print("Example: python3 bulk-ip-check.py failed_logins.txt")
        sys.exit(1)
    
    ip_file = sys.argv[1]
    ips = read_ips_from_file(ip_file)
    
    print(f"[Bulk IP Reputation Checker]")
    print(f"Found {len(ips)} IPs to check")
    print(f"Checking each IP (rate-limited to {RATE_LIMIT_DELAY}s/request)...\n")
    
    results = []
    for i, ip in enumerate(ips, 1):
        print(f"[{i}/{len(ips)}] Checking {ip}...", end=' ')
        result = check_ip_abuse(ip)
        results.append(result)
        
        if result["error"]:
            print(f"ERROR: {result['error']}")
        else:
            score = result["abuse_score"]
            if score > 75:
                print(f"🚨 HIGH RISK (score: {score})")
            elif score > 25:
                print(f"⚠️  MEDIUM RISK (score: {score})")
            else:
                print(f"✓ LOW RISK (score: {score})")
        
        time.sleep(RATE_LIMIT_DELAY)
    
    # Summary
    print(f"\n[Summary]")
    high_risk = [r for r in results if isinstance(r.get("abuse_score"), int) and r["abuse_score"] > 75]
    medium_risk = [r for r in results if isinstance(r.get("abuse_score"), int) and 25 < r["abuse_score"] <= 75]
    low_risk = [r for r in results if isinstance(r.get("abuse_score"), int) and r["abuse_score"] <= 25]
    
    print(f"High Risk (>75): {len(high_risk)} IPs")
    print(f"Medium Risk (25-75): {len(medium_risk)} IPs")
    print(f"Low Risk (<25): {len(low_risk)} IPs")
    
    # Write report
    write_csv_report(results, "day26_ip_report.csv")


if __name__ == "__main__":
    main()
