import maya.cmds as cmds

tempSel_Parent = cmds.ls(sl=True,long=True)
cmds.pickWalk( direction='down' );
tempSel_AimAt = cmds.ls(sl=True,long=True)
cmds.select( d=True );

cmds.circle(name='CTRL_');
cmds.rotate(0,90,0);
cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
cmds.bakePartialHistory()
cmds.group( em=True, name='PIVOT_');
cmds.parent('CTRL_', 'PIVOT_');

cmds.parentConstraint( tempSel_Parent, 'PIVOT_', mo=False, name='tempParentConstraint');
cmds.delete( 'tempParentConstraint');
cmds.aimConstraint( tempSel_AimAt, 'PIVOT_', name='tempAimConstraint');
cmds.delete( 'tempAimConstraint');
