import socket
import struct
import sys
import random

BUFFER_SIZE = 1024

WORD = input("Adj meg egy szót: ")
NUM = random.randint(1, len(WORD)-1)

server_addr = ("127.0.0.1", 10001)

packer = struct.Struct('20s i')
data = packer.pack(WORD.encode(), NUM) 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)
client.sendall(data)
print(f"Sent word: {WORD} with num: {NUM}")

response = client.recv(BUFFER_SIZE)
print("Received:", response.decode())
client.close()