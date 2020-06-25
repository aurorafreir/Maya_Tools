import maya.cmds as cmds
from functools import partial

winID = 'setNurbOverrideColorPanel'
    
def setNurbOverrideColor(Color, self):
    ctrl = cmds.ls(sl=True)
    for i in ctrl:
        cmds.setAttr(i + ".overrideEnabled",1)
        cmds.setAttr(i + ".overrideColor", Color)

#setNurbOverrideColor(1, 12)
            
# CREATE WINDOW
hv = 25
wv = 100

if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

cmds.window(winID, title='Override NURB Color')
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, width=200)

cmds.frameLayout(label='NURBS Colours', labelAlign='top')

cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,1))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,2))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,3))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,4))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,5))
cmds.button(label='blue', ann='', command=partial(setNurbOverrideColor,6))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,7))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,8))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,9))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,10))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,11))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,12))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,13))
cmds.button(label='light green', ann='', command=partial(setNurbOverrideColor,14))
cmds.button(label='navy', ann='', command=partial(setNurbOverrideColor,15))
cmds.button(label='white', ann='', command=partial(setNurbOverrideColor,16))
cmds.button(label='yellow', ann='', command=partial(setNurbOverrideColor,17))
cmds.button(label='light blue', ann='', command=partial(setNurbOverrideColor,18))

cmds.showWindow()
