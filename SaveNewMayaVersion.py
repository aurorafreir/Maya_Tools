import maya.cmds as cmds
import os
# set current python directory to project dir
CurrentProj = cmds.workspace(active=True, q=True)
os.chdir("{}".format(CurrentProj))
# get current scene name
filepath = cmds.file(q=True, sn=True)
filename = os.path.basename(filepath)
# get new scene name
SceneName = filename[:-7]
VersionNumber = int(filename.split("_v")[1][:-3])
newVersion = SceneName + "_v" + str(VersionNumber+1).zfill(2) + ".ma"
print newVersion
# save the new file
cmds.file(rename=newVersion)
cmds.file(save=True, force=True)
