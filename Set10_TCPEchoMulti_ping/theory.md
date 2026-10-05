# Set 10 — Iterative TCP Echo Server (multiple messages) + `ping`

## Q1. Iterative TCP Echo Server — multiple messages per client (Experiment 6)

### Theory
Socket sequence — **Server:** `socket → bind → listen → accept → recv/send (loop) → close`.
**Client:** `socket → connect → send/recv (loop) → close`.

An **iterative server** serves **one client until it disconnects**, then calls `accept()` again. Other clients queue in
the listen backlog and are served in arrival order. Easy to implement but not scalable (a concurrent server would use
threads/fork/`select`).

`recv()` returning an **empty bytes object** means the peer closed the connection — that is how the server knows to
go back to `accept()`.

### Program explanation
- `server.py` — outer loop `accept()` per client; inner loop `recv()` → echo `sendall()` until the client closes.
  Logs every message and client connect/disconnect.
- `client.py` — one connection, many sequential messages: prompts, sends, prints the echo; type `exit` to leave.

### How to run
```
python3 server.py
python3 client.py        # send: hi / hello / bye, then exit
# open a second client while the first is connected: it waits until the first leaves (demonstrates "iterative")
```
**Exam-critical:** the echoed text equals the sent text; a 2nd simultaneous client is blocked until the 1st disconnects.

---

## Q2. Command: `ping`

### Theory
`ping` sends **ICMP Echo Request** packets and waits for **Echo Reply** to test if a destination is **reachable** and to
measure **RTT**. ICMP is a Network-layer (IP) helper protocol — no ports involved.

### Commands
| OS | Command |
|---|---|
| Linux / macOS | `ping -c 5 <host>` |
| Windows | `ping -n 5 <host>` |
| Local stack test | `ping 127.0.0.1` (or `localhost`) |
| Own server's machine | `ping 127.0.0.1` before running the echo program |

### Determining reachability
1. Replies received (`Reply from…` / `64 bytes from…`) ⇒ **reachable**.
2. `Request timed out` / 100% loss ⇒ host down, route missing, or ICMP blocked by firewall.
3. `Destination host unreachable` ⇒ a router/host reports no route.
4. `Name or service not known` ⇒ DNS failure (try the IP directly to separate DNS from connectivity problems).

### Sample output (Linux)
```
$ ping -c 5 8.8.8.8
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=18.4 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=18.1 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=117 time=19.0 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=117 time=18.3 ms
64 bytes from 8.8.8.8: icmp_seq=5 ttl=117 time=18.2 ms

--- 8.8.8.8 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4006ms
rtt min/avg/max/mdev = 18.1/18.4/19.0/0.3 ms
```
(Example values — record your own.)

### What to record
- **Transmitted:** 5 · **Received:** 5 · **Loss:** 0% = (5−5)/5 × 100.
- **RTT:** min 18.1 ms, avg 18.4 ms, max 19.0 ms (approximate round-trip time).
- **TTL 117:** started at 128 (or 64 + …) and decreased per router hop.
- Large `mdev`/jitter or growing times suggest congestion.
