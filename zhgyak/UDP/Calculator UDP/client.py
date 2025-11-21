import socket
import struct
import sys

packer = struct.Struct('i i 1s')
NUM1 = int(sys.argv[1])
NUM2 = int(sys.argv[2])
OP = sys.argv[3]


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    server_address = ("localhost", 10001)
    data = packer.pack(NUM1, NUM2, OP.encode())
    sock.settimeout(1.0)
    try:
        sock.sendto(data, server_address)
        print(f"Sent task: {NUM1} {OP} {NUM2} = ?")
        data, _ = sock.recvfrom(1024)
        print(f"Received: {data.decode()}")
    except socket.timeout:
        pass
