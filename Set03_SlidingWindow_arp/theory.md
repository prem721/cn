# Set 3 — Sliding Window Protocol + `arp`

## Q1. Sliding Window Protocol (Experiment 4)

### Theory
Stop-and-wait wastes bandwidth: one frame, then idle until the ACK. **Sliding window** lets the
sender transmit up to **N frames (window size)** before needing an ACK, keeping the pipe full.

- Frames carry **sequence numbers**.
- The window `[base, base+N-1]` = frames that may be in flight.
- Each **ACK slides the window** forward.
- Implemented here: **Go-Back-N (GBN)** —
  - Receiver accepts frames **only in order**; out-of-order frames are discarded and the last good ACK is repeated.
  - **Cumulative ACK n** means "all frames up to n received".
  - On **timeout**, sender **goes back** and retransmits from `base` (the first unacked frame).
- (Selective Repeat differs: receiver buffers out-of-order frames and only the lost one is resent.)

### Program explanation
- `server.py` (receiver) — **simulates loss** of frame 3 the first time it arrives (no ACK). Later frames
  4,5,… arrive out of order → discarded, ACK 2 repeated.
- `client.py` (sender) — `base` = oldest unacked, `nxt` = next to send. Fills the window, waits for an ACK
  (2 s timeout); on ACK n sets `base = n+1`; on timeout sets `nxt = base` (retransmit).
- Console prints every send/ACK so the sequence can be shown in the exam.

### How to run
```
python3 server.py [lost_frame]      # default 3
python3 client.py [window] [frames] # default 4, 10
```
Expected flow: frames 0–3 sent, ACK 0,1,2, frame 3 lost → duplicate ACK 2 → TIMEOUT → frames 3.. retransmitted → completes.

**Exam-critical:** GBN max window = 2^m − 1 (sequence bits m); Selective Repeat max = 2^(m−1).
Efficiency of sliding window = N / (1 + 2a), where a = propagation delay / transmission time.

---

## Q2. Command: `arp`

### Theory
**ARP (Address Resolution Protocol)** maps a **32-bit IPv4 address → 48-bit MAC address** on the local
network. A host broadcasts "Who has 192.168.1.1?"; the owner unicasts back its MAC. Results are kept in the
**ARP cache** (entries expire after a short time). Communication within a LAN needs MAC addresses; the IP only
identifies the host logically. For off-subnet destinations the host ARPs for the **gateway's** MAC.

### Commands
| OS | Command |
|---|---|
| Windows / Linux / macOS | `arp -a` (show all entries) |
| Linux modern | `ip neigh` |
| Windows add static | `arp -s 192.168.1.50 aa-bb-cc-dd-ee-ff` |
| Delete entry | `arp -d 192.168.1.50` |

Tip: to fill the cache, `ping` a few LAN hosts first, then run `arp -a`.

### Sample output
```
? (192.168.1.1)   at 3c:52:82:aa:10:01 [ether] on eth0
? (192.168.1.10)  at b8:27:eb:12:34:56 [ether] on eth0
? (192.168.1.34)  at 08:00:27:9d:ab:cd [ether] on eth0
```
(Windows format: `Internet Address  Physical Address  Type` with `dynamic`/`static`.)

### Explanation
- Each row = **IP ↔ MAC binding** for a device on the same subnet.
- `192.168.1.1` is typically the router/gateway.
- **dynamic** entries are learned via ARP and time out; **static** are manually added.
- `ff-ff-ff-ff-ff-ff` / `224.x.x.x` entries are broadcast/multicast.
- ARP works only within a broadcast domain; it is not routed.
