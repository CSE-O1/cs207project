import sys
from server.Server import Server
from simsearch.findKthSimilarity import max_similarity_search, kth_similarity_search

class DBServer(Server):
    def __init__(self, port_num):
        super(DBServer, self).__init__(port_num)

    def process(self, dat, conn):
        min_dis, min_db_name, min_ts_file_name = max_similarity_search(dat)
        kth_similarity_list = kth_similarity_search(dat, min_dis, min_db_name, 1)
        return kth_similarity_list[0]

if __name__ == "__main__":
    ts_server = DBServer(int(sys.argv[1]))
    ts_server.start()
