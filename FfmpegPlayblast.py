# CREATE WINDOW
def create_window():
    import maya.cmds as cmds
    import os

    winID = 'playblastFFmpeg'
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)
    cmds.window(winID, title='Playblast FFmpeg')

    # TODO
    # ffmpeg location /media/aurora/gdrive/Apps/ffmpeg.exe
    # output location
    # // send commands to CLI
    # in/out frames
    # resolution
    # format/encoder
    # actual playblast

    # os.system('gnome-terminal && cd ~/Downloads && ffmpeg -i video0.mp4 video1.mp4')

    def save_settings(self):
        cmds.optionVar(sv=('playblastFFmpeg_ffmpegLoc', cmds.textFieldButtonGrp(ffmpegLocationText, q=True, text=True)))
        cmds.optionVar(sv=('playblastFFmpeg_outputLoc', cmds.textField(outputLocationText, q=True, text=True)))

    # FFMPEG LOCATION
    cmds.columnLayout(w=300, rs=5)
    #cmds.text(label="FFmpeg Location")
    ffmpegLocation = cmds.optionVar(q='playblastFFmpeg_ffmpegLoc')
    #ffmpegLocationText = cmds.textField(text=ffmpegLocation, ec=save_settings, aie=True, w=300)
    ffmpegLocationText = cmds.textFieldButtonGrp(label='FFmpeg Location', buttonLabel='FFmpeg Location', text=ffmpegLocation, cc=save_settings)
    cmds.button(label="open FFmpeg")
    cmds.setParent('..')

    # RESOLUTION
    cmds.columnLayout()
    cmds.text(label="Video Resolution")
    cmds.textField()
    cmds.textField()

    # IN/OUT
    cmds.columnLayout()
    cmds.text(label="In and Out Frames")
    cmds.textField()
    cmds.textField()

    # FORMAT
    def printNewMenuItem(item):
        video_format = item
        print video_format

    cmds.columnLayout()
    cmds.text(label="Video Format")
    cmds.optionMenu(label='Format', cc=printNewMenuItem)
    cmds.menuItem(label="h.264")
    cmds.menuItem(label="h.265")
    cmds.menuItem(label="Webm AV9")

    # OUTPUT LOCATION
    cmds.columnLayout()
    #cmds.text(label="Output Location")
    OutputLocation = cmds.optionVar(q='playblastFFmpeg_outputLoc')
    #outputLocationText = cmds.textField(text=OutputLocation, ec=save_settings, aie=True, w=300)
    outputLocationText = cmds.textFieldButtonGrp(label="Video Output Location", buttonLabel="Set Output Location", text=OutputLocation, cc=save_settings, bc="cmds.fileDialog2(ds=2)")
    cmds.button(label="Output Location")
    cmds.setParent('..')

    # EXPORT PLAYBLAST
    cmds.columnLayout()
    cmds.button(label="Export Playblast", h=50)

    cmds.showWindow(winID)


create_window()
