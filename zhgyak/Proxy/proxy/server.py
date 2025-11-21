import socket

server_addr = ('localhost', 10001)

with socket.socket(type=socket.SOCK_DGRAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(server_addr)
    data, address = server.recvfrom(4096)
    print("MSG", data.decode(), "addrress:", address)
    server.sendto(b'Hello client', address)