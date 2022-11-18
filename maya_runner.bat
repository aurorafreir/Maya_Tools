@ECHO OFF

:: Gets this script's running directory
set SCRIPT_DIR=%~dp0

set PYTHONPATH=%SCRIPT_DIR%;
set MAYA_MODULE_PATH=%SCRIPT_DIR%mgear_4.0.9/release;
set MAYA_PLUG_IN_PATH=%SCRIPT_DIR%plugins
set XBMLANGPATH=%SCRIPT_DIR%icons/%B
set MAYA_SHELF_PATH=%SCRIPT_DIR%shelves

set MGEAR_SHIFTER_COMPONENT_PATH="%SCRIPT_DIR%/mGearScripts/Components/"

:: Actually open maya
set KEY_NAME="HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\Maya\2022\Setup\InstallPath"
set VALUE_NAME=MAYA_INSTALL_LOCATION

FOR /F "usebackq tokens=2*" %%A IN (`REG QUERY %KEY_NAME% /v %VALUE_NAME% 2^>nul`) DO (
    set ValueName=%%A
    set ValueType=%%B
    set ValueValue=%%C
)

set MAYA_DIR_PATH="%ValueType%"
cd "%MAYA_DIR_PATH%/bin"
start maya.exe

:: Close the terminal window after opening Maya
exit
