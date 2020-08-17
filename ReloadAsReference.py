def reload_as_reference():
    import maya.cmds as cmds
    import os
    from shutil import move

    CurrentProj = cmds.workspace(active=True, q=True)
    os.chdir("{}".format(CurrentProj))

    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)

    if cmds.ls(sl=True):
        SelectedObjs = cmds.ls(sl=True)[0]
        cmds.file(rename=SelectedObjs)
        cmds.file(save=True)
        cmds.file(rename=filename)

        move(
            "{}/scenes/{}.ma".format(CurrentProj, SelectedObjs),
            "{}/assets/{}.ma".format(CurrentProj, SelectedObjs))

        cmds.file("{}/assets/{}.ma".format(CurrentProj, SelectedObjs), reference=True)
        cmds.delete(SelectedObjs)