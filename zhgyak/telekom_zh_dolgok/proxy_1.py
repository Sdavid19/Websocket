import socket
import struct
import select

# --- Proxy konfiguráció ---
TCP_HOST = "127.0.0.1"
TCP_PORT = 10002  # ide csatlakoznak a diák/admin kliensek
FEEDBACK_SERVER_HOST = "127.0.0.1"
FEEDBACK_SERVER_PORT = 10003  # UDP port a visszajelzés szerverhez

# --- Structok ---
student_packer = struct.Struct('6s 6s i')  # Neptun, Tárgy, Pontszám
server_packer = struct.Struct('6s i')      # Tárgy, Pontszám
response_buffer = 1024                      # max UDP/TCP válasz méret

# --- TCP szerver létrehozása (proxyhoz jövő kliensek) ---
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((TCP_HOST, TCP_PORT))
tcp_sock.listen(5)
tcp_sock.setblocking(False)

inputs = [tcp_sock]  # select input listája

# --- UDP socket a feedback szerverhez ---
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Proxy fut TCP: {TCP_HOST}:{TCP_PORT} -> UDP: {FEEDBACK_SERVER_HOST}:{FEEDBACK_SERVER_PORT}")

while True:
    try:
        readables, _, _ = select.select(inputs, [], [], 1.0)
        for s in readables:
            if s is tcp_sock:
                # új kliens
                client_sock, addr = tcp_sock.accept()
                client_sock.setblocking(False)
                inputs.append(client_sock)
                print("Kapcsolódott:", addr)
            else:
                # kliens üzenet fogadása
                data = s.recv(student_packer.size)
                if not data:
                    # kliens bontotta
                    print("Kliens bontotta")
                    inputs.remove(s)
                    s.close()
                    continue

                neptun_raw, targy_raw, pontszam = student_packer.unpack(data)
                neptun = neptun_raw.decode().strip('\x00')
                targy = targy_raw.decode().strip('\x00')

                # --- ellenőrzés pontszámra ---
                if pontszam >= 6 and neptun != "AAA000":
                    # Diák hibás pont
                    s.sendall(b"Hibas pontszam")
                    continue

                # --- továbbítás a feedback szerverhez UDP-n ---
                send_data = server_packer.pack(targy.encode(), pontszam)
                udp_sock.sendto(send_data, (FEEDBACK_SERVER_HOST, FEEDBACK_SERVER_PORT))

                # --- válasz fogadása a feedback szervertől ---
                resp_data, _ = udp_sock.recvfrom(response_buffer)
                resp_text = resp_data.decode()

                # --- Admin kliens esetében tárgy prefix ---
                if neptun == "AAA000":
                    resp_text = f"{targy} {resp_text}"

                # --- válasz visszaküldése TCP kliensnek ---
                s.sendall(resp_text.encode())

    except KeyboardInterrupt:
        print("Proxy leállítva")
        tcp_sock.close()
        udp_sock.close()
        break
