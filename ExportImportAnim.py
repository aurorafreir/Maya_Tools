"""
Script used for exporting and importing all the controller animation in a scene
"""

# Standard library imports
import json
import sys
import os

# Third party imports
import maya.cmds as cmds

# Local application imports



def export_anim():    
    # Get current project directory and scene name
    projectDirectory = cmds.workspace(q=True, rd=True)

    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)

    # Create empty json file to dump data to
    jsonfile = projectDirectory + "data/" + raw_name + "_Anim.json"
    with open(jsonfile, "w") as outfile:
        pass

    # Gather all control curves in scene
    controls = []
    for ctrl in cmds.ls(type="nurbsCurve"):
        tempname = (cmds.listRelatives(ctrl, p=1)[0])
        
        # Make sure that duplicates don't get added to the controls list
        if tempname not in controls:
            controls.append(tempname)

    export_data = []

    for ctrl in controls:
        ctrlattrs = [ctrl]
        for attr in cmds.listAttr(ctrl, k=1, u=1):
            # Get all keyframe times, and keyframe values as their own lists
            # [[frame], [frame], [frame]]
            # [[value], [value], [value]]
            keytimes = cmds.keyframe(ctrl + "." + attr, q=1, timeChange=1)
            keyvalues = cmds.keyframe(ctrl + "." + attr, q=1, valueChange=1)
            if keytimes and keyvalues:
                keytimevalue = []
                # Sort data to be [[frame, value], [frame, value], [frame, value]]
                for time, value in zip(keytimes, keyvalues):
                    keytimevalue.append([time, value])
                keydata = {ctrl + "." + attr : keytimevalue}
                
                export_data.append(keydata)


    with open(jsonfile, "w") as outfile:
        json.dump(export_data, outfile, indent=4)


def import_anim(name="", force=False):
    if not name:
        raise Exception("Must set the name of the file in the name arg!")
    
    # Get current project directory and scene name
    projectDirectory = cmds.workspace(q=True, rd=True)

    jsonfile = projectDirectory + "data/" + name
    print jsonfile
    with open(jsonfile, "r") as infile:
        data = json.load(infile)
    for item in data:
        for ctrlattr in item:
            for keyframedata in item[ctrlattr]:
                frame = keyframedata[0]
                value = keyframedata[1]
                # inputtangent = keyframedata[2]
                # outtangent = keyframedata[3]
                # keytype = keyframedata[4]
                cmds.setKeyframe(ctrlattr.split(".")[-2], at=ctrlattr.split(".")[-1], t=frame, v=value)



# Usage in scripts:
# Exports the current scene data to /data/ as the name of the file + "_Anim.json"
"""
import ExportImportAnim as EIA
EIA.export_anim()
"""

# Imports the set filename from the /data/ folder and applies it to the current scene
"""
import ExportImportAnim as EIA
EIA.import_anim(name="PoseTests_v0002_Anim.json", force=False)
"""