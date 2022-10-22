"""

"""
# SYSTEM IMPORTS

# STANDARD LIBRARY IMPORTS
import pymel.core as pm

# LOCAL APPLICATION IMPORTS


def proper_rivet(mesh_in: str, vtx: int, mesh_shape_in="", mesh_shape_orig_in="") -> [pm.nt.Transform, pm.nt.UvPin]:
    # im mad
    # normal cmds.Rivet() doesn't actually return the data it prints out, the uvPin and Rivet names.

    mesh_transform = pm.PyNode(mesh_in)

    if mesh_shape_in:
        mesh_shape = pm.PyNode(mesh_shape_in)  # Lets the user overwrite mesh_shape if wanted
    else:
        mesh_shape = mesh_transform.getShapes()[0]

    if mesh_shape_orig_in:
        mesh_shape_orig = pm.PyNode(mesh_shape_orig_in)  # Lets the user overwrite mesh_shape_orig if wanted
    else:
        # Check if orig shape exists, and if not, set the shape_orig to the first shape
        transform_shapes = mesh_transform.getShapes()
        does_orig_shape_exist = [i for i in transform_shapes if i.name().endswith("Orig")][0]
        if does_orig_shape_exist:
            mesh_shape_orig = does_orig_shape_exist
        else:
            mesh_shape_orig = mesh_shape

    temp_loc = pm.spaceLocator()

    ws_vert_loc = pm.pointPosition(f"{mesh_transform}.vtx[{vtx}]", world=True)

    temp_loc.t.set(ws_vert_loc)

    cpom_node = pm.createNode("closestPointOnMesh")
    temp_loc.t >> cpom_node.inPosition
    mesh_shape.outMesh >> cpom_node.inMesh

    u = cpom_node.parameterU.get()
    v = cpom_node.parameterV.get()

    pm.delete(temp_loc)
    pm.delete(cpom_node)

    rivet_loc = pm.spaceLocator()
    rivet_loc.rename(f"rivet_{vtx}_rvt")

    uv_pin_node = pm.createNode("uvPin")
    uv_pin_node.coordinate[0].coordinateU.set(u)
    uv_pin_node.coordinate[0].coordinateV.set(v)

    mesh_shape.outMesh >> uv_pin_node.deformedGeometry
    mesh_shape_orig.outMesh >> uv_pin_node.originalGeometry

    uv_pin_node.outputMatrix[0] >> rivet_loc.offsetParentMatrix

    return rivet_loc, uv_pin_node
