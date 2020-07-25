import socket
import threading
import random
import os
from functions import *


class NetWolf:
    ENCODING = 'utf-8'
    timer_dic = {}

    def __init__(self, name, udp_port, discovery_msg_interval, wait_for_response_interval, maximum_TCP_connections):

        self.name = name
        self.address = socket.gethostbyname(socket.gethostname())
        self.udp_port = udp_port
        self.tcp_port = random.randint(5000, 7430)
        self.discovery_msg_interval = discovery_msg_interval
        self.wait_for_response_interval = wait_for_response_interval
        self.maximum_TCP_connections = maximum_TCP_connections
        self.current_TCP_connections = 0
        self.response_list = []
        self.get_history = []

        threading.Thread(target=self.UDP_server, args=()).start()
        threading.Thread(target=self.TCP_server, args=()).start()
        time.sleep(0.35)
        threading.Thread(target=self.UDP_client, args=()).start()


    def UDP_server(self):

        HOST_INFORMATION = (self.address, self.udp_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(HOST_INFORMATION)

        while True:
            data, address = server.recvfrom(2048)
            data = data.decode(self.ENCODING)

            if data[0:1] == 'N':
                merge_discovery_msg(self.name, self.udp_port, data, address)

            elif data[0:1] == 'G':

                files_in_folder = os.listdir(self.name)
                split_data = data.split(' ')

                if split_data[1] in files_in_folder:
                    index = len(NetWolf.timer_dic) + 1
                    start_time = time.time()
                    if not split_data[2] in self.get_history:
                        time.sleep(round(random.uniform(0.5, 1), 2))
                    NetWolf.timer_dic.update({str(index): str(start_time)})
                    msg = "{} {} {}".format(self.name, self.tcp_port, str(index))
                    server.sendto(msg.encode(self.ENCODING), address)

    def TCP_server(self):
        HOST_INFORMATION = (self.address, self.tcp_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(HOST_INFORMATION)
        server.listen(5)
        while True:
            conn, address = server.accept()
            if self.current_TCP_connections < self.maximum_TCP_connections:
                threading.Thread(target=self.TCP_server_handle_client, args=(conn, address)).start()
                self.current_TCP_connections += 1
            else:
                conn.close()



    def TCP_server_handle_client(self, connection, address):
        name = connection.recv(1024).decode(self.ENCODING)
        filename = self.name + "//" + name
        file = open(filename, 'rb')
        buffer = file.read(1024)
        while buffer:
            connection.send(buffer)
            buffer = file.read(1024 * 1000)
        file.close()
        connection.close()
        self.current_TCP_connections -= 1


    def UDP_client(self):
        threading.Thread(target=self.UDP_client_discovery, args=()).start()
        threading.Thread(target=self.UDP_client_service, args=()).start()


    def UDP_client_discovery(self):

        while True:
            file_name = self.name + "//" + self.name + "_list.txt"
            file = open(file_name)
            discovery_list = file.read()
            coList = discovery_list.split('\n')
            line_count = 0
            file.close()

            for _ in coList:
                line_count += 1

            if discovery_list == '':
                time.sleep(self.discovery_msg_interval)
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
                time.sleep(round(random.uniform(0.15, 0.20), 3))

            time.sleep(self.discovery_msg_interval)


    def UDP_client_service(self):

        while True:
            time.sleep(round(random.uniform(0.5, 0.75), 3))
            try:
                file = open(self.name + "//command.txt")
                command = file.read()
                file.close()
            except FileNotFoundError:
                continue

            if command == '':
                continue

            split_command = command.split(' ')

            if split_command[1] == 'list':
                UDP_list(self.name)
            if split_command[1] == 'GET':
                threading.Thread(target=self.UDP_GET, args=(split_command,)).start()

            delete_command_file(self.name)
            time.sleep(1.25)


    def UDP_GET(self, split_command):

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
            msg = split_command[1] + " " + split_command[2] + " " + split_command[0]
            msg = msg.encode(self.ENCODING)
            t = threading.Thread(target=self.client_receive_GET_response, args=(client, msg, SERVER_INFORMATION,))
            thread_list.append(t)
            t.start()

        for t in thread_list:
            t.join()

        best_response = ""
        file_name = split_command[2]

        if len(self.response_list) == 0:
            print(RED + "{} Could Not Find {}!".format(self.name, file_name))
            return
        else:
            minimum_delay = self.wait_for_response_interval
            # print("Responses:")
            for response in self.response_list:
                # print("\t" + response)
                split_response = response.split(' ')
                if float(split_response[4]) < minimum_delay:
                    minimum_delay = float(split_response[4])
                    best_response = response
        # print("\tbest response = " + best_response)

        thread_list.clear()
        best_response_split = best_response.split()
        tcp_port = int(best_response_split[1])
        source = best_response_split[0]
        threading.Thread(target=self.TCP_client, args=(tcp_port, file_name, source,)).start()
        self.response_list.clear()


    def client_receive_GET_response(self, client, msg, SERVER_INFORMATION):
        try:
            client.sendto(msg, SERVER_INFORMATION)
            client.settimeout(self.wait_for_response_interval)
            response, server = client.recvfrom(1024)
            stop_time = time.time()
            start_time = 0
            response = response.decode(NetWolf.ENCODING)
            split_response = response.split(' ')
            for i in NetWolf.timer_dic:
                if split_response[2] == i:
                    start_time = float(NetWolf.timer_dic.get(i))
                    break
            # print("start time = {}".format(start_time))
            # print("stop  time = {}".format(stop_time))
            # print("delay      = {}".format(stop_time - start_time))
            # print("UDP CLIENT {}: RECEIVED RESPONSE \"{}\"".format(self.name, response))
            delay = stop_time - start_time
            response = split_response[0] + " " + split_response[1] + " delay = " + str(delay)
            self.response_list.append(response)
        except socket.timeout:
            # print("UDP CLIENT {}: GOT NO RESPONSE".format(self.name))
            client.close()


    def TCP_client(self, port, file_name, source):
        SERVER_INFORMATION = (self.address, port)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        name = self.name + "//" + file_name
        status = 'success'
        try:
            client.connect(SERVER_INFORMATION)
            client.send(file_name.encode(self.ENCODING))
            with open(name + ".raw", 'wb') as f:
                print(RESET + "{} Wants To Get {} from {}".format(self.name, file_name, source))
                while True:
                    data = client.recv(1024 * 1000)
                    if not data:
                        break
                    f.write(data)
            f.close()
            client.close()
            print(GREEN + '{} Successfully Received {}'.format(self.name, file_name))
            self.get_history.append(source)
        except:
            print(RED + "{} Could Not Connect To {} Due To Congestion!".format(self.name, source))
            os.remove(name + ".raw")
            status = 'fail'

        try:
            if status == 'success':
                os.rename(name + ".raw", name)
            elif status == 'fail':
                os.remove(name + ".raw")
        except:
            pass

        files_in_folder = os.listdir(self.name)
        for item in files_in_folder:
            if '.raw' in item:
                os.remove(self.name + "//" + item)