import maya.cmds as cmds
import maya.mel as mm

mesh = cmds.ls(sl=True)[0]
dup_mesh = cmds.duplicate(mesh)
mesh_parent = cmds.listRelatives(p=1, f=1)

all_nodes = cmds.ls()
mm.eval('doCreateNCloth 0')
new_nodes = cmds.ls()
diff = list(set(new_nodes)-set(all_nodes))

# Rename initial mesh to have suffix _inMesh and output mesh with _outMesh
cmds.rename(mesh, mesh+"_inMesh")
cmds.rename(dup_mesh[0], mesh+"_outMesh")

# Sets the inMesh shape as the inputMesh for the nCloth node
cmds.listConnections(diff[1]+".inputMesh", s=True)
cmds.connectAttr(mesh+"_inMeshShape.worldMesh", diff[1]+".inputMesh", f=True)

# Renames the nCloth node to the mesh name + _nCloth
nCloth = cmds.rename(diff[1], mesh+"_nCloth")

# groups the nCloth node, inMesh, and outMesh, and parents them where the inMesh was before
cmds.group(mesh+"_nCloth", mesh+"_inMesh", mesh+"_outMesh", n=mesh)
cmds.parent(mesh, mesh_parent)
# hides the initial mesh
cmds.hide(mesh+"_inMesh")