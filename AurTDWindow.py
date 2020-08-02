import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import os
from shutil import move

winID = 'aurWindow'


# SCENE
def AurTDSceneSetup(self):
    if not cmds.ls("_GEO_"):
        cmds.group(em=True, n="_GEO_")
    if not cmds.ls("_LGT_"):
        cmds.group(em=True, n="_LGT_")
    if not cmds.ls("_REFS_"):
        cmds.group(em=True, n="_REFS_")
    if not cmds.ls("_CAMS_"):
        cmds.group(em=True, n="_CAMS_")


    cmds.setAttr('_GEO_.useOutlinerColor', True)
    cmds.setAttr('_GEO_.outlinerColor', .1,.7,.7)
    cmds.setAttr('_LGT_.useOutlinerColor', True)
    cmds.setAttr('_LGT_.outlinerColor', .8,.8,.2)
    cmds.setAttr('_REFS_.useOutlinerColor', True)
    cmds.setAttr('_REFS_.outlinerColor', .5,.6,.8)
    cmds.setAttr('_CAMS_.useOutlinerColor', True)
    cmds.setAttr('_CAMS_.outlinerColor', .6,.8,.4)



def AurTDSceneSetupPY(self):
    import AurSceneSetup

def AurReloadAsReference(self):
    CurrentProj = cmds.workspace(active=True, q=True)
    os.chdir("{}".format(CurrentProj))

    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)

    if cmds.ls(sl=True):
        SelectedObjs = cmds.ls(sl=True)[0]
        cmds.file(rename=SelectedObjs)
        cmds.file(save=True)
        cmds.file(rename=filename)

        move(
            "{}/scenes/{}.ma".format(CurrentProj, SelectedObjs),
            "{}/assets/{}.ma".format(CurrentProj, SelectedObjs))

        cmds.file("{}/assets/{}.ma".format(CurrentProj, SelectedObjs), reference=True)
        cmds.delete(SelectedObjs)


# RIGGING
def AurTDBlendshapeOriginal(self):
    SelectedObj = cmds.ls(sl=True, sn=True)

    if SelectedObj:
        # get material
        SelectedObj = cmds.ls(sl=True, dag=True, s=True)
        shadeEng = cmds.listConnections(SelectedObj, type="shadingEngine")
        SelectedObjMaterial = cmds.ls(cmds.listConnections(shadeEng), materials=True)
        print SelectedObjMaterial[0]
        # duplicate object and switch it to original shape node
        cmds.duplicate(n="{}Blendshape".format(SelectedObj[0]))
        cmds.setAttr("{}BlendshapeShapeOrig.intermediateObject".format(SelectedObj[0]), 0)
        cmds.delete("{}BlendshapeShape".format(SelectedObj[0]))
        # assign material
        cmds.select('{}Blendshape'.format(SelectedObj[0]))
        cmds.select(SelectedObjMaterial[0], add=True)
        SelectedObjShaderGroup = cmds.listConnections(SelectedObjMaterial[0])
        print SelectedObjShaderGroup[0]
        cmds.hyperShade(assign='aiStandardSurface1SG')
        # unlock translate attrs
        axis = ['X', 'Y', 'Z']
        attrs = ['translate', 'rotate', 'scale']
        for ax in axis:
            for attr in attrs:
                cmds.setAttr('{}Blendshape'.format(SelectedObj[0]) + '.' + attr + ax, lock=0)


def AurTDJointController(self):
    # Makes a square NURBS controller and parent constraints the joints to the controllers
    # Makes an array of the selected joints
    tempSel_jointArray = cmds.ls(type=('joint'), sl=True)

    for i in tempSel_jointArray:
        # Selects current joint and sets it as variable tempSel_Parent
        cmds.select(i)
        tempSel_parent = cmds.ls(sl=True)

        # Selects child joint and sets it as variable tempSel_AimAt
        tempSel_aimAt = cmds.listRelatives(type='joint')

        # Creates square NURBS curve and deletes it's history
        cmds.select(d=True);
        cmds.curve(d=1, p=[(-0.5, 0, .5), (-0.5, 0, -.5), (.5, 0, -.5), (.5, 0, .5), (-0.5, 0, .5)], name='CTRL_' + i);
        cmds.rotate(0, 0, 90);
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        cmds.bakePartialHistory()

        # Makes a group and makes the controller a child of the PIVOT group
        cmds.group(em=True, name='PIVOT_' + (i));
        cmds.parent('CTRL_' + (i), 'PIVOT_' + (i));

        # TODO try point constraint
        # Makes parent constraint for controller location
        cmds.parentConstraint(tempSel_parent, 'PIVOT_' + i, mo=False, name='tempParentConstraint' + i);
        cmds.delete('tempParentConstraint' + (i));

        # Makes aim constraint for controller orientation
        cmds.aimConstraint(tempSel_aimAt, 'PIVOT_' + i, name='tempAimConstraint' + i);
        cmds.delete('tempAimConstraint' + (i));

        # Parent constrains the joint to the controller
        cmds.select('CTRL_' + i)
        cmds.select((i), add=True)
        cmds.parentConstraint(name='parentConstraint_' + (i) + '_CTRL_' + i)
        cmds.select(d=True)


