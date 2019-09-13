from abc import ABC, abstractmethod
from typing import List

import numpy as np


class FilteredInfo(ABC):
    def compile(self):
        """Filtered info holds on to the information a filter needs to operate one step."""
        raise NotImplementedError


class Filter(ABC):
    @abstractmethod
    def do_recursion_step(self, new_observation: np.array, filtered_info: FilteredInfo) -> FilteredInfo:
        """A filter will do a recursion step, i.e. return update filtered information according to a new observation."""
        raise NotImplementedError

    @abstractmethod
    def filter(self, time_series: List) -> List[FilteredInfo]:
        """A filter will implement a filter method."""
        raise NotImplementedError
