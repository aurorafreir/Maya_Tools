import sys

sys.path.append(r"C:\Users\aurora\PycharmProjects\Maya_Scripts/")


import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import os

# scene
from SceneSetup import scene_setup
from ReloadAsReference import reload_as_reference

# rigging
from GetUndeformedMesh import get_undeformed_mesh
from CreateJointControllers import create_joint_controllers
from SetEndJointOrient import end_joint_orient

import CreateNurbsShapes

    ctrl = cmds.ls(sl=True)
def SetNurbsColorRed(self):
    for i in ctrl:
        cmds.setAttr(i + ".overrideEnabled", 1)
        cmds.setAttr(i + ".overrideColor", 13)

def SetNurbsColorYellow(self):
    ctrl = cmds.ls(sl=True)
    for i in ctrl:
        cmds.setAttr(i + ".overrideEnabled", 1)
        cmds.setAttr(i + ".overrideColor", 17)

def SetNurbsColorBlue(self):
    ctrl = cmds.ls(sl=True)
    for i in ctrl:
        cmds.setAttr(i + ".overrideEnabled", 1)
        cmds.setAttr(i + ".overrideColor", 18)


# RENDERING
from SetOCIOOnOff import ocio_toggle
from SingleFramePlayblast import single_frame_playblast


def AurTDEndFrameRange(self):
    endFrame = cmds.playbackOptions(q=True, maxTime=1)
    cmds.setAttr('defaultRenderGlobals.endFrame', endFrame)
    print ("set Render Range end frame to " + str(endFrame))


# MODELLING
def AurTDSafeDelHistory(self):
    tempSel_SafeDelHistory = cmds.ls(sl=True)
    cmds.bakePartialHistory(tempSel_SafeDelHistory, prePostDeformers=True)

# CAMERAS
def AurTDOverscan(self):
    view = OpenMayaUI.M3dView.active3dView()
    cam = OpenMaya.MDagPath()
    view.getCamera(cam)
    camPath = cam.fullPathName()
    # if cmds.camera(camPath, q=True, displayResolution=1):
    cmds.camera(camPath, e=True, overscan=1.05)
    print ("set current camera's overscan to 1.05")


# CREATE WINDOW
def create_window(self):

    winID = 'aurWindow'

    hv = 25
    wv = 100

    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)

    cmds.window(winID, title='Control Panel')
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, width=200)

    cmds.frameLayout(label='Scene/Layout', labelAlign='top')
    cmds.button(label='Scene Setup', ann='Set up scene groups with Outliner colours', command=scene_setup())
    cmds.button(label='Reload as Reference', ann='', command=reload_as_reference())

    cmds.frameLayout(label='Rigging', labelAlign='top')
    cmds.button(label='Original Blendshape', ann='Get the original shape without blendshapes or joint deformation',
                command=get_undeformed_mesh())
    cmds.button(label='Joint Controllers _BROKEN_', ann='Make a controller for each selected joint',
                command=create_joint_controllers(), bgc=[.5, .5, .6])
    cmds.button(label='End Joint Orient', ann='Orient the end joint of each chain correctly', command=end_joint_orient())

    cmds.frameLayout(label='Controls', labelAlign='top')
    cmds.button(label='Nurbs Circle', ann='Makes a NURBS circle', command=CreateNurbsShapes.create_nurbs_circle())
    cmds.button(label='Nurbs Cube', ann='Makes a NURBS cube', command=CreateNurbsShapes.create_nurbs_cube())
    cmds.button(label='Nurbs Pyramid', ann='Makes a NURBS cube', command=CreateNurbsShapes.create_nurbs_pyramid())
    cmds.rowColumnLayout("NurbsColours", numberOfColumns=3, h=20)
    cmds.button(label='Red', ann='Set NURBS curve to Red', command=SetNurbsColorRed, bgc=[.8,0.3,0.3])
    cmds.button(label='Yellow', ann='Set NURBS curve to Yellow', command=SetNurbsColorYellow, bgc=[.8,.8,.3])
    cmds.button(label='Blue', ann='Set NURBS curve to Blue', command=SetNurbsColorBlue, bgc=[.3,.6,.8])
    cmds.setParent('..')


    cmds.frameLayout(label='Rendering', labelAlign='top')
    cmds.button('OCIO_Toggle', label='OCIO Toggle', h=hv, w=wv, ann='Toggle OCIO colour management',
                command=ocio_toggle())

    cmds.button(label='Set Frame End same as Timeline',
                ann='Set the End Frame for rendering to the End Frame of the timeline', command=AurTDEndFrameRange)

    cmds.frameLayout(label='Modelling', labelAlign='top')
    cmds.button(label='Delete non-deformer history', ann='Delete non-deformer history', command=AurTDSafeDelHistory)

    cmds.frameLayout(label='Cameras', labelAlign='top')
    cmds.button(label='Overscan to 1.05', ann="Set current camera's Overscan to 1.05", command=AurTDOverscan)
    cmds.button(label='Playblast single frame', ann="Playblasts a single frame as a jpg at the render resolution",
                command=SingleFramePlayblast.single_frame_playblast())

    cmds.rowColumnLayout("uiMenuRow", adjustableColumn=True)

    # OCIO Toggle color and name set on open
    if cmds.colorManagementPrefs(q=True, cfe=True):
        cmds.button('OCIO_Toggle', e=True, label='OCIO Off', bgc=[.8, .5, .5])
    else:
        cmds.button('OCIO_Toggle', e=True, label='OCIO On', bgc=[.5, .7, .5])

    cmds.showWindow()
