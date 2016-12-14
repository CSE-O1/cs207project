import sys
from server.Server import Server
from server.pgDB import postgresAPI
from storagemanager.FileStorageManager import FileStorageManager
from timeseries.ArrayTimeSeries import ArrayTimeSeries
from simsearch.findKthSimilarity import max_similarity_search, kth_similarity_search


class DBServer(Server):
    def __init__(self, port_num):
        super(DBServer, self).__init__(port_num)
        self._postgres = postgresAPI(host='localhost', dbname='ubuntu', user='ubuntu', password='cs207password',
                                     table='meta')

    def process(self, dat, conn):
        fsm = FileStorageManager()
        query = dat['type']
        if query == "all":
            result = self._postgres.query_all()
        elif query == "mean_in":
            result = self._postgres.query_mean_range(dat['mean_in'])
        elif query == "level_in":
            result = self._postgres.query_level(dat['level_in'])
        elif query == "ts_data":
            msg = dat['ts_data']
            result = fsm.store(msg[0], ArrayTimeSeries(msg[1], msg[2]))
        elif query == "id":
            msg = dat['id']
            result = {}
            try:
                result['tsdata'] = fsm.get(msg)
                result['exist'] = 1
                result['metadata'] = self._postgres.query_id(msg)
            except ValueError:
                result['exist'] = 0
        elif query == "ss_id":
            msg_id = dat['id']
            msg_k = dat['k']
            result = []
            try:
                ts = fsm.get(msg_id)
                min_dis, min_db_name, min_ts_file_name = max_similarity_search(ts)
                result = kth_similarity_search(ts, min_dis, min_db_name, msg_k)
                print(result)
            except ValueError:
                pass
        elif query == "ss_tsdata":
            ts = dat['tsdata']
            msg_k = dat['k']
            min_dis, min_db_name, min_ts_file_name = max_similarity_search(ts)
            result = kth_similarity_search(ts, min_dis, min_db_name, msg_k)
        else:
            raise NotImplementedError

        return result


if __name__ == "__main__":
    ts_server = DBServer(int(sys.argv[1]))
    ts_server.start()
