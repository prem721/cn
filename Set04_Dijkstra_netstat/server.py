"""Set 4 - Dijkstra's Shortest Path : SERVER
Receives a weighted (undirected) graph as JSON, runs Dijkstra, returns path + distance.
"""
import heapq
import json
import socket

HOST, PORT = "127.0.0.1", 5004


def dijkstra(n, edges, src, dst):
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))           # undirected
    dist = [float("inf")] * n
    prev = [None] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    if dist[dst] == float("inf"):
        return None, None
    path, cur = [], dst
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return path[::-1], dist[dst]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(5)
    print(f"[SERVER] Dijkstra server on {HOST}:{PORT}")
    while True:
        conn, addr = srv.accept()
        with conn:
            req = json.loads(conn.makefile("r").readline())
            print(f"\n[SERVER] Graph from {addr}: n={req['n']}, edges={req['edges']}")
            print(f"[SERVER] Source={req['src']}  Destination={req['dst']}")
            path, d = dijkstra(req["n"], req["edges"], req["src"], req["dst"])
            if path is None:
                resp = {"ok": False, "msg": "No path exists"}
            else:
                resp = {"ok": True, "path": path, "distance": d}
            print("[SERVER] Result:", resp)
            conn.sendall((json.dumps(resp) + "\n").encode())
