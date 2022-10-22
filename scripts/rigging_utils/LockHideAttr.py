"""
Little script to lock and hide translation/rotation/scale/visibiltiy of an input object
"""

# Standard library imports

# Third party imports
from maya import cmds

# Local application imports


def lockhideattr(self, obj="",
                     hide=True, lock=True,
                     translation=True, rotate=True,
                     scale=True, visibility=True):
        if not translation and not rotate and not scale and not visibility:
            raise Exception("lockhideattr function for {} not set to do anything!".format(obj))

        attrs = []
        if translation:
            attrs.append("translate")
        if rotate:
            attrs.append("rotate")
        if scale:
            attrs.append("scale")

        kwargs = {

        }

        if hide:
            kwargs["keyable"] = 0
            kwargs["channelBox"] = 0
        if lock:
            kwargs["lock"] = 1

        for attr in attrs:
            for xyz in ["X", "Y", "Z"]:
                cmds.setAttr("{}.{}{}".format(obj, attr, xyz), **kwargs)
        if visibility:
            cmds.setAttr("{}.visibility".format(obj), **kwargs)
