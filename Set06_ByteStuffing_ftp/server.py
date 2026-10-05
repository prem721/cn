"""Set 6 - Byte (Character) Stuffing : SERVER
FLAG = '~' (0x7E), ESC = '}' (0x7D).  Frame = FLAG + stuffed payload + FLAG.
De-stuffing rule: an ESC means "take the next byte literally".
"""
import socket

HOST, PORT = "127.0.0.1", 5006
FLAG, ESC = 0x7E, 0x7D


def destuff(frame: bytes) -> bytes:
    if len(frame) < 2 or frame[0] != FLAG:
        raise ValueError("frame must start with FLAG")
    out, i = bytearray(), 1
    while i < len(frame):
        c = frame[i]
        if c == ESC:                # escaped byte -> copy next one literally
            out.append(frame[i + 1])
            i += 2
        elif c == FLAG:             # unescaped FLAG = end of frame
            return bytes(out)
        else:
            out.append(c)
            i += 1
    raise ValueError("closing FLAG missing")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(5)
    print(f"[SERVER] Byte-stuffing receiver on {HOST}:{PORT}")
    while True:
        conn, addr = srv.accept()
        with conn:
            chunks = []
            while True:                     # client half-closes after sending
                d = conn.recv(1024)
                if not d:
                    break
                chunks.append(d)
            frame = b"".join(chunks)
            print(f"\n[SERVER] Frame received : {frame.decode(errors='replace')}")
            try:
                data = destuff(frame)
                print(f"[SERVER] De-stuffed data: {data.decode()}")
                conn.sendall(b"OK: " + data)
            except ValueError as e:
                print("[SERVER] Error:", e)
                conn.sendall(f"ERROR: {e}".encode())
