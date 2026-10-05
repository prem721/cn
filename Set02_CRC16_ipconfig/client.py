"""Set 2 - 16-bit CRC : CLIENT (generator)
Appends 16 zeros, divides by the generator, appends the remainder (CRC) to the data.
"""
import socket

HOST, PORT = "127.0.0.1", 5002
POLY = "10001000000100001"          # x^16 + x^12 + x^5 + 1


def crc_remainder(bits: str, poly: str = POLY) -> str:
    r = list(bits)
    for i in range(len(bits) - (len(poly) - 1)):
        if r[i] == "1":
            for j in range(len(poly)):
                r[i + j] = "0" if r[i + j] == poly[j] else "1"
    return "".join(r[-(len(poly) - 1):])


data = input("Enter data bits (e.g. 110101101011): ").strip()
if not data or set(data) - {"0", "1"}:
    raise SystemExit("Please enter only 0s and 1s.")

crc = crc_remainder(data + "0" * 16)
codeword = data + crc
print(f"Data      : {data}")
print(f"Generator : {POLY}")
print(f"CRC (16)  : {crc}")
print(f"Codeword  : {codeword}")

if input("Introduce an error (flip one bit)? (y/n): ").strip().lower() == "y":
    pos = int(input(f"Bit position to flip (0-{len(codeword) - 1}): "))
    flipped = "1" if codeword[pos] == "0" else "0"
    codeword = codeword[:pos] + flipped + codeword[pos + 1:]
    print(f"Corrupted : {codeword}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall((codeword + "\n").encode())
    print("Server reply:", s.makefile("r").readline().strip())
