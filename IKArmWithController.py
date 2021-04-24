import maya.cmds as cmds

class ThreeJointIK(object):
    def __init__(self,
                 prefix='L', # prefix is a prefix before the joint, group (and etc) names, e.g. 'L' or 'R'
                 start_location=(0, 0, 0), # start_location is the starting joint location in 3 axis e.g. (0,0,0)
                 end_location=(10, 0, 0), # end_location is the ending joint location in 3 axis e.g. (10,0,0)
                 mid_joint_push_back=1, # amount to push the middle joint backwards (in the Z axis) in Maya units
                 joint_one='Shoulder',
                 joint_two='Elbow',
                 joint_three='Wrist'
                 ):
        self.prefix = prefix
        self.start_location = start_location
        self.end_location = end_location
        self.mid_joint_push_back = mid_joint_push_back
        self.joint_one = joint_one
        self.joint_two = joint_two
        self.joint_three = joint_three
        self.extension = ['GRP', 'CTRL', 'IK']

    def build(self):
        # Create arm joints
        cmds.joint(n=self.prefix + '_' + self.joint_one, p=self.start_location)
        cmds.joint(n=self.prefix + '_' + self.joint_two,
                   p=((self.start_location[0] + self.end_location[0])/2, 0, 0 - self.mid_joint_push_back))
        cmds.joint(n=self.prefix + '_' + self.joint_three, p=self.end_location)

        # Set Joint Orient so X points down the bone
        for joint in [self.joint_one, self.joint_two]:
            cmds.joint(self.prefix + '_' + joint, e=1, zso=1, oj="xyz")

        # Create IK handle from L_Shoulder to L_Wrist
        cmds.ikHandle(n=self.prefix+'_Arm_' + self.extension[2], sj=self.prefix + '_' + self.joint_one, ee=self.prefix + '_' + self.joint_three)

        # Create IK control circle, parent it to empty group, and move to Wrist joint
        cmds.circle(n=self.prefix + '_' + self.joint_three + '_' + self.extension[2] + '_' + self.extension[1], nrx=1, nrz=0)
        cmds.group(n=self.prefix + '_' + self.joint_three + '_' + self.extension[2] + '_' + self.extension[0], em=1)
        cmds.parent(self.prefix + '_' + self.joint_three + '_' + self.extension[2] + '_' + self.extension[1],
                    self.prefix+'_' + self.joint_three + '_' + self.extension[2] + '_' + self.extension[0])
        cmds.xform(self.prefix + '_' + self.joint_three + '_' + self.extension[2] + '_' + self.extension[0],
                   t=(cmds.xform(self.prefix + '_' + self.joint_three, q=1, t=1, ws=1)))
        # Parent the IK Handle to the IK Controller
        cmds.parent(self.prefix + '_Arm_' + self.extension[2],
                    self.prefix + '_' + self.joint_three + '_' + self.extension[2] + '_' + self.extension[1])

        # Create Shoulder controller, parent it to empty group, and move to Shoulder joint
        cmds.circle(n=self.prefix + '_' + self.joint_one+ '_' + self.extension[1], nrx=1, nrz=0)
        cmds.group(n=self.prefix + '_' + self.joint_one+ '_' + self.extension[0], em=1)
        cmds.parent(self.prefix + '_' + self.joint_one+ '_' + self.extension[1],
                    self.prefix + '_' + self.joint_one + '_' + self.extension[0])
        cmds.xform(self.prefix + '_' + self.joint_one+ '_' + self.extension[0], t=(cmds.xform(self.prefix + '_' + self.joint_one, q=1, t=1, ws=1)))
        # Parent constrain the Shoulder to the Controller
        cmds.parentConstraint(self.prefix + '_Shoulder_CTRL', self.prefix + '_Shoulder')

        # Create Pole Vector controller that looks visually distinct from the others
        cmds.circle(n=self.prefix + '_PV_CTRL', nrx=1, nrz=0)
        cmds.select(d=1)
        for x in range(0, 7)[::2]:
            cmds.select(self.prefix + '_PV_CTRL' + '.cv[{}]'.format(x), tgl=0, add=True)
        cmds.selectMode(co=1)
        cmds.xform(s=(.2, .2, .2))
        cmds.selectMode(o=1)
        # Create PV parent group and parent PV control to it, and move behind the elbow location
        cmds.group(n=self.prefix + '_PV_GRP', em=1)
        cmds.parent(self.prefix + '_PV_CTRL', self.prefix + '_PV_GRP')
        cmds.xform(self.prefix + '_PV_GRP', t=(cmds.xform(self.prefix + '_Elbow', q=1, t=1, ws=1)))
        cmds.xform(self.prefix + '_PV_GRP', t=(0, 0, - self.mid_joint_push_back*3), r=1)
        # Parent constrain the Shoulder to the Controller
        cmds.poleVectorConstraint(self.prefix + '_PV_CTRL', self.prefix + '_Arm_IK')

        # Cleanup
        # Hide the IK Handle
        cmds.hide(self.prefix+'_Arm_IK')
        # delete history on controller
        cmds.bakePartialHistory(self.prefix+'_Wrist_IK_CTRL')
        # Lock the Scale and View attributes on the controllers
        cmds.setAttr(self.prefix+'_Wrist_IK_CTRL.scale', lock=True)
        cmds.setAttr(self.prefix+'_Wrist_IK_CTRL.visibility', lock=True)
        cmds.setAttr(self.prefix+'_Shoulder_CTRL.scale', lock=True)
        cmds.setAttr(self.prefix+'_Shoulder_CTRL.visibility', lock=True)
        cmds.select(d=1)

# Run the ik_arm function
spine = ThreeJointIK(prefix='L', start_location=(2,0,0), end_location=(10,0,0), mid_joint_push_back=1)
spine.build()
#three_joint_IK.ik_arm('L', (2,0,0), (10,0,0), 1)
#ik_arm('R', (-2,0,0), (-10,0,0), 1)


def TJIK():  # three joint IK
    # Create three joints
    cmds.joint(n="shoulder", p=(0, 0, 0))
    cmds.joint(n="Elbow", p=(5, 0, -1))
    cmds.joint(n="Wrist", p=(10, 0, 0))
    # Create IK Handle
    cmds.ikHandle(n="IKHandle", sj="shoulder", ee="Wrist")
    # Create Wrist Controller
    cmds.circle(n="Wrist_CTRL", nrx=1, nrz=0)
    cmds.xform("Wrist_CTRL", a=1, t=(cmds.xform("Wrist", q=1, t=1, ws=1)))
    # Parent IK handle to Wrist Controller
    cmds.parentConstraint("Wrist_CTRL", "IKHandle")
    # Create IK PV
    cmds.circle(n="PV_CTRL", nrx=1, nrz=0)
    cmds.xform("PV_CTRL", a=1, t=(5, 0, -5))
    cmds.poleVectorConstraint("PV_CTRL", "IKHandle")


TJIK()