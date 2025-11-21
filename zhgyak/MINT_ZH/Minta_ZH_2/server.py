#szeretlek

import socket
import struct
import select
import time

packer = struct.Struct('4s i')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("127.0.0.1", 10000)
sock.bind(server_addr)
sock.listen(5)
num = 0

inputs = [sock]
timeout = 3.0

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
                if not data:
                    print("Disconnected")
                    inputs.remove(s)
                    s.close()
                    continue
                operation, amount = packer.unpack(data)
        
                operation = operation.decode().rstrip("\x00")
                
                if operation == 'IN':
                    num = amount
                if operation == 'INCR':
                    num = num + amount
                if operation == 'DECR':
                    num = num - amount

                print(f"Changed value: {operation} {amount} => {num}")
                response = num

                s.sendall(str(num).encode())
    except socket.timeout:
        pass
    except KeyboardInterrupt:
        print("Shutting down server...")
        sock.close()
        break
