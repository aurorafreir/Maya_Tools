#makes a circular controller

import maya.cmds as cmds

tempSel_JointArray = cmds.ls(sl=True)
print tempSel_JointArray

for i in tempSel_JointArray:
    cmds.select(i)
    tempSel_Parent = cmds.ls(sl=True)
    print tempSel_Parent
    cmds.pickWalk( direction='down' );
    tempSel_AimAt = cmds.ls(sl=True)
    print tempSel_AimAt
    
    cmds.select( d=True );
    cmds.circle(name='CTRL_' + (i));
    cmds.rotate(0,90,0);
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.bakePartialHistory()
    cmds.group( em=True, name='PIVOT_' + (i));
    cmds.parent('CTRL_' + (i), 'PIVOT_' + (i));

    cmds.parentConstraint( tempSel_Parent, 'PIVOT_' + (i) , mo=False, name='tempParentConstraint' +(i));
    cmds.delete( 'tempParentConstraint' +(i));
    cmds.aimConstraint( tempSel_AimAt, 'PIVOT_' +(i), name='tempAimConstraint' +(i));
    cmds.delete( 'tempAimConstraint' +(i));

    
    
    
    
    
    
#makes a square controller    
import maya.cmds as cmds

tempSel_JointArray = cmds.ls(sl=True)
print tempSel_JointArray

for i in tempSel_JointArray:
    cmds.select(i)
    tempSel_Parent = cmds.ls( sl=True)
    print tempSel_Parent
    cmds.pickWalk( direction='down' );
    tempSel_AimAt = cmds.ls( sl=True)
    print tempSel_AimAt
    cmds.select( d=True );
    
    cmds.curve( d=1, p=[(-0.5, 0, .5), (-0.5, 0, -.5), (.5, 0, -.5), (.5, 0, .5), (-0.5, 0, .5)], name='CTRL_' + (i));
    cmds.rotate( 0,0,90);
    cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0)
    cmds.bakePartialHistory()
    cmds.group( em=True, name='PIVOT_' + (i));
    cmds.parent( 'CTRL_' + (i), 'PIVOT_' + (i));
    
    cmds.parentConstraint( tempSel_Parent, 'PIVOT_' + (i) , mo=False, name='tempParentConstraint' + (i));
    cmds.delete( 'tempParentConstraint' + (i));
    cmds.aimConstraint( tempSel_AimAt, 'PIVOT_' + (i), name='tempAimConstraint' + (i));
    cmds.delete( 'tempAimConstraint' + (i));
