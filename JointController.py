#makes a circular controller

import maya.cmds as cmds

#makes an array of the selected joints
tempSel_JointArray = cmds.ls( type=('joint'), sl=True)
print ("Selected joints", tempSel_JointArray)

#loops through each joint in tempSel_JointArray
for i in tempSel_JointArray:
    
    #selects current joint and sets it as variable tempSel_Parent
    cmds.select(i)
    tempSel_Parent = cmds.ls( sl=True)
    print ("current parent joint", tempSel_Parent)
    
    #selects child joint and sets it as variable tempSel_AimAt
    tempSel_AimAt = cmds.listRelatives( type='joint')
    cmds.select(tempSel_jointChild)
    print ("current aim at joint", tempSel_AimAt)
    
    #creates circe NURBS curve and deletes it's history
    cmds.select( d=True );
    cmds.circle(name='CTRL_' + (i));
    cmds.rotate(0,90,0);
    cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0)
    cmds.bakePartialHistory()
    
    #makes a group and makes the controller a child of the PIVOT group
    cmds.group( em=True, name='PIVOT_' + (i));
    cmds.parent( 'CTRL_' + (i), 'PIVOT_' + (i));
    
    #makes parent constraint for controller location
    cmds.parentConstraint( tempSel_Parent, 'PIVOT_' + (i) , mo=False, name='tempParentConstraint' + (i));
    cmds.delete( 'tempParentConstraint' + (i));
    
    #makes aim constraint for controller orientation
    cmds.aimConstraint( tempSel_AimAt, 'PIVOT_' + (i), name='tempAimConstraint' + (i));
    cmds.delete( 'tempAimConstraint' + (i));

    
#makes a square controller    
import maya.cmds as cmds

#makes an array of the selected joints
tempSel_JointArray = cmds.ls( type=('joint'), sl=True)
print ("Selected joints", tempSel_JointArray)

#loops through each joint in tempSel_JointArray
for i in tempSel_JointArray:
    
    #selects current joint and sets it as variable tempSel_Parent
    cmds.select(i)
    tempSel_Parent = cmds.ls( sl=True)
    print ("current parent joint", tempSel_Parent)
    
    #selects child joint and sets it as variable tempSel_AimAt
    tempSel_AimAt = cmds.listRelatives( type='joint')
    cmds.select(tempSel_jointChild)
    print ("current aim at joint", tempSel_AimAt)
    
    #creates square NURBS curve and deletes it's history
    cmds.select( d=True );
    cmds.curve( d=1, p=[(-0.5, 0, .5), (-0.5, 0, -.5), (.5, 0, -.5), (.5, 0, .5), (-0.5, 0, .5)], name='CTRL_' + (i));
    cmds.rotate( 0,0,90);
    cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0)
    cmds.bakePartialHistory()
    
    #makes a group and makes the controller a child of the PIVOT group
    cmds.group( em=True, name='PIVOT_' + (i));
    cmds.parent( 'CTRL_' + (i), 'PIVOT_' + (i));
    
    #makes parent constraint for controller location
    cmds.parentConstraint( tempSel_Parent, 'PIVOT_' + (i) , mo=False, name='tempParentConstraint' + (i));
    cmds.delete( 'tempParentConstraint' + (i));
    
    #makes aim constraint for controller orientation
    cmds.aimConstraint( tempSel_AimAt, 'PIVOT_' + (i), name='tempAimConstraint' + (i));
    cmds.delete( 'tempAimConstraint' + (i));
