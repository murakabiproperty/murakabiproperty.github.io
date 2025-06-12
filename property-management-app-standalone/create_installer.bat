@echo off
echo ========================================
echo Property Management System Installer Builder
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

echo Step 1: Creating application icon from your website logo...
python create_icon.py
if errorlevel 1 (
    echo ERROR: Failed to create application icon!
    pause
    exit /b 1
)

echo.
echo Step 2: Building application executable...
python build_installer.py
if errorlevel 1 (
    echo ERROR: Failed to build application!
    pause
    exit /b 1
)

echo.
echo Step 3: Checking for Inno Setup...
if not exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    if not exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
        echo WARNING: Inno Setup 6 not found!
        echo.
        echo Please download and install Inno Setup 6 from:
        echo https://jrsoftware.org/isdl.php
        echo.
        echo After installation, run this script again.
        pause
        exit /b 1
    )
    set "INNO_SETUP=%ProgramFiles%\Inno Setup 6\ISCC.exe"
) else (
    set "INNO_SETUP=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
)

echo Found Inno Setup at: %INNO_SETUP%

echo.
echo Step 4: Creating installer with Inno Setup...
echo Using simple installer script (no optional files required)...

"%INNO_SETUP%" installer_script_simple.iss
if errorlevel 1 (
    echo ERROR: Simple installer failed! Trying advanced installer...
    "%INNO_SETUP%" installer_script.iss
    if errorlevel 1 (
        echo ERROR: Both installer scripts failed!
        echo Check that all required files exist:
        echo - installer_files\app\PropertyManager.exe
        echo - AIRTABLE_INTEGRATION_GUIDE.md
        echo - USER_MANUAL.md
        echo - airtable_config.py
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo SUCCESS! Installer created successfully!
echo ========================================
echo.
echo The installer file is: PropertyManagementSystem_Setup.exe
echo.
echo 🎨 Features included:
echo   - Your website logo as the application icon
echo   - Desktop shortcut created by default
echo   - Professional installer wizard with your branding
echo.
echo You can now distribute this installer to users.
echo Users just need to double-click the installer to set up everything automatically!
echo.
echo NOTE: If you want the advanced installer with Airtable configuration wizard,
echo      make sure all optional files exist and use installer_script.iss directly.
echo.
pause 