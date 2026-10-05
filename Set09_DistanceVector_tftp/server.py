"""Set 9 - Distance Vector Routing : SERVER
Receives the cost matrix (9999 = no direct link), runs the Bellman-Ford based
Distance Vector exchange until no table changes, returns routing tables.
"""
import json
import socket

HOST, PORT = "127.0.0.1", 5009
INF = 9999


def distance_vector(cost):
    n = len(cost)
    dist = [row[:] for row in cost]
    nxt = [[j if cost[i][j] < INF else None for j in range(n)] for i in range(n)]
    log = []
    rnd = 0
    changed = True
    while changed:
        changed = False
        rnd += 1
        for i in range(n):
            for k in range(n):                       # k = neighbour of i
                if i == k or cost[i][k] >= INF:
                    continue
                for j in range(n):
                    if cost[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = cost[i][k] + dist[k][j]
                        nxt[i][j] = k                # go via neighbour k
                        changed = True
        log.append((rnd, [r[:] for r in dist]))
    return dist, nxt, log


def fmt(v):
    return "INF" if v >= INF else str(v)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(5)
    print(f"[SERVER] Distance Vector server on {HOST}:{PORT}")
    while True:
        conn, addr = srv.accept()
        with conn:
            req = json.loads(conn.makefile("r").readline())
            cost = req["matrix"]
            print(f"\n[SERVER] Cost matrix from {addr}: {cost}")
            dist, nxt, log = distance_vector(cost)
            lines = [f"Converged after {len(log)} round(s) (last round = no change)\n"]
            for i in range(len(cost)):
                lines.append(f"Routing table of node {i}:")
                lines.append("  Dest | Cost | Next hop")
                for j in range(len(cost)):
                    hop = "-" if i == j else (str(nxt[i][j]) if nxt[i][j] is not None else "-")
                    lines.append(f"   {j}   | {fmt(dist[i][j]):>4} | {hop}")
                lines.append("")
            out = "\n".join(lines)
            print(out)
            conn.sendall(out.encode())
