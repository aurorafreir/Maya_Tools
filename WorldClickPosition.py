'''
viewport click to world position code from
https://gist.github.com/fredrikaverpil/731e5d43c35d6372e19864243c6e0231
'''

import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.cmds as cmds

# Maya Python API:
# http://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__py_ref_index_html

'''
def onPress():
    """Take x,y from mouse click, convert into 3d world coordinates"""
    vpX, vpY, _ = cmds.draggerContext(ctx, query=True, anchorPoint=True)
    position = om.MPoint()  # 3D point with double-precision coordinates
    direction = om.MVector()  # 3D vector with double-precision coordinates

    # This takes vpX and vpY as input and outputs position and direction
    # values for the active view.
    # - M3dView: provides methods for working with 3D model views
    # - active3dView(): Returns the active view in the form of a class
    # - viewToWorld: Takes a point in port coordinates and
    #                returns a corresponding ray in world coordinates
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

        # Find the closest intersection with the mesh and of a ray (starting
        # at raySource and travelling in rayDirection).
        # The maxParam and testBothDirections flags can be used to control
        # the radius of the search around the raySource point.
        intersection = fnMesh.closestIntersection(
            om.MFloatPoint(position),  # raySource
            om.MFloatVector(direction),  # rayDirection
            om.MSpace.kWorld,  # space
            99999,  # maxParam
            False)  # testBothDirections
        allIntersections = fnMesh.closestIntersection(
            om.MFloatPoint(position),  # raySource
            om.MFloatVector(direction),  # rayDirection
            om.MSpace.kWorld,  # space
            99999,  # maxParam
            False)  # testBothDirections

        # Extract the different values from the intersection result
        hitPoint, hitRayParam, hitFace, hitTriangle, \
            hitBary1, hitBary2 = allIntersections

        # Extract x, y, z world coordinates of the hitPoint result
        print hitFace
        x, y, z, _ = hitPoint
        if (x, y, z) != (0.0, 0.0, 0.0):
            print(x, y, z)  # Print the world coordinates
    xyz = [x, y, z]
    #print xyz
    cmds.spaceLocator(p=xyz)
    #return xyz

# Name of dragger context
ctx = 'Click2dTo3dCtx'
# Delete dragger context if it already exists
if cmds.draggerContext(ctx, exists=True):
    cmds.deleteUI(ctx)
# Create dragger context and set it to the active tool
cmds.draggerContext(ctx, pressCommand=onPress, name=ctx, cursor='crossHair')
cmds.setToolTo(ctx)
'''

rt = 'traceDraggerContext'

def worldClickPosition():
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

        allIntersections = fnMesh.allIntersections(
            om.MFloatPoint(position),  # raySource
            om.MFloatVector(direction),  # rayDirection
            om.MSpace.kWorld,  # space
            99999,  # maxParam
            False)  # testBothDirections

    # Extract the different values from the intersection result
    hitPoint = allIntersections
    #print hitPoint
    #print type(hitPoint)
    #print hitPoint[0][0]
    print (tuple([tup for tup in hitPoint[0][0]][:-1]))
    #cmds.spaceLocator(p=(tuple([tup for tup in hitPoint[0][0]])))
    cmds.spaceLocator(p=tuple([tup for tup in hitPoint[0][0]][:-1]))
    cmds.spaceLocator(p=tuple([tup for tup in hitPoint[0][1]][:-1]))

    # Extract x, y, z world coordinates of the hitPoint result
    x, y, z, x2, y2, z2 = hitPoint
    #print (x[0], y[0], z[0], x2[0], y2[0], z2[0])
    #print x[0]

    #cmds.spaceLocator(p=(x2[0], y2[0], z2[0]))
    #cmds.spaceLocator(p=(x[0])
    #x, y, z, _ = hitPoint[0]
    #if (x, y, z) != (0.0, 0.0, 0.0):
    #    print(x, y, z)  # Print the world coordinates

    cmds.setToolTo('selectSuperContext')


def rayTrace():
    # checks if trace dragger context exists, and deletes if it exist
    if cmds.draggerContext(rt, exists=True):
        cmds.deleteUI(rt)
    cmds.draggerContext(rt, rc=worldClickPosition, cursor='crossHair')
    cmds.setToolTo(rt)

rayTrace()