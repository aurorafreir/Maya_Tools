import maya.cmds as cmds


def shape_grabber():
    if not cmds.ls(sl=1):
        raise Exception("Nothing Selected!")
        return
    
    shapes = {  }
    selected = cmds.ls(sl=1)
    
    for i in cmds.listRelatives(cmds.ls(sl=1), c=1):
        shapecvs = []
        for x in range(cmds.getAttr(i + '.cp', s=1)):
            ppos = cmds.pointPosition(i + ".cp[{}]".format(x), l=1)
            shapecvs.append(ppos)
        shapes[i] = shapecvs
            
    newcurves = []
    
    if len(selected) == 0:
        crvname = selected
    else:
        crvname = selected[0]
    
    print("---- Start selection from next row ----")
    print(crvname + " = {")
    for i, x in shapes.items():
        print("'{}':{},".format(i, x))
    print("}")
    print("---- End selection from previous row ----")

                
shape_grabber()

"""
Usage in scripts:

created_dictionary = {
    
}

newcurves = []
for i, x in NAME_OF_SELECTED_OBJECT.items():
    curve = cmds.curve(d=5, p=x)
    newcurves.append(curve)

for crv, num in zip(newcurves, range(len(newcurves))):
    if num == 0:
        parent = crv
    else:
        cmds.parent(cmds.listRelatives(crv), parent, r=1, s=1)
        cmds.delete(crv)
cmds.rename(parent, "NewCurve")

"""