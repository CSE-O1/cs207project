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
            self.process(dat, conn)

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
        print(dat)
        conn.send(pickle.dumps("done"))

if __name__ == "__main__":
    ts_server = Server(int(sys.argv[1]))
    ts_server.start()

