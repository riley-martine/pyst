Pystiler (a PYthon Simple TILER)
================================

.. image:: https://badge.fury.io/py/pystiler.svg
       :target: https://badge.fury.io/py/pystiler


The goal of this project is to be able to define tiled workspaces and
open them with ease on non-tiling wms.

This is a simple python script which wraps wmctrl to allow for easier
tiling.

Bind it to a key or to autowhatever-on-window-creation-hook, create scripts to setup a workspace, or make aliases to quickly move terminals.


Install
~~~~~~~
Install with 
:: 
    pip3 install pystiler


run simple commands with

::

    pyst move <arg>


Currently arguments are

left, right

top, bottom

top\_left, bottom\_left

top\_right, bottom\_right

maximize

All of which do pretty much what you'd expect to the active window.


run more complex commands with

::

    pyst explicit <screen rows> <screen columns> <first column> <last column> <first row> <last row>


eg.

::

    pyst explicit 2 3 2 2 1 2

defines a screen grid of dimensions 2 rows, 3 columns, and resizes the active window to fill the second column only, first through second row. (so, the window would now occupy the center vertical third of the screen) 

and

::
    
    pyst explicit 3 2 1 2 1 2

defines a screen grid of 3 rows, 2 columns, and resizes the active window to fill the first through second row of the first through second column (the top 2/3 of the screen)



Todos for the project
~~~~~~~~~~~~~~~~~~~~~

-  [x] Add top and bottom targets
-  [x] Add [top,bottom][left,right] targets
-  [x] Add simple CLI interface
-  [x] Add simple test cases
-  [x] Make nice python package
-  [ ] Add tests for window resizing
-  [ ] Make explicit api nicer
-  [ ] Find out why cols and rows reverse and fix it
-  [ ] Find out what's causing wmctrl to misfire on second call
-  [ ] Find out what bug fixes others have done
-  [ ] Map out final goals of project
-  [ ] Make list of already-resized window IDs to mitigate the resizing
   problem
