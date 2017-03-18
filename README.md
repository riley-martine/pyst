# Stiler Spaces
The goal of this project is to be able to define tiled workspaces and open them with ease on non-tiling wms.

This is a simple python script which wraps wmctrl to allow for easier tiling.

Bind it to a key or to autowhatever-on-window-creation-hook.


run with

    python3 stiler.py <arg>


Currently arguments are

left, right

top, bottom 

top\_left, bottom\_left

top\_right, bottom\_right

maximize

All of which do pretty much what you'd expect to the active window.


On first run it will create a config file ~/.stilerrc. Modify the values to suit your window decorations/Desktop padding. 

