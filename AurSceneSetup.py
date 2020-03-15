import maya.cmds as cmds

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
cmds.setAttr('_CAMS_.outlinerColor', .5,.6,.8)
