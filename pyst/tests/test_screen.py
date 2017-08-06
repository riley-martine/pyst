"""Test screen functionality."""
import unittest
from pystiler.screen import Screen

class TestScreen(unittest.TestCase):

    def test_create_grid(self):
        rows, cols = 2, 3
        s = Screen(rows, cols)
        self.assertEqual(len(s.grid), rows)
        self.assertEqual(len(s.grid[0]), cols)
        self.assertEqual(len(s.grid[1]), cols)

