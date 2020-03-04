import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

winID = 'aurWindow'

# SCENE
def AurTDSceneSetup(self):
	if not cmds.ls("_GEO_"):
		cmds.group(em=True, n="_GEO_")
	if not cmds.ls("_LGT_"):
		cmds.group(em=True, n="_LGT_")
	if not cmds.ls("_REFS_"):
		cmds.group(em=True, n="_REFS_")

	cmds.setAttr('_GEO_.useOutlinerColor', True)
	cmds.setAttr('_GEO_.outlinerColor', .1,.7,.7)
	cmds.setAttr('_LGT_.useOutlinerColor', True)
	cmds.setAttr('_LGT_.outlinerColor', .8,.8,.2)
	cmds.setAttr('_REFS_.useOutlinerColor', True)
	cmds.setAttr('_REFS_.outlinerColor', .5,.6,.8)

# RIGGING
def AurTDBlendshapeOriginal(self):

	SelectedObj = cmds.ls(sl=True, sn=True)

	if SelectedObj:
		#get material
		SelectedObj = cmds.ls(sl = True, dag = True, s = True)
		shadeEng = cmds.listConnections(SelectedObj , type="shadingEngine")
		SelectedObjMaterial = cmds.ls(cmds.listConnections(shadeEng ), materials = True)
		print SelectedObjMaterial[0]
		#duplicate object and switch it to original shape node
		cmds.duplicate(n="{}Blendshape".format(SelectedObj[0]))
		cmds.setAttr("{}BlendshapeShapeOrig.intermediateObject".format(SelectedObj[0]), 0)
		cmds.delete("{}BlendshapeShape".format(SelectedObj[0]))
		#assign material
		cmds.select('{}Blendshape'.format(SelectedObj[0]))
		cmds.select(SelectedObjMaterial[0], add=True)
		SelectedObjShaderGroup = cmds.listConnections(SelectedObjMaterial[0])
		print SelectedObjShaderGroup[0]
		cmds.hyperShade( assign='aiStandardSurface1SG')
		#unlock translate attrs
		axis = ['X', 'Y', 'Z']
		attrs = ['translate', 'rotate', 'scale']
		for ax in axis:
			for attr in attrs:
				cmds.setAttr('{}Blendshape'.format(SelectedObj[0])+'.'+attr+ax, lock=0)



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

	    #TODO try point constraint
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

def AurTDEndJointOrient(self):
    tempSel_jointArray = cmds.ls( type=('joint'), sl=True)
    
    for i in tempSel_jointArray:
        
        cmds.select(i)
        tempSel_parent = cmds.ls( sl=True)
        
        tempSel_child = cmds.listRelatives( type='joint')
       
        if not tempSel_child:
            cmds.joint( edit=True, o=(0,0,0));


# CONTROLS
def AurTDnurbsCircle(self):
	#TODO update to add Pivot group hierarchy
	cmds.circle(name='CircleNURB_#')
	cmds.bakePartialHistory()
	
def AurTDnurbsCube(self):
	cmds.group(em=True, n='PIVOT_Cube')
	cmds.curve( d=1, p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5), (.5, -0.5, -0.5), (.5, .5, -0.5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (.5, -0.5, -0.5), (.5, .5, -0.5), (.5, .5, .5), (-0.5, .5, .5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5), (.5, -0.5, .5)], n='CTRL_Cube');
	cmds.parent('CTRL_Cube', 'PIVOT_Cube')
	#cmds.select('CTRL_Cube')
	cmds.rename('CTRL_Cube', 'CTRL_Cube#')
	cmds.rename('PIVOT_Cube', 'PIVOT_Cube#')
# RENDERING
def AurTDOCIOoff(self):
    cmds.colorManagementPrefs( e=True, cfe=False );
    
def AurTDOCIOon(self):
    cmds.colorManagementPrefs( e=True, cfe=True );

