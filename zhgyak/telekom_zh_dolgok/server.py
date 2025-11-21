import socket
import struct
import select
import sys

marks = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("127.0.0.1", 10001)
sock.bind(server_addr)
sock.listen(5)

inputs = [sock]
timeout = 1.0

packer = struct.Struct('3s 6s 6s f')
packer_res = struct.Struct('f')

while True:
    try:
        readables, _, _ = select.select(inputs, [], [], timeout)
        for s in readables:
            if s is sock:
                client_socket, client_addr = sock.accept()
                print("Connected:", client_addr)
                inputs.append(client_socket)
            else:
                data = s.recv(packer.size)
                res = 0.0
                if not data:
                    print("Disconnected")
                    inputs.remove(s)
                    s.close()
                    continue
                op, targy, hallgato, jegy = packer.unpack(data)
                op = op.decode()
                targy = targy.decode()
                hallgato = hallgato.decode()
                print(op, targy, hallgato, jegy)
                if op == 'INS':
                    if targy not in marks:
                        marks[targy] = {}
                    marks[targy][hallgato] = jegy
                    res = marks[targy][hallgato]
                if op == 'GET':
                    res = marks[targy][hallgato] 
                if op == 'AVG':
                    jegyek = marks[targy].values()
                    atlag = sum(jegyek) / len(jegyek)
                    res = atlag
                print(f"Resp sent: {res}")
                data_res = packer_res.pack(res)
                s.sendall(data_res)
    except KeyboardInterrupt:
        print("Shutting down server...")
        sock.close()
        break

