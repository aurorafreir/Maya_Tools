from maya import cmds
import maya.mel as mel

def outliner_focus():
    outliner = [i for i in cmds.lsUI(ed=1) if 'outliner' in i]
    if outliner:
        outliner = outliner[0]
    else:
        return

    cmds.outlinerEditor(outliner, e=1, sc=1)
    cmds.setFocus(outliner)

outliner_focus()
cmds.select(hi=1)
mel.eval('OutlinerRevealSelected;')