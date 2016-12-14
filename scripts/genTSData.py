import os
import sys
from simsearch.SimilaritySearch import tsmaker
from storagemanager.FileStorageManager import FileStorageManager
import numpy as np
import shutil

def gen_ts_data(num):
    "generate given number of random timeseries data"
    if os.path.isdir('data'):
        shutil.rmtree('data')
    os.mkdir('data')
    fsm = FileStorageManager()
    for i in range(num):
        t1 = tsmaker(0.5, 0.1, 0.01)
        fsm.store(i, t1)
    return

if __name__ == "__main__":
    gen_ts_data(1000)
