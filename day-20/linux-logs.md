# 5 Important Linux Log Files for SOC Analysis

## 1. /var/log/auth.log (or /var/log/secure on RHEL/CentOS)
**What it records:** Authentication events — successful/failed logins, sudo usage, SSH attempts, password changes.
**Why it matters:** Brute-force attacks, privilege escalation, unauthorized access attempts.
**Example line:** 
```
Jul 21 02:14:23 server sshd[1234]: Failed password for root from 203.0.113.5 port 52341 ssh2
```
**What to look for:**
- Many "Failed password" lines from the same IP → brute-force.
- "sudo: user : TTY=..." → who used sudo and when.
- "New user created" messages → new accounts (may be unauthorized).

---

## 2. /var/log/syslog (or /var/log/messages on RHEL)
**What it records:** System-wide messages from kernel, daemons, and programs. Broad catch-all.
**Why it matters:** System errors, service crashes, cron job output, disk space warnings.
**Example line:**
```
Jul 21 03:45:12 server kernel: [1234567.890123] Out of memory: Kill process sshd (1234) score 120 or sacrifice child
```
**What to look for:**
- "Out of memory" / "Killed process" → denial of service or resource exhaustion.
- Service restart loops → service crashing repeatedly.
- Cron job failures → scheduled tasks not running.

---

## 3. /var/log/audit/audit.log
**What it records:** Detailed audit trail from auditd — system calls, file access, user actions at the kernel level.
**Why it matters:** Deep visibility into what processes/users did; required for compliance (PCI-DSS, HIPAA).
**Example line:**
```
type=EXECVE msg=audit(1626857112.234:5678): argc=2 a0="/bin/bash" a1="-c" a2="rm -rf /var/www/html"
```
**What to look for:**
- Unusual commands executed as root or service accounts.
- File deletion patterns.
- System call anomalies.

---

## 4. /var/log/audit/auditlog (alternative: systemd journal via journalctl)
**What it records (via journalctl):** All systemd services' output, kernel messages, and application logs in one structured stream.
**Why it matters:** Centralized, structured logging makes parsing and searching easier; replaces syslog in modern Linux.
**Example line:**
```
-- Logs begin at Mon 2026-07-21 00:00:01 IST. --
Jul 21 02:14:23 server sshd[1234]: Failed password for root from 203.0.113.5 port 52341 ssh2
```
**What to look for:**
- Same patterns as syslog + auth.log, but in unified format.
- Use `journalctl -u sshd` to follow a specific service.

---

## 5. /var/www/apache2/access.log (or /var/log/apache2/access.log, /var/log/nginx/access.log)
**What it records:** HTTP/HTTPS requests to the web server — IP, method (GET/POST), URL, response code, user agent.
**Why it matters:** Web attack detection (SQL injection, path traversal, command injection), DDoS patterns, unauthorized access.
**Example line:**
```
203.0.113.5 - - [21/Jul/2026:02:14:23 +0530] "GET /admin.php HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
```
**What to look for:**
- 403/404 errors from single IP → scanning for weak/default endpoints.
- Requests with special characters (%27, %20, ../../../) → SQL injection or path traversal attempts.
- POST requests to /admin or /config → unauthorized admin panel access attempts.
- High volume of requests from one IP in short time → DDoS.
