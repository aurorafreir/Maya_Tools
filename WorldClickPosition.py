'''
viewport click to world position code from, edited to work here
https://gist.github.com/fredrikaverpil/731e5d43c35d6372e19864243c6e0231
'''

import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.cmds as cmds

# global script variables
global current_joint
global symmetry

symmetry_joints = [
    'L_Shoulder', 'R_Shoulder',
    'L_Leg', 'R_Leg'
]

# 2d lerp
def lerp(min, max, percent):
    return ((max-min)*percent)+min

# 3d lerp
def vector_lerp(min, max, percent):
    x = lerp(min[0], max[0], percent)
    y = lerp(min[1], max[1], percent)
    z = lerp(min[2], max[2], percent)
    return x, y, z

def ray_trace():
    if cmds.objExists('LOC_{}'.format(current_joint)):
        print "obj already exists"
        cmds.setToolTo('selectSuperContext')
    else:
        vpX, vpY, _ = cmds.draggerContext(rt, query=True, anchorPoint=True)
        position = om.MPoint()
        direction = om.MVector()
        #print vpX, vpY, position, direction
        omui.M3dView().active3dView().viewToWorld(
            int(vpX),  # Viewport click X position as int
            int(vpY),  # Viewport click Y position as int
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
        # Extract hit values from the intersection result
        hitPoint = allIntersections
        #sets the 'centre' var to the midpoint first and last intersection
        temp_start = [tup for tup in hitPoint[0][0]][:-1]
        temp_end = [tup for tup in hitPoint[0][1]][:-1]
        centre = vector_lerp(temp_start, temp_end, .5)
        # creates a locator at 0,0,0, and moves it to the centre point of the click
        cmds.spaceLocator(n='LOC_{}'.format(current_joint))
        cmds.xform('LOC_{}'.format(current_joint), t=centre)
        #print ('LOC_{}'.format(current_joint)).replace('_L_', '_R_')
        print symmetry
        if symmetry and current_joint in symmetry_joints:
            current_joint_symmetry = ('LOC_{}'.format(current_joint)).replace('_L_', '_R_')
            #centre_flipped = centre
            xyz = list(centre)
            xyz[0] = centre[0] * -1
            centre_flipped = tuple(xyz)
            #centre_flipped[0] = centre[0] * -1
            #print centre
            #print centre_flipped
            cmds.spaceLocator(n=current_joint_symmetry)
            cmds.xform(current_joint_symmetry, t=centre_flipped)
            cmds.select('LOC_{}'.format(current_joint))
        # sets the current tool back to the selector
        cmds.setToolTo('selectSuperContext')

rt = 'traceDraggerContext'

def world_click_position(joint):
    global current_joint
    current_joint = joint
    # checks if trace dragger context exists, and deletes if it exist
    if cmds.draggerContext(rt, exists=True):
        cmds.deleteUI(rt)
    # calls the rayTrace func, and then sets the tool to the rt draggerContext
    cmds.draggerContext(rt, rc=ray_trace, cursor='crossHair')
    cmds.setToolTo(rt)

def build_rig():
    # print 'Rig Build currently not working'
    all_locators = [
        'LOC_Hips', 'LOC_L_Shoulder', 'LOC_R_Shoulder', 'LOC_L_Leg', 'LOC_R_Leg'
    ]
    # check if all joints exist
    found_locators = cmds.ls(all_locators)
    #print all_locators
    #print found_locators
    if found_locators == all_locators:
        for i in all_locators:
            joint_name = i.replace('LOC_', 'JNT_')
            print joint_name
            #cmds.joint()
            #cmds.rename('joint1', joint_name)
            cmds.joint(n='{}'.format(joint_name), p=(0,0,0))
            new_location = cmds.xform((i), q=True, t=True)
            print new_location
            cmds.xform('{}'.format(joint_name), t=new_location)
            cmds.select(d=True)
    else:
        print "missing locators"


def create_window():
    global symmetry

    # sets a window ID
    winID = 'aurtorigger'
    # checks if the window ID already exists and deletes it if it does
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)

    cmds.window(winID, title='Aurtorigger')
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, width=200)
    cmds.checkBox('symmetryCheckbox', label='Automatic Symmetry', v=1, onc='symmetry=1', ofc='symmetry=0')
    symmetry = cmds.checkBox('symmetryCheckbox', q=1, v=1)

    cmds.frameLayout(label='Arms', labelAlign='top')
    cmds.rowColumnLayout("NurbsColours", numberOfColumns=2)
    cmds.button(label='L_Shoulder', ann='', command='world_click_position("L_Shoulder")')
    cmds.button(label='R_Shoulder', ann='', command='world_click_position("R_Shoulder")')
    cmds.setParent('..')

    cmds.frameLayout(label='', labelAlign='top')
    cmds.button(label='Spine 1', ann='', command='world_click_position("Spine_1")')
    cmds.button(label='Hips', ann='', command='world_click_position("Hips")')
    cmds.setParent('..')

    cmds.frameLayout(label='Legs', labelAlign='top')
    cmds.rowColumnLayout("NurbsColours", numberOfColumns=2)
    cmds.button(label='L_Leg', ann='', command='world_click_position("L_Leg")')
    cmds.button(label='R_Leg', ann='', command='world_click_position("R_Leg")')
    cmds.setParent('..')

    cmds.checkBox(label='Smooth twist limbs')

    cmds.button(label='B U I L D    R I G', bgc=(.8,.3,.3), command='build_rig()')

    cmds.showWindow()

create_window()