def AurTDEndJointOrient(self):
    tempSel_jointArray = cmds.ls(type=('joint'), sl=True)

    for i in tempSel_jointArray:

        cmds.select(i)
        tempSel_parent = cmds.ls(sl=True)

        tempSel_child = cmds.listRelatives(type='joint')

        if not tempSel_child:
            cmds.joint(edit=True, o=(0, 0, 0));


# CONTROLS
def AurTDnurbsCircle(self):
    cmds.group(em=True, n='PIVOT_Circle')
    cmds.circle(name='CTRL_Circle')
    cmds.parent('CTRL_Circle', 'PIVOT_Circle')
    cmds.bakePartialHistory()
    cmds.select('PIVOT_Circle')

def AurTDnurbsCube(self):
    cmds.group(em=True, n='PIVOT_Cube')
    cmds.curve(d=1, p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5), (.5, -0.5, -0.5), (.5, .5, -0.5),
                       (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (.5, -0.5, -0.5), (.5, .5, -0.5), (.5, .5, .5),
                       (-0.5, .5, .5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5), (.5, -0.5, .5)],
               n='CTRL_Cube');
    cmds.parent('CTRL_Cube', 'PIVOT_Cube')
    cmds.rename('CTRL_Cube', 'CTRL_Cube#')
    cmds.select('PIVOT_Cube')
    cmds.rename('PIVOT_Cube', 'PIVOT_Cube#')


def AurTDnurbsPyramid(self):
    cmds.group(em=True, n='PIVOT_Pyramid')
    cmds.curve(d=1, p=[(-.5, -1, -.5), (.5, -1, -.5), (.5, -1, .5), (-.5, -1, .5), (-.5, -1, -.5), (0, 0, 0),
                       (-.5, -1, .5), (.5, -1, .5), (0, 0, 0), (.5, -1 ,-.5)],
               n='CTRL_Pyramid');
    cmds.parent('CTRL_Pyramid', 'PIVOT_Pyramid')
    cmds.rename('CTRL_Pyramid', 'CTRL_Pyramid#')
    cmds.select('PIVOT_Pyramid')
    cmds.rename('PIVOT_Pyramid', 'PIVOT_Pyramid#')


def SetNurbsColorRed(self):
    ctrl = cmds.ls(sl=True)
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
def AurTDOCIOToggle(self):
    if cmds.colorManagementPrefs(q=True, cfe=True):
        cmds.colorManagementPrefs(e=True, cfe=False)
        cmds.button('OCIO_Toggle', e=True, label='OCIO Off', bgc=[.8, .5, .5])
    elif not cmds.colorManagementPrefs(q=True, cfe=True):
        cmds.colorManagementPrefs(e=True, cfe=True)
        cmds.button('OCIO_Toggle', e=True, label='OCIO On', bgc=[.5, .7, .5])


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


def AurTDSingleFramePlayblast(self):
    #gets current frame
    CurrentFrame = cmds.currentTime(q=True)

    #gets current render format, and sets image format to jpg
    CurrentImageFormat = cmds.getAttr("defaultRenderGlobals.imageFormat")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 8) # *.jpg

    #gets current render resolution
    RenderWidth = cmds.getAttr("defaultResolution.width")
    RenderHeight= cmds.getAttr("defaultResolution.height")

    #get current camera name
    view = OpenMayaUI.M3dView.active3dView()
    cam = OpenMaya.MDagPath()
    view.getCamera(cam)
    camPath = cam.fullPathName()
    cmds.select(camPath)
    currentCamLong = cmds.ls(sl=True,long=False) or []
    cmds.select(currentCamLong[0])
    CurrentCam = cmds.listRelatives(parent=True)[0]
    print CurrentCam

    #check if film gate is on
    if cmds.camera(CurrentCam, dr=True, q=True):
        FilmGateOverscan = cmds.camera(CurrentCam, q=True, overscan=1)
        FilmGateOn = True
        cmds.camera(CurrentCam, dr=False, e=True)
        cmds.camera(CurrentCam, e=True, overscan=1.00)

    #check what vers was last
    CurrentVersCheck = 0
    while cmds.file("images/{}_v{}.jpg".format(CurrentCam, str(CurrentVersCheck).zfill(2)), exists=True, q=True):
        print CurrentVersCheck
        CurrentVersCheck+=1

        if not cmds.file("images/{}_v{}.jpg".format(CurrentCam, str(CurrentVersCheck).zfill(2)), exists=True, q=True):
            break

    #starts playblast for current frame, as jpeg, at render resolution, without ornaments
    cmds.playblast(
        frame=CurrentFrame,
        f="{}_v{}".format(CurrentCam, str(CurrentVersCheck).zfill(2)),
        fmt="image",
        p=100,
        width=RenderWidth,
        height=RenderHeight,
        qlt=95,
        orn=False)
    #sets render format back to previous
    cmds.setAttr("defaultRenderGlobals.imageFormat", CurrentImageFormat)

    #rename file to remove ".0000"
    CurrentProj = cmds.workspace(active=True, q=True)
    os.chdir("{}".format(CurrentProj))
    os.rename(
        "images/{}_v{}".format(CurrentCam, str(CurrentVersCheck).zfill(2)) + ".0000.jpg",
        "images/{}_v{}".format(CurrentCam, str(CurrentVersCheck).zfill(2)) + ".jpg")

