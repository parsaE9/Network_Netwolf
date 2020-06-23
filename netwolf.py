import time
import socket
import threading
import random
import functions


class Netwolf:
    ENCODING = 'utf-8'
    peers_count = 0

    def __init__(self, name, udp_port):

        self.address = socket.gethostbyname(socket.gethostname())
        self.name = name
        self.udp_port = udp_port

        Netwolf.peers_count += 1

        threading.Thread(target=self.discovery_server, args=()).start()
        time.sleep(0.25)
        threading.Thread(target=self.discovery_client, args=()).start()
        time.sleep(0.75)
        threading.Thread(target=self.GET_client, args=()).start()

    def discovery_server(self):

        HOST_INFORMATION = (self.address, self.udp_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(HOST_INFORMATION)
        print("UDP SERVER {} STARTS".format(self.name))

        while True:
            data, address = server.recvfrom(2048)
            data = data.decode(self.ENCODING)

            if data[0:1] == 'N':
                functions.merge_discovery_msg(self.name, self.udp_port, data, address)

            elif data[0:1] == 'G':
                print("UDP SERVER {} RECEIVED {}".format(self.name, data))


    def discovery_client(self):

        while True:
            file_name = self.name + "//" + self.name + "_list.txt"
            file = open(file_name)
            discovery_list = file.read()
            coList = discovery_list.split('\n')
            line_count = 0
            file.close()

            for i in coList:
                line_count += 1

            if discovery_list == '':
                time.sleep(round(random.uniform(1, 2), 2))
                continue

            for i in range(line_count):

                line = coList[i]

                if line == '' or line == ' ' or line == '\n':
                    continue

                port = int(line[line.find(':') + 1: line.find(':') + 5])

                for j in range(line_count):
                    SERVER_INFORMATION = (self.address, port)
                    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    msg = coList[j].encode(self.ENCODING)
                    client.sendto(msg, SERVER_INFORMATION)
                    # print("UDP CLIENT {} SENT MESSAGE TO {}".format(self.name, port))

                    time.sleep(round(random.uniform(1, 2), 2))

            if Netwolf.peers_count == line_count + 1:
                time.sleep(5)
            else:
                time.sleep(round(random.uniform(2, 3), 2))


    def GET_client(self):

        while True:
            time.sleep(round(random.uniform(1, 1.1), 3))
            file = open("command.txt")
            command = file.read()
            file.close()

            if command == '':
                continue
            elif command[0:2] != self.name:
                continue

            split_command = command.split(' ')

            if split_command[1] == 'list':
                functions.print_node_list(self.name)
            if split_command[1] == 'GET':

                file = open(self.name + "//" + self.name + "_list.txt")
                discovery_list = file.read().split('\n')
                file.close()

                for i in range(len(discovery_list)):

                    if discovery_list[i] == '\n' or discovery_list[i] == '':
                        continue

                    line = discovery_list[i]
                    port = int(line[line.find(':') + 1: line.find(':') + 5])

                    SERVER_INFORMATION = (self.address, port)
                    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    msg = split_command[1] + " " + split_command[2]
                    print("UDP CLIENT {} SENT MESSAGE \"{}\" TO {}".format(self.name, msg , port))
                    msg = msg.encode(self.ENCODING)
                    client.sendto(msg, SERVER_INFORMATION)

                functions.delete_command_file()
