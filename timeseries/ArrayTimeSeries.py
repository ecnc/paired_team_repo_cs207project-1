import numpy as np
import reprlib
import collections
import math
from TimeSeries import TimeSeries
from lazy import *

class ArrayTimeSeries(TimeSeries):
    """
    ArrayTimeSeries.

    TODO:
    1. testcases;
    2. documents
    """
    def __init__(self, times, values):
        self._time = np.array(times)
        self._value = np.array(values)
        self._timeseries = np.array(list(zip(self._time, self._value)))

    def __len__(self):
        return len(self._value)

    def __getitem__(self, index):
        return self._timeseries[index]

    def __setitem__(self, index, value):
        self._value[index] = value
        self._timeseries[index][1] = value

    def __str__(self):
        if len(self) > 5:
            return 'Length: {}, [{}, {}, ..., {}]'.format\
            (len(self), self._timeseries[0], self._timeseries[1],\
                self._timeseries[len(self) - 1])
        else:
            return '{}'.format([item for item in self._timeseries])

    def __repr__(self):
        if len(self) > 5:
            return 'TimeSeries(Length: {}, [{}, {}, ..., {}])'.format\
            (len(self), self._timeseries[0], self._timeseries[1],\
                self._timeseries[len(self) - 1])
        else:
            return 'TimeSeries: {}'.format([item for item in self._timeseries])

    def __iter__(self):
        for item in self._value:
            yield item

    def __contains__(self, val):
        return val in self._value

    def values(self):
        return self._value

    def times(self):
        return self._time

    def items(self):
        return self._timeseries

    def itervalues(self):
        for item in self._value:
            yield item

    def itertimes(self):
        for item in self._time:
            yield item

    def iteritems(self):
        for item in zip(self._time, self._value):
            yield item

    def __add__(self, other):
        if not isinstance(other, ArrayTimeSeries):
            raise TypeError("NotImplemented Error")
        if len(self) != len(other) or not np.allclose(self._time, other._time):
            raise ValueError(str(self)+' and '+str(other)+' must have the same time points')
        return ArrayTimeSeries(self._time, self._value + other._value)

    def __sub__(self, other):
        if not isinstance(other, ArrayTimeSeries):
            raise TypeError("NotImplemented Error")
        if len(self) != len(other) or not np.allclose(self._time, other._time):
            raise ValueError(str(self) + ' and ' + str(other) + ' must have the same time points')
        return ArrayTimeSeries(self._time, self._value - other._value)

    def __mul__(self, other):
        if not isinstance(other, ArrayTimeSeries):
            raise TypeError("NotImplemented Error")
        if len(self) != len(other) or not np.allclose(self._time, other._time):
            raise ValueError(str(self) + ' and ' + str(other) + ' must have the same time points')
        return ArrayTimeSeries(self._time, self._value * other._value)

    def __eq__(self, other):
        if not isinstance(other, ArrayTimeSeries):
            raise TypeError("NotImplemented Error")
        if len(self) != len(other) or not np.allclose(self._time, other._time):
            raise ValueError(str(self) + ' and ' + str(other) + ' must have the same time points')
        return np.all(self._value == other._value) == True and np.allclose(self._time, other._time)

    def __abs__(self):
        return math.sqrt(self._value.dot(self._value))

    def __bool__(self):
        return bool(abs(self))

    def __neg__(self):
        return ArrayTimeSeries(self._time, - self._value)

    def __pos__(self):
        return ArrayTimeSeries(self._time, self._value)

    def interpolate(self, time_seq):
        value_seq = []
        for i_t in time_seq:
            if i_t < self._time[0]:
                value_seq.append(self._time[0])
                continue
            if i_t > self._time[len(self._time) - 1]:
                value_seq.append(self._time[len(self._time) - 1])
                continue
            for i in range(len(self._time) - 1):
                if i_t >= self._time[i] and i_t <= self._time[i + 1]:
                    v_delta = self._value[i + 1] - self._value[i]
                    t_delta = self._time[i + 1] - self._time[i]
                    slop = v_delta / t_delta
                    new_v = slop * (i_t - self._time[i]) + self._value[i]
                    value_seq.append(new_v)
                    break
        return ArrayTimeSeries(time_seq, value_seq)

    @property
    def lazy(self):
        # indentity function
        identity = lambda x: x
        return LazyOperation(identity, self)


# lazy test part
@lazy
def check_length(a, b):
    return len(a) == len(b)
