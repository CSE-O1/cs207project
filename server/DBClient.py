import sys
from server.Client import Client
from simsearch.findKthSimilarity import load_ts_data
from storagemanager.FileStorageManager import FileStorageManager

class DBClient(Client):
    def __init__(self, port_num):
        super(DBClient, self).__init__(port_num)
        self._fsm = FileStorageManager()

    def query(self, q):
        return_ts = self.sender(q)
        return return_ts

if __name__ == "__main__":
    ts_client = DBClient(int(sys.argv[1]))
    if "txt" in sys.argv[2]:
        return_ts = ts_client.query(sys.argv[2])
    else:
        return_ts = ts_client.query(int(sys.argv[2]))
    print(return_ts)