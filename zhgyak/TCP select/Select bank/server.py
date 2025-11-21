import socket
import select
import struct

TCP_IP = "localhost"
TCP_PORT = 10000

# Struct: 2 byte parancs + 4 byte egész szám
packer = struct.Struct('2s i')

# Egyenlegek: kulcs a kliens socketje
balances = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(5)
inputs = [sock]
timeout = 1.0

print(f"Server listening on {TCP_IP}:{TCP_PORT}...")

try:
    while True:
        readables, _, _ = select.select(inputs, [], [], timeout)

        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                print(f"Connected: {client_info[0]}:{client_info[1]}")
                print(connection)
                balances[connection] = 0
                inputs.append(connection)
            else:
                data = s.recv(packer.size)
                if not data:
                    print("Client disconnected")
                    s.close()
                    inputs.remove(s)
                    balances.pop(s, None)
                    continue

                try:
                    command, amount = packer.unpack(data)
                    command = command.decode()
                except struct.error:
                    s.sendall(b"Hibas uzenet")
                    continue

                # BE/KI logika
                if command == 'BE':
                    balances[s] += amount
                elif command == 'KI':
                    balances[s] -= amount
                else:
                    s.sendall(b"Hibas parancs")
                    continue

                new_balance = balances[s]
                s.sendall(f"Jelenlegi egyenleged: {new_balance} ft".encode())

except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    for s in inputs:
        s.close()
