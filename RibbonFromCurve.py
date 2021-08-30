"""
Creates a ribbon rig from an input NURBS Curve and NURBS Surface, while handling inconsistent cv/joint placement
Works by selecting either just a NURBS Curve and running, or selecting a NURBS Curve and Surface and running
"""

# TODO Make code work with just a NURBS Surface selected

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


def ribbon_from_crv():

    nrbpatch = ""

    if not cmds.ls(sl=1):
        raise Exception("Nothing selected! Select a NURBS Curve, or NURBS Curve and NURBS Surface.")
        return

    if cmds.objectType(cmds.listRelatives(cmds.ls(sl=1), type="nurbsCurve", c=1)) == "nurbsCurve":
        inputcrv = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl=1), type="nurbsCurve", c=1)[0], p=1)[0]

    if not len(cmds.ls(sl=1)) == 1:
        nurbssurface = cmds.listRelatives(cmds.ls(sl=1)[1], type="nurbsSurface", c=1)
        if not len(nurbssurface) == 1: # Make sure that nurbssurface is only the first Shape node
            nurbssurface = nurbssurface[0]
        if cmds.objectType(nurbssurface) == "nurbsSurface":
            nrbpatch = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl=1), type="nurbsSurface", c=1)[0], p=1)[0]

    if inputcrv:
        print("input curve = " + inputcrv)
    if nrbpatch:
        print("input surface = " + nrbpatch)

    # Set up groups for ribbon rig
    parentgrp = cmds.group(n="RibbonRig", em=1)
    for i in ["Joints", "Follicle"]:
        cmds.group(n=i + "_GRP", em=1, p=parentgrp)

    # Get input curve and each CV on the curve
    inputcrv_cvs = cmds.getAttr(inputcrv + '.cp', s=1)
    # Create a joint for each curve CV
    for i in range(0, inputcrv_cvs):
        tempcv = inputcrv + ".cv[" + str(i) + "]"
        newjoint = cmds.joint(n="joint_" + str(i))
        cmds.xform(newjoint, t=(cmds.pointPosition(tempcv, l=1)), ws=1)
        cmds.parent(newjoint, "Joints_GRP")
        cmds.select(d=1)

    # Create NURBS surface if one isn't selected
    # (Not recommended, very simplistic creation)
    if not nrbpatch:
        raise Exception("It is recommended to create your own NURBS Surface, this Surface creation is very simplistic!")
        for i, x in zip(["A", "B"], [-.5, .5]):
            newcrv = cmds.duplicate(inputcrv, n=inputcrv + "_" + i)
            cmds.xform(newcrv, t=(0, 0, x), r=1)
        nrbpatch = cmds.loft(inputcrv + "_A", inputcrv + "_B", n=inputcrv + "_NRB")
        nrbpatch = cmds.bakePartialHistory(nrbpatch)[0]
        for i in ["A", "B"]:
            cmds.delete(inputcrv + "_" + i)


    # Create follicles
    for i in range(inputcrv_cvs):
        oFoll = create_follicle(nrbpatch, 0, 0.5)
        cmds.rename("follicle1", "follicle_" + str(i))
        cmds.parent("follicle_" + str(i), "Follicle_GRP")
    cmds.select(d=1)


    # Convert nrbpatch to poly mesh
    nrbpolypatch = cmds.nurbsToPoly(nrbpatch, ch=False)
    nrbpolypatch = nrbpolypatch[0]

    # Get the NURBS Max V Range, so that follicles can be placed directly in the centre of it along the surface
    nrbvmax = cmds.getAttr(cmds.listRelatives(nrbpatch, s=1)[0] + ".minMaxRangeV")[0][1]

    for i in range(inputcrv_cvs):
        temp_follicle = "follicle_" + str(i)

        temp_loc = cmds.spaceLocator(n="tempLoc_" + str(i))[0]
        cmds.select(d=1)
        loc_pos = cmds.pointOnSurface(nrbpatch, u=i, v=nrbvmax / 2, position=True)
        cmds.xform(temp_loc, t=loc_pos, ws=1)

        # Create nearestPointOnPoly node
        nearest_point_node = cmds.createNode("nearestPointOnMesh")
        
        # Attach new poly mesh and temp locator into nearestPointOnMesh node
        cmds.connectAttr(nrbpolypatch + ".worldMesh", nearest_point_node + ".inMesh")
        cmds.connectAttr(temp_loc + ".t", nearest_point_node + ".inPosition")
        
        paramu = cmds.getAttr(nearest_point_node + ".parameterU")
        
        # Make sure that paramu is never 0 or 1, as this can result in weird rotations
        if paramu == 0:
            paramu = 0.002
        if paramu == 1:
            paramu = 0.998

        # Set the follicles' u position
        cmds.setAttr(temp_follicle + ".parameterU", paramu)

        # Cleanup
        cmds.delete(nearest_point_node)
        cmds.delete(temp_loc)


        cmds.parentConstraint(temp_follicle, "joint_" + str(i))

    # Final cleanup
    cmds.hide("Follicle_GRP")
    cmds.delete(nrbpolypatch)
    cmds.parent(nrbpatch, parentgrp)
    cmds.parent(inputcrv, parentgrp)
    cmds.hide(inputcrv)

ribbon_from_crv()
