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
cmds.button(label='black', width=wv, command=partial(setNurbOverrideColor,1), bgc=(0,0,0))
cmds.button(label='dark grey', width=wv, command=partial(setNurbOverrideColor,2), bgc=(.2,.2,.2))
cmds.button(label='light grey', width=wv, command=partial(setNurbOverrideColor,3), bgc=(.6,.6,.6))
cmds.button(label='dark red', width=wv, command=partial(setNurbOverrideColor,4), bgc=(.7,.2,.2))
cmds.button(label='dark blue', width=wv, command=partial(setNurbOverrideColor,5), bgc=(.2,.2,.7))
cmds.button(label='blue', width=wv, command=partial(setNurbOverrideColor,6), bgc=(.2,.3,1))
cmds.button(label='dark green', width=wv, command=partial(setNurbOverrideColor,7), bgc=(.3,.6,.3))
cmds.button(label='dark purple', width=wv, command=partial(setNurbOverrideColor,8))
cmds.button(label='pink', width=wv, command=partial(setNurbOverrideColor,9))
cmds.button(label='soft brown', width=wv, command=partial(setNurbOverrideColor,10), bgc=(.6,.4,.4))
cmds.button(label='??', width=wv, command=partial(setNurbOverrideColor,11))
cmds.button(label='soft dark orange', width=wv, command=partial(setNurbOverrideColor,12))
cmds.button(label='red', width=wv, command=partial(setNurbOverrideColor,13))
cmds.button(label='light green', width=wv, command=partial(setNurbOverrideColor,14))
cmds.button(label='navy', width=wv, command=partial(setNurbOverrideColor,15))
cmds.setParent('..')
cmds.rowColumnLayout(numberOfRows=1 )
cmds.button(label='white', width=wv, command=partial(setNurbOverrideColor,16), bgc=(.9,.9,.9))
cmds.button(label='yellow', width=wv, command=partial(setNurbOverrideColor,17), bgc=(.9,.9,.2))
cmds.button(label='light blue', width=wv, command=partial(setNurbOverrideColor,18), bgc=(.6,.7,1))
cmds.button(label='light green', width=wv, command=partial(setNurbOverrideColor,19), bgc=(.6,1,.7))
cmds.button(label='light pink', width=wv, command=partial(setNurbOverrideColor,20), bgc=(1,.8,1))
cmds.button(label='light orange', width=wv, command=partial(setNurbOverrideColor,21), bgc=(.9,.8,.6))
cmds.button(label='light yellow', width=wv, command=partial(setNurbOverrideColor,22), bgc=(.9,.9,.6))
cmds.button(label='soft green', width=wv, command=partial(setNurbOverrideColor,23), bgc=(1,1,1))
cmds.button(label='soft orange', width=wv, command=partial(setNurbOverrideColor,24), bgc=(1,1,1))
cmds.button(label='soft yellow', width=wv, command=partial(setNurbOverrideColor,25), bgc=(1,1,1))
cmds.button(label='lime green', width=wv, command=partial(setNurbOverrideColor,26), bgc=(1,1,1))
cmds.button(label='light blue', width=wv, command=partial(setNurbOverrideColor,27), bgc=(1,1,1))
cmds.button(label='soft light blue', width=wv, command=partial(setNurbOverrideColor,28), bgc=(1,1,1))
cmds.button(label='soft blue', width=wv, command=partial(setNurbOverrideColor,29), bgc=(1,1,1))
cmds.button(label='dark purple', width=wv, command=partial(setNurbOverrideColor,30), bgc=(1,1,1))
cmds.button(label='dark pink', width=wv, command=partial(setNurbOverrideColor,31), bgc=(1,1,1))
cmds.setParent('..')

cmds.showWindow()
