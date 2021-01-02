# Set as Ctrl+Shift+G

import maya.cmds as cmds

sel = cmds.ls(sl=1)

for i in sel:
    cmds.select(i)
    cmds.group(n='GRP_{}'.format(i).replace('JNT_',''))