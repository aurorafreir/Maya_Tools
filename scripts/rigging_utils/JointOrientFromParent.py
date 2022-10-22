"""
Script to make a new joint beneath the selection, placed outwards from the parent joint
Used to help set the Joint Orient for any leaf joints
"""

# Standard library imports

# Third party imports
from maya import cmds

# Local application imports


def JointOrientFromParent():
    selected_joints = cmds.ls(selection=True, type="joint")

    for joint in selected_joints:
        end_joint_name = "{}_end".format(joint)
        if end_joint_name not in joint:
            parent_joint = cmds.listRelatives(joint, parent=True, fullPath=True)[0]
            cmds.duplicate(joint, name=end_joint_name)
            cmds.aimConstraint(parent_joint, end_joint_name)
            cmds.xform(end_joint_name, relative=True, objectSpace=True, translation=(-.5,0,0))
            cmds.parent(end_joint_name, joint)
            cmds.delete("{}_aimConstraint1".format(end_joint_name))
            cmds.xform(end_joint_name, rotation=(0,0,0))

JointOrientFromParent()