#!/usr/bin/python3
"""Screen class for accessing screen information and moving windows."""

import subprocess
import os
import sys

DEBUG = False

class Screen(object):
    """Represents the screen."""
    def __init__(self, rows, cols, padding_bottom=20):
        """Define the screen grid in pixels based on screen size."""
        self.rows = rows
        self.cols = cols
        self.padding_bottom = padding_bottom

        # All workspaces and their data
        desk_output = subprocess.getoutput("wmctrl -d").split("\n")
        # All workspace numbers
        # desk_list = [line.split()[0] for line in desk_output]

        # Data about current desktop. Not sure how it works with multiple.
        current = [line for line in desk_output if line.split()[1] == "*"][0].split()

        self.desktop = current[0]
        self.width, self.height = map(int, current[8].split('x'))
        self.orig_x, self.orig_y = current[7].split(',')

        row_division = self.height // self.rows
        col_division = self.width // self.cols


        self.grid = []
        for rownum in range(rows):
            row = []
            for colnum in range(cols):
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
        x_final_coord =  self.grid[0][col_end - 1][0][1]
        x_coords = (x_start_coord, x_final_coord)
        
        y_start_coord = self.grid[row_start-1][0][1][0]
        y_final_coord = self.grid[row_end - 1][0][1][1] - self.padding_bottom
        y_coords = (y_start_coord, y_final_coord)


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
        self.move_coords(x, y, w, h)


    def move_coords(self, x, y, w, h):
        """Move active window to specified coords."""

        command = ','.join(map(str, [" wmctrl -r :ACTIVE: -e 0", x, y, w, h]))

        if DEBUG:
            print(command)

        os.system(command)





if __name__ == "__main__":
    screen_rows = int(sys.argv[1])
    screen_cols = int(sys.argv[2])
    first_col = int(sys.argv[3])
    last_col = int(sys.argv[4])
    first_row = int(sys.argv[5])
    last_row = int(sys.argv[6])

    cols_filled = (first_col, last_col)
    rows_filled = (first_row, last_row)

    s = Screen(screen_rows, screen_cols)

    if DEBUG:
        print(c)

    s.move_active(rows_filled, cols_filled)

