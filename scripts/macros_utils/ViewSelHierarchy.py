"""
Script used for exporting and importing all the controller animation in a scene
"""

# Standard library imports


# Third party imports
from maya import cmds
from maya import mel

# Local application imports



def outliner_focus():
    outliner = [i for i in cmds.lsUI(editors=1) if 'outliner' in i]
    if outliner:
        outliner = outliner[0]
    else:
        return

    cmds.outlinerEditor(outliner, edit=1, showSelected=1)
    cmds.setFocus(outliner)

outliner_focus()
cmds.select(hierarchy=1)
mel.eval('OutlinerRevealSelected;')

