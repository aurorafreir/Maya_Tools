import maya.cmds as cmds

SelectedObj = cmds.ls(sl=True, sn=True)

if SelectedObj:
    cmds.duplicate(n="{}Blendshape".format(SelectedObj[0]))
    cmds.setAttr("{}BlendshapeShapeOrig.intermediateObject".format(SelectedObj[0]), 0)
    cmds.delete("{}BlendshapeShape".format(SelectedObj[0]))

#TODO reapply material

#TODO unlock translate attrs

#axis = ['X', 'Y', 'Z']
#attrs = ['t', 'r', 's']
#for ax in axis:
#    for attr in attrs:
#       cmds.setAttr("Blendshape"+'.'+attr+ax, lock=0)
