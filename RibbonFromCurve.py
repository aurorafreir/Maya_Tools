"""
Creates a ribbon rig from an input NURBS Curve and NURBS Surface, while handling inconsistent cv/joint placement
"""

# Standard library imports

# Third party imports
import maya.cmds as cmds

# Local application imports


def create_follicle(oNurbs, uPos=0.0, vPos=0.0, pName=""):
    # place and connect a follicle onto a nurbs surface.
    oFoll = cmds.createNode('follicle')
    cmds.connectAttr(oNurbs + ".local", oFoll + ".inputSurface")

    cmds.connectAttr(oNurbs + ".worldMatrix[0]", oFoll + ".inputWorldMatrix")
    cmds.connectAttr(oFoll + ".outRotate", cmds.listRelatives(oFoll, p=1)[0] + ".r")
    cmds.connectAttr(oFoll + ".outTranslate", cmds.listRelatives(oFoll, p=1)[0] + ".t")
    cmds.setAttr(oFoll + ".parameterU", uPos)
    cmds.setAttr(oFoll + ".parameterV", vPos)
    cmds.setAttr(cmds.listRelatives(oFoll, p=1)[0] + ".t", lock=1)
    cmds.setAttr(cmds.listRelatives(oFoll, p=1)[0] + ".r", lock=1)

    return oFoll


def ribbon_from_crv():

    nrbpatch = ""

    if not cmds.ls(sl=1):
        raise Exception("No input curve or input surface found!")
        return
    # print cmds.listRelatives(cmds.ls(sl=1)[1], type="nurbsSurface", c=1)
    if cmds.objectType(cmds.listRelatives(cmds.ls(sl=1), type="nurbsCurve", c=1)) == "nurbsCurve":
        inputcrv = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl=1), type="nurbsCurve", c=1)[0], p=1)[0]

    if not len(cmds.ls(sl=1)) == 1:
        nurbssurface = cmds.listRelatives(cmds.ls(sl=1)[1], type="nurbsSurface", c=1)
        if not len(nurbssurface) == 1: # Make sure that nurbssurface is only the first Shape node
            nurbssurface = nurbssurface[0]
        if cmds.objectType(nurbssurface) == "nurbsSurface":
            nrbpatch = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl=1), type="nurbsSurface", c=1)[0], p=1)[0]


    print("input curve = " + inputcrv)
    if nrbpatch:
        print("input surface = " + nrbpatch)

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

    # create NURBS surface if one isn't selected
    if not nrbpatch:
        for i, x in zip(["A", "B"], [-.5, .5]):
            newcrv = cmds.duplicate(inputcrv, n=inputcrv + "_" + i)
            cmds.xform(newcrv, t=(0, 0, x), r=1)
        nrbpatch = cmds.loft(inputcrv + "_A", inputcrv + "_B", n=inputcrv + "_NRB")
        nrbpatch = cmds.bakePartialHistory(nrbpatch)[0]
        for i in ["A", "B"]:
            cmds.delete(inputcrv + "_" + i)


    # Create follicles
    foll_cur_name = 0
    for i in range(0, inputcrv_cvs):
        oFoll = create_follicle(nrbpatch, 0, 0.5)
        cmds.rename("follicle1", "follicle_" + str(foll_cur_name))
        cmds.parent("follicle_" + str(foll_cur_name), "Follicle_GRP")
        foll_cur_name = foll_cur_name + 1
    cmds.select(d=1)


    # Convert nrbpatch to poly mesh
    nrbpolypatch = cmds.nurbsToPoly(nrbpatch, ch=False)
    nrbpolypatch = nrbpolypatch[0]

    nrbvmax = cmds.getAttr(cmds.listRelatives(nrbpatch, s=1)[0] + ".minMaxRangeV")[0][1]

    for i in range(inputcrv_cvs):
        temp_follicle = "follicle_" + str(i)

        temp_loc = cmds.spaceLocator(n="tempLoc_" + str(i))[0]
        cmds.select(d=1)
        loc_pos = cmds.pointOnSurface(nrbpatch, u=i, v=nrbvmax / 2, position=True)
        cmds.xform(temp_loc, t=loc_pos, ws=1)


        # Create nearestPointOnPoly node
        nearest_point_node = cmds.createNode("nearestPointOnMesh")

        cmds.connectAttr(nrbpolypatch + ".worldMesh", nearest_point_node + ".inMesh")
        cmds.connectAttr(temp_loc + ".t", nearest_point_node + ".inPosition")

        paramu = cmds.getAttr(nearest_point_node + ".parameterU")
        if paramu == 0:
            paramu = 0.001

        cmds.setAttr(temp_follicle + ".parameterU", paramu)

        cmds.delete(nearest_point_node)
        cmds.delete(temp_loc)

        cmds.parentConstraint(temp_follicle, "joint_" + str(i))

    cmds.hide("Follicle_GRP")
    cmds.delete(nrbpolypatch)
    cmds.parent(nrbpatch, parentgrp)
    cmds.parent(inputcrv, parentgrp)
    cmds.hide(inputcrv)


ribbon_from_crv()