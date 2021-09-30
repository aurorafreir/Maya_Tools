"""
Takes an input CSV file and sets it as the Translate X/Y/Z positions on the selected object
based on the A/B/C columns in the CSV file, with the rows as frame numbers
"""

# python imports
import csv

# Third party imports
import maya.cmds


def csvtotransanim(filename, selection):
    """description of what the command does here

    :param filename: name of the file to get the information from
    :type filename: str

    :param selection: selection to apply the transfer of animation to
    :type selection: list
    """

    # init
    results = []

    # update result
    with open(filename) as csvFile:
        reader = csv.reader(csvFile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            results.append(row)

    # Run through each row, and set the values for each (X, Y, Z) value accordingly
    for iteration, values in enumerate(results):
        for value, axis in zip(values, ["X", "Y", "Z"]):
            maya.cmds.setKeyframe(selection, value=value, attribute="translate{}".format(axis), time=iteration)
