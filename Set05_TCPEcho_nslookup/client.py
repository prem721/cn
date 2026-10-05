"""Set 5 - TCP Echo Client: send one message, display the echo."""
import socket

HOST, PORT = "127.0.0.1", 5005

msg = input("Enter message: ")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(msg.encode())
    echo = s.recv(1024).decode()
print("Echoed from server:", echo)
