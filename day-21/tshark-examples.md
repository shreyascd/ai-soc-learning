# 10 tshark (CLI Wireshark) Command Examples

tshark is the command-line version of Wireshark — useful for scripting, analyzing PCAP files, or working on servers without a GUI.

## 1. List All Network Interfaces
```bash
tshark -D
```
Shows available interfaces you can capture on.

---

## 2. Capture Traffic from a Specific Interface (Live)
```bash
tshark -i eth0 -c 100
```
Capture 100 packets from eth0 and print to terminal.

---

## 3. Capture and Save to a PCAP File
```bash
tshark -i eth0 -w capture.pcap -c 1000
```
Capture 1000 packets from eth0 and write to `capture.pcap` (can be opened in Wireshark GUI later).

---

## 4. Read and Display a Saved PCAP File
```bash
tshark -r capture.pcap | head -20
```
Read a PCAP file and print first 20 packets.

---

## 5. Filter PCAP for HTTP Traffic Only
```bash
tshark -r capture.pcap -Y "http"
```
Display only HTTP packets from a saved PCAP. (`-Y` = display filter; `-f` = capture filter)

---

## 6. Extract HTTP Requests with URLs
```bash
tshark -r capture.pcap -Y "http.request" -T fields -e http.host -e http.request.uri
```
Show only HTTP requests with hostname and requested URI. (`-T fields` = output as fields; `-e` = export field)

---

## 7. List All DNS Queries and Their Responses
```bash
tshark -r capture.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name
```
Show only DNS queries (requests, not responses) with the domain name being looked up.

---

## 8. Count Packets by Protocol
```bash
tshark -r capture.pcap -q -z io,phs
```
Print statistics of how many packets of each protocol are in the PCAP.

---

## 9. Extract All Conversations (Who Talked to Whom)
```bash
tshark -r capture.pcap -q -z conv,tcp
```
List all TCP conversations (source IP:port ↔ destination IP:port) and byte counts.

---

## 10. Live Capture with Filters (Focused Hunting)
```bash
tshark -i eth0 -f "tcp port 443" -w https_only.pcap
```
Capture ONLY HTTPS traffic (TCP port 443) live and save to file. (`-f` = capture filter; runs before packets are saved.)

---

## Bonus: Extract HTTP Credentials (if sent in plaintext)
```bash
tshark -r capture.pcap -Y "http.authorization" -T fields -e http.authorization
```
Show HTTP Basic Auth headers (plaintext username:password in base64). If this returns anything, that's a security issue.

---

## Pro Tips

1. **Combine filters:** `tshark -r capture.pcap -Y "http and ip.src == 10.0.1.50"` — show only HTTP from a specific IP.
2. **Save filtered subset:** `tshark -r big.pcap -Y "dns" -w dns_only.pcap` — filter and re-save to a smaller file.
3. **Real-time stats:** `tshark -i eth0 -q -z io,phs` — live traffic breakdown by protocol.
4. **Check for beaconing:** `tshark -r capture.pcap -Y "dns" -T fields -e dns.time -e dns.qry.name | sort | uniq -c | sort -rn` — find repetitive DNS queries (C2 beacon).
