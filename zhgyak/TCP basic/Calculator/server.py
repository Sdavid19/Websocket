import socket
import struct

packer = struct.Struct('i i 1s')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("127.0.0.1", 10000)
sock.bind(server_addr)
sock.listen(5)
sock.settimeout(1.0)

while True:
    try:
        print("Waiting...")
        client_socket, client_addr = sock.accept()
        print("Connected:", client_addr)

        data = client_socket.recv(packer.size)
        if not data:
            print("Disconnected")
            client_socket.close()
            continue

        num1, num2, op = packer.unpack(data)
        print(f"Got task from client: {num1} {op.decode()} {num2} = ?")
        
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

        client_socket.sendall(response.encode())
        client_socket.close()

    except socket.timeout:
        pass
    except socket.error as msg:
        print(msg)