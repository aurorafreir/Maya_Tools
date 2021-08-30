import maya.cmds as cmds

def renameSkinClusters():
    for SC in cmds.ls(type="skinCluster"):
        SCobject = cmds.listConnections(SC + ".outputGeometry[0]")[0]
        cmds.rename(SC, SCobject + "_SkinCluster")

def renameUnitConversionNodes():
    for i in cmds.ls(type="unitConversion"):
        input = cmds.listConnections(i)[0]
        cmds.rename(i, input + "_UC")