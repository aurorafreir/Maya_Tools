import maya.cmds as cmds

tempSel_jointArray = cmds.ls( type=('joint'), sl=True)

for i in tempSel_jointArray:
    
    cmds.select(i)
    tempSel_parent = cmds.ls( sl=True)
    
    tempSel_child = cmds.listRelatives( type='joint')
   
    if not tempSel_child:
        cmds.joint( edit=True, o=(0,0,0));
