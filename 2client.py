import socket

PORT = 7447
MESSAGE_LENGTH_SIZE = 64
ENCODING = 'utf-8'

def send_file():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    address = socket.gethostbyname(socket.gethostname())
    buf = 1024
    addr = (address, PORT)

    file_name = "N1//N1_list.txt"

    s.sendto(file_name.encode(ENCODING), addr)

    f = open(file_name, "rb")
    data = f.read(buf)


    while data:
        if s.sendto(data, addr):

            print("sending ...")
            data = f.read(buf)
    s.close()
    f.close()


if __name__ == '__main__':
    send_file()