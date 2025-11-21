# Socket zh összefoglaló

---

## Alapfogalmak

**Mit jelent az `AF_INET` paraméter?**  
> Az IPv4 címzési családot jelöli. Ez azt jelenti, hogy a socket IPv4 alapú kommunikációt fog használni (IP-cím és port).

**Mit csinál a `socket()` függvény?**  
> Létrehoz egy új socket objektumot, amelyen keresztül hálózati kommunikáció történhet.  
> Példa:  
> ```python
> s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
> ```

**Mi a különbség a `SOCK_STREAM` és `SOCK_DGRAM` között?**  
> - `SOCK_STREAM`: kapcsolat-orientált (TCP), megbízható, sorrendtartó.  
> - `SOCK_DGRAM`: kapcsolat nélküli (UDP), gyorsabb, de nem garantálja a sorrendet vagy a kézbesítést.

**Mit jelent a `localhost`?**  
> A helyi számítógépet jelöli, IP címe: `127.0.0.1`.

**Mit jelent a port szám?**  
> Egy adott folyamat vagy szolgáltatás azonosítására szolgáló szám az adott gépen.

**Mi az IP cím szerepe?**  
> Az IP cím azonosítja a hálózaton lévő számítógépet (hostot).

**Mit jelent a `('localhost', 10000)` pár?**  
> Egy cím–port pár, amely megadja a hálózati végpontot:  
> `host='localhost'`, `port=10000`.

---

## TCP Alapműveletek

**Mit jelent a `bind()` művelet?**  
> A socketet egy adott IP-címhez és porthoz köti.

**Mire szolgál a `listen()` függvény?**  
> Engedélyezi a socket számára, hogy bejövő kapcsolatokat fogadjon (csak TCP-nél).  
> Példa: `server_socket.listen(5)` → maximum 5 várakozó kliens.

**Mi történik, ha a `listen()` paraméter 1?**  
> Legfeljebb 1 kliens várhat a kapcsolódásra a sorban.

**Mit csinál az `accept()` függvény?**  
> Elfogad egy beérkező kapcsolatot, és visszaad egy új socketet és a kliens címét.  
> ```python
> client_socket, addr = server_socket.accept()
> ```

**Mikor használjuk a `connect()` függvényt?**  
> A kliens oldalon, hogy kapcsolatot hozzon létre a szerverrel.

**Mi történik `accept()` után TCP szerveren?**  
> A szerver új socketet kap, amin keresztül az adott klienssel kommunikálhat.

**Hogyan zárjuk be helyesen a kliens kapcsolatot a TCP szerveren?**  
> ```python
> client_socket.close()
> ```

**Mit csinál a `close()` függvény?**  
> Bezárja a socketet és felszabadítja az erőforrásokat.

**Mi a különbség a szerver socket és kliens socket között TCP-ben?**  
> - **Szerver socket**: hallgat (`listen()`), és új kapcsolatokat fogad (`accept()`).  
> - **Kliens socket**: csatlakozik (`connect()`), és adatot küld/fogad.

---

## TCP Kommunikáció

**Mikor kell a `recv()` függvényt alkalmazni?**  
> Akkor, amikor adatot szeretnénk fogadni a kapcsolaton keresztül.

**Mi történik, ha a `recv()` 0 byte-ot ad vissza?**  
> A kapcsolat bezárult (a másik fél lezárta a kapcsolatot).

**Mi a `sendall()` függvény előnye a `send()`-del szemben?**  
> A `sendall()` addig küldi az adatot, amíg az egész el nem jut a címzetthez, míg a `send()` részleges küldést is visszaadhat.

**Hogyan kezeljük a részleges adatküldést TCP-ben?**  
> `sendall()` használatával, vagy ciklusban újraküldve a maradékot.

**Mi a TCP szerver helyes sorrendje?**  
> ```python
> socket() → bind() → listen() → accept() → recv()/send() → close()
> ```

**Mi a TCP kliens helyes sorrendje?**  
> ```python
> socket() → connect() → send()/recv() → close()
> ```

**Hogyan hozunk létre TCP socketet?**  
> ```python
> s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
> ```

---

## Fájlkezelés és bináris adatok TCP-n

**Hogyan küldünk bináris adatokat TCP-n?**  
> Bináris módban nyitjuk meg a fájlt és byte-okat küldünk:  
> ```python
> f = open('data.bin', 'rb')
> data = f.read()
> s.sendall(data)
> ```

**Hogyan olvassunk és küldjünk fájlt TCP-n hatékonyan?**  
> Csomagonként, pl. 4096 byte-os blokkokban:  
> ```python
> while chunk := f.read(4096):
>     s.sendall(chunk)
> ```

**Mi a fő különbség TCP és UDP fájlküldés között?**  
> - **TCP**: megbízható, sorrendtartó, teljes fájlátvitel biztosított.  
> - **UDP**: gyorsabb, de csomagvesztés lehetséges.

---

## struct Modul

**Mi a `struct` modul szerepe socket programozásban?**  
> Bináris adatok csomagolása és kicsomagolása (pl. integer, float → byte).

**Mit csinál a `struct.pack()`?**  
> Bináris formátumba csomagol Python-adatokat.  
> ```python
> data = struct.pack('I f 1s', 42, 3.14, b'A')
> ```

