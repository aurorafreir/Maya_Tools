# CREATE WINDOW
def create_window():
    winID = 'playblastFfmpeg'

    hv = 25
    wv = 100

    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)

    cmds.window(winID, title='Playblast Ffmpeg')

    # TODO
    # ffmpeg location
    # output location
    # in/out frames
    # resolution
    # format/encoder
    #

    #cmds.rowLayout(numberOfColumns=3)
    cmds.columnLayout(w=300)
    cmds.text(label="Ffmpeg Location")
    cmds.textField()
    cmds.setParent('..')

    cmds.columnLayout(w=300)
    cmds.text(label="Output Location")
    cmds.textField()
    cmds.button(label="Export Playblast")
    cmds.setParent('..')

    cmds.showWindow()


create_window()