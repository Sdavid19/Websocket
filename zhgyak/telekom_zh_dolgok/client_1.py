import socket
import struct
import sys

IP = sys.argv[1]
PORT = int(sys.argv[2])

server_addr = (IP, PORT)

packer_send = struct.Struct('6s 10s i')   # mindig ezt kell küldeni
packer_res = struct.Struct('10s i')       # szerver válasza
packer_final = struct.Struct("12s")       # végső válasz

code = "FBQFSE"
date = "2029-12-05"
msg_count = 1

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)

good_room = ""

while True:
    data = packer_send.pack(code.encode(), date.encode(), msg_count)
    client.sendall(data)

    response = client.recv(packer_res.size)
    room_raw, cap = packer_res.unpack(response)
    room = room_raw.decode().rstrip("\x00")

    print(f"Recv room={room} cap={cap}")

    msg_count += 1

    if cap >= 45:
        good_room = room
        break

# küldés: (neptun_kód, terem_azonosító, üzenetszám)
data_final = packer_send.pack(code.encode(), good_room.encode(), msg_count)
client.sendall(data_final)

# végső válasz: (12s)
final_raw = client.recv(packer_final.size)
(final_code_raw,) = packer_final.unpack(final_raw)

final_code = final_code_raw.decode().rstrip("\x00")
print("Final booking code:", final_code)

client.close()
