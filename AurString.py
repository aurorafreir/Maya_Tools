import maya.cmds as cmds

selected = cmds.ls(selection=True)

selected_len = (len(selected))
print selected_len

if len(selected) == 2:
    for item in selected[:1]:
        rPiv = cmds.xform(item, q=True, rp=True)  # query rotation pivot
        sPiv = cmds.xform(item, q=True, sp=True)  # query scale pivot

        loc = cmds.spaceLocator(n="wireLocator1")
        cmds.xform(t=rPiv)

    for item in selected[1:]:
        rPiv = cmds.xform(item, q=True, rp=True)  # query rotation pivot
        sPiv = cmds.xform(item, q=True, sp=True)  # query scale pivot

        loc = cmds.spaceLocator(n= "wireLocator2")
        cmds.xform(t=rPiv)


#cmds.curve('string_##',)

#cmds.delete("wireLocator1")
#cmds.delete("wireLocator2")
