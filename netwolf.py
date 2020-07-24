import time
import socket
import threading
import random
import functions
import os


class NetWolf:

    ENCODING = 'utf-8'
    MESSAGE_LENGTH_SIZE = 64
    peers_count = 0
    timer_dic = {}

    def __init__(self, name, udp_port):

        self.name = name
        self.address = socket.gethostbyname(socket.gethostname())
        self.udp_port = udp_port
        self.tcp_port = random.randint(5000,7430)
        self.wait_for_response_interval = 2
        self.maximum_request_to_respond = 4
        self.response_list = []
        self.get_history = []

        NetWolf.peers_count += 1

        threading.Thread(target=self.UDP_server, args=()).start()
        threading.Thread(target=self.TCP_server, args=()).start()
        time.sleep(0.35)
        threading.Thread(target=self.UDP_client, args=()).start()


    def UDP_server(self):

        HOST_INFORMATION = (self.address, self.udp_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(HOST_INFORMATION)
        print("[UDP SERVER {} STARTS]".format(self.name))

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
                    index = len(NetWolf.timer_dic) + 1
                    start_time = time.time()
                    if not split_data[2] in self.get_history:
                        time.sleep(round(random.uniform(0.5, 1), 2))
                    NetWolf.timer_dic.update({str(index) : str(start_time)})
                    msg = "{} {} {}".format(self.name, self.tcp_port, str(index))
                    server.sendto(msg.encode(self.ENCODING), address)


    def TCP_server(self):
        HOST_INFORMATION = (self.address, self.tcp_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(HOST_INFORMATION)
        print("[TCP SERVER {} STARTS]".format(self.name))
        server.listen(5)
        while True:
            conn, address = server.accept()
            threading.Thread(target=self.handle_client, args=(conn, address)).start()


    def handle_client(self, connection, address):

        print("[SERVER {}] NEW CONNECTION FROM {}".format(self.name, address))
        name = connection.recv(1024).decode(self.ENCODING)
        filename = self.name + "//" + name
        f = open(filename, 'rb')
        l = f.read(1024)
        while l:
            connection.send(l)
            # print('Sent ', repr(l))
            l = f.read(1024 * 1000)
        f.close()
        connection.close()
        print('Done sending')


    def UDP_client(self):
        threading.Thread(target=self.UDP_discovery, args=()).start()
        threading.Thread(target=self.UDP_GET, args=()).start()


    def UDP_discovery(self):

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

            if NetWolf.peers_count == line_count + 1:
                time.sleep(3)
            else:
                time.sleep(round(random.uniform(2, 2.5), 2))


    def UDP_GET(self):

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
                    msg = split_command[1] + " " + split_command[2] + " " + split_command[0]
                    msg = msg.encode(self.ENCODING)
                    t = threading.Thread(target=self.client_receive_GET_response, args=(client, msg, SERVER_INFORMATION, ))
                    thread_list.append(t)
                    t.start()

                for t in thread_list:
                    t.join()

                best_response = ""

                if len(self.response_list) == 0:
                    print("Could Not Find Requested File!")
                else:
                    minimum_delay = self.wait_for_response_interval
                    print("Responses:")
                    for response in self.response_list:
                        print("\t" + response)
                        split_response = response.split(' ')
                        if float(split_response[4]) < minimum_delay:
                            minimum_delay = float(split_response[4])
                            best_response = response

                print("\tbest response = " + best_response)

                self.response_list.clear()
                thread_list.clear()
                functions.delete_command_file()
                best_response_split = best_response.split()
                tcp_port = int(best_response_split[1])
                self.get_history.append(best_response_split[0])
                file_name = split_command[2]

                threading.Thread(target=self.TCP_client, args=(tcp_port, file_name,)).start()


    def client_receive_GET_response(self, client, msg, SERVER_INFORMATION):
        try:
            client.sendto(msg, SERVER_INFORMATION)
            client.settimeout(2)
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


    def TCP_client(self, port, file_name):
        SERVER_INFORMATION = (self.address, port)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(SERVER_INFORMATION)
        client.send(file_name.encode(self.ENCODING))
        with open(self.name + "//" + file_name, 'wb') as f:
            # print('file opened')
            while True:
                # print('receiving data...')
                data = client.recv(1024 * 1000)
                # print('data=%s', data)
                if not data:
                    break
                f.write(data)
        f.close()
        print('Successfully received the file')
        client.close()
