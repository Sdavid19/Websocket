from socket import socket, AF_INET, SOCK_STREAM
import random
import struct

BUFFER_SIZE = 1024
server_addr = ("localhost", 10000)

packer = struct.Struct("13s i")
message = "Hello Server!"
id = random.randint(1,11)
data = packer.pack(message.encode(), id)

client = socket(AF_INET, SOCK_STREAM)
client.connect(server_addr)
client.sendall(data)
print(f"Sent: {message} with ID:{id}")

response = client.recv(BUFFER_SIZE)
print("Received:", response.decode())

client.close()
