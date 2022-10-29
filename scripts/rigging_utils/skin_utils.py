"""
Trans Rights are Human Rights

A collection of skinning utilities that I use for my personal work.
"""
# SYSTEM IMPORTS
import os

# STANDARD LIBRARY IMPORTS
import pymel.core as pm
import maya.cmds as cmds
import mgear.core.skin as skin
import ngSkinTools2.api as ngst_api

# LOCAL APPLICATION IMPORTS


def current_paths() -> [str, str, str, str]:
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)

    return filepath, filename, raw_name, extension


def make_dir_if_missing(direc: str) -> None:
    if not os.path.exists(direc):
        os.mkdir(direc)
    return None


def export_skin():
    filepath, filename, raw_name, extension = current_paths()
    
    data_dir = os.path.join(os.path.dirname(filepath), "data")
    skin_dir = os.path.join(data_dir, raw_name)
    make_dir_if_missing(data_dir)
    make_dir_if_missing(skin_dir)

    skin_clusters = pm.ls(type="skinCluster")
    if skin_clusters:
        for i in skin_clusters:
            mesh = i.outputGeometry.listConnections()[0]
            skin_path = os.path.join(skin_dir, f"{mesh.name()}.jSkin")
            skin.exportSkin(filePath=skin_path, objs=[mesh])

        for i in pm.ls(type="ngst2SkinLayerData"):
            try:
                mesh = i.skinCluster.listConnections()[0].outputGeometry.listConnections()[0]
                output_file_name = os.path.join(skin_dir, f"ngskin_{mesh}.json")
                ngst_api.export_json(i.name(), file=output_file_name)
                pm.displayInfo(f"Exported {i.name()} as {output_file_name}")
            except:
                pass

    else:
        print("No Skinclusters in scene!")
    
def import_skin():
    filepath, filename, raw_name, extension = current_paths()

    data_dir = os.path.join(os.path.dirname(filepath), "data")
    skin_dir = os.path.join(data_dir, raw_name)

    for file_name in os.listdir(skin_dir):
        try:
            if file_name.endswith(".jSkin"):
                mesh_name = file_name.split(".jSkin")[0]
                skin.importSkin(os.path.join(skin_dir, file_name), [mesh_name])
                print(f"# Imported skin data for {mesh_name}")
            if file_name.startswith("ngskin_"):
                mesh_name = file_name.split("ngskin_")[1].split(".json")[0]

                config = ngst_api.InfluenceMappingConfig()
                config.use_distance_matching = True
                config.use_name_matching = False

                ngst_api.import_json(
                    mesh_name,
                    file=os.path.join(skin_dir, file_name),
                    vertex_transfer_mode=ngst_api.VertexTransferMode.vertexId,
                    influences_mapping_config=config,
                )
                print(f"# Imported ngskin data for {mesh_name}")
        except:
            pass

    pass
