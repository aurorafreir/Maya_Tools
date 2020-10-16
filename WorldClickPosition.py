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
global centre_mid_joints
symmetry_joints = []

# list of joints that would require symmetry if created
L_symmetry_joints = [
    'L_Scapula', 'L_Shoulder', 'L_Elbow', 'L_Wrist',
    'L_Leg', 'L_Knee', 'L_Ankle',

    'L_Index1', 'L_Index2', 'L_Index3',
    'L_Middle1', 'L_Middle2', 'L_Middle3',
    'L_Ring1', 'L_Ring2', 'L_Ring3',
    'L_Pinky1', 'L_Pinky2', 'L_Pinky3',
    'L_Thumb1', 'L_Thumb2', 'L_Thumb3',
]
for i in L_symmetry_joints:
    symmetry_joints.append(i.replace('L_', 'R_'))
symmetry_joints.append(L_symmetry_joints)


# finds the point between two numbers based on the Percent variable
def lerp(min, max, percent):
    return ((max-min)*percent)+min


# finds the point in 3d space between two XYZ positions in world space
def vector_lerp(min, max, percent):
    x = lerp(min[0], max[0], percent)
    y = lerp(min[1], max[1], percent)
    z = lerp(min[2], max[2], percent)
    return x, y, z


def ray_trace():
    # this function creates the locators based on where the user clicks in the viewport
    # checks if the current locator is already created

    if cmds.objExists('LOC_{}'.format(current_joint)):
        print "obj already exists"
        cmds.setToolTo('selectSuperContext')
    else:
        vpX, vpY, _ = cmds.draggerContext(rt, query=True, anchorPoint=True)
        position = om.MPoint()
        direction = om.MVector()
        # print vpX, vpY, position, direction
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

        # sets the 'centre' var to the midpoint first and last intersection
        temp_start = [tup for tup in hitPoint[0][0]][:-1]
        temp_end = [tup for tup in hitPoint[0][1]][:-1]
        centre = vector_lerp(temp_start, temp_end, .5)

        # creates a locator at 0,0,0, and moves it to the centre point of the click
        loc_current_joint = 'LOC_{}'.format(current_joint)
        cmds.spaceLocator(n=loc_current_joint)
        cmds.xform(loc_current_joint, t=centre)

        if symmetry and current_joint in symmetry_joints:
            current_joint_symmetry = (loc_current_joint).replace('_L_', '_R_')
            # centre_flipped = centre
            xyz = list(centre)
            xyz[0] = centre[0] * -1
            centre_flipped = tuple(xyz)
            cmds.spaceLocator(n=current_joint_symmetry)
            cmds.xform(current_joint_symmetry, t=centre_flipped)
            cmds.select(loc_current_joint)

        # sets the current tool back to the selector
        cmds.setToolTo('selectSuperContext')


rt = 'traceDraggerContext'


def world_click_position(joint):
    # this function checks if the draggerContext exists, and it it does,
    # deletes the old one before making a new one
    global current_joint
    current_joint = joint
    # checks if trace dragger context exists, and deletes if it exist
    if cmds.draggerContext(rt, exists=True):
        cmds.deleteUI(rt)
    # calls the rayTrace func, and then sets the tool to the rt draggerContext
    cmds.draggerContext(rt, rc=ray_trace, cursor='crossHair')
    cmds.setToolTo(rt)


