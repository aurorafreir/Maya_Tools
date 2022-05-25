"""
This is a script to take two input skeletons and constrain the second to the first
In my personal pipeline, this is used to make a skeleton from my hair groom scene follow my animation skeleton
"""

# SYSTEM IMPORTS

# STANDARD LIB IMPORTS
import maya.cmds

# LOCAL APP IMPORTS


def groom_attach():

    # todo rewrite this to just take two namespaces and one joint name
    groom_tlj = "GROOM_SCENE:spine_C0_0_jnt"
    rig_tlj   = "RIG_SCENE:spine_C0_0_jnt"
    
    groom_ns  = groom_tlj.split(":")[0]
    rig_ns    = rig_tlj.split(":")[0]
    
    rig_joints= maya.cmds.listRelatives(rig_tlj, children=True, allDescendents=True)
    rig_joints.insert(0, rig_tlj)
    
    for x in rig_joints:
        driven = "{}:{}".format(groom_ns, x.split(":")[1])
        driver = x

        # todo replace this with a proper check instead of try:except
        try:
            # todo replace this with a matrix constraint for performance and scene cleanliness
            maya.cmds.parentConstraint(driver, driven)
        except:
            pass
        print("Constrained {} to {}".format(driver, driven))
