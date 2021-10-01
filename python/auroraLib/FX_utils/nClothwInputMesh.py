"""
Script to make an nCloth mash out of the current object, with the original as an in mesh,
and the new as the out (simulated) mesh
"""

# Standard library imports

# Third party imports
from maya import cmds
from maya import mel

# Local application imports



def nClothwInputMesh():
    mesh = cmds.ls(selection=True)[0]
    dup_mesh = cmds.duplicate(mesh)
    mesh_parent = cmds.listRelatives(parent=True, fullPath=True)

    all_nodes = cmds.ls()
    mel.eval('doCreateNCloth 0')
    new_nodes = cmds.ls()
    diff = list(set(new_nodes)-set(all_nodes))

    # Rename initial mesh to have suffix _inMesh and output mesh with _outMesh
    cmds.rename(mesh, "{}_inMesh".format(mesh))
    cmds.rename(dup_mesh[0], "{}_outMesh".format(mesh))

    # Sets the inMesh shape as the inputMesh for the nCloth node
    cmds.listConnections("{}.inputMesh".format(diff[1]), shapes=True)
    cmds.connectAttr("{}_inMeshShape.worldMesh".format(mesh), "{}.inputMesh".format(diff[1]), force=True)

    # Renames the nCloth node to the mesh name + _nCloth
    nCloth = cmds.rename(diff[1], "{}_nCloth".format(mesh))

    # groups the nCloth node, inMesh, and outMesh, and parents them where the inMesh was before
    cmds.group("{}_nCloth".format(mesh), "{}_inMesh".format(mesh), "{}_outMesh".format(mesh), name=mesh)
    cmds.parent(mesh, mesh_parent)
    # hides the initial mesh
    cmds.hide("{}_inMesh".format(mesh))

nClothwInputMesh()
