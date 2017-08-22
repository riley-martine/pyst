#!/usr/bin/python3
"""API interface for pystiler.screen."""

import argparse
import sys

try:
    from screen import Screen, move_coords
except ModuleNotFoundError:
    from pystiler.screen import Screen, move_coords


def parse_args(args):
    """Wrapper that parses CLI arguments via argparse and returns the parsed args."""
    parser = argparse.ArgumentParser(description='Python tiler for non-tiling wms')
    subparsers = parser.add_subparsers(help='sub-command help', dest='cmd')

    parser_english = subparsers.add_parser('move', help='English Move Commands')
    directions = [
        'right',
        'left',
        'bottom',
        'top',
        'top_left',
        'top_right',
        'bottom_left',
        'bottom_right',
        'maximize']
    parser_english.add_argument(
        'location',
        type=str,
        help='Enter one of the available choices',
        choices=directions)

    parser_api = subparsers.add_parser('explicit', help='Direct API Interface')
    parser_api.add_argument('screen_columns', type=int)
    parser_api.add_argument('screen_rows', type=int)
    parser_api.add_argument('first_column', type=int)
    parser_api.add_argument('last_column', type=int)
    parser_api.add_argument('first_row', type=int)
    parser_api.add_argument('last_row', type=int)

    return parser.parse_args(args)


def move(location):
    """Move via an english location."""
    mapping = {
        'top_left':     {'cols': (1, 1), 'rows': (1, 1)},
        'left':         {'cols': (1, 1), 'rows': (1, 2)},
        'bottom_left':  {'cols': (1, 1), 'rows': (2, 2)},
        'top':          {'cols': (1, 2), 'rows': (1, 1)},
        'maximize':     {'cols': (1, 2), 'rows': (1, 2)},
        'bottom':       {'cols': (1, 2), 'rows': (2, 2)},
        'top_right':    {'cols': (2, 2), 'rows': (1, 1)},
        'right':        {'cols': (2, 2), 'rows': (1, 2)},
        'bottom_right': {'cols': (2, 2), 'rows': (2, 2)},
    }
    screen = Screen(2, 2)
    filled = mapping[location]
    cols_filled = filled['cols']
    rows_filled = filled['rows']

    # I have been tearing my hair out over this one
    # WMCTRL works the first time, no problem.
    # The second time, running the same command, it ignores borders/decoration
    # The line below "resets" the geometry so it has to take it again.
    # See askubuntu.com/questions/576604/what-causes-the-deviation-in-the-wmctrl-window-move-command
    move_coords(0, 0, 0, 0)
    screen.move_active(cols_filled, rows_filled)

def explicit_move(screen_grid, cols_filled, rows_filled):
    """Move via an explicit grid location specification."""

    screen = Screen(screen_grid[0], screen_grid[1])

    # See comment in move()
    move_coords(0, 0, 0, 0)
    screen.move_active(cols_filled, rows_filled)


def main(args=None):
    """Parse args and then do the moving according to them."""
    if not args:
        args = sys.argv[1:]

    params = parse_args(args)

    if params.cmd == 'move':
        move(params.location)
    elif params.cmd == 'explicit':
        screen_grid = (params.screen_columns, params.screen_rows)
        cols_filled = (params.first_column, params.last_column)
        rows_filled = (params.first_row, params.last_row)
        explicit_move(screen_grid, cols_filled, rows_filled)



if __name__ == "__main__":
    main(sys.argv[1:])

