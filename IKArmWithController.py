import maya.cmds as cmds

# arm_start_location and arm_end_location are shoulder and wrist locations in 3 axis e.g. (0,0,0), (10,0,0)
# mid_joint_push_back is the amount to push the middle joint backwards (in the Z axis) in Maya units
# prefix is a prefix before the joint names, e.g. 'L' or 'R'
def ik_arm(prefix, arm_start_location, arm_end_location, mid_joint_push_back):
    # Create arm joints
    cmds.joint(n=prefix+'_Shoulder', p=arm_start_location)
    cmds.joint(n=prefix+'_Elbow', p=((arm_start_location[0]+arm_end_location[0])/2, 0, 0 - mid_joint_push_back))
    cmds.joint(n=prefix+'_Wrist', p=arm_end_location)

    # Set Joint Orient so X points down the bone
    cmds.joint(prefix+'_Shoulder', e=1, zso=1, oj="xyz")
    cmds.joint(prefix+'_Elbow', e=1, zso=1, oj="xyz")

    # Create IK handle from L_Shoulder to L_Wrist
    cmds.ikHandle(n=prefix+'_Arm_IK', sj=prefix+'_Shoulder', ee=prefix+'_Wrist')

    # Create IK control circle, parent it to empty group, and move to Wrist joint
    cmds.circle(n=prefix+'_Wrist_IK_CTRL', nrx=1, nrz=0)
    cmds.group(n=prefix+'_Wrist_IK_GRP', em=1)
    cmds.parent(prefix+'_Wrist_IK_CTRL', prefix+'_Wrist_IK_GRP')
    cmds.xform(prefix+'_Wrist_IK_GRP', t=(cmds.xform(prefix+'_Wrist', q=1, t=1, ws=1)))
    # Parent the IK Handle to the IK Controller
    cmds.parent(prefix+'_Arm_IK', prefix+'_Wrist_IK_CTRL')

    # Create Shoulder controller, parent it to empty group, and move to Shoulder joint
    cmds.circle(n=prefix + '_Shoulder_CTRL', nrx=1, nrz=0)
    cmds.group(n=prefix + '_Shoulder_GRP', em=1)
    cmds.parent(prefix + '_Shoulder_CTRL', prefix + '_Shoulder_GRP')
    cmds.xform(prefix + '_Shoulder_GRP', t=(cmds.xform(prefix + '_Shoulder', q=1, t=1, ws=1)))
    # Parent constrain the Shoulder to the Controller
    cmds.parentConstraint(prefix + '_Shoulder_CTRL', prefix + '_Shoulder')

    # Create Pole Vector controller that looks visually distinct from the others
    cmds.circle(n=prefix + '_PV_CTRL', nrx=1, nrz=0)
    cmds.select(d=1)
    for x in range(0, 7)[::2]:
        cmds.select(prefix + '_PV_CTRL' + '.cv[{}]'.format(x), tgl=0, add=True)
    cmds.selectMode(co=1)
    cmds.xform(s=(.2, .2, .2))
    cmds.selectMode(o=1)
    # Create PV parent group and parent PV control to it, and move behind the elbow location
    cmds.group(n=prefix + '_PV_GRP', em=1)
    cmds.parent(prefix + '_PV_CTRL', prefix + '_PV_GRP')
    cmds.xform(prefix + '_PV_GRP', t=(cmds.xform(prefix + '_Elbow', q=1, t=1, ws=1)))
    cmds.xform(prefix + '_PV_GRP', t=(0, 0, -mid_joint_push_back*3), r=1)
    # Parent constrain the Shoulder to the Controller
    cmds.poleVectorConstraint(prefix + '_PV_CTRL', prefix + '_Arm_IK')

    # Cleanup
    # Hide the IK Handle
    cmds.hide(prefix+'_Arm_IK')
    # delete history on controller
    cmds.bakePartialHistory(prefix+'_Wrist_IK_CTRL')
    # Lock the Scale and View attributes on the controllers
    cmds.setAttr(prefix+'_Wrist_IK_CTRL.scale', lock=True)
    cmds.setAttr(prefix+'_Wrist_IK_CTRL.visibility', lock=True)
    cmds.setAttr(prefix+'_Shoulder_CTRL.scale', lock=True)
    cmds.setAttr(prefix+'_Shoulder_CTRL.visibility', lock=True)
    cmds.select(d=1)

# Run the ik_arm function
ik_arm('L', (2,0,0), (10,0,0), 1)
#ik_arm('R', (-2,0,0), (-10,0,0), 1)