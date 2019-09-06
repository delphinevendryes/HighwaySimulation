from abc import ABC, abstractmethod
from typing import List

import numpy as np


class FilteredInfo(ABC):
    def compile(self):
        """Filtered info holds on to the information a filter needs to operate one step."""
        raise NotImplementedError


class Filter(ABC):
    @abstractmethod
    def do_recursion_step(self, new_observation: np.array, filtered_info: FilteredInfo):
        raise NotImplementedError

    @abstractmethod
    def filter(self, time_series: List):
        """A filter will implement a filter method."""
        raise NotImplementedError
