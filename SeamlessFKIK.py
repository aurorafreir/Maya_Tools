###mostly from https://bindpose.com/seamless-ik-fk-switch-maya-python/
###script edited to include my own naming conventions
###and also to work whether the rig is referenced or not

import maya.cmds as mc

if mc.objExists('*:CTRL_Left_FKIK.IK'):
	if mc.getAttr('*:CTRL_Left_FKIK.IK'):
		# From IK to FK
		mc.delete(mc.orientConstraint('*:JNT_Left_IK_Shoulder', '*:CTRL_Left_FK_Shoulder'))
		mc.delete(mc.orientConstraint('*:JNT_Left_IK_Elbow', '*:CTRL_Left_FK_Elbow'))
		mc.delete(mc.orientConstraint('*:JNT_Left_IK_Wrist', '*:CTRL_Left_FK_Wrist'))

		mc.setAttr('*:CTRL_Left_FKIK.IK', 0)
	else:
		# From FK to IK
		mc.delete(mc.parentConstraint('*:CTRL_Left_IK_Wrist_LOC', '*:CTRL_Left_IK_Wrist'))

		arm01Vec = [mc.xform('*:JNT_Left_FK_Elbow', t=1, ws=1, q=1)[i] - mc.xform('*:CTRL_Left_FK_Shoulder', t=1, ws=1, q=1)[i] for i in range(3)]
		arm02Vec = [mc.xform('*:JNT_Left_FK_Elbow', t=1, ws=1, q=1)[i] - mc.xform('*:CTRL_Left_FK_Wrist', t=1, ws=1, q=1)[i] for i in range(3)]

		mc.xform('*:CTRL_Left_Arm_IK_PoleVector', t=[mc.xform('*:CTRL_Left_FK_Elbow', t=1, q=1, ws=1)[i] + arm01Vec[i] * .75 + arm02Vec[i] * .75 for i in range(3)], ws=1)

		mc.setAttr('*:CTRL_Left_FKIK.IK', 1)
		
else:
	if mc.getAttr('CTRL_Left_FKIK.IK'):
		# From IK to FK
		mc.delete(mc.orientConstraint('JNT_Left_IK_Shoulder', 'CTRL_Left_FK_Shoulder'))
		mc.delete(mc.orientConstraint('JNT_Left_IK_Elbow', 'CTRL_Left_FK_Elbow'))
		mc.delete(mc.orientConstraint('JNT_Left_IK_Wrist', 'CTRL_Left_FK_Wrist'))

		mc.setAttr('CTRL_Left_FKIK.IK', 0)
	else:
		# From FK to IK
		mc.delete(mc.parentConstraint('CTRL_Left_IK_Wrist_LOC', 'CTRL_Left_IK_Wrist'))

		arm01Vec = [mc.xform('JNT_Left_FK_Elbow', t=1, ws=1, q=1)[i] - mc.xform('CTRL_Left_FK_Shoulder', t=1, ws=1, q=1)[i] for i in range(3)]
		arm02Vec = [mc.xform('JNT_Left_FK_Elbow', t=1, ws=1, q=1)[i] - mc.xform('CTRL_Left_FK_Wrist', t=1, ws=1, q=1)[i] for i in range(3)]

		mc.xform('CTRL_Left_Arm_IK_PoleVector', t=[mc.xform('CTRL_Left_FK_Elbow', t=1, q=1, ws=1)[i] + arm01Vec[i] * .75 + arm02Vec[i] * .75 for i in range(3)], ws=1)

		mc.setAttr('CTRL_Left_FKIK.IK', 1)
