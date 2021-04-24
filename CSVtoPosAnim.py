# Takes an input CSV file and sets it as the Translate X/Y/Z positions on the selected object
# based on the A/B/C columns in the CSV file, with the rows as frame numbers

import maya.cmds as cmds
import csv

sel = cmds.ls(sl=1)

results = []
cur_frame = 0
with open('/home/aurorafreir/Downloads/300Frames_XYZ_-_Copy.csv') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        results.append(row)

for iter, frame in enumerate(results):
    X, Y, Z = frame[0], frame[1], frame[2]
    cmds.setKeyframe(sel, v=X, attribute='translateX', t=iter)
    cmds.setKeyframe(sel, v=Y, attribute='translateY', t=iter)
    cmds.setKeyframe(sel, v=Z, attribute='translateZ', t=iter)