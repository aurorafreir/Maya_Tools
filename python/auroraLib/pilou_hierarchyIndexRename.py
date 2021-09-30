"""
docstring of the module here
"""

# third parties import
import maya.cmds


# all your code should be defined in functions. so it can be used like :
# import myModule
# myModule.rename_hierarchy_index(['joint1', 'joint2'])
# It will also allow you to sort your commands better. Modules are not usually meants to execute you definition when imported
# this is actually not quite true, but in your case you just want to store some command so you can reuse them


def rename_hierarchy_index(joints):
    """description here

    :param joints:
    :type joints:
    """

    if joints:
        for parent_joint in joints:
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
        maya.cmds.warning("No joints selected!")
