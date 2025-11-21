import socket

BUFFER_SIZE = 200
MESSAGE = "Hello server!".encode()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    server_address = ("localhost", 10001)
    sock.settimeout(1.0)
    try:
        sock.sendto(MESSAGE, server_address)
        print(f"Sent: {MESSAGE}")
        data, _ = sock.recvfrom(BUFFER_SIZE)
        print(f"Received: {data.decode()}")
    except socket.timeout:
        pass
