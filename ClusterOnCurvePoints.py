import maya.cmds as cmds

points = cmds.ls(sl=1, fl=1)
count = 0
for point in points:
    count += 1
    cmds.select(point)
    cmds.cluster(n=point.split(".")[0] + "_" + str(count))
