"""
This is a script to take two input skeletons and constrain the second to the first
In my personal pipeline, this is used to make a skeleton from my hair groom scene follow my animation skeleton
"""

# SYSTEM IMPORTS

# STANDARD LIB IMPORTS
import maya.cmds

# LOCAL APP IMPORTS


def groom_attach(rig_ns="", groom_ns="", top_level_joint=""):

    rig_tlj   = f"{rig_ns}:{top_level_joint}"
    groom_tlj = f"{groom_ns}:{top_level_joint}"

    rig_joints= maya.cmds.listRelatives(rig_tlj, children=True, allDescendents=True)
    rig_joints.insert(0, rig_tlj)
    
    for x in rig_joints:
        driven = "{}:{}".format(groom_ns, x.split(":")[1])
        driver = x

        if maya.cmds.objExists(driven):
            # todo replace this with a matrix constraint for performance and scene cleanliness
            maya.cmds.parentConstraint(driver, driven)

        print("Constrained {} to {}".format(driver, driven))
