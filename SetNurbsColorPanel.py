import maya.cmds as cmds
from functools import partial


###Function to set colour
def setNurbOverrideColor(Color, self):
    ctrl = cmds.ls(sl=True)
    for i in ctrl:
        ctrlShape = cmds.listRelatives(i, s=True)
        for shape in ctrlShape:
            conDispLayer = cmds.listConnections('{}.drawOverride'.format(shape))
            shapeDrawOverride = '{}.drawOverride'.format(shape)
            if cmds.connectionInfo(shapeDrawOverride, id=True):
                conDispLayerDrawInfo = '{}.drawInfo'.format(conDispLayer[0])
                cmds.disconnectAttr(conDispLayerDrawInfo, shapeDrawOverride)
            cmds.setAttr(shape + ".overrideEnabled", 1)
            cmds.setAttr(shape + ".overrideColor", Color)


wv = 25
winID = 'setNurbOverrideColorPanel'
# Create Window with buttons for each color override
if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

cmds.window(winID, title='Override NURB Color')
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, width=200)

cmds.frameLayout(label='NURBS Colours', labelAlign='top')
cmds.rowColumnLayout(numberOfRows=1)
cmds.button(label='', ann='black', width=wv, command=partial(setNurbOverrideColor, 1), bgc=(0, 0, 0))
cmds.button(label='', ann='dark grey', width=wv, command=partial(setNurbOverrideColor, 2), bgc=(.2, .2, .2))
cmds.button(label='', ann='light grey', width=wv, command=partial(setNurbOverrideColor, 3), bgc=(.6, .6, .6))
cmds.button(label='', ann='white', width=wv, command=partial(setNurbOverrideColor, 16), bgc=(.9, .9, .9))

cmds.button(label='', ann='dark green', width=wv, command=partial(setNurbOverrideColor, 7), bgc=(.3, .6, .3))
cmds.button(label='', ann='soft green', width=wv, command=partial(setNurbOverrideColor, 23), bgc=(.4, .7, .4))
cmds.button(label='', ann='lime green', width=wv, command=partial(setNurbOverrideColor, 26), bgc=(.6, .8, .4))
cmds.button(label='', ann='light green', width=wv, command=partial(setNurbOverrideColor, 14), bgc=(.4, .9, .2))
cmds.button(label='', ann='light green', width=wv, command=partial(setNurbOverrideColor, 27), bgc=(.4, .8, .4))
cmds.button(label='', ann='light green', width=wv, command=partial(setNurbOverrideColor, 19), bgc=(.6, 1, .7))

cmds.button(label='', ann='dark purple', width=wv, command=partial(setNurbOverrideColor, 30), bgc=(.4, .3, .7))
cmds.button(label='', ann='navy', width=wv, command=partial(setNurbOverrideColor, 15), bgc=(.2, .3, .5))
cmds.button(label='', ann='dark blue', width=wv, command=partial(setNurbOverrideColor, 5), bgc=(.2, .2, .7))
cmds.button(label='', ann='blue', width=wv, command=partial(setNurbOverrideColor, 6), bgc=(.2, .3, 1))
cmds.button(label='', ann='soft blue', width=wv, command=partial(setNurbOverrideColor, 29), bgc=(.4, .5, .6))
cmds.button(label='', ann='light blue', width=wv, command=partial(setNurbOverrideColor, 18), bgc=(.6, .7, 1))
cmds.button(label='', ann='soft light blue', width=wv, command=partial(setNurbOverrideColor, 28), bgc=(.3, .8, .8))
cmds.setParent('..')

cmds.rowColumnLayout(numberOfRows=1)

cmds.button(label='', ann='soft dark red', width=wv, command=partial(setNurbOverrideColor, 11), bgc=(.5, .2, .2))
cmds.button(label='', ann='soft brown', width=wv, command=partial(setNurbOverrideColor, 10), bgc=(.6, .4, .4))

cmds.button(label='', ann='dark red', width=wv, command=partial(setNurbOverrideColor, 4), bgc=(.7, .2, .2))
cmds.button(label='', ann='red', width=wv, command=partial(setNurbOverrideColor, 13), bgc=(.9, .3, .3))
cmds.button(label='', ann='soft orange', width=wv, command=partial(setNurbOverrideColor, 24), bgc=(.8, .5, .3))
cmds.button(label='', ann='light orange', width=wv, command=partial(setNurbOverrideColor, 21), bgc=(.9, .8, .6))
cmds.button(label='', ann='soft yellow', width=wv, command=partial(setNurbOverrideColor, 25), bgc=(.8, .8, .3))
cmds.button(label='', ann='yellow', width=wv, command=partial(setNurbOverrideColor, 17), bgc=(.9, .9, .2))
cmds.button(label='', ann='light yellow', width=wv, command=partial(setNurbOverrideColor, 22), bgc=(.9, .9, .6))

cmds.button(label='', ann='dark purple', width=wv, command=partial(setNurbOverrideColor, 8), bgc=(.3, .1, .3))
cmds.button(label='', ann='soft dark brown', width=wv, command=partial(setNurbOverrideColor, 12), bgc=(.4, .2, .3))
cmds.button(label='', ann='dark pink', width=wv, command=partial(setNurbOverrideColor, 31), bgc=(.6, .2, .4))
cmds.button(label='', ann='pink', width=wv, command=partial(setNurbOverrideColor, 9), bgc=(.8, .2, .8))
cmds.button(label='', ann='light pink', width=wv, command=partial(setNurbOverrideColor, 20), bgc=(1, .8, 1))
cmds.setParent('..')

cmds.showWindow()
