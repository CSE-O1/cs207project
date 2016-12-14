import os
import sys
import shutil
import numpy as np
import random
import timeseries.ArrayTimeSeries as ts
import simsearch.SimilaritySearch as ss
import simsearch.database as rbtreeDB
from storagemanager.FileStorageManager import FileStorageManager
from concurrent import futures

fsm = FileStorageManager()

def gen_vps(num):
    "generate vantage point"
    vp_indexes = random.sample(range(1000), num)
    vps_list = []
    for i in range(num):
        vp_ts = fsm.get(vp_indexes[i])
        std_vp_ts = ss.standardize(vp_ts)
        vps_list.append(std_vp_ts)
    return vps_list


def save_vp_dbs(num, vps_list):
    "save vantage point in btreeDB given in LAB10"
    for index in range(num):
        db_name = "vpDB/db_" + str(index) + ".dbdb"
        db = rbtreeDB.connect(db_name)
        for i in fsm.id:
            print(i)
            comp_ts = fsm.get(i)
            std_comp_ts = ss.standardize(comp_ts)
            dis_to_vp = ss.kernel_dis(vps_list[index], std_comp_ts)
            db.set(dis_to_vp, str(i))
        db.commit()
        db.close()


def save_vp_dbs_kernel(index, vps):
    """
    store distance between vp to ts into vp database
    """
    db_name = "vpDB/db_" + str(index) + ".dbdb"
    db = rbtreeDB.connect(db_name)
    for i in fsm.id:
        comp_ts = fsm.get(i)
        std_comp_ts = ss.standardize(comp_ts)
        dis_to_vp = ss.kernel_dis(vps, std_comp_ts)
        db.set(dis_to_vp, str(i))
    db.commit()
    db.close()


def gen_dbs(num):
    "main function of generate vantage point database"
    if os.path.isdir('vpDB'):
        shutil.rmtree('vpDB')
    os.mkdir('vpDB')
    vps = gen_vps(num)
    with futures.ProcessPoolExecutor(max_workers=10) as pool:
        for index in range(num):
            pool.submit(save_vp_dbs_kernel, index, vps[index])
    #save_vp_dbs(num, vps)

if __name__ == "__main__":
    gen_dbs(20)
