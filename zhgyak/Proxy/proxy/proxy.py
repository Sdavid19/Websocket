import socket
import select

proxy_addr = 'localhost'
proxy_port = 10001

server_addr = "localhost"
server_port = 10000

BUFFER_SIZE = 200

proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with socket.socket() as proxy:
    proxy.setblocking(0)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind((server_addr, server_port))
    proxy.listen(5)
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
                        data_dc = data.decode()
                        print(f"The clients msg:", data_dc)
                        proxy_sock.sendto(data, (proxy_addr, proxy_port))
                        reply, _ = proxy_sock.recvfrom(BUFFER_SIZE)
                        reply_dc = reply.decode()
                        print(f'The servers msg: {reply_dc}')
                    else:
                        print(f'Closing {sock.getpeername()} after reading no data')
                        inputs.remove(sock)
                        sock.close()
        except KeyboardInterrupt:
            print('Closing the system')
            for c in inputs:
                c.close()
            inputs = []