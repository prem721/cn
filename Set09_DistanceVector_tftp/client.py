"""Set 9 - Distance Vector Routing : CLIENT
Sends the network cost matrix (use 9999 for 'no direct link') to the server.
"""
import json
import socket

HOST, PORT = "127.0.0.1", 5009

SAMPLE = [
    [0, 2, 9999, 1],
    [2, 0, 3, 9999],
    [9999, 3, 0, 4],
    [1, 9999, 4, 0],
]

if input("Use sample topology (4 nodes)? (y/n): ").strip().lower() == "y":
    matrix = SAMPLE
else:
    n = int(input("Number of nodes: "))
    print("Enter each row of the cost matrix (use 9999 for no link):")
    matrix = [list(map(int, input(f"Row {i}: ").split())) for i in range(n)]

print("Sending matrix:")
for r in matrix:
    print("  ", r)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall((json.dumps({"matrix": matrix}) + "\n").encode())
    s.shutdown(socket.SHUT_WR)
    out = b""
    while True:
        d = s.recv(4096)
        if not d:
            break
        out += d
print("\n--- Server result ---")
print(out.decode())
