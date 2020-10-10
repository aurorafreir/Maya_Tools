'''
viewport click to world position code from, edited to work here
https://gist.github.com/fredrikaverpil/731e5d43c35d6372e19864243c6e0231
'''

import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.cmds as cmds

global currentJoint

def lerp(min, max, percent):
    return ((max-min)*percent)+min

def vector_lerp(min, max, percent):
    x = lerp(min[0], max[0], percent)
    y = lerp(min[1], max[1], percent)
    z = lerp(min[2], max[2], percent)
    return x, y, z

def rayTrace():
    vpX, vpY, _ = cmds.draggerContext(rt, query=True, anchorPoint=True)
    position = om.MPoint()
    direction = om.MVector()
    #print vpX, vpY, position, direction
    omui.M3dView().active3dView().viewToWorld(
        int(vpX),
        int(vpY),
        position,  # world point
        direction)  # world vector

    for mesh in cmds.ls(type='mesh'):
        # Create a list which can hold MObjects, MPlugs, MDagPaths
        selectionList = om.MSelectionList()
        selectionList.add(mesh)  # Add mesh to list
        dagPath = selectionList.getDagPath(0)  # Path to a DAG node
        fnMesh = om.MFnMesh(dagPath)  # Function set for operation on meshes

        # Creates an array of all the worldSpace hits
        allIntersections = fnMesh.allIntersections(
            om.MFloatPoint(position),  # raySource
            om.MFloatVector(direction),  # rayDirection
            om.MSpace.kWorld,  # space
            99999,  # maxParam
            False)  # testBothDirections

    # Extract the different values from the intersection result
    hitPoint = allIntersections

    # Create a locator at the first and last intersection
    #cmds.spaceLocator(p=tuple([tup for tup in hitPoint[0][0]][:-1]), n='LOC_firstHit', a=True)
    #cmds.spaceLocator(p=tuple([tup for tup in hitPoint[0][1]][:-1]), n='LOC_lastHit', a=True)

    #centreLoc = vector_lerp(cmds.xform('LOC_firstHit', q=1, t=1, ws=1), cmds.xform('LOC_lastHit', q=1, t=1, ws=1), .5)
    #print vector_lerp(cmds.xform('LOC_firstHit', q=1, t=1, ws=1), cmds.xform('LOC_lastHit', q=1, t=1, ws=1), .5)
    print vector_lerp(tuple([tup for tup in hitPoint[0][0]][:-1]), tuple([tup for tup in hitPoint[0][1]][:-1]), .5)
    centre = vector_lerp(tuple([tup for tup in hitPoint[0][0]][:-1]), tuple([tup for tup in hitPoint[0][1]][:-1]), .5)
    cmds.spaceLocator(n='LOC_{}'.format(currentJoint))
    cmds.xform('LOC_{}'.format(currentJoint), t=centre)
    print currentJoint
    cmds.setToolTo('selectSuperContext')

rt = 'traceDraggerContext'

def worldClickPosition(joint):
    global currentJoint
    currentJoint = joint
    # checks if trace dragger context exists, and deletes if it exist
    if cmds.draggerContext(rt, exists=True):
        cmds.deleteUI(rt)
    cmds.draggerContext(rt, rc=rayTrace, cursor='crossHair')
    cmds.setToolTo(rt)

worldClickPosition('Shoulder')
