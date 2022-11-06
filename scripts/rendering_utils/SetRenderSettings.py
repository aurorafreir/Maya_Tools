"""
Trans Rights are Human Rights

Some scripts to set up my scenes for rendering
"""
# SYSTEM IMPORTS

# STANDARD LIBRARY IMPORTS
import pymel.core as pm

# LOCAL APPLICATION IMPORTS


def model_attrs_setter():
    for obj in pm.selected(type=pm.nt.Transform):
        for shape in obj.getShapes():
            shape.aiSubdivType.set(1)
            shape.aiSubdivIterations.set(2)
            shape.useSmoothPreviewForRender.set(0)
