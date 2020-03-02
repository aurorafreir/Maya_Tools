import maya.cmds as cmds

SelectedObj = cmds.ls(sl=True, sn=True)

if SelectedObj:
    print SelectedObj
    cmds.duplicate(n="Blendshape")
    cmds.select("{}Orig".format(SelectedObj))

#axis = ['X', 'Y', 'Z']
#attrs = ['t', 'r', 's']
#for ax in axis:
    #for attr in attrs:
        #cmds.setAttr("Blendshape"+'.'+attr+ax, lock=0)