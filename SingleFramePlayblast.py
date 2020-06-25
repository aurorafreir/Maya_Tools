import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import os

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
