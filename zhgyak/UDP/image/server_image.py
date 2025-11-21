import socket
import sys

server_addr = ('localhost', 10000)
BUFFER_SIZE = 200

with socket.socket(type=socket.SOCK_DGRAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.timeout(1.0)
    with open(sys.argv[1], "wb") as f:
        while True:
            try:
                data, client_addr = server.recvfrom(BUFFER_SIZE)
                if data == b'\x00':
                    print("Receive null byte")
                    break
                print(f"Received: {len(data)} bytes")
                f.write(data)
                server.sendto(b"OK", client_addr)
            except socket.timeout:
                pass