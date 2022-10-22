"""
Script to create a locator on each of the selected items (objects or components)
"""

# Standard library imports


# Third party imports
from maya import cmds

# Local application imports



def lerp(min, max, percent):  # linear_interpolate
    # Return float between min and max based on the percent (0-1)
    return ((max - min) * percent) + min


def vector_lerp(min, max, percent):  # vector_linear_interpolate
    # Get a 3 axis point between min (x,y,z) and max (x,y,z) based on the percent (0-1), and return (x,y,z)
    x = lerp(min[0], max[0], percent)
    y = lerp(min[1], max[1], percent)
    z = lerp(min[2], max[2], percent)

    return x, y, z

def LocatorOnSelected():
    selected = cmds.ls(selection=True)

    if selected:
        for item in selected:
            min = cmds.xform(item, absolute=True, worldSpace=True, query=True, boundingBox=True)[0:3]
            max = cmds.xform(item, absolute=True, worldSpace=True, query=True, boundingBox=True)[3:6]
            bboxmid = vector_lerp(min, max, 0.5)
            newloc = cmds.spaceLocator(name="new_loc#")
            cmds.xform(newloc, translate=bboxmid)
    else:
        raise Exception("Make sure to select objects or components!")

LocatorOnSelected()
