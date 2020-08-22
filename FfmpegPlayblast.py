# TODO
# ffmpeg location /media/aurora/gdrive/Apps/ffmpeg.exe
# output location
# // send commands to CLI
# in/out frames
# resolution
# format/encoder
# actual playblast

# os.system('gnome-terminal && cd ~/Downloads && ffmpeg -i video0.mp4 video1.mp4')

def printFormatMenuItem(item):
    video_format = item
    print video_format

def ffmpeg_playblast(resolutionx, resolutiony, inframe, outframe, exportlocation):
    print resolutionx
    print resolutiony
    print inframe
    print outframe
    cmds.playblast(st=int(inframe), et=int(outframe), w=int(resolutionx), h=int(resolutiony), f=exportlocation)

# CREATE WINDOW
def create_window():
    import maya.cmds as cmds
    from functools import partial
    import os

    if not cmds.optionVar(q='playblastFFmpeg_ffmpegLoc'):
        cmds.optionVar(sv=('playblastFFmpeg_ffmpegLoc', ''))
    if not cmds.optionVar(q='playblastFFmpeg_outputLoc'):
        cmds.optionVar(sv=('playblastFFmpeg_outputLoc', '/movies/playblast.mov'))
    if not cmds.optionVar(q='playblastFFmpeg_resolutionx'):
        cmds.optionVar(sv=('playblastFFmpeg_resolutionx', 1920))
    if not cmds.optionVar(q='playblastFFmpeg_resolutiony'):
        cmds.optionVar(sv=('playblastFFmpeg_resolutiony', 1080))
    if not cmds.optionVar(q='playblastFFmpeg_inframe'):
        cmds.optionVar(sv=('playblastFFmpeg_inframe', 0))
    if not cmds.optionVar(q='playblastFFmpeg_outframe'):
        cmds.optionVar(sv=('playblastFFmpeg_outframe', 100))


    winID = 'playblastFFmpeg'
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)
    cmds.window(winID, title='Playblast FFmpeg')

    def save_settings(*args):
        if cmds.textFieldButtonGrp('ffmpegLoc', q=True, text=True):
            cmds.optionVar(sv=('playblastFFmpeg_ffmpegLoc', cmds.textFieldButtonGrp('ffmpegLoc', q=True, text=True)))
        if cmds.textFieldButtonGrp(outputLocationText, q=True, text=True):
            cmds.optionVar(sv=('playblastFFmpeg_outputLoc', cmds.textFieldButtonGrp('VideoOutputLoc', q=True, text=True)))
        cmds.optionVar(sv=('playblastFFmpeg_resolutionx', cmds.textField(set_resolutionx, q=True, text=True)))
        cmds.optionVar(sv=('playblastFFmpeg_resolutiony', cmds.textField(set_resolutiony, q=True, text=True)))
        cmds.optionVar(sv=('playblastFFmpeg_inframe', cmds.textField(set_inframe, q=True, text=True)))
        cmds.optionVar(sv=('playblastFFmpeg_outframe', cmds.textField(set_outframe, q=True, text=True)))

    def get_ffmpeg_path(*args):
        file_path = cmds.fileDialog2(fm=1)[0]
        cmds.textFieldButtonGrp('ffmpegLoc', e=1, text=file_path)
        save_settings()

    # FFMPEG LOCATION
    cmds.columnLayout(w=300, rs=5)
    ffmpegLocation = cmds.optionVar(q='playblastFFmpeg_ffmpegLoc')
    ffmpegLocationText = cmds.textFieldButtonGrp('ffmpegLoc', label='FFmpeg Location', buttonLabel='FFmpeg Location', text=ffmpegLocation, cc=save_settings, bc=get_ffmpeg_path)
    #cmds.button(label="open FFmpeg")
    cmds.setParent('..')

    # RESOLUTION
    cmds.columnLayout()
    cmds.text(label="")
    cmds.text(label="Video Resolution")
    resolutionx = cmds.optionVar(q='playblastFFmpeg_resolutionx')
    set_resolutionx = cmds.textField(text=resolutionx, cc=save_settings)
    resolutiony = cmds.optionVar(q='playblastFFmpeg_resolutiony')
    set_resolutiony = cmds.textField(text=resolutiony, cc=save_settings)

    # IN/OUT
    cmds.columnLayout()
    cmds.text(label="")
    cmds.text(label="In and Out Frames")
    inframe = cmds.optionVar(q="playblastFFmpeg_inframe")
    set_inframe = cmds.textField(text=inframe, cc=save_settings)
    outframe = cmds.optionVar(q="playblastFFmpeg_outframe")
    set_outframe = cmds.textField(text=outframe, cc=save_settings)

    # FORMAT
    cmds.columnLayout()
    cmds.text(label="")
    cmds.text(label="")
    cmds.optionMenu(label='Format', cc=printFormatMenuItem)
    cmds.menuItem(label="mov h.264")
    cmds.menuItem(label="mov h.265")
    cmds.menuItem(label="Webm AV9")

    def get_video_output_path(*args):
        file_path = cmds.fileDialog2()[0]
        cmds.textFieldButtonGrp('VideoOutputLoc', e=1, text=file_path)
        save_settings()

    # OUTPUT LOCATION
    cmds.columnLayout()
    OutputLocation = cmds.optionVar(q='playblastFFmpeg_outputLoc')
    outputLocationText = cmds.textFieldButtonGrp('VideoOutputLoc', label="Video Output Location", buttonLabel="Set Output Location", text=OutputLocation, cc=save_settings, bc=get_video_output_path)
    #cmds.button(label="Output Location")
    cmds.setParent('..')

    # EXPORT PLAYBLAST
    cmds.columnLayout()
    cmds.button(
        label="Export Playblast",
        h=50,
        c="ffmpeg_playblast(cmds.optionVar(q='playblastFFmpeg_resolutionx'), cmds.optionVar(q='playblastFFmpeg_resolutiony'), cmds.optionVar(q='playblastFFmpeg_inframe'), cmds.optionVar(q='playblastFFmpeg_outframe'), cmds.optionVar(q='playblastFFmpeg_outputLoc'))")

    cmds.showWindow(winID)
create_window()


def clearOptionVars():
    cmds.optionVar(rm='playblastFFmpeg_ffmpegLoc')
    cmds.optionVar(rm='playblastFFmpeg_outputLoc')
    cmds.optionVar(rm='playblastFFmpeg_outframe')
    #print cmds.optionVar(q='playblastFFmpeg_outframe')
    cmds.optionVar(rm='playblastFFmpeg_inframe')
    cmds.optionVar(rm='playblastFFmpeg_resolutionx')
    cmds.optionVar(rm='playblastFFmpeg_resolutiony')
    #print cmds.optionVar(q='playblastFFmpeg_ffmpegLoc')
    print "cleared Option Vars"
#clearOptionVars()
