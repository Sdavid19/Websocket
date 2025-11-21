import socket
import struct
import select

packer = struct.Struct('i i 1s')

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ("localhost", 10001)
    sock.bind(server_address)

    print("UDP server running on port 10001")

    inputs = [sock]
    timeout = 1.0

    while True:
        try:
            readables, _, _ = select.select(inputs, [], [], timeout)

            for s in readables:
                data, client_addr = s.recvfrom(packer.size)

                if not data:
                    continue

                num1, num2, op = packer.unpack(data)
                op = op.decode()

                if op == '+':
                    result = num1 + num2
                elif op == '-':
                    result = num1 - num2
                elif op == '*':
                    result = num1 * num2
                elif op == '/':
                    result = num1 / num2
                else:
                    result = 0

                print(f"Solved: {num1} {op} {num2} = {result}")

                response = f"The result is {result}".encode()
                s.sendto(response, client_addr)

        except KeyboardInterrupt:
            print("Shutting down...")
            break
