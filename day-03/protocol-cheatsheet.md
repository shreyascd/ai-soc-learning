# Protocol Cheat Sheet

| Protocol | Port | TCP/UDP | What it does | Security risk if exposed |
|----------|------|---------|--------------|---------------------------|
| HTTP | 80 | TCP | Serves unencrypted web traffic | Data sent in plaintext, easily intercepted |
| HTTPS | 443 | TCP | Serves encrypted web traffic | Misconfigured TLS/certs can still leak data |
| SSH | 22 | TCP | Secure remote shell access | Brute-force login attempts, weak passwords |
| DNS | 53 | UDP/TCP | Resolves domain names to IPs | DNS spoofing, cache poisoning, amplification attacks |
| FTP | 21 | TCP | File transfer | Sends credentials/data in plaintext |
| RDP | 3389 | TCP | Remote desktop access | Common ransomware entry point if exposed to internet |
