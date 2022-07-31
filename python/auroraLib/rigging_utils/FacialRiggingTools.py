"""
A set of scripts that I use for my personal facial rigs!
This was done in probably less than a week, so it's all pretty messy lol, i'll clean it up at some point
All of these scripts assume Y+ Up and Z+ Forwards for characters.
An example of how to use them is at the end :)
"""

# SYSTEM IMPORTS

# STANDARD LIBRARY IMPORTS
import pymel.core as pm

# LOCAL APPLICATION IMPORTS


class FacialRiggingTools:
    def __init__(self, main_group:str, head_jnt:str):
        self.main_group = main_group
        self.head_jnt = head_jnt

        self.attr_settings = {"keyable": True, "hidden": False,
                         "hasMinValue": True, "hasMaxValue": True,
                         "minValue": 0, "maxValue": 1}

        self.ensure_setup()

    def ensure_setup(self) -> None:
        if not pm.objExists(self.main_group):
            pm.group(name=self.main_group, empty=True)

        return None

    def proper_rivet(self, mesh_in: str, vtx: int, mesh_shape_in="", mesh_shape_orig_in="") -> [pm.nt.Transform, pm.nt.UvPin]:
        # im mad
        # normal cmds.Rivet() doesn't actually return the data it prints out, the uvPin and Rivet names.

        mesh_transform = pm.PyNode(mesh_in)

        if mesh_shape_in:
            mesh_shape = pm.PyNode(mesh_shape_in)  # Lets the user overwrite mesh_shape if wanted
        else:
            mesh_shape = mesh_transform.getShapes()[0]

        if mesh_shape_orig_in:
            mesh_shape_orig = pm.PyNode(mesh_shape_orig_in)  # Lets the user overwrite mesh_shape_orig if wanted
        else:
            # Check if orig shape exists, and if not, set the shape_orig to the first shape
            transform_shapes = mesh_transform.getShapes()
            does_orig_shape_exist = [i for i in transform_shapes if i.name().endswith("Orig")][0]
            if does_orig_shape_exist:
                mesh_shape_orig = does_orig_shape_exist
            else:
                mesh_shape_orig = mesh_shape

        temp_loc = pm.spaceLocator()

        ws_vert_loc = pm.pointPosition(f"{mesh_transform}.vtx[{vtx}]", world=True)

        temp_loc.t.set(ws_vert_loc)

        cpom_node = pm.createNode("closestPointOnMesh")
        temp_loc.t >> cpom_node.inPosition
        mesh_shape.outMesh >> cpom_node.inMesh

        u = cpom_node.parameterU.get()
        v = cpom_node.parameterV.get()

        pm.delete(temp_loc)
        pm.delete(cpom_node)

        rivet_loc = pm.spaceLocator()
        rivet_loc.rename(f"rivet_{vtx}_rvt")

        uvPin_node = pm.createNode("uvPin")
        uvPin_node.coordinate[0].coordinateU.set(u)
        uvPin_node.coordinate[0].coordinateV.set(v)

        mesh_shape.outMesh >> uvPin_node.deformedGeometry
        mesh_shape_orig.outMesh >> uvPin_node.originalGeometry

        uvPin_node.outputMatrix[0] >> rivet_loc.offsetParentMatrix

        return rivet_loc, uvPin_node

    def rivets_per_vertex(self, object_to_rivet:str) -> pm.nt.Transform:
        rivet_object = pm.PyNode(object_to_rivet)

        rvt_grp = pm.group(name="Rivets", empty=True)
        pm.parent(rvt_grp, self.main_group)

        pm.select(object_to_rivet)
        vtx_count = pm.polyEvaluate(rivet_object, vertex=True)

        for index in range(vtx_count):
            rivet, _ = self.proper_rivet(mesh_in=object_to_rivet, vtx=index)
            pm.parent(rivet, rvt_grp)

        return rvt_grp

    def name_arbitrary_mirrored_objects(self, group_name:str, centre_variance=0.2) -> None:
        group = pm.PyNode(group_name)
        for object in group.getChildren():
            worldspace_translate = pm.xform(object, translation=True, worldSpace=True, query=True)
            lcr = "l" if worldspace_translate[0] >=  centre_variance else "c"
            lcr = lcr if worldspace_translate[0] >= -centre_variance else "r"

            object.rename(f"{lcr}_{object.name()}")

        l_rvts = [i for i in group.getChildren() if i.name().startswith("l_")]
        r_rvts = [i for i in group.getChildren() if i.name().startswith("r_")]
        for r_object in r_rvts:
            worldspace_translate = pm.xform(r_object, translation=True, worldSpace=True, query=True)
            worldspace_translate_mirrored = [worldspace_translate[0] * -1, worldspace_translate[1], worldspace_translate[2]]

            for index, l_object in enumerate(l_rvts):
                l_worldspace_translation_dp = ["{:.2f}".format(i) for i in pm.xform(l_object, translation=True, worldSpace=True, query=True)]
                r_worldspace_translation_dp = ["{:.2f}".format(i) for i in worldspace_translate_mirrored]
                if l_worldspace_translation_dp == r_worldspace_translation_dp:
                    print(r_object, l_object)
                    r_object.rename(l_object.name().replace("l_", "r_"))
                    l_rvts.pop(index)
                    continue

        return None

    def joint_per_rivet(self, rivet_group:str) -> None:
        rvt_grp = pm.PyNode(rivet_group)

        jnt_grp = pm.group(name="Joints", empty=True)
        pm.parent(jnt_grp, self.main_group)

        for i in rvt_grp.getChildren():
            t = pm.xform(i, t=True, worldSpace=True, query=True)
            jnt = pm.joint(name="{}".format(i.name().replace("_rvt", "_jnt")))
            pm.parent(jnt, jnt_grp)
            jnt.radius.set(0.25)
            i.worldMatrix >> jnt.offsetParentMatrix
            pm.select(deselect=True)

        return None

    def ctl_create(self, shape:str, name:str) -> [pm.nt.Transform, pm.nt.Transform]:

        pm.select(deselect=True)

        grp = pm.group(name=f"{name}_grp")

        if shape == "square":
            ctl = pm.curve(degree=1,
                           name=f"{name}_ctl",
                           point=[(-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0), (-.5, -.5, 0)])
        elif shape == "circle":
            ctl, _ = pm.circle(name=f"{name}_ctl")
            pm.bakePartialHistory(ctl)
        elif shape == "cube":
            ctl = pm.curve(degree=1,
                           name=f"{name}_ctl",
                           p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5),
                              (.5, -0.5, .5), (.5, -0.5, -0.5), (.5, .5, -0.5),
                              (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (.5, -0.5, -0.5),
                              (.5, .5, -0.5), (.5, .5, .5), (-0.5, .5, .5),
                              (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5),
                              (.5, -0.5, .5)])

        pm.parent(ctl, grp)

        return grp, ctl

    def normalized_invert_floatmath_node(self, side:str, prefix:str, input_node:str, input_att:str) -> str:
        inv_node = pm.createNode("floatMath", name=f"eyelid_{prefix}_{side}_invert")
        pm.connectAttr(f"{input_node}.{input_att}", inv_node.floatB)
        inv_node.operation.set(1)
        inv_node_name = inv_node.name()

        return inv_node_name

    def eye_rig(self, side:str, eye_loc:str) -> classmethod:
        eye_loc = pm.PyNode(eye_loc)
        eye_loc_pos = eye_loc.t.get()
        head_jnt = pm.PyNode(self.head_jnt)

        main_jnt = pm.joint(name=f"eye_{side}_jnt")
        lower_jnt = pm.joint(name=f"eye_lower_{side}_jnt")
        lower_jnt.radius.set(0.75)
        upper_jnt = pm.joint(name=f"eye_upper_{side}_jnt")
        upper_jnt.radius.set(0.5)

        pm.parent(upper_jnt, main_jnt)
        pm.select(deselect=True)
        pm.parent(main_jnt, head_jnt)
        pm.parent(lower_jnt, head_jnt)
        pm.parent(upper_jnt, head_jnt)
        pm.xform(main_jnt, translation=eye_loc_pos, worldSpace=True)
        pm.xform(lower_jnt, translation=eye_loc_pos, worldSpace=True)
        pm.xform(upper_jnt, translation=eye_loc_pos, worldSpace=True)
        pm.select(deselect=True)

        eye_grp, eye_ctl  = self.ctl_create(shape="circle", name=f"eye_{side}")
        eye_grp.t.set(eye_loc_pos)
        pm.xform(eye_grp, translation=[0,0,40], relative=True)
        pm.select(deselect=True)

        eye_attributes = []

        for attr_name in ["Follow", "Lower", "Upper"]:
            pm.addAttr(eye_ctl, longName=f"{side}_Eyelid_{attr_name}", **self.attr_settings)
            eye_attributes.append(f"{eye_ctl.name()}.{side}_Eyelid_{attr_name}")

        # NODE SETUP
        for u_l in ["Lower", "Upper"]:
            # EYELID FOLLOW SETUP
            eye_follow_invfm = self.normalized_invert_floatmath_node(side=side, prefix=f"{u_l}_Follow",
                                                                 input_node=eye_ctl, input_att=f"{side}_Eyelid_Follow")
            eye_follow_invfm = pm.PyNode(eye_follow_invfm)

            eye_follow_abnar = pm.createNode("animBlendNodeAdditiveRotation", name=f"eyelid_follow_{side}_abnar")

            # pm.connectAttr(f"{eye_ctl.name()}.{side}_Eyelid_Follow", eye_follow_invfm.floatB)
            pm.connectAttr(eye_follow_invfm.outFloat, eye_follow_abnar.weightA)
            pm.connectAttr(f"{eye_ctl.name()}.{side}_Eyelid_Follow", eye_follow_abnar.weightB)

            main_jnt.rotate >> eye_follow_abnar.inputB

            # EYELID CLOSE SETUP
            eye_close_invfm = self.normalized_invert_floatmath_node(side=side, prefix=f"{u_l}_Close",
                                                                     input_node=eye_ctl,
                                                                     input_att=f"{side}_Eyelid_{u_l}")
            eye_close_invfm = pm.PyNode(eye_close_invfm)

            eye_close_abnar = pm.createNode("animBlendNodeAdditiveRotation", name=f"eyelid_close_{side}_abnar")

            pm.connectAttr(eye_close_invfm.outFloat, eye_close_abnar.weightA)
            pm.connectAttr(f"{eye_ctl.name()}.{side}_Eyelid_{u_l}", eye_close_abnar.weightB)

            eye_close_interactive_loc = pm.spaceLocator()
            eye_close_interactive_loc.rename(f"{side}_Eyelid_{u_l}_Closed_DELETEME_loc")

            eye_close_interactive_loc.t.set(eye_loc_pos)
            pm.parent(eye_close_interactive_loc, self.main_group)
            eye_close_interactive_loc.r >> eye_close_abnar.inputB

            # EYELID BLEND SETUP
            eye_blend_abnar = pm.createNode("animBlendNodeAdditiveRotation", name=f"eyelid_blend_{side}_abnar")
            eye_follow_abnar.output >> eye_blend_abnar.inputA
            eye_close_abnar.output >> eye_blend_abnar.inputB

            pm.connectAttr(eye_blend_abnar.output, f"eye_{u_l.lower()}_{side}_jnt.rotate")

        # END NODE SETUP

        pm.aimConstraint(eye_ctl, main_jnt, worldUpType="objectrotation", worldUpObject=head_jnt, aimVector=[0,0,1])

        # return eye_ctl
        class eye_rig:
            def __init__(self, eye_ctl, eye_grp, eye_attributes):
                self.control = eye_ctl
                self.group = eye_grp
                self.eye_attributes = eye_attributes

        return eye_rig(eye_ctl, eye_grp, eye_attributes)

    def eye_runner(self, eyes:list, sides:list) -> None:
        eyeMain_grp, eyeMain_ctl = self.ctl_create(shape="square", name="eyesMain")

        # Creating an attribute for the Follow attr on the individual controls, as well as the main control
        # I'll connect these up so that only the main control does anything later
        follow_attr_name = "Eyes_Follow"
        pm.addAttr(eyeMain_ctl, ln=follow_attr_name, **self.attr_settings)

        eye_ctls = []
        eye_grps = []
        for eye, side in zip(eyes, sides):
            rig_class = self.eye_rig(side=side, eye_loc=eye)
            eye_ctls.append(rig_class.control)
            eye_grps.append(rig_class.group)

            eye_follow_attr = rig_class.eye_attributes[0]
            eye_follow_attr_proxy_name = f"{eye_follow_attr.split('.')[1]}_Proxy"
            pm.addAttr(eyeMain_ctl, proxy=eye_follow_attr, ln=eye_follow_attr_proxy_name)
            pm.connectAttr(f"{eyeMain_ctl}.{follow_attr_name}", eye_follow_attr)

        # Getting the average position of any created eye controls
        eye_ctl_count = len(eye_ctls)
        x = [pm.xform(x, ws=True, t=True, query=True)[0] for x in eye_ctls]
        y = [pm.xform(y, ws=True, t=True, query=True)[1] for y in eye_ctls]
        z = [pm.xform(z, ws=True, t=True, query=True)[2] for z in eye_ctls]
        eye_ctls_pos = [sum(x)/eye_ctl_count, sum(y)/eye_ctl_count, sum(z)/eye_ctl_count]
        eyeMain_grp.t.set(eye_ctls_pos)

        for grp in eye_grps:
            pm.parent(grp, eyeMain_ctl)

        pm.parent(eyeMain_grp, self.main_group)

        return None

    def mouth_rig(self, jaw_loc:str, ends:list, sides:list, front_c_loc:str) -> None:
        head_jnt = pm.PyNode(self.head_jnt)
        jaw_loc = pm.PyNode(jaw_loc)
        jaw_loc_pos = jaw_loc.t.get()

        mouth_rig_grp = pm.group(name="Mouth_Rig_grp", empty=True)
        pm.parent(mouth_rig_grp, self.main_group)

        front_c_loc = pm.PyNode(front_c_loc)
        pm.select(deselect=True)

        jaw_jnt = pm.joint(name="jaw_C_jnt")
        jaw_jnt.t.set(jaw_loc_pos)
        pm.parent(jaw_jnt, head_jnt)
        pm.select(deselect=True)

        jaw_grp, jaw_ctl = self.ctl_create(shape="cube", name="jaw")
        jaw_grp.t.set(jaw_loc_pos)
        pm.parent(jaw_grp, mouth_rig_grp)
        pm.parentConstraint(jaw_ctl, jaw_jnt, maintainOffset=True)

        for end, side in zip(ends, sides):
            end_loc = pm.PyNode(end)
            end_loc_pos = end_loc.t.get()

            pm.select(deselect=True)
            main_end_jnt = pm.joint(name=f"mouth_end_{side}_jnt")
            upper_jnt = pm.joint(name=f"mouth_upper_{side}_jnt")
            lower_jnt = pm.joint(name=f"mouth_lower_{side}_jnt")
            upper_jnt.radius.set(.75)
            lower_jnt.radius.set(.5)

            pm.parent(lower_jnt, main_end_jnt)
            main_end_jnt.t.set(end_loc_pos)
            pm.parent(main_end_jnt, head_jnt)

            pm.select(deselect=True)

            end_grp, end_ctl = self.ctl_create(shape="cube", name=f"mouth_end_{side}")
            end_grp.t.set(end_loc_pos)
            pm.parent(end_grp, mouth_rig_grp)
            pm.parentConstraint(head_jnt, jaw_jnt, end_grp, maintainOffset=True)

            pm.parentConstraint(end_ctl, main_end_jnt)

            mid_z_pos = (front_c_loc.t.get()[2] + end_loc_pos[2]) / 2
            mid_ctl_pos = [end_loc_pos[0], end_loc_pos[1], mid_z_pos]

            mid_upper_grp, mid_upper_ctl = self.ctl_create(shape="cube", name=f"mouth_upper_mid_{side}")
            mid_lower_grp, mid_lower_ctl = self.ctl_create(shape="cube", name=f"mouth_lower_mid_{side}")
            mid_upper_grp.t.set(mid_ctl_pos)
            mid_lower_grp.t.set(mid_ctl_pos)

            pm.parent(mid_upper_grp, mouth_rig_grp)
            pm.parentConstraint(self.head_jnt, mid_upper_grp, maintainOffset=True)
            pm.parent(mid_lower_grp, jaw_ctl)

            pm.aimConstraint(mid_upper_ctl, upper_jnt, worldUpType="objectrotation", worldUpObject=head_jnt,
                             aimVector=[0, 0, 1])
            pm.aimConstraint(mid_lower_ctl, lower_jnt, worldUpType="objectrotation", worldUpObject=head_jnt,
                             aimVector=[0, 0, 1])

    def eyebrow_rig(self) -> None:
        pass

"""
from Rigging import FacialRiggingTools

# SETUP
frt = FacialRiggingTools.FacialRiggingTools(main_group="Facial_Rig", head_jnt="neck_C0_head_jnt")

# RIVET RIG
rivet_group = frt.rivets_per_vertex(object_to_rivet="Facial_Buffer")
frt.name_arbitrary_mirrored_objects(group_name=rivet_group, centre_variance=0.2)
frt.joint_per_rivet(rivet_group=rivet_group)

# EYES RIG
frt.eye_runner(eyes=["eye_L_loc", "eye_R_loc"], sides=["L", "R"])

# MOUTH RIG
frt.mouth_rig(jaw_loc="jaw_loc", l_r_side=["mouth_end_L_loc", "mouth_end_R_loc"], front_c_loc="mouth_front_C_loc")

# EYEBROW RIG
#frt.eyebrow_rig()
"""
