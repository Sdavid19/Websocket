import socket
import struct
import sys
import random
import time

ops = ['+', '-', '*', '/']

BUFFER_SIZE = 1024

server_addr = ('127.0.0.1', 10000)

packer = struct.Struct('i i 1s')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)

for i in range(1,10):
    time.sleep(3)
    NUM1 = random.randint(1, 100)
    NUM2 = random.randint(1, 100)
    OP =  random.choice(ops)

    data = packer.pack(NUM1, NUM2, OP.encode())
    
    client.sendall(data)
    print(f"Sent task: {NUM1} {OP} {NUM2} = ?")

    response = client.recv(BUFFER_SIZE)
    print("Received:", response.decode())
client.close()