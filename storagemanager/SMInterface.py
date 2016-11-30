import abc

class StorageManagerInterface(abc.ABC):
    @abc.abstractmethod
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

    @abc.abstractmethod
    def size(self, id):
        """
        Get the size of timeseries with given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: Size of the timeseries
        :rtype: int
        """

    @abc.abstractmethod
    def get(self, id):
        """
        Get the timeseries of given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: Timeseries of given ID
        :rtype: SizedContainerTimeSeriesInterface
        """
