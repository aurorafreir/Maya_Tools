import maya.cmds as cmds

TempSel_JointArray = cmds.ls( type=('joint'), sl=True)

for i in TempSel_JointArray:
    
    cmds.select(i)
    TempSel_Parent = cmds.ls( sl=True)
    
    TempSel_Child = cmds.listRelatives( type='joint')
   
    if not TempSel_Child:
        cmds.joint( edit=True, o=(0,0,0));
