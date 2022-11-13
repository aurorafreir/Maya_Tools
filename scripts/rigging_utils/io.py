"""
Trans Rights are Human Rights

"""
# SYSTEM IMPORTS
import os

# STANDARD LIBRARY IMPORTS
import pymel.core as pm

# LOCAL APPLICATION IMPORTS
from scripts.rigging_utils import skin_utils
from scripts.rigging_utils import extract_skeleton
import mgear.shifter.io as mgio


# PATHS SETUP
def current_paths() -> [str, str, str, str]:
    filepath = pm.sceneName()
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)

    return filepath, filename, raw_name, extension


def make_dir_if_missing(direc: str) -> None:
    if not os.path.exists(direc):
        os.mkdir(direc)
    return None


def data_dump() -> None:
    filepath, filename, raw_name, extension = current_paths()

    scene_name = f"{raw_name.strip('Guides')[:-1]}"

    data_dir = os.path.join(os.path.dirname(filepath), "data")
    skin_dir = os.path.join(data_dir, raw_name)
    make_dir_if_missing(data_dir)
    make_dir_if_missing(skin_dir)

    # PRECHECK WRITE ACCESS
    required_read_only_files = []
    if not os.access(filepath, os.W_OK):
        required_read_only_files.append(filepath)

    guide_template_export_filepath = os.path.join(data_dir, f"{scene_name}_mGearGuides.sgt")
    if not os.access(guide_template_export_filepath, os.W_OK):
        required_read_only_files.append(guide_template_export_filepath)

    skel_filename = os.path.join(data_dir, f"{scene_name}_Skeleton.ma")
    if not os.access(skel_filename, os.W_OK):
        required_read_only_files.append(skel_filename)

    # Throw an error if any or all export paths are not writeable
    if required_read_only_files:
        ro_files = " \n".join(required_read_only_files)
        pm.displayError(f"files: \n{ro_files} \nnot writeable!")
        return

    pm.saveFile()

    # EXPORT SKIN
    skin_utils.export_skin()

    # EXPORT GUIDES
    if pm.ls("guide"):
        pm.select("guide")
        mgio.export_guide_template(filePath=guide_template_export_filepath)

    # EXPORT SKELETON
    skel_filename = os.path.join(data_dir, f"{scene_name}_Skeleton.ma")
    pm.renameFile(skel_filename)
    extract_skeleton.extract_skeleton()
    pm.saveFile()
    pm.openFile(filepath)

    return None
