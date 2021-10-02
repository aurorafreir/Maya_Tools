"""
Script used for creating a selection of NURBS curves shapes
"""

# Standard library imports


# Third party imports
from maya import cmds

# Local application imports


def nurbs_surf_setup(curve_name=""):
    curve_name_short = curve_name.split("_")[0]
    curve_group = cmds.group(empty=True, name='{}_GRP'.format(curve_name_short))
    cmds.parent(curve_name, curve_group)
    cmds.rename(curve_name, '{}#'.format(curve_name))
    cmds.select(curve_group)
    cmds.rename(curve_group, "{}#".format(curve_group))

def create_nurbs_circle():
    curve = cmds.circle(name='Circle_CTRL')[0]
    cmds.bakePartialHistory(curve)
    nurbs_surf_setup(curve_name=curve)


def create_nurbs_cube():
    curve = cmds.curve(d=1, p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5), (.5, -0.5, -0.5), (.5, .5, -0.5),
                       (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (.5, -0.5, -0.5), (.5, .5, -0.5), (.5, .5, .5),
                       (-0.5, .5, .5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5), (.5, -0.5, .5)],
               n='Cube_CTRL')
    nurbs_surf_setup(curve_name=curve)


def create_nurbs_pyramid():
    curve = cmds.curve(d=1, p=[(-.5, -1, -.5), (.5, -1, -.5), (.5, -1, .5), (-.5, -1, .5), (-.5, -1, -.5), (0, 0, 0),
                       (-.5, -1, .5), (.5, -1, .5), (0, 0, 0), (.5, -1 ,-.5)],
               n='Pyramid_CTRL')
    nurbs_surf_setup(curve_name=curve)
     
