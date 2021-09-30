"""
Old script used for creating a joint for creating square controllers for each joint in selection
"""

# Third party imports
import maya.cmds


def create_joint_controllers(joints):
    """same here description of the command, and eventually from argument and return
    Do not make the economy of not doing them as you create your command. Docstring are how you will be able, to
    get back to why the command exists and how to use it. And thi is what your mates will rely on !!

    :param joints:
    :type joints:

    :return:
    :rtype:
    """

    # same here

    for index, joint in enumerate(joints):

        # Selects child joint and sets it as variable tempSel_AimAt
        TempSel_AimAt = maya.cmds.listRelatives(joint, type='joint')

        # Creates square NURBS curve and deletes it's history
        # Explicit is better than implicit - resist the temptation to shorten the name of argument
        # in the long run you'll be happy to have them in the complete form. It's easier to understand

        # not sure the deselect is necessary here - again better avoid selection manipulation if not necessary
        maya.cmds.select(deselect=True)

        controller = maya.cmds.curve(degree=1,
                                     point=[(-0.5, 0, .5), (-0.5, 0, -.5), (.5, 0, -.5), (.5, 0, .5), (-0.5, 0, .5)],
                                     name='CTRL_{}'.format(index))

        maya.cmds.rotate(0, 0, 90)
        maya.cmds.makeIdentity(apply=True, translate=1, rotate=1, scale=1, normal=0)
        maya.cmds.bakePartialHistory()

        # Makes a group and makes the controller a child of the PIVOT group
        pivotGroup = maya.cmds.group(empty=True, name='PIVOT_{}'.format(index))
        maya.cmds.parent(controller, pivotGroup)

        # Makes parent constraint for controller location
        constraint = maya.cmds.parentConstraint(joint, pivotGroup, maintainOffset=False)
        maya.cmds.delete(constraint)

        if not joint:
            maya.cmds.warning("no child joint of {}, skipping rotation".format(index))
        elif len(TempSel_AimAt) == 1:
            # Makes aim constraint for controller orientation
            constraint = maya.cmds.aimConstraint(TempSel_AimAt, pivotGroup)
            maya.cmds.delete(constraint)

        # Parent constraint the joint to the controller
        maya.cmds.parentConstraint(controller, joint, name='parentConstraint_{0}_CTRL_{0}'.format(index))
