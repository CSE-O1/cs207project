import sys
from server.Client import Client
from simsearch.findKthSimilarity import load_ts_data
from storagemanager.FileStorageManager import FileStorageManager

class DBClient(Client):
    def __init__(self, port_num):
        """
        inite DB Client
        """
        super(DBClient, self).__init__(port_num)

    def query(self, q):
        return_ts = self.sender(q)
        return return_ts

if __name__ == "__main__":
    ts_client = DBClient(int(sys.argv[1]))
    query={}
    query['type']='id'
    query['id']=(sys.argv[2])
    return_ts = ts_client.query(query)
    if return_ts['exist']:
        print(return_ts['tsdata'])
    else:
        print('Not exist!')
#    print(return_ts)
