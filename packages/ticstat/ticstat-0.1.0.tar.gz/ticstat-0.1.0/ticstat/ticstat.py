""" A class implementing a simple timer with a nice time display and
a TicStat.

"""
from datetime import datetime
from math import log10
from time import perf_counter
from typing import Iterable

class Timer:
    """ Simple timer to get the elapsed time in a nice formatted string """
    def __init__(self):
        """ Create a new timer. The time is started at creation."""
        self.init_time = perf_counter()
        self.stop_time = None

    def stop(self) -> str:
        """ Stop the timer."""
        self.stop_time = perf_counter()
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Elapsed time: {format_seconds(self.elapsed)}"

    def __str__(self) -> str:
        """ A nice string representation of the time with hours, minutes and seconds."""
        return format_seconds(self.elapsed)

    @property
    def elapsed(self) -> float:
        """ The elapsed between init and stop (or now if the timer is not stopped)."""
        if self.stop_time is None:
            return perf_counter() - self.init_time
        else:
            return self.stop_time - self.init_time


class TicStat:
    """ Timing of execution time with multiple tic. Useful for logging also.
    After initialisation, Timing.tic print useful information about the
    process. Can be used as a context manager.
    """
    level = 0  # depth of the timing (for display)
    logger = None

    def __init__(self,
                 length: int = 0,
                 name: str = "Calcalation",
                 min_update_time: float = 10.0,
                 printer=print,
                 preprint="\n",
                 ):
        """ A new timing. Increase the level by 1 until finished is called.
        Parameters
        ----------
        name: str
            A name for this timer
        nbsteps: int
            If set, will be use to track the number of steps left todo with
            time estimation.
        printer: function
            function to use to print. Default: print
        min_update_time: float
            minimal time between two stat print. default 10.0s
        """
        self.nbsteps = length
        self._step = 0

        self.name = name
        self.printer = printer
        self.min_update_time = min_update_time
        self.preprint = preprint

        self._tics = [perf_counter(), ]
        self._last_update_time = self._tics[-1] - min_update_time / 2
        self._period_time = 0.0

        # period scaling. use to update the estimated period time
        self._ps1 = 0.9
        self._ps2 = 0.1

        self.starting()

    @property
    def steps_done(self):
        """ Number of steps completed. """
        return len(self._tics) - 1

    @property
    def steps_todo(self):
        """ Number of steps left to do."""
        return self.nbsteps - self.steps_done

    @property
    def elapsed_time(self):
        """ Time elapsed since the last tic."""
        return self._tics[-1] - self._tics[0]

    @property
    def last_period(self):
        """ Time elapsed between the two last tics."""
        return self._tics[-1] - self._tics[-2]

    @property
    def estimated_time_left(self):
        """ Estimation of the time left."""
        return self._period_time * self.steps_todo

    @property
    def estimated_total_time(self):
        """ Estimation of the total time."""
        return self.estimated_time_left + self.elapsed_time

    def tic(self, extra_info: dict=None):
        """ Clock tic. Print info about the timing."""
        self._tics.append(perf_counter())

        if self._period_time > 0.0:
            self._period_time = self._ps1 * self._period_time + self._ps2 * self.last_period
        else:
            self._period_time = self.last_period

        if (self._tics[-1] - self._last_update_time) > self.min_update_time:
            self._last_update_time = self._tics[-1]
            self.printer(self.stat(extra_info))

    def starting(self):
        if self.nbsteps > 0:
            self.printer(self.format(**{
                "Starting time": str(datetime.now()),
                "Number of steps": self.nbsteps
            }))
        else:
            self.printer(self.format(**{
                "Starting time": str(datetime.now()),
            }))

    def finished(self):
        if self.nbsteps > 0:
            self.printer(self.format(**{
                "End time": str(datetime.now()),
                "Run time": format_seconds(self.elapsed_time)
            }))
        else:
            self.printer(self.format(**{
                "End time": str(datetime.now()),
            }))

    def stat(self, extra_info: dict=None) -> str:
        """ Statistics about the current step."""
        if extra_info is None:
            extra_info = {}
        if self.nbsteps > 0:
            return self.format(**{
                "Step": f"{self.steps_done} / {self.nbsteps}",
                "Time elapsed": f"{format_seconds(self.elapsed_time)}",
                "Time left": f"{format_seconds(self.estimated_time_left)}",
                "Total runtime": f"{format_seconds(self.estimated_total_time)}",
                "Time per step": f"{format_seconds(self._period_time)}",
                **extra_info
            })
        else:
            return self.format(**{
                "Step": f"{self.steps_done}",
                "Time elapsed": f"{format_seconds(self.elapsed_time)}",
                "Time per step": f"{format_seconds(self._period_time)}",
                **extra_info
            })

    def format(self, **kwargs):
        if self.preprint is not None:
            return self.preprint + "\n".join(self._format_info_(**kwargs))
        else:
            return "\n".join(self._format_info_(**kwargs))

    def _format_info_(self, **kwargs):
        maxlen = max((len(k) for k in kwargs.keys())) + 4
        kv = list(kwargs.items())

        yield f" ┌──── {self.name}"

        for k, v in kv[:-1]:
            s = k + ":"
            yield f" ├─ {s:{maxlen}} {v}"

        k, v = kv[-1]
        s = k + ":"
        yield f" └─ {s:{maxlen}} {v}"

    def __enter__(self):
        """ Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the context manager."""
        self.finished()


def format_seconds(seconds: float) -> str:
    """Nice format for seconds with hours and minutes values if needed.

    Example:
        0.02 -> "20.0ms"
        12.2 -> "12.200s"
        78.4 -> "1m 18.40s"
        4000 -> "1h 6m 40.0s"
    """
    if seconds < 1:
        return f"{seconds*1000:.1f}ms  ({seconds:g} s)"
    if seconds < 60:
        return f"{seconds:.3f}s  ({seconds:g} s)"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes):d}m {seconds:.2f}s  ({seconds:g} s)"
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):d}h {int(minutes):d}m {seconds:.1f}s  ({seconds:g} s) "


def format_number(i: int, total: int, zero_indexed=True) -> str:
    """ Format a number to have the right number of leading zero for a nice
    ordering.

    Parameters
    ----------
    i: int
        value to convert to a str
    total: int
        max value to convert
    zero_indexed: bool
        Should the numbering start at zero or one

    Examples
    --------
    >>> format_number(1, 100)
    '01'
    >>> format_number(1, 100, zero_indexed=False)
    '001'
    """
    if zero_indexed:
        total = total - 1
    if total < 1:
        return f"{i}"
    return f"{i:0{int(log10(total)) + 1}}"


if __name__ == "__main__":
    import random
    import time
    import logging

    with TicStat(10, name="test", min_update_time=1.0) as ts:
        for i in range(10):
            t = random.randint(0, 10) / 10
            time.sleep(t)
            ts.tic({"extra": f"info - {i}"})

    with TicStat(name="test", printer=print, min_update_time=1.0) as ts:
        for i in range(10):
            t = random.randint(0, 10) / 10
            time.sleep(t)
            ts.tic({"extra": f"info - {i}"})

    log = logging.getLogger(__name__)
    log.setLevel("INFO")
    with TicStat(1000, name="test", printer=log.error, min_update_time=1.0) as ts:
        for i in range(10):
            t = random.randint(0, 10) / 10
            time.sleep(t)
            ts.tic({"extra": f"info - {i}"})

