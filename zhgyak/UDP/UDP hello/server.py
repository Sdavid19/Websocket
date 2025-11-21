import socket

BUFFER_SIZE = 200

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ("localhost", 10001)
    sock.bind(server_address)
    sock.settimeout(1.0)

    while True:
        try:
            data, client = sock.recvfrom(BUFFER_SIZE)

            print("Received: ", data.decode())

            sock.sendto("Hello client!".encode(), client)

        except socket.timeout:
            pass
        except socket.error as msg:
            print(msg)
