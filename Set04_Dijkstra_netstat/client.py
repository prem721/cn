"""Set 4 - Dijkstra's Shortest Path : CLIENT
Sends the weighted graph + source/destination to the server and prints the answer.
"""
import json
import socket

HOST, PORT = "127.0.0.1", 5004

SAMPLE = {
    "n": 6,
    "edges": [[0, 1, 7], [0, 2, 9], [0, 5, 14], [1, 2, 10], [1, 3, 15],
              [2, 3, 11], [2, 5, 2], [3, 4, 6], [4, 5, 9]],
    "src": 0,
    "dst": 4,
}

if input("Use sample graph? (y/n): ").strip().lower() == "y":
    req = SAMPLE
else:
    n = int(input("Number of vertices (labelled 0..n-1): "))
    m = int(input("Number of edges: "))
    edges = []
    for i in range(m):
        u, v, w = map(int, input(f"Edge {i + 1} (u v weight): ").split())
        edges.append([u, v, w])
    src = int(input("Source vertex: "))
    dst = int(input("Destination vertex: "))
    req = {"n": n, "edges": edges, "src": src, "dst": dst}

print("Sending graph:", req)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall((json.dumps(req) + "\n").encode())
    resp = json.loads(s.makefile("r").readline())

if resp["ok"]:
    print("Shortest path     :", " -> ".join(map(str, resp["path"])))
    print("Shortest distance :", resp["distance"])
else:
    print(resp["msg"])
