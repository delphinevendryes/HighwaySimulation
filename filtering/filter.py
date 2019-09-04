from abc import ABC, abstractmethod
from typing import List


class Filter(ABC):
    @abstractmethod
    def filter(self, time_series: List):
        """A filter will implement a filter method."""
        raise NotImplementedError