# CREATE WINDOW
# def main():
hv = 25
wv = 100

if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

cmds.window(winID, title='Control Panel')
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, width=200)

cmds.frameLayout(label='Scene/Layout', labelAlign='top')
cmds.button(label='Scene Setup', ann='Set up scene groups with Outliner colours', command=AurTDSceneSetup)
cmds.button(label='Scene Setup PY _BROKEN_', ann='Set up scene groups with Outliner colours', command=AurTDSceneSetupPY,
            bgc=[.5, .5, .6])
cmds.button(label='Reload as Reference', ann='', command=AurReloadAsReference)

cmds.frameLayout(label='Rigging', labelAlign='top')
cmds.button(label='Original Blendshape', ann='Get the original shape without blendshapes or joint deformation',
            command=AurTDBlendshapeOriginal)
cmds.button(label='Joint Controllers _BROKEN_', ann='Make a controller for each selected joint',
            command=AurTDJointController, bgc=[.5, .5, .6])
cmds.button(label='End Joint Orient', ann='Orient the end joint of each chain correctly', command=AurTDEndJointOrient)

cmds.frameLayout(label='Controls', labelAlign='top')
cmds.button(label='Nurbs Circle', ann='Makes a NURBS circle', command=AurTDnurbsCircle)
cmds.button(label='Nurbs Cube', ann='Makes a NURBS cube', command=AurTDnurbsCube)
cmds.button(label='Nurbs Pyramid', ann='Makes a NURBS cube', command=AurTDnurbsPyramid)
cmds.rowColumnLayout("NurbsColours", numberOfColumns=3, h=20)
cmds.button(label='Red', ann='Set NURBS curve to Red', command=SetNurbsColorRed, bgc=[.8,0.3,0.3])
cmds.button(label='Yellow', ann='Set NURBS curve to Yellow', command=SetNurbsColorYellow, bgc=[.8,.8,.3])
cmds.button(label='Blue', ann='Set NURBS curve to Blue', command=SetNurbsColorBlue, bgc=[.3,.6,.8])
cmds.setParent('..')


cmds.frameLayout(label='Rendering', labelAlign='top')
cmds.button('OCIO_Toggle', label='OCIO Toggle', h=hv, w=wv, ann='Toggle OCIO colour management',
            command=AurTDOCIOToggle)

cmds.button(label='Set Frame End same as Timeline',
            ann='Set the End Frame for rendering to the End Frame of the timeline', command=AurTDEndFrameRange)

cmds.frameLayout(label='Modelling', labelAlign='top')
cmds.button(label='Delete non-deformer history', ann='Delete non-deformer history', command=AurTDSafeDelHistory)

cmds.frameLayout(label='Cameras', labelAlign='top')
cmds.button(label='Overscan to 1.05', ann="Set current camera's Overscan to 1.05", command=AurTDOverscan)
cmds.button(label='Playblast single frame', ann="Playblasts a single frame as a jpg at the render resolution",
            command=AurTDSingleFramePlayblast)

cmds.rowColumnLayout("uiMenuRow", adjustableColumn=True)

# OCIO Toggle color and name set on open
if cmds.colorManagementPrefs(q=True, cfe=True):
    cmds.button('OCIO_Toggle', e=True, label='OCIO Off', bgc=[.8, .5, .5])
elif not cmds.colorManagementPrefs(q=True, cfe=True):
    cmds.button('OCIO_Toggle', e=True, label='OCIO On', bgc=[.5, .7, .5])

cmds.showWindow()
