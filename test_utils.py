from unittest import TestCase
from utils import *

class Test(TestCase):
    def test_flatten(self):
        self.assertEqual(flatten([]), [])
        self.assertEqual(flatten([[[], []], []]), [])
        self.assertEqual(flatten([1]), [1])
        self.assertEqual(flatten([1, [], [], 2]), [1, 2])
        self.assertEqual(flatten([[[1]], [[], [3]]]), [1, 3])
