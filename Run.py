import functions
import netwolf
import threading
import time


def create_object(name, udp_port, discovery_msg_interval, wait_for_response_interval, maximum_TCP_connections):
    """
    :param name: node name , must be N1 or N2 or ...
    :param udp_port: node UDP port
    :param discovery_msg_interval: discovery message interval
    :param wait_for_response_interval: UDP GET wait for response interval
    :param maximum_TCP_connections: maximum TCP connections for a node
    """
    netwolf.NetWolf(name, udp_port, discovery_msg_interval, wait_for_response_interval, maximum_TCP_connections)


if __name__ == '__main__':

    # creating nodes
    threading.Thread(target=create_object, args=("N1", 7447, 2, 2, 4)).start()
    time.sleep(0.05)
    threading.Thread(target=create_object, args=("N2", 7448, 2, 2, 4)).start()
    time.sleep(0.05)
    threading.Thread(target=create_object, args=("N3", 7449, 2, 2, 4)).start()
    time.sleep(0.05)
    threading.Thread(target=create_object, args=("N4", 7450, 2, 2, 4)).start()
    time.sleep(0.05)
    threading.Thread(target=create_object, args=("N5", 7451, 2, 2, 4)).start()

    # getting user input
    functions.get_user_input()