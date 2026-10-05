# Set 7 — 16-bit CRC (correct + corrupted) + `dig`

## Q1. 16-bit CRC with error demonstration (Experiment 3)

### Theory
CRC treats the data as a polynomial and divides it (modulo-2, i.e. XOR, no borrows) by a **generator polynomial**.
Generator used: **CRC-16-CCITT `x^16 + x^12 + x^5 + 1`** = `10001000000100001`.

1. **Sender:** `data + 16 zeros` ÷ generator → 16-bit remainder = **CRC**.
2. **Codeword** = `data + CRC` (always exactly divisible by the generator).
3. **Receiver:** codeword ÷ generator → remainder `0` ⇒ accepted, otherwise ⇒ error.

Why a flipped bit is caught: an error pattern E(x) is missed only if the generator divides E(x). A single-bit error
`x^i` is never divisible by a generator with ≥2 terms, so every single-bit error is detected.

### Program explanation
- `client.py` — computes the codeword, then **automatically sends two transmissions**:
  1. the correct codeword → server reports **NO ERROR**;
  2. the same codeword with the middle data bit flipped → server reports **ERROR**.
- `server.py` — loops over connections, prints the received codeword, remainder and verdict.

### How to run
```
python3 server.py
python3 client.py       # enter e.g. 1011001110001111
```
Show both outputs: remainder `0000000000000000` for the clean frame, non-zero remainder for the corrupted frame.

**Exam-critical:** CRC detects but doesn't correct; hardware implements it with an LFSR (shift register + XORs);
CRC-32 is used in Ethernet.

---

## Q2. Command: `dig`

### Theory
`dig` (Domain Information Groper) is the flexible **DNS query tool** on Linux/macOS (package `dnsutils` /
`bind-utils`; Windows needs BIND tools installed). It shows the full DNS response, including the question, answer,
and which server replied.

### Commands
| Task | Command |
|---|---|
| A record | `dig google.com` |
| Short answer | `dig +short google.com` |
| Record type | `dig google.com MX` / `AAAA` / `NS` / `TXT` |
| Specific server | `dig @8.8.8.8 google.com` |
| Reverse lookup | `dig -x 8.8.8.8` |
| Trace delegation | `dig +trace google.com` |

### Sample output (trimmed)
```
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             214     IN      A       142.250.77.14

;; Query time: 12 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Mon Oct 05 09:10:00 IST 2026
;; MSG SIZE  rcvd: 55
```
(Example — your values will differ.)

### Explanation
- **QUESTION SECTION** — what was asked: domain `google.com.`, class `IN` (Internet), type `A`.
- **ANSWER SECTION** columns: name · **TTL** (seconds the answer may be cached) · class · **record type** · **data (IP)**.
- Multiple A lines = multiple IPs (load balancing).
- **SERVER** — the DNS resolver that answered (port 53); **Query time** — latency.
- Flags in header: `qr` response, `rd` recursion desired, `ra` recursion available; `aa` would mean authoritative.
- Status `NOERROR` = success, `NXDOMAIN` = name doesn't exist.
