"""
Script to create a cluster for each selected Curve point
"""

# Standard library imports


# Third party imports
from maya import cmds

# Local application imports


crvpoints = cmds.ls(selection=1, flatten=1)

for num, crvpoint in enumerate(crvpoints):
    cmds.select(crvpoint)
    cmds.cluster(n="{}_{}".format(crvpoint.split(".")[0], str(num)))