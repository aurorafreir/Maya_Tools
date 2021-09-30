"""
description here

"""

# third parties imports
import maya.cmds


def renameSkinClusters():
    for skinCluster in maya.cmds.ls(type="skinCluster"):

        skinClusterObject = maya.cmds.listConnections(skinCluster + ".outputGeometry[0]")[0]
        maya.cmds.rename(skinCluster, skinClusterObject + "_SkinCluster")


def renameUnitConversionNodes():
    """

    :return:
    :rtype:
    """

    for i in maya.cmds.ls(type="unitConversion"):

        # you can't use input as a variable name as it's a name already use by python itself
        # be really carefull about what's called shadow built in command that python uses
        # using those names for your own variable will override python original behaviour which ca lead to really
        # uncool situation as you can imagine

        # also remember that Capital letter at the beginning of a name is Exclusive to classes - Only constants
        # have capitals too as they are written in full capital by convention

        # classes : class MyClass
        # variable : myVariable
        # definition : def myDefinition  or def my_definition
        # constant : MYCONSTANT or MY_CONSTANT

        nodeInput = maya.cmds.listConnections(i)[0]
        maya.cmds.rename(i, nodeInput + "_UC")
