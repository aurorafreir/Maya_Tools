import maya.cmds as cmds

points = cmds.ls(sl=1, fl=1)
for point in points:
    cmds.select(point)
    cmds.cluster()