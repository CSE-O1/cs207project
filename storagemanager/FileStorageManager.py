from SMInterface import StorageManagerInterface

class FileStorageManager(StorageManagerInterface):

    def __init__(self):
        """
        Constructor of FileStorageManager
        """

    def store(self, id, t):
        """
        Store the given timeseries in database
        :param id: Assigned ID of timeseries,
        :param t: The timeseries to store
        :type id: int or string
        :type t: SizedContainerTimeSeriesInterface
        :return: The same timeseries
        :rtype: SizedContainerTimeSeriesInterface
        """

    def size(self, id):
        """
        Get the size of timeseries with given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: Size of the timeseries
        :rtype: int
        """

    def get(self, id):
        """
        Get the timeseries of given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: Timeseries of given ID
        :rtype: SizedContainerTimeSeriesInterface
        """
