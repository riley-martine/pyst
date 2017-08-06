#!/usr/bin/python3
"""Screen class for accessing screen information and moving windows."""

import subprocess
import os
import sys

DEBUG = False

class Screen(object):
    """Represents the screen."""
    def __init__(self, grid_rows, grid_cols, padding_bottom=20):
        """Define the screen grid in pixels based on screen size."""
        self.padding_bottom = padding_bottom

        # All workspaces and their data
        desk_output = subprocess.getoutput("wmctrl -d").split("\n")
        # All workspace numbers
        # desk_list = [line.split()[0] for line in desk_output]
        # self.desktop = current[0]

        # Data about current desktop. Not sure how it works with multiple.
        current = [line for line in desk_output if line.split()[1] == "*"][0].split()

        width, height = [int(x) for x in current[8].split('x')]
        # self.orig_x, self.orig_y = current[7].split(',')

        row_division = height // grid_rows
        col_division = width // grid_cols


        self.grid = []
        for rownum in range(grid_rows):
            row = []
            for colnum in range(grid_cols):
                col = []
                col.append((col_division*colnum, col_division*(colnum+1)))
                col.append((row_division*rownum, row_division*(rownum+1)))
                row.append(col)
            self.grid.append(row)


        #Grid format is something like this:
        #[[(0, 640), (0, 522)],    [(640, 1280), (0, 522)],    [(1280, 1920), (0, 522)]],
        #[[(0, 640), (522, 1044)], [(640, 1280), (522, 1044)], [(1280, 1920), (522, 1044)]]

        if DEBUG:
            for i in self.grid:
                print(i)


    # umm ignore that the rows and columns switch here
    def get_coords(self, cols, rows):
        """Precondition: two two-tuples of (start,end) for rows and columns.
           Postcondition: x, y, w, h for new window location.
        """
        row_start, row_end = rows
        col_start, col_end = cols

        x_start_coord = self.grid[0][col_start-1][0][0]
        x_final_coord = self.grid[0][col_end - 1][0][1]

        y_start_coord = self.grid[row_start-1][0][1][0]
        y_final_coord = self.grid[row_end - 1][0][1][1] - self.padding_bottom


        x = x_start_coord
        y = y_start_coord
        w = x_final_coord - x_start_coord
        h = y_final_coord - y_start_coord

        return (x, y, w, h)

    def move_active(self, cols, rows):
        """Move the currently active window to specified location.
           Precondition: two two-tuples of (start,end) for rows and columns.
        """
        x, y, w, h = self.get_coords(cols, rows)
        move_coords(x, y, w, h)


def move_coords(x, y, w, h):
    """Move active window to specified coords."""

    params = ','.join([str(pix) for pix in [x, y, w, h]])
    command = " wmctrl -r :ACTIVE: -e 0," + params

    if DEBUG:
        print(command)

    os.system(command)





if __name__ == "__main__":
    GRID_ROWS = int(sys.argv[1])
    GRID_COLS = int(sys.argv[2])
    FIRST_COL = int(sys.argv[3])
    FINAL_COL = int(sys.argv[4])
    FIRST_ROW = int(sys.argv[5])
    FINAL_ROW = int(sys.argv[6])

    COLS_FILLED = (FIRST_COL, FINAL_COL)
    ROWS_FILLED = (FIRST_ROW, FINAL_ROW)

    SCREEN = Screen(GRID_ROWS, GRID_COLS)

    if DEBUG:
        print(SCREEN.get_coords(ROWS_FILLED, COLS_FILLED))

    SCREEN.move_active(ROWS_FILLED, COLS_FILLED)

