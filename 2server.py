import socket
import threading
import select

PORT = 7447
MESSAGE_LENGTH_SIZE = 64
ENCODING = 'utf-8'


def main():
    address = socket.gethostbyname(socket.gethostname())
    addr = (address, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    print("[SERVER STARTS] Server is starting ...")

    buf = 1024

    data, addr = s.recvfrom(buf)
    print(addr[0])
    print(type(addr[0]))
    data = data.decode(ENCODING)
    print("Received File:", data)

    f = open(data.strip(), 'wb')

    data, addr = s.recvfrom(buf)
    try:
        while data:
            f.write(data)
            s.settimeout(2)
            data, addr = s.recvfrom(buf)
    except:
        f.close()
        s.close()
        print("File Downloaded")




if __name__ == '__main__':
    main()
