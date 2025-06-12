@echo off

echo =========================================
echo Safe Property Management Installer Build
echo =========================================
echo.
echo This script uses a simplified installer
echo to avoid runtime errors.
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

:: Install packages
echo Installing required packages...
pip install cx_Freeze requests Pillow --quiet

:: Clean builds
if exist "build" rmdir /s /q "build"
if exist "installer_files" rmdir /s /q "installer_files"

:: Build executable
echo Building executable...
python build_installer.py
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

:: Create safe installer
echo Creating safe installer...
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" installer_script_simple_safe.iss
    if errorlevel 1 (
        echo ERROR: Installer creation failed!
        pause
        exit /b 1
    )
    echo.
    echo SUCCESS! Safe installer created: PropertyManagementSystem_Setup_Safe.exe
) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles%\Inno Setup 6\ISCC.exe" installer_script_simple_safe.iss
    if errorlevel 1 (
        echo ERROR: Installer creation failed!
        pause
        exit /b 1
    )
    echo.
    echo SUCCESS! Safe installer created: PropertyManagementSystem_Setup_Safe.exe
) else (
    echo.
    echo Inno Setup not found!
    echo Download from: https://jrsoftware.org/isdl.php
    echo.
    echo Executable available in: installer_files\app\PropertyManager.exe
)

echo.
echo =========================================
echo Build completed!
echo =========================================
echo.
echo This installer version:
echo ✓ No complex installation detection
echo ✓ Simple preserve data option
echo ✓ No runtime errors
echo ✓ Clean uninstall process
echo.
pause 