"""Set 7 - 16-bit CRC : CLIENT
Sends TWO transmissions automatically:
  1) the correct codeword
  2) the same codeword with one bit deliberately flipped
"""
import socket

HOST, PORT = "127.0.0.1", 5007
POLY = "10001000000100001"          # x^16 + x^12 + x^5 + 1


def crc_remainder(bits: str, poly: str = POLY) -> str:
    r = list(bits)
    for i in range(len(bits) - (len(poly) - 1)):
        if r[i] == "1":
            for j in range(len(poly)):
                r[i + j] = "0" if r[i + j] == poly[j] else "1"
    return "".join(r[-(len(poly) - 1):])


def send(codeword: str) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall((codeword + "\n").encode())
        print("   Server reply:", s.makefile("r").readline().strip())


data = input("Enter data bits (e.g. 1011001110001111): ").strip()
if not data or set(data) - {"0", "1"}:
    raise SystemExit("Please enter only 0s and 1s.")

crc = crc_remainder(data + "0" * 16)
codeword = data + crc
print(f"Data     : {data}\nCRC (16) : {crc}\nCodeword : {codeword}")

print("\n--- Transmission 1: CORRECT codeword ---")
send(codeword)

pos = len(data) // 2                       # flip a bit in the middle of the data
bad = codeword[:pos] + ("1" if codeword[pos] == "0" else "0") + codeword[pos + 1:]
print(f"\n--- Transmission 2: CORRUPTED codeword (bit {pos} flipped) ---")
print(f"   Sent: {bad}")
send(bad)
