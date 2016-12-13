import numpy as np
import sys
from socket import *
import pickle

class Client:

    def __init__(self, port_num):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.connect(('localhost', port_num))

    def sender(self, obj):
        msg = pickle.dumps(obj)
        msghead = str(len(msg))
        if len(msghead) < 10:
            msghead = "0"* (10-len(msghead)) + msghead
            self._socket.send(pickle.dumps(msghead))
        while len(msg):
            nsent = self._socket.send(msg)
            msg = msg[nsent:]

if __name__ == "__main__":
    ts_client = Client(int(sys.argv[1]))
    ts_client.sender(sys.argv[2])



