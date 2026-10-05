"""Set 1 - Bit Stuffing : SENDER / CLIENT
Run after the server:  python3 client.py
Rule: after five consecutive 1s insert a 0. Frame = FLAG + stuffed data + FLAG.
"""
import socket

HOST, PORT = "127.0.0.1", 5001
FLAG = "01111110"


def stuff(bits: str) -> str:
    out, ones = [], 0
    for b in bits:
        out.append(b)
        ones = ones + 1 if b == "1" else 0
        if ones == 5:
            out.append("0")
            ones = 0
    return "".join(out)


data = input("Enter data bit stream (e.g. 0111111011111100): ").strip()
if not data or set(data) - {"0", "1"}:
    raise SystemExit("Please enter only 0s and 1s.")

stuffed = stuff(data)
frame = FLAG + stuffed + FLAG
print(f"Original data : {data}")
print(f"Stuffed data  : {stuffed}")
print(f"Frame sent    : {frame}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall((frame + "\n").encode())
    print("Server reply  :", s.makefile("r").readline().strip())
