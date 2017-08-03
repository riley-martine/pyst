#!/usr/bin/python3

import argparse
import sys

try:
    from screen import Screen
except ModuleNotFoundError:
    from .screen import Screen



def parse_args(args):
    parser = argparse.ArgumentParser(description='Python tiler for non-tiling wms')
    subparsers = parser.add_subparsers(help='sub-command help', dest='cmd')
    
    parser_english = subparsers.add_parser('move', help='English Move Commands')
    parser_english.add_argument('location', type=str, help='Enter one of the available choices', choices=['right', 'left', 'bottom', 'top', 'top_left', 'top_right', 'bottom_left', 'bottom_right', 'maximize'])
    
    parser_api = subparsers.add_parser('explicit', help='Direct API Interface')
    parser_api.add_argument('screen_columns', type=int)
    parser_api.add_argument('screen_rows', type=int)
    parser_api.add_argument('first_column', type=int)
    parser_api.add_argument('last_column', type=int)
    parser_api.add_argument('first_row', type=int)
    parser_api.add_argument('last_row', type=int)
    
    return parser.parse_args(args)


def move(location):
    mapping = {
        'top_left':     {'cols': (1,1), 'rows': (1,1)},
        'left':         {'cols': (1,1), 'rows': (1,2)},
        'bottom_left':  {'cols': (1,1), 'rows': (2,2)},
        'top':          {'cols': (1,2), 'rows': (1,1)},
        'maximize':     {'cols': (1,2), 'rows': (1,2)},
        'bottom':       {'cols': (1,2), 'rows': (2,2)},
        'top_right':    {'cols': (2,2), 'rows': (1,1)},
        'right':        {'cols': (2,2), 'rows': (1,2)},
        'bottom_right': {'cols': (2,2), 'rows': (2,2)},
    }
    screen = Screen(2,2)
    filled = mapping[location]
    coords = screen.get_coords(filled['cols'], filled['rows'])

    # I have been tearing my hair out over this one
    # WMCTRL works the first time, no problem.
    # The second time, running the same command, it ignores borders/decoration
    # The line below "resets" the geometry so it has to take it again.
    # See https://askubuntu.com/questions/576604/what-causes-the-deviation-in-the-wmctrl-window-move-command
    screen.move_active(0,0,0,0)
    screen.move_active(*coords)

def explicit_move(s_cols, s_rows, f_col, l_col, f_row, l_row):
    cols_filled = (f_col, l_col)
    rows_filled = (f_row, l_row)

    screen = Screen(s_cols, s_rows)
    coords = screen.get_coords(cols_filled, rows_filled)

    screen.move_active(0,0,0,0)
    screen.move_active(*coords)


def main(args):
    params = parse_args(args)
    
    if params.cmd == 'move':
        move(params.location)
    elif params.cmd == 'explicit':
        explicit_move(params.screen_columns,
                      params.screen_rows,
                      params.first_column,
                      params.last_column,
                      params.first_row,
                      params.last_row)
    

if __name__ == "__main__":
    main( sys.argv[1:] )

