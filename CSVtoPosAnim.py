"""
Takes an input CSV file and sets it as the Translate X/Y/Z positions on the selected object
based on the A/B/C columns in the CSV file, with the rows as frame numbers
"""

# Standard library imports
import csv

# Third party imports
from maya import cmds

# Local application imports


def csvtotransanim(filename=""):
    sel = cmds.ls(sl=1)

    results = []
    cur_frame = 0

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            results.append(row)

    # Run through each row, and set the values for each (X, Y, Z) value accordingly
    for iter, values in enumerate(results):
        for value, attr in zip(values, ["X", "Y", "Z"]:
            cmds.setKeyframe(sel, value=value, attribute="translate{}".format(attr), t=iter)


csvtotransanim(filename="/home/aurorafreir/Downloads/300Frames_XYZ_-_Copy.csv")