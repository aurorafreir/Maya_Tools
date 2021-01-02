import maya.cmds as cmds

selected_joints = cmds.ls(sl=1)

if selected_joints:
    for parent_joint in selected_joints:
        cur_joint_name = parent_joint
        rename_joints = cmds.listRelatives(parent_joint, ad=1)[::-1]
        new_name = parent_joint.strip("1234567890")
        count = 1

        for child_joint in rename_joints:
            count += 1
            cmds.select(child_joint)
            cmds.rename(child_joint, new_name + str(count))
        cmds.rename(parent_joint, new_name + "1")
        cmds.select(new_name + "1")

else:
    print "No joints selected!"
