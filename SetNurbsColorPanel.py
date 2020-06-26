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
# def main():
wv = 25

if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

cmds.window(winID, title='Override NURB Color')
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, width=200)

cmds.frameLayout(label='NURBS Colours', labelAlign='top')
cmds.rowColumnLayout(numberOfRows=1 )
cmds.button(label='', ann='black', width=wv, command=partial(setNurbOverrideColor,1), bgc=(0,0,0))
cmds.button(label='', ann='dark grey', width=wv, command=partial(setNurbOverrideColor,2), bgc=(.2,.2,.2))
cmds.button(label='', ann='light grey', width=wv, command=partial(setNurbOverrideColor,3), bgc=(.6,.6,.6))
cmds.button(label='', ann='dark red', width=wv, command=partial(setNurbOverrideColor,4), bgc=(.7,.2,.2))
cmds.button(label='', ann='dark blue', width=wv, command=partial(setNurbOverrideColor,5), bgc=(.2,.2,.7))
cmds.button(label='', ann='blue', width=wv, command=partial(setNurbOverrideColor,6), bgc=(.2,.3,1))
cmds.button(label='', ann='dark green', width=wv, command=partial(setNurbOverrideColor,7), bgc=(.3,.6,.3))
cmds.button(label='', ann='dark purple',width=wv, command=partial(setNurbOverrideColor,8), bgc=(.3,.1,.3))
cmds.button(label='', ann='pink', width=wv, command=partial(setNurbOverrideColor,9), bgc=())
cmds.button(label='', ann='soft brown', width=wv, command=partial(setNurbOverrideColor,10), bgc=(.6,.4,.4))
cmds.button(label='', ann='soft dark red', width=wv, command=partial(setNurbOverrideColor,11), bgc=(.2,.2,.5))
cmds.button(label='', ann='soft dark brown', width=wv, command=partial(setNurbOverrideColor,12))
cmds.button(label='', ann='red', width=wv, command=partial(setNurbOverrideColor,13), bgc=(.9,.3,.3))
cmds.button(label='', ann='light green', width=wv, command=partial(setNurbOverrideColor,14))
cmds.button(label='', ann='navy', width=wv, command=partial(setNurbOverrideColor,15))
cmds.setParent('..')
cmds.rowColumnLayout(numberOfRows=1 )
cmds.button(label='', ann='white', width=wv, command=partial(setNurbOverrideColor,16), bgc=(.9,.9,.9))
cmds.button(label='', ann='yellow', width=wv, command=partial(setNurbOverrideColor,17), bgc=(.9,.9,.2))
cmds.button(label='', ann='light blue', width=wv, command=partial(setNurbOverrideColor,18), bgc=(.6,.7,1))
cmds.button(label='', ann='light green', width=wv, command=partial(setNurbOverrideColor,19), bgc=(.6,1,.7))
cmds.button(label='', ann='light pink', width=wv, command=partial(setNurbOverrideColor,20), bgc=(1,.8,1))
cmds.button(label='', ann='light orange', width=wv, command=partial(setNurbOverrideColor,21), bgc=(.9,.8,.6))
cmds.button(label='', ann='light yellow', width=wv, command=partial(setNurbOverrideColor,22), bgc=(.9,.9,.6))
cmds.button(label='', ann='soft green', width=wv, command=partial(setNurbOverrideColor,23), bgc=(1,1,1))
cmds.button(label='', ann='soft orange', width=wv, command=partial(setNurbOverrideColor,24), bgc=(1,1,1))
cmds.button(label='', ann='soft yellow', width=wv, command=partial(setNurbOverrideColor,25), bgc=(1,1,1))
cmds.button(label='', ann='lime green', width=wv, command=partial(setNurbOverrideColor,26), bgc=(1,1,1))
cmds.button(label='', ann='light blue', width=wv, command=partial(setNurbOverrideColor,27), bgc=(1,1,1))
cmds.button(label='', ann='soft light blue', width=wv, command=partial(setNurbOverrideColor,28), bgc=(1,1,1))
cmds.button(label='', ann='soft blue', width=wv, command=partial(setNurbOverrideColor,29), bgc=(1,1,1))
cmds.button(label='', ann='dark purple', width=wv, command=partial(setNurbOverrideColor,30), bgc=(1,1,1))
cmds.button(label='', ann='dark pink', width=wv, command=partial(setNurbOverrideColor,31), bgc=(1,1,1))
cmds.setParent('..')

cmds.showWindow()
