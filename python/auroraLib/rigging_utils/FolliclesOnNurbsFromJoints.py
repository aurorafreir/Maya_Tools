"""
Takes both an input Nurbs Surface, and a set of joint selections, and creates follicles on the Nurbs Surface
based on the closest position of each of the joints
Joints must have the "_JNT" suffix
"""

# Standard library imports

# Third party imports
import maya.cmds as cmds

# Local application imports



def create_follicle(nurbs_surf, uPos=0.0, vPos=0.0):
    # Create a follicle object, and attach it to the NURBS surface (nurbs_surf)
    follicle = cmds.createNode('follicle')

    cmds.connectAttr("{}.local".format(nurbs_surf), "{}.inputSurface".format(follicle))
    cmds.connectAttr("{}.worldMatrix[0]".format(nurbs_surf), "{}.inputWorldMatrix".format(follicle))
    for attr, a in zip(["Rotate", "Translate"], ["r", "t"]):
        cmds.connectAttr("{}.out{}".format(follicle, attr), "{}.{}".format(cmds.listRelatives(follicle, parent=True)[0], a))
    for uv, pos in zip(["U", "V"], [uPos, vPos]):
        cmds.setAttr("{}.parameter{}".format(follicle, uv), pos)
    for tr in ["t", "r"]:
        cmds.setAttr("{}.{}".format(cmds.listRelatives(follicle, parent=True)[0], tr), lock=True)

    return follicle


def create_follicles_on_surf():
    
    nrb_patch = ""
    jnt_sel = []

    if not cmds.ls(selection=True):
        raise Exception("Nothing selected! Select a NURBS Curve, or NURBS Curve and NURBS Surface.")
    
    selected = cmds.ls(selection=True)

    jnt_sel = cmds.ls(selection=True, type="joint")
    nrb_patch_surf = cmds.listRelatives(selected, type="nurbsSurface", children=1)[0]
    nrb_patch = cmds.listRelatives(nrb_patch_surf, parent=1)[0]


    # Set up groups for ribbon rig
    parent_grp = cmds.group(name="RibbonRig", empty=True)
    for group_name in ["Joints", "Follicle"]:
        cmds.group(name="{}_GRP".format(group_name), empty=True, parent=parent_grp)


     # Convert nrb_patch to poly mesh
    nrb_poly_patch = cmds.nurbsToPoly(nrb_patch, constructionHistory=False)[0]


    # Get the NURBS Max V Range, so that follicles can be placed directly in the centre of it along the surface
    nrb_v_max = cmds.getAttr("{}.minMaxRangeV".format(cmds.listRelatives(nrb_patch, shapes=True)[0]))[0][1]
    nrb_v_mid = nrb_v_max / 2

    countup = 0
    for jnt in jnt_sel:
        flc_name = jnt.replace("_JNT", "_FLC")

        new_follicle = create_follicle(nrb_patch, 0, .5)
        cmds.rename(cmds.listRelatives(new_follicle, p=1)[0], flc_name)
        cmds.parent(flc_name, "Follicle_GRP")

        # Create nearestPointOnPoly node
        nearest_point_node = cmds.createNode("nearestPointOnMesh")
        
        # Attach new poly mesh and temp locator into nearestPointOnMesh node
        cmds.connectAttr("{}.worldMesh".format(nrb_poly_patch), "{}.inMesh".format(nearest_point_node))
        cmds.connectAttr("{}.t".format(jnt), "{}.inPosition".format(nearest_point_node))
        
        paramu = cmds.getAttr("{}.parameterU".format(nearest_point_node))
        
        # Make sure that paramu is never 0 or 1, as this can result in weird rotations
        if paramu == 0:
            paramu = 0.002
        if paramu == 1:
            paramu = 0.998

        # Set the follicles' u position
        cmds.setAttr("{}.parameterU".format(flc_name), paramu)

        # Cleanup
        cmds.delete(nearest_point_node)

        cmds.parentConstraint(flc_name, jnt, maintainOffset=True)

        cmds.parent(jnt, "Joints_GRP")
        
    cmds.delete(nrb_poly_patch)
    cmds.parent(nrb_patch, parent_grp)



