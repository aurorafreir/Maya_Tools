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

    jsonfile = os.path.join(project_directory, "data", raw_name + "_Anim.json")

    # Gather all control curves in scene
    controls = []
    export_data = []

    for ctrl in cmds.ls(type="nurbsCurve"):
        ctrlcrvparent = cmds.listRelatives(ctrl, parent=1)[0]
        
        # Make sure that duplicates don't get added to the controls list
        if ctrlcrvparent in controls:
            continue
        controls.append(ctrlcrvparent)

        for attr in cmds.listAttr(ctrlcrvparent, keyable=1, unlocked=1):
            # Get all keyframe times, and keyframe values as their own lists
            # [[frame], [frame], [frame]]
            # [[value], [value], [value]]
            ctrl_attr = "{}.{}".format(ctrlcrvparent, attr)
            

            key_times = cmds.keyframe(ctrl_attr, query=1, timeChange=1)
            key_values = cmds.keyframe(ctrl_attr, query=1, valueChange=1)

            in_tangents = cmds.keyTangent(ctrl_attr, query=1, itt=1)
            out_tangents = cmds.keyTangent(ctrl_attr, query=1, ott=1)
            in_angle = cmds.keyTangent(ctrl_attr, query=1, ia=1)
            out_angle = cmds.keyTangent(ctrl_attr, query=1, oa=1)
            in_tangents_x  = cmds.keyTangent(ctrl_attr, query=1, ix=1)
            in_tangents_y  = cmds.keyTangent(ctrl_attr, query=1, iy=1)
            out_tangents_x = cmds.keyTangent(ctrl_attr, query=1, ox=1)
            out_tangents_y = cmds.keyTangent(ctrl_attr, query=1, oy=1)

            if key_times and key_values:
                keytimevalue = []
                
                for i in range(len(key_times)):
                    keytimevalue.append({
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
                
                export_data.append({"{}.{}".format(ctrlcrvparent, attr) : keytimevalue})


    with open(jsonfile, "w") as outfile:
        json.dump(export_data, outfile)
    
    print("Exported correctly to: " + jsonfile)


def import_anim(name="", abspath="", force=False):
    if not name:
        raise Exception("Must set the name of the fyTanile in the name arg!") 
    
    if abspath:
        jsonfile = abspath
    else:
        # Get current project directory and scene name
        project_directory = cmds.workspace(query=True, rootDirectory=True)
        jsonfile = os.path.join(project_directory, "data", name)


    if not os.path.isfile(jsonfile):
        raise OSError("File: " + jsonfile + " - not found!")

    with open(jsonfile, "r") as infile:
        data = json.load(infile)

    for item in data:
        for ctrlattr in item:
            ctrl = ctrlattr.split(".")[-2]
            attr = ctrlattr.split(".")[-1]

            # Skip the current attribute if it exists, and force is off
            # Otherwise, delete the channel and then import the data to that channel
            anim_connections = cmds.listConnections(ctrl + "." + attr, type="animCurve", s=1)
            if anim_connections:
                # Check if attribute is already animated
                if force:
                    print("channel exists for: " + ctrl + "." + attr + " - deleting and replacing with file data")
                    cmds.delete(anim_connections)
                else:
                    continue

            for keyframedata in item[ctrlattr]:
                time = keyframedata["time"]
                in_tangents = keyframedata["itt"]
                out_tangents = keyframedata["ott"]
                in_angle = keyframedata["ia"]
                out_angle = keyframedata["oa"]
                in_tangents_x = keyframedata["ix"]
                in_tangents_y = keyframedata["iy"]
                out_tangents_x = keyframedata["ox"]
                out_tangents_y = keyframedata["oy"]

                cmds.setKeyframe(ctrl, attribute=attr, time=time, v=keyframedata["value"])

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

    print("Imported correctly from: " + jsonfile)



# Usage in scripts:
# Exports the current scene data to /data/ as the name of the file + "_Anim.json"
"""
import ExportImportAnim as EIA
EIA.export_anim()
"""

# Imports the set filename from the /data/ folder and applies it to the current scene
# Using abspath will overwrite the name argument
"""
import ExportImportAnim as EIA
EIA.import_anim(name="PoseTests_v0002_Anim.json", abspath="~/home/user/docs/mayaproj/data/filename.json", force=False)

"""