import maya.cmds as cmds

selected = cmds.ls(sl=True)
for i in selected:
    print cmds.xform(i, absolute=True, t=True, ws=True, q=True)
    sel_trans = cmds.xform(i, absolute=True, t=True, ws=True, q=True)
    #sel_rot = cmds.xform(selected, absolute=True, t=True, ws=True, q=True)

    cmds.spaceLocator(n=i + "_loc")
    cmds.xform(i + "_loc", t=sel_trans)