def AurTDEndFrameRange(self):
	endFrame = cmds.playbackOptions(q=True, maxTime=1)
	cmds.setAttr('defaultRenderGlobals.endFrame', endFrame)
	print ("set Render Range end frame to " + str(endFrame))
    
# MODELLING
def AurTDSafeDelHistory(self):
    tempSel_SafeDelHistory = cmds.ls( sl=True)
    cmds.bakePartialHistory( tempSel_SafeDelHistory,prePostDeformers=True )

def AurTDString(self):
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
def AurTDOverscan(self):
	view = OpenMayaUI.M3dView.active3dView()
	cam = OpenMaya.MDagPath()
	view.getCamera(cam)
	camPath = cam.fullPathName()
	#if cmds.camera(camPath, q=True, displayResolution=1):
	cmds.camera(camPath, e=True, overscan=1.05)
	print ("set current camera's overscan to 1.05")



# CREATE WINDOW
#def main():
hv=25
wv=100

if cmds.window(winID, exists=True):
	cmds.deleteUI(winID)

cmds.window( winID, title = 'Aur TD Window')
cmds.columnLayout( adjustableColumn=True,  rowSpacing=5, width=200 )

cmds.frameLayout( label='Scene', labelAlign='top' )
cmds.button( label = 'Scene Setup', ann = 'Set up scene groups with outliner colours', command=AurTDSceneSetup)



cmds.frameLayout( label='Rigging', labelAlign='top' )
cmds.button( label = 'Original Blendshape', ann = 'Get the original shape without blendshapes or joint deformation', command=AurTDBlendshapeOriginal)
cmds.button( label = 'Joint Controllers', ann = 'Make a controller for each selected joint', command=AurTDJointController)
cmds.button( label = 'End Joint Orient', ann = 'Orient the end joint of each chain correctly', command=AurTDEndJointOrient)

cmds.frameLayout( label='Controls', labelAlign='top' )
cmds.button( label = 'Nurbs Circle', ann = 'Makes a NURBS circle', command=AurTDnurbsCircle)
cmds.button( label = 'Nurbs Cube', ann = 'Makes a NURBS cube', command=AurTDnurbsCube)

cmds.frameLayout( label='Rendering', labelAlign='top' )
cmds.rowColumnLayout("uiMenuRow3", numberOfColumns=2, h=hv)
cmds.button( label = 'OCIO Off', h = hv,w = wv, ann = 'Switch to default Maya colour management', command=AurTDOCIOoff, bgc=[.8,.5,.5])
cmds.button( label = 'OCIO On', h = hv,w = wv, ann = 'Switch to OCIO colour management', command=AurTDOCIOon, bgc=[.5,.7,.5])
cmds.setParent('..')
#cmds.frameLayout()
#cmds.button( label = 'OCIO Off', ann = 'Switch to default Maya colour management', command=AurTDOCIOoff)
#cmds.button( label = 'OCIO On', ann = 'Switch to OCIO colour management', command=AurTDOCIOon)
cmds.button( label = 'Set Frame End same as Timeline', ann = 'Set the End Frame for rendering to the End Frame of the timeline', command=AurTDEndFrameRange)

cmds.frameLayout( label='Modelling', labelAlign='top' )
cmds.button( label = 'Delete non-deformer history', ann = 'Delete non-deformer history', command=AurTDSafeDelHistory)
cmds.button( label = 'String _WIP_', ann = 'Make string between two selected objects', command=AurTDString, bgc=[.5,.5,.6])

cmds.frameLayout( label='Cameras', labelAlign='top' )
cmds.button( label = 'Overscan to 1.05', ann = "Set current camera's Overscan to 1.05", command=AurTDOverscan)

cmds.rowColumnLayout("uiMenuRow", adjustableColumn=True)


#allowedAreas = ['right', 'left']
#cmds.dockControl( "AurTD", area='left',content=winID, allowedArea=allowedAreas )

cmds.showWindow()
