import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ('127.0.0.1', 1000)

sock.bind(server_addr)
sock.listen(1)
sock.settimeout(1.0)

while True:
    client_sock, client_addr = sock.accept()
    data = client_sock.recv(16)
    if data:
        client_sock.send("Hello Client!".encode())
    client_sock.close()
    