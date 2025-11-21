import socket
import struct

server_addr = ('127.0.0.1', 10000)

# Egyszer létrehozzuk és csatlakozunk
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)

packer = struct.Struct('2s i')

try:
    while True:
        input_str = input("Parancs: ")
        data = input_str.split(" ")

        if len(data) != 2:
            print("Hibás formátum. Példa: BE 50000")
            continue

        command = data[0].upper().encode()
        try:
            amount = int(data[1])
        except ValueError:
            print("Hibás összeg")
            continue

        # Csomagolás és küldés
        data_to_send = packer.pack(command, amount)
        client.sendall(data_to_send)

        # Válasz fogadása
        response = client.recv(1024)
        print("Received:", response.decode())

except KeyboardInterrupt:
    print("Shutting down client...")
finally:
    client.close()
