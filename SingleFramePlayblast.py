import maya.cmds as cmds

#gets current frame
CurrentFrame = cmds.currentTime(q=True)
#gets current render format, and sets image format to jpg
CurrentImageFormat = cmds.getAttr("defaultRenderGlobals.imageFormat")
cmds.setAttr("defaultRenderGlobals.imageFormat", 8) # *.jpg
#gets current render resolution
RenderWidth = cmds.getAttr("defaultResolution.width")
RenderHeight= cmds.getAttr("defaultResolution.height")
#starts playblast for current frame, as jpeg, at render resolution, without ornaments
cmds.playblast(frame=CurrentFrame, format="image", p=100, width=RenderWidth, height=RenderHeight, qlt=95, orn=False)
#sets render format back to previous
cmds.setAttr("defaultRenderGlobals.imageFormat", CurrentImageFormat)
