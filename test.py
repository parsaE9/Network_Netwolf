import socket
import random
import functions

if __name__ == '__main__':

    file = open("N3//N3_list.txt", 'r+')

    node_list = file.read()
    file.seek(0)
    file.truncate()
    file.close()
    print(node_list)