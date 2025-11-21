import socket

server_address = ("127.0.0.1", 10000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)
client.sendall("Hello Server!".encode())
data = client.recv(16)
client.close