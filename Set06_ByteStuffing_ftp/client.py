"""Set 6 - Byte (Character) Stuffing : CLIENT
Inserts ESC before every FLAG or ESC byte found in the data, then wraps with FLAGs.
"""
import socket

HOST, PORT = "127.0.0.1", 5006
FLAG, ESC = 0x7E, 0x7D          # '~' and '}'


def stuff(data: bytes) -> bytes:
    out = bytearray([FLAG])
    for b in data:
        if b in (FLAG, ESC):
            out.append(ESC)
        out.append(b)
    out.append(FLAG)
    return bytes(out)


text = input("Enter data (try something containing ~ and }, e.g. A~B}C): ")
data = text.encode()
frame = stuff(data)
print(f"Original : {text}")
print(f"Framed   : {frame.decode()}")
print(f"Hex      : {frame.hex(' ')}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(frame)
    s.shutdown(socket.SHUT_WR)          # tell server the frame is complete
    print("Server reply:", s.recv(4096).decode())
