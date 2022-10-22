"""
Script used for renaming different types of objects inside of the current Maya scene
"""

# Standard library imports

# Third party imports
from maya import cmds

# Local application imports



def renameSkinClusters():
    for skincluster in cmds.ls(type="skinCluster"):
        sc_object = cmds.listConnections("{}.outputGeometry[0]".format(skincluster))[0]
        cmds.rename(skincluster, "{}_SkinCluster".format(sc_object))

def renameUnitConversionNodes():
    for unitconversion in cmds.ls(type="unitConversion"):
        input = cmds.listConnections(unitconversion)[0]
        cmds.rename(unitconversion, "{}_UC".format(input))