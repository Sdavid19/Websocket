import socket
import struct
import select
import time

packer = struct.Struct('i i 1s')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("127.0.0.1", 10000)
sock.bind(server_addr)
sock.listen(5)

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
                num1, num2, op = packer.unpack(data)
        
                result = 0
                if op.decode() == '+':
                    result = int(num1) + int(num2)
                elif op.decode() == '-':
                    result = int(num1) - int(num2)
                elif op.decode() == '*':
                    result = int(num1) * int(num2)
                elif op.decode() == '/':
                    result = int(num1) / int(num2)

                print(f"Solved task: {num1} {op.decode()} {num2} = {result}")
                response = f"The result is {result}"

                s.sendall(response.encode())
    except socket.timeout:
        pass
    except KeyboardInterrupt:
        print("Shutting down server...")
        sock.close()
        break