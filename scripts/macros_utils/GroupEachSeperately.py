"""
Script used to group each selected object in it's own seperate group
"""

# Standard library imports


# Third party imports
from maya import cmds

# Local application imports



def GroupEachSeperately():
    sel = cmds.ls(selection=1)

    for object in sel:
        cmds.select(object)
        cmds.group(name='GRP_{}'.format(object).replace('JNT_',''))

GroupEachSeperately()
