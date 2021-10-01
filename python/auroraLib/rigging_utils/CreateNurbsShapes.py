def create_nurbs_circle(self):
    cmds.group(em=True, n='PIVOT_Circle')
    cmds.circle(name='CTRL_Circle')
    cmds.parent('CTRL_Circle', 'PIVOT_Circle')
    cmds.bakePartialHistory()
    cmds.select('PIVOT_Circle')

def create_nurbs_cube(self):
    cmds.group(em=True, n='PIVOT_Cube')
    cmds.curve(d=1, p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5), (.5, -0.5, -0.5), (.5, .5, -0.5),
                       (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (.5, -0.5, -0.5), (.5, .5, -0.5), (.5, .5, .5),
                       (-0.5, .5, .5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5), (.5, -0.5, .5)],
               n='CTRL_Cube');
    cmds.parent('CTRL_Cube', 'PIVOT_Cube')
    cmds.rename('CTRL_Cube', 'CTRL_Cube#')
    cmds.select('PIVOT_Cube')
    cmds.rename('PIVOT_Cube', 'PIVOT_Cube#')


def create_nurbs_pyramid(self):
    cmds.group(em=True, n='PIVOT_Pyramid')
    cmds.curve(d=1, p=[(-.5, -1, -.5), (.5, -1, -.5), (.5, -1, .5), (-.5, -1, .5), (-.5, -1, -.5), (0, 0, 0),
                       (-.5, -1, .5), (.5, -1, .5), (0, 0, 0), (.5, -1 ,-.5)],
               n='CTRL_Pyramid');
    cmds.parent('CTRL_Pyramid', 'PIVOT_Pyramid')
    cmds.rename('CTRL_Pyramid', 'CTRL_Pyramid#')
    cmds.select('PIVOT_Pyramid')
    cmds.rename('PIVOT_Pyramid', 'PIVOT_Pyramid#')