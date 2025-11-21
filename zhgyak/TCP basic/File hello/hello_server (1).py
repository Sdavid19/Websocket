import socket
import json
import sys
import struct

USERS_FILE = sys.argv[1]

try:
    with open(USERS_FILE) as f:
        USERNAMES = json.load(f)
except FileNotFoundError:
    print(f"The file: {USERS_FILE} udoes not exist!")
    exit()

packer = struct.Struct("13s i")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, TCP
server_addr = ("127.0.0.1", 10000)  # ('localhost',10000)
sock.bind(server_addr)
sock.listen(1)
sock.settimeout(1.0)  # Only necessary for Windows, so that CTRL+C works

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

        message, id = packer.unpack(data)
        print(f"The client sent: {message.decode()} with ID: {id}")
        try:
            username = USERNAMES[str(id)]
            print(f"The username for this ID is {username}")
        except KeyError:
            username = "Anonymous"
            print(f"There is no username for this ID, using {username}")
        response = f"Hello {username}!"

        client_socket.sendall(response.encode())
        client_socket.close()

    except socket.timeout:
        pass
    except KeyboardInterrupt:
        print("Shutting down server...")
        sock.close()
        break
