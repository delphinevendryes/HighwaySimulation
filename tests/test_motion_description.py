from ..car import Vector2d
import numpy as np
import unittest


class TestVector2D(unittest.TestCase):
    def test_polar_coordinates(self):
        vector = Vector2d(x=0, y=0)
        r, theta = vector.to_polar()
        self.assertEqual(r, 0)
        self.assertEqual(theta, 0)

        vector = Vector2d(x=1, y=0)
        r, theta = vector.to_polar()
        self.assertEqual(r, 1)
        self.assertEqual(theta, 0)

        vector = Vector2d(x=0, y=-1)
        r, theta = vector.to_polar()
        self.assertEqual(r, 1)
        self.assertEqual(theta, - np.pi / 2)

        vector = Vector2d(x=0, y=1)
        r, theta = vector.to_polar()
        self.assertEqual(r, 1)
        self.assertEqual(theta, np.pi / 2)

        vector = Vector2d(x=-1, y=0)
        r, theta = vector.to_polar()
        self.assertEqual(r, 1)
        self.assertEqual(theta, np.pi)


