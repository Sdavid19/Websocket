import socket
import struct
import sys

NUM1 = int(sys.argv[1])
NUM2 = int(sys.argv[2])
OP = sys.argv[3]

BUFFER_SIZE = 1024

server_addr = ('127.0.0.1', 10000)

packer = struct.Struct('i i 1s')
data = packer.pack(NUM1, NUM2, OP.encode())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)
client.sendall(data)
print(f"Sent task: {NUM1} {OP} {NUM2} = ?")

response = client.recv(BUFFER_SIZE)
print("Received:", response.decode())
client.close()