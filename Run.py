import discovery
import threading
import time



def create_object(name, udp_port):
    discovery.Server(name, udp_port)


if __name__ == '__main__':

    threading.Thread(target=create_object, args=("N1", 7447)).start()
    time.sleep(0.05)
    threading.Thread(target=create_object, args=("N2", 7448)).start()
    time.sleep(0.05)
    threading.Thread(target=create_object, args=("N3", 7449)).start()
