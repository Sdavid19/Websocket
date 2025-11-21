import socket
import select
import struct

CLIENT_FORMAT = struct.Struct("i 20s")
SERVER_FORMAT = struct.Struct("20s")

TCP_SERVER_ADDR = ("127.0.0.1", 10001)
UDP_SERVER_ADDR = ("127.0.0.1", 10002)

tcp_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_sock.connect(TCP_SERVER_ADDR)

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy.bind(("0.0.0.0", 3000))
proxy.listen()

clients = {}

while True:
    r, _, _ = select.select([proxy, tcp_server_sock] + list(clients.keys()), [], [])

    for s in r:
        if s is proxy:
            cs, _ = proxy.accept()
            clients[cs] = True

        elif s is tcp_server_sock:
            resp = tcp_server_sock.recv(SERVER_FORMAT.size)
            if not resp:
                continue
            for c in clients:
                if clients[c] == "waiting_tcp":
                    c.sendall(resp)
                    clients[c] = True
                    break

        else:
            data = s.recv(CLIENT_FORMAT.size)
            if not data:
                del clients[s]
                s.close()
                continue

            urg, msg = CLIENT_FORMAT.unpack(data)

            if urg == 0:
                tcp_server_sock.sendall(SERVER_FORMAT.pack(msg))
                clients[s] = "waiting_tcp"

            else:
                udp_sock.sendto(SERVER_FORMAT.pack(msg), UDP_SERVER_ADDR)
                resp, _ = udp_sock.recvfrom(SERVER_FORMAT.size)
                s.sendall(resp)
