"""
Script to print out a dictionary that can be used in other scripts to
create the same nurbs curves through the cmds.curve function
"""

# Standard library imports


# Third party imports
from maya import cmds

# Local application imports



def shape_grabber():
    if not cmds.ls(selection=True):
        raise Exception("Nothing Selected!")
    
    shapes = {  }
    selected = cmds.ls(selection=True)
    try:
        for shape in cmds.listRelatives(selected, children=True):
            shapecvs = []
            for x in range(cmds.getAttr('{}.cp'.format(shape), size=True)):
                ppos = cmds.pointPosition("{}.cp[{}]".format(shape, x), local=True)
                shapecvs.append(ppos)
            shapes[shape] = shapecvs
    except TypeError:
        raise Exception("More than one object with the name of the currently selected object")

    newcurves = []
    
    if len(selected) == 0:
        crvname = selected
    else:
        crvname = selected[0]
    
    print("---- Start selection from next row ----")
    print(crvname + " = {")
    for shape, point_data in shapes.items():
        print("'{}':{},".format(shape, point_data))
    print("}")
    print("---- End selection from previous row ----")


# Usage in scripts:
"""
created_dictionary = {

}

newcurves = []
for i, x in created_dictionary.items():
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