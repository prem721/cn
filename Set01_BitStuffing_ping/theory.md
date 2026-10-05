# Set 1 — Bit Stuffing + `ping`

## Q1. Bit Stuffing (Experiment 2 — Data Link Framing)

### Theory
The data link layer must tell the receiver where a frame begins and ends. A common
bit-oriented method (HDLC) marks both ends with a **FLAG = `01111110`**. If the user data
itself contains `01111110`, the receiver would see a false end-of-frame. **Bit stuffing**
solves this:

- **Sender rule:** after **five consecutive 1s** in the data, insert a **0**.
- **Receiver rule:** after five consecutive 1s, the next bit is a stuffed 0 — **remove it**.
- Frame = `FLAG + stuffed data + FLAG`.

So the pattern `111111` can never occur inside the payload, and FLAG (six 1s) is unique.

### Example
| Step | Bits |
|---|---|
| Original data | `0111111011111100` |
| Stuffed data | `011111010111110100` (a `0` inserted after each run of five 1s) |
| Frame sent | `01111110` `011111010111110100` `01111110` |

(Run the program to see the exact output — it is computed, not hand-written.)

### Program explanation
- `client.py` — reads a bit string, `stuff()` walks the bits counting consecutive 1s and
  appends `0` when the count hits 5, builds the frame and sends it over TCP (newline-terminated).
- `server.py` — receives the frame, checks FLAGs at both ends, strips them, `destuff()` skips
  the bit after every run of five 1s, prints and returns the original data.

### How to run (two terminals)
```
python3 server.py
python3 client.py        # enter e.g. 0111111011111100
```
**Exam-critical:** counter resets to 0 after inserting the stuffed bit; stuffing happens even if
the sixth bit would have been 0 anyway (receiver can't know otherwise).

---

## Q2. Command: `ping`

### Theory
`ping` tests **reachability** and **latency** to a host using **ICMP Echo Request / Echo Reply**
messages (Network layer, ICMP rides inside IP). It reports the destination IP, **TTL**, and the
**round-trip time (RTT)** per packet, then a summary of packet loss and min/avg/max RTT.

### Commands
| OS | Command |
|---|---|
| Linux / macOS | `ping -c 4 google.com` (`-c` = count; without it Linux pings forever, Ctrl+C to stop) |
| Windows | `ping google.com` (sends 4 by default) or `ping -n 4 google.com` |
| Loopback test | `ping 127.0.0.1` |

### Sample output (Linux)
```
PING google.com (142.250.77.14) 56(84) bytes of data.
64 bytes from 142.250.77.14: icmp_seq=1 ttl=117 time=14.2 ms
64 bytes from 142.250.77.14: icmp_seq=2 ttl=117 time=13.8 ms
64 bytes from 142.250.77.14: icmp_seq=3 ttl=117 time=14.0 ms
64 bytes from 142.250.77.14: icmp_seq=4 ttl=117 time=13.9 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 13.8/14.0/14.2/0.2 ms
```
(Your IPs and times will differ — paste your own output in the exam.)

### Explanation of the output
- **IP address:** `142.250.77.14` — DNS resolved the name before pinging.
- **bytes:** 64 = 56 data bytes + 8 byte ICMP header.
- **icmp_seq:** sequence number; gaps indicate lost packets.
- **ttl:** remaining hop limit when reply arrived (initial value minus routers crossed).
- **time:** RTT — time from sending request to receiving reply.
- **Packet loss:** `(transmitted − received) / transmitted × 100`. 0% = healthy link.
- **Request timed out / 100% loss:** host down, firewall blocking ICMP, or no route.
