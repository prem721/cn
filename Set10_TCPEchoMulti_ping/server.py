"""Set 10 - Iterative TCP Echo Server (multiple messages per client)
Serves one client until it disconnects, and only then accepts the next client.
"""
import socket

HOST, PORT = "127.0.0.1", 5010

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    print(f"[ECHO SERVER] Listening on {HOST}:{PORT} (Ctrl+C to stop)")
    while True:
        conn, addr = srv.accept()
        print(f"\n[ECHO SERVER] Client connected: {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:                # client closed
                    break
                print(f"[ECHO SERVER] Received: {data.decode()!r} -> echoing")
                conn.sendall(data)
        print(f"[ECHO SERVER] Client {addr} disconnected. Waiting for next client...")
