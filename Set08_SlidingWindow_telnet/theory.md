# Set 8 — Sliding Window Protocol (window 3) + `telnet`

## Q1. Sliding Window Protocol (Experiment 4)

### Theory
The sender may have up to **N unacknowledged frames** outstanding (the **window**). Each ACK slides the window forward,
so the link stays busy instead of idling as in stop-and-wait. This implementation is **Go-Back-N**:

- Receiver window = 1 → frames accepted **only in order**.
- **Cumulative ACK n** = everything up to frame n received.
- An out-of-order frame is **discarded** and the last in-order ACK is repeated (a duplicate ACK = "I'm still waiting for n+1").
- Sender timer expires → **retransmit from the first unacknowledged frame** (`base`) onwards.

### Program explanation
Same engine as Set 3, but different defaults to show a different run: **window = 3, 12 frames, frame 4 lost once**.
- `server.py [lost_frame]` — acknowledges good frames, drops frame 4 the first time (simulated loss), re-ACKs 3
  for later out-of-order frames, finishes on `END`.
- `client.py [window] [frames]` — prints each frame sent with the current window `[base..end]`, every ACK received, and
  the `TIMEOUT -> retransmitting from frame X` event. This printed sequence is the "frame transmission and acknowledgement
  sequence" the question asks for.

### How to run
```
python3 server.py            # or: python3 server.py 6   (lose frame 6 instead)
python3 client.py            # or: python3 client.py 4 15
```
Expected: frames 0–2, ACK 0..2, window slides, frame 4 lost → duplicate ACK 3 → timeout → resend 4,5,6 → done.

**Exam-critical:** with m-bit sequence numbers, GBN window ≤ 2^m − 1. Utilization = N/(1+2a). Larger window helps until
it fills the bandwidth-delay product.

---

## Q2. Command: `telnet`

### Theory
`telnet` opens a **TCP connection to any host:port** and gives a raw text session (originally a remote-login protocol on
port **23**, unencrypted — replaced by SSH). Today it's mainly a **port connectivity tester**.

Note: modern Windows has telnet *disabled* — enable via *Turn Windows features on or off → Telnet Client*, or run
`dism /online /Online /Enable-Feature /FeatureName:TelnetClient`. Linux: `sudo apt install telnet`. (Alternative: `nc -vz host port`.)

### Commands
| Task | Command |
|---|---|
| Test a port | `telnet <host> <port>` e.g. `telnet google.com 80` |
| Test your own server | start `python3 server.py`, then `telnet 127.0.0.1 5008` |
| Exit | `Ctrl + ]` then `quit` |

### Sample outputs
**Success**
```
$ telnet 127.0.0.1 5008
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
```
**Failure**
```
$ telnet 127.0.0.1 9999
Trying 127.0.0.1...
telnet: Unable to connect to remote host: Connection refused
```
### Explanation
- **Connected** ⇒ the TCP three-way handshake (SYN, SYN-ACK, ACK) completed: host reachable and a service is listening.
- **Connection refused** ⇒ host reachable but **no process listening** on that port (host replied with RST).
- **Timed out / hangs** ⇒ packets dropped: firewall filtering, host down, or wrong route.
- **Unknown host / could not resolve** ⇒ DNS failure.
- Because telnet is plaintext, never send passwords over it.
