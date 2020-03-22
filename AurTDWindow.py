import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import os

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
    # TODO update to add Pivot group hierarchy
    cmds.circle(name='CircleNURB_#')
    cmds.bakePartialHistory()


def AurTDnurbsCube(self):
    cmds.group(em=True, n='PIVOT_Cube')
    cmds.curve(d=1, p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5), (.5, -0.5, -0.5), (.5, .5, -0.5),
                       (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (.5, -0.5, -0.5), (.5, .5, -0.5), (.5, .5, .5),
                       (-0.5, .5, .5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5), (.5, -0.5, .5)],
               n='CTRL_Cube');
    cmds.parent('CTRL_Cube', 'PIVOT_Cube')
    # cmds.select('CTRL_Cube')
    cmds.rename('CTRL_Cube', 'CTRL_Cube#')
    cmds.rename('PIVOT_Cube', 'PIVOT_Cube#')


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


def AurTDString(self):
    selected = cmds.ls(selection=True)

    selected_len = (len(selected))
    # print selected_len

    if len(selected) == 2:
        # todo add check for frozen translations
        for item in selected[:1]:
            rPiv = cmds.xform(item, q=True, rp=True)  # query rotation pivot
            # sPiv = cmds.xform(item, q=True, sp=True)  # query scale pivot

            loc = cmds.spaceLocator(n="wireLocator1")
            cmds.xform(t=rPiv)

        for item in selected[1:]:
            rPiv = cmds.xform(item, q=True, rp=True)  # query rotation pivot
            # sPiv = cmds.xform(item, q=True, sp=True)  # query scale pivot

            loc = cmds.spaceLocator(n="wireLocator2")
            cmds.xform(t=rPiv)

    else:
        print "Two objects required for string"

    # cmds.curve('string_##',)

    # cmds.delete("wireLocator1")
    # cmds.delete("wireLocator2")

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

    #turn film gate back on if it was on
    if FilmGateOn:
        cmds.camera(CurrentCam, dr=True, e=True)
        cmds.camera(CurrentCam, e=True, overscan=FilmGateOverscan)


# CREATE WINDOW
# def main():
hv = 25
wv = 100

if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

cmds.window(winID, title='Aur TD Window')
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, width=200)

cmds.frameLayout(label='Scene', labelAlign='top')
cmds.button(label='Scene Setup', ann='Set up scene groups with Outliner colours', command=AurTDSceneSetup)
cmds.button(label='Scene Setup PY _BROKEN_', ann='Set up scene groups with Outliner colours', command=AurTDSceneSetupPY,
            bgc=[.5, .5, .6])

cmds.frameLayout(label='Rigging', labelAlign='top')
cmds.button(label='Original Blendshape', ann='Get the original shape without blendshapes or joint deformation',
            command=AurTDBlendshapeOriginal)
cmds.button(label='Joint Controllers _BROKEN_', ann='Make a controller for each selected joint',
            command=AurTDJointController, bgc=[.5, .5, .6])
cmds.button(label='End Joint Orient', ann='Orient the end joint of each chain correctly', command=AurTDEndJointOrient)

cmds.frameLayout(label='Controls', labelAlign='top')
cmds.button(label='Nurbs Circle', ann='Makes a NURBS circle', command=AurTDnurbsCircle)
cmds.button(label='Nurbs Cube', ann='Makes a NURBS cube', command=AurTDnurbsCube)

cmds.frameLayout(label='Rendering', labelAlign='top')
cmds.button('OCIO_Toggle', label='OCIO Toggle', h=hv, w=wv, ann='Toggle OCIO colour management',
            command=AurTDOCIOToggle)

cmds.button(label='Set Frame End same as Timeline',
            ann='Set the End Frame for rendering to the End Frame of the timeline', command=AurTDEndFrameRange)

cmds.frameLayout(label='Modelling', labelAlign='top')
cmds.button(label='Delete non-deformer history', ann='Delete non-deformer history', command=AurTDSafeDelHistory)
cmds.button(label='String _WIP_', ann='Make string between two selected objects', command=AurTDString, bgc=[.5, .5, .6])

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
