"""Set 10 - TCP Echo Client: send several messages sequentially. Type 'exit' to quit."""
import socket

HOST, PORT = "127.0.0.1", 5010

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}. Type messages ('exit' to quit).")
    while True:
        msg = input("Message: ")
        if msg.strip().lower() == "exit":
            break
        s.sendall(msg.encode())
        print("Echo   :", s.recv(1024).decode())
print("Connection closed.")
