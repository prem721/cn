"""Set 2 - 16-bit CRC : SERVER (verifier)
Generator: CRC-16-CCITT  x^16 + x^12 + x^5 + 1  -> 10001000000100001
"""
import socket

HOST, PORT = "127.0.0.1", 5002
POLY = "10001000000100001"          # 17 bits


def crc_remainder(bits: str, poly: str = POLY) -> str:
    """Modulo-2 long division. Returns the last 16 bits (remainder)."""
    r = list(bits)
    for i in range(len(bits) - (len(poly) - 1)):
        if r[i] == "1":
            for j in range(len(poly)):
                r[i + j] = "0" if r[i + j] == poly[j] else "1"
    return "".join(r[-(len(poly) - 1):])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(5)
    print(f"[SERVER] CRC-16 verifier on {HOST}:{PORT}")
    while True:
        conn, addr = srv.accept()
        with conn:
            code = conn.makefile("r").readline().strip()
            rem = crc_remainder(code)
            print(f"\n[SERVER] Codeword received : {code}")
            print(f"[SERVER] Remainder         : {rem}")
            if int(rem, 2) == 0:
                msg = "NO ERROR detected (remainder = 0)"
            else:
                msg = "ERROR detected (remainder != 0)"
            print("[SERVER]", msg)
            conn.sendall((msg + "\n").encode())
