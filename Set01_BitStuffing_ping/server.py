"""Set 1 - Bit Stuffing : RECEIVER / SERVER
Run first:  python3 server.py
Receives a stuffed frame, strips the FLAGs, de-stuffs and prints the original data.
"""
import socket

HOST, PORT = "127.0.0.1", 5001
FLAG = "01111110"


def destuff(bits: str) -> str:
    """Remove the '0' that follows every run of five consecutive 1s."""
    out, ones, i = [], 0, 0
    while i < len(bits):
        b = bits[i]
        out.append(b)
        ones = ones + 1 if b == "1" else 0
        if ones == 5:      # next bit is a stuffed 0 -> skip it
            i += 1
            ones = 0
        i += 1
    return "".join(out)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    print(f"[SERVER] Listening on {HOST}:{PORT} ...")
    while True:
        conn, addr = srv.accept()
        with conn:
            frame = conn.makefile("r").readline().strip()
            print(f"\n[SERVER] Connection from {addr}")
            print(f"[SERVER] Received frame   : {frame}")
            if not (frame.startswith(FLAG) and frame.endswith(FLAG)):
                print("[SERVER] Invalid frame (FLAG missing)")
                conn.sendall(b"ERROR: bad frame\n")
                continue
            stuffed = frame[len(FLAG):-len(FLAG)]
            data = destuff(stuffed)
            print(f"[SERVER] Stuffed payload  : {stuffed}")
            print(f"[SERVER] De-stuffed (orig): {data}")
            conn.sendall(f"OK original data = {data}\n".encode())
