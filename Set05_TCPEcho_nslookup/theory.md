# Set 5 — Iterative TCP Echo Server + `nslookup`

## Q1. Iterative TCP Echo Server (Experiment 6)

### Theory
**TCP** is connection-oriented and reliable. Server-side socket call sequence:
`socket() → bind() → listen() → accept() → recv()/send() → close()`.
Client side: `socket() → connect() → send()/recv() → close()`.

An **iterative server** handles **one client at a time**: while it serves client A, client B waits in the
`listen` backlog. (A *concurrent* server would fork/thread per client.) Simple, but a slow client blocks the rest.

An **echo server** simply sends back whatever it receives — classic test of connectivity and socket code.

### Program explanation
- `server.py` — binds `127.0.0.1:5005`, loops forever: `accept()`, `recv()` one message, `sendall()` it back, close,
  then accept the next client. `SO_REUSEADDR` avoids "address already in use" after restart.
- `client.py` — connects, sends the typed message, prints what the server echoed.

### How to run
```
python3 server.py
python3 client.py       # type: hello CN lab
```
Output: `Echoed from server: hello CN lab`.

**Exam-critical:** `listen(n)` n = backlog queue length; `accept()` returns a *new* socket for that client;
TCP is a byte stream (no message boundaries) so for large messages loop on `recv()`.

---

## Q2. Command: `nslookup`

### Theory
**DNS** translates domain names to IP addresses (and back). `nslookup` queries a DNS server directly and shows the
answer. **Forward lookup:** name → IP (A/AAAA record). **Reverse lookup:** IP → name (PTR record, in `in-addr.arpa`).

### Commands
| Task | Command |
|---|---|
| Forward lookup | `nslookup google.com` |
| Reverse lookup | `nslookup 8.8.8.8` |
| Specific record type | `nslookup -type=MX gmail.com` |
| Use specific DNS server | `nslookup google.com 8.8.8.8` |

Available on Windows, Linux (package `dnsutils`/`bind-utils`) and macOS.

### Sample output
```
> nslookup google.com
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
Name:   google.com
Address: 142.250.77.14

> nslookup 8.8.8.8
8.8.8.8.in-addr.arpa    name = dns.google.
```
(Examples — real IPs may differ.)

### Explanation
- **Server / Address `#53`** — the DNS resolver used (often your router); DNS uses port 53.
- **Non-authoritative answer** — came from a cache, not the domain's own authoritative server.
- **Name / Address** — the queried domain and its A record (IPv4); several addresses = load balancing.
- **Reverse lookup** returns the PTR name; may say `NXDOMAIN` if none is configured.