def build_rig():
    # this function creates all the joints
    global centre_mid_joints
    # makes sure nothing is selected so that joints don't get parented to other objects
    cmds.select(d=True)

    # list of all the locators that should be centred if centre_mid_joints is on
    centre_joints = [
        'LOC_Head', 'LOC_Neck', 'LOC_Chest', 'LOC_Hips'
    ]
    # Checks if centre_mid_joints is checked on, and sets the middle joints to 0 on the X axis
    found_centre_locators = cmds.ls(centre_joints)
    if centre_mid_joints:
        for i in found_centre_locators:
            xyz = cmds.xform(i, t=1, q=1)
            cmds.xform(i, t=(0, xyz[1], xyz[2]))

    # List of all the joints that are required to make a rig
    required_locators = [
        'LOC_Hips', 'LOC_Chest', 'LOC_Neck', 'LOC_Head',
        'LOC_L_Shoulder', 'LOC_R_Shoulder',
        'LOC_L_Elbow', 'LOC_R_Elbow',
        'LOC_L_Wrist', 'LOC_R_Wrist',
        'LOC_L_Leg', 'LOC_R_Leg',
        'LOC_L_Knee', 'LOC_R_Knee',
        'LOC_L_Ankle', 'LOC_R_Ankle'
    ]

    # List of all the joints that aren't required to make the rig, but can still be built
    not_required_locators = [
        'LOC_L_Scapula', 'LOC_R_Scapula',
        'LOC_L_Index1', 'LOC_L_Index2', 'LOC_L_Index3',
        'LOC_L_Middle1', 'LOC_L_Middle2', 'LOC_L_Middle3',
        'LOC_L_Ring1', 'LOC_L_Ring2', 'LOC_L_Ring3',
        'LOC_L_Pinky1', 'LOC_L_Pinky2', 'LOC_L_Pinky3',
        'LOC_L_Thumb1', 'LOC_L_Thumb2', 'LOC_L_Thumb3',

        'LOC_R_Index1', 'LOC_R_Index2', 'LOC_R_Index3',
        'LOC_R_Middle1', 'LOC_R_Middle2', 'LOC_R_Middle3',
        'LOC_R_Ring1', 'LOC_R_Ring2', 'LOC_R_Ring3',
        'LOC_R_Pinky1', 'LOC_R_Pinky2', 'LOC_R_Pinky3',
        'LOC_R_Thumb1', 'LOC_R_Thumb2', 'LOC_R_Thumb3'
    ]

    # searches the scene for the locators from all_locators and sets them in found_locators
    found_required_locators = cmds.ls(required_locators)

    # creates all the joints that are required by the scene,
    # and if they don't all exist, creates a popup dialog saying which are missing
    if found_required_locators == required_locators:
        for i in required_locators:
            joint_name = i.replace('LOC_', 'JNT_')
            if not cmds.objExists(joint_name):
                cmds.joint(n='{}'.format(joint_name), p=(0, 0, 0))
                new_location = cmds.xform(i, q=True, t=True)
                cmds.xform('{}'.format(joint_name), t=new_location)
                cmds.select(d=True)
    else:
        set1 = set(found_required_locators)
        set2 = set(required_locators)
        print list(sorted(set2 - set1))
        cmds.confirmDialog(message='{} joints missing'.format(list(sorted(set2 - set1))))

    # creates all the joints that aren't required to make the rig
    for i in not_required_locators:
        joint_name = i.replace('LOC_', 'JNT_')
        if cmds.objExists(i):
            if not cmds.objExists(joint_name):
                cmds.joint(n='{}'.format(joint_name), p=(0, 0, 0))
                new_location = cmds.xform(i, q=True, t=True)
                cmds.xform('{}'.format(joint_name), t=new_location)
                cmds.select(d=True)

    # Sets up the parents for the joints, after checking that they're not already parented
    if found_required_locators == required_locators:
        if not cmds.listRelatives('JNT_Chest', p=True):
            cmds.parent('JNT_Chest', 'JNT_Hips')
        if not cmds.listRelatives('JNT_Neck', p=True):
            cmds.parent('JNT_Neck', 'JNT_Chest')
        if not cmds.listRelatives('JNT_Head', p=True):
            cmds.parent('JNT_Head', 'JNT_Neck')
        # parenting for joints with both L and R sides
        for i in ['L', 'R']:
            if cmds.objExists('JNT_{}_Scapula'.format(i)):
                if not cmds.listRelatives('JNT_{}_Scapula'.format(i), p=True):
                    cmds.parent('JNT_{}_Scapula'.format(i), 'JNT_Chest')
                if not cmds.listRelatives('JNT_{}_Shoulder'.format(i), p=True):
                    cmds.parent('JNT_{}_Shoulder'.format(i), 'JNT_{}_Scapula'.format(i))
            else:
                cmds.parent('JNT_{}_Shoulder'.format(i), 'JNT_Chest')

            if not cmds.listRelatives('JNT_{}_Elbow'.format(i), p=True):
                cmds.parent('JNT_{}_Elbow'.format(i), 'JNT_{}_Shoulder'.format(i))
            if not cmds.listRelatives('JNT_{}_Wrist'.format(i), p=True):
                cmds.parent('JNT_{}_Wrist'.format(i), 'JNT_{}_Elbow'.format(i))
            if not cmds.listRelatives('JNT_{}_Leg'.format(i), p=True):
                cmds.parent('JNT_{}_Leg'.format(i), 'JNT_Hips')
            if not cmds.listRelatives('JNT_{}_Knee'.format(i), p=True):
                cmds.parent('JNT_{}_Knee'.format(i), 'JNT_{}_Leg'.format(i))
            if not cmds.listRelatives('JNT_{}_Ankle'.format(i), p=True):
                cmds.parent('JNT_{}_Ankle'.format(i), 'JNT_{}_Knee'.format(i))

            # fingers #
            if cmds.objExists('JNT_{}_Thumb1'.format(i)):
                if not cmds.listRelatives('JNT_{}_Thumb1'.format(i), p=True):
                    cmds.parent('JNT_{}_Thumb1'.format(i), 'JNT_{}_Wrist'.format(i))
                if not cmds.listRelatives('JNT_{}_Thumb2'.format(i), p=True):
                    cmds.parent('JNT_{}_Thumb2'.format(i), 'JNT_{}_Thumb1'.format(i))
                if not cmds.listRelatives('JNT_{}_Thumb3'.format(i), p=True):
                    cmds.parent('JNT_{}_Thumb3'.format(i), 'JNT_{}_Thumb2'.format(i))

            if cmds.objExists('JNT_{}_Index1'.format(i)):
                if not cmds.listRelatives('JNT_{}_Index1'.format(i), p=True):
                    cmds.parent('JNT_{}_Index1'.format(i), 'JNT_{}_Wrist'.format(i))
                if not cmds.listRelatives('JNT_{}_Index2'.format(i), p=True):
                    cmds.parent('JNT_{}_Index2'.format(i), 'JNT_{}_Index1'.format(i))
                if not cmds.listRelatives('JNT_{}_Index3'.format(i), p=True):
                    cmds.parent('JNT_{}_Index3'.format(i), 'JNT_{}_Index2'.format(i))

            if cmds.objExists('JNT_{}_Middle1'.format(i)):
                if not cmds.listRelatives('JNT_{}_Middle1'.format(i), p=True):
                    cmds.parent('JNT_{}_Middle1'.format(i), 'JNT_{}_Wrist'.format(i))
                if not cmds.listRelatives('JNT_{}_Middle2'.format(i), p=True):
                    cmds.parent('JNT_{}_Middle2'.format(i), 'JNT_{}_Middle1'.format(i))
                if not cmds.listRelatives('JNT_{}_Middle3'.format(i), p=True):
                    cmds.parent('JNT_{}_Middle3'.format(i), 'JNT_{}_Middle2'.format(i))

            if cmds.objExists('JNT_{}_Ring1'.format(i)):
                if not cmds.listRelatives('JNT_{}_Ring1'.format(i), p=True):
                    cmds.parent('JNT_{}_Ring1'.format(i), 'JNT_{}_Wrist'.format(i))
                if not cmds.listRelatives('JNT_{}_Ring2'.format(i), p=True):
                    cmds.parent('JNT_{}_Ring2'.format(i), 'JNT_{}_Ring1'.format(i))
                if not cmds.listRelatives('JNT_{}_Ring3'.format(i), p=True):
                    cmds.parent('JNT_{}_Ring3'.format(i), 'JNT_{}_Ring2'.format(i))

            if cmds.objExists('JNT_{}_Pinky1'.format(i)):
                if not cmds.listRelatives('JNT_{}_Pinky1'.format(i), p=True):
                    cmds.parent('JNT_{}_Pinky1'.format(i), 'JNT_{}_Wrist'.format(i))
                if not cmds.listRelatives('JNT_{}_Pinky2'.format(i), p=True):
                    cmds.parent('JNT_{}_Pinky2'.format(i), 'JNT_{}_Pinky1'.format(i))
                if not cmds.listRelatives('JNT_{}_Pinky3'.format(i), p=True):
                    cmds.parent('JNT_{}_Pinky3'.format(i), 'JNT_{}_Pinky2'.format(i))


