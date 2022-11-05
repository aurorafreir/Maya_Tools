#! /bin/bash

SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ) # Gets this script's running directory

export PYTHONPATH="$SCRIPT_DIR":
export MAYA_MODULE_PATH="$SCRIPT_DIR/mgear_4.10.0/Release"
export MAYA_PLUG_IN_PATH="$SCRIPT_DIR/plugins"
export XBMLANGPATH="$SCRIPT_DIR/icons"
export MAYA_SHELF_PATH="$SCRIPT_DIR/shelves"

maya