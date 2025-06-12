@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Property Management System - Complete Installer Builder
echo ============================================================
echo.
echo This script will:
echo 1. Install required Python packages
echo 2. Create application icon
echo 3. Build standalone executable
echo 4. Create installer with Inno Setup
echo.

:: Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://python.org/
    echo Make sure to add Python to PATH during installation
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Found Python %PYTHON_VERSION%

:: Check if pip is available
echo Checking pip installation...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available!
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)
echo ✓ pip is available

:: Step 1: Install required packages
echo.
echo Step 1/4: Installing required Python packages...
echo ================================================

set PACKAGES=cx_Freeze requests urllib3 certifi charset-normalizer idna Pillow
for %%p in (%PACKAGES%) do (
    echo Installing %%p...
    python -m pip install %%p --quiet --disable-pip-version-check
    if errorlevel 1 (
        echo WARNING: Failed to install %%p, trying with --user flag...
        python -m pip install %%p --user --quiet --disable-pip-version-check
        if errorlevel 1 (
            echo ERROR: Failed to install %%p completely!
            pause
            exit /b 1
        )
    )
    echo ✓ %%p installed successfully
)

:: Step 2: Create application icon
echo.
echo Step 2/4: Creating application icon...
echo =====================================

if exist "create_icon.py" (
    python create_icon.py
    if errorlevel 1 (
        echo WARNING: Failed to create custom icon, using default...
    ) else (
        echo ✓ Application icon created successfully
    )
) else (
    echo WARNING: create_icon.py not found, skipping icon creation...
)

:: Step 3: Build executable
echo.
echo Step 3/4: Building standalone executable...
echo ==========================================

:: Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "installer_files" rmdir /s /q "installer_files"
echo ✓ Cleaned previous build artifacts

:: Build the executable
python build_installer.py
if errorlevel 1 (
    echo ERROR: Failed to build executable!
    echo.
    echo Troubleshooting tips:
    echo - Make sure main.py exists
    echo - Check that all dependencies are installed
    echo - Verify no syntax errors in main.py
    pause
    exit /b 1
)
echo ✓ Executable built successfully

:: Step 4: Create installer
echo.
echo Step 4/4: Creating installer with Inno Setup...
echo ==============================================

:: Check for Inno Setup
set "INNO_SETUP="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    set "INNO_SETUP=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    set "INNO_SETUP=%ProgramFiles%\Inno Setup 6\ISCC.exe"
) else (
    echo.
    echo WARNING: Inno Setup 6 not found!
    echo.
    echo Please download and install Inno Setup 6 from:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo After installation, run this script again.
    echo.
    echo Alternatively, you can create the installer manually using:
    echo - installer_files/app/PropertyManager.exe (main executable)
    echo - Supporting files in installer_files/
    echo.
    pause
    goto :skip_installer
)

echo ✓ Found Inno Setup at: !INNO_SETUP!

:: Try simple installer first
if exist "installer_script_simple.iss" (
    echo Creating installer using simple script...
    "!INNO_SETUP!" installer_script_simple.iss
    if not errorlevel 1 (
        echo ✓ Simple installer created successfully!
        goto :success
    )
    echo WARNING: Simple installer failed, trying advanced script...
)

:: Try advanced installer
if exist "installer_script.iss" (
    echo Creating installer using advanced script...
    "!INNO_SETUP!" installer_script.iss
    if not errorlevel 1 (
        echo ✓ Advanced installer created successfully!
        goto :success
    )
    echo ERROR: Advanced installer also failed!
)

echo ERROR: All installer scripts failed!
echo Check that the following files exist:
echo - installer_files\app\PropertyManager.exe
echo - installer_script_simple.iss or installer_script.iss
pause
exit /b 1

:success
echo.
echo ============================================================
echo SUCCESS! Complete build process finished!
echo ============================================================
echo.
echo 🎉 Your installer is ready!
echo.
echo 📁 Files created:
if exist "PropertyManagementSystem_Setup.exe" (
    echo    ✓ PropertyManagementSystem_Setup.exe
)
if exist "PropertyManagementSystem_Setup_Simple.exe" (
    echo    ✓ PropertyManagementSystem_Setup_Simple.exe
)
echo    ✓ installer_files/ (executable and support files)
echo.
echo 🚀 You can now distribute the installer to users!
echo.
echo 📋 Next steps:
echo    1. Test the installer on a clean Windows machine
echo    2. Distribute the .exe file to users
echo    3. Users can install by double-clicking the .exe
echo.
goto :end

:skip_installer
echo.
echo ============================================================
echo Build completed (without installer)
echo ============================================================
echo.
echo ✓ Executable built successfully in installer_files/app/
echo ⚠ Installer creation skipped (Inno Setup not found)
echo.
echo You can still distribute the files manually:
echo - Copy the entire installer_files/app/ folder to target machines
echo - Run PropertyManager.exe from the app folder
echo.

:end
echo Press any key to exit...
pause >nul 