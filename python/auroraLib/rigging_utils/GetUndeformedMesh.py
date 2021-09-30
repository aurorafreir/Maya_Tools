"""
Script get the mesh of an object, 
"""

# Standard library imports

# Third party imports
from maya import cmds

# Local application imports



def get_undeformed_mesh():
    SelectedObj = cmds.ls(selection=True, sn=True)

    if SelectedObj:
    # get material
        SelectedObj = cmds.ls(selection=True, dag=True, shape=True)[0]
        shadeEng = cmds.listConnections(SelectedObj , type="shadingEngine")
        SelectedObjMaterial = cmds.ls(cmds.listConnections(shadeEng), materials=True)
        print SelectedObjMaterial[0]
    # duplicate object and switch it to original shape node
        cmds.duplicate(n="{}Blendshape".format(SelectedObj))
        cmds.setAttr("{}BlendshapeShapeOrig.intermediateObject".format(SelectedObj), 0)
        cmds.delete("{}BlendshapeShape".format(SelectedObj))
    # assign material
        cmds.select('{}Blendshape'.format(SelectedObj[0]))
        cmds.select(SelectedObjMaterial[0], add=True)
        SelectedObjShaderGroup = cmds.listConnections(SelectedObjMaterial[0])
        print SelectedObjShaderGroup[0]
        cmds.hyperShade( assign='aiStandardSurface1SG')
    # unlock translate attrs
        axis = ['X', 'Y', 'Z']
        attrs = ['translate', 'rotate', 'scale']
        for ax in axis:
            for attr in attrs:
               cmds.setAttr('{}Blendshape.{}{}'.format(SelectedObj, attr, ax), lock=0)

get_undeformed_mesh()