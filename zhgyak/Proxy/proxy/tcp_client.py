import socket

server_addr = ('localhost', 10000)

BUFFER_SIZE = 200

with socket.socket() as client:
    client.connect(server_addr)
    client.sendall(b'Hello server!')
    msg = client.recv(BUFFER_SIZE)
    print(msg.decode())