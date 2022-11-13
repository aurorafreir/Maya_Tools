"""
Trans Rights are Human Rights

Takes all the blendshapes from currently selected objects, blendshape nodes, or inputted object names,
    and extracts the blendshapes out to their own objects
"""
# SYSTEM IMPORTS

# STANDARD LIBRARY IMPORTS
import maya.cmds as cmds

# LOCAL APPLICATION IMPORTS


def extract_bs_targets(bs_node, geo) -> list:
    target_data = cmds.aliasAttr(bs_node, q=1)
    target_names = target_data[::2]

    extracted_target_meshes = []
    for index, target_name in enumerate(target_names):
        new_obj_name = cmds.sculptTarget(bs_node, edit=True, target=index, regenerate=True)
        cmds.rename(new_obj_name, "{}_{}".format(bs_node, target_name))
        print("Rebuilt Blendshape target {0} {1} as {0}_{1}".format(bs_node, target_name))

    return extracted_target_meshes


def extract_bs_targets_runner(bs_node, geo_trans) -> None:
    if bs_node and geo_trans:
        extract_bs_targets(bs_node=bs_node, geo=geo_trans)

    elif cmds.ls(selection=True):
        trans_selection = cmds.ls(selection=True, type="transform")
        bs_selection = cmds.ls(selection=True, type="blendShape")
        if trans_selection:
            for sel in trans_selection:
                trans_shape = cmds.listRelatives(sel, shapes=True)[0]
                trans_bs = cmds.listConnections("{}.inMesh".format(trans_shape))[0]
                extract_bs_targets(bs_node=trans_bs, geo=sel)

        elif bs_selection:
            for sel in bs_selection:
                bs_shape = cmds.listConnections("{}.outputGeometry".format(sel))[0]
                extract_bs_targets(bs_node=sel, geo=bs_shape)

    else:
        raise Exception("No Blendshape node found/selected, exiting")

    return None

# extract_bs_targets_runner(bs_node="", geo_trans="")
