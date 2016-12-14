import types
import math
from timeseries.TSInterface import StreamTimeSeriesInterface

class SimulatedTimeSeries(StreamTimeSeriesInterface):
    """
    A stream-like time series class without storage that implements StreamTimeSeriesInterface.

    The class needs to take a generator, and could produce a chunk size of list of values each time. 
    The timeseries is moving forward chunk steps after produce is called. It also implements 
    online_mean and online_std functions, which both return SimulatedTimeSeries.

    >>> data = (x for x in range(5))
    >>> ts = SimulatedTimeSeries(data)
    >>> ts.produce(3) 
    [(0, 0), (1, 1), (2, 2)]
    >>> ts.produce(3) 
    [(3, 3), (4, 4)]
    >>> data = (x for x in range(5))
    >>> ts = SimulatedTimeSeries(data)
    >>> ts_online_mean = ts.online_mean()
    >>> ts_online_std = ts.online_std()
    >>> ts_online_mean.produce(3) 
    [(0, 0.0), (1, 0.5), (2, 1.0)]
    >>> ts_online_std.produce(3) 
    [(0, 0), (1, 0.7071067811865476)]

    """
    def __init__(self, gen):
        """
        Initialize a SimulatedTimeSeries instance, inherited from StreamTimeSeriesInterface

        The input parameter gen should be a generator, otherwise it will print an error message 
        to ask user to input a generator
        self._gen: store the generator
        self._time: record the current time
        """
        if not isinstance(gen, types.GeneratorType):
            print("start printing")
            print(gen)
            for v in gen: 
                print(v)
        assert isinstance(gen, types.GeneratorType), "SimulatedTimeSeries should be initialized by a generator"
        self._gen = gen
        self._time = 0

    def __str__(self):
        """
        Return class name and current time
        """
        class_name = type(self).__name__
        return "{}(time={})".format(class_name, self._time)

    def __repr__(self):
        """
        Return class name and current time
        """
        class_name = type(self).__name__
        return "{}(time={})".format(class_name, self._time)

    def __iter__(self):
        """
        Iterate over the generator
        """
        yield from self._gen

    def itervalues(self):
        """
        Iterate over the generator
        """
        yield from self._gen

    def produce(self, chunk=1):
        """
        Return a chunk size of list of values 

        chunk must be an integer and is set as 1 by defult. Calling this function will move 
        forward the time series chunk steps each time, but will stop when the generator reaches 
        the end. self._time is changed correspondingly.
        """
        values = []
        while len(values) < chunk:
            try:
                values.append((self._time, next(self._gen)))
                self._time += 1
            except StopIteration:
                return values
        return values
            
 
    def online_mean(self):
        """
        Return a SimulatedTimeSeries of means

        The starting point of the series of means is the current starting point of the time series.
        The mean generated each time is the mean of data from the starting time to current time.
        """

        def mean_generator():
            n = 0
            mu = 0
            for value in self._gen:
                n += 1
                delta = value - mu
                mu = mu + delta / n
                yield mu
        mean_gen = mean_generator()
        ret = SimulatedTimeSeries(mean_gen)
        return ret

    def online_std(self):
        """
        Return a SimulatedTimeSeries of standard deviations

        The starting point of the series of standard deviations is the current starting point of 
        the time series. The standard deviation generated each time is the standard deviation of 
        data from the starting time to current time.
        """

        def std_generator():
            n = 0
            mu = 0
            stddev = 0
            dev_accum = 0
            for value in self._gen:
                n += 1
                delta = value - mu
                old_mu, mu = mu, mu + delta / n
                dev_accum = dev_accum + (value - old_mu) * (value - mu)
                if n > 1:
                    stddev = math.sqrt(dev_accum / (n - 1))
                yield stddev
        std_gen = std_generator()
        ret = SimulatedTimeSeries(std_gen)
        return ret

    def mean(self):
        """
        Return the mean of the complete sequence

        The sequence is considered infinite when the length exceeds 20000.
        When the sequence is infinite it moves 20000 steps forward and would raise ValueError,
        otherwise it exhausts the stream and returns the mean 
        """
        count = 0
        gen_mean = self.online_mean()
        while True:
            t = gen_mean.produce()
            if count > 20000:
                     raise ValueError("The time series is a infinite sequence, can't calculate mean")
            if t == []:
                return saved_t[0][1]
            saved_t = t
            count = count + 1

    def std(self):
        """
        Return the standard deviation of the complete sequence

        The sequence is considered infinite when the length exceeds 20000.
        When the sequence is infinite it moves 2000 steps forward and would raise ValueError,
        otherwise it exhausts the stream and returns the standard deviation
        """
        count = 0
        gen_std = self.online_std()
        while True:
            t = gen_std.produce()
            if count > 20000:
                     raise ValueError("The time series is a infinite sequence, can't calculate mean")
            if t == []:
                return saved_t[0][1]
            saved_t = t
            count = count + 1




