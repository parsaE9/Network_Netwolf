import socket
import random
import functions
import glob
import os
import time


if __name__ == '__main__':

    # file = open("N3//N3_list.txt", 'r+')
    # file.close()
    begin = round(time.time(), 6)
    time.sleep(2)
    end = round(time.time(), 6)
    msg = "hi"
    print(begin)
    print(end)
    a = end - begin
    print("difference = {}".format(a))
    msg += str(a)
    print(msg)
    address = socket.gethostbyname(socket.gethostname())
    print(address)