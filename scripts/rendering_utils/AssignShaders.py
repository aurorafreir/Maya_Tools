import pymel.core as pm

def assign_shader(shader="surface"):
    sel = pm.selected()
    if not sel:
        raise Exception("Nothing selected!")
    
    if "surface" in shader:
        ai_shader = pm.rendering.shadingNode("aiStandardSurface", asShader=True)
    elif "hair" in shader:
        ai_shader = pm.rendering.shadingNode("aiStandardHair", asShader=True)
    elif "volume" in shader:
        ai_shader = pm.rendering.shadingNode("aiStandardVolume", asShader=True)
        
    for obj in sel:
        pm.select(obj)
        pm.hyperShade(assign=ai_shader)
        print(f"assigned {ai_shader} to {obj}")
    pm.select(sel)
        
assign_shader()
