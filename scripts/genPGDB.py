import os
import sys
import shutil
import numpy as np
import random
from server.pgDB import postgresAPI
from storagemanager.FileStorageManager import FileStorageManager
from concurrent import futures

fsm = FileStorageManager()


def gen_pg_db():
    "main function of generate vantage point database"
    if os.path.isfile('pgDB'):
        os.remove('pgDB')

    table_now = 'meta'
    pg = postgresAPI(host='localhost', dbname='pgDB', user='ubuntu', password='cs207password', table=table_now)
    for id in fsm.id:
        ts_data = fsm.get(id)
        meta = [id,
                np.random.uniform(low=0.0, high=1.0),
                ts_data.mean(),
                ts_data.std(),
                random.choice(['A', 'B', 'C', 'D', 'E', 'F'])]
        pg.insert(meta)
    pg.close()

if __name__ == "__main__":
    gen_pg_db()
