"""
Script used for exporting and importing all the controller animation in a scene
"""

# Standard library imports
import json
import os.path
import sys

# Third party imports
from maya import cmds

# Local application imports


### todo
# TODO optimize data export/import, e.g. if stepped them no need for oa, ox, oy


def export_anim():    
    # Get current project directory and scene name
    project_directory = cmds.workspace(query=True, rootDirectory=True)

    file_path = cmds.file(query=True, sceneName=True)
    file_name = os.path.basename(file_path)
    raw_name, extension = os.path.splitext(file_name)

    json_file = os.path.join(project_directory, "data", raw_name + "_Anim.json")

    # Gather all control curves in scene
    controls = []
    export_data = []

    for ctrl in cmds.ls(type="nurbsCurve"):
        ctrl_crv_parent = cmds.listRelatives(ctrl, parent=True)[0]
        
        # Make sure that duplicates don't get added to the controls list
        if ctrl_crv_parent in controls:
            continue
        controls.append(ctrl_crv_parent)

        for attr in cmds.listAttr(ctrl_crv_parent, keyable=True, unlocked=True):
            # Get all keyframe times, and keyframe values as their own lists
            # [[frame], [frame], [frame]]
            # [[value], [value], [value]]
            ctrl_attr = "{}.{}".format(ctrl_crv_parent, attr)
            

            key_times = cmds.keyframe(ctrl_attr, query=True, timeChange=True)
            key_values = cmds.keyframe(ctrl_attr, query=True, valueChange=True)

            in_tangents = cmds.keyTangent(ctrl_attr, query=True, inTangentType=True)
            out_tangents = cmds.keyTangent(ctrl_attr, query=True, outTangentType=True)
            in_angle = cmds.keyTangent(ctrl_attr, query=True, inAngle=True)
            out_angle = cmds.keyTangent(ctrl_attr, query=True, outAngle=True)
            in_tangents_x  = cmds.keyTangent(ctrl_attr, query=True, ix=True)
            in_tangents_y  = cmds.keyTangent(ctrl_attr, query=True, iy=True)
            out_tangents_x = cmds.keyTangent(ctrl_attr, query=True, ox=True)
            out_tangents_y = cmds.keyTangent(ctrl_attr, query=True, oy=True)

            if key_times and key_values:
                keytime_value = []
                
                for i in range(len(key_times)):
                    keytime_value.append({
                        "time": key_times[i],
                        "value": key_values[i],
                        "itt": in_tangents[i],
                        "ott": out_tangents[i],
                        "ia": in_angle[i],
                        "oa": out_angle[i],
                        "ix": in_tangents_x[i],
                        "iy": in_tangents_y[i],
                        "ox": out_tangents_x[i],
                        "oy": out_tangents_y[i]
                    })
                
                export_data.append({"{}.{}".format(ctrl_crv_parent, attr) : keytime_value})


    with open(json_file, "w") as out_file:
        json.dump(export_data, out_file)
    
    print("Exported correctly to: " + json_file)


def import_anim(name="", abs_path="", force=False):
    if not name:
        raise Exception("Must set the name of the file in the name arg!") 
    
    if abs_path:
        json_file = abs_path
    else:
        # Get current project directory and scene name
        project_directory = cmds.workspace(query=True, rootDirectory=True)
        json_file = os.path.join(project_directory, "data", name)


    if not os.path.isfile(json_file):
        raise OSError("File: {} - not found!".format(json_file))

    with open(json_file, "r") as in_file:
        data = json.load(in_file)

    for item in data:
        for ctrl_attr in item:
            ctrl = ctrl_attr.split(".")[-2]
            attr = ctrl_attr.split(".")[-1]

            # Skip the current attribute if it exists, and force is off
            # Otherwise, delete the channel and then import the data to that channel
            anim_connections = cmds.listConnections("{}.{}".format(ctrl, attr), type="animCurve", source=True)
            if anim_connections:
                # Check if attribute is already animated
                if force:
                    print("channel exists for: {}.{} - deleting and replacing with file data".format(ctrl, attr))
                    cmds.delete(anim_connections)
                else:
                    continue

            for keyframe_data in item[ctrl_attr]:
                time = keyframe_data["time"]
                in_tangents = keyframe_data["itt"]
                out_tangents = keyframe_data["ott"]
                in_angle = keyframe_data["ia"]
                out_angle = keyframe_data["oa"]
                in_tangents_x = keyframe_data["ix"]
                in_tangents_y = keyframe_data["iy"]
                out_tangents_x = keyframe_data["ox"]
                out_tangents_y = keyframe_data["oy"]

                cmds.setKeyframe(ctrl, attribute=attr, time=time, value=keyframe_data["value"])

                kwargs = {
                    "at": attr,
                    "t": (time, time),
                    "itt": in_tangents,
                    "ott": out_tangents
                }

                if out_tangents != "step":
                    if in_angle or out_angle:
                        kwargs["ia"] = in_angle
                        kwargs["oa"] = out_angle
                    elif ix or iy or ox or oy:
                        kwargs["ix"] = ix
                        kwargs["iy"] = iy
                        kwargs["ox"] = ox
                        kwargs["oy"] = oy
                
                cmds.keyTangent(ctrl, **kwargs)

    print("Imported correctly from: " + json_file)



# Usage in scripts:
# Exports the current scene data to /data/ as the name of the file + "_Anim.json"
"""
import ExportImportAnim as EIA
EIA.export_anim()
"""

# Imports the set filename from the /data/ folder and applies it to the current scene
# Using abs_path will overwrite the name argument
"""
import ExportImportAnim as EIA
EIA.import_anim(name="PoseTests_v0002_Anim.json", abs_path="~/home/user/docs/mayaproj/data/filename.json", force=False)

"""