import threading
import time

def hello():
    print("hello")
    time.sleep(1)

def hey():
    print("hey")
    time.sleep(2)


if __name__ == "__main__":

    thread_1 = threading.Thread(target=hello)
    thread_2 = threading.Thread(target=hey)

    thread_1.start()
    thread_2.start()
