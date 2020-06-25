import netwolf
import threading
import time
import functions


def create_object(name, udp_port):
    netwolf.NetWolf(name, udp_port)


if __name__ == '__main__':

    threading.Thread(target=create_object, args=("N1", 7447)).start()
    time.sleep(0.05)
    threading.Thread(target=create_object, args=("N2", 7448)).start()
    time.sleep(0.05)
    threading.Thread(target=create_object, args=("N3", 7449)).start()


    functions.delete_command_file()
    while True:
        time.sleep(1)
        print("\n*************************************************************"
              "\n- Commands: \"list\"\t  \"GET\"\n- Example:  \"N1 list\"\t  \"N2 GET sampleFile.txt\"\n- Commands Are Case Sensitive!")

        user_input = input("- enter Command: ")
        file = open("command.txt", "w")
        file.write(user_input)
        file.close()

        time.sleep(1.5)
        while True:
            file = open("command.txt")
            content = file.read()
            if content == '':
                file.close()
                break
            file.close()
            time.sleep(0.55)
