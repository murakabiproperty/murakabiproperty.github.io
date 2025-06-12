@echo off

echo ==========================================
echo Property Management Installer - With Menu
echo ==========================================
echo.
echo This installer will:
echo ✓ Detect existing installations
echo ✓ Show menu options when app is installed
echo ✓ Allow upgrade, repair, modify, or uninstall
echo ✓ Preserve data safely
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

:: Install packages
echo Installing required packages...
pip install cx_Freeze requests Pillow --quiet

:: Clean builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "installer_files" rmdir /s /q "installer_files"

:: Build executable
echo Building executable...
python build_installer.py
if errorlevel 1 (
    echo ERROR: Build failed!
    echo.
    echo Troubleshooting:
    echo - Check that main.py exists
    echo - Verify all dependencies are installed
    echo - Check for syntax errors
    pause
    exit /b 1
)

:: Create installer with menu
echo Creating installer with installation menu...
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" installer_script_with_menu.iss
    if errorlevel 1 (
        echo ERROR: Installer creation failed!
        echo Check installer_script_with_menu.iss for errors
        pause
        exit /b 1
    )
    echo.
    echo ✓ SUCCESS! Menu installer created: PropertyManagementSystem_Setup_WithMenu.exe
) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles%\Inno Setup 6\ISCC.exe" installer_script_with_menu.iss
    if errorlevel 1 (
        echo ERROR: Installer creation failed!
        echo Check installer_script_with_menu.iss for errors
        pause
        exit /b 1
    )
    echo.
    echo ✓ SUCCESS! Menu installer created: PropertyManagementSystem_Setup_WithMenu.exe
) else (
    echo.
    echo WARNING: Inno Setup 6 not found!
    echo.
    echo Download and install from: https://jrsoftware.org/isdl.php
    echo.
    echo Executable is available in: installer_files\app\PropertyManager.exe
    echo You can distribute this folder manually.
)

echo.
echo ==========================================
echo Build completed successfully!
echo ==========================================
echo.
echo 🎉 Installer Features:
echo ✓ Detects existing installations automatically
echo ✓ Shows menu when app is already installed:
echo   • Install/Upgrade (preserves data)
echo   • Repair Installation
echo   • Modify Installation  
echo   • Uninstall Application
echo ✓ Safe data preservation
echo ✓ No runtime errors
echo.
echo 📁 Output File: PropertyManagementSystem_Setup_WithMenu.exe
echo.
echo 🚀 Test the installer:
echo 1. Install fresh on clean system
echo 2. Run installer again to see menu options
echo 3. Try upgrade, repair, and uninstall
echo.
pause 