"""
An object that tracks X number of actions within N seconds

Author: Preocts <Preocts#8196>
"""
import time
from typing import List


class DecayingCounter:
    """Tracks number of events within a given life_span of seconds"""

    def __init__(self, life_span: int, max_count: int) -> None:
        """Define the max_count number of events allowed within life_span seconds"""
        self._max = max_count
        self._events: List[float] = []
        self._life_span = life_span

    @property
    def count(self) -> int:
        """Returns count of events"""
        self._clean()
        return len(self._events)

    def inc(self) -> bool:
        """Increments event count by 1 unless max is reached, then returns false"""
        if self.count < self._max:
            self._events.append(time.time())
            return True
        else:
            return False

    def _clean(self) -> None:
        """Removes expired events from front of list"""
        while len(self._events):
            if (time.time() - self._events[0]) > self._life_span:
                self._events.pop(0)
            else:
                break
