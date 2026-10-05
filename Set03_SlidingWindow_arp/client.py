"""Set 3 - Sliding Window (Go-Back-N) : SENDER / CLIENT
Usage: python3 client.py [WINDOW_SIZE] [TOTAL_FRAMES]     (defaults: 4, 10)
Sends up to WINDOW_SIZE frames without waiting; slides the window on each ACK;
on timeout retransmits every unacknowledged frame starting from `base`.
"""
import socket
import sys

HOST, PORT = "127.0.0.1", 5003
WINDOW = int(sys.argv[1]) if len(sys.argv) > 1 else 4
TOTAL = int(sys.argv[2]) if len(sys.argv) > 2 else 10
TIMEOUT = 2.0

buf = b""


def recv_line(sock):
    global buf
    while b"\n" not in buf:
        chunk = sock.recv(1024)
        if not chunk:
            raise ConnectionError("receiver closed")
        buf += chunk
    line, buf = buf.split(b"\n", 1)
    return line.decode().strip()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.settimeout(TIMEOUT)
    base = nxt = 0
    print(f"[SENDER] Window={WINDOW}, frames={TOTAL}\n")
    while base < TOTAL:
        while nxt < base + WINDOW and nxt < TOTAL:
            s.sendall(f"{nxt}|DATA{nxt}\n".encode())
            print(f"[SENDER] Sent frame {nxt:2d}   window=[{base}..{min(base + WINDOW - 1, TOTAL - 1)}]")
            nxt += 1
        try:
            ack = int(recv_line(s).split("|")[1])
            print(f"[SENDER] Got  ACK   {ack:2d}")
            if ack + 1 > base:
                base = ack + 1          # slide the window
        except socket.timeout:
            print(f"[SENDER] TIMEOUT -> retransmitting from frame {base} (Go-Back-N)")
            nxt = base
    s.sendall(b"END\n")
    print("\n[SENDER] All frames acknowledged.")
