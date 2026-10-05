"""Set 5 - Iterative TCP Echo Server
Serves ONE client at a time: receive one message, echo it back, close, next client.
"""
import socket

HOST, PORT = "127.0.0.1", 5005

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    print(f"[ECHO SERVER] Listening on {HOST}:{PORT} (Ctrl+C to stop)")
    while True:
        conn, addr = srv.accept()           # blocks until a client arrives
        with conn:
            msg = conn.recv(1024)
            print(f"[ECHO SERVER] {addr} sent: {msg.decode()!r}")
            conn.sendall(msg)               # echo
            print("[ECHO SERVER] Echoed back, closing connection.")
