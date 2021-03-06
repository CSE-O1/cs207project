import os
import sys
import shutil
import numpy as np
import random
from server.pgDB import postgresAPI
from storagemanager.FileStorageManager import FileStorageManager

fsm = FileStorageManager()


def gen_pg_db():
    "main function of generate postgres database"
    #delete file if it is already existed
    if os.path.isfile('pgDB'):
        os.remove('pgDB')
    #new table
    table_now = 'meta'
    #create new postgres database
    pg = postgresAPI(host='localhost', dbname='ubuntu', user='ubuntu', password='cs207password', table=table_now)
    tmp1 = "DROP TABLE meta"
    pg._cursor.execute(tmp1)
    pg._conn.commit()
    pg.create()
    #created metadata for each timeseries
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