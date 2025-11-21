import socket
import sys
import select

proxy_addr = 'localhost'
proxy_port = int(sys.argv[2])

server_addr = sys.argv[1]
server_port = 80

web_addr = (server_addr, server_port)

BUFFER_SIZE = 65000

with socket.socket() as proxy, socket.socket() as proxy_sock:
    proxy.setblocking(0)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind((proxy_addr, proxy_port))
    proxy.listen(5)
    proxy_sock.connect(web_addr)
    inputs = [proxy]
    while inputs:
        try:
            readable, writeable, exceptional = select.select(inputs, [], [], 1.0)
            
            if not (readable, writeable, exceptional):
                continue
            
            for sock in readable:
                if sock is proxy:
                    conn, client = sock.accept()
                    conn.setblocking(0)
                    inputs.append(conn)
                else: 
                    data = sock.recv(BUFFER_SIZE)
                    if data:
                        data = data.decode()
                        data = data.replace(f'{proxy_addr}:{proxy_port}', server_addr)
                        data = data.encode()
                        proxy_sock.sendall(data)
                        datafromserver = proxy_sock.recv(BUFFER_SIZE)
                        sock.sendall(datafromserver)
                    inputs.remove(sock)
                    sock.close()
        except KeyboardInterrupt:
            print('Closing the system')
            for c in inputs:
                c.close()
            inputs = []
