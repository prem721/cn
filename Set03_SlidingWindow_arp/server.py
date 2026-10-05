"""Set 3 - Sliding Window (Go-Back-N) : RECEIVER / SERVER
Usage: python3 server.py [DROP_SEQ]      (default: frame 3 is "lost" once)
The receiver accepts frames only in order, sends cumulative ACKs and silently
drops frame DROP_SEQ the first time it arrives to simulate a lost frame.
"""
import socket
import sys

HOST, PORT = "127.0.0.1", 5003
DROP_SEQ = int(sys.argv[1]) if len(sys.argv) > 1 else 3

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    print(f"[RECEIVER] Listening on {HOST}:{PORT} (will lose frame {DROP_SEQ} once)")
    conn, addr = srv.accept()
    print(f"[RECEIVER] Sender connected: {addr}\n")
    expected, dropped = 0, False
    with conn:
        for line in conn.makefile("r"):
            line = line.strip()
            if line == "END":
                print("\n[RECEIVER] Transfer complete.")
                break
            seq_s, data = line.split("|", 1)
            seq = int(seq_s)
            if seq == DROP_SEQ and not dropped:
                dropped = True
                print(f"[RECEIVER] Frame {seq} ({data}) LOST (simulated) - no ACK")
                continue
            if seq == expected:
                print(f"[RECEIVER] Frame {seq} ({data}) accepted  -> send ACK {seq}")
                conn.sendall(f"ACK|{seq}\n".encode())
                expected += 1
            else:
                print(f"[RECEIVER] Frame {seq} out of order (expected {expected}) "
                      f"-> discarded, re-ACK {expected - 1}")
                if expected > 0:
                    conn.sendall(f"ACK|{expected - 1}\n".encode())
