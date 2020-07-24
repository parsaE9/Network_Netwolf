import threading



def create_object():
    print("create object")


if __name__ == '__main__':

    threading.Thread(target=create_object, ).start()

    print("main")