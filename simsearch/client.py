import numpy as np
from socket import *
import pickle

def recv_into(arr, source):
    view = memoryview(arr).cast('B')
    while len(view):
        nrecv = source.recv_into(view)
        print("recieved", nrecv)
        view = view[nrecv:]


c = socket(AF_INET, SOCK_STREAM)
c.connect(('localhost', 25000))
a = np.zeros(shape=50000000, dtype=float)
print(a[0:10])
recv_into(a, c)
print(a[0:10])


