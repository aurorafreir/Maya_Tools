"""
A script to automatically create some shaders and apply them to selected objects
"""
# SYSTEM IMPORTS

# STANDARD LIBRARY IMPORTS
import pymel.core as pm

# LOCAL APPLICATION IMPORTS


def assign_shader(shader: str = "surface") -> None:
    sel = pm.selected()
    if not sel:
        raise Exception("Nothing selected!")

    ai_shader_type = "aiStandardSurface"
    if "hair" in shader:
        ai_shader_type = "aiStandardHair"
    if "volume" in shader:
        ai_shader_type = "aiStandardVolume"

    ai_shader = pm.rendering.shadingNode(ai_shader_type, asShader=True)

    for obj in sel:
        pm.select(obj)
        pm.hyperShade(assign=ai_shader)
        print(f"assigned {ai_shader} to {obj}")
    pm.select(sel)

    return None
