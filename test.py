import socket
import random
import functions
import glob
import os
import time


if __name__ == '__main__':

    # file = open("N3//N3_list.txt", 'r+')
    # file.close()
    data = {}
    data.update({"key1" : 85})
    print(data)
    data.update({"sex" : 22})
    print(data.get("key1"))
    print(data.get("sex"))
    print(data.get("sexx"))
    print(len(data))
    for i in data:
        print(data.get(i))