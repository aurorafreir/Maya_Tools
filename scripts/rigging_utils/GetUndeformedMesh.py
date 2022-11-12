"""
Script get the mesh of an object, before any skinCluster or deformers
Essentially just grabs the bind "_Orig" version of the mesh
"""

# Standard library imports

# Third party imports
from maya import cmds

# Local application imports



def get_undeformed_mesh():
    selected_obj = cmds.ls(selection=True, shortNames=True)

    if selected_obj:
    # get material
        selected_obj = cmds.ls(selection=True, dag=True, shape=True)[0]
        shade_eng = cmds.listConnections(selected_obj , type="shadingEngine")
        selected_obj_material = cmds.ls(cmds.listConnections(shade_eng), materials=True)
        print(selected_obj_material[0])
    # duplicate object and switch it to original shape node
        cmds.duplicate(name="{}Blendshape".format(selected_obj))
        cmds.setAttr("{}BlendshapeShapeOrig.intermediateObject".format(selected_obj), 0)
        cmds.delete("{}BlendshapeShape".format(selected_obj))
    # assign material
        cmds.select('{}Blendshape'.format(selected_obj[0]))
        cmds.select(selected_obj_material[0], add=True)
        selected_obj_shadergroup = cmds.listConnections(selected_obj_material[0])
        print(selected_obj_shadergroup[0])
        cmds.hyperShade( assign='aiStandardSurface1SG')
    # unlock translate attrs
        axis = ['X', 'Y', 'Z']
        attrs = ['translate', 'rotate', 'scale']
        for ax in axis:
            for attr in attrs:
               cmds.setAttr('{}Blendshape.{}{}'.format(selected_obj, attr, ax), lock=True)
    else:
        print("Nothing selected!")