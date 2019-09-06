import unittest
from ..car import Vector2d


class TestList(unittest.TestCase):
    def test_vector_2d(self):
        vector_list = []
        x = Vector2d(2, 3)
        vector_list.append(x)
        x.set_x(3)
        x.set_y(5)
        vector_list.append(x)
        self.assertEqual(
            vector_list,
            [x, x]
        )

        vector_list = []
        x = Vector2d(2, 3)
        y = x.copy()
        vector_list.append(y)
        x.set_x(3)
        x.set_y(5)
        vector_list.append(x)
        self.assertEqual(
            vector_list,
            [y, x]
        )
