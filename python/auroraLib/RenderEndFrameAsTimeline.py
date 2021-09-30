import maya.cmds as cmds
EndFrame = cmds.playbackOptions(q=True, maxTime=1)
cmds.setAttr('defaultRenderGlobals.endFrame', EndFrame)
print ("set Render Range end frame to " + str(EndFrame))
