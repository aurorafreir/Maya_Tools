"""
Script used for exporting and importing all the controller animation in a scene
"""

# Standard library imports
import json
import sys
import os.path

# Third party imports
import maya.cmds as cmds

# Local application imports



def export_anim():    
    # Get current project directory and scene name
    projectDirectory = cmds.workspace(q=True, rd=True)

    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)

    jsonfile = projectDirectory + "data/" + raw_name + "_Anim.json"

    # Gather all control curves in scene
    controls = []
    for ctrl in cmds.ls(type="nurbsCurve"):
        ctrlcrvparent = (cmds.listRelatives(ctrl, p=1)[0])
        
        # Make sure that duplicates don't get added to the controls list
        if ctrlcrvparent not in controls:
            controls.append(ctrlcrvparent)

    export_data = []

    for ctrl in controls:
        for attr in cmds.listAttr(ctrl, k=1, u=1):
            # Get all keyframe times, and keyframe values as their own lists
            # [[frame], [frame], [frame]]
            # [[value], [value], [value]]
            ctrlattr = ctrl + "." + attr
            keytimes = cmds.keyframe(ctrlattr, q=1, timeChange=1)
            keyvalues = cmds.keyframe(ctrlattr, q=1, valueChange=1)

            intangent = cmds.keyTangent(ctrlattr, q=1, itt=1)
            outtangent = cmds.keyTangent(ctrlattr, q=1, ott=1)
            inangle = cmds.keyTangent(ctrlattr, q=1, ia=1)
            outangle = cmds.keyTangent(ctrlattr, q=1, oa=1)
            ix, iy = cmds.keyTangent(ctrlattr, q=1, ix=1), cmds.keyTangent(ctrlattr, q=1, iy=1)
            ox, oy = cmds.keyTangent(ctrlattr, q=1, ox=1), cmds.keyTangent(ctrlattr, q=1, oy=1)

            if keytimes and keyvalues:
                keytimevalue = []
                # Sort data to be [[frame, value], [frame, value], [frame, value]]
                for time, value, itt, ott, ia, oa, ix, iy, ox, oy in zip(keytimes, keyvalues, intangent, outtangent, inangle, outangle, ix, iy, ox, oy):
                    keytimevalue.append([time, value, itt, ott, ia, oa, ix, iy, ox, oy])
                keydata = {ctrl + "." + attr : keytimevalue}
                
                export_data.append(keydata)


    with open(jsonfile, "w") as outfile:
        json.dump(export_data, outfile, indent=4)
    
    print("Exported correctly to: " + jsonfile)


def import_anim(name="", force=False):
    if not name:
        raise Exception("Must set the name of the file in the name arg!") 
    
    # Get current project directory and scene name
    projectDirectory = cmds.workspace(q=True, rd=True)
    jsonfile = projectDirectory + "data/" + name

    if not os.path.isfile(jsonfile):
        raise Exception("File: " + jsonfile + " - not found!")

    with open(jsonfile, "r") as infile:
        data = json.load(infile)

    for item in data:
        for ctrlattr in item:
            ctrl = ctrlattr.split(".")[-2]
            attr = ctrlattr.split(".")[-1]

            print item[ctrlattr]

            # Skip the current attribute if it exists, and force is off
            # Otherwise, delete the channel and then import the data to that channel
            if cmds.listConnections(ctrl + "." + attr, type="animCurve", s=1):
                # Check if attribute is already animated
                if force:
                    print("channel exists for: " + ctrl + "." + attr + " - deleting and replacing with file data")
                    cmds.delete(cmds.listConnections(ctrl + "." + attr, type="animCurve", s=1))
                else:
                    continue

            for keyframedata in item[ctrlattr]:   
                frame = keyframedata[0]
                value = keyframedata[1]

                intangent = keyframedata[2]
                outtangent = keyframedata[3]
                inangle = keyframedata[4]
                outangle = keyframedata[5]

                ix, iy = keyframedata[6], keyframedata[7]
                ox, oy = keyframedata[8], keyframedata[9]

                cmds.setKeyframe(ctrl, at=attr, t=frame, v=value)

                if outtangent == "step":
                    cmds.keyTangent(ctrl, at=attr, t=(frame, frame),
                        itt=intangent, ott=outtangent)
                elif inangle or outangle:
                    cmds.keyTangent(ctrl, at=attr, t=(frame, frame),
                        itt=intangent, ott=outtangent,
                        ia=inangle, oa=outangle)
                elif ix or iy or ox or iy:
                    cmds.keyTangent(ctrl, at=attr, t=(frame, frame),
                        itt=intangent, ott=outtangent,
                        ix=ix, iy=iy,
                        ox=ox, oy=oy)

    print("Imported correctly from: " + jsonfile)



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