from socket import *
import numpy as np
import pickle
import logging
from storagemanager.FileStorageManager import FileStorageManager

fsm = FileStorageManager()
def send_from(connection):
    while True:
        received = connection.recv(10000)
        if not received:
            break
        dat = pickle.loads(received)
        if dat['op'] == 'id':
            ts = fsm.get(dat['id'])



    view = pickle.dumps(arr)
    while len(view):
        nsent = dest.send(view)
        view = view[nsent:]


s = socket(AF_INET, SOCK_STREAM)
s.bind(('Timeseries Database', 885310))
s.listen(5)
connection, addr = s.accept()
logging.info("Connection from {0}".format(addr))
send_from(connection)
