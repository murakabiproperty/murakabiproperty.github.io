@echo off

echo ========================================
echo Quick Property Management Installer
echo ========================================
echo.

:: Quick install required packages
pip install cx_Freeze requests Pillow --quiet

:: Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "installer_files" rmdir /s /q "installer_files"

:: Build executable
python build_installer.py

:: Create installer if Inno Setup is available
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" installer_script_simple.iss
    echo.
    echo SUCCESS! Installer created: PropertyManagementSystem_Setup_Simple.exe
) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles%\Inno Setup 6\ISCC.exe" installer_script_simple.iss
    echo.
    echo SUCCESS! Installer created: PropertyManagementSystem_Setup_Simple.exe
) else (
    echo.
    echo Executable built in: installer_files\app\PropertyManager.exe
    echo Install Inno Setup from https://jrsoftware.org/isdl.php to create installer
)

pause 