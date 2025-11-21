import socket
import struct
import sys

IP = sys.argv[1]
PORT = int(sys.argv[2])

server_addr = (IP, PORT)

packer_send = struct.Struct('6s 13s 6s')
packer_res =  struct.Struct('i i')
packer_final_res = struct.Struct('12s')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)

code = "FBQFSE"
ids = "9780679760801"
command = "submit"

days_t = 21

final_res = ""

data = packer_send.pack(code.encode(), ids.encode(), "submit".encode())
client.sendall(data)
response = client.recv(packer_res.size)
av, days = packer_res.unpack(response)
print(f"Recieved: {av} {days}")
if av == 0:
    data = packer_send.pack(code.encode(), ids.encode(), "cancel".encode())
    client.sendall(data)
    response = client.recv(packer_final_res)
    final_res = packer_res.unpack(response)
else:
    if days >= days_t:
        data = packer_send.pack(code.encode(), ids.encode(), "borrow".encode())
        client.sendall(data)
        
        response = client.recv(packer_final_res)
        final_res = packer_res.unpack(response)
    else:
        data = packer_send.pack(code.encode(), ids.encode(), "extend".encode())
        client.sendall(data)
        response = client.recv(packer_res.size)
        av, days = packer_res.unpack(response)
        print(f"Recieved: {av} {days}")
        if days >= days_t:
            data = packer_send.pack(code.encode(), ids.encode(), "borrow".encode())
            client.sendall(data)
        else:
            data = packer_send.pack(code.encode(), ids.encode(), "cancel".encode())
            client.sendall(data)
        response = client.recv(packer_final_res.size)
        final_res = packer_final_res.unpack(response)

print(final_res[0].decode())
client.close()