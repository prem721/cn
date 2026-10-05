# Set 4 — Dijkstra's Shortest Path + `netstat`

## Q1. Dijkstra's Algorithm (Experiment 5)

### Theory
Dijkstra finds the **least-cost path from one source to all vertices** in a graph with
**non-negative edge weights** — the basis of **link-state routing (OSPF)**.

Algorithm:
1. `dist[src] = 0`, all others `∞`; `prev[]` empty.
2. Repeatedly pick the unvisited vertex `u` with the smallest `dist`.
3. **Relax** each neighbour `v`: if `dist[u] + w(u,v) < dist[v]`, update `dist[v]` and `prev[v] = u`.
4. Stop when all reachable vertices are done. Rebuild the path by following `prev[]` back from the destination.

Complexity: `O(V²)` with an array, `O((V+E) log V)` with a priority queue (heap) — used here (`heapq`).

### Program explanation
- `client.py` — takes number of vertices, edges `(u v w)`, source and destination (or uses a built-in sample),
  packs them as JSON and sends it to the server.
- `server.py` — builds an adjacency list (undirected), runs Dijkstra, returns JSON `{path, distance}`.

Sample graph: edges 0-1:7, 0-2:9, 0-5:14, 1-2:10, 1-3:15, 2-3:11, 2-5:2, 3-4:6, 4-5:9.
Source 0 → destination 4 gives path `0 -> 2 -> 5 -> 4`, distance **20**.

### How to run
```
python3 server.py
python3 client.py       # answer 'y' for the sample graph
```
**Exam-critical:** Dijkstra fails with negative weights (use Bellman-Ford). Greedy choice = closest
unvisited node. Link-state = every router knows the full topology; Distance Vector = only neighbours' vectors.

---

## Q2. Command: `netstat`

### Theory
`netstat` (network statistics) lists **active connections, listening ports, routing table and interface
statistics**. Useful for checking which services are running and who is connected.

### Commands
| OS | Command |
|---|---|
| Windows | `netstat -an` (all, numeric), `netstat -ano` (adds PID), `netstat -r` (routes) |
| Linux | `netstat -tuln` (TCP/UDP listening, numeric), `netstat -an`, `netstat -r` |
| Linux modern | `ss -tuln` |

Flags: `-a` all, `-n` numeric, `-t` TCP, `-u` UDP, `-l` listening, `-p` program/PID, `-o` owner PID (Windows).
Tip: run `python3 server.py` first, then `netstat -an | grep 5004` to see your own socket in `LISTEN`.

### Sample output
```
Proto  Local Address        Foreign Address      State
tcp    0.0.0.0:22           0.0.0.0:*            LISTEN
tcp    127.0.0.1:5004       0.0.0.0:*            LISTEN
tcp    192.168.1.25:51514   142.250.77.14:443    ESTABLISHED
tcp    192.168.1.25:51520   151.101.1.69:443     TIME_WAIT
udp    0.0.0.0:68           0.0.0.0:*
```
(Examples — use your real output.)

### Explanation
- **Proto** — TCP or UDP.
- **Local Address:Port** — this host's endpoint (`0.0.0.0` = all interfaces).
- **Foreign Address:Port** — remote endpoint (`*` for listening sockets).
- **State:** `LISTEN` waiting for connections; `ESTABLISHED` active connection; `TIME_WAIT` closed, waiting
  2·MSL; `SYN_SENT`/`SYN_RECV` handshake in progress; `CLOSE_WAIT` remote closed, local app hasn't.
- Port 22 = SSH, 80 = HTTP, 443 = HTTPS.
