Pystiler (a PYthon Simple TILER)
================================

.. image:: https://api.codacy.com/project/badge/Grade/d1f80616b8344a3d84de1016defae26d
   :target: https://www.codacy.com/app/rmartine/pyst?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=riley-martine/pyst&amp;utm_campaign=Badge_Grade

.. image:: https://badge.fury.io/py/pystiler.svg
       :target: https://badge.fury.io/py/pystiler


The goal of this project is to be able to define tiled workspaces and
open them with ease on non-tiling wms.

This is a simple python script which wraps wmctrl to allow for easier
tiling.

Bind it to a key or to autowhatever-on-window-creation-hook, create scripts to setup a workspace, or make aliases to quickly move terminals.

Originally a fork of github.com/TheWanderer/stiler, but has diverged to the point of countaining almost none of the original code.


Install
~~~~~~~
Install with 

:: 

    pip3 install pystiler


Usage
~~~~~~
You can use the pyst tool to move the active window.

Run simple commands with

::

    pyst move <arg>


Currently arguments are left, right, top, bottom, top\_left, bottom\_left, top\_right, bottom\_right, and maximize, all of which do pretty much what you'd expect to the active window.


Run more complex commands with

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


Workspacing
~~~~~~~~~~~
Using this script, you can define and run workspace configs. Workspace configs allow you to set up worksapces where certain applications are opened in positions on the screen.

Pystiler looks for ~/.pystiler.ini for the config file. It uses configparser to parse it. You can generate an example config by running ``pyst workspace-example``. There are three types of config modes:

- simple, where the application (and optionally, directory) is the same every time, but the locations are different
- specific, where there may be more than one application, and the directories might be different
- explicit, where you can use non-named locations using the explicit api.

Start a workspace with ``pyst workspace $workspacename``

Currently, terminaldir does nothing. This is on the todo list.



Aliases
~~~~~~~
Here's some nice aliases for use in terminals:

::

    alias l='pyst move left'
    alias r='pyst move right' # override r builtin
    alias tl='pyst move top_left'
    alias tr='pyst move top_right' # override tr builtin
    alias bl='pyst move bottom_left'
    alias br='pyst move bottom_right'
    alias m='pyst move maximize'
    alias t='pyst move top'
    alias b='pyst move bottom'
    alias ws='pyst workspace'
    function wso {
    	pyst workspace $1
    	exit
    }
 



Todos for the project
~~~~~~~~~~~~~~~~~~~~~

-  [x] Add top and bottom targets
-  [x] Add [top,bottom][left,right] targets
-  [x] Add simple CLI interface
-  [x] Add simple test cases
-  [x] Make nice python package
-  [x] Add simple workspace config
-  [x] Add complex workspace config
-  [ ] Allow passing arguments to workspace config
-  [ ] Add coverage
-  [ ] Use logging instead of debug flag
-  [ ] Add tests for window resizing
-  [ ] Make explicit api nicer
-  [ ] Find out why cols and rows reverse and fix it
-  [ ] Find out what's causing wmctrl to misfire on second call
-  [ ] Find out what bug fixes others have done
-  [ ] Map out final goals of project
-  [ ] Make list of already-resized window IDs to mitigate the resizing
   problem
-  [ ] Figure out async loading for workspaces
-  [ ] Add code quality review
