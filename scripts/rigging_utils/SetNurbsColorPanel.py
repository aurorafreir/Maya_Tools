"""
Creates a simple GUI to set the colour of selected NURBS shapes
"""

# Standard library imports
from functools import partial

# Third party imports
from maya import cmds

# Local application imports



#Function to set colour
def setNurbOverrideColor(Color, self):
    ctrl = cmds.ls(selection=True)
    for control in ctrl:
        ctrl_shapes = cmds.listRelatives(shapes=1, fullPath=1)
        for shape in ctrl_shapes:
            cmds.setAttr("{}.overrideEnabled".format(shape), 1)
            cmds.setAttr("{}.overrideColor".format(shape), Color)
            
            
buttons_one = (
            ("black",         1,     (0,0,0)), 
            ("dark grey",     2,     (.2, .2, .2)),
            ("light grey",    3,     (.6, .6, .6)),
            ("white",         16,    (.9, .9, .9)),
            
            ("dark green",    7,     (.3, .6, .3)),
            ("soft green",    23,    (.4, .7, .4)),
            ("lime green",    26,    (.6, .8, .4)),
            ("light green",   14,    (.4, .9, .2)),
            ("light green",   27,    (.4, .8, .2)),
            ("light green",   19,    (.6,  1, .7)),
            
            ("dark purple",   30,    (.4, .3, .7)),
            ("navy",          15,    (.2, .3, .5)),
            ("dark blue",     5,     (.2, .2, .7)),
            ("blue",          6,     (.2, .3,  1)),
            ("soft blue",     29,    (.4, .5, .6)),
            ("light blue",    18,    (.6, .7,  1)),
            ("soft light blue",28,   (.3, .8, .8)),
            
            )
            
buttons_two = (
            ("soft dark red", 11,    (.5, .2, .2)),
            ("soft brown",    10,    (.6, .4, .4)),
            ("dark red",      4,     (.7, .2, .2)),
            ("red",           13,    (.9, .3, .3)),
            
            ("soft orange",   24,    (.8, .5, .3)),
            ("light orange",  21,    (.9, .8, .6)),
            ("soft yellow",   25,    (.8, .8, .3)), 
            ("yellow",        17,    (.9, .9, .2)),
            ("light yellow",  22,    (.9, .9, .6)),
            
            ("dark purple",   8,     (.3, .1, .3)),
            ("soft dark brown",12,   (.4, .2, .3)),
            ("dark pink",     31,    (.6, .2, .4)),
            ("pink",          9,     (.8, .2, .8)),
            ("light pink",    20,    ( 1, .8,  1)) 
            )


wv = 25
winID = 'setNurbOverrideColorPanel'
#Create Window with buttons for each color override
if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

cmds.window(winID, title='Override NURB Color')
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, width=200)

cmds.frameLayout(label='NURBS Colours', labelAlign='top')


cmds.rowColumnLayout(numberOfRows=1 )
for button in buttons_one:
    cmds.button(label='', annotation=button[0], width=wv, command=partial(setNurbOverrideColor, button[1]), backgroundColor=button[2])
cmds.setParent('..')


cmds.rowColumnLayout(numberOfRows=1 )
for button in buttons_two:
    cmds.button(label='', annotation=button[0], width=wv, command=partial(setNurbOverrideColor, button[1]), backgroundColor=button[2])
cmds.setParent('..')


cmds.showWindow()
