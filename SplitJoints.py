import maya.cmds as cmds

joints = cmds.ls(sl=True, type='joint')

def lerp(min, max, percent):
    return ((max-min)*percent)+min

def vectorLerp(min, max, percent):
    x = lerp(min[0], max[0], percent)
    y = lerp(min[1], max[1], percent)
    z = lerp(min[2], max[2], percent)
    return (x,y,z)

pos1= vectorLerp(cmds.xform(joints[0], q=1, ws=1, rp=1), cmds.xform(joints[1], q=1, ws=1, rp=1), .25)
pos2= vectorLerp(cmds.xform(joints[0], q=1, ws=1, rp=1), cmds.xform(joints[1], q=1, ws=1, rp=1), .5)
pos3= vectorLerp(cmds.xform(joints[0], q=1, ws=1, rp=1), cmds.xform(joints[1], q=1, ws=1, rp=1), .75)

cmds.select(joints[0])

cmds.joint(p=pos1)
cmds.joint(p=pos2)
cmds.joint(p=pos3)
cmds.parent(joints[1], cmds.ls(sl=True, type='joint'))

cmds.rename(cmds.select(cmds.listRelatives(parent=True)), joints[0] + "4")
cmds.rename(cmds.select(cmds.listRelatives(parent=True)), joints[0] + "3")
cmds.rename(cmds.select(cmds.listRelatives(parent=True)), joints[0] + "2")
cmds.rename(joints[0], joints[0] + "1")

##world orient for joint
#currentJoint = cmds.ls(sl=True, type='joint')
#cmds.joint(oj='none', e=True)
#cmds.select(joints[1])