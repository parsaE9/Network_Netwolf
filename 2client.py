import socket

PORT = 7447
MESSAGE_LENGTH_SIZE = 64
ENCODING = 'utf-8'

def send_file():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    address = socket.gethostbyname(socket.gethostname())
    buf = 1024
    addr = (address, PORT)
    msg = "hi im client"
    s.sendto(msg.encode(ENCODING), addr)
    data, server = s.recvfrom(buf)
    print("Client: I got msg back {}".format(data.decode(ENCODING)))
    s.close()




if __name__ == '__main__':
    send_file()