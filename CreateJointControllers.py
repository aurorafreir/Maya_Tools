"""
Old script used for creating a joint for creating square controllers for each joint in selection
"""

# Standard library imports

# Third party imports
from maya import cmds

# Local application imports



def create_joint_controllers():
    # Makes an array of the selected joints
    TempSel_JointArray = cmds.ls(type=('joint'), selection=True, flatten=True)

    for TempSel_Parent in TempSel_JointArray:
        # Selects child joint and sets it as variable tempSel_AimAt
        TempSel_AimAt = cmds.listRelatives(TempSel_Parent, type='joint')

        # Creates square NURBS curve and deletes it's history
        cmds.select( d=True )
        cmds.curve( d=1, p=[(-0.5, 0, .5), (-0.5, 0, -.5), (.5, 0, -.5), (.5, 0, .5), (-0.5, 0, .5)], name='CTRL_' + i)
        cmds.rotate( 0,0,90)
        cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0)
        cmds.bakePartialHistory()

        # Makes a group and makes the controller a child of the PIVOT group
        cmds.group( em=True, name='PIVOT_' + i)
        cmds.parent( 'CTRL_' + i, 'PIVOT_' + i)

        # Makes parent constraint for controller location
        cmds.parentConstraint( TempSel_Parent, 'PIVOT_' + i , maintainOffset=False, name='TempParentConstraint' + i)
        cmds.delete( 'TempParentConstraint' + i)
        if not TempSel_AimAt:
            print "no child joint of {}, skipping rotation".format(i)
        elif len(TempSel_AimAt) == 1:
            # Makes aim constraint for controller orientation
            cmds.aimConstraint( TempSel_AimAt, 'PIVOT_' + i, name='TempAimConstraint' + i)
            cmds.delete( 'TempAimConstraint' + i)

        # Parent constrains the joint to the controller
        cmds.select( 'CTRL_' + i)
        cmds.select( (i), add=True)
        cmds.parentConstraint( name='parentConstraint_' + i + '_CTRL_' + i)
        cmds.select( d=True)
