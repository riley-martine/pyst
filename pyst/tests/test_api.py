import unittest

import pystiler

class TestParser(unittest.TestCase):

    def test_move_parser(self):
        args = pystiler.api.parse_args(['move', 'left'])
        self.assertEqual(args.cmd, 'move')
        self.assertEqual(args.location, 'left')

    def test_all_directions(self):
        for direction in ['right', 'left', 'bottom', 'top', 'top_left', 'top_right', 'bottom_left', 'bottom_right', 'maximize']:
            with self.subTest(direction=direction):
                args = pystiler.api.parse_args(['move', direction])
                self.assertEqual(args.cmd, 'move')
                self.assertEqual(args.location, direction)

    def test_explicit_parser(self):
        args = pystiler.api.parse_args(['explicit', '1', '2', '3', '4', '5', '6'])
        self.assertEqual(args.cmd, 'explicit')
        self.assertEqual(args.screen_columns, 1)
        self.assertEqual(args.screen_rows, 2)
        self.assertEqual(args.first_column, 3)
        self.assertEqual(args.last_column, 4)
        self.assertEqual(args.first_row, 5)
        self.assertEqual(args.last_row, 6)


