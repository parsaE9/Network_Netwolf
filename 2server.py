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
    data, address2 = s.recvfrom(1024)
    if data:
        print("SERVER : client sent msg {}".format(data.decode(ENCODING)))
        s.sendto(data, address2)


if __name__ == '__main__':
    main()
