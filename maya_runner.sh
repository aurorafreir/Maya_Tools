#! /bin/bash

SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ) # Gets this script's running directory

export PYTHONPATH="$SCRIPT_DIR":
export MAYA_MODULE_PATH="$SCRIPT_DIR/mgear_4.0.9/release"
export MAYA_PLUG_IN_PATH="$SCRIPT_DIR/plugins"
export XBMLANGPATH="$SCRIPT_DIR/icons/%B"
export MAYA_SHELF_PATH="$SCRIPT_DIR/shelves"

export MGEAR_SHIFTER_COMPONENT_PATH="$SCRIPT_DIR/mGearScripts/Components/"

#export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libffi.so.6"

maya
