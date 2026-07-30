# Threat Hunting Queries - Ready to Run

Copy these queries into your SIEM (Splunk SPL, Elastic KQL, etc). Adapt field names to match your data.

---

## Hunt 1: Unauthorized Admin Account Creation

**Splunk SPL:**
```spl
index=main EventID=4720 OR EventID=4722 OR EventID=4756
| search group_member="Domain Admins" OR group_member="Administrators"
| stats earliest(timestamp) as first_seen, latest(timestamp) as last_seen, 
         count by user_created, created_by_user, host
| where created_by_user != "admin" AND created_by_user != "it_team"
| sort - first_seen
```

**Purpose:** Find new admin accounts created by non-IT users or outside business hours.

**If you find:** Confirm with IT. If not authorized, isolate host and investigate who created it.

---

## Hunt 2: DNS Beaconing (Repeated Queries to Same Domain)

**Splunk SPL:**
```spl
index=main sourcetype=dns record_type=A
| stats count as query_count by src_ip, dest_domain, _time
| where query_count > 10
| eval time_bucket=_time - ((_time % 300) % 300)  # 5-min buckets
| stats sum(query_count) as total_queries by src_ip, dest_domain, time_bucket
| where total_queries > 5
| sort - total_queries
```

**Purpose:** Find IPs querying the same domain repeatedly (C2 beacon pattern).

**If you find:** Check IP/domain against threat intel. If malicious, investigate machine for malware.

---

## Hunt 3: Large Outbound Data Transfer

**Splunk SPL:**
```spl
index=main sourcetype=firewall dest_ip NOT IN (8.8.8.8, 1.1.1.1, 208.67.222.222)
| where bytes_out > 104857600
| stats sum(bytes_out) as total_bytes, earliest(timestamp) as first_seen
         by src_ip, dest_ip
| where total_bytes > 1073741824
| sort - total_bytes
```

**Purpose:** Find internal IPs sending >1GB to external IPs (possible data theft).

**If you find:** Was this expected? Check with user/admin. If not authorized, escalate.

---

## Hunt 4: Process Injection via Suspicious Parent-Child Relationship

**Splunk SPL (Windows):**
```spl
index=main EventID=4688
| search (parent_process=explorer.exe AND (child_process=powershell.exe OR child_process=cmd.exe))
         OR (parent_process=svchost.exe AND child_process NOT IN (svchost.exe, conhost.exe))
         OR (parent_process=services.exe AND child_process=powershell.exe)
| stats count by host, parent_process, child_process, Command_Line
| where count < 10
| sort host
```

**Purpose:** Find unusual process hierarchies (parent spawning unexpected child).

**If you find:** Check command line for obfuscation. If suspicious, check file hash against VirusTotal.

---

## Hunt 5: Scheduled Task Persistence

**Splunk SPL (Windows):**
```spl
index=main (EventID=4698 OR source=*schtasks*)
| regex Task_Name="\\(System32|Temp)" OR regex Task_Action="(powershell|cmd|vbscript)"
| stats count by host, Task_Name, Task_Action, Creator
| where count < 10
| sort host
```

**Purpose:** Find scheduled tasks that look suspicious (system tasks in unusual locations, running scripts).

**If you find:** Confirm with IT. If not known, check what the task does and disable if malicious.

---

## Hunt 6: Failed Login Followed by Success

**Splunk SPL:**
```spl
index=main EventID=4625 OR EventID=4624
| stats values(EventID) as events, count as attempt_count by user, src_ip, host, _time
| where (4625 in events AND 4624 in events) AND attempt_count > 10
| table _time, user, src_ip, host, attempt_count
| sort - attempt_count
```

**Purpose:** Find brute-force attacks that succeeded (many failures then 1 success).

**If you find:** Force password reset, check for lateral movement from that account.

---

## Hunt 7: Unusual File Access on Sensitive Share

**Splunk SPL:**
```spl
index=main sourcetype=file_access path=*\Finance\* OR path=*\HR\* 
| where action="read" OR action="access"
| stats count as access_count, earliest(timestamp) as first_access by user, host, path
| where access_count > 100
| sort - access_count
```

**Purpose:** Find users accessing sensitive files they shouldn't (data theft indicator).

**If you find:** Check user's role. If access not justified, audit what files were accessed.

---

## Tips for Running These Hunts

1. **Adapt field names:** Your SIEM may use different field names. Check your field reference.
2. **Test on small time window first:** Run on last 24h, then expand to 30d if no issues.
3. **Whitelist known good activity:** Exclude known good IPs, users, processes (IT maintenance, automation).
4. **Set alert if hunt finds results:** Convert hunt to automated alert once validated.
5. **Document baseline:** Know what normal looks like before hunting for anomalies.
