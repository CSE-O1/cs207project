""" Interface Module for Storage Manager.
This module defines the abstract interface class StorageManagerInterface
 for the FileStorageManager class.

Classes
-------
StorageManagerInterface(abc.ABC):
    Define the abstract class for the FileStorageManager class

Methods
-------
store:
    Abstract method for storing a timeseries in database
size:
    Abstract method for getting the size of a timeseries with the given ID
get:
    Abstract method for getting a timeseries with the given ID
"""

import abc


class StorageManagerInterface(abc.ABC):
    """
    StorageManagerInterface(abc.ABC):
    Define the abstract class for the FileStorageManager class

    Methods
    -------
    store:
        Abstract method for storing a timeseries in database
    size:
        Abstract method for getting the size of a timeseries with the given ID
    get:
        Abstract method for getting a timeseries with the given ID
    """
    @abc.abstractmethod
    def store(self, id, t):
        """
        Store the given timeseries in database
        :param id: the assigned ID of the timeseries,
        :param t: the timeseries to store
        :type id: int or string
        :type t: SizedContainerTimeSeriesInterface
        :return: the same timeseries
        :rtype: SizedContainerTimeSeriesInterface
        """

    @abc.abstractmethod
    def size(self, id):
        """
        Get the size of a timeseries with the given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: size of the timeseries
        :rtype: int
        """

    @abc.abstractmethod
    def get(self, id):
        """
        Get a timeseries with the given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: timeseries of the given ID
        :rtype: SizedContainerTimeSeriesInterface
        """
