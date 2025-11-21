import socket
import sys

BUFFER_SIZE = 200
END_BYTE = b"\x00"

with socket.socket(type=socket.SOCK_DGRAM) as client:
    server_addr = ('localhost', 10000)
    with open(sys.argv[1], "rb") as f:
        data = f.read(BUFFER_SIZE)
        while data:
            try:
                client.sendto(data, server_addr)
                print(f"Sent: {len(data)}" )
                client.recvfrom(BUFFER_SIZE)
                reply, _ = client.recvfrom(BUFFER_SIZE)
                print(f'Received: {reply.decode()}')
                data = f.read(BUFFER_SIZE)
            except socket.timeout:
                pass
        client.sendto(END_BYTE, server_addr)