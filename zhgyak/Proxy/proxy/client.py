import socket

with socket.socket(type=socket.SOCK_DGRAM) as client:
    server_addr = ('localhost', 10000)
    client.sendto(b'Hello server', server_addr)
    data, address = client.recvfrom(4096)
    print("MSG", data.decode(), "addrress:", address)