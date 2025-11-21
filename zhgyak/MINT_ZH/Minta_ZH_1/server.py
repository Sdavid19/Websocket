import struct
import socket

packer = struct.Struct("20s i")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("127.0.0.1", 10001)
sock.bind(server_addr)
sock.listen(1)
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

        word, num = packer.unpack(data)
        word = word.decode().rstrip("\x00")
        print(f"The client sent word: {word} with num: {num}")

        sliced = word[:num]
        print(f"The {word} word {num} times")
        response = sliced[::-1]

        client_socket.sendall(response.encode())
        client_socket.close()

    except socket.timeout:
        pass
    except KeyboardInterrupt:
        print("Shutting down server...")
        sock.close()
        break
