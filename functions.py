import time


RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

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


def UDP_list(name):
    file = open(name + "//" + name + "_list.txt")
    node_list = file.read()
    file.close()
    print(BLUE + node_list)


def delete_command_file(name):
    file = open(name + "//command.txt", "r+")
    file.seek(0)
    file.truncate()
    file.close()

def get_user_input():
    last_command = ''

    while True:
        time.sleep(1)
        print(CYAN + "\n******************************************************************************************************"
              "\n- Commands: \"list\"\t     \"GET\"\n- Example:  \"N1 list\"\t \"N2 GET sampleFile.txt\"")

        user_input = input("- enter Command: ")
        split_user_input = user_input.split(' ')
        if split_user_input[1].lower() == 'list' and len(split_user_input) == 2:
            user_input = split_user_input[0].upper() + " " + split_user_input[1].lower()
        elif split_user_input[1].upper() == 'GET' and len(split_user_input) == 3:
            user_input = split_user_input[0].upper() + " " + split_user_input[1].upper() + " " + split_user_input[2]
        else:
            print(RED + "- unknown Command! Try Again...")
            continue

        if last_command == split_user_input[0]:
            time.sleep(1)

        last_command = split_user_input[0]
        file_name = split_user_input[0] + "//command.txt"
        file = open(file_name, "w")
        file.write(user_input)
        file.close()