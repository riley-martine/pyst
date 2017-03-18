#!/usr/bin/python

############################################################################
# Copyright (c) 2009   unohu <unohu0@gmail.com>                            #
#                                                                          #
# Permission to use, copy, modify, and/or distribute this software for any #
# purpose with or without fee is hereby granted, provided that the above   #
# copyright notice and this permission notice appear in all copies.        #
#                                                                          #
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES #
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF         #
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR  #
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES   #
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN    #
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF  #
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.           #
#                                                                          #
############################################################################

import sys
import os
import subprocess
import pickle
import configparser

def initconfig():
    rcfile=os.getenv('HOME')+"/.stilerrc"
    if not os.path.exists(rcfile):
        cfg=open(rcfile,'w')
        cfg.write("""#Tweak these values 
[default]
BottomPadding = 0
TopPadding = 0
LeftPadding = 0
RightPadding = 0
WinTitle = 21
WinBorder = 1
MwFactor = 0.65
TempFile = /tmp/tile_winlist
""")
        cfg.close()

    config=configparser.RawConfigParser()
    config.read(rcfile)
    return config


def initialize():
    desk_output = subprocess.getoutput("wmctrl -d").split("\n")
    desk_list = [line.split()[0] for line in desk_output]

    current =  [x for x in desk_output if x.split()[1] == "*"][0].split()

    desktop = current[0]
    width =  current[8].split("x")[0]
    height =  current[8].split("x")[1]
    orig_x =  current[7].split(",")[0]
    orig_y =  current[7].split(",")[1]

    win_output = subprocess.getoutput("wmctrl -lG").split("\n")
    win_list = {}

    for desk in desk_list:
        win_list[desk] = [hex(int(y.split()[0],16)) for y in [x for x in win_output if x.split()[1] == desk]]

    return (desktop,orig_x,orig_y,width,height,win_list)


def get_active_window():
    return str(hex(int(subprocess.getoutput("xdotool getactivewindow 2>/dev/null").split()[0])))
    

def store(object,file):
    with open(file, 'w') as f:
        pickle.dump(object,f)
    f.close()


def retrieve(file):
    try:
        with open(file,'r+') as f:
            obj = pickle.load(f)
        f.close()
        return(obj)
    except:
        f = open(file,'w')
        f.close
        dict = {}
        return (dict)


# Get all global variables
Config = initconfig()
BottomPadding = Config.getint("default","BottomPadding")
TopPadding = Config.getint("default","TopPadding")
LeftPadding = Config.getint("default","LeftPadding")
RightPadding = Config.getint("default","RightPadding")
WinTitle = Config.getint("default","WinTitle")
WinBorder = Config.getint("default","WinBorder")
MwFactor = Config.getfloat("default","MwFactor")
TempFile = Config.get("default","TempFile")
(Desktop,OrigXstr,OrigYstr,MaxWidthStr,MaxHeightStr,WinList) = initialize()
MaxWidth = int(MaxWidthStr) - LeftPadding - RightPadding
MaxHeight = int(MaxHeightStr) - TopPadding - BottomPadding
OrigX = int(OrigXstr) + LeftPadding
OrigY = int(OrigYstr) + TopPadding 
OldWinList = retrieve(TempFile)


def get_simple_tile(wincount):
    rows = wincount - 1
    layout = [] 
    if rows == 0:
        layout.append((OrigX,OrigY,MaxWidth,MaxHeight-WinTitle-WinBorder))
        return layout
    else:
        layout.append((OrigX,OrigY,int(MaxWidth*MwFactor),MaxHeight-WinTitle-WinBorder))

    x=OrigX + int((MaxWidth*MwFactor)+(2*WinBorder))
    width=int((MaxWidth*(1-MwFactor))-2*WinBorder)
    height=int(MaxHeight/rows - WinTitle-WinBorder)
    
    for n in range(0,rows):
        y= OrigY+int((MaxHeight/rows)*(n))
        layout.append((x,y,width,height))

    return layout


def get_vertical_tile(wincount):
    layout = [] 
    y = OrigY
    width = int(MaxWidth/wincount)
    height = MaxHeight - WinTitle - WinBorder
    for n in range(0,wincount):
        x= OrigX + n * width
        layout.append((x,y,width,height))

    return layout


def get_horiz_tile(wincount):
    layout = [] 
    x = OrigX
    height = int(MaxHeight/wincount - WinTitle - WinBorder)
    width = MaxWidth
    for n in range(0,wincount):
        y= OrigY + int((MaxHeight/wincount)*(n))
        layout.append((x,y,width,height))

    return layout

def get_max_all(wincount):
    layout = [] 
    x = OrigX
    y = OrigY 
    height = MaxHeight - WinTitle - WinBorder
    width = MaxWidth
    for n in range(0,wincount):
        layout.append((x,y,width,height))

    return layout



def move_active(PosX,PosY,Width,Height):
    command =  " wmctrl -r :ACTIVE: -e 0," + str(PosX) + "," + str(PosY)+ "," + str(Width) + "," + str(Height)
    print(command)
    os.system(command)


def move_window(windowid,PosX,PosY,Width,Height):
    command =  " wmctrl -i -r " + windowid +  " -e 0," + str(PosX) + "," + str(PosY)+ "," + str(Width) + "," + str(Height)
    os.system(command)
    command = "wmctrl -i -r " + windowid + " -b remove,hidden,shaded"
    os.system(command)


def raise_window(windowid):
    if windowid == ":ACTIVE:":
        command = "wmctrl -a :ACTIVE: "
    else:
        command - "wmctrl -i -a " + windowid
    
    os.system(command)


def left():
    Width=MaxWidth//2-1
    Height=MaxHeight - WinTitle -WinBorder
    PosX=LeftPadding
    PosY=TopPadding
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")


def right():
    Width=MaxWidth//2-1
    Height=MaxHeight - WinTitle - WinBorder 
    PosX=MaxWidth//2
    PosY=TopPadding
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")

def top():
    Width=MaxWidth
    Height=MaxHeight//2-WinTitle-WinBorder
    PosX=LeftPadding
    PosY=TopPadding
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")

def bottom():
    Width=MaxWidth
    Height=MaxHeight//2-WinTitle-WinBorder
    PosX=LeftPadding
    PosY=MaxHeight//2-BottomPadding
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")

def top_left():
    Width=MaxWidth//2-1
    Height=MaxHeight//2 - WinTitle - WinBorder
    PosX=LeftPadding
    PosY=TopPadding
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")

def top_right():
    Width=MaxWidth//2-1
    Height=MaxHeight//2 - WinTitle - WinBorder
    PosX=MaxWidth//2
    PosY=TopPadding
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")

def bottom_left():
    Width=MaxWidth//2-1
    Height=MaxHeight//2 - WinTitle - WinBorder
    PosX=LeftPadding
    PosY=MaxHeight//2-1
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")

def bottom_right():
    Width=MaxWidth//2-1
    Height=MaxHeight//2 - WinTitle - WinBorder
    PosX=MaxWidth//2
    PosY=MaxHeight//2-1
    move_active(PosX,PosY,Width,Height)


def compare_win_list(newlist,oldlist):
    templist = []
    for window in oldlist:
        if newlist.count(window) != 0:
            templist.append(window)
    for window in newlist:
        if oldlist.count(window) == 0: 
            templist.append(window)
    return templist


def create_win_list():
    Windows = WinList[Desktop]

    if OldWinList == {}:
        pass
    else:
        OldWindows = OldWinList[Desktop]
        if Windows == OldWindows:
            pass
        else:
            Windows = compare_win_list(Windows,OldWindows)

    return Windows


def arrange(layout,windows):
    for win , lay  in zip(windows,layout):
        move_window(win,lay[0],lay[1],lay[2],lay[3])
    WinList[Desktop]=windows
    store(WinList,TempFile)


def simple():
    Windows = create_win_list()
    arrange(get_simple_tile(len(Windows)),Windows)
   

def swap():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange(get_simple_tile(len(winlist)),winlist)


def vertical():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange(get_vertical_tile(len(winlist)),winlist)


def horiz():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange(get_horiz_tile(len(winlist)),winlist)


def cycle():
    winlist = create_win_list()
    winlist.insert(0,winlist[len(winlist)-1])
    winlist = winlist[:-1]
    arrange(get_simple_tile(len(winlist)),winlist)


def maximize():
    Width=MaxWidth
    Height=MaxHeight - WinTitle -WinBorder
    PosX=LeftPadding
    PosY=TopPadding
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")

def max_all():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange(get_max_all(len(winlist)),winlist)


arg=sys.argv[1]
if arg == "left":
    left()
elif arg == "right":
    right()
elif arg == "top":
    top()
elif arg == "bottom":
    bottom()
elif arg == "top_left":
    top_left()
elif arg == "top_right":
    top_right()
elif arg == "bottom_left":
    bottom_left()
elif arg == "bottom_right":
    bottom_right()
elif arg == "simple":
    simple()
elif arg == "vertical":
    vertical()
elif arg == "horizontal":
    horiz()
elif arg == "swap":
    swap()
elif arg == "cycle":
    cycle()
elif arg == "maximize":
    maximize()
elif arg == "max_all":
    max_all()

