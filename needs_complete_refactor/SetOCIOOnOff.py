#Turn OCIO Off
import maya.cmds as cmds
cmds.colorManagementPrefs( e=True, cfe=False )

#Turn OCIO On
cmds.colorManagementPrefs( e=True, cfe=True )

def ocio_toggle(self):
    if cmds.colorManagementPrefs(q=True, cfe=True):
        cmds.colorManagementPrefs(e=True, cfe=False)
        cmds.button('OCIO_Toggle', e=True, label='OCIO Off', bgc=[.8, .5, .5])
    elif not cmds.colorManagementPrefs(q=True, cfe=True):
        cmds.colorManagementPrefs(e=True, cfe=True)
        cmds.button('OCIO_Toggle', e=True, label='OCIO On', bgc=[.5, .7, .5])