"""
Trans Rights are Human Rights

A script to extract skinned skeletons in the scene
This script is really slow currently, but it does what I want it
    to do so I'm leaving it for now lol
"""
# SYSTEM IMPORTS

# STANDARD LIBRARY IMPORTS
import pymel.core as pm

# LOCAL APPLICATION IMPORTS


def extract_skeleton() -> None:
    world_objects = pm.ls(assemblies=True)
    scene_skinned_joints = []
    for sc in pm.ls(type="skinCluster"):
        skinned_joints = [x for x in pm.skinCluster(sc, influence=True, query=True)]
        new_skinned_joints = [i for i in skinned_joints if i not in scene_skinned_joints]
        scene_skinned_joints.extend(new_skinned_joints)

    # Fallback for if this is run in a guides scene without skinned joints
    if not scene_skinned_joints:
        scene_skinned_joints = [i for i in pm.listRelatives("rig", children=True, allDescendents=True, type="joint") if i.visibility.get()]

    for jnt in scene_skinned_joints:
        parent_is_joint = True if type(jnt.getParent()) == pm.nt.Joint else False
        incoming_attrs = jnt.listConnections(plugs=True, source=True)
        for attr in incoming_attrs:
            pm.disconnectAttr(attr)
        if not parent_is_joint:
            print(f"moving {jnt} to top level")
            pm.parent(jnt, world=True)

    # Cleanup all the other objects in the scene
    pm.delete(world_objects)
    for non_joint_obj in [i for i in pm.ls(dependencyNodes=True) if i not in pm.ls(type="joint")]:
        try:
            pm.delete(non_joint_obj)
        except:
            pass

    return None
