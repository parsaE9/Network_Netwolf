import time
import socket
import threading
import random
import functions
import os


class Netwolf:
    ENCODING = 'utf-8'
    peers_count = 0

    def __init__(self, name, udp_port):

        self.address = socket.gethostbyname(socket.gethostname())
        self.name = name
        self.udp_port = udp_port
        self.reply_list = []

        Netwolf.peers_count += 1

        threading.Thread(target=self.UDP_server, args=()).start()
        time.sleep(0.25)
        threading.Thread(target=self.discovery_client, args=()).start()
        threading.Thread(target=self.GET_client, args=()).start()



    def UDP_server(self):

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

                # print("UDP SERVER {}: RECEIVED msg \"{}\"".format(self.name, data))
                files_in_folder = os.listdir(self.name)
                split_data = data.split(' ')

                if split_data[1] in files_in_folder:
                    msg = "UDP SERVER {} : I Got \"{}\"".format(self.name, split_data[1])
                    server.sendto(msg.encode(self.ENCODING), address)



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
                    time.sleep(round(random.uniform(0.75, 1), 3))

            if Netwolf.peers_count == line_count + 1:
                time.sleep(4)
            else:
                time.sleep(round(random.uniform(2, 2.5), 2))


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

                thread_list = []

                for i in range(len(discovery_list)):

                    if discovery_list[i] == '\n' or discovery_list[i] == '':
                        continue

                    line = discovery_list[i]
                    port = int(line[line.find(':') + 1: line.find(':') + 5])

                    SERVER_INFORMATION = (self.address, port)
                    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    msg = split_command[1] + " " + split_command[2]
                    msg = msg.encode(self.ENCODING)
                    t = threading.Thread(target=self.client_receive_GET_response, args=(client, msg, SERVER_INFORMATION, ))
                    thread_list.append(t)
                    t.start()

                for t in thread_list:
                    t.join()

                # TODO: implement TCP file sharing

                functions.delete_command_file()


    def client_receive_GET_response(self, client, msg, SERVER_INFORMATION):
        try:
            client.sendto(msg, SERVER_INFORMATION)
            client.settimeout(2)
            reply, server = client.recvfrom(1024)
            reply = reply.decode(Netwolf.ENCODING)
            print("UDP CLIENT {}: RECEIVED REPLY \"{}\"".format(self.name, reply))
            self.reply_list.append(reply)
        except socket.timeout:
            print("UDP CLIENT {}: GOT NO REPLY".format(self.name))
            client.close()
