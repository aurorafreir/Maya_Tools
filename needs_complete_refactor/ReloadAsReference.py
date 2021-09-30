"""
Script to export out a currently selected object(s) to a new file, and then import back into the scene
Very old, needs a refactor
"""

# Standard library imports
import os

# Third party imports
from maya import cmds

# Local application imports



def reload_as_reference():

    CurrentProj = cmds.workspace(active=True, q=True)
    os.chdir("{}".format(CurrentProj))

    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)

    if cmds.ls(sl=True):
        SelectedObjs = cmds.ls(sl=True)[0]
        cmds.file(rename=SelectedObjs)
        cmds.file(save=True)
        cmds.file(rename=filename)

        os.rename(
            "{}/scenes/{}.ma".format(CurrentProj, SelectedObjs),
            "{}/assets/{}.ma".format(CurrentProj, SelectedObjs))

        cmds.file("{}/assets/{}.ma".format(CurrentProj, SelectedObjs), reference=True)
        cmds.hide(SelectedObjs)