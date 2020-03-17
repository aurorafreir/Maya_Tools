import maya.cmds as cmds
import urllib
import os
import pymel.core as pmc

CurrentProj = cmds.workspace(active=True, q=True)
print CurrentProj
os.chdir("{}".format(CurrentProj))

urllib.urlretrieve("https://i.imgur.com/7lG8Jms.jpg", "assets/purewhite.jpg")

cmds.polyPlane(name="grid_Single", sx=1, sy=1)
#cmds.shadingNode("lambert", asShader=True)

#cmds.shadingNode("")

pmc.rendering.shadingNode("aiStandardSurface", asShader=True, name="grid_aiStandard")
pmc.rendering.shadingNode("file", asTexture=True, name="grid_file")
pmc.rendering.shadingNode("place2dTexture", asUtility=True, name="grid_place2dTex")
pmc.general.connectAttr("grid_place2dTex.outUV", "grid_file.uvCoord")
pmc.general.connectAttr("grid_file.outColor", "grid_aiStandard.baseColor")
pmc.general.setAttr("grid_aiStandard.base", 1)
pmc.general.setAttr("grid_file.fileTextureName", "assets/purewhite.jpg")
cmds.select("grid_Single")
cmds.hyperShade( assign="grid_aiStandard")