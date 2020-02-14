import maya.cmds as cmds

selected = cmds.ls(selection=True)

for item in selected:
    rPiv = cmds.xform(item, q=True, rp=True)  # query rotation pivot
    sPiv = cmds.xform(item, q=True, sp=True)  # query scale pivot

    loc = cmds.spaceLocator(n=item + "wireLocator")
    cmds.xform(t=rPiv)

cmds.curve()
