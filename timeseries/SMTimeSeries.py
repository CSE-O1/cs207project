from Interface import SizedContainerTimeSeriesInterface

class SMTimeSeries(SizedContainerTimeSeriesInterface):

    def __init__(self, times, values, id = None):
        """
        Constructor for SMTimeSeries
        :param times:
        :param values:
        :param id:
        """
        raise NotImplementedError

    @classmethod
    def from_db(cls, id):
        """
        Look up and fetch timeseries from the storage manager
        :param id: ID of timeseries
        :type id: int or string
        :return: Timeseries
        """
        raise NotImplementedError