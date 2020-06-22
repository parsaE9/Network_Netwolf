import time
import socket
import threading
import random
import functions


class Server:

    ENCODING = 'utf-8'
    peers_count = 0

    def __init__(self, name, udp_port):
        self.address = socket.gethostbyname(socket.gethostname())
        self.name = name
        self.udp_port = udp_port
        Server.peers_count += 1
        threading.Thread(target=self.discovery_server, args=()).start()
        time.sleep(2)
        threading.Thread(target=self.discovery_client, args=()).start()


    def discovery_server(self):

        HOST_INFORMATION = (self.address, self.udp_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(HOST_INFORMATION)
        print("[DISCOVERY SERVER {} STARTS] Server is starting ...".format(self.name))
        while True:
            data, address = server.recvfrom(2048)
            data = data.decode(self.ENCODING)
            print("[DISCOVERY SERVER {} ] DATA : {} \t RECEIVED FROM : {}".format(self.name, data, address))

            name_index = data.replace(':', 'X', 1).find(':')
            port_index = data.replace(':', 'X', 2).find(':')
            sender_name = data[name_index + 1 : name_index + 3]
            sender_udp_port = data[port_index + 1 : port_index + 5]
            sender_ip = address[0]
            sender_info = sender_name + " " + sender_ip + ":" + sender_udp_port

            file_name = self.name + "//" + self.name + "_list.txt"
            file = open(file_name)
            discovery_list = file.read()
            file.close()

            '''print(sender_name)
            print(sender_ip)
            print(sender_udp_port)'''
            print("[SERVER {}] SENDER INFO : {}".format(self.name, sender_info))

            if sender_info not in discovery_list:

                file = open(file_name, 'a')
                if discovery_list == '':
                    file.write(sender_info + " NODE:" + self.name + " UDP_PORT:" + str(self.udp_port) + "\n")
                else:
                    file.write("\n" + sender_info + " NODE:" + self.name + " UDP_PORT:" + str(self.udp_port))
                file.close()

            if data[0 : data.find(':') + 5] not in discovery_list and self.name != data[0 : 2] :

                file = open(file_name, 'a')
                if discovery_list == '':
                    file.write(data[0 : data.find(':') + 5] + " NODE:" + self.name + " UDP_PORT:" + str(self.udp_port) + "\n")
                else:
                    file.write("\n" + data[0 : data.find(':') + 5] + " NODE:" + self.name + " UDP_PORT:" + str(self.udp_port))
                file.close()

            functions.remove_empty_lines(file_name)
            time.sleep(round(random.uniform(0, 2), 2))


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
                time.sleep(round(random.uniform(0, 2), 2))
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
                    print("client {} sent message to {}".format(self.name, port))

                    time.sleep(round(random.uniform(0, 2), 2))

            time.sleep(round(random.uniform(2, 4), 2))
