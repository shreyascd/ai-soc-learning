# 10 Critical Windows Event IDs — SOC Analyst's Must-Know

**Event ID 4624 (Successful Logon)**
What it means: A user successfully logged in.
Why it matters: Baseline for normal activity; spikes can mean brute-force success. Watch for logons from unusual IPs or times.
Logon Types: 2 (interactive), 3 (network), 10 (remote desktop), 7 (unlock).

**Event ID 4625 (Failed Logon)**
What it means: A login attempt failed (wrong password, account doesn't exist, etc.).
Why it matters: 10+ from same IP in short time = brute-force attempt. Escalate immediately.
Common causes: Typos, credential stuffing, account locked out.

**Event ID 4688 (Process Creation)**
What it means: A new process started (PowerShell, cmd, executable, etc.).
Why it matters: Spot suspicious processes (encoded PowerShell, rare executables). Base64-encoded commands are a red flag.
Use for: Tracking lateral movement, command injection, malware execution.

**Event ID 4648 (Explicit Credentials Use)**
What it means: A user logged in using a username/password (not the current session's credentials).
Why it matters: Can indicate credential use for lateral movement or privilege escalation. admin using a second admin account = suspicious.
Watch for: Service accounts running under different credentials.

**Event ID 4720 (User Account Created)**
What it means: A new user account was created.
Why it matters: Unauthorized accounts = backdoor or privilege escalation. Should match change tickets.
Action: If unexpected, disable immediately and investigate who created it.

**Event ID 4722 (User Account Enabled)**
What it means: A disabled account was re-enabled.
Why it matters: Attacker re-enabling an old dormant account for persistence. Check if this was authorized.

**Event ID 4738 (User Account Changed)**
What it means: A user account's properties were modified (group membership, description, etc.).
Why it matters: Adding a user to Domain Admins = privilege escalation. Check for unauthorized group additions.

**Event ID 4768 (Kerberos Ticket Requested)**
What it means: A user requested a Kerberos authentication ticket.
Why it matters: Volume spikes can indicate pass-the-hash or ticket-granting-ticket attacks. Multiple failed 4768 events = brute-force over network.

**Event ID 4769 (Kerberos Ticket Used)**
What it means: A Kerberos service ticket was used.
Why it matters: If a rare or high-privilege service (e.g., Database) is accessed, it's worth investigating.

**Event ID 4756 (User Added to Group)**
What it means: A user was added to a security group (Local Admins, Domain Admins, etc.).
Why it matters: Privilege escalation red flag. Unauthorized additions = account compromise or attacker activity.
Action: Check if this matches a scheduled change request; if not, investigate immediately.
