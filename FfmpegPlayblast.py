import os
import maya.cmds as cmds

def printFormatMenuItem(item):
    menu_item = item
    print menu_item

format_list = ['libx264', 'libx265', 'libvpx-vp9']

def printEncodeMenuItem(*args):
    selected_encode_format = cmds.optionMenu('selected_encode_format', q=True, sl=1)
    #print cmds.optionMenu('selected_encode_format', q=True, sl=1) - 1
    encode_format = format_list[selected_encode_format-1]
    print encode_format
    return encode_format

# CREATE WINDOW
def create_window():
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
    # Set the in and out frames for the playblast
    cmds.columnLayout()
    cmds.text(label="")
    cmds.text(label="In and Out Frames")
    inframe = cmds.optionVar(q="playblastFFmpeg_inframe")
    set_inframe = cmds.textField(text=inframe, cc=save_settings)
    outframe = cmds.optionVar(q="playblastFFmpeg_outframe")
    set_outframe = cmds.textField(text=outframe, cc=save_settings)

    # VIDEO FORMAT
    cmds.columnLayout()
    cmds.text(label="")
    cmds.text(label="")
    cmds.optionMenu('selected_video_format', label='Format', cc=printFormatMenuItem)
    cmds.menuItem('ext', label="use extension")
    #cmds.menuItem('mov', label="mov")
    #cmds.menuItem('mp4', label="mp4")
    #cmds.menuItem('webm', label="Webm")

    # ENCODE FORMAT
    # Set the video encode format
    cmds.columnLayout()
    cmds.optionMenu('selected_encode_format', label='Encoder', cc=printEncodeMenuItem)
    cmds.menuItem('libx264', label="(mov/mp4) h.264")
    cmds.menuItem('libx265', label="(mov/mp4) h.265/HEVC")
    cmds.menuItem('libvpx-vp9', label="(Webm) AV9")

    def get_video_output_path(*args):
        file_path = cmds.fileDialog2()[0]
        cmds.textFieldButtonGrp('VideoOutputLoc', e=1, text=file_path)
        save_settings()

    # OUTPUT LOCATION
    # Sets output location for playblast file and ffmpeg file
    cmds.columnLayout()
    OutputLocation = cmds.optionVar(q='playblastFFmpeg_outputLoc')
    outputLocationText = cmds.textFieldButtonGrp('VideoOutputLoc', label="Video Output Location", buttonLabel="Set Output Location", text=OutputLocation, cc=save_settings, bc=get_video_output_path)
    cmds.setParent('..')

    # EXPORT PLAYBLAST
    cmds.columnLayout()
    cmds.button(
        label="Export Playblast",
        h=50,
        c="ffmpeg_playblast(cmds.optionVar(q='playblastFFmpeg_resolutionx'), cmds.optionVar(q='playblastFFmpeg_resolutiony'), cmds.optionVar(q='playblastFFmpeg_inframe'), cmds.optionVar(q='playblastFFmpeg_outframe'), cmds.optionVar(q='playblastFFmpeg_outputLoc'))")

    cmds.showWindow(winID)

    selected_video_format = cmds.optionMenu('selected_video_format', q=True, value=True)
    selected_encode_format = cmds.optionMenu('selected_encode_format', q=True, value=True)
    selected_output_location = cmds.textFieldButtonGrp('VideoOutputLoc', q=True, text=True)
    return ffmpegLocation, selected_video_format, selected_output_location
create_window()


def ffmpeg_playblast(resolutionx, resolutiony, inframe, outframe, exportlocation):
    ffmpegLocation, video_format, output_location = create_window()
    encode_format = printEncodeMenuItem()
    print encode_format
    print video_format
    #print os.path.splitext(output_location)[0]
    #print os.path.splitext(output_location)[1]
    print 'RUNNING COMMAND: "{} -i {} -c:v {} {}_playblast{}"'.format(ffmpegLocation, output_location, encode_format, os.path.split(output_location)[0], os.path.split(output_location)[1])
    #cmds.playblast(st=int(inframe), et=int(outframe), w=int(resolutionx), h=int(resolutiony), f=exportlocation)
    #os.system('"{} -i {} -c:v {} {}_playblast{}"'.format(ffmpegLocation, output_location, encode_format, os.path.split(output_location)[0], os.path.split(output_location)[1]))


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
