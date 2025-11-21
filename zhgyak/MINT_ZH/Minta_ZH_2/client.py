import socket
import struct
import sys

OPERATION = sys.argv[1]
AMOUNT = int(sys.argv[2])

BUFFER_SIZE = 1024

server_addr = ('127.0.0.1', 10000)

packer = struct.Struct('4s i')
data = packer.pack(OPERATION.encode(), AMOUNT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)
client.sendall(data)
print(f"Sent task: {OPERATION} {AMOUNT}")

response = client.recv(BUFFER_SIZE)
print("Received:", response.decode())
client.close()