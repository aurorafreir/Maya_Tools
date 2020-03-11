import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

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
CurrentCam = str(currentCamLong[0])[:-5]


#TODO check if film gate is on

#TODO check what vers was last
CurrentVersCheck = 100
while CurrentVersCheck > 0:
    CurrentVersCheck-=1
#    print CurrentVersCheck
    if cmds.file("images/{}_v{}.jpg".format(CurrentCam, str(CurrentVersCheck).zfill(2)), exists=True, q=True):
        file = "images/{}_v{}.jpg".format(CurrentCam, str(CurrentVersCheck).zfill(2))
        print file
        break
CurrentVers = CurrentVersCheck + 1
print CurrentVers

#starts playblast for current frame, as jpeg, at render resolution, without ornaments
cmds.playblast(frame=CurrentFrame, f="{}_v{}".format(CurrentCam, str(CurrentVers).zfill(2)), fmt="image", p=100, width=RenderWidth, height=RenderHeight, qlt=95, orn=False)
#sets render format back to previous
cmds.setAttr("defaultRenderGlobals.imageFormat", CurrentImageFormat)