def create_window():
    # this function creates the window and UI for the script

    global symmetry
    global centre_mid_joints
    required_joints_colour = (.7,.6,.6)

    # sets a window ID
    win_id = 'aurtorigger'
    # checks if the window ID already exists and deletes it if it does
    if cmds.window(win_id, exists=True):
        cmds.deleteUI(win_id)

    cmds.window(win_id, title='Aurtorigger')
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, width=200)
    cmds.checkBox('symmetryCheckbox', label='Automatic Symmetry', v=1, onc='symmetry=1', ofc='symmetry=0')
    symmetry = cmds.checkBox('symmetryCheckbox', q=1, v=1)

    cmds.frameLayout(label='Arms', labelAlign='top')
    cmds.rowColumnLayout("arms_buttons", numberOfColumns=2)
    cmds.button(label='L_Scapula', ann='', command='world_click_position("L_Scapula")')
    cmds.button(label='R_Scapula', ann='', command='world_click_position("R_Scapula")')
    cmds.button(label='L_Shoulder', ann='', command='world_click_position("L_Shoulder")', bgc=required_joints_colour)
    cmds.button(label='R_Shoulder', ann='', command='world_click_position("R_Shoulder")', bgc=required_joints_colour)
    cmds.button(label='L_Elbow', ann='', command='world_click_position("L_Elbow")', bgc=required_joints_colour)
    cmds.button(label='R_Elbow', ann='', command='world_click_position("R_Elbow")', bgc=required_joints_colour)
    cmds.button(label='L_Wrist', ann='', command='world_click_position("L_Wrist")', bgc=required_joints_colour)
    cmds.button(label='R_Wrist', ann='', command='world_click_position("R_Wrist")', bgc=required_joints_colour)
    cmds.setParent('..')

    # creates the layout for the Fingers buttons
    cmds.rowColumnLayout("fingers_buttons", numberOfColumns=7)
    finger_joints = ['Index', 'Middle', 'Ring', 'Pinky', 'Thumb']
    for finger_joint in finger_joints:
        for hand in ['L', 'R']:
            for idx in range(1, 4):
                label = hand + "_" + finger_joint + str(idx)
                command = 'world_click_position("{}")'.format(label)
                data = {
                    'label': label,
                    'ann': '',
                    'command': command
                }
                cmds.button(**data)
            data = {
                'label': '',
                'w': 20,
                'en': False
            }
            if hand == 'L':
                cmds.button(**data)
    cmds.setParent('..')

    cmds.frameLayout(label='Hips/Chest/Head', labelAlign='top')
    cmds.rowColumnLayout("NurbsColours", numberOfColumns=1)
    cmds.button(label='Head', ann='', command='woood grld_click_position("Head")', bgc=required_joints_colour)
    cmds.button(label='Neck', ann='', command='world_click_position("Neck")', bgc=required_joints_colour)
    cmds.button(label='Chest', ann='', command='world_click_position("Chest")', bgc=required_joints_colour)
    cmds.button(label='Hips', ann='', command='world_click_position("Hips")', bgc=required_joints_colour)
    cmds.setParent('..')

    cmds.frameLayout(label='Legs', labelAlign='top')
    cmds.rowColumnLayout("NurbsColours", numberOfColumns=2)
    cmds.button(label='L_Leg', ann='', command='world_click_position("L_Leg")', bgc=required_joints_colour)
    cmds.button(label='R_Leg', ann='', command='world_click_position("R_Leg")', bgc=required_joints_colour)
    cmds.button(label='L_Knee', ann='', command='world_click_position("L_Knee")', bgc=required_joints_colour)
    cmds.button(label='R_Knee', ann='', command='world_click_position("R_Knee")', bgc=required_joints_colour)
    cmds.button(label='L_Ankle', ann='', command='world_click_position("L_Ankle")', bgc=required_joints_colour)
    cmds.button(label='R_Ankle', ann='', command='world_click_position("R_Ankle")', bgc=required_joints_colour)
    cmds.setParent('..')

    cmds.frameLayout(label='Build Options', labelAlign='top')
    cmds.checkBox(label='Smooth twist limbs', ed=False)
    cmds.checkBox('centreMidJoints', label='Centre mid joints', v=1, onc='centre_mid_joints=1', ofc='centre_mid_joints=0')
    centre_mid_joints = cmds.checkBox('centreMidJoints', q=True, v=True)

    cmds.button(label='B U I L D    R I G', bgc=(.8, .3, .3), command='build_rig()')

    cmds.showWindow()

create_window()
