#!/usr/bin/python3

import argparse
import sys
from .screen import Screen



def main(args):
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

def explicit_move(cols, rows, f_col, l_col, f_row, l_row):
    pass

if __name__ == "__main__":
    args = main( sys.argv[1:] )
    if args.cmd == 'move':
        move(args.location)
    elif args.cmd == 'explicit':
        explicit_move(args.screen_columns,
                      args.screen_rows,
                      args.first_column,
                      args.last_column,
                      args.first_row,
                      args.last_row)

