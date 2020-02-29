import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

winID = 'aurWindow'

#TODO fix variable names to fit PEP8 var conventions

# RIGGING
def AurTDJointController(self):
	# Makes a square NURBS controller and parent constraints the joints to the controllers
	# Makes an array of the selected joints
	tempSel_jointArray = cmds.ls( type=('joint'), sl=True)
	
	for i in tempSel_jointArray:
	    
	    # Selects current joint and sets it as variable tempSel_Parent
	    cmds.select(i)
	    tempSel_parent = cmds.ls( sl=True)
	    
	    # Selects child joint and sets it as variable tempSel_AimAt
	    tempSel_aimAt = cmds.listRelatives( type='joint')
	    
	    # Creates square NURBS curve and deletes it's history
	    cmds.select( d=True );
	    cmds.curve( d=1, p=[(-0.5, 0, .5), (-0.5, 0, -.5), (.5, 0, -.5), (.5, 0, .5), (-0.5, 0, .5)], name='CTRL_' + i);
	    cmds.rotate( 0,0,90);
	    cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0)
	    cmds.bakePartialHistory()
	    
	    # Makes a group and makes the controller a child of the PIVOT group
	    cmds.group( em=True, name='PIVOT_' + (i));
	    cmds.parent( 'CTRL_' + (i), 'PIVOT_' + (i));
	    
	    # Makes parent constraint for controller location
	    cmds.parentConstraint( tempSel_parent, 'PIVOT_' + i , mo=False, name='tempParentConstraint' + i);
	    cmds.delete( 'tempParentConstraint' + (i));
	    
	    # Makes aim constraint for controller orientation
	    cmds.aimConstraint( tempSel_aimAt, 'PIVOT_' + i, name='tempAimConstraint' + i);
	    cmds.delete( 'tempAimConstraint' + (i));
	    
	    # Parent constrains the joint to the controller
	    cmds.select( 'CTRL_' + i)
	    cmds.select( (i), add=True)
	    cmds.parentConstraint( name='parentConstraint_' + (i) + '_CTRL_' + i)
	    cmds.select( d=True)

def AurTD_EndJointOrient(self):
    tempSel_jointArray = cmds.ls( type=('joint'), sl=True)
    
    for i in tempSel_jointArray:
        
        cmds.select(i)
        tempSel_parent = cmds.ls( sl=True)
        
        tempSel_child = cmds.listRelatives( type='joint')
       
        if not tempSel_child:
            cmds.joint( edit=True, o=(0,0,0));


# CONTROLS
def AurTD_nurbsCircle(self):
	cmds.circle(name='CircleNURB_#')
	cmds.bakePartialHistory()
	
def AurTD_nurbsCube(self):
	cmds.curve( d=1, p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5), (.5, -0.5, -0.5), (.5, .5, -0.5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (.5, -0.5, -0.5), (.5, .5, -0.5), (.5, .5, .5), (-0.5, .5, .5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5), (.5, -0.5, .5)], n='NURBS_Cube#');


# RENDERING
def AurTD_OCIOoff(self):
    cmds.colorManagementPrefs( e=True, cfe=False );
    
def AurTD_OCIOon(self):
    cmds.colorManagementPrefs( e=True, cfe=True );

def AurTD_EndFrameRange(self):
	endFrame = cmds.playbackOptions(q=True, maxTime=1)
	cmds.setAttr('defaultRenderGlobals.endFrame', endFrame)
	print ("set Render Range end frame to " + str(endFrame))
    
# MODELLING
def AurTD_SafeDelHistory(self):
	tempSel_SafeDelHistory = cmds.ls( sl=True)
	cmds.bakePartialHistory( tempSel_SafeDelHistory,prePostDeformers=True )

def AurTD_String(self):
	selected = cmds.ls(selection=True)

	selected_len = (len(selected))
	#print selected_len

	if len(selected) == 2:
		#todo add check for frozen translations
		for item in selected[:1]:
			rPiv = cmds.xform(item, q=True, rp=True)  # query rotation pivot
			#sPiv = cmds.xform(item, q=True, sp=True)  # query scale pivot

			loc = cmds.spaceLocator(n="wireLocator1")
			cmds.xform(t=rPiv)

		for item in selected[1:]:
			rPiv = cmds.xform(item, q=True, rp=True)  # query rotation pivot
			#sPiv = cmds.xform(item, q=True, sp=True)  # query scale pivot

			loc = cmds.spaceLocator(n="wireLocator2")
			cmds.xform(t=rPiv)

	else:
		print "Two objects required for string"

	#cmds.curve('string_##',)

	#cmds.delete("wireLocator1")
	#cmds.delete("wireLocator2")
# CAMERAS
def AurTD_Overscan(self):
	if cmds.camera('Shot_0050', q=True, displayResolution=1):
		view = OpenMayaUI.M3dView.active3dView()
		cam = OpenMaya.MDagPath()
		view.getCamera(cam)
		camPath = cam.fullPathName()
		cmds.camera(camPath, e=True, overscan=1.05)
		print ("set current camera's overscan to 1.05")

# CREATE WINDOW
#def main():
if cmds.window(winID, exists=True):
	cmds.deleteUI(winID)

cmds.window( winID, title = 'Aur TD Window')
cmds.columnLayout( adjustableColumn=True,  rowSpacing=5, width=200 )

cmds.frameLayout( label='Rigging', labelAlign='top' )
cmds.button( label = 'Joint Controllers', ann = 'Make a controller for each selected joint', command=AurTD_JointController)
cmds.button( label = 'End Joint Orient', ann = 'Orient the end joint of each chain correctly', command=AurTD_JointController)

cmds.frameLayout( label='Controls', labelAlign='top' )
cmds.button( label = 'Nurbs Circle', ann = 'Makes a NURBS circle', command=AurTD_nurbsCircle)
cmds.button( label = 'Nurbs Cube', ann = 'Makes a NURBS cube', command=AurTD_nurbsCube)

cmds.frameLayout( label='Rendering', labelAlign='top' )
cmds.button( label = 'OCIO Off', ann = 'Switch to default Maya colour management', command=AurTD_OCIOoff)
cmds.button( label = 'OCIO On', ann = 'Switch to OCIO colour management', command=AurTD_OCIOon)
cmds.button( label = 'Set Frame End same as Timeline', ann = 'Set the End Frame for rendering to the End Frame of the timeline', command=aurTD_EndFrameRange)

cmds.frameLayout( label='Modelling', labelAlign='top' )
cmds.button( label = 'Delete non-deformer history', ann = 'Delete non-deformer history', command=AurTD_SafeDelHistory)
cmds.button( label = 'String _WIP_', ann = 'Make string between two selected objects', command=AurTD_String)

cmds.frameLayout( label='Cameras', labelAlign='top' )
cmds.button( label = 'Overscan to 1.05', ann = "Set current camera's Overscan to 1.05", command=AurTD_Overscan)

#allowedAreas = ['right', 'left']
#cmds.dockControl( "AurTD", area='left',content=winID, allowedArea=allowedAreas )

cmds.showWindow()
    
#if __name__=="__main__":
        #cmds.evalDeferred(main())
        
