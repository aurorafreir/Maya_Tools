import maya.cmds as cmds

winID = 'aurWindow'

# RIGGING
def aurTD_JointController(self):
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

def aurTD_EndJointOrient(self):
    tempSel_jointArray = cmds.ls( type=('joint'), sl=True)
    
    for i in tempSel_jointArray:
        
        cmds.select(i)
        tempSel_parent = cmds.ls( sl=True)
        
        tempSel_child = cmds.listRelatives( type='joint')
       
        if not tempSel_child:
            cmds.joint( edit=True, o=(0,0,0));


# CONTROLS
def aurTD_nurbsCircle(self):
	cmds.circle(name='CircleNURB_#')
	cmds.bakePartialHistory()
	
def aurTD_nurbsCube(self):
	cmds.curve( d=1, p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5), (.5, -0.5, -0.5), (.5, .5, -0.5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (.5, -0.5, -0.5), (.5, .5, -0.5), (.5, .5, .5), (-0.5, .5, .5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5), (.5, -0.5, .5)], n='NURBS_Cube#');


# RENDERING
def aurTD_OCIOoff(self):
    cmds.colorManagementPrefs( e=True, cfe=False );
    
def aurTD_OCIOon(self):
    cmds.colorManagementPrefs( e=True, cfe=True );


# CREATE WINDOW
def main():
    if cmds.window(winID, exists=True):
    	cmds.deleteUI(winID)
    
    cmds.window( winID, title = 'Aur TD Window')
    cmds.columnLayout( adjustableColumn=True,  rowSpacing=5, width=200 )
    
    cmds.frameLayout( label='Rigging', labelAlign='top' )
    cmds.button( label = 'Joint Controllers', ann = 'Make a controller for each selected joint', command=aurTD_JointController)
    cmds.button( label = 'End Joint Orient', ann = 'Orient the end joint of each chain correctly', command=aurTD_JointController)
    
    cmds.frameLayout( label='Controls', labelAlign='top' )
    cmds.button( label = 'Nurbs Circle', ann = 'Makes a NURBS circle', command=aurTD_nurbsCircle)
    cmds.button( label = 'Nurbs Cube', ann = 'Makes a NURBS cube', command=aurTD_nurbsCube)
    
    
    cmds.frameLayout( label='Rendering', labelAlign='top' )
    cmds.button( label = 'OCIO Off', ann = 'Switch to default Maya colour management', command=aurTD_OCIOoff)
    cmds.button( label = 'OCIO On', ann = 'Switch to OCIO colour management', command=aurTD_OCIOon)
    allowedAreas = ['right', 'left']
    cmds.dockControl( "AurTD", area='left', content=winID, allowedArea=allowedAreas )
    
    cmds.showWindow()
    
if __name__=="__main__":
        cmds.evalDeferred(main())
        
