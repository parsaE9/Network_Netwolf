def remove_empty_lines(file_name):
    fh = open(file_name)
    lines = fh.readlines()
    fh.close()
    keep = []
    for line in lines:
        if not line.isspace():
            keep.append(line)
    fh = open(file_name, "w")
    fh.write("".join(keep))
    fh.close()


def merge_discovery_msg(name, udp_port, data, address):

    # print("[UDP SERVER {} ] DATA : {} \t RECEIVED FROM : {}".format(name, data, address))

    name_index = data.replace(':', 'X', 1).find(':')
    port_index = data.replace(':', 'X', 2).find(':')
    sender_name = data[name_index + 1: name_index + 3]
    sender_udp_port = data[port_index + 1: port_index + 5]
    sender_ip = address[0]
    sender_info = sender_name + " " + sender_ip + ":" + sender_udp_port

    file_name = name + "//" + name + "_list.txt"
    file = open(file_name)
    discovery_list = file.read()
    file.close()

    # print("[SERVER {}] SENDER INFO : {}".format(name, sender_info))

    if sender_info not in discovery_list:

        file = open(file_name, 'a')
        if discovery_list == '':
            file.write(sender_info + " NODE:" + name + " UDP_PORT:" + str(udp_port) + "\n")
        else:
            file.write("\n" + sender_info + " NODE:" + name + " UDP_PORT:" + str(udp_port))
        file.close()

    if data[0: data.find(':') + 5] not in discovery_list and name != data[0: 2]:

        file = open(file_name, 'a')
        if discovery_list == '':
            file.write(data[0: data.find(':') + 5] + " NODE:" + name + " UDP_PORT:" + str(udp_port) + "\n")
        else:
            file.write("\n" + data[0: data.find(':') + 5] + " NODE:" + name + " UDP_PORT:" + str(udp_port))
        file.close()

    remove_empty_lines(file_name)


def print_node_list(name):
    file = open(name + "//" + name + "_list.txt")
    node_list = file.read()
    file.close()
    delete_command_file()
    print(node_list)

def delete_command_file():
    file = open("command.txt", "r+")
    file.seek(0)
    file.truncate()
    file.close()
