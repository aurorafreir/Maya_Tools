import maya.cmds as cmds

selected_joints = cmds.ls(sl=1, type="joint")

for joint in selected_joints:
    parent_joint = cmds.listRelatives(joint, p=1)[0]
    cmds.duplicate(joint, n=joint + "_end")
    cmds.aimConstraint(parent_joint, joint+"_end")
    cmds.xform(joint+"_end", r=1, os=1, t=(-.5,0,0))
    cmds.parent(joint+"_end", joint)
    cmds.delete(joint + "_end_aimConstraint1")
    cmds.xform(joint + "_end", ro=(0,0,0))
    cmds.joint(joint, e=1, zso=1, oj="xyz")

    # TODO set end joints rotation to 0,0,0