import numpy as np
import sys
from socket import *
import pickle

class Client:

    def __init__(self, port_num):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.connect(('localhost', port_num))

    def sender(self, obj):
        '''
        Send object to server, and get message back from server
        '''
        msg = pickle.dumps(obj)
        msghead = str(len(msg))
        if len(msghead) < 10:
            msghead = "0"* (10-len(msghead)) + msghead
            self._socket.send(pickle.dumps(msghead))
        while len(msg):
            nsent = self._socket.send(msg)
            msg = msg[nsent:]

        return_msghead = self._socket.recv(20)
        if not return_msghead:
            return None
        return_msglen = int(pickle.loads(return_msghead))
        return_msg = self._socket.recv(return_msglen)
        if not return_msg:
            return None
        return_dat = pickle.loads(return_msg)
        return return_dat

if __name__ == "__main__":
    ts_client = Client(int(sys.argv[1]))
    print(ts_client.sender(sys.argv[2]))



