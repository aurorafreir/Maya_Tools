# CREATE WINDOW
def create_window(self):

    winID = 'aurWindow'

    hv = 25
    wv = 100

    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)

    cmds.window(winID, title='Control Panel')
    cmds.columnLayout()

    cmds.showWindow()
