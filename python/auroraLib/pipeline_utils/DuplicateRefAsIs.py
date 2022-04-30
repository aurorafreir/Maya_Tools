"""
Duplicates a reference and makes sure the new one matches the currently selected one
Currently doesn't duplicate animation curves, and needs a bit of cleanup
"""

import pymel.core as pm

def reference_dup_as_is():
    selected_object = pm.selected()
    
    if not selected_object:
        raise Exception("Nothing selected!")
    
    ref_object = selected_object[0]
    
    if ":" not in ref_object.name():
        raise Exception("First selected object isn't referenced!")
        
    ref_name = ref_object.name().split(":")[0]
    #print(ref_name)
    ref_path = pm.referenceQuery(ref_object, filename=True)
    #print(ref_path)
    
    newnodes = pm.createReference(ref_path, 
          namespace=ref_path.replace("\\", "/").split("/")[-1].split(".ma")[0], returnNewNodes=True)
    #print([x.type() for x in newnodes])
    
    new_ref_name = newnodes[0].split(":")[0]
    print(ref_name,  new_ref_name)
    
    affect_objects = [x for x in newnodes if x.type() in ["transform", "locator"]]
    #print(affect_objects)
    
    for new_obj in affect_objects:
        new_obj_attrs = new_obj.listAttr(keyable=True)
        #print([x.name().split(":")[-1] for x in new_obj_attrs])
        for attr in new_obj_attrs:
            #print(attr, pm.getAttr(f"{ref_name}:{attr.name().split(':')[-1]}"))
            attr.set(pm.getAttr(f"{ref_name}:{attr.name().split(':')[-1]}"))
        
    pm.select([x.replace(ref_name, new_ref_name) for x in selected_object])
    
reference_dup_as_is()
