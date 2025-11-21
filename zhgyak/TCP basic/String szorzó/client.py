import socket
import struct
import sys

BUFFER_SIZE = 1024

WORD = sys.argv[1]
NUM = int(sys.argv[2])

server_addr = ("127.0.0.1", 10000)

packer = struct.Struct('4s i')
data = packer.pack(WORD.encode(), NUM) 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)
client.sendall(data)
print(f"Sent word: {WORD} with num: {NUM}")

response = client.recv(BUFFER_SIZE)
print("Received:", response.decode())
client.close()