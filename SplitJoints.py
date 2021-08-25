import maya.cmds as cmds

joints = cmds.ls(sl=True, type='joint')


def lerp(min, max, percent):
    return ((max-min)*percent)+min


def vector_lerp(min, max, percent):
    x = lerp(min[0], max[0], percent)
    y = lerp(min[1], max[1], percent)
    z = lerp(min[2], max[2], percent)
    return x, y, z


joint_count = 3
joint_adder = 1.0 / (joint_count + 1)
cur_jnt_count = 0.0
cmds.select(d=1)
for joint in range(1, joint_count+1):
    jointend = cmds.joint(p=vector_lerp(cmds.xform(joints[0], q=1, ws=1, rp=1),
                             cmds.xform(joints[1], q=1, ws=1, rp=1),
                             cur_jnt_count))

    cur_jnt_count = cur_jnt_count + joint_adder

cmds.parent(joints[1], jointend)
