from socket import *
import numpy as np
import pickle
import logging
import sys

class Server:
    def __init__(self, port_num):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind(("", port_num))
        self._socket.listen(5)
        self._close = False

    def handler(self, conn):
        '''
        Receive query from client and processing the query.
        Call process to handling data, and get message to return to client.
        '''
        msghead = conn.recv(20)
        if not msghead:
            return
        msglen = int(pickle.loads(msghead))
        while True:
            msg = conn.recv(msglen)
            if not msg:
                break
            dat = pickle.loads(msg)
            if dat == "close":
                self._close = True
                break

            return_obj = self.process(dat, conn)

            return_msg = pickle.dumps(return_obj)
            return_msghead = str(len(return_msg))
            if len(return_msghead) < 10:
                return_msghead = "0" * (10 - len(return_msghead)) + return_msghead
                conn.send(pickle.dumps(return_msghead))
            while len(return_msg):
                nsent = conn.send(return_msg)
                return_msg = return_msg[nsent:]

    def shutdown(self):
        self._socket.close()

    def start(self):
        while True:
            conn, addr = self._socket.accept()
            logging.info("Connection from {0}".format(addr))
            self.handler(conn)
            if self._close:
                self.shutdown()
                break

    def process(self, dat, conn):
        '''
        Main function you should implement to process incoming messages,
        and possibly return some messages to client via conn.
        '''

        #processing data
        print(dat)

        #data to be returned to client
        return str(dat) + "done"

if __name__ == "__main__":
    ts_server = Server(int(sys.argv[1]))
    ts_server.start()