**Mit csinál a `struct.unpack()`?**  
> Bináris adatokat alakít vissza Python-típusokra.  
> ```python
> values = struct.unpack('I f 1s', data)
> ```

**Mi a `'f f 1s'` formátum jelentése struct-ban?**  
> 2 darab float és 1 darab 1 hosszú byte-string.

**Mit jelent az `'I I 1s'` struct formátum?**  
> 2 darab unsigned int (`I`) és 1 darab 1 byte-os karakter (`1s`).

---

## Socket Beállítások

**Mit jelent a `SO_REUSEADDR` opció?**  
> Engedélyezi, hogy egy lezárt portot azonnal újra lehessen használni (ne kelljen várni TIME_WAIT állapotban).

**Hogyan állítjuk be a `SO_REUSEADDR` opciót?**  
> ```python
> s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
> ```

---

## Timeout és Blocking mód

**Mit jelent a socket timeout?**  
> Az az időtartam, ameddig a socket vár egy művelet (pl. `recv()`) befejezésére, mielőtt kivételt dob.

**Mire való a `settimeout()` függvény?**  
> Beállítja, mennyi ideig várjon a socket egy műveletre.  
> ```python
> s.settimeout(5)  # 5 másodperc
> ```

**Mikor dobódik `socket.timeout` kivétel?**  
> Ha a megadott idő alatt nem érkezik adat vagy nem jön létre kapcsolat.

**Mit jelent a “blocking” socket művelet?**  
> A program addig vár, amíg a művelet (pl. `recv()`, `accept()`) be nem fejeződik.

**Mi történik, ha `select()` timeout-ol?**  
> Üres listát ad vissza, azaz nincs olvasásra/írásra kész socket.

**Hogyan kezeljük a timeout kivételt UDP-nél?**  
> `try-except socket.timeout:` blokkban.

---

## UDP Socketek

**Hogyan hozunk létre UDP socketet?**  
> ```python
> s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
> ```

**Mi a fő különbség UDP és TCP között?**  
> UDP nem kapcsolat-orientált, nincs kézbesítési garancia, de gyorsabb.

**Mit csinál a `sendto()` függvény?**  
> Adatot küld egy adott címre:  
> ```python
> s.sendto(b'Hello', ('localhost', 9999))
> ```

**Mit ad vissza a `recvfrom()` függvény?**  
> Egy `(data, addr)` párt: a beérkező adatot és a küldő címét.

**Mit ad vissza pontosan a `recvfrom()`?**  
> ```python
> data, address = s.recvfrom(1024)
> ```

**Milyen paramétereket vár a `sendto()`?**  
> `sendto(data: bytes, address: (host, port))`

**Kell-e `connect()` UDP kliensnél?**  
> Nem szükséges, de opcionálisan megadható fix célcím.

**Kell-e `listen()` UDP szervernél?**  
> Nem, mert UDP kapcsolat nélküli.

**Mi az UDP szerver alapvető sorrendje?**  
> ```python
> socket() → bind() → recvfrom() → sendto()
> ```

**Mi az UDP kliens alapvető sorrendje?**  
> ```python
> socket() → sendto() → recvfrom()
> ```

**Kell-e `bind()` az UDP kliensnek?**  
> Nem feltétlenül, a rendszer automatikusan kioszt egy portot.

**Mi a UDP datagram elméleti maximális mérete?**  
> 65 507 byte (a 65 535-ös IP-csomagméretből levonva a fejléceket).

**Mi történik, ha UDP csomag elvész?**  
> Egyszerűen elveszik, az alkalmazásnak kell kezelnie.

**Mi a timeout szerepe UDP-nél?**  
> Megakadályozza, hogy a kliens végtelen ideig várjon válaszra.

---

## Többszálúság és több kliens kezelése

**Hogyan kezeljük a többszörös kliens kapcsolatokat?**  
> - Többszálú vagy többfolyamatú megoldással  
> - Vagy `select()` / `asyncio` használatával, ami több socketet kezel párhuzamosan.

**Mit csinál a `select()` függvény?**  
> Figyeli több socket állapotát (olvasható/írható/hibás).  
> ```python
> readable, writable, errored = select.select(inputs, outputs, inputs)
> ```

**Mik a `select()` visszatérési értékei?**  
> Három lista:  
> - Olvasható socketek  
> - Írható socketek  
> - Hibás socketek

**Mi a `with` statement előnye socket programozásban?**  
> Automatikusan bezárja a socketet a blokk végén:  
> ```python
> with socket.socket(...) as s:
>     ...
> ```

---

## Proxy és HTTP

**Mi a proxy szerver szerepe?**  
> Közvetítő a kliens és a cél szerver között, továbbítja vagy szűri a forgalmat.

**Hogyan szűrhetjük a HTTP kéréseket proxy-ban?**  
> A beérkező kérések fejlécének elemzésével (pl. `Host`, `User-Agent` mezők).

**Mit jelent a 404 HTTP státuszkód?**  
> „Not Found” – a kért erőforrás nem található a szerveren.

---

## Hiba- és kapcsolatkezelés

**Hogyan detektáljuk a kapcsolat megszakadást TCP-ben?**  
> - `recv()` 0 byte-ot ad vissza  
> - `socket.error` vagy `ConnectionResetError` kivétel dobódik.

**Mi a leggyakoribb oka a `bind()` sikertelenségének?**  
> A port már foglalt, vagy a programnak nincs jogosultsága használni azt.
