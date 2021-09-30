"""
Script to create a cluster for each selected Curve point
"""

# This is something we already discussed on the discord server but to me it's better to import as full name
# It's not mandatory but definitely avoid some clashes once in a while.

# Third party imports
import maya.cmds

# also don't keep what is not necessary.delete of put aside in another folder to reintegrate properly leater on eventually
# don't pollute the code. It make it more dense than it's actually is thus making the reading less efficient

# here it is better to put the curvePoints as an argument rather that querying them as selection inside the command
# the reason if that if you want to execute the command on a bunch of curve point that are not coming from a selection
# then you can.
# Ex : clusters = create_cluster_on_curve_points(['curve.cv[0]', 'curve.cv[2]'])
# also having it return the created clusters is always nice to have it you want to combine this command with others.


def create_cluster_on_curve_points(curvePoints):
    """create clusters on curve points

    :param curvePoints: curve points to create the clusters on
    :type curvePoints: list

    :return: the created clusters
    :rtype: list
    """

    # init
    clusters = []

    # execute
    for index, curvePoint in enumerate(curvePoints):

        # select the curve point to create the cv point on
        # generally speaking it's better to avoid selecting in command as it can alter the current selection once
        # the script is executed. I would follow maya doc example and create a cluster and add  the curvePoint to the
        # cluster set. But to make it work like what you already have you'll also have to put the cluster into position
        maya.cmds.select(curvePoint)

        # create cluster
        cluster, _ = maya.cmds.cluster(n="{}_{}".format(curvePoint.split(".")[0], str(index)))

        # add created cluster to the list
        clusters.append(cluster)

    # return
    return clusters
