# Set 9 — Distance Vector Routing + `tftp`

## Q1. Distance Vector Routing Algorithm (Experiment 5)

### Theory
Each router keeps a **distance vector**: best-known cost to every destination plus the **next hop**. Routers exchange
vectors **only with direct neighbours** and update using the **Bellman-Ford equation**:

`D_x(y) = min over neighbours v { c(x,v) + D_v(y) }`

Repeat until no vector changes → the network has **converged**. Used by **RIP**. Weakness: **count-to-infinity**
(slow convergence after link failure) — mitigated by split horizon, poison reverse, hop limit 15 in RIP.
Contrast with link-state (Dijkstra, Set 4): every router learns the whole topology.

### Program explanation
- `client.py` — sends the cost matrix as JSON (`9999` = no direct link, `0` on the diagonal). Built-in 4-node sample:
  ```
  0: [0, 2, INF, 1]   1: [2, 0, 3, INF]   2: [INF, 3, 0, 4]   3: [1, INF, 4, 0]
  ```
- `server.py` — `distance_vector()` initialises each node's table from direct costs, then repeatedly lets every node
  relax each destination through each neighbour (`cost[i][k] + dist[k][j]`) until a full round changes nothing.
  Prints a routing table (**Dest | Cost | Next hop**) for every node and sends it back.

### How to run
```
python3 server.py
python3 client.py       # 'y' for sample topology
```
Check: node 0 → node 2 should cost 5 (0→1→2 = 2+3) vs 5 via 0→3→2 (1+4); node 1 → node 3 costs 3 via node 0.

**Exam-critical:** convergence takes at most (N−1) rounds; DV messages go to neighbours only, periodically
(RIP: every 30 s).

---

## Q2. Command: `tftp`

### Theory
**TFTP (Trivial File Transfer Protocol)** — a minimal file-transfer protocol over **UDP port 69**.
- **No authentication, no directory listing**, no encryption; only `get` (read) and `put` (write).
- Uses simple **lock-step (stop-and-wait)** with 512-byte blocks and ACKs; reliability is implemented by TFTP itself
  because UDP is unreliable.
- Used for booting diskless devices, loading router/switch firmware and configs (PXE).

### Difference from FTP
| | FTP | TFTP |
|---|---|---|
| Transport | TCP (ports 20/21) | UDP (port 69) |
| Authentication | Username/password | None |
| Directory listing | Yes (`ls`, `cd`) | No |
| Reliability | From TCP | Own ACK/timeout, stop-and-wait |
| Complexity / size | Heavy, many commands | Tiny, `get`/`put` only |
| Use | General file transfer | Boot/config of network devices |

### Commands
```
tftp <server-ip>                 # interactive (Linux/macOS)
tftp> binary
tftp> get test.txt
tftp> put local.txt
tftp> quit

tftp -i <server-ip> GET test.txt # Windows one-liner (-i = binary)
```
Windows needs *TFTP Client* enabled in Windows Features. Linux: `sudo apt install tftp-hpa`.

### Lab server setup (if none is provided)
```
sudo apt install tftpd-hpa           # serves /srv/tftp
echo "hello tftp" | sudo tee /srv/tftp/test.txt
sudo chmod 666 /srv/tftp/test.txt
```
or `pip install tftpy` then `python3 -c "import tftpy; tftpy.TftpServer('.').listen('0.0.0.0',6969)"` and `tftp 127.0.0.1 6969`.
Use only a server you are authorised to access.

### Sample session
```
$ tftp 127.0.0.1
tftp> binary
tftp> get test.txt
Received 12 bytes in 0.0 seconds
tftp> quit
```
### Explanation
`get` sends a Read Request (RRQ) to port 69; server replies from a new port with DATA block 1; client ACKs each block;
a block shorter than 512 bytes ends the transfer. There is no `ls` because TFTP defines no listing operation —
you must know the file name.
