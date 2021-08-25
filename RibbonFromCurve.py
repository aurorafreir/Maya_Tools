"""

"""

# Standard library imports
from math import pow,sqrt

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
    # DONE get input curve
    # DONE place joints for each curve CV
    # TODO create ribbon from curve
    # TODO place follicles for each joint
    # TODO move follicle to closest UV coord for each joint

    inputcrv = cmds.ls(sl=1)[0]

    parentgrp = cmds.group(n="RibbonRig", em=1)
    for i in ["Joints", "Follicle"]:
        cmds.group(n=i + "_GRP", em=1, p=parentgrp)

    # Get input curve and each CV on the curve
    inputcrv_cvs = cmds.getAttr(inputcrv + '.cp', s=1)
    # Create a joint for each curve CV
    joint_cur_name = 0
    for i in range(0, inputcrv_cvs):
        tempcv = inputcrv + ".cv[" + str(i) + "]"
        newjoint = cmds.joint(n="joint_" + str(joint_cur_name))
        cmds.xform(newjoint, t=(cmds.pointPosition(tempcv, l=1)), ws=1)
        cmds.parent(newjoint, "Joints_GRP")
        joint_cur_name = joint_cur_name + 1
        cmds.select(d=1)

    # create NURBS surface
    for i, x in zip(["A", "B"], [-.5, .5]):
        newcrv = cmds.duplicate(inputcrv, n=inputcrv + "_" + i)
        cmds.xform(newcrv, t=(0,0,x), r=1)

    nrbpatch = cmds.loft(inputcrv + "_A", inputcrv + "_B", n=inputcrv + "_NRB")
    nrbpatch = cmds.bakePartialHistory(nrbpatch)[0]
    cmds.parent(nrbpatch, parentgrp)

    for i in ["A", "B"]:
        cmds.delete(inputcrv + "_" + i)

    # Create follicles
    foll_cur_name = 0
    for i in range(0, inputcrv_cvs):
        oFoll = create_follicle(nrbpatch, 0.5, 0)
        cmds.rename("follicle1", "follicle_" + str(foll_cur_name))
        cmds.parent("follicle_" + str(foll_cur_name), "Follicle_GRP")
        foll_cur_name = foll_cur_name + 1
    cmds.select(d=1)


    # Convert nrbpatch to poly mesh
    nrbpolypatch = cmds.nurbsToPoly(nrbpatch, ch=False)
    nrbpolypatch = nrbpolypatch[0]

    for i in range(0, inputcrv_cvs):
        temp_follicle = "follicle_" + str(i)
        temp_joint = "joint_" + str(i)

        # Create nearestPointOnPoly node
        nearest_point_node = cmds.createNode("nearestPointOnMesh")

        cmds.connectAttr(nrbpolypatch + ".worldMesh", nearest_point_node + ".inMesh")
        cmds.connectAttr(temp_joint + ".t", nearest_point_node + ".inPosition")

        paramv = cmds.getAttr(nearest_point_node + ".parameterV")
        if paramv == 0:
            paramv = 0.001

        cmds.setAttr(temp_follicle + ".parameterV", paramv)

        cmds.delete(nearest_point_node)

        cmds.parentConstraint(temp_follicle, temp_joint)

    cmds.delete(nrbpolypatch)


ribbon_from_crv()