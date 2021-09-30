"""
Takes both an input Nurbs Surface, and a set of joint selections, and creates follicles on the Nurbs Surface
based on the closest position of each of the joints
"""

# Standard library imports

# Third party imports
import maya.cmds as cmds

# Local application imports


def create_follicle(nurbssurf, uPos=0.0, vPos=0.0):
    # Create a follicle object, and attach it to the NURBS surface (nurbssurf)
    follicle = cmds.createNode('follicle')

    cmds.connectAttr(nurbssurf + ".local", follicle + ".inputSurface")
    cmds.connectAttr(nurbssurf + ".worldMatrix[0]", follicle + ".inputWorldMatrix")
    for name, n in zip(["Rotate", "Translate"], ["r", "t"]):
        cmds.connectAttr(follicle + ".out" + name, cmds.listRelatives(follicle, p=1)[0] + "." + n)
    for uv, pos in zip(["U", "V"], [uPos, vPos]):
        cmds.setAttr(follicle + ".parameter" + uv, pos)
    for tr in ["t", "r"]:
        cmds.setAttr(cmds.listRelatives(follicle, p=1)[0] + "." + tr, lock=1)

    return follicle


def create_follicles_on_surf():
    
    nrbpatch = ""
    jntsel = []

    if not cmds.ls(sl=1):
        raise Exception("Nothing selected! Select a NURBS Curve, or NURBS Curve and NURBS Surface.")
    
    selected = cmds.ls(sl=1)

    jntsel = cmds.ls(sl=1, type="joint")
    nrbpatchsurf = cmds.listRelatives(selected, type="nurbsSurface", c=1)[0]
    nrbpatch = cmds.listRelatives(nrbpatchsurf, p=1)[0]

    print(jntsel)
    print(nrbpatch)


    # Set up groups for ribbon rig
    parentgrp = cmds.group(n="RibbonRig", em=1)
    for i in ["Joints", "Follicle"]:
        cmds.group(n=i + "_GRP", em=1, p=parentgrp)


     # Convert nrbpatch to poly mesh
    nrbpolypatch = cmds.nurbsToPoly(nrbpatch, ch=False)[0]


    # Get the NURBS Max V Range, so that follicles can be placed directly in the centre of it along the surface
    nrbvmax = cmds.getAttr(cmds.listRelatives(nrbpatch, s=1)[0] + ".minMaxRangeV")[0][1]
    nrbvmid = nrbvmax / 2

    countup = 0
    for i in jntsel:
        flcname = i.replace("_JNT", "_FLC")

        new_follicle = create_follicle(nrbpatch, 0, 0.5)
        cmds.rename(cmds.listRelatives(new_follicle, p=1)[0], flcname)
        cmds.parent(flcname, "Follicle_GRP")

        # Create nearestPointOnPoly node
        nearest_point_node = cmds.createNode("nearestPointOnMesh")
        
        # Attach new poly mesh and temp locator into nearestPointOnMesh node
        cmds.connectAttr(nrbpolypatch + ".worldMesh", nearest_point_node + ".inMesh")
        cmds.connectAttr(i + ".t", nearest_point_node + ".inPosition")
        
        paramu = cmds.getAttr(nearest_point_node + ".parameterU")
        
        # Make sure that paramu is never 0 or 1, as this can result in weird rotations
        if paramu == 0:
            paramu = 0.002
        if paramu == 1:
            paramu = 0.998

        # Set the follicles' u position
        cmds.setAttr(flcname + ".parameterU", paramu)

        # Cleanup
        cmds.delete(nearest_point_node)

        cmds.parentConstraint(flcname, i, mo=1)

        cmds.parent(i, "Joints_GRP")
        
    cmds.delete(nrbpolypatch)
    cmds.parent(nrbpatch, parentgrp)


create_follicles_on_surf